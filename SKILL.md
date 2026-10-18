---
name: dynamicstudio-guide
version: 8.5-kb-2026.10.18
description: "DynamicStudio Users Guide 8.5（Dantec Dynamics 官方用户手册）知识库（20 章 / 26,165 行 / 722 条目录骨架）。涵盖 PIV/DIC/BOS/LIF/LII/PTV 等测量技术、数据采集（Acquisition）、设备配置（相机/激光/同步器/遍历）、标定（Camera/Multi-Camera/DIC/LIF/LII 标定）、图像处理、矢量验证与后处理、模态分析、Python/MATLAB/Octave 链接、数据导出与显示。当用户询问如何在 DynamicStudio 中完成某项操作（如何设置 PIV 采集、如何标定相机、如何验证矢量、某对话框/参数含义、某分析模块用法、报错为什么出现）时使用此技能。"
---

# DynamicStudio Users Guide 8.5（官方手册知识库）

**来源**: Dantec Dynamics《DynamicStudio Users Guide 8.5》（Build no. 8.5.0058，Publication no. 9040U1874） |
**规模**: 20 章 / 26,165 行 / 722 条目录骨架 | **语言**: 中文回答，UI 名称、参数、模块名保留英文原名

## 第零步：先分型，再决定检索多少（优先于一切）

DynamicStudio 的问题分三种，检索要求完全不同。**分型判断错误是回答失败的主因**：把一个"手册里根本没有答案"的问题当成查证题，就会在语料里无限换词打转——因为查证型有天然停止条件（找到那一页就停），推理型没有。

| 类型 | 判别信号（看用户怎么问） | 检索要求 | 典型问法 |
|---|---|---|---|
| **A 查证型** | 问"是什么 / 在哪 / 怎么设 / 默认值 / 某对话框字段含义 / 某模块用法" | **强制取回原文，逐字核对，不得跳过** | "Adaptive PIV 的 Grid Step Size 是什么"、"怎么开 Acquisition Manager" |
| **B 推理型** | 问"可行吗 / 为什么 / 能不能这样 / 哪个做法对 / 为什么出不来结果" | **不要求原文给出结论**；只查前提与反证，按预算封顶 | "双相机不同触发率能同步吗"、"标定精化什么时候必须做" |
| **C 混合型**（最常见） | 既问为什么又问怎么设 | 先按 B 出骨架，再把骨架里每个事实点按 A 单点核 | "为什么标定误差大？标定参数怎么改" |
| **D 故障排查型** | 贴报错原文、问"失败 / 异常 / 打不开 / 不准 / 不够"，**无论有没有"为什么"字样** | 手册通常不解释该报错：先按 B 推理（查前提与反证），再把其中可核实的事实点按 A 单点核 | "DatasetException … failed to deserialize 为什么"、"PIV 采集失败"、"标定精度不够怎么办" |

**唯一判据**：这个问题的答案，手册里会不会有一句话直接写着？

- 会 → **A**，去把那句话找出来，逐字引。
- 不会（答案要靠多条事实推出来） → **B**，推理是你的职责，检索只用来锁前提。
- 报错/失败/异常类 → **D**，先去缺口台账和反证检索**证明手册确实没写**，再给推理结论。**不要为了凑 A 型去语料里找一句不存在的结论。**

### B 推理型的执行流程（与 A 不同，必须按序）

1. **不搜结论，先拆前提。** 把"这个结论成立与否，取决于哪 3–5 条可查事实"先列出来，写成清单（如介质/折射率、相机数、触发率、授权模块）。
2. **逐条只查前提**，每条 1–2 次检索。
3. **至少做一次反证查询（强制）**：主动搜"这个功能/做法不存在、被禁止、有前提限制"的表述。判断越自信越要先查反证——只搜支持性证据，等于把偏见包装成结论。
4. **0 命中也是证据。** 若某个前提在 722 条目录骨架和全文中都搜不到，结论就是"该能力不在本手册（8.5）范围"，这比"没找到所以不确定"有用得多，必须写进答案。**先查 `search_tool.py --gaps`**——已知缺口已登记在案，别重复搜。
5. **总预算 6 次检索封顶。** 超预算立刻出答案，未核实项按下方三档标注如实交代。**没有预算就没有停止条件。**

