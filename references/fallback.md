# 退让流程与术语自学习

只在 `ask.py` 给出的 `置信度：低` 或 0 命中时使用。每一步都要真的读过原文再答。

1. **术语没展开** → 自己把问题译成 2–4 个英文手册术语重跑：
   `ask.py "interrogation area grid step size"`
2. **换英文 + 限章**：`ask.py "adaptive PIV" --chapter 16`（`--chapter` 范围 1–20）。
3. **翻目录骨架路由**：`search_tool.py --toc "<英文词>"` 在 722 条标题里找候选节；`search_tool.py --outline 16` 看整章结构。选中节后必须 `search_tool.py --page N` 取原文核实——**标题相符不等于内容相符**。
4. **直接原文检索**：`search_tool.py <英文词> --source raw --chapter N --max-results 20`。
5. **全部落空** → 工具会输出 `STATUS: NOT_FOUND_IN_DOCSET` 并以退出码 3 结束：这是“26,165 行里确实没有”。先 `search_tool.py --gaps` 看是否已登记，再明确告诉用户手册未覆盖，并说明查了哪些词、哪些标题节。若问的是“某能力是否存在”（B 型），0 命中本身就是“不在手册范围”的证据，据此作答，不要继续搜。

## 术语自学习（自译命中后回写）

退让流程里自译的英文术语**成功命中原文**后，把映射写回术语表，下次同类问题直接命中：

```
python "$S/tools/merge_terms.py" --add "体视标定=stereo calibration"           # 演练
python "$S/tools/merge_terms.py" --add "体视标定=stereo calibration" --apply   # 写回
python "$S/tools/merge_terms.py" --from references/_terms-pending.json --apply # 批量
```

英文值必须能在 raw 里检索到，否则拒收（退出码 4）；多个同义写法用 ` / ` 分隔，逐个校验。原文 0 命中的术语**不要硬加进术语表**，登记到 `references/corpus-gaps.json`（写清证据、版本、处置口径）。

`ask.py` 输出里的 `⚠ 未收录的中文词` 就是要用本节消除的对象；单字残留会写成 `自+标定` 的形式，说明只剩一个汉字没被术语覆盖。

## 维护

- 换语料/换版本：重跑 `tools/build_toc.py` → `tools/check_tasks.py` → `python -m unittest discover -s tests`。
- 改了排名或术语：必须先跑 `tests/test_retrieval_quality.py` 看 top1 / top3 是否退化。
- 禁止为了让某条金标准过关而在代码里写死页码或问题字符串——那是过拟合，抽查未公开问题时会立刻暴露。
