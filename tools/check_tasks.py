#!/usr/bin/env python3
"""校验高频任务表：确认每条任务的 section + page 能在原文/目录骨架中对上，并回写 curated 标记。

用法：
    python tools/check_tasks.py            # 只报告
    python tools/check_tasks.py --apply    # 把通过校验的任务 curated 置 true

判定（三项全过才算通过）：
  chapter 存在   = raw/chNN.txt 存在，且 section 首段号属于该章
  目录页一致     = references/toc_full.json 中该小节号存在，且其打印页 == 任务声明的 page
  原文可检索     = section 的小节号出现在该章 raw 原文里

退出码：0 全部通过；5 存在未通过项。
"""
from __future__ import annotations

import argparse
import json
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

TASKS_PATH = SKILL_DIR / "references" / "high-frequency-tasks.json"
EXIT_UNRESOLVED = 5


def main() -> None:
    parser = argparse.ArgumentParser(description="校验高频任务表")
    parser.add_argument("--apply", action="store_true", help="把通过校验的任务 curated 置 true")
    args = parser.parse_args()

    search = DynamicStudioSearch(SKILL_DIR)
    toc = {str(entry["section"]): entry for entry in search.toc()}
    data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    tasks = data["tasks"]

    unresolved = 0
    for task in tasks:
        source = task["source"]
        chapter = int(source["chapter"])
        section = str(source["section"])
        page = int(source["page"])
        num = section.split()[0]
        reasons: list[str] = []

        raw_file = SKILL_DIR / "raw" / f"ch{chapter:02d}.txt"
        if not raw_file.is_file():
            reasons.append(f"raw/ch{chapter:02d}.txt 不存在")
            raw_text = ""
        else:
            raw_text = raw_file.read_text(encoding="utf-8")

        if num.split(".")[0] != str(chapter):
            reasons.append(f"section 号 {num} 不属于第 {chapter} 章")

        entry = toc.get(num)
        if entry is None:
            reasons.append(f"目录骨架中查无小节号 {num}")
        elif int(entry["page"]) != page:
            reasons.append(f"目录页不一致：toc={entry['page']} 任务={page}")
        elif int(entry["chapter"]) != chapter:
            reasons.append(f"目录章不一致：toc=ch{entry['chapter']} 任务=ch{chapter}")

        if num not in raw_text:
            reasons.append(f"原文中找不到小节号 {num}")

        passed = not reasons
        if passed:
            task["curated"] = True
            mark = "OK   "
        else:
            unresolved += 1
            mark = "FAIL "
        print(f"  {mark} {task['id']:<28} ch{chapter:02d}:{num:<8} p.{page:<5} curated={task.get('curated')}  {'; '.join(reasons)}")

    if args.apply:
        TASKS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\n已回写 {TASKS_PATH.relative_to(SKILL_DIR)}。")

    print(f"\n共 {len(tasks)} 条，未通过 {unresolved} 条。")
    if unresolved:
        sys.exit(EXIT_UNRESOLVED)


if __name__ == "__main__":
    main()