### 作答前的证据等级（三档标注，不得混用）

| 标注 | 含义 | 使用条件 |
|---|---|---|
| `[手册 p.N]` | 手册原文，可逐字回查 | 已用 `--source raw` 或整页读取核实过 |
| `[推理]` | 由原文明示的公式/定义/机制推出 | **必须附依据**，如"由手册 p.146 ISA 说明推出" |
| `[未覆盖·判断]` | 手册无此内容，属工程经验或跨版本推断 | 必须写清"什么条件会推翻它"，且**不得伪装成有出处** |

第三档禁止写成"我的知识库认为 / 我的训练数据说"。对 DynamicStudio 的事实（菜单路径、参数默认值、模块命名），先验知识存在**跨版本**过时风险（本语料是 8.5.0058），**说成"知识库说"会让用户误以为有出处**。只能写"本手册未覆盖，以下为判断"。

## 第一步：取回原文（A 查证型与 C 型的事实点，强制）

DynamicStudio 的界面、参数默认值、模块命名在训练数据里零散且容易张冠李戴（尤其"分析模块"在不同大版本间有增删）。所以凡属 A 型，或 C 型/B 型里的**事实点**，必须先运行检索入口取回官方手册原文：

```powershell
# --- 解释器与目录解析（全部走环境变量 + 自动探测，不写死本机路径） ---
# Python：本技能脚本为纯标准库零依赖，任何 Python 3.8+ 均可运行。
# 优先级：① 环境变量 DYNAMICSTUDIO_SKILL_PYTHON  ② PATH 上的 python/python3  ③ py 启动器
$py = $null
foreach ($c in @($env:DYNAMICSTUDIO_SKILL_PYTHON, "python", "python3", "py")) {
    if (-not $c) { continue }
    $cmd = if ($c -match '[\\/]') { $c } else { (Get-Command $c -ErrorAction SilentlyContinue).Source }
    if ($cmd -and (Test-Path $cmd)) { $py = $cmd; break }
}
if (-not $py) { throw "未找到可用 Python：请设置 DYNAMICSTUDIO_SKILL_PYTHON 或将 python 加入 PATH" }
$env:PYTHONIOENCODING = "utf-8"   # 防 PowerShell 管道把 UTF-8 输出按 GBK 解码出乱码

# 技能目录：优先环境变量 DYNAMICSTUDIO_SKILL_DIR（可用它强制指定某个副本）；
# 未设置时，从各 Agent 约定的 skills 根目录自动探测含 tools/ask.py 的 dynamicstudio-guide 副本。
$S = $env:DYNAMICSTUDIO_SKILL_DIR
if (-not ($S -and (Test-Path (Join-Path $S "tools\ask.py")))) {
    $S = @(
        "$HOME\.config\opencode\skills\dynamicstudio-guide",   # opencode（用户级）
        "$HOME\.dsh\skills\dynamicstudio-guide",               # DSH（用户级）
        "$HOME\.claude\skills\dynamicstudio-guide",            # Claude Code（用户级）
        ".opencode\skills\dynamicstudio-guide",                # opencode（项目级）
        ".claude\skills\dynamicstudio-guide"                   # Claude Code（项目级）
    ) | Where-Object { Test-Path (Join-Path $_ "tools\ask.py") } | Select-Object -First 1
}
if (-not $S) { throw "未找到技能目录：请设置 DYNAMICSTUDIO_SKILL_DIR 指向含 tools/ask.py 的 dynamicstudio-guide 目录" }

& $py (Join-Path $S "tools\ask.py") "<用户的原问题，中文原样照抄>" --top-pages 6
```

> **更省事的方式**：`ask.py` 会按自身位置（`Path(__file__).parents[1]`）自动定位技能根目录，
> 所以只要能定位到脚本本身，就不用管技能装在哪、也不必设环境变量。bash / zsh / 其它 shell：
>
> ```bash
> python "<技能根目录>/tools/ask.py" "<用户的原问题，中文原样照抄>" --top-pages 6
> # <技能根目录> 换成你实际的 dynamicstudio-guide 路径即可
> ```

