# 章节目录、主题索引与语料缺口

## 章节索引（起页为打印页）

| # | 章节 | 主题（起页） |
|---|------|------|
| [ch01](../chapters/ch01-introduction.md) | Introduction | 软件概述、能力（p.17） |
| [ch02](../chapters/ch02-related-documentation.md) | Related Documentation | 相关文档（p.18） |
| [ch03](../chapters/ch03-contacting-dantec-dynamics.md) | Contacting Dantec Dynamics | 联系支持（p.19） |
| [ch04](../chapters/ch04-software-license-agreement.md) | Software License Agreement | 许可协议（p.21） |
| [ch05](../chapters/ch05-laser-safety.md) | Laser Safety | 激光安全（p.25） |
| [ch06](../chapters/ch06-requirements.md) | Requirements | 系统要求（p.27） |
| [ch07](../chapters/ch07-note-to-administrators.md) | Note to Administrators | 安装/防火墙/内存（p.29） |
| [ch08](../chapters/ch08-software-update-agreement.md) | Software Update Agreement | 更新协议（p.31） |
| [ch09](../chapters/ch09-acknowledgement-of-third-party-software-components.md) | Third Party Software | 第三方组件（p.33） |
| [ch10](../chapters/ch10-add-ons-and-options-for-dynamicstudio.md) | Add-Ons and Options | 附加项（p.47） |
| [ch11](../chapters/ch11-legacy-options.md) | Legacy Options | 旧版选项（p.49） |
| [ch12](../chapters/ch12-getting-started.md) | Getting Started | 快速入门/UI/数据库（p.51） |
| [ch13](../chapters/ch13-acquisition.md) | Acquisition | 采集/ISA/远程采集/模拟器（p.130） |
| [ch14](../chapters/ch14-devices.md) | Devices | 相机/同步器/激光/遍历/靶标（p.186） |
| [ch15](../chapters/ch15-analysis.md) | Analysis | 分析序列/分布式分析（p.461） |
| [ch16](../chapters/ch16-python-link.md) | Python Link + 分析模块 | Adaptive PIV、DIC、BOS、LIF/LII、PTV、标定、模态分析等（p.471） |
| [ch17](../chapters/ch17-data-exchange.md) | Data Exchange | 导入导出（p.1002） |
| [ch18](../chapters/ch18-displays.md) | Displays | 显示交互（p.1013） |
| [ch19](../chapters/ch19-dialogs.md) | Dialogs | Numeric Display 与状态码（p.1088） |
| [ch20](../chapters/ch20-accessibility-conformance-report.md) | Accessibility | 无障碍一致性报告（p.1091） |

正文到 p.1114 结束；原文每页以 `PAGE|N` 标记（1,080 个）。章节目录可用 `search_tool.py --outline N` 展开。

## 主题索引（主题 → 章节 / 打印页）

- **PIV（速度场）** → ch13 采集；16.6 Adaptive PIV（p.485）；16.93 Stereo-PIV（p.905）；16.2–16.4 PTV（p.474 起）
- **DIC（应变/位移）** → 16.24（p.577）
- **BOS（密度梯度）** → 16.14（p.526）
- **标定** → 16.15 Camera（p.541）、16.16 精化（p.551）、16.63 Multi-Camera（p.765）、16.108 体积精化（p.965）、16.46/16.48 LIF/LII（p.678/688）
- **图像处理** → 16.22 Define Mask（p.571）、16.25 背景去除（p.584）、16.31–16.41、16.5 拼接（p.482）、16.39 IPL（p.635）
- **矢量验证** → 16.64 N-Sigma（p.774）、16.67 Peak（p.792）、16.62 Moving Average（p.763）、16.75 Range（p.825）、16.99 UOD（p.936）
- **模态分析** → 16.59–16.61（POD/sPOD/mPOD/FMD，p.722 起）
- **激光安全** → ch05（p.25）；**同步器/触发** → 14.6（p.315）；**相机选型** → 14.5（p.210）
- **Python / MATLAB / Octave 链接** → 16.74 / 16.54 / 16.65（p.824 / 696 / 777）
- **数据交换** → ch17（p.1002）；**显示与数值表** → ch18（p.1013）、ch19（p.1088）

## 语料缺口台账

固化在 `references/corpus-gaps.json`，`search_tool.py --gaps` 可查。涉及这些点时**直接引用台账口径**，不要重新检索、不要凭记忆补内容：

| 项 | 状态 | 处置口径 |
|---|---|---|
| `13.2.1 Registering 3rd party devices` | 印刷目录漏列，正文有 | 以 p.141 为准；`toc_full.json` 已补录（721+1=722） |
| 非 8.5 版本的界面/参数差异 | 超出语料 | 标 `[未覆盖·判断]`，以本机 Help / Release Notes 为准 |
| 相机/激光/同步器硬件规格 | 超出语料 | 以硬件手册为准；软件侧用 14.5 / 14.6 回答 |
| `DatasetException … failed to deserialize` | 手册不解释该异常 | 按 D 型推理，报错原文检索 0 命中即是证据 |
| `peak locking`（峰值锁定） | 全文 0 命中 | 讲现象用 sub-pixel / peak validation 原文，机制标 `[未覆盖·判断]` |
| `window offset`（窗口偏移） | 全文 0 命中 | 用 16.6.6 的 offset / displacement predictor 原文（p.495 起） |
| `self-calibration`（自标定） | 手册叫 calibration refinement | 用 16.16（p.551）原文，术语本身标 `[未覆盖·判断]` |
| `quarter rule`（1/4 法则） | 全文 0 命中 | 登记在 `param-guidelines.json`（source=judgement），必须带适用与推翻条件 |

新增缺口必须写明证据与版本，并给出处置口径，再并入 `corpus-gaps.json`。
