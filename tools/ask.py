#!/usr/bin/env python3
"""问题入口：把中文问题变成“英文手册术语 + 候选页 + 命中片段 + 置信度”。

用法：
    python tools/ask.py "怎么设置自适应 PIV 的查询窗口"
    python tools/ask.py "双相机触发率不同还能同步吗" --json
    python tools/ask.py "Grid Step Size" --full --page-lines 200

它做的事（按顺序）：
  1. 分型 A/B/C/D/E：决定该查一句话、该推理、还是该给参数建议。
  2. 术语展开：中文 → 手册英文术语；同一条英文里连续 token 组成短语（``grid step size``），
     短语只在原文真的出现过时才收，避免“拼一个查不到的短语”。
  3. 打分排序：``Σ w·idf(术语) + 标题链加分``，再按概念覆盖率加权。idf 让全书高频词
     （piv / image / camera）自动让位给判别性强的短语。
  4. 只打印**命中行附近**的片段（页级上限 + 全局字符预算），并在首部给出置信度，
     让调用方知道“能不能就此停手”。

候选页一律以 raw 原文为准：页码来自原文显式 ``PAGE|N`` 标记，每个候选页都已确认正文真的
出现了对应术语。本工具只负责取回证据，结论仍须按三档标注（[手册 p.N] / [推理] / [未覆盖·判断]）。
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
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
_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9$!_.\-]*")
_HEADING = re.compile(r"^(\d+(?:\.\d+)*)\s+(\S.*)$")
_CJK = re.compile(r"[\u4e00-\u9fff]")

# 英文停用词：提问用语，不是手册术语。
EN_STOP = frozenset(
    "how what is are was were the a an to of and or in on for with use used using "
    "do does did i my me we our you your it its this that these those at by as be "
    "can could should would will why which when where from about into than then".split()
)

# 提问用语而非主题名词：术语展开后残留这些词属正常，不应触发“主题词丢失”告警。
# 按长度降序排列，先剔除长短语，避免“怎么办”被拆成“怎么”后留下“办”。
STOP_PHRASES = tuple(
    sorted(
        (
            "为什么", "为何", "什么", "怎么办", "怎么回事", "怎么会", "怎么用", "怎么设置",
            "怎么调", "怎么接", "怎么做", "怎么样", "怎样", "怎么", "如何", "多少合适",
            "哪个", "哪些", "哪里", "在哪", "怎么改", "能不能", "可不可以", "是不是",
            "有没有", "会不会", "要不要", "多少", "多久", "是不是", "是否合适",
            "设置", "步骤", "方法", "写法", "含义", "意思", "默认", "区别", "差异",
            "原理", "依据", "公式", "可行", "用法", "推荐", "建议", "合适", "合理", "多大",
            "问题", "报错", "错误", "异常", "失败", "出错", "不行", "不工作",
            "出不来", "不对", "不够", "不能", "无法", "不了",
            "解决", "处理", "排查", "修复", "办", "吗", "呢", "啊",
            # 口语填充与泛指词（实测误报：不同还能同步 / 有很多 / 数据到）
            "不同", "还能", "很多", "有很多", "一下", "时候", "这个", "那个",
            "我们", "我", "应该", "需要", "可以", "一般", "有哪些", "有什么",
            # 通用动词/后缀：不带主题信息，留着只会把置信度拉成“低”（实测误报：
            # 做+图像 / 率+重叠 / 打算 / 计算 / 批量 / 注意）
            "打算", "计算", "批量", "注意", "查看", "看一下", "使用", "做", "率",
            "的", "了", "和", "与", "在", "到", "用", "有",
        ),
        key=len,
        reverse=True,
    )
)

# 故障排查类信号：这类问题手册通常没有一句现成结论，应直接归入推理型，避免在语料里空转。
TROUBLE_KEYWORDS = (
    "报错", "错误", "异常", "失败", "出错", "崩溃", "闪退", "打不开", "无法打开",
    "不行", "不工作", "出不来", "不对", "不够", "不能", "无法", "失效", "丢失",
    "怎么解决", "偏大", "偏小", "不准", "噪声大", "很多错误", "跳动",
    "failed", "error", "exception", "crash", "deserialize", "not found",
)

# 疑问结构：修掉“能不能 ⊃ 不能”的误判——先把它们从串里去掉再匹配故障词。
INTERROGATIVE_STRUCTURES = ("能不能", "可不可以", "是不是", "会不会", "行不行", "要不要")

THEORY_KEYWORDS = (
    "为什么", "为何", "原理", "依据", "公式", "可行", "能不能", "会怎样", "原因",
    "区别", "差异", "为什么", "凭什么",
    # 可行性类信号（“还能同步吗 / 可以吗 / 够吗”都是可行性问题，不是查证题）
    "能否", "是否", "还能", "可以吗", "行吗", "行不行", "够吗", "对吗",
)

HOWTO_KEYWORDS = (
    "怎么", "如何", "怎样", "在哪", "哪里", "设置", "步骤", "含义", "默认",
    "是什么", "写成", "多少", "怎么用", "用法",
)

# E 型：方案确认 / 参数推荐。这是用户的核心需求，必须单独一类。
ADVICE_KEYWORDS = (
    "合适", "合理", "推荐", "建议", "多大", "多少合适", "选多少",
    "我打算", "我准备", "我的方案", "这样设", "这样做", "是否合适", "够不够",
)

# 标题链上每往上一层，加分按此系数衰减：父节比最深小节弱，爷爷节更弱。
ANCHOR_FACTOR = 0.6
# 章级标题（无点号，如 “16 Python Link”）只是容器，标题加分再压一档。
CHAPTER_HEADING_FACTOR = 0.5
# 中文问题的中心词（最后一个概念）抬一档，修饰性概念降一档。
HEAD_WEIGHT = 1.3
# 词频饱和强度：log1p 形式，0 = 完全不用词频，越大越偏向“反复讨论该词”的页。
TF_STRENGTH = 0.4

KIND_ADVICE = {    "A": "查证型：据片段逐字作答，标注 [手册 p.N]。",
    "B": "推理型：不要求原文给结论；只查前提与反证，检索封顶。",
    "C": "混合型：先出骨架，再把每个事实点单点回原文核。",
    "D": "故障排查型：先证明手册没写，再按机制推链条。",
    "E": "方案确认型：把方案拆成参数清单 → 逐项比对手册/经验依据 → 逐项判合适与否。",
}


# --------------------------------------------------------------------- 分型 ----
def _strip_interrogative(text: str) -> str:
    for phrase in INTERROGATIVE_STRUCTURES:
        text = text.replace(phrase, " ")
    return text


def classify(question: str) -> tuple[str, str]:
    """判定问题类型。故障排查优先，其次方案确认，再看推理/查证。"""
    probe = _strip_interrogative(question).casefold()
    if any(word in probe for word in TROUBLE_KEYWORDS):
        return "D", KIND_ADVICE["D"]
    if any(word in question for word in ADVICE_KEYWORDS):
        return "E", KIND_ADVICE["E"]
    theory = any(word in question for word in THEORY_KEYWORDS)
    howto = any(word in question for word in HOWTO_KEYWORDS)
    if theory and howto:
        return "C", KIND_ADVICE["C"]
    if theory:
        return "B", KIND_ADVICE["B"]
    if howto:
        return "A", KIND_ADVICE["A"]
    return "C", KIND_ADVICE["C"]


def filter_leftovers(leftovers: list[str], matched: list[tuple[str, str]] | None = None) -> list[str]:
    """剔除提问用语残留，只保留可能是主题名词的中文词。

    ``matched`` 给定时，只剩单个汉字且紧贴某个已匹配术语的残留会写成 ``自+标定``，
    避免“自标定”里的“自”被静默丢弃。
    """
    kept: list[str] = []
    for word in leftovers:
        remainder = word
        for stop in STOP_PHRASES:
            remainder = remainder.replace(stop, " ")
        fragments = [fragment for fragment in remainder.split() if len(fragment) >= 2]
        kept.extend(fragments)
    return kept


def residue_warnings(question: str, matched: list[tuple[str, str]]) -> list[str]:
    """单字残留 + 术语相邻时，输出 ``自+标定`` 形式的告警项。"""
    masked = list(question)
    # 提问用语先占位：否则“怎么标定相机”里“怎么”剩下的“么”会被当成丢掉的主题字。
    for stop in STOP_PHRASES:
        start = 0
        while True:
            pos = question.find(stop, start)
            if pos < 0:
                break
            for i in range(pos, pos + len(stop)):
                masked[i] = "\0"
            start = pos + len(stop)
    spans: list[tuple[int, int, str]] = []
    for zh, _en in sorted(matched, key=lambda pair: len(pair[0]), reverse=True):
        start = 0
        while True:
            pos = question.find(zh, start)
            if pos < 0:
                break
            if all(masked[i] != "\0" for i in range(pos, pos + len(zh))):
                for i in range(pos, pos + len(zh)):
                    masked[i] = "\0"
                spans.append((pos, pos + len(zh), zh))
            start = pos + len(zh)
    items: list[str] = []
    for index, char in enumerate(question):
        if masked[index] == "\0" or not _CJK.match(char):
            continue
        # 只报“紧贴术语之前的单字”——它是修饰语（自+标定），真的会改变检索语义；
        # 术语之后的单字（率+重叠、做+图像）基本是语法后缀，报了只会制造假告警。
        right = next((zh for (a, b, zh) in spans if a == index + 1), None)
        if right:
            items.append(f"{char}+{right}")
    return items


# ------------------------------------------------------------------ 语料索引 ----
@dataclass(frozen=True)
class Heading:
    line: int
    page: int
    section: str
    title: str
    depth: int


class ChapterData:
    """一章原文的行、页块与标题链。"""

    def __init__(self, chapter: int, lines: list[str], toc_sections: dict[str, str]) -> None:
        self.chapter = chapter
        self.lines = lines
        self.norm_lines = [_norm(line) for line in lines]
        blocks: dict[int, tuple[int, int]] = {}
        marks: list[tuple[int, int]] = []
        for index, line in enumerate(lines):
            marker = PAGE_MARKER.fullmatch(line.strip())
            if marker:
                marks.append((int(marker.group(1)), index))
        for position, (page, marker_index) in enumerate(marks):
            start = marker_index + 1
            end = marks[position + 1][1] if position + 1 < len(marks) else len(lines)
            blocks.setdefault(page, (start, end))
        self.pages = blocks
        self.page_text = {page: " ".join(self.norm_lines[s:e]) for page, (s, e) in blocks.items()}
        self.headings: list[Heading] = []
        for index, line in enumerate(lines):
            stripped = line.strip()
            match = _HEADING.match(stripped)
            if not match or len(stripped) > 120:
                continue
            section = match.group(1)
            if section not in toc_sections:
                continue
            page = self.page_of_line(index)
            if page is None:
                continue
            self.headings.append(Heading(index, page, section, match.group(2).strip(), section.count(".")))
        self.heading_lines = [heading.line for heading in self.headings]
        self.by_section: dict[str, Heading] = {}
        for heading in self.headings:
            self.by_section.setdefault(heading.section, heading)

    def page_of_line(self, line_index: int) -> int | None:
        best = None
        for page, (start, end) in self.pages.items():
            if start <= line_index < end:
                best = page
                break
        return best

    def chain_at(self, line_index: int) -> list[Heading]:
        """命中行所在的标题链：[最深小节, 父节, ..., 章]。"""
        position = -1
        for index, heading in enumerate(self.headings):
            if heading.line <= line_index:
                position = index
            else:
                break
        if position < 0:
            return []
        chain = [self.headings[position]]
        section = self.headings[position].section
        while "." in section:
            section = section.rsplit(".", 1)[0]
            parent = self.by_section.get(section)
            if parent is not None:
                chain.append(parent)
        return chain

    def headings_on_page(self, page: int) -> list[Heading]:
        return [heading for heading in self.headings if heading.page == page]

    def title_of(self, section: str) -> str:
        heading = self.by_section.get(section)
        return heading.title if heading else ""


class Corpus:
    """全部 raw 页块 + 术语倒排（postings）。df/idf 在进程内缓存，供打分使用。"""

    def __init__(self, search: DynamicStudioSearch) -> None:
        self.search = search
        self._chapters: dict[int, ChapterData] = {}
        self._postings: dict[str, dict[tuple[int, int], list[int]]] = {}
        self._toc: dict[int, dict[str, str]] | None = None

    def toc_sections(self) -> dict[int, dict[str, str]]:
        if self._toc is None:
            table: dict[int, dict[str, str]] = {}
            for entry in self.search.toc():
                table.setdefault(int(entry["chapter"]), {})[str(entry["section"])] = str(entry["title"])
            self._toc = table
        return self._toc

    def chapter(self, chapter: int) -> ChapterData:
        if chapter not in self._chapters:
            path = self.search.raw_dir / f"ch{chapter:02d}.txt"
            lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
            self._chapters[chapter] = ChapterData(chapter, lines, self.toc_sections().get(chapter, {}))
        return self._chapters[chapter]

    def page_count(self) -> int:
        total = 0
        for chapter in range(1, 21):
            data = self.chapter(chapter)
            if data.lines:
                total += len(data.pages)
        return total

    def postings(self, term: str) -> dict[tuple[int, int], list[int]]:
        """术语出现在哪些页的哪些行：{(chapter, page): [行号...]}。

        2–3 字符的缩写（IA、UOD、POD、dt）按词边界匹配，否则 "ia" 会命中 media / -ial 之类的噪声。
        """
        needle = _norm(term)
        if not needle:
            return {}
        cached = self._postings.get(needle)
        if cached is not None:
            return cached
        pattern = None
        if len(needle) <= 3:
            pattern = re.compile(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])")

        def hit(text: str) -> bool:
            return bool(pattern.search(text)) if pattern else needle in text

        found: dict[tuple[int, int], list[int]] = {}
        for chapter in range(1, 21):
            data = self.chapter(chapter)
            for page, (start, end) in data.pages.items():
                if not hit(data.page_text[page]):
                    continue
                lines = [index for index in range(start, end) if hit(data.norm_lines[index])]
                if lines:
                    found[(chapter, page)] = lines
        self._postings[needle] = found
        return found

    def document_frequency(self, term: str) -> int:
        return len(self.postings(term))

    def idf(self, term: str) -> float:
        total = self.page_count()
        df = self.document_frequency(term)
        if total <= 0:
            return 0.0
        return math.log(total / (1 + df))

    def text_blob(self) -> str:
        """全语料归一化文本，用于低成本判断“这个短语原文里到底有没有”。"""
        blob = getattr(self, "_blob", None)
        if blob is None:
            blob = " ".join(
                data.page_text[page]
                for chapter in range(1, 21)
                for data in (self.chapter(chapter),)
                for page in data.pages
            )
            self._blob = blob
        return blob

    def contains(self, phrase: str) -> bool:
        needle = _norm(phrase)
        return bool(needle) and needle in self.text_blob()


# --------------------------------------------------------------- 术语与短语 ----
@dataclass
class Term:
    text: str
    weight: float
    kind: str  # phrase / zh / word

    def idf(self, corpus: Corpus) -> float:
        cache = getattr(self, "_idf", None)
        if cache is None:
            cache = corpus.idf(self.text)
            object.__setattr__(self, "_idf", cache)
        return cache


def _runs(question: str) -> list[list[str]]:
    """把问题切成英文 token run：中文/标点断句，段内连续英文 token（含空格）成组。"""
    runs: list[list[str]] = []
    for segment in re.split(r"[^A-Za-z0-9$!_.\- ]+", question):
        tokens = [
            token
            for token in _TOKEN.findall(segment)
            if len(token) >= 2 and not re.fullmatch(r"[xX]\d+", token)
        ]
        if tokens:
            runs.append(tokens)
    return runs


def build_terms(question: str, corpus: Corpus, matched: list[tuple[str, str]]) -> list[Term]:
    """短语优先：连续英文 token 的 n-gram 只有真的出现在原文里才收。"""
    phrases: list[Term] = []
    covered: set[str] = set()
    for tokens in _runs(question):
        ngrams: list[tuple[int, int, str]] = []
        size = len(tokens)
        while size >= 2:
            for start in range(0, len(tokens) - size + 1):
                candidate = " ".join(tokens[start : start + size])
                if candidate.casefold() in EN_STOP:
                    continue
                ngrams.append((start, size, candidate))
            size -= 1
        accepted: list[tuple[int, int, str]] = []
        for start, size, candidate in ngrams:
            if any(other_start <= start and start + size <= other_start + other_size
                   for other_start, other_size, _text in accepted):
                continue  # 已被更长的短语覆盖
            if not corpus.contains(candidate):
                continue
            accepted.append((start, size, candidate))
            phrases.append(Term(candidate, 2.0, "phrase"))
            covered.update(token.casefold() for token in candidate.split())

    zh_terms = [Term(en, 1.5, "zh") for _zh, en in matched]
    zh_keys = {term.text.casefold() for term in zh_terms}
    words: list[Term] = []
    seen: set[str] = set()
    for tokens in _runs(question):
        for token in tokens:
            key = token.casefold()
            if key in seen or key in EN_STOP or len(token) < 2:
                continue
            seen.add(key)
            if any(term.text.casefold() == key for term in phrases) or key in zh_keys:
                continue
            weight = 0.3 if key in covered else 1.0
            words.append(Term(token, weight, "word"))

    terms = phrases + zh_terms + words
    return _apply_head_weight(question, terms, matched)


def _apply_head_weight(question: str, terms: list[Term], matched: list[tuple[str, str]]) -> list[Term]:
    """中文是“定语 + 中心词”语序：问题里最后的那个概念才是被问的东西。

    “Stereo PIV 标定精化”问的是标定精化，不是 Stereo PIV 本身；把末尾概念抬一档、
    前面的概念降一档，避免修饰性技术名把答案带到该技术的总述页。
    """
    lowered = question.casefold()
    positions: dict[str, int] = {}
    for term in terms:
        if term.kind not in ("phrase", "zh"):
            continue
        candidates = [term.text]
        if term.kind == "zh":
            candidates += [zh for zh, en in matched if en == term.text]
        found = [lowered.find(candidate.casefold()) for candidate in candidates]
        found = [index for index in found if index >= 0]
        if found:
            positions[term.text] = max(found)
    if len(positions) < 2:
        return terms
    head = max(positions, key=positions.get)
    adjusted = []
    for term in terms:
        if term.kind in ("phrase", "zh"):
            factor = HEAD_WEIGHT if term.text == head else 1.0 / HEAD_WEIGHT
            adjusted.append(Term(term.text, round(term.weight * factor, 3), term.kind))
        else:
            adjusted.append(term)
    return adjusted


def _title_tokens(title: str) -> int:
    return max(1, len(re.findall(r"[A-Za-z0-9]+", title)))


@dataclass
class PageScore:
    chapter: int
    page: int
    score: float
    base: float
    bonus: float
    coverage: float
    section: str
    title: str
    hits: list[str] = field(default_factory=list)
    phrases: list[str] = field(default_factory=list)
    title_hit: bool = False
    lines: list[int] = field(default_factory=list)


def rank_pages(corpus: Corpus, terms: list[Term]) -> list[PageScore]:
    """score = (Σ w·idf·tf饱和 + 标题链加分) × (1 + 0.5·概念覆盖率)。

    tf 用 log1p 饱和而不是线性计数，避免“顺带列了一次术语”的页面积分；标题加分只取该页
    最好的一个标题，跨小节页不叠加。
    """
    concept_count = sum(1 for term in terms if term.kind in ("phrase", "zh")) or 1
    postings = {term.text: corpus.postings(term.text) for term in terms}
    idf = {term.text: term.idf(corpus) for term in terms}
    weights = {term.text: term.weight for term in terms}
    kinds = {term.text: term.kind for term in terms}

    page_terms: dict[tuple[int, int], dict[str, list[int]]] = {}
    for text, hits in postings.items():
        for key, lines in hits.items():
            page_terms.setdefault(key, {})[text] = lines

    scored: list[PageScore] = []
    for (chapter, page), hits in page_terms.items():
        data = corpus.chapter(chapter)
        # BM25 式的 tf 饱和：术语在页内反复出现说明这一页在讲它，而不是顺带列了一次。
        base = sum(
            weights[text] * idf[text] * (1 + TF_STRENGTH * math.log1p(len(lines) - 1))
            for text, lines in hits.items()
        )

        # 标题加分：链上每个标题按“标题被命中的比例”计分，页面只取其中最好的一个标题
        # （同一页跨小节时，不给它叠加两份加分）。
        grouped: dict[str, dict] = {}
        section_votes: dict[str, float] = {}
        occurrence_lines: list[int] = []
        chain_cache: dict[int, list[Heading]] = {}
        for text, lines in hits.items():
            needle = _norm(text)
            occurrence_lines.extend(lines)
            for line in lines:
                chain = chain_cache.get(line)
                if chain is None:
                    chain = data.chain_at(line)
                    chain_cache[line] = chain
                if not chain:
                    section_votes[""] = section_votes.get("", 0.0) + weights[text] * idf[text]
                    continue
                deepest = chain[0]
                section_votes[deepest.section] = (
                    section_votes.get(deepest.section, 0.0) + weights[text] * idf[text]
                )
                for depth, heading in enumerate(chain):
                    if needle not in _norm(heading.title):
                        continue
                    bucket = grouped.setdefault(
                        heading.section,
                        {
                            "terms": set(),
                            "factor": ANCHOR_FACTOR ** depth
                            * (1.5 if depth == 0 else 1.0)
                            * (CHAPTER_HEADING_FACTOR if "." not in heading.section else 1.0),
                            "tokens": _title_tokens(heading.title),
                        },
                    )
                    bucket["terms"].add(text)
        bonus = 0.0
        for bucket in grouped.values():
            share = min(1.0, len(bucket["terms"]) / max(1, bucket["tokens"]))
            contribution = bucket["factor"] * share * sum(
                idf[text] * weights[text] for text in bucket["terms"]
            )
            bonus = max(bonus, contribution)
        section = max(section_votes, key=section_votes.get) if section_votes else ""

        concept_hits = sum(
            1
            for text, kind in kinds.items()
            if kind in ("phrase", "zh") and text in hits
        )
        coverage = concept_hits / concept_count
        score = (base + bonus) * (1 + 0.5 * coverage)
        scored.append(
            PageScore(
                chapter=chapter,
                page=page,
                score=score,
                base=base,
                bonus=bonus,
                coverage=coverage,
                section=section,
                title=data.title_of(section),
                hits=sorted(hits, key=lambda text: -weights[text] * idf[text]),
                phrases=[text for text in hits if kinds[text] == "phrase"],
                title_hit=bool(grouped),
                lines=sorted(set(occurrence_lines)),
            )
        )

    scored.sort(key=lambda item: (-item.score, item.page))
    # 同一小节最多保留 2 页，避免 top-K 被一个小节占满。
    per_section: dict[tuple[int, str], int] = {}
    kept: list[PageScore] = []
    for item in scored:
        key = (item.chapter, item.section or f"page{item.page}")
        if per_section.get(key, 0) >= 2:
            continue
        per_section[key] = per_section.get(key, 0) + 1
        kept.append(item)
    return kept


def confidence(pages: list[PageScore], leftovers: list[str]) -> tuple[str, str]:
    if not pages:
        return "低", "0 命中：按退让流程改英文术语重试，或直接判定手册未覆盖"
    top = pages[0]
    margin = top.score >= 1.3 * pages[1].score if len(pages) > 1 else True
    full = top.coverage >= 0.999
    titled = top.title_hit or bool(top.phrases)
    if leftovers:
        return "低", f"存在未收录中文词（{', '.join(leftovers[:3])}），主题词可能丢失，按退让流程重试"
    if full and titled and margin:
        return "高", "top1 页同时命中短语/核心概念与小节标题，可直接据此作答，无需再检索"
    if top.score < 2.0:
        return "低", "top1 分数偏低，命中的多是全书高频泛词，建议换英文术语重试"
    return "中", "建议对 top1 用 search_tool.py --page N 读整页后作答"


# --------------------------------------------------------------- 片段与打印 ----
def page_snippet(
    corpus: Corpus,
    item: PageScore,
    window: int = 6,
    cap: int = 30,
) -> tuple[list[str], bool]:
    """命中行 ±window 的窗口，合并相邻窗口；页中小节标题在命中之前时从标题行开始。"""
    data = corpus.chapter(item.chapter)
    span = data.pages.get(item.page)
    if not span:
        return [], False
    start, end = span
    local = sorted({line - start for line in item.lines if start <= line < end})
    if not local:
        local = [0]
    windows: list[list[int]] = []
    for offset in local:
        low = max(0, offset - window)
        high = min(end - start, offset + window + 1)
        if windows and low <= windows[-1][1]:
            windows[-1][1] = max(windows[-1][1], high)
        else:
            windows.append([low, high])
    # 标题行之前的内容属于上一小节：若命中点上方有本页的小节标题，就从标题行开始打印。
    first_hit = local[0]
    starts = [
        heading.line - start
        for heading in data.headings_on_page(item.page)
        if 0 <= heading.line - start <= first_hit
    ]
    if starts:
        windows[0][0] = max(windows[0][0], max(starts))

    rendered: list[str] = []
    truncated = False
    for index, (low, high) in enumerate(windows):
        if index:
            rendered.append("      ⋯")
        for offset in range(low, high):
            text = data.lines[start + offset].strip()
            if not text:
                continue
            if len(rendered) >= cap:
                truncated = True
                break
            rendered.append(text)
        if truncated:
            break
    return rendered, truncated


def _fmt_terms(terms: list[Term]) -> str:
    """只展开概念（短语/中文），单词只报个数——它们是背景词，不该占输出预算。"""
    concepts = [term for term in terms if term.kind in ("phrase", "zh")]
    words = [term for term in terms if term.kind == "word"]
    chunks = [f"{term.text}({term.weight:.2f})" for term in concepts]
    text = " · ".join(chunks) if chunks else "（无概念词）"
    if words:
        tail = "、".join(term.text for term in words[:6])
        text += f" ＋单词 {tail}"
    return text


def print_page(
    search: DynamicStudioSearch,
    index: "EvidenceIndex",
    chapter: str,
    page: int,
    terms: set[str],
    max_lines: int,
) -> None:
    """整页打印（--full 用，即旧行为）。"""
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


# ------------------------------------------------- 兼容层（历史测试与 --full） ----
class EvidenceIndex:
    """一次读入整章原文，按 ``PAGE|N`` 页块做术语命中索引。"""

    def __init__(self, search: DynamicStudioSearch) -> None:
        self.search = search
        self._cache: dict[int, dict[int, str]] = {}
        self._sections: dict[int, list[tuple[str, int]]] = {}

    def sections(self, chapter: int) -> list[tuple[str, int]]:
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
    """汇总候选页（旧接口，保留给回归测试与 --full 的术语缺失提示）。"""
    buckets: dict[tuple[str, int], dict] = {}

    def touch(chapter_name: str, page: int, term: str, mode: str, *, verified: bool) -> None:
        bucket = buckets.setdefault((chapter_name, page), {"terms": set(), "mode": mode, "verified": verified})
        bucket["terms"].add(term)
        bucket["verified"] = bucket["verified"] or verified

    for term in terms:
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
                page = int(entry["page"])
                verified = _norm(term) in _norm(index.body(chapter_num, page))
                touch(chapter_name, page, term, "toc", verified=verified)

        targets = [chapter] if chapter is not None else list(range(1, 21))
        for chapter_num in targets:
            for page in index.pages_with(chapter_num, term):
                touch(f"ch{chapter_num:02d}", page, term, "raw", verified=True)

    return buckets


def section_affinity(index: EvidenceIndex, chapter: str, page: int, terms: set[str]) -> int:
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


# ------------------------------------------------------------------ 参数依据 ----
def guideline_matches(skill_dir: Path, question: str, terms: list[Term]) -> list[dict]:
    path = skill_dir / "references" / "param-guidelines.json"
    if not path.is_file():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    lowered = question.casefold()
    term_text = " ".join(term.text.casefold() for term in terms)
    matches: list[dict] = []
    for item in payload.get("items", []):
        zh_hit = any(word in question for word in item.get("zh", []))
        en_hit = any(str(param).casefold() in term_text for param in item.get("params", []))
        if zh_hit or en_hit:
            matches.append(item)
    return matches


def _fmt_guideline(item: dict) -> str:
    source = item.get("source")
    if source == "manual":
        refs = "、".join(item.get("manual_refs", [])) or "（缺页码）"
        tag = f"手册 {refs}"
    else:
        tag = f"判断｜适用：{item.get('applies_when', '—')}｜推翻：{item.get('overturn_when', '—')}"
    return f"  · {item.get('id')}：{item.get('rule')}  [{tag}]"


# ------------------------------------------------------------------- 主流程 ----
def main() -> None:
    parser = argparse.ArgumentParser(description="中文问题 → 分型 + 置信度 + 候选页 + 命中片段")
    parser.add_argument("question", nargs="+")
    parser.add_argument("--chapter", type=int, help="限定章节（如 16）")
    parser.add_argument("--top-pages", type=int, default=3, help="候选页数量（默认 3）")
    parser.add_argument("--page-lines", type=int, default=None, help="每页最多打印的行数（默认片段 24 / 整页 120）")
    parser.add_argument("--window", type=int, default=6, help="命中行上下各取多少行（默认 6）")
    parser.add_argument("--budget", type=int, default=3400, help="整段输出的总字符预算（默认 3400）")
    parser.add_argument("--full", action="store_true", help="打印整页（旧行为）")
    parser.add_argument("--json", action="store_true", help="输出结构化 JSON")
    args = parser.parse_args()

    question = " ".join(args.question)
    search = DynamicStudioSearch(SKILL_DIR)
    corpus = Corpus(search)
    kind, advice = classify(question)

    expanded, leftovers_raw, matched = search.expand(question)
    useful_leftovers = filter_leftovers(leftovers_raw, matched)
    useful_leftovers += residue_warnings(question, matched)

    terms = build_terms(question, corpus, matched)
    pages = rank_pages(corpus, terms)
    if args.chapter is not None:
        pages = [item for item in pages if item.chapter == args.chapter]
    pages = pages[: max(1, args.top_pages)]
    level, reason = confidence(pages, useful_leftovers)
    guidelines = guideline_matches(SKILL_DIR, question, terms) if kind == "E" or terms else []

    if args.json:
        payload = {
            "question": question,
            "kind": kind,
            "advice": advice,
            "confidence": {"level": level, "reason": reason},
            "terms": [
                {"term": term.text, "kind": term.kind, "weight": term.weight, "idf": round(term.idf(corpus), 2)}
                for term in terms
            ],
            "leftovers": useful_leftovers,
            "guidelines": guidelines,
            "pages": [
                {
                    "page": item.page,
                    "chapter": f"ch{item.chapter:02d}",
                    "section": item.section,
                    "title": item.title,
                    "score": round(item.score, 2),
                    "coverage": round(item.coverage, 2),
                    "lines": page_snippet(corpus, item, args.window, 24)[0],
                }
                for item in pages
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=1))
        return

    head: list[str] = ["=" * 62, f"问题：{question}", f"分型：{kind} 型 —— {advice}", f"置信度：{level} —— {reason}", "-" * 62]
    if matched:
        head.append("术语展开：" + "， ".join(f"{zh}→{en}" for zh, en in matched))
    else:
        head.append("术语展开：无（术语表未覆盖，可自行把关键词译成英文手册术语重试）")
    if useful_leftovers:
        head.append(f"⚠ 未收录的中文词：{' / '.join(useful_leftovers)}   ← 主题词可能丢失，请自译英文后重试")
    if not terms:
        head += ["检索用术语：（无）", "=" * 62, "无可检索英文术语。请把问题译成 2–4 个英文手册术语后重试。"]
        print("\n".join(head))
        return
    head.append(f"检索用术语：{_fmt_terms(terms)}")

    if not pages:
        total = sum(int(item["lines"]) for item in search.chapter_stats())
        head += ["-" * 62, f"STATUS: NOT_FOUND_IN_DOCSET（已在 {total} 行语料中检索，无候选页）"]
        for term in terms:
            for gap in search.known_gaps(term.text):
                head.append(f"缺口台账命中：{gap.get('term')} —— {gap.get('action')}")
        head.append("→ 0 命中本身是证据：若属 B 型，可直接判定“手册未覆盖该能力”。")
        print("\n".join(head))
        return

    head.append(f"候选页（Σw·idf + 标题链加分，共 {len(pages)} 页）：")
    previous: PageScore | None = None
    for rank, item in enumerate(pages, start=1):
        label = f"{item.section} {item.title}".strip() or "（无小节标题）"
        adjacent = (
            previous is not None
            and previous.chapter == item.chapter
            and previous.section == item.section
            and item.page == previous.page + 1
        )
        head.append(
            f" {rank}. p.{item.page} [ch{item.chapter:02d}] {label}  "
            f"分 {item.score:.1f} 覆盖 {item.coverage:.0%}"
            + ("  ←连上一页（同小节续页）" if adjacent else "")
        )
        previous = item
    head.append("-" * 62)
    if guidelines:
        head.append("参数依据（param-guidelines.json）：")
        for item in guidelines[:6]:
            head.append(_fmt_guideline(item))
    print("\n".join(head))

    if args.full:
        index = EvidenceIndex(search)
        cap = args.page_lines if args.page_lines is not None else 120
        print("\n证据包（整页原文）：")
        for item in pages:
            print_page(search, index, f"ch{item.chapter:02d}", item.page, set(item.hits), cap)
    else:
        # 证据片段受总字符预算约束：预算按已打印的首部长度折算，保证整段输出可一次读完。
        budget = max(700, args.budget - len("\n".join(head)))
        cap = args.page_lines if args.page_lines is not None else 24
        print("证据（命中行片段，非结论）：")
        for index_page, item in enumerate(pages):
            if budget < 300 and index_page:
                print(f"\n（字符预算已用完，其余 {len(pages) - index_page} 页未打印：用 --page N 或 --budget 调整）")
                break
            lines, truncated = page_snippet(corpus, item, args.window, cap)
            while len(lines) > 4 and len("\n".join(lines)) > budget:
                lines = lines[: len(lines) - 4]
                truncated = True
            budget -= len("\n".join(lines)) + 80
            label = f"{item.section} {item.title}".strip()
            print(f"\n--- p.{item.page} {label} ---")
            print("\n".join(lines) if lines else "（该页无可用片段，请用 --full 或 --page 读取整页）")
            if truncated:
                print(
                    f"…（本页已截断或受字符预算限制；取全页请运行 python search_tool.py --page {item.page}）"
                )
    print("\n提示：以上为原页文本，非结论。请按分型标注 [手册 p.N] / [推理] / [未覆盖·判断]。")


if __name__ == "__main__":
    main()