它会自动完成四件事并把**原始页面全文**交给你：

1. **判定意图**——含"报错/失败/异常/打不开/不准"等故障信号归为**故障排查型（D）**，优先于 A/B/C；含"为什么/原理/依据/可行"归为推理型（B）；含"怎么/如何/设置/步骤/含义/默认"归为查证型（A）；两者都有按 C 处理。输出首行给出分型与策略建议。
2. **中文术语展开成英文手册术语**（`references/zh-en-terms.json`，96 条；补词条用 `tools/merge_terms.py`，英文值会自动对照原文验证）——手册里没有"查询窗口"这四个字，只有 `Interrogation Area`。**术语表没覆盖的中文词会列在输出「⚠ 未收录的中文词」段**：看到它就说明有主题词丢了，当前结果可能主题漂移——按下方退让流程自译英文重试，不要直接采用结果。提问用语（怎么、如何、怎么办、报错……）已被停用词表过滤，**不会**触发该告警；若仍出现"⚠ 未收录"，那基本就是真丢了主题词。
3. **给出候选页**：先用目录骨架定位小节，**再按小节跨度回 raw 原文逐页校验术语确实出现在该页**，只有校验通过才标"已校验"。这不是多余步骤——目录只记**小节起始页**，而小节正文常跨页（例：16.6 Adaptive PIV 起始于 p.485 页末，其配置说明在 p.486），只按起始页取整页会读到**上一小节的内容**。看到"待核对"标记就说明该页未经原文确认，引用前必须自己读原文。
4. **打印候选页原文**，标注打印页号；每页默认打印 120 行（`--page-lines` 可调），**若被截断会显式提示行数与取全页命令**，不要把"打印不全"误读成"手册没写"。

**拿到之后：**

- **事实只认原文**：菜单路径、对话框字段、参数默认值、模块步骤，只依据返回的原文写，逐字一致。
- 每条**事实**结论后用 `[手册 p.打印页]` 标注（DS 全书连续编页，不需要文档前缀），例如 `[手册 p.485]`、`[手册 p.130]`。
- 原文没写到的，说「本手册未覆盖」，**然后按三档规则决定**：属于可推理的写 `[推理]` 并给依据；属于工程经验或跨版本推断的写 `[未覆盖·判断]` 并给推翻条件。**不要补全事实，但不要因此放弃回答。**
- 需要整页上下文或相邻页：`python search_tool.py --page <打印页>`

**绝对禁止**：凭记忆写菜单路径、参数默认值、模块步骤。**注意区分**——禁止的是**编造事实**，不是禁止**做推理**。这两件事必须分开执行。

### 如果 `ask.py` 没命中

按顺序退让，每一步都要真的读过原文再答：

1. 报「无法提取检索词」→ **你自己把问题译成 2–4 个英文手册术语重跑**：`ask.py "interrogation area grid step size"`。
2. 换成英文术语重试，或限定章节：`ask.py "adaptive PIV" --chapter 16`（`--chapter` 只在原文/章节检索下有效，范围 1–20）。
3. 仍不中 → **翻目录骨架路由**：`search_tool.py --toc "<英文关键词>"` 在 722 条标题里找候选节；或 `search_tool.py --outline 16` 看某章整体结构。选中节后必须 `search_tool.py --page <打印页>` 取原文核实，**标题相符不等于内容相符**。
4. 直接原文检索：`search_tool.py <英文关键词> --source raw --chapter <N> --max-results 20`。
5. 全部落空 → **先看返回值**：工具会输出 `STATUS: NOT_FOUND_IN_DOCSET` 并以退出码 3 结束——这表示"在 26,165 行里确实没有"，不是"参数写错了"。明确告诉用户手册没有覆盖，并说明你查了哪些词、哪些标题节。**若检索的是"某能力是否存在"（B 型），落空本身就是"该能力不在手册范围"的证据，应据此作答，而不是继续搜。**

