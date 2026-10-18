"""回归测试：ask.py 页锚错配 / 故障类分型 / 未收录词噪声 / 截断提示。

对应三类历史缺陷：
  P0  目录骨架只记小节**起始页**，直接取该页整页会读到上一小节的内容，
      使候选页“指向错误内容”，并可能让模型照抄并标注错页码。
  P1  故障类提问（报错/失败/异常）被误判成 A 或 C，导致在语料里空转；
      提问用语（怎么办、如何）被当成“主题词丢失”重复告警，掩盖真正的主题漂移。
  P2  证据包静默截断，容易把“打印不全”误读成“手册没写”。
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from search_tool import DynamicStudioSearch  # noqa: E402
import ask  # noqa: E402


class PageAnchorTests(unittest.TestCase):
    """P0：小节起始页 ≠ 该小节正文所在页，必须按 raw 页块校正。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.search = DynamicStudioSearch(ROOT)
        cls.index = ask.EvidenceIndex(cls.search)

    def test_section_spans_cover_multi_page_section(self) -> None:
        span = self.search.section_spans(16, "16.6")
        self.assertIsNotNone(span)
        first, last = span
        self.assertEqual(first, 485, "16.6 Adaptive PIV 起始页应仍为 p.485")
        self.assertGreater(last, first, "16.6 应跨多页")

    def test_section_span_excludes_next_sibling_section(self) -> None:
        span = self.search.section_spans(16, "16.6.1")
        self.assertIsNotNone(span)
        first, last = span
        self.assertLessEqual(last, first + 2, "子小节跨度不应吞掉后续大段内容")

    def test_candidate_pages_are_verified_against_raw_body(self) -> None:
        """核心回归：候选页正文必须真的包含检索术语，杜绝“指向上一小节”。"""
        expanded, _leftovers, _matched = self.search.expand("怎么设置自适应PIV的查询窗口")
        terms = sorted({term for term in ask._WORD.findall(expanded) if len(term) >= 3})
        self.assertIn("adaptive", [term.casefold() for term in terms])

        buckets = ask.collect(self.search, self.index, terms, None)
        self.assertTrue(buckets)

        ranked = sorted(
            buckets.items(),
            key=lambda kv: (
                not kv[1]["verified"],
                -ask.section_affinity(self.index, kv[0][0], kv[0][1], kv[1]["terms"]),
                -len(kv[1]["terms"]),
                kv[0][1],
            ),
        )
        (chapter, page), info = ranked[0]
        self.assertEqual(chapter, "ch16")
        body = ask._norm(self.index.body(16, page))
        for term in info["terms"]:
            self.assertIn(ask._norm(term), body, f"候选页 p.{page} 正文中不含术语 {term}")

    def test_adaptive_piv_section_body_found_on_documented_page(self) -> None:
        """16.6 的正文（含 Interrogation areas 说明）应从 p.485 起可检索到。"""
        pages = self.index.pages_with(16, "interrogation area")
        self.assertIn(485, pages, "16.6 小节正文应覆盖 p.485")
        self.assertIn(486, pages, "16.6.1 的 IA 说明在 p.486")


class ClassificationTests(unittest.TestCase):
    """P1：故障类提问必须走推理路径，而不是被要求去原文找一句不存在的结论。"""

    def test_exception_question_is_troubleshooting(self) -> None:
        kind, _ = ask.classify("DatasetException Dataset.LoadFile failed to deserialize OK 为什么")
        self.assertEqual(kind, "D")

    def test_failure_question_without_why_keyword_is_troubleshooting(self) -> None:
        for question in ("PIV 采集失败", "标定精度不够怎么办", "数据加载报错", "相机无法连接"):
            with self.subTest(question=question):
                kind, _ = ask.classify(question)
                self.assertEqual(kind, "D", question)

    def test_pure_howto_stays_verification_type(self) -> None:
        kind, _ = ask.classify("怎么设置自适应PIV的查询窗口")
        self.assertEqual(kind, "A")

    def test_pure_theory_stays_reasoning_type(self) -> None:
        kind, _ = ask.classify("双相机不同触发率为什么能同步")
        self.assertEqual(kind, "B")


class LeftoverNoiseTests(unittest.TestCase):
    """P1：提问用语不应触发“主题词丢失”告警。"""

    def test_interrogative_phrases_are_filtered(self) -> None:
        self.assertEqual(ask.filter_leftovers(["怎么设置"]), [])
        self.assertEqual(ask.filter_leftovers(["怎么办"]), [])
        self.assertEqual(ask.filter_leftovers(["为什么"]), [])

    def test_topic_nouns_survive_filtering(self) -> None:
        kept = ask.filter_leftovers(["精度不够怎么办"])
        self.assertEqual(kept, ["精度"], "真正的主题词必须保留，否则告警失去意义")

    def test_mixed_leftover_keeps_only_topic(self) -> None:
        self.assertIn("标定", ask.filter_leftovers(["标定怎么办"]))


class EvidenceOutputTests(unittest.TestCase):
    """P2：截断必须显式提示，且默认页文本上限要够用。"""

    def _run_ask(self, *args: str) -> subprocess.CompletedProcess:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / "ask.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )

    def test_truncation_is_announced(self) -> None:
        proc = self._run_ask("自适应 PIV 的 Validation 设置", "--top-pages", "1", "--page-lines", "5")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("本页已截断", proc.stdout)
        self.assertIn("search_tool.py --page", proc.stdout)

    def test_default_page_lines_is_generous(self) -> None:
        proc = self._run_ask("自适应 PIV 的 Validation 设置", "--top-pages", "1")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("p.4", proc.stdout)

    def test_verified_pages_have_no_terms_missing_warning(self) -> None:
        proc = self._run_ask("怎么设置自适应PIV的查询窗口", "--top-pages", "2")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("该页正文未出现术语", proc.stdout, "已校验页不应再报术语缺失")


if __name__ == "__main__":
    unittest.main()
