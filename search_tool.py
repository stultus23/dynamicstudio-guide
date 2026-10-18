#!/usr/bin/env python3
"""检索 DynamicStudio Users Guide 8.5 skill 中的本地资料。

设计要点（“索引优先 + 原文验证”检索层）：
  * 默认源为 ``auto``：先检索结构化索引，无命中时自动降级到 chapters/raw，并打印实际使用的来源。
  * ``--chapter`` 只在 chapters/raw/all（或 auto 且给了 --chapter）下生效，其余组合直接报错，不再静默忽略。
  * 匹配前对关键词与整行做空白归一化（合并多空格 / NBSP），修 PDF 抽取造成的漏检。
  * 0 命中输出 ``STATUS: NOT_FOUND_IN_DOCSET`` 并以退出码 3 结束，区分“没找到”与“文档没有”。
  * 页码锚点来自原文显式 ``PAGE|N`` 标记，零漂移；目录骨架来自 ``references/toc_full.json``。
  * 语料为 DynamicStudio 8.5；能力/术语不在语料时，由 ``references/corpus-gaps.json`` 台账给出结论性提示。

索引优先只是“先定位章节”，关键操作、参数与警告必须再读 ``raw`` 原文核实。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

INDEX_FILES = ("procedures.md", "dialogs.md", "troubleshooting.md", "glossary.md")
SOURCE_CHOICES = ("auto", "index", "chapters", "raw", "full", "all")
DEFAULT_SOURCE = "auto"
EXIT_NOT_FOUND = 3
PAGE_MARKER = re.compile(r"^PAGE\|(-?\d+)$")
_WS = re.compile(r"\s+")


def _norm(text: str) -> str:
    """空白归一化：合并多空格、NBSP，避免 PDF 抽取的空白差异造成漏检。"""
    return _WS.sub(" ", text.replace("\xa0", " ")).casefold()


@dataclass(frozen=True)
class SearchResult:
    source: str
    line: int
    page: int | None
    content: str
    context: tuple[str, ...]


class DynamicStudioSearch:
    def __init__(self, skill_dir: Path) -> None:
        self.skill_dir = skill_dir
        self.raw_dir = skill_dir / "raw"
        self.chapters_dir = skill_dir / "chapters"
        self.references_dir = skill_dir / "references"
        self.task_map_file = self.references_dir / "high-frequency-tasks.json"
        self.toc_path = self.references_dir / "toc_full.json"
        self.terms_path = self.references_dir / "zh-en-terms.json"
        self.gaps_path = self.references_dir / "corpus-gaps.json"

    # ------------------------------------------------------------- file sets ----
    def _index_files(self) -> tuple[Path, ...]:
        return tuple(self.skill_dir / name for name in INDEX_FILES if (self.skill_dir / name).exists())

    def _chapter_files(self, chapter: int | None) -> list[Path]:
        pattern = f"ch{chapter:02d}-*.md" if chapter is not None else "ch*.md"
        return sorted(self.chapters_dir.glob(pattern))

    def _raw_files(self, chapter: int | None) -> list[Path]:
        pattern = f"ch{chapter:02d}.txt" if chapter is not None else "ch*.txt"
        return sorted(self.raw_dir.glob(pattern))

    def _full_files(self) -> list[Path]:
        full_text = self.skill_dir / "full_text.txt"
        return [full_text] if full_text.exists() else []

    def _files_for_source(self, source: str, chapter: int | None) -> Iterable[Path]:
        if source == "index":
            return self._index_files()
        if source == "chapters":
            return self._chapter_files(chapter)
        if source == "raw":
            return self._raw_files(chapter)
        if source == "full":
            return self._full_files()
        raise ValueError(f"Unknown source: {source}")

    # ------------------------------------------------------------- scanning ----
    @staticmethod
    def _page_at(lines: list[str], line_index: int) -> int | None:
        for line in reversed(lines[: line_index + 1]):
            marker = PAGE_MARKER.fullmatch(line.strip())
            if marker:
                return int(marker.group(1))
        return None

    def _scan(self, keyword: str, paths: Iterable[Path], context_lines: int, *, with_page: bool) -> list[SearchResult]:
        needle = _norm(keyword)
        if not needle:
            return []
        results: list[SearchResult] = []
        for file_path in paths:
            if not file_path.is_file():
                continue
            lines = file_path.read_text(encoding="utf-8").splitlines()
            for index, line in enumerate(lines):
                if needle not in _norm(line):
                    continue
                start = max(0, index - context_lines)
                end = min(len(lines), index + context_lines + 1)
                results.append(
                    SearchResult(
                        source=file_path.relative_to(self.skill_dir).as_posix(),
                        line=index + 1,
                        page=self._page_at(lines, index) if with_page else None,
                        content=line.strip(),
                        context=tuple(lines[start:end]),
                    )
                )
        return results

    # ------------------------------------------------------------- task map ----
    def load_task_map(self) -> list[dict[str, object]]:
        """Load the maintained high-frequency task map and validate its minimal schema."""
        with self.task_map_file.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        tasks = payload.get("tasks")
        if not isinstance(tasks, list):
            raise ValueError("Task map must contain a 'tasks' list")
        return tasks

    def lookup_task(self, task_id: str) -> dict[str, object] | None:
        """Find a high-frequency task by its stable, case-insensitive identifier."""
        normalized = task_id.casefold()
        for task in self.load_task_map():
            if str(task.get("id", "")).casefold() == normalized:
                return task
        return None

    def _task_results(self, keyword: str, max_results: int) -> list[SearchResult]:
        needle = _norm(keyword)
        results: list[SearchResult] = []
        for number, task in enumerate(self.load_task_map(), start=1):
            if needle in _norm(json.dumps(task, ensure_ascii=False)):
                source = task.get("source", {})
                page = source.get("page") if isinstance(source, dict) else None
                curated = "（已校）" if task.get("curated") else ""
                results.append(
                    SearchResult(
                        "references/high-frequency-tasks.json",
                        number,
                        int(page) if isinstance(page, int) else None,
                        f"{task['id']}: {task['title']}{curated}",
                        (json.dumps(task, ensure_ascii=False),),
                    )
                )
                if len(results) >= max_results:
                    break
        return results

    # ------------------------------------------------------------------- TOC ----
    def toc(self) -> list[dict[str, object]]:
        if not self.toc_path.is_file():
            return []
        return json.loads(self.toc_path.read_text(encoding="utf-8")).get("entries", [])

    def outline(self, chapter: int) -> list[dict[str, object]]:
        return [entry for entry in self.toc() if int(entry["chapter"]) == chapter]

    def _toc_results(self, keyword: str, chapter: int | None, max_results: int) -> list[SearchResult]:
        needle = _norm(keyword)
        results: list[SearchResult] = []
        for number, entry in enumerate(self.toc(), start=1):
            if chapter is not None and int(entry["chapter"]) != chapter:
                continue
            section = str(entry["section"])
            if needle in _norm(str(entry["title"])) or needle in _norm(section):
                page = int(entry["page"]) if entry.get("page") is not None else None
                results.append(
                    SearchResult(
                        "toc",
                        number,
                        page,
                        f"{section} {entry['title']}  →  p.{page}",
                        (f"ch{int(entry['chapter']):02d}",),
                    )
                )
                if len(results) >= max_results:
                    break
        return results

    # --------------------------------------------------------- source search ----
    def _index_results(self, keyword: str, max_results: int, context_lines: int) -> list[SearchResult]:
        results = self._task_results(keyword, max_results)
        results.extend(self._scan(keyword, self._index_files(), context_lines, with_page=False))
        results.extend(self._toc_results(keyword, None, max_results))
        return results

    def search_with_mode(
        self,
        keyword: str,
        source: str = DEFAULT_SOURCE,
        chapter: int | None = None,
        context_lines: int = 2,
        max_results: int = 20,
    ) -> tuple[list[SearchResult], str]:
        """返回 (结果, 实际使用的模式)。source=auto 时先索引，无命中依次降级 chapters → raw。"""
        if source == "auto":
            scoped = chapter is not None
            if not scoped:
                hits = self._index_results(keyword, max_results, context_lines)
                if hits:
                    return hits, "index"
            hits = self._scan(keyword, self._chapter_files(chapter), context_lines, with_page=False)
            if hits:
                return hits, f"chapters (auto-fallback{', ch%d' % chapter if scoped else ''})"
            hits = self._scan(keyword, self._raw_files(chapter), context_lines, with_page=True)
            return hits, f"raw (auto-fallback{', ch%d' % chapter if scoped else ''})"

        results: list[SearchResult] = []
        if source in ("index", "all"):
            results.extend(self._index_results(keyword, max_results, context_lines))
        if source in ("chapters", "all"):
            results.extend(self._scan(keyword, self._chapter_files(chapter), context_lines, with_page=False))
        if source in ("raw", "all"):
            results.extend(self._scan(keyword, self._raw_files(chapter), context_lines, with_page=True))
        if source in ("full", "all"):
            results.extend(self._scan(keyword, self._full_files(), context_lines, with_page=True))
        return results, source

    def search_keyword(
        self,
        keyword: str,
        *,
        source: str = DEFAULT_SOURCE,
        chapter: int | None = None,
        context_lines: int = 2,
        max_results: int = 20,
    ) -> list[SearchResult]:
        """Case-insensitively search the selected source without loading unrelated sources."""
        return self.search_with_mode(keyword, source, chapter, context_lines, max_results)[0]

    # ---------------------------------------------------------- page / chapter ----
    def search_page(self, page_num: int, max_lines: int = 60) -> list[tuple[str, str]]:
        """Return page content for exact ``PAGE|N`` markers in the chapter originals."""
        marker = f"PAGE|{page_num}"
        results: list[tuple[str, str]] = []
        for file_path in self._raw_files(None):
            lines = file_path.read_text(encoding="utf-8").splitlines()
            for index, line in enumerate(lines):
                if line.strip() != marker:
                    continue
                page_content: list[str] = []
                for candidate in lines[index + 1 :]:
                    if PAGE_MARKER.fullmatch(candidate.strip()):
                        break
                    page_content.append(candidate)
                results.append((file_path.relative_to(self.skill_dir).as_posix(), "\n".join(page_content[:max_lines])))
        return results

    def chapter_stats(self) -> list[dict[str, object]]:
        stats: list[dict[str, object]] = []
        for file_path in self._raw_files(None):
            lines = file_path.read_text(encoding="utf-8").splitlines()
            stats.append(
                {
                    "file": file_path.relative_to(self.skill_dir).as_posix(),
                    "name": file_path.stem,
                    "lines": len(lines),
                    "pages": sum(bool(PAGE_MARKER.fullmatch(line.strip())) for line in lines),
                    "size_kb": round(file_path.stat().st_size / 1024, 1),
                }
            )
        return stats

    def search_chapter(self, chapter_num: int) -> dict[str, object]:
        """Return availability and basic statistics for a chapter."""
        chapter_files = list(self.chapters_dir.glob(f"ch{chapter_num:02d}-*.md"))
        raw_file = self.raw_dir / f"ch{chapter_num:02d}.txt"
        stats: dict[str, int] = {}
        if raw_file.exists():
            lines = raw_file.read_text(encoding="utf-8").splitlines()
            stats = {
                "total_lines": len(lines),
                "page_count": sum(bool(PAGE_MARKER.fullmatch(line.strip())) for line in lines),
                "file_size": raw_file.stat().st_size,
            }
        return {
            "chapter": chapter_num,
            "chapter_file": str(chapter_files[0]) if chapter_files else None,
            "raw_file": str(raw_file) if raw_file.exists() else None,
            "stats": stats,
        }

    # --------------------------------------------------------- term / gaps ----
    def terms(self) -> dict[str, str]:
        if not self.terms_path.is_file():
            return {}
        return json.loads(self.terms_path.read_text(encoding="utf-8")).get("terms", {})

    def expand(self, question: str) -> tuple[str, list[str], list[tuple[str, str]]]:
        """把中文问题按术语表展开为英文手册术语。返回 (展开串, 未收录中文词, 命中的映射)。"""
        table = self.terms()
        expanded = question
        matched: list[tuple[str, str]] = []
        for zh in sorted(table, key=len, reverse=True):
            if zh and zh in expanded:
                expanded = expanded.replace(zh, f" {table[zh]} ")
                matched.append((zh, table[zh]))
        leftovers = re.findall(r"[\u4e00-\u9fff]{2,}", expanded)
        return re.sub(r"\s+", " ", expanded).strip(), leftovers, matched

    def known_gaps(self, keyword: str) -> list[dict[str, object]]:
        if not self.gaps_path.is_file():
            return []
        needle = _norm(keyword)
        if not needle:
            return []
        gaps = json.loads(self.gaps_path.read_text(encoding="utf-8")).get("gaps", [])
        return [gap for gap in gaps if needle in _norm(str(gap.get("term", ""))) or needle in _norm(str(gap.get("aliases", "")))]


# ------------------------------------------------------------------ printing ----
def _print_results(results: list[SearchResult], show_context: bool, max_results: int) -> None:
    print(f"找到 {len(results)} 个结果；显示前 {min(max_results, len(results))} 个")
    for number, result in enumerate(results[:max_results], start=1):
        location = f"{result.source}:{result.line}"
        if result.page is not None:
            location += f" (p.{result.page})"
        print(f"\n{number}. [{location}]\n   {result.content[:220]}")
        if show_context:
            for line in result.context:
                print(f"   | {line.strip()}")


def _print_task(task: dict[str, object]) -> None:
    source = task["source"]
    assert isinstance(source, dict)
    chapter = source["chapter"]
    section = source["section"]
    page = source["page"]
    print(f"{task['title']} ({task['id']})")
    print(f"用途: {task['intent']}")
    print(f"原文核验: raw/ch{int(chapter):02d}.txt, {section}, p.{page}")
    print(f"建议检索: python search_tool.py \"{section}\" --source raw --chapter {chapter} --show-context")
    print(f"回答前应确认: {'；'.join(task['context_to_collect'])}")
    print(f"风险级别: {task['risk']}")


def _run_tests(search: DynamicStudioSearch) -> None:
    stats = search.chapter_stats()
    assert len(stats) == 20, f"应有 20 章原文，实得 {len(stats)}"
    assert sum(int(item["lines"]) for item in stats) >= 25000, "原文行数异常偏少"

    tasks = search.load_task_map()
    assert len(tasks) >= 20, "任务表必须覆盖至少 20 个高频任务"
    assert search.lookup_task("adaptive-piv"), "任务查询失败"

    # 索引路由
    assert search.search_keyword("Adaptive PIV", source="index"), "索引未命中 Adaptive PIV"
    # 原文 + --chapter 作用域
    hits = search.search_keyword("Adaptive PIV", source="raw", chapter=16)
    assert hits and all(hit.source == "raw/ch16.txt" for hit in hits), "--chapter 未限定 raw 到 ch16"
    # 页码锚点
    pages = search.search_page(130)
    assert len(pages) == 1 and pages[0][0] == "raw/ch13.txt", "精确页码查询失败"
    assert search.search_chapter(13)["raw_file"], "章节查询失败"

    # 空白归一化：双空格与单空格召回一致
    assert search.search_keyword("Grid  Step  Size", source="raw", chapter=16), "空白归一化失效"

    # auto 降级：只在原文出现的词（索引 0 命中）应被自动召回
    probe = "Burst"
    assert not search._index_results(probe, 5, 0), f"{probe} 应只在原文出现，用于验证降级"
    auto_hits, mode = search.search_with_mode(probe, "auto", None, 0)
    assert auto_hits, f"auto 源未召回 {probe}（应自动降级）"
    assert mode.startswith(("chapters", "raw")), mode

    # TOC 骨架
    assert len(search.toc()) >= 700, "TOC 骨架缺失或过小"
    assert search._toc_results("Calibration", None, 5), "TOC 未命中 Calibration"
    assert search.outline(16), "ch16 目录骨架为空"

    # 术语表与缺口台账
    assert len(search.terms()) >= 80, "术语表过小"
    assert search.known_gaps("device registration"), "缺口台账未命中 13.2.1"

    print("自检通过：20 章原文、任务/TOC 索引、--chapter 作用域、页码、空白归一化、auto 降级、术语表与缺口台账均可用。")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="检索 DynamicStudio 8.5 skill。默认 auto：先索引，无命中自动降级 chapters/raw。",
        epilog=(
            "示例：\n"
            '  python search_tool.py "Adaptive PIV"\n'
            '  python search_tool.py "Grid Step Size" --source raw --chapter 16 --context 3\n'
            '  python search_tool.py --task adaptive-piv\n'
            '  python search_tool.py --toc "Python Link"\n'
            '  python search_tool.py --outline 16\n'
            '  python search_tool.py -p 486\n'
            '  python search_tool.py -c 16'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", nargs="?", help="要检索的字面关键词或短语")
    parser.add_argument("-p", "--page", type=int, help="按精确打印页码读取原文")
    parser.add_argument("-c", "--chapter-info", type=int, help="查看章节文件和原文统计")
    parser.add_argument("--task", help="查看高频任务的原文定位、前提与风险")
    parser.add_argument("--toc", help="在目录骨架（722 条）中检索标题")
    parser.add_argument("--outline", type=int, help="打印某章的目录骨架（如 --outline 16）")
    parser.add_argument("--topics", action="store_true", help="打印中文→英文术语表")
    parser.add_argument("--gaps", action="store_true", help="打印语料缺口台账（corpus-gaps.json）")
    parser.add_argument("--stats", action="store_true", help="打印各章原文行数/页数")
    parser.add_argument("--source", choices=SOURCE_CHOICES, default=DEFAULT_SOURCE, help="检索来源；默认 auto")
    parser.add_argument("--chapter", type=int, help="将 chapters/raw 检索限定到该章节")
    parser.add_argument("--max-results", type=int, default=20, help="最多返回的命中数（默认 20）")
    parser.add_argument("--context", type=int, default=2, help="每个命中的上下文行数（默认 2）")
    parser.add_argument("--show-context", action="store_true", help="打印上下文")
    parser.add_argument("--test", action="store_true", help="运行内置可执行性检查")
    args = parser.parse_args()

    if args.max_results < 1 or args.context < 0:
        parser.error("--max-results 必须大于 0，--context 不能小于 0")
    if args.chapter is not None and not 1 <= args.chapter <= 20:
        parser.error("--chapter 必须在 1 到 20 之间")
    special_actions = sum(value is not None for value in (args.page, args.chapter_info, args.task, args.toc, args.outline))
    special_actions += sum(bool(value) for value in (args.topics, args.gaps, args.stats, args.test))
    if special_actions > 1:
        parser.error("--page/--chapter-info/--task/--toc/--outline/--topics/--gaps/--stats/--test 不能同时使用")
    if args.task and args.query:
        parser.error("--task 不能与关键词同时使用")

    search = DynamicStudioSearch(Path(__file__).resolve().parent)
    try:
        if args.test:
            _run_tests(search)
            return
        if args.stats:
            stats = search.chapter_stats()
            for item in stats:
                print(f"{item['name']}: {item['lines']} 行，{item['pages']} 个 PAGE 标记，{item['size_kb']} KB")
            print(f"合计：{sum(int(item['lines']) for item in stats)} 行")
            return
        if args.topics:
            table = search.terms()
            print(f"术语表：{len(table)} 条（references/zh-en-terms.json）")
            for zh, en in sorted(table.items()):
                print(f"  {zh}  →  {en}")
            return
        if args.gaps:
            if not search.gaps_path.is_file():
                print("（无缺口台账）")
                return
            data = json.loads(search.gaps_path.read_text(encoding="utf-8"))
            print(data.get("note", ""))
            for gap in data.get("gaps", []):
                print(f"\n- {gap.get('term')}  [{gap.get('kind')} / {gap.get('status')}]")
                print(f"  版本: {gap.get('inferred_version')}")
                print(f"  证据: {gap.get('evidence')}")
                print(f"  处置: {gap.get('action')}")
            return
        if args.outline is not None:
            entries = search.outline(args.outline)
            if not entries:
                print(f"（ch{args.outline:02d} 无目录骨架）")
                return
            for entry in entries:
                print(f"  p.{entry['page']:>4}  {entry['section']} {entry['title']}")
            print(f"共 {len(entries)} 条")
            return
        if args.page is not None:
            pages = search.search_page(args.page)
            print(f"找到 {len(pages)} 个页码命中")
            for source, content in pages:
                print(f"\n[{source}, p.{args.page}]\n{'-' * 60}\n{content}")
            return
        if args.chapter_info is not None:
            info = search.search_chapter(args.chapter_info)
            print(f"章节 {info['chapter']}\n摘要: {info['chapter_file']}\n原文: {info['raw_file']}\n统计: {info['stats']}")
            return
        if args.task:
            task = search.lookup_task(args.task)
            if task is None:
                parser.error(f"未找到任务 ID: {args.task}")
            _print_task(task)
            return

        # --chapter 作用域校验：仅 chapters/raw/all 生效（auto 会转成章内检索）
        source = args.source
        if args.chapter is not None and source in ("index", "full"):
            parser.error(f"--chapter 仅在 --source chapters/raw/all 下生效；请改用 --source raw --chapter {args.chapter}")

        if args.toc:
            results = search._toc_results(args.toc, None, args.max_results)
            _print_results(results, args.show_context, args.max_results)
            if not results:
                print("STATUS: NOT_FOUND_IN_DOCSET（TOC 骨架无匹配）")
                sys.exit(EXIT_NOT_FOUND)
            return

        if not args.query:
            parser.print_help()
            return

        results, used = search.search_with_mode(args.query, source, args.chapter, args.context, args.max_results)
        if source == "auto" and used.startswith(("chapters", "raw")):
            print(f"提示：索引无命中，已自动降级到 {used} 检索。")
        _print_results(results, args.show_context, args.max_results)
        if not results:
            searched = sum(int(item["lines"]) for item in search.chapter_stats())
            print(f"STATUS: NOT_FOUND_IN_DOCSET（已检索 {searched} 行；请改用英文术语或换关键词）")
            for gap in search.known_gaps(args.query):
                print(f"缺口台账命中：{gap.get('term')} —— {gap.get('action')}")
            sys.exit(EXIT_NOT_FOUND)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