### 术语自学习（自译命中后回写，避免下次再降级）

你在退让流程里自译的英文术语**成功命中原文**后，把这对映射回写术语表，下次同类问题直接命中、不再走兜底：

```powershell
# 1) 直接给一对映射；英文值会自动对照 raw 原文验证，原文中不存在的会被拒收（退出码 4）
python "$S\tools\merge_terms.py" --add "体视标定=stereo calibration"

# 2) 确认"收录 N 条"无误后写回
python "$S\tools\merge_terms.py" --add "体视标定=stereo calibration" --apply

# 或从 JSON 文件批量并入：python "$S\tools\merge_terms.py" --from references\_terms-pending.json --apply
```

问题输出中的「⚠ 未收录的中文词」就是要用本节消除的对象。

## 检索工具

- **问题入口（首选）**：`tools/ask.py "<中文问题>"` —— 见上一节
- **默认源是 `auto`**：`python search_tool.py <关键词>` 先查索引，**索引无命中时自动降级到 chapters/raw 并提示**——所以直接 `python search_tool.py <英文词>` 也能召回只在原文出现的词（如 `Burst`），不必手动加 `--source raw`。
- 结构化索引：`--source index`（任务表 + 4 份速查摘要 + 目录骨架）；章节摘要：`--source chapters`
- **目录骨架路由**：`python search_tool.py --toc "<英文关键词>"`（722 条标题）；`python search_tool.py --outline <章节号>`（某章标题→打印页清单）
- **原文验证**：`python search_tool.py <关键词> --source raw --chapter <N>`
- 定位到打印页：`python search_tool.py --page <打印页>`
- 任务证据路由：`python search_tool.py --task <id>`
- **语料缺口台账**：`python search_tool.py --gaps`（已确认的手册未覆盖项，见下）
- 术语表：`python search_tool.py --topics`；章节统计：`--stats`
- **自检**：`python search_tool.py --test`（20 章、任务/目录索引、`--chapter` 作用域、页码、空白归一化、auto 降级、术语表与缺口台账）

**注意两处易错点（已修）**：

- `--chapter` 只在 `--source chapters/raw/all`（或 `auto` 且给了 `--chapter`）下生效。`--source index --chapter 16` 会**直接报错**（退出码 2），不再静默忽略。
- 匹配前对关键词与整行做**空白归一化**（合并多空格 / NBSP），PDF 抽取造成的 `Grid  Step  Size`（双空格）也能命中 `Grid Step Size`，二者召回一致。

## 回答格式

对"原理 + 操作"这类问题（C 型），按这个结构回答：

```markdown
**一句话结论**（含 [手册 p.N]）

## 原理
<为什么这样 / 什么条件下成立 / 前提与限制>  每条带 [手册 p.N]

## 操作步骤
1. <菜单路径，与原文逐字一致>   [手册 p.N]
2. ...
涉及的关键参数：<参数名> = <取值/默认值>   [手册 p.N]

## 需要注意
<易错点、副作用、安全提示（激光/同步器）>   [手册 p.N]

## 需要你确认的上下文
<会改变答案的条件，如介质/折射率、相机数、触发率、授权模块、DynamicStudio 版本>
```

**B 型（推理/可行性）用这个结构**，先给结论，再交代推理链与证据状态：

```markdown
**一句话结论**（是 / 否 / 分情况，每种给判定依据）

## 为什么
<前提 → 推到结论的链条；每条前提标 [手册 p.N] 或 [推理] 或 [未覆盖·判断]>

## 手册里查到了什么 / 没查到什么
<逐条列出检索过的关键词与命中情况；0 命中要明说，它是证据>

## 如果是这样，那实际可行的是哪几种做法
<把"看似同一个做法"拆成几种真实存在的做法，逐一标注可行性>
```

**D 型（故障排查）用这个结构**，核心是**先证明手册没写**，再给推理：

