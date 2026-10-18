#!/usr/bin/env python3
"""抽取 DynamicStudio 8.5 手册的目录骨架，生成 references/toc_full.json。

数据来源（优先级）：
  1. ``full_text.txt`` 中的官方印刷目录（"Table of Content"，标题一行、页码一行）。
     它是权威目录，页码与纸质版一致，用于 --toc / --outline 路由。
  2. ``raw/chNN.txt`` 中的小节标题，用于补录官方印刷目录**漏列**的小节
     （已发现：印刷目录漏列 13.2.1，而正文 p.141 存在）。

抽取时会跳过小节列表（正文开头的"章节内含小节清单"，形如标题后紧跟一个纯数字行），
避免把清单行误当成真正的标题行。

用法：
    python tools/build_toc.py            # 生成/覆盖 references/toc_full.json
    python tools/build_toc.py --check    # 只打印统计，不写文件
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
FULL_TEXT = SKILL_DIR / "full_text.txt"
RAW_DIR = SKILL_DIR / "raw"
OUT_PATH = SKILL_DIR / "references" / "toc_full.json"

_TOC_HEAD = re.compile(r"^Table of Content$")
_SECTION = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){0,3})\s+(\S.{0,100})$")
_PAGE_MARKER = re.compile(r"^PAGE\|(-?\d+)$")
_PAGE_NUM = re.compile(r"^\d{1,4}$")


def _clean(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip(" .\t")


def parse_printed_toc(lines: list[str]) -> list[dict]:
    start = next((i for i, line in enumerate(lines) if _TOC_HEAD.match(line.strip())), None)
    if start is None:
        raise ValueError("full_text.txt 中未找到 Table of Content")
    entries: list[dict] = []
    index = start + 1
    while index < len(lines) - 1:
        stripped = lines[index].strip()
        marker = _PAGE_MARKER.match(stripped)
        if marker:
            if int(marker.group(1)) >= 17:  # 正文从打印页 17 开始
                break
            index += 1
            continue
        match = _SECTION.match(stripped)
        following = lines[index + 1].strip() if index + 1 < len(lines) else ""
        if match and _PAGE_NUM.match(following):
            section = match.group(1)
            entries.append({"chapter": int(section.split(".")[0]), "section": section, "title": _clean(match.group(2)), "page": int(following)})
            index += 2
            continue
        index += 1
    return entries


def parse_raw_headings() -> list[dict]:
    """抽取正文小节标题；跳过"章节内含小节清单"（标题后紧跟纯数字行）。"""
    entries: list[dict] = []
    for path in sorted(RAW_DIR.glob("ch*.txt")):
        chapter = int(re.search(r"ch(\d+)", path.name).group(1))
        lines = path.read_text(encoding="utf-8").splitlines()
        page: int | None = None
        index = 0
        while index < len(lines):
            stripped = lines[index].strip()
            marker = _PAGE_MARKER.match(stripped)
            if marker:
                page = int(marker.group(1))
                index += 1
                continue
            match = _SECTION.match(stripped)
            if match and match.group(1).split(".")[0] == str(chapter):
                following = lines[index + 1].strip() if index + 1 < len(lines) else ""
                if _PAGE_NUM.match(following):  # 这是清单行，不是正文标题
                    index += 1
                    continue
                entries.append({"chapter": chapter, "section": match.group(1), "title": _clean(match.group(2)), "page": page})
            index += 1
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="抽取 DynamicStudio 8.5 目录骨架")
    parser.add_argument("--check", action="store_true", help="只统计，不写文件")
    args = parser.parse_args()

    lines = FULL_TEXT.read_text(encoding="utf-8").splitlines()
    printed = parse_printed_toc(lines)
    raw = parse_raw_headings()

    by_section = {entry["section"]: entry for entry in printed}
    supplemented = []
    for entry in raw:
        if entry["section"] not in by_section:
            by_section[entry["section"]] = entry
            supplemented.append(entry)

    entries = sorted(by_section.values(), key=lambda e: [int(part) for part in e["section"].split(".")])
    print(f"印刷目录条目: {len(printed)}")
    print(f"正文标题条目: {len(raw)}")
    print(f"补录（印刷目录漏列）: {len(supplemented)}")
    for entry in supplemented:
        print(f"  + {entry['section']}  p.{entry['page']}  {entry['title'][:60]}")
    print(f"合计: {len(entries)} 条")

    if args.check:
        return
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_from": "full_text.txt 印刷目录 + raw/ 正文标题补录",
        "note": "标题 → 打印页码骨架，用于 --toc / --outline 路由；命中的标题仍需回 raw 原文核实内容。",
        "entries": entries,
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"已写入 {OUT_PATH.relative_to(SKILL_DIR)}")


if __name__ == "__main__":
    main()
