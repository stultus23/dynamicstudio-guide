# DynamicStudio 对话框与参数速查

> 按功能提问时（"XX 参数是什么意思/怎么调"）使用本文件；详情见 `raw/chXX.txt` 对应页码。

## 1. Acquisition Manager（采集管理器）— ch13.1（p.130-141）

| 参数/控件 | 含义 | 默认/建议 |
|-----------|------|-----------|
| Analysis sequence | 对采集数据自动应用的分析序列；在"Selecting Analysis seqeunce"选择 | 无 |
| Start delay | 采集启动时的延迟；延迟期间相机禁用但其余设备运行 | 0 |
| Prompt | 勾选后每行采集前弹 OK 对话框确认 | 关 |
| Traverses | 遍历轴显示为独立列（如 Active Target Traverse） | — |
| Time between pulses | 激光两脉冲间隔，µs（双帧模式核心参数） | 按流速设定 |
| Trigger rate | 事件触发率，Hz；单帧=每脉冲率，双帧=每双脉冲率 | 按实验 |
| Number of images | 每个遍历位置的采集图像数 | 依需求 |
| Save for calibration | 勾选后图像另存为标定图像 | 关 |
| Postpone Analysis | 勾选后全部采集完成再执行分析，否则每行采集后立即分析 | 关 |
| Save | 保存为数据库 Grid Definition 记录（双击记录可重新打开） | — |
| Run all / Stop | 启动/停止整个网格采集 | — |
| Manage manual axis | 手动轴支持：Add/Remove Axis，设置 Name/Min/Max/Type/前缀；运行时提示手动移动 | — |

### Grid Generator（p.138）
1. 选择 Grid 类型：1D / 2D / 3D（轴数）
2. 设置起点（Start position）、步数（Steps）、步长（Step size）
3. OK 后自动生成行；Run name convention：Creation time / Position / Index

## 2. Imaging Setup Assistant (ISA) — ch13.5（p.146-161）

| 参数 | 含义 |
|------|------|
| Medium Bounds | 介质边界 X/Y/Z（mm），默认 (-300,300;-200,200;-300,300) |
| Medium Refractive Index | 介质折射率 n=c/v；气体≈1，液体按实际设定 |
| Measurement Volume (MV) | 期望成像体积；中心固定 (0,0,0)；光片平行 X/Y 面，厚度中心在 Z=0 |
| Light sheet Depth | 光片厚度；与出平面速度共同决定 Δt 上限：Δt ≤ ¼×光片厚度/出平面速度 |
| FoV / DoF | 当前相机+镜头的视场与景深可视化 |
| Camera-Object distance (Zo) | 放大率 M=f/(Zo-f)；小视场用微距镜头 |
| Scheimpflug | 相机与镜头间倾斜适配器（Pan/Tilt），保证光片平面聚焦；透过非垂直窗口时校正不可预测 |
| 模板选择 | 15 种预置构型：平面（1 相机）/立体（2 相机，同侧或对侧）/体积（4 相机 Fan/Plus/Cross）；测量穿过水窗时窗口应垂直于光轴，推荐窗口∥光片 |

## 3. 同步器（Synchronizer）— ch14.6（p.315-404）

| 模式 | 说明 |
|------|------|
| Internal sync + internal trigger（默认） | 按 System Control 面板 Trigger rate 运行，按 Acquire 启动 |
| External sync + internal trigger | 触发率由 Trigger input 2 的外部同步设备给定 |
| Internal sync + external trigger | Trigger input 1 收到脉冲启动；帧率由 System Control 指定 |
| 双相机异速 | 每相机独立 Reference time；慢相机触发率÷N；Image Buffer 按各自实际图像数设置 |

接线建议：使用 "Create Default Connections"（Synchronization Cables 面板）。
典型 2D-2C PIV：双腔激光（如 DualPower 145-15，15 Hz）+ CCD（如 FlowSense EO 4M-32，双帧 15 Hz）。

## 4. 设备参数 — ch14.5（p.210-314）

相机通用参数（以各型号 "Parameters for the camera" 小节为准）：Resolution、Bit Depth、Exposure Time、Interframe time、FPS、Pixel Size、Double frame 支持。
典型型号：FlowSense CX（高分辨率）、FlowSense EO（通用）、SpeedSense（高速）、HiSense（低光/荧光）、NanoSense（微型）、PCO Dimax、Photron Nova。

## 5. Adaptive PIV（自适应 PIV）— ch16.6（p.485-495）