```markdown
**一句话结论**（这不是操作错误 / 是 X 类故障；能确定的与不能确定的分开写）

## 为什么
<按“错误串结构 → 手册机制 → 可能成因”推链条；每条标 [手册 p.N] / [推理] / [未覆盖·判断]>

## 手册里查到了什么 / 没查到什么
<明确写出：报错原文关键词（如 deserialize）检索 0 命中 = 手册不解释该异常；
 相邻主题（如数据库格式变更、转换器失败条件）命中了什么，逐条给页码>

## 如果是这样，那实际可行的是哪几种做法
<按“最可能 → 备选”排序，每条注明是手册依据还是工程建议>

## 需要你确认的上下文
<版本/构建号、发生时机、文件位置、是否断电或网盘同步、报错前是否移动过数据>
```

规则：**用户问"怎么做"必须同时给出原理**（否则他下次遇到变体还是不会）；反之亦然。**D 型必须给"确认上下文"清单**——故障排查的结论高度依赖现场条件，缺了它，推理就无从收敛。

## 页码规则（易错，务必遵守）

- 页码为手册**打印页**（与纸质版一致，可用于 cross-reference），全书**连续编页**：正文从 p.17 开始，往后到 p.1114；引用写成 `[手册 p.N]` 即可，无需文档前缀。
- 章节起页（供快速定位，均为打印页）：ch05 p.25、ch06 p.27、ch07 p.29、ch12 p.51、ch13 p.130、ch14 p.186、ch15 p.461、ch16 p.471、ch17 p.1002、ch18 p.1013、ch19 p.1088。
- **页码锚点零漂移**：原文每页以显式 `PAGE|N` 标记（共 1,080 个），工具按此锚定打印页，不靠页脚猜测。需要整页原文时用 `search_tool.py --page N`。
- 若某内容找不到对应 `PAGE|N` 标记（极少数），引用时补 `raw/chNN.txt` 行号，不得推测页码。

## 回答约束

先确认会改变答案的上下文：DynamicStudio 版本/构建号、测量方法（PIV/DIC/BOS/LIF/LII/PTV/Shadow）、相机数、介质与折射率、同步器/触发率、授权模块、目标结果与当前数据条件。

- **手册事实**：菜单路径、对话框字段、支持格式、默认值和安全提示，须经原文验证并标注 `手册 p.N`。
- **工程建议**：如 IA 尺寸选择、粒子密度、标定靶摆放，必须说明适用条件；不能写成官方默认值。
- **版本敏感**：本语料是 8.5.0058；模块与参数在不同版本间有增删（见缺口台账），跨版本结论必须标明 `[未覆盖·判断]`。
- **安全优先**：对激光、同步器接线或可能影响设备安全的操作，先呈现原文中的 Note/Warning 和必要前提；本 skill 不替代现场安全规程、硬件手册或 Dantec 技术支持。
- **证据不足或版本不明**：指出缺失条件，不虚构菜单路径、参数、模块步骤；但**仍须给出可推理的结论**并标明档位。

## 问答示例

**问（A 型）**：Adaptive PIV 的 Grid Step Size 是什么意思？
**答**：它是相邻 interrogation area (IA) 中心的间距（像素），直接决定矢量密度……`[手册 p.486]`。配置时 IA 尺寸、Grid Step Size 与速度梯度共同决定能否适应该流场 `[手册 p.485]`。

**问（A 型）**：怎么用 Acquisition Manager 做网格化采集？
**答**：进入 Acquisition Mode 并确保所有设备 Ready `[手册 p.130]` → 打开 Acquisition Manager → Grid Generator 选 1D/2D/3D 生成遍历行 `[手册 p.133]` → 逐行设置 Time between pulses / Trigger rate / Number of images → Run All。注意：进入 Acquisition Manager 会禁用激光警告对话框，采集前必须自行确认激光安全 `[手册 p.130]`。

**问（B 型，回归用例，别删）**：双相机触发率不同，还能同步测量吗？
**答**：**可以。** 手册专设一节 14.6.4 "Running two cameras synchronized but at different trigger rate" `[手册 p.351]`。反证查询：检索 "different trigger rate" 命中该节，并非手册未覆盖。要点是先确认每台相机的最大帧率、Reference time 设置与各自 Image Buffer 数量（详见原文）`[手册 p.351]`。

