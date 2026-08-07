# Chapter 15: Analysis（分析）

> 完整原文：`raw/ch15.txt`（287 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

After images and related data is acquired an Analysis can be applied, selecting Analyze... from the
menu. DynamicStudio includes a wide range of common analysis for image and vector processing,
LIF, particle sizing, spray diagnostics etc.
Note
The different analysis methods available are dependent on the add-on' enabled and installed on
your system.

## 操作步骤（关键操作）

### 创建分析序列
- **UI 路径**：手动执行分析步骤 → Ctrl 多选结果 → 右键 "Add Analysis Sequence to Sequence Library"
- **步骤**：
  1. 手动执行各分析步骤到满意
  2. Ctrl 多选结果记录
  3. 右键选择 "Add Analysis Sequence to Sequence Library"
  4. 命名和描述序列
- **说明**：分析序列是模块化数据处理流水线

### 应用分析序列
- **UI 路径**：右键数据 → Apply Analysis Sequence → 从全局序列库选择
- **步骤**：
  1. 右键要处理的数据
  2. 选择 "Apply Analysis Sequence"
  3. 从全局序列库选择合适的序列
  4. 点击 Apply
- **前提**：父数据必须匹配（如单帧序列只能用于单帧）

### 管理分析序列
- **UI 路径**：Analysis Sequence Library
- **操作**：
  - Duplicate（Ctrl+D）：复制序列
  - F2/右键 Rename：重命名
  - 导入/导出 .sequence 文件
  - 删除序列

### 配置分布式分析
- **UI 路径**：Analysis → Distributed Analysis
- **步骤**：
  1. 安装 Analysis Agent 软件
  2. 配置分布式分析设置
  3. 选择分析代理
  4. 配置结果存储位置
- **说明**：支持本地多数据集并行计算加速

### 使用外部依赖
- **说明**：依赖分析必须标记为 Input for Analysis 才能用于序列
- **步骤**：
  1. 选择依赖分析
  2. 标记为 "Input for Analysis"
  3. 在序列中查看依赖关系

## 章节目录（含页码）

- `15` Analysis … p.461
- `15.1` Analysis Sequence … p.461
  - `15.1.1` "Pickup" an Analysis Sequence … p.461
- `15.2` Analysis Sequence Library … p.461
- `15.3` Using Analysis Sequences … p.462
- `15.4` Predefined Analysis Sequences … p.462
  - `15.4.1` Use of Analysis Sequences … p.463
- `15.5` Context menu … p.463
- `15.6` Distributed Analysis … p.463
  - `15.6.1` Installing Analysis Agent software … p.463
  - `15.6.2` Configuring Distributed Analysis. … p.463
  - `15.6.3` Analyzing using Distributed Analysis … p.464
- `15.7` Analysis results … p.466
- `15.8` Distributed Database … p.466
  - `15.8.1` Collecting remotely stored data … p.467
  - `15.8.2` Troubleshooting Distributed Database … p.467
- `15.9` Custom Properties … p.468
  - `15.9.1` Example … p.468
- `15.10` Timestamp … p.468
- `15.11` Selection (Input to Analysis) … p.468
  - `15.11.1` Example … p.468
- `15.12` Fixed Selection (Input to Analysis) … p.468

## 注意事项 / 警告

- Note The differentanalysis methods available are dependent on the add-on' enabled and installed on your system.
- The Configuration Wizard will guide you through the selection of Analysis Agents to be used. Note that itis not possible to disable the local Analysis Agent.
- (Note: Itispossible to specify for each Analysis Agent if results are to be saved distributed or in the main database. This is done in the Pending Analysis Jobs dialog.)
- (Note: itis not possible to remove a job that is being analyzed). After having started the execution of the jobs in the queue, and after the firstjob is finished the system tries to give an estimate on how long time it will take to do the rest of the jobs in the queue. This estimate is presented just below the job content.

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示