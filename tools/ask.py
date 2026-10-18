#!/usr/bin/env python3
"""问题入口：把中文问题变成“英文手册术语 + 候选页 + 原页证据包”。

用法：
    python tools/ask.py "怎么设置自适应 PIV 的查询窗口" --top-pages 6
    python tools/ask.py "为什么标定要精化" --chapter 16
    python tools/ask.py "双相机不同触发率怎么接线"

它做的事：
  1. 用 references/zh-en-terms.json 把中文术语展开成手册英文术语；未收录的中文词会列在
     「⚠ 未收录的中文词」段（看到它说明主题词可能丢了，应自译英文重试，不要直接用结果）。
     疑问/动作类短语（怎么、如何、怎么办……）不计入该告警，避免噪声掩盖真正的主题漂移。
  2. 判定问题类型（A 查证 / B 推理 / C 混合 / 故障排查），提示该用哪种检索策略与证据口径。
  3. 按术语逐条检索，**候选页一律以 raw 原文为准**：目录骨架只用来定位小节，随后在
     raw 的 ``PAGE|N`` 页块里重新校验术语确实出现在该页，避免“起始页取到上一小节内容”。
  4. 给出候选页清单，并打印候选页原文；截断时显式标注，避免把“打印不全”误读成“手册没写”。

注意：本工具只负责“取回原文证据”。最终结论仍必须回原文核对（A 型事实点强制）。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR))

from search_tool import PAGE_MARKER, DynamicStudioSearch, _norm  # noqa: E402

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9$!_.\-]{2,}")
_RAW_CH = re.compile(r"raw/ch(\d+)\.txt")

# 提问用语而非主题名词：术语展开后残留这些词属正常，不应触发“主题词丢失”告警。
# 按长度降序排列，先剔除长短语，避免“怎么办”被拆成“怎么”后留下“办”。
STOP_PHRASES = tuple(
    sorted(
        (
            "为什么", "为何", "什么", "怎么办", "怎么回事", "怎么会", "怎么用", "怎么设置",
            "怎么调", "怎么接", "怎么做", "怎么样", "怎样", "怎么", "如何",
            "哪个", "哪些", "哪里", "在哪", "怎么改", "能不能", "可不可以", "是不是",
            "有没有", "会不会", "要不要", "多少", "多久",
            "设置", "步骤", "方法", "写法", "含义", "意思", "默认", "区别", "差异",
            "原理", "依据", "公式", "可行", "用法",
            "问题", "报错", "错误", "异常", "失败", "出错", "不行", "不工作",
            "出不来", "不对", "不够", "不能", "无法", "不了",
            "解决", "处理", "排查", "修复", "办", "吗", "呢", "啊",
        ),
        key=len,
        reverse=True,
    )
)

# 故障排查类信号：这类问题手册通常没有一句现成结论，应直接归入推理型，避免在语料里空转。
TROUBLE_KEYWORDS = (
    "报错", "错误", "异常", "失败", "出错", "崩溃", "闪退", "打不开", "无法打开",
    "不行", "不工作", "出不来", "不对", "不够", "不能", "无法", "失效", "丢失",
    "failed", "error", "exception", "crash", "deserialize", "not found",
)

THEORY_KEYWORDS = (
    "为什么", "为何", "原理", "依据", "公式", "可行", "能不能", "会怎样", "原因",
    "区别", "差异", "为什么", "凭什么",
)

HOWTO_KEYWORDS = (
    "怎么", "如何", "怎样", "在哪", "哪里", "设置", "步骤", "含义", "默认",
    "是什么", "写成", "多少", "怎么用", "用法",
)


def classify(question: str) -> tuple[str, str]:
    """判定问题类型。故障排查类优先于 A/B，因为它要求的是推理而不是查证。"""
    lowered = question.casefold()
    if any(word in lowered for word in TROUBLE_KEYWORDS):
        return (
            "D",
            "故障排查型：手册通常不直接解释该报错，先按 B 推理（查前提与反证），"
            "再对其中可核实的事实点按 A 单点回原文核。",
        )
    theory = any(word in question for word in THEORY_KEYWORDS)
    howto = any(word in question for word in HOWTO_KEYWORDS)
    if theory and howto:
        return "C", "混合型：先按 B 出骨架，再把骨架里每个事实点按 A 单点回原文核。"
    if theory:
        return "B", "推理型：不要求原文给结论；只查前提与反证，检索封顶（建议 ≤6 次），0 命中也是证据。"
    if howto:
        return "A", "查证型：强制回原文逐字核对，标注 [手册 p.N]。"
    return "C", "混合/不明：默认按 C 处理，事实点回原文核。"


def filter_leftovers(leftovers: list[str]) -> list[str]:
    """剔除提问用语残留，只保留可能是主题名词的中文词。"""
    kept: list[str] = []
    for word in leftovers:
        remainder = word
        for stop in STOP_PHRASES:
            remainder = remainder.replace(stop, " ")
        # 剩余片段按空格切开，任何一个仍有 2 字以上才认为可能是主题词。
        fragments = [fragment for fragment in remainder.split() if len(fragment) >= 2]
        kept.extend(fragments)
    return kept


class EvidenceIndex:
    """一次读入整章原文，按 ``PAGE|N`` 页块做术语命中索引。"""

    def __init__(self, search: DynamicStudioSearch) -> None:
        self.search = search
        self._cache: dict[int, dict[int, str]] = {}
        self._sections: dict[int, list[tuple[str, int]]] = {}

    def sections(self, chapter: int) -> list[tuple[str, int]]:
        """该章所有小节标题及其起始页，用于判断某页最接近哪个小节。"""
        if chapter in self._sections:
            return self._sections[chapter]
        spans: list[tuple[str, int]] = []
        for entry in self.search.toc():
            if int(entry["chapter"]) != chapter:
                continue
            page = entry.get("page")
            if page is None:
                continue
            spans.append((_norm(str(entry["title"])), int(page)))
        spans.sort(key=lambda item: item[1])
        self._sections[chapter] = spans
        return spans

    def pages(self, chapter: int) -> dict[int, str]:
        if chapter in self._cache:
            return self._cache[chapter]
        path = self.search.raw_dir / f"ch{chapter:02d}.txt"
        blocks: dict[int, str] = {}
        if path.is_file():
            lines = path.read_text(encoding="utf-8").splitlines()
            current: int | None = None
            buffer: list[str] = []
            for line in lines:
                marker = PAGE_MARKER.fullmatch(line.strip())
                if marker:
                    if current is not None:
                        blocks[current] = "\n".join(buffer)
                    current = int(marker.group(1))
                    buffer = []
                elif current is not None:
                    buffer.append(line)
            if current is not None:
                blocks[current] = "\n".join(buffer)
        self._cache[chapter] = blocks
        return blocks

    def pages_with(self, chapter: int, term: str) -> list[int]:
        needle = _norm(term)
        if not needle:
            return []
        return [page for page, body in sorted(self.pages(chapter).items()) if needle in _norm(body)]

    def body(self, chapter: int, page: int) -> str:
        return self.pages(chapter).get(page, "")


def collect(
    search: DynamicStudioSearch,
    index: EvidenceIndex,
    terms: list[str],
    chapter: int | None,
) -> dict[tuple[str, int], dict]:
    """汇总候选页。index 命中只用来定位小节，最终页码一律由 raw 页块校验后给出。"""
    buckets: dict[tuple[str, int], dict] = {}

    def touch(chapter_name: str, page: int, term: str, mode: str, *, verified: bool) -> None:
        bucket = buckets.setdefault((chapter_name, page), {"terms": set(), "mode": mode, "verified": verified})
        bucket["terms"].add(term)
        bucket["verified"] = bucket["verified"] or verified

    for term in terms:
        # 1) 目录骨架：把术语匹配到小节，再按小节跨度在 raw 里找真正包含它的页。
        for entry in search.toc():
            if chapter is not None and int(entry["chapter"]) != chapter:
                continue
            if _norm(term) not in _norm(str(entry["title"])):
                continue
            chapter_num = int(entry["chapter"])
            chapter_name = f"ch{chapter_num:02d}"
            span = search.section_spans(chapter_num, str(entry["section"]))
            placed = False
            if span:
                for page in range(span[0], span[1] + 1):
                    if _norm(term) in _norm(index.body(chapter_num, page)):
                        touch(chapter_name, page, term, "toc", verified=True)
                        placed = True
            if not placed and entry.get("page") is not None:
                # 跨度解析失败时，仍以 raw 校验该页是否真的含术语。
                page = int(entry["page"])
                verified = _norm(term) in _norm(index.body(chapter_num, page))
                touch(chapter_name, page, term, "toc", verified=verified)

        # 2) 原文直接命中：天然与整页正文对齐，作为最强证据。
        targets = [chapter] if chapter is not None else list(range(1, 21))
        for chapter_num in targets:
            for page in index.pages_with(chapter_num, term):
                touch(f"ch{chapter_num:02d}", page, term, "raw", verified=True)

    return buckets


def section_affinity(index: EvidenceIndex, chapter: str, page: int, terms: set[str]) -> int:
    """该页“最贴近的小节标题”命中了多少个检索术语，用于把分布在全书的泛词命中压下去。"""
    chapter_num = int(chapter[2:])
    spans = index.sections(chapter_num)
    if not spans:
        return 0
    best_title = ""
    best_page = -1
    for title, start in spans:
        if start <= page and start >= best_page:
            best_page = start
            best_title = title
    score = 0
    for term in terms:
        if _norm(term) in best_title:
            score += 1
    return score


def print_page(
    search: DynamicStudioSearch,
    index: EvidenceIndex,
    chapter: str,
    page: int,
    terms: set[str],
    max_lines: int,
) -> None:
    chapter_num = int(chapter[2:])
    body = index.body(chapter_num, page)
    if not body:
        print(f"\n----- [{chapter}] 打印页 {page} -----")
        print("（该页在原文中未检索到内容，请用 search_tool.py --page 核实）")
        return
    lines = [line for line in body.splitlines() if line.strip()]
    missing = [term for term in sorted(terms) if _norm(term) not in _norm(body)]
    print(f"\n----- [{chapter}] 打印页 {page} -----")
    if missing:
        print(f"⚠ 该页正文未出现术语：{', '.join(missing)}（页码可能仍不精确，请人工核对）")
    shown = lines[:max_lines]
    print("\n".join(shown))
    if len(lines) > len(shown):
        print(
            f"…（本页已截断：共 {len(lines)} 行，此处仅显示前 {len(shown)} 行；"
            f"取全页请运行 python search_tool.py --page {page}）"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="中文问题 → 原文证据包")
    parser.add_argument("question", nargs="+")
    parser.add_argument("--chapter", type=int, help="限定章节（如 16）")
    parser.add_argument("--top-pages", type=int, default=6)
    parser.add_argument("--page-lines", type=int, default=120, help="每页最多打印的行数（默认 120）")
    args = parser.parse_args()

    question = " ".join(args.question)
    search = DynamicStudioSearch(SKILL_DIR)
    index = EvidenceIndex(search)

    print("=" * 66)
    print(f"问题：{question}")
    kind, advice = classify(question)
    print(f"分型：{kind} 型 —— {advice}")

    expanded, leftovers, matched = search.expand(question)
    print("-" * 66)
    if matched:
        print("术语展开：" + "， ".join(f"{zh}→{en}" for zh, en in matched))
    else:
        print("术语展开：无（术语表未覆盖，建议自行把关键词译成英文手册术语）")
    useful_leftovers = filter_leftovers(leftovers)
    if useful_leftovers:
        print(f"⚠ 未收录的中文词：{' / '.join(useful_leftovers)}   ← 主题词可能丢失，请自译英文后重试")

    terms = {en for _, en in matched}
    terms.update(_WORD.findall(question))
    terms = sorted({term for term in terms if len(term) >= 3})
    print(f"检索用英文术语：{terms if terms else '（无）'}")

    if not terms:
        print("=" * 66)
        print("无可检索英文术语。请把问题译成 2–4 个英文手册术语后重试。")
        return

    buckets = collect(search, index, terms, args.chapter)
    print("-" * 66)
    if not buckets:
        total = sum(int(item["lines"]) for item in search.chapter_stats())
        print(f"STATUS: NOT_FOUND_IN_DOCSET（已在 {total} 行语料中检索，无候选页）")
        for term in terms:
            for gap in search.known_gaps(term):
                print(f"缺口台账命中：{gap.get('term')} —— {gap.get('action')}")
        print("→ 0 命中本身是证据：若属 B 型，可直接判定“手册未覆盖该能力”。")
        return

    ranked = sorted(
        buckets.items(),
        key=lambda kv: (
            not kv[1]["verified"],
            -section_affinity(index, kv[0][0], kv[0][1], kv[1]["terms"]),
            -len(kv[1]["terms"]),
            kv[0][1],
        ),
    )
    verified_count = sum(1 for _, info in ranked if info["verified"])
    print(f"候选页（按 raw 校验 + 小节相关度排序，共 {len(ranked)} 页，其中 {verified_count} 页已在原文校验）：")
    for (chapter, page), info in ranked[: args.top_pages]:
        flag = "已校验" if info["verified"] else "待核对"
        affinity = section_affinity(index, chapter, page, info["terms"])
        print(
            f"  ★ p.{page:<5} [{chapter}]  {flag}  小节相关度 {affinity}  "
            f"命中 {len(info['terms'])} 术语: {', '.join(sorted(info['terms']))}"
        )

    print("\n" + "=" * 66)
    print("证据包（top 页原文，逐字核对用）：")
    for (chapter, page), info in ranked[: args.top_pages]:
        print_page(search, index, chapter, page, info["terms"], args.page_lines)
    print("\n提示：以上为原页文本，非结论。请按分型规则标注 [手册 p.N] / [推理] / [未覆盖·判断]。")


if __name__ == "__main__":
    main()
