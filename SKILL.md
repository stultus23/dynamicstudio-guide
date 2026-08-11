---
name: dynamicstudio-guide
description: "DynamicStudio Users Guide 8.5（Dantec Dynamics 官方用户手册）知识库。涵盖 PIV/DIC/BOS/LIF/LII/PTV 等测量技术、数据采集（Acquisition）、设备配置（相机/激光/同步器/遍历）、标定（Camera/Multi-Camera/DIC/LIF 标定）、图像处理、矢量验证与后处理、模态分析、Python/MATLAB 链接、数据导出与显示。当用户询问如何在 DynamicStudio 中完成某项操作（如何设置 PIV 采集、如何标定相机、如何验证矢量、某对话框/参数含义、某分析模块用法）时使用本技能。"
---

# DynamicStudio Users Guide 8.5（官方手册知识库）

**来源**: Dantec Dynamics《DynamicStudio Users Guide 8.5》(1128 页) | **语言**: 中文回答，UI/参数保留英文原名

## 使用方法

- **操作类问题**（"如何/怎么实现 XX"）→ 先查 `procedures.md`（任务索引，含小节编号+页码），再按页码去 `raw/chXX.txt` 读取完整步骤
- **功能/参数详情**（"XX 是什么/参数怎么调"）→ 查 `dialogs.md`（参数速查表），需要细节时读对应 raw 章节
- **章节概览** → 读 `chapters/chXX.md`（每章含完整小节目录+页码+注意事项）
- **没有命中** → 在 `raw/chXX.txt`（每章完整原文）中用 grep 搜索关键词，最后兜底搜索 `full_text.txt`（全文，含 PAGE|N 页码标记）

## 回答协议（How-to 问答强制要求）

回答操作类问题时，输出必须包含：

1. **UI 路径**：在哪个 Ribbon/菜单/面板/对话框中操作（如 "System Control" 面板、"Device properties" 面板）
2. **编号步骤**：按顺序给出可执行步骤
3. **关键参数**：涉及参数名（英文原名）+ 含义 + 典型值/建议
4. **注意事项**：从原文 Note/Warning 提取的坑与警告
5. **来源引用**：小节编号 + 打印页码（如 `ch16.6 Adaptive PIV, p.485`），便于用户查原手册

搜索降级链：`procedures.md / dialogs.md` → `chapters/chXX.md` → `raw/chXX.txt`（章节完整原文）→ `full_text.txt`（全文 grep）。回答前至少确认一次原文，不要凭手册之外的知识作答；原文缺失时才补充常识并注明。

## 问答示例

**问**：如何用 Acquisition Manager 做网格化 PIV 采集？
**答**：进入采集模式确保设备就绪（ch13.1.1, p.130）→ 打开 Acquisition Manager → Grid Generator 选 1D/2D/3D 生成遍历行（p.133）→ 逐行设置 Time between pulses/Trigger rate/Number of images（p.131）→ 可选挂载分析序列 → Run All。注意：进入 Acquisition Manager 会禁用激光警告（p.130）……

**问**：Adaptive PIV 的 Grid Step Size 是什么意思？
**答**：相邻 interrogation area 中心间距（像素），直接决定矢量密度……（详见 `dialogs.md` §5，原文 ch16.6.1, p.486）

## 章节索引

| # | 章节 | 主题 |
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
| [ch16](chapters/ch16-python-link.md) | Python Link + 114 个分析模块 | Adaptive PIV、DIC、BOS、LIF/LII、PTV、标定、模态分析等（p.471） |
| [ch17](chapters/ch17-data-exchange.md) | Data Exchange | 导入导出（p.1002） |
| [ch18](chapters/ch18-displays.md) | Displays | 显示交互（p.1013） |
| [ch19](chapters/ch19-dialogs.md) | Dialogs | Numeric Display 与状态码（p.1088） |
| [ch20](chapters/ch20-accessibility-conformance-report.md) | Accessibility | 无障碍一致性 |

## 主题索引（主题 → 章节）

- **PIV（速度场测量）** → ch13 采集, ch16.6 Adaptive PIV, ch16.93 Stereo-PIV, ch16.2-4 PTV
- **DIC（应变/位移）** → ch16.24（p.577）
- **BOS（密度梯度）** → ch16.14（p.526）
- **标定 Calibration** → ch16.15 Camera、ch16.63 Multi-Camera、ch16.16 精化、ch16.108 体积精化、ch16.46/48 LIF/LII
- **图像处理** → ch16.31-41, ch16.22 掩模, ch16.5 拼接, ch16.39 IPL
- **矢量验证** → ch16.64 N-Sigma、16.67 Peak、16.62 Moving Average、16.75 Range、16.99 UOD
- **模态分析** → ch16.59-61（POD/sPOD/mPOD/FMD）
- **激光安全** → ch05
- **同步器/触发** → ch14.6（p.315）
- **相机选型** → ch14.5（p.210）
- **Python/MATLAB/Octave** → ch16.74/16.54/16.65
- **数据交换** → ch17
- **显示/数值表** → ch18, ch19

## 支持文件

- [procedures.md](procedures.md) — 任务→步骤索引（操作类问题第一落点）
- [dialogs.md](dialogs.md) — 对话框与参数速查
- [glossary.md](glossary.md) — 术语表
- [patterns.md](patterns.md) — 技术模式
- [cheatsheet.md](cheatsheet.md) — 决策表
- [troubleshooting.md](troubleshooting.md) — 故障排查指南（常见问题→原因→处置）
- [search_tool.py](search_tool.py) — 搜索工具（支持关键词、页码、章节搜索）
- `raw/ch01.txt … ch20.txt` — 每章完整原文（按 PAGE|N 页码定位）
- `full_text.txt` — 全文兜底（1.5 MB）

## 范围与限制

- 内容仅来自手册 8.5 版本；**页码均为手册打印页码**（与纸质版一致，可用于 cross-reference）
- 章节文件（chapters/chXX.md）与索引文件的页码 = 原文 `raw/chXX.txt` 中 `PAGE|N` 标记（手册页脚打印页码），在 raw 中定位时搜索 `PAGE|目标页` 或直接 grep 小节编号（如 `16.6 Adaptive PIV`）
- 提取文本可能有少量排版残疵（行末连字符、图注混入正文、表头换行），关键操作步骤请交叉核对原文
- 不替代软件实际操作与 Dantec 官方支持