## 章节索引

| # | 章节 | 主题（起页） |
|---|------|------|
| [ch01](chapters/ch01-introduction.md) | Introduction | 软件概述、能力 |
| [ch02](chapters/ch02-related-documentation.md) | Related Documentation | 相关文档 |
| [ch03](chapters/ch03-contacting-dantec-dynamics.md) | Contacting Dantec Dynamics | 联系支持 |
| [ch04](chapters/ch04-software-license-agreement.md) | Software License Agreement | 许可协议 |
| [ch05](chapters/ch05-laser-safety.md) | Laser Safety | 激光安全（p.25） |
| [ch06](chapters/ch06-requirements.md) | Requirements | 系统要求（p.27） |
| [ch07](chapters/ch07-note-to-administrators.md) | Note to Administrators | 安装/防火墙/内存（p.29） |
| [ch08](chapters/ch08-software-update-agreement.md) | Software Update Agreement | 更新协议 |
| [ch09](chapters/ch09-acknowledgement-of-third-party-software-components.md) | Third Party Software | 第三方组件 |
| [ch10](chapters/ch10-add-ons-and-options-for-dynamicstudio.md) | Add-Ons and Options | 附加项 |
| [ch11](chapters/ch11-legacy-options.md) | Legacy Options | 旧版选项 |
| [ch12](chapters/ch12-getting-started.md) | Getting Started | 快速入门/UI/数据库（p.51） |
| [ch13](chapters/ch13-acquisition.md) | Acquisition | 采集/ISA/远程采集/模拟器（p.130） |
| [ch14](chapters/ch14-devices.md) | Devices | 相机/同步器/激光/遍历/靶标（p.186） |
| [ch15](chapters/ch15-analysis.md) | Analysis | 分析序列/分布式分析（p.461） |
| [ch16](chapters/ch16-python-link.md) | Python Link + 分析模块 | Adaptive PIV、DIC、BOS、LIF/LII、PTV、标定、模态分析等（p.471） |
| [ch17](chapters/ch17-data-exchange.md) | Data Exchange | 导入导出（p.1002） |
| [ch18](chapters/ch18-displays.md) | Displays | 显示交互（p.1013） |
| [ch19](chapters/ch19-dialogs.md) | Dialogs | Numeric Display 与状态码（p.1088） |
| [ch20](chapters/ch20-accessibility-conformance-report.md) | Accessibility | 无障碍一致性 |

## 主题索引（主题 → 章节 / 打印页）

- **PIV（速度场测量）** → ch13 采集, ch16.6 Adaptive PIV（p.485）, ch16.93 Stereo-PIV（p.905）, ch16.2-4 PTV（p.474-478）
- **DIC（应变/位移）** → ch16.24（p.577）
- **BOS（密度梯度）** → ch16.14（p.526）
- **标定 Calibration** → ch16.15 Camera（p.541）、ch16.63 Multi-Camera（p.765）、ch16.16 精化（p.551）、ch16.108 体积精化（p.965）、ch16.46/48 LIF/LII（p.678/688）
- **图像处理** → ch16.31-41、ch16.22 掩模（p.571）、ch16.5 拼接（p.482）、ch16.39 IPL（p.635）
- **矢量验证** → ch16.64 N-Sigma（p.774）、16.67 Peak（p.792）、16.62 Moving Average（p.763）、16.75 Range（p.825）、16.99 UOD（p.936）
- **模态分析** → ch16.59-61（POD/sPOD/mPOD/FMD，p.722 起）
- **激光安全** → ch05（p.25）
- **同步器/触发** → ch14.6（p.315）
- **相机选型** → ch14.5（p.210）
- **Python/MATLAB/Octave 链接** → ch16.74/16.54/16.65（p.824/696/777）
- **数据交换** → ch17（p.1002）；**显示/数值表** → ch18（p.1013）、ch19（p.1088）

## 语料缺口台账（已识别、已回写）

下列条目固化在 `references/corpus-gaps.json`，`search_tool.py --gaps` 可查；回答涉及这些点时**直接引用台账口径**，不要重新检索、不要凭记忆补内容：