| 参数 | 含义 | 建议 |
|------|------|------|
| Grid Step Size | IA 间距（像素），决定矢量密度；小于 IA 尺寸则重叠 | 依需求，越小矢量越多 |
| Min / Max IA Size | IA 尺寸自适应范围；首轮迭代用最大 IA | 按粒子密度与梯度 |
| Use only selected region | 只分析 ROI 矩形区域 | 关 |
| Use only cross correlation | 关闭自适应，退化为经典固定 IA 互相关（快速测试/基准） | 关 |
| Enable GPU acceleration | NVIDIA GPU CC≥5.2 且 ≥2GB 内存 | 检测到 GPU 时开 |
| Window/Filter | 空间窗函数与频域滤波 | 依信噪比 |
| Validation | 内置 Universal Outlier Detection 等验证 | 依数据质量 |
| 分布式分析 | 本地多数据集并行计算加速 | 可开 |

## 6. 验证方法参数 — ch16.62-75（p.763-825）

| 方法 | 参数 | 典型值 |
|------|------|--------|
| N-Sigma（16.64） | 接受限 N | N=4-6（正态分布 99% 在 3σ 内，4-6 兼顾非正态） |
| Peak Validation（16.67） | 相关峰质量参数 | 交互式调参；相分离示例 |
| Moving Average（16.62） | 邻域 M×N、接受因子 Ap、迭代数 n | M=N=3/5/7；Ap=0.12-0.15；n=2-3 |
| Range Validation（16.75） | 速度范围上下限 | 按物理预期 |
| Universal Outlier Detection（16.99） | 通用离群检测 | — |

## 7. 相机标定 — ch16.15 / 16.63（p.541-550/765-773）

| 项 | 说明 |
|----|------|
| 标定模型 | DLT / 3'rd order XYZ 多项式 / Pinhole / Telecentric（16.42，p.659-671） |
| 靶标类型 | 点阵、棋盘、双层多级、单面/双面；主动靶标（逐点开关）、被动靶标；靶标库或自定义参数 |
| 标定模式 | 全自动 / 半自动（自动检测标记+手动指定原点）/ 手动（手工放置网格） |
| 标定图像要求 | 光照均匀、无阴影、不过曝；中心标记+至少 2 个邻域标记在视场内；多相机时各相机同一索引对应同一靶标姿态 |
| Search Settings（16.15.1） | 通用搜索设置；Image-Specific 设置（光照/透视问题图像）；特征响应黄点标记、红圈拒绝、绿色虚拟标记；参考/轴标记强制网格生成 |
| 精化（16.16，p.556-564） | 输入：标定图像+粒子图像；设置精化区域、帧、IA 尺寸；检查 Disparity Map / Average Correlation Map / Dewarped Particle Images |

## 8. 分析序列（Analysis Sequence）— ch15（p.461-463）

| 操作 | 步骤 |
|------|------|
| 创建 | 手动执行各分析步骤到满意 → Ctrl 多选结果 → 右键 "Add Analysis Sequence to Sequence Library" |
| 应用 | 右键数据 → Apply Analysis Sequence → 从全局序列库选择（父数据必须匹配，如单帧序列只能用于单帧） |
| 管理 | 序列库：命名、描述、删除；Duplicate（Ctrl+D）→"copy of…"；F2/右键 Rename；导入导出 .sequence 文件 |
| 外部依赖 | 依赖分析必须标记为 Input for Analysis 才能用于序列；点步骤查看依赖关系 |

## 9. Numeric Display（数值表）— ch19（p.1088-1090）

| 列 | 含义 |
|----|------|
| # | 连续行号（唯一 ID） |
| Grid Indexes (x, y) | 矢量在矢量图中的位置（列/行） |
| x(pix), y(pix) | 矢量像素坐标（IA 中心，偶数尺寸→坐标恒以 .5 结尾） |
| x(mm), y(mm) | 公制坐标（依 "Define Axes" 设置） |
| Upix, Vpix | 粒子图像位移（像素） |
| U, V | 公制速度（基于标定比例与激光脉冲间隔 Δt） |
| Length | 矢量欧氏长度 |
| Status Code | 位编码：0 有效、1 软件拒绝、2 手动拒绝（legacy）、4 Outside、8 Disabled、16 Substituted；可叠加（17=1+16）；显示时取最高位 |

## 10. 输出与导出 — ch17（p.1002-1012）

- 支持格式与文件格式说明见 ch17.1-17.2；导出方式见 ch17.2.4 "How to Export Data"（p.1008）
- Numeric Export（p.1009）：数值导出
- 数据交换/Distributed Database 见 ch15.8（p.466-467）