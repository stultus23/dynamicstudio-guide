#!/usr/bin/env python3
"""问题入口：把中文问题变成“英文手册术语 + 候选页 + 原页证据包”。

用法：
    python tools/ask.py "怎么设置自适应 PIV 的查询窗口" --top-pages 6
    python tools/ask.py "为什么标定要精化" --chapter 16
    python tools/ask.py "双相机不同触发率怎么接线"

它做的事：
  1. 用 references/zh-en-terms.json 把中文术语展开成手册英文术语；未收录的中文词会列在
     「⚠ 未收录的中文词」段（看到它说明主题词可能丢了，应自译英文重试，不要直接用结果）。
  2. 判定问题类型（A 查证 / B 推理 / C 混合），提示该用哪种检索策略与证据口径。
  3. 按术语逐条检索（默认 auto：先索引、无命中降级 chapters/raw），按 章 + 打印页 聚合排序。
  4. 给出候选页清单，并打印 top 页的原文，供逐字核对。

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

from search_tool import DynamicStudioSearch  # noqa: E402

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9$!_.\-]{2,}")
_RAW_CH = re.compile(r"raw/ch(\d+)\.txt")


def classify(question: str) -> tuple[str, str]:
    theory = any(k in question for k in ("为什么", "原理", "依据", "公式", "可行", "能不能", "会怎样", "原因", "区别"))
    howto = any(k in question for k in ("怎么", "如何", "在哪", "哪里", "设置", "步骤", "含义", "默认", "是什么", "写成", "多少"))
    if theory and howto:
        return "C", "混合型：先按 B 出骨架，再把骨架里每个事实点按 A 单点回原文核。"
    if theory:
        return "B", "推理型：不要求原文给结论；只查前提与反证，检索封顶（建议 ≤6 次），0 命中也是证据。"
    if howto:
        return "A", "查证型：强制回原文逐字核对，标注 [手册 p.N]。"
    return "C", "混合/不明：默认按 C 处理，事实点回原文核。"


def bucket_of(result, term: str) -> tuple[str, int] | None:
    if result.page is None:
        return None
    match = _RAW_CH.match(result.source)
    if match:
        return (f"ch{int(match.group(1)):02d}", result.page)
    if result.source == "toc" and result.context:
        return (result.context[0], result.page)
    return None


def collect(search: DynamicStudioSearch, terms: list[str], chapter: int | None) -> dict[tuple[str, int], dict]:
    buckets: dict[tuple[str, int], dict] = {}
    for term in terms:
        source = "raw" if chapter else "auto"
        results, mode = search.search_with_mode(term, source, chapter, 1)
        for res in results:
            key = bucket_of(res, term)
            if key is None:
                continue
            bucket = buckets.setdefault(key, {"terms": set(), "sample": res.content, "mode": mode})
            bucket["terms"].add(term)
    return buckets


def main() -> None:
    parser = argparse.ArgumentParser(description="中文问题 → 原文证据包")
    parser.add_argument("question", nargs="+")
    parser.add_argument("--chapter", type=int, help="限定章节（如 16）")
    parser.add_argument("--top-pages", type=int, default=6)
    args = parser.parse_args()

    question = " ".join(args.question)
    search = DynamicStudioSearch(SKILL_DIR)

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
    if leftovers:
        print(f"⚠ 未收录的中文词：{' / '.join(leftovers)}   ← 主题词可能丢失，请自译英文后重试")

    terms = {en for _, en in matched}
    terms.update(_WORD.findall(question))
    terms = sorted({t for t in terms if len(t) >= 3})
    print(f"检索用英文术语：{terms if terms else '（无）'}")

    if not terms:
        print("=" * 66)
        print("无可检索英文术语。请把问题译成 2–4 个英文手册术语后重试。")
        return

    buckets = collect(search, terms, args.chapter)
    print("-" * 66)
    if not buckets:
        total = sum(int(item["lines"]) for item in search.chapter_stats())
        print(f"STATUS: NOT_FOUND_IN_DOCSET（已在 {total} 行语料中检索，无候选页）")
        for term in terms:
            for gap in search.known_gaps(term):
                print(f"缺口台账命中：{gap.get('term')} —— {gap.get('action')}")
        print("→ 0 命中本身是证据：若属 B 型，可据此判定“手册未覆盖该能力”。")
        return

    ranked = sorted(buckets.items(), key=lambda kv: (-len(kv[1]["terms"]), kv[0][1]))
    print(f"候选页（按命中术语数排序，共 {len(ranked)} 页）：")
    for (chapter, page), info in ranked[: args.top_pages]:
        print(f"  ★ p.{page:<5} [{chapter}]  命中 {len(info['terms'])} 术语: {', '.join(sorted(info['terms']))}")

    print("\n" + "=" * 66)
    print("证据包（top 页原文，逐字核对用）：")
    for (chapter, page), info in ranked[: args.top_pages]:
        pages = search.search_page(page)
        if not pages:
            continue
        source, content = pages[0]
        body = [ln for ln in content.splitlines() if ln.strip()]
        print(f"\n----- [{chapter} / {source}] 打印页 {page} -----")
        print("\n".join(body[:35]))
    print("\n提示：以上为原页文本，非结论。请按分型规则标注 [手册 p.N] / [推理] / [未覆盖·判断]。")


if __name__ == "__main__":
    main()
