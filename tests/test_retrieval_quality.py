"""检索质量回归测试：金标准问题 → 期望页集合。

用子进程跑 ``tools/ask.py``，解析候选页（优先 ``--json``，不支持时退回文本行）。
断言：top3 = 13/13，top1 ≥ 11/13；分型断言；默认输出长度与单次运行时间上限。

这些用例是“整体检索链路是否退化”的唯一量化口径，改动排名/术语/分型后必须先跑它。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASK = ROOT / "tools" / "ask.py"
GOLDEN = Path(__file__).resolve().parent / "golden_queries.json"

_PAGE_LINE = re.compile(r"p\.(\d+)")

# 门槛（见优化规格第 6 节）：top3 全中，top1 允许 2 条偏差。
MIN_TOP3 = 13
MIN_TOP1 = 11


def run_ask(question: str, *extra: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(ASK), question, *extra],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def candidate_pages(question: str, limit: int = 3) -> tuple[list[int], str]:
    """返回 (候选页序列, 分型)。优先解析 --json，退化到文本行。"""
    proc = run_ask(question, "--json")
    if proc.returncode == 0 and proc.stdout.lstrip().startswith("{"):
        payload = json.loads(proc.stdout)
        pages = [int(item["page"]) for item in payload.get("pages", [])[:limit]]
        return pages, str(payload.get("kind", ""))
    proc = run_ask(question)
    if proc.returncode != 0:
        raise AssertionError(f"ask.py 失败：{question}\n{proc.stderr}")
    pages: list[int] = []
    in_list = False
    for line in proc.stdout.splitlines():
        if "候选页" in line:
            in_list = True
            continue
        if in_list and line.startswith(("=", "证据")):
            break
        if in_list:
            match = _PAGE_LINE.search(line)
            if match:
                pages.append(int(match.group(1)))
    kind = ""
    for line in proc.stdout.splitlines():
        if line.startswith("分型："):
            kind = line.split("：", 1)[1].strip()[:1]
            break
    return pages[:limit], kind


class GoldenRetrievalTests(unittest.TestCase):
    """金标准问题集的 top1 / top3 命中率。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads(GOLDEN.read_text(encoding="utf-8"))

    def test_top1_and_top3_rates(self) -> None:
        top1 = 0
        top3 = 0
        failures: list[str] = []
        for case in self.cases:
            pages, _kind = candidate_pages(case["q"])
            expect = set(case["expect"])
            if pages and pages[0] in expect:
                top1 += 1
            else:
                failures.append(f"top1 未中：{case['q']} → {pages[:3]}，期望 {sorted(expect)}")
            if expect & set(pages):
                top3 += 1
            else:
                failures.append(f"top3 全脱：{case['q']} → {pages[:3]}，期望 {sorted(expect)}")
        total = len(self.cases)
        print(f"\n检索质量：top1 = {top1}/{total}，top3 = {top3}/{total}")
        for failure in failures:
            print("  - " + failure)
        self.assertGreaterEqual(top3, MIN_TOP3, "；".join(failures))
        self.assertGreaterEqual(top1, MIN_TOP1, "；".join(failures))


class ClassificationAssertionTests(unittest.TestCase):
    """分型修正：疑问结构不得被判成故障型；推荐/确认类应独立成 E 型。"""

    def test_synonym_question_is_not_troubleshooting(self) -> None:
        _pages, kind = candidate_pages("能不能用两台相机同步")
        self.assertNotEqual(kind, "D", "“能不能”不是故障信号")

    def test_peak_locking_question_is_troubleshooting(self) -> None:
        _pages, kind = candidate_pages("peak locking 怎么解决")
        self.assertEqual(kind, "D")

    def test_interrogation_area_size_question_is_recommendation(self) -> None:
        _pages, kind = candidate_pages("IA 用 32x32 合适吗")
        self.assertEqual(kind, "E")


class OutputBudgetTests(unittest.TestCase):
    """默认输出必须短到能一次读完，且单次调用足够快。"""

    def test_default_output_is_compact(self) -> None:
        question = "Adaptive PIV 的 Grid Step Size 是什么"
        start = time.perf_counter()
        proc = run_ask(question)
        elapsed = time.perf_counter() - start
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertLessEqual(len(proc.stdout), 4000, f"默认输出 {len(proc.stdout)} 字符，超出 4,000 上限")
        self.assertLessEqual(elapsed, 1.5, f"单次 ask.py 用时 {elapsed:.2f}s，超出 1.5s 上限")

    def test_output_states_confidence(self) -> None:
        proc = run_ask("Adaptive PIV 的 Grid Step Size 是什么")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("置信度：", proc.stdout, "必须给出可停止信号")


if __name__ == "__main__":
    unittest.main()
