# 📚 DynamicStudio Users Guide 8.5 — Agent Skill

<p align="center">
  <img src="https://img.shields.io/badge/DynamicStudio-8.5-blue?style=for-the-badge&logo=dantec" alt="DynamicStudio 8.5">
  <img src="https://img.shields.io/badge/Pages-1128-green?style=for-the-badge" alt="1128 Pages">
  <img src="https://img.shields.io/badge/Chapters-20-orange?style=for-the-badge" alt="20 Chapters">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <strong>将 Dantec Dynamics《DynamicStudio Users Guide 8.5》转化为可被 AI Agent 直接调用的技能知识库</strong>
</p>

<p align="center">
  安装后，直接用中文提问即可获得带页码出处、可执行的操作步骤
</p>

---

## 🤔 这是什么？为什么有用？

DynamicStudio 是 Dantec Dynamics 的 **PIV/DIC/BOS/LIF/LII/PTV** 测量系统核心软件。其官方手册长达 **1128 页**，日常使用中"怎么设置某功能""某参数什么意思"极难翻查。

本技能解决两个问题：

| 问题 | 解决方案 |
|------|----------|
| 🔍 **检索难** | 手册被拆解为结构化知识库（任务索引、参数速查、章节摘要、逐章原文），Agent 可在数秒内定位到目标小节 |
| 🎯 **回答不可信** | 内置"回答协议"强制 Agent 先查原文、引用**小节编号 + 打印页码**作答，从机制上降低 AI 编造操作步骤的可能性 |

## 📖 适用场景

| 问题类型 | 示例问题 | 回答内容 |
|----------|----------|----------|
| **操作类** | "如何用 Acquisition Manager 做网格化 PIV 采集？" | UI 路径 + 编号步骤 + 关键参数（含警告提示） |
| **参数类** | "Adaptive PIV 的 Grid Step Size 是什么意思？" | 参数含义与典型值，并注明出处（ch16.6.1, p.486） |
| **综合类** | "怎么标定相机 / 如何验证矢量 / 模态分析怎么做？" | 同上，均有对应章节支撑 |

---

## 🚀 安装

### 方案一：让 Agent 自主安装（推荐）

在支持 Skill 机制的 Agent（如 opencode）对话中，直接说：

```
请把这个仓库安装为技能：
https://github.com/stultus23/dynamicstudio-guide
```

Agent 会自动将仓库内容放入你的技能目录并启用，随后即可提问。

### 方案二：手动安装

1. 下载本仓库（`git clone` 或页面 Code → Download ZIP），解压后得到目录 `dynamicstudio-guide`；
2. 将整个目录放入你的 Agent 技能目录，例如：
   - **opencode**（用户级，Windows）：`C:\Users\<用户名>\.config\opencode\skills\`
   - **opencode**（用户级，macOS/Linux）：`~/.config/opencode/skills/`
   - **项目级**（仅当前项目生效）：项目根目录下 `.opencode/skills/`
   - **其他支持 Skill 的 Agent**：放入其对应 skills 目录（如 `~/.claude/skills/`）；
3. 重启会话（新会话会重新扫描技能），然后直接提问即可验证是否生效。

---

## 💡 使用方法

安装后无需任何额外配置。以中文提问，例如：

```
"如何设置双相机 PIV 采集？"
"DynamicStudio 里 LIF 标定的步骤是什么？"
"Vector validation 的 Peak Validation 参数什么意思？"
```

回答会包含：**UI 路径** → **编号步骤** → **关键参数**（英文原名 + 含义 + 典型值）→ **注意事项** → **来源引用**（小节 + 打印页码），方便你回到原手册核对。

---

## 📁 目录结构

```
dynamicstudio-guide/
├── 📄 SKILL.md              # 技能入口：使用方法 + 回答协议 + 章节/主题索引（AI 读取此文件）
├── 📄 README.md             # 本文件（面向人类，非技能组成部分）
├── 📋 procedures.md         # 任务→步骤索引（操作类问题第一落点，含小节+打印页码）
├── 📋 dialogs.md            # 对话框与参数速查（功能/参数详情）
├── 📖 glossary.md           # 术语表
├── 📖 patterns.md           # 技术模式
├── 📖 cheatsheet.md         # 决策表
├── 🔧 troubleshooting.md    # 故障排除指南
├── 🔍 search_tool.py        # 搜索工具（支持关键词、页码、章节搜索）
├── 📂 chapters/             # 各章结构化摘要：核心概念+操作步骤+完整小节目录（含页码）+注意事项
│   ├── ch01-introduction.md
│   ├── ...
│   └── ch20-accessibility-conformance-report.md
├── 📂 raw/                  # 每章完整原文（可按 PAGE|N 或小节编号定位）
│   ├── ch01.txt
│   ├── ...
│   └── ch20.txt
└── 📄 full_text.txt         # 全文兜底（1.5 MB, 27,674 行）
```

### 章节文件结构

每个章节文件包含：
- **核心概念**：章节概述
- **操作步骤（关键操作）**：UI 路径 + 编号步骤 + 关键参数
- **章节目录（含页码）**：完整小节目录
- **注意事项/警告**：重要提示
- **关联章节**：相关章节引用

### 搜索工具

```bash
python search_tool.py <关键词>      # 搜索关键词
python search_tool.py -p <页码>      # 搜索页码
python search_tool.py -c <章节号>    # 查看章节信息
python search_tool.py --test         # 运行测试
```

---

## 📊 内容来源与质量

| 项目 | 说明 |
|------|------|
| **文本提取** | 由 pdfminer 从原 PDF 提取（LTTextLine 行向排序，保留字符级空格与行向表格） |
| **章节边界** | 按手册页脚 `PAGE|N` 标记切分，20 章全部精确命中原书目录 |
| **页码说明** | 全部页码均为**手册打印页码**（与纸质版一致） |
| **已知问题** | 仍存在少量排版残疵（行末连字符、图注混入标题、表头换行），涉及关键操作请交叉核对原文 |

---

## 🔧 维护

- **更新手册内容**：替换原 PDF → 重新提取并按 `PAGE|N` 切分 → 更新索引（`procedures.md` 等）；
- **新增分析模块**：直接更新 `procedures.md` 与对应章节文件。

---

## 📜 版权声明

本技能仅用于个人学习与参考。原文版权归 **Dantec Dynamics A/S** 所有，本仓库不含原 PDF 文件。

---

<p align="center">
  <strong>⭐ 如果这个技能对你有帮助，请给个 Star！</strong>
</p>

<p align="center">
  <a href="https://github.com/stultus23/dynamicstudio-guide">
    <img src="https://img.shields.io/github/stars/stultus23/dynamicstudio-guide?style=social" alt="GitHub Stars">
  </a>
  <a href="https://github.com/stultus23/dynamicstudio-guide/fork">
    <img src="https://img.shields.io/github/forks/stultus23/dynamicstudio-guide?style=social" alt="GitHub Forks">
  </a>
</p>
