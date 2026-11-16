# 检索工具参考

技能根目录记作 `$S`（`<本 SKILL.md 所在目录>`）。所有脚本只在 Python 标准库上运行。

## tools/ask.py — 问题入口（首选）

```
python "$S/tools/ask.py" "<中文问题>" [选项]
```

它做四件事：分型 → 中文术语展开（含短语）→ Σw·idf + 标题链打分 → 只打印命中行片段并给出置信度。

| 选项 | 默认 | 说明 |
|---|---|---|
| `--top-pages N` | 3 | 候选页数量；同一小节最多 2 页 |
| `--page-lines N` | 片段 24 / 整页 120 | 每页最多打印的行数 |
| `--window N` | 6 | 命中行上下各取几行 |
| `--budget N` | 3400 | 整段输出的字符预算（含首部），超出即截断并在末尾提示 |
| `--full` | 关 | 打印整页（旧行为），用于需要完整上下文的核对 |
| `--chapter N` | — | 限定章节 1–20 |
| `--json` | 关 | 结构化输出，字段见下 |

### --json 字段

```json
{
  "question": "...", "kind": "A|B|C|D|E", "advice": "...",
  "confidence": {"level": "高|中|低", "reason": "..."},
  "terms": [{"term": "...", "kind": "phrase|zh|word", "weight": 2.0, "idf": 6.31}],
  "leftovers": ["未收录的中文词"],
  "guidelines": [{"id": "...", "rule": "...", "source": "manual|judgement"}],
  "pages": [{"page": 486, "chapter": "ch16", "section": "16.6.1", "title": "...",
             "score": 58.7, "coverage": 1.0, "lines": ["片段行"]}]
}
```

### 打分口径（想知道“为什么排第一”时看这里）

```
score(p) = [ Σ_t w_t·idf(t)·(1+0.4·ln tf)  +  title_bonus(p) ] × (1 + 0.5·概念覆盖率)
```

- `idf = ln(N / (1+df))`，`N` = 全部 raw 页数（≈1,100）。全书高频词（piv、image、camera）自动让位给判别性强的短语。
- `w_t`：英文短语 2.0；中文展开 1.5；单词 1.0（被某个短语包含时 ×0.3）；问题末尾的“中心概念” ×1.3，前面的修饰概念 ÷1.3。
- 短语是真短语：连续英文 token 的 n-gram 只有**在原文里真的出现过**才收（`grid step size` 全书只出现 1 页，因此极具判别力）。
- `title_bonus`：命中行所在小节的**标题链**（`16.6.1 → 16.6 → 16`）按 `idf·w·factor·(标题被命中比例)` 计分；最深小节 factor 1.5、父节 0.6、更上层 0.36，无点号的章级标题再 ×0.5。同一页只取最好的一个标题，避免跨小节页叠加加分。
- 2–3 字符缩写（IA / UOD / dt）按词边界匹配，不会命中 media 之类的噪声。
- 页中小节标题位于命中行上方时，片段从标题行开始打印——标题行之前属于上一小节。

## search_tool.py — 兜底检索与结构查询

| 用法 | 作用 |
|---|---|
| `python "$S/search_tool.py" "<关键词>"` | 默认 `auto`：先索引，无命中自动降级 chapters → raw |
| `--source index\|chapters\|raw\|full\|all` | 指定来源；`--chapter N` 只在 chapters/raw/all 或 auto 下生效 |
| `--toc "<英文词>"` | 在 722 条目录骨架里找候选节 |
| `--outline N` | 打印某章“小节 → 标题 → 打印页” |
| `--page N` | 取某一打印页整页原文（最常用的核对手段） |
| `--task <id>` | 高频任务的原文定位、前提与风险 |
| `--topics` / `--gaps` / `--stats` | 术语表 / 缺口台账 / 各章行数页数 |
| `--test` | 内置自检（20 章、索引、作用域、页码、空白归一化、auto 降级、术语与缺口） |
| `--max-results N` / `--context N` / `--show-context` | 结果条数、上下文行数 |

0 命中输出 `STATUS: NOT_FOUND_IN_DOCSET` 并以退出码 3 结束——这是“语料里确实没有”，不是参数写错。`--source index --chapter N` 会直接报错（退出码 2），不再静默忽略。

## 其他脚本

- `tools/merge_terms.py --add "中文=english" [--add …] [--apply]`：术语回写，英文值必须能在 raw 里检索到（多写法用 ` / ` 分隔，逐个校验），否则拒收（退出码 4）。
- `tools/check_guidelines.py`：校验 `param-guidelines.json` 的页码存在且该页确实出现相关词，judgement 条目必须有适用/推翻条件。
- `tools/check_tasks.py`：校验 `high-frequency-tasks.json` 的 section/page 与目录、原文一致，并回写 `curated`。
- `tools/build_toc.py`：从 `full_text.txt` 印刷目录 + `raw/` 正文标题重抽 `toc_full.json`。

## 测试

```
python -m unittest discover -s tests        # 38 项（含检索质量金标准）
```

测试文件：

| 文件 | 覆盖 |
|---|---|
| `tests/test_search_tool.py` | 页码锚点、`--chapter` 作用域、空白归一化、auto 降级、0 命中退出码 |
| `tests/test_task_map.py` | 任务表的小节与页码仍存在 |
| `tests/test_ask_evidence.py` | 页锚错配、故障分型、未收录词噪声、截断提示 |
| `tests/test_retrieval_quality.py` | 13 条金标准的 top1/top3、输出长度、单次耗时、分型断言 |

`tests/golden_queries.json` 是检索质量金标准（13 条）。`tests/test_retrieval_quality.py` 会打印 **top1 / top3** 并断言 top3 = 13/13、top1 ≥ 11/13，同时检查默认输出 ≤ 4,000 字符、单次 `ask.py` ≤ 1.5 s。改动排名、术语或分型后先跑它。
