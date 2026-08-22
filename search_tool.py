#!/usr/bin/env python3
"""检索 DynamicStudio Users Guide 8.5 skill 中的本地资料。

默认仅检索索引，以便先定位章节；关键操作、参数与警告必须再以 ``raw``
来源核验。全文检索是显式的最后兜底，避免重复扫描整本手册。
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
SOURCE_CHOICES = ("index", "chapters", "raw", "full", "all")
PAGE_MARKER = re.compile(r"^PAGE\|(\d+)$")
TASK_MAP_FILE = Path("references") / "high-frequency-tasks.json"


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
        self.task_map_file = skill_dir / TASK_MAP_FILE

    def _files_for_source(self, source: str, chapter: int | None) -> Iterable[Path]:
        if source == "index":
            return (self.skill_dir / name for name in INDEX_FILES if (self.skill_dir / name).exists())
        if source == "chapters":
            pattern = f"ch{chapter:02d}-*.md" if chapter is not None else "ch*.md"
            return sorted(self.chapters_dir.glob(pattern))
        if source == "raw":
            pattern = f"ch{chapter:02d}.txt" if chapter is not None else "ch*.txt"
            return sorted(self.raw_dir.glob(pattern))
        if source == "full":
            full_text = self.skill_dir / "full_text.txt"
            return (full_text,) if full_text.exists() else ()
        raise ValueError(f"Unknown source: {source}")

    @staticmethod
    def _page_at(lines: list[str], line_index: int) -> int | None:
        for line in reversed(lines[: line_index + 1]):
            marker = PAGE_MARKER.fullmatch(line.strip())
            if marker:
                return int(marker.group(1))
        return None

    def search_keyword(
        self,
        keyword: str,
        *,
        source: str = "index",
        chapter: int | None = None,
        context_lines: int = 2,
        max_results: int = 20,
    ) -> list[SearchResult]:
        """Case-insensitively search the selected source without loading unrelated sources."""
        sources = SOURCE_CHOICES[:-1] if source == "all" else (source,)
        needle = keyword.casefold()
        results: list[SearchResult] = []

        for selected_source in sources:
            for file_path in self._files_for_source(selected_source, chapter):
                lines = file_path.read_text(encoding="utf-8").splitlines()
                for index, line in enumerate(lines):
                    if needle not in line.casefold():
                        continue
                    start = max(0, index - context_lines)
                    end = min(len(lines), index + context_lines + 1)
                    results.append(
                        SearchResult(
                            source=file_path.relative_to(self.skill_dir).as_posix(),
                            line=index + 1,
                            page=self._page_at(lines, index),
                            content=line.strip(),
                            context=tuple(lines[start:end]),
                        )
                    )
                    if len(results) >= max_results:
                        return results
        return results

    def search_page(self, page_num: int, max_lines: int = 50) -> list[tuple[str, str]]:
        """Return page content for exact ``PAGE|N`` markers in the chapter originals."""
        marker = f"PAGE|{page_num}"
        results: list[tuple[str, str]] = []
        for file_path in self._files_for_source("raw", chapter=None):
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
            if task.get("id", "").casefold() == normalized:
                return task
        return None


def _print_results(results: list[SearchResult], show_context: bool) -> None:
    print(f"找到 {len(results)} 个结果")
    for number, result in enumerate(results, start=1):
        location = f"{result.source}:{result.line}"
        if result.page is not None:
            location += f" (p.{result.page})"
        print(f"\n{number}. [{location}]\n   {result.content}")
        if show_context:
            for line in result.context:
                print(f"   | {line}")


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
    assert search.search_keyword("Adaptive PIV", source="index"), "index search returned no result"
    assert search.search_keyword("Adaptive PIV", source="raw", chapter=16), "chapter-scoped raw search returned no result"
    assert search.search_keyword("Adaptive PIV", source="chapters", chapter=16), "chapter summary search returned no result"
    pages = search.search_page(130)
    assert len(pages) == 1 and pages[0][0] == "raw/ch13.txt", "exact page lookup failed"
    info = search.search_chapter(13)
    assert info["raw_file"] and info["chapter_file"], "chapter lookup failed"
    tasks = search.load_task_map()
    assert len(tasks) >= 20, "task map must cover at least 20 high-frequency tasks"
    assert search.lookup_task("adaptive-piv"), "task lookup failed"
    print("All search-tool checks passed.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="检索 DynamicStudio 8.5 skill。默认检索索引；操作细节须再检索 raw 原文。",
        epilog=(
            '示例：\n'
            '  python search_tool.py "Adaptive PIV"\n'
            '  python search_tool.py "Grid Step Size" --source raw --chapter 16 --context 3\n'
            '  python search_tool.py --task adaptive-piv\n'
            '  python search_tool.py -p 486\n'
            '  python search_tool.py -c 16'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", nargs="?", help="要检索的字面关键词或短语")
    parser.add_argument("-p", "--page", type=int, help="按精确打印页码读取原文")
    parser.add_argument("-c", "--chapter-info", type=int, help="查看章节文件和原文统计")
    parser.add_argument("--task", help="查看高频任务的原文定位、前提与风险")
    parser.add_argument("--source", choices=SOURCE_CHOICES, default="index", help="检索来源；默认 index")
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
    special_actions = sum(value is not None for value in (args.page, args.chapter_info, args.task))
    if special_actions > 1:
        parser.error("--page、--chapter-info 与 --task 不能同时使用")
    if args.task and args.query:
        parser.error("--task 不能与关键词同时使用")

    search = DynamicStudioSearch(Path(__file__).resolve().parent)
    if args.test:
        _run_tests(search)
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
    if not args.query:
        parser.print_help()
        return

    results = search.search_keyword(
        args.query,
        source=args.source,
        chapter=args.chapter,
        context_lines=args.context,
        max_results=args.max_results,
    )
    _print_results(results, args.show_context)
    if not results and args.source != "full":
        print("\n未命中。可改用 --source chapters/raw（必要时加 --chapter）；仅在仍无命中时使用 --source full。")


if __name__ == "__main__":
    main()
