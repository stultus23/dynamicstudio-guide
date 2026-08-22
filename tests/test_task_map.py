"""Regression checks for high-frequency DynamicStudio task routing."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from search_tool import DynamicStudioSearch  # noqa: E402


class HighFrequencyTaskMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.search = DynamicStudioSearch(ROOT)
        cls.tasks = cls.search.load_task_map()

    def test_task_ids_are_unique_and_coverage_is_material(self) -> None:
        task_ids = [task["id"] for task in self.tasks]
        self.assertGreaterEqual(len(task_ids), 20)
        self.assertEqual(len(task_ids), len(set(task_ids)))

    def test_every_task_points_to_an_existing_section_and_page_marker(self) -> None:
        for task in self.tasks:
            with self.subTest(task=task["id"]):
                source = task["source"]
                chapter = source["chapter"]
                raw_file = ROOT / "raw" / f"ch{chapter:02d}.txt"
                raw_text = raw_file.read_text(encoding="utf-8")
                self.assertIn(source["section"], raw_text)
                self.assertIn(f"PAGE|{source['page']}", raw_text)

    def test_lookup_returns_the_expected_task(self) -> None:
        task = self.search.lookup_task("adaptive-piv")
        self.assertIsNotNone(task)
        self.assertEqual(task["source"]["chapter"], 16)


if __name__ == "__main__":
    unittest.main()
