#!/usr/bin/env python3
"""术语回写：把 AI 自行识别出的中文→英文术语并回 references/zh-en-terms.json。

关键约束：英文值必须能在 raw 原文中检索到，否则拒收（防止把“记忆里的词”写进表里，
导致 tools/ask.py 用不存在的英文术语去检索、把 0 命中当正常）。

用法：
    # 只看会写什么，不落盘（默认）
    python tools/merge_terms.py --add "体视标定=stereo calibration"
    python tools/merge_terms.py --from pending.json

    # 真正并回
    python tools/merge_terms.py --add "体视标定=stereo calibration" --apply

pending.json 格式：
    {"体视标定": "stereo calibration", "图像对": "image pair"}

退出码：0 全部通过；4 有词条因“原文查无”被拒收。
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
TERMS_PATH = SKILL_DIR / "references" / "zh-en-terms.json"

_WS = re.compile(r"\s+")
EXIT_REJECTED = 4


def _norm(text: str) -> str:
    return _WS.sub(" ", text.replace("\xa0", " ")).casefold().strip()


def load_corpus() -> dict[str, str]:
    corpus = {}
    for path in sorted(RAW_DIR.glob("*.txt")):
        corpus[path.name] = _norm(path.read_text(encoding="utf-8"))
    return corpus


def verify(english: str, corpus: dict[str, str]) -> tuple[bool, str]:
    needle = _norm(english)
    if not needle:
        return False, "空值"
    if len(needle) < 3:
        return False, "过短（<3 字符），可能是误识别"
    docs = [name for name, text in corpus.items() if needle in text]
    if docs:
        return True, f"命中 {len(docs)} 章：" + ", ".join(docs[:3]) + ("..." if len(docs) > 3 else "")
    return False, "全部 raw 章节均未命中"


def parse_pairs(args: argparse.Namespace) -> dict[str, str]:
    pending: dict[str, str] = {}
    if args.from_:
        pending.update(json.loads(Path(args.from_).read_text(encoding="utf-8")))
    for raw in args.add or []:
        if "=" not in raw:
            raise SystemExit(f"--add 需要 “中文=english” 形式，收到：{raw}")
        zh, en = raw.split("=", 1)
        pending[zh.strip()] = en.strip()
    return pending


def main() -> None:
    parser = argparse.ArgumentParser(description="术语回写（英文值须通过原文校验）")
    parser.add_argument("--add", action="append", metavar="中文=english", help="可重复")
    parser.add_argument("--from", dest="from_", metavar="FILE", help="从 JSON 文件读入待并入词条")
    parser.add_argument("--apply", action="store_true", help="通过校验后写回 zh-en-terms.json")
    parser.add_argument("--force", action="store_true", help="对“原文查无”的词条也强制写入（会在值后加 ? 标记）")
    args = parser.parse_args()

    pending = parse_pairs(args)
    if not pending:
        parser.error("请用 --add 或 --from 提供至少一条词条")

    corpus = load_corpus()
    data = json.loads(TERMS_PATH.read_text(encoding="utf-8"))
    terms: dict[str, str] = data.setdefault("terms", {})

    accepted: dict[str, str] = {}
    rejected: list[tuple[str, str, str]] = []
    for zh, en in pending.items():
        if zh in terms and terms[zh] == en:
            print(f"  = 已有  {zh} → {en}（跳过）")
            continue
        ok, reason = verify(en, corpus)
        if ok:
            accepted[zh] = en
            print(f"  + 收录  {zh} → {en}   [{reason}]")
        elif args.force:
            accepted[zh] = f"{en}?"
            print(f"  ! 强制  {zh} → {en}?  [{reason}]（已加 ? 标记待核）")
        else:
            rejected.append((zh, en, reason))
            print(f"  x 拒收  {zh} → {en}   [{reason}]")

    if accepted and args.apply:
        terms.update(accepted)
        TERMS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\n已写回 {TERMS_PATH.relative_to(SKILL_DIR)}：新增 {len(accepted)} 条，共 {len(terms)} 条。")
    elif accepted:
        print(f"\n（演练模式）{len(accepted)} 条通过校验，未落盘。加 --apply 写回。")

    if rejected:
        print(f"\n{len(rejected)} 条被拒收（原文查无）。逐条复核后重试，或用 --force 标记待核。")
        sys.exit(EXIT_REJECTED)


if __name__ == "__main__":
    main()
