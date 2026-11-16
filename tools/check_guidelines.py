#!/usr/bin/env python3
"""校验 references/param-guidelines.json：每条依据是否真的站得住。

检查项：
  1. 结构：id 唯一、source ∈ {manual, judgement}、rule 非空。
  2. manual：manual_refs 必须是 ``p.N``；页码在 raw 原文里存在；该页正文必须至少出现
     params / zh 里的一个词（否则“页码—内容”对不上，属于编造出处）。
  3. judgement：必须有 applies_when 与 overturn_when（推翻条件），否则经验规则会被当成默认值。
  4. 覆盖率：条目数 ≥ 15，且 manual 与 judgement 都有。

退出码：0 全部通过；4 有失败项。
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
RAW_DIR = SKILL_DIR / "raw"
GUIDELINES = SKILL_DIR / "references" / "param-guidelines.json"
PAGE_MARKER = re.compile(r"^PAGE\|(-?\d+)$")
_WS = re.compile(r"\s+")
EXIT_FAILED = 4
MIN_ITEMS = 15


def _norm(text: str) -> str:
    return _WS.sub(" ", text.replace("\xa0", " ")).casefold()


class Pages:
    def __init__(self) -> None:
        self.blocks: dict[int, str] = {}
        for path in sorted(RAW_DIR.glob("*.txt")):
            current: int | None = None
            buffer: list[str] = []
            for line in path.read_text(encoding="utf-8").splitlines():
                marker = PAGE_MARKER.fullmatch(line.strip())
                if marker:
                    if current is not None:
                        self.blocks.setdefault(current, _norm("\n".join(buffer)))
                    current = int(marker.group(1))
                    buffer = []
                elif current is not None:
                    buffer.append(line)
            if current is not None:
                self.blocks.setdefault(current, _norm("\n".join(buffer)))

    def text(self, page: int) -> str:
        return self.blocks.get(page, "")


def check(skill_dir: Path = SKILL_DIR) -> list[str]:
    problems: list[str] = []
    path = skill_dir / "references" / "param-guidelines.json"
    if not path.is_file():
        return [f"缺少 {path.name}"]
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items", [])
    if len(items) < MIN_ITEMS:
        problems.append(f"条目只有 {len(items)} 条，少于 {MIN_ITEMS} 条")
    if not any(item.get("source") == "manual" for item in items):
        problems.append("没有任何 source=manual 的条目")
    if not any(item.get("source") == "judgement" for item in items):
        problems.append("没有任何 source=judgement 的条目")

    pages = Pages()
    seen: set[str] = set()
    for item in items:
        item_id = str(item.get("id", "")).strip()
        if not item_id:
            problems.append(f"条目缺 id：{item}")
            continue
        if item_id in seen:
            problems.append(f"id 重复：{item_id}")
        seen.add(item_id)
        source = item.get("source")
        if source not in ("manual", "judgement"):
            problems.append(f"{item_id}: source 必须是 manual/judgement，实得 {source!r}")
        if not str(item.get("rule", "")).strip():
            problems.append(f"{item_id}: rule 为空")

        if source == "judgement":
            for field in ("applies_when", "overturn_when"):
                if not str(item.get(field, "")).strip():
                    problems.append(f"{item_id}: judgement 条目缺 {field}")
            continue

        refs = item.get("manual_refs") or []
        if not refs:
            problems.append(f"{item_id}: manual 条目缺 manual_refs")
            continue
        keywords = [w for w in list(item.get("params", [])) + list(item.get("zh", [])) if w]
        for ref in refs:
            match = re.fullmatch(r"p\.(\d+)", str(ref).strip())
            if not match:
                problems.append(f"{item_id}: 页码格式必须是 p.N，实得 {ref!r}")
                continue
            page = int(match.group(1))
            body = pages.text(page)
            if not body:
                problems.append(f"{item_id}: p.{page} 在 raw 原文中不存在")
                continue
            if keywords and not any(_norm(word) in body for word in keywords):
                problems.append(
                    f"{item_id}: p.{page} 正文没有出现任何 params/zh 关键词（{', '.join(keywords[:3])}…），页码与内容对不上"
                )
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description="校验参数推荐依据的页码与内容一致性")
    parser.add_argument("--quiet", action="store_true", help="只输出失败项")
    args = parser.parse_args()

    problems = check()
    if not args.quiet:
        payload = json.loads(GUIDELINES.read_text(encoding="utf-8"))
        items = payload.get("items", [])
        manual = sum(1 for item in items if item.get("source") == "manual")
        print(f"param-guidelines.json：{len(items)} 条（manual {manual} / judgement {len(items) - manual}）")
    if problems:
        print(f"\n{len(problems)} 项不合格：")
        for problem in problems:
            print(f"  x {problem}")
        sys.exit(EXIT_FAILED)
    print("校验通过：页码存在、页码与关键词一致、judgement 条目都写了适用与推翻条件。")


if __name__ == "__main__":
    main()
