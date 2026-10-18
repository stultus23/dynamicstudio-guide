"""Regression checks for the DynamicStudio 8.5 search layer (A-line fixes).

覆盖：auto 降级、--chapter 作用域、空白归一化、0 命中退出码、页码锚点、TOC 骨架、
术语表 / 缺口台账，以及高频任务表的 section+page 与原文/目录一致性。
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from search_tool import EXIT_NOT_FOUND, DynamicStudioSearch  # noqa: E402


class SearchLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.search = DynamicStudioSearch(ROOT)

    def test_auto_source_falls_back_for_raw_only_term(self) -> None:
        probe = "Burst"
        self.assertFalse(self.search._index_results(probe, 5, 0), "Burst 应只在原文出现，用于验证降级")
        results, mode = self.search.search_with_mode(probe, "auto", None, 0)
        self.assertTrue(results, "auto 源未召回只在原文出现的词")
        self.assertTrue(mode.startswith(("chapters", "raw")), mode)

    def test_chapter_scope_limits_raw_results(self) -> None:
        hits = self.search.search_keyword("Adaptive PIV", source="raw", chapter=16)
        self.assertTrue(hits)
        self.assertTrue(all(hit.source == "raw/ch16.txt" for hit in hits))

    def test_whitespace_normalization_matches_single_and_double_spaces(self) -> None:
        single = self.search.search_keyword("Grid Step Size", source="raw", chapter=16)
        double = self.search.search_keyword("Grid  Step  Size", source="raw", chapter=16)
        self.assertTrue(single)
        self.assertEqual(len(single), len(double), "空白归一化后双空格应与单空格召回一致")

    def test_zero_hit_returns_empty_list(self) -> None:
        self.assertEqual(self.search.search_keyword("zzzz_no_such_term_xyz", source="raw"), [])

    def test_page_lookup_uses_explicit_page_marker(self) -> None:
        pages = self.search.search_page(130)
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0][0], "raw/ch13.txt")

    def test_chapter_stats_cover_all_20_chapters(self) -> None:
        stats = self.search.chapter_stats()
        self.assertEqual(len(stats), 20)
        self.assertGreaterEqual(sum(int(item["lines"]) for item in stats), 25000)

    def test_toc_skeleton_is_complete_and_includes_toc_omitted_section(self) -> None:
        toc = self.search.toc()
        self.assertGreaterEqual(len(toc), 700, "TOC 骨架过小")
        by_section = {str(entry["section"]): entry for entry in toc}
        # 印刷目录漏列、由正文补录的小节
        self.assertIn("13.2.1", by_section)
        self.assertTrue(self.search.outline(16), "ch16 目录骨架为空")
        self.assertTrue(self.search._toc_results("Calibration", None, 5), "TOC 未命中 Calibration")

    def test_term_table_and_expand(self) -> None:
        table = self.search.terms()
        self.assertGreaterEqual(len(table), 80)
        expanded, _leftovers, matched = self.search.expand("查询窗口")
        self.assertIn("interrogation area", expanded)
        self.assertTrue(matched)

    def test_corpus_gaps_ledger(self) -> None:
        self.assertTrue(self.search.known_gaps("device registration"), "缺口台账应命中 13.2.1 条目的别名")
        self.assertTrue(self.search.known_gaps("13.2.1"))


class HighFrequencyTaskMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.search = DynamicStudioSearch(ROOT)
        cls.tasks = cls.search.load_task_map()
        cls.toc = {str(entry["section"]): entry for entry in cls.search.toc()}

    def test_task_ids_are_unique_and_coverage_is_material(self) -> None:
        task_ids = [task["id"] for task in self.tasks]
        self.assertGreaterEqual(len(task_ids), 20)
        self.assertEqual(len(task_ids), len(set(task_ids)))

    def test_every_task_section_and_page_align_with_raw_and_toc(self) -> None:
        for task in self.tasks:
            with self.subTest(task=task["id"]):
                source = task["source"]
                chapter = int(source["chapter"])
                section = str(source["section"])
                page = int(source["page"])
                num = section.split()[0]

                raw_text = (ROOT / "raw" / f"ch{chapter:02d}.txt").read_text(encoding="utf-8")
                self.assertIn(num, raw_text, "小节号应出现在本章原文中")
                entry = self.toc.get(num)
                self.assertIsNotNone(entry, f"目录骨架缺少小节 {num}")
                self.assertEqual(int(entry["page"]), page, "任务页码应与目录一致")
                self.assertEqual(int(entry["chapter"]), chapter)

    def test_lookup_returns_the_expected_task(self) -> None:
        task = self.search.lookup_task("adaptive-piv")
        self.assertIsNotNone(task)
        self.assertEqual(task["source"]["chapter"], 16)


class CliBehaviourTests(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, "search_tool.py", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )

    def test_self_test_exits_zero(self) -> None:
        proc = self._run("--test")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_zero_hit_exits_with_not_found_code(self) -> None:
        proc = self._run("zzzz_no_such_term_xyz", "--source", "raw")
        self.assertEqual(proc.returncode, EXIT_NOT_FOUND)
        self.assertIn("STATUS: NOT_FOUND_IN_DOCSET", proc.stdout)

    def test_chapter_with_index_source_is_rejected(self) -> None:
        proc = self._run("Adaptive PIV", "--source", "index", "--chapter", "16")
        self.assertEqual(proc.returncode, 2, "index 源不应静默忽略 --chapter")


if __name__ == "__main__":
    unittest.main()