| 项 | 类型 | 状态 | 处置口径 |
|---|---|---|---|
| `13.2.1 Registering 3rd party devices` | 手册目录编排 | **印刷目录漏列（正文有）** | 正文 p.141 存在；`toc_full.json` 已补录（721+1=722 条）；引用以 p.141 为准 |
| 非 8.5 版本的界面/参数差异 | 版本范围 | **本语料只覆盖 8.5.0058** | 用户版本 ≠ 8.5 时标 `[未覆盖·判断]`，以本机 Help / Release Notes 为准 |
| 相机/激光/同步器硬件规格 | 硬件范围 | **不在本手册内** | 硬件规格/接线/安全距离以硬件手册为准；软件侧用 ch14.5/14.6 回答 |

**新增缺口必须写明证据与版本**，并给出处置口径，再并入 `corpus-gaps.json`。

## 支持文件

- **`tools/ask.py`** — 问题入口（中文问题 → 分型 + 术语展开 + 候选页 + 原页证据包）；A 型与 C 型事实点**必跑**，B 型仅用于查前提
- **`tools/merge_terms.py`** — 术语回写（英文值自动对照原文校验，查无则拒收）；**`tools/check_tasks.py`** — 校验任务表 section/page 与原文、目录一致性并回写 `curated`
- **`tools/build_toc.py`** — 从 `full_text.txt` 印刷目录 + `raw/` 正文标题重抽目录骨架 → `references/toc_full.json`
- [procedures.md](procedures.md) — 任务→步骤索引（操作类问题第一落点）
- [dialogs.md](dialogs.md) — 对话框与参数速查；**其中"建议"是按原文和上下文推断的，不能当作默认值**
- [glossary.md](glossary.md) — 术语表；[patterns.md](patterns.md) — 技术模式；[cheatsheet.md](cheatsheet.md) — 决策表
- [troubleshooting.md](troubleshooting.md) — 故障排查（现象 → 原因 → 核实步骤）
- [references/zh-en-terms.json](references/zh-en-terms.json) — 中文→英文手册术语（96 条；`ask.py` 依赖，命中率低时优先补这里）
- [references/high-frequency-tasks.json](references/high-frequency-tasks.json) — 20 条高频任务；`curated: true` 表示已回原文与目录校验 section/page，另带 `context_to_collect`/`risk`
- [references/toc_full.json](references/toc_full.json) — 722 条目录骨架（小节 → 标题 → 打印页）
- [references/corpus-gaps.json](references/corpus-gaps.json) — 语料缺口台账（见上）
- `chapters/chNN-*.md` — 各章结构化摘要（**用于路由，不作证据**）
- `raw/ch01.txt … ch20.txt` — 每章完整原文（含 `PAGE|N` 页码标记），**唯一证据源**
- `full_text.txt` — 全文（含扉页与官方印刷目录），兜底检索用
- `tests/test_search_tool.py`、`tests/test_task_map.py` — 页码锚点、任务对齐、空白归一化、auto 降级、0 命中退出码回归测试

## 范围与限制

- 内容来自 DynamicStudio **8.5.0058** 官方 Users Guide；其它版本（尤其分析模块命名）行为可能不同
- 目录骨架来自官方印刷目录 + 正文标题补录；正文 3 位数小节（如 `16.100–16.111`）已纳入，`13.2.1` 为补录项（见缺口台账）
- 界面截图、图表无法文本化；需要看图时按打印页回原 PDF 查阅
- 页码为原文 `PAGE|N` 标记锚定的**打印页**，全书连续编页，引用写 `[手册 p.N]`
- `procedures.md` / `dialogs.md` / `patterns.md` / `cheatsheet.md` / `troubleshooting.md` 与 `chapters/*.md` 是**人工整理的导航摘要**，用于路由与提速；**具体值一律回 `raw/` 原文核实**
- **本知识库只有手册，不含工程经验**：B 型问题的判断部分必然超出语料，这是设计边界而非缺陷；按三档标注如实交代即可，不要因此拒答
- 不替代软件实际操作、硬件手册与 Dantec 官方支持
