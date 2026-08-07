# DynamicStudio 操作手册（任务索引）

> 用法：找到你的任务 → 跳转到对应 `小节（章节.编号）` → 在 `raw/chXX.txt` 中按**页码**（`PAGE|N`）定位原文读取完整步骤。
> 本文件是"怎么实现 XX 操作"类问题的第一落点。页码为手册打印页码。

## A. 安装与系统设置

| 任务 | 位置 | 说明 |
|------|------|------|
| 系统最低/推荐配置 | ch06（p.27-28） | 64 位 Windows 10、8GB 内存、NVIDIA GPU CC≥5.2 |
| 安装 DynamicStudio（管理员、关闭 UAC、拔 USB 加密狗） | ch07（p.29-30） | 安装要求管理员权限，`bcdedit /deletevalue truncatememory` 可释放保留内存 |
| 多个版本共存（6.x/7.x/8.x 可并存） | ch12.2.1（p.51） | 安装新大版本会保留旧版并复制 Analysis Sequence Library |
| 激光安全规范（Class III/IV） | ch05（p.25-26） | 佩戴激光护目镜、屏蔽反射光、对齐时低功率运行 |
| 相机传感器激光损伤预防 | ch12.1.1（p.51） | 直射/反射激光会永久损坏传感器，镜头盖常闭 |

## B. 硬件与采集设置

| 任务 | 位置 | 说明 |
|------|------|------|
| 设备注册（含第三方设备解锁） | ch13.2（p.141） | 未注册设备无法采集；注册后获得 `RegisteredDeviceKeys.zip` |
| 打开采集管理器（Acquisition Manager） | ch13.1.1（p.130） | 数据库双击 Grid Definition 或点击 Ribbon 图标；进入时激光警告被禁用 |
| Acquisition Manager 网格化批量采集 | ch13.1（p.130-141） | 定义 Grid（1D/2D/3D 遍历）、每行参数（脉冲间隔、触发率、图像数），Run All 运行 |
| 用 Grid Generator 生成遍历行 | ch13.1.4（p.133） | 选 1D/2D/3D → 起点、步数、步长 → OK 自动生成行 |
| 采集参数报告/保存加载 | ch13.3-13.4（p.144-145） | 报告当前采集设置；保存/加载采集配置文件 |
| Imaging Setup Assistant (ISA) 实验设计 | ch13.5（p.146-161） | 15 种预置构型（空气/水、平面/立体/体视），定义介质折射率、测量体积、相机/镜头、光片位置，自动估算 Δt |
| 远程控制采集（Remote Controlled Acquisition） | ch13.6（p.162-166） | 通过命令字符串（如 RC_DELETE_RUN）自动化采集 |
| PIV Simulator 模拟实验 | ch13.7（p.167-171） | 生成合成粒子图像测试分析流程 |
| 在线向量/在线对焦辅助（Online Vectors / Focus Assist） | ch13.8-13.12（p.172-180） | 采集中实时显示向量；Focus Assist 辅助立体 PIV 对焦 |
| 同步器与激光/相机的 PIV 接线 | ch14.6.2（p.345） | 推荐用 "Create Default Connections"；双腔激光 + CCD 相机典型接法 |
| 同步模式配置（内/外同步 × 内/外触发） | ch14.6.3（p.347-350） | Device properties → Trigger mode setup 三档组合 |
| 双相机不同触发率同步采集 | ch14.6.4（p.351-353） | 每相机独立 Reference time + 慢相机触发率除以 N，Image Buffer 按相机分别设置 |
| 相机参数（型号、曝光、分辨率） | ch14.5（p.210-314） | FlowSense/SpeedSense/HiSense/NanoSense 等各型号参数表 |
| 遍历系统控制（Traverse Control） | ch14.9（p.423-438） | 自动移动测量位置 |
| 主动靶标（Active Target）采集标定图像 | ch14.10.6（p.447） | 标定图像采集用（校准靶标） |
| 图像缓冲资源（Image Buffer） | ch14.5.22 / ch12.3.9（p.264/111） | 帧抓取相机需预留物理内存（truncatememory） |

## C. 标定

| 任务 | 位置 | 说明 |
|------|------|------|
| 多相机标定（Multi Camera Calibration） | ch16.63（p.765-773） | 生成各相机 IMF（成像模型拟合）；自动/半自动/手动三种模式；点阵、棋盘、双层靶标 |
| 相机标定（Camera Calibration，特殊标定） | ch16.15（p.541-550） | 立体 PIV/体积法用；UI 六部分（预览、图像滚动、靶标设置、模型、搜索设置、搜索区域） |
| 标定精化（Calibration Refinement） | ch16.16（p.551-559） | 用粒子图像精化 IMF：设置精化区域、帧、IA 尺寸，检查 Disparity Map |
| 体积标定精化（Volumetric Refinement） | ch16.108（p.965-979） | 静态/时间分辨率体积标定精化（Tomographic PIV 用） |
| 主动靶标标定流程 | ch16.63.5 / ch14.10（p.770/439） | Active Target 逐标记开关，全自动标定 |
| 坐标系统定义 | ch12.3.6（p.83-105） | 标定前必须定义；全局坐标系 Bounds 与轴定义 |
| 标定图像要求 | ch16.15（p.541） | 光照均匀、无阴影不过曝、中心标记+至少 2 邻域在视场内；多相机同索引对应同一姿态 |
| 标定模型选择 | ch16.42（p.659-667） | DLT、三阶 XYZ 多项式、Pinhole、Telecentric |
| DIC 标定 | ch16.24.1（p.577） | 散斑图相机系统标定（DIC 专用） |
| LIF / LII 标定 | ch16.46 / 16.48 / 16.49（p.678/688/689） | 荧光/激光诱导白炽光定量标定；LII 气体组分标定 |

## D. 速度场分析（PIV / PTV / 体视）

| 任务 | 位置 | 说明 |
|------|------|------|
| Adaptive PIV（自适应互相关，推荐默认） | ch16.6（p.485-495） | 自动调整 IA 尺寸/形状/位置；Grid Step Size、Min/Max IA、窗口/滤波、验证、GPU 加速、分布式分析 |
| 经典互相关（关闭自适应） | ch16.6.1（p.486） | 勾选 'Use only cross correlation' |
| Stereo-PIV（立体 PIV 处理） | ch16.93（p.905-909） | 双相机三维速度；方法/公式、输入要求、处理配方、结果显示 |
| 2-Frame 2D PTV（粒子跟踪） | ch16.2（p.474-475） | 低粒子密度下跟踪单个粒子 |
| Time-Resolved 2D PTV | ch16.3（p.476-477） | 时间分辨粒子跟踪 |
| 3D PTV | ch16.4（p.478-481） | 三维粒子跟踪测速 |
| Tomographic PTV（体视层析 PTV） | ch16.96（p.913-922） | 多相机体积速度场 |
| Ensemble PTV | ch16.26（p.591-594)） | 集合平均粒子跟踪 |
| Flex PIV（网格点自定义） | ch16.29（p.600-603） | 定义网格点与向量分析（灵活网格） |
| 自动相关（Auto-Correlation） | ch16.9（p.510） | 单帧自相关分析 |
| 平均相关（Average Correlation） | ch16.12（p.519-523） | 评估平均 PIV 信号条件、偏置向量图、预处理 |
| 互相关窗口/滤波选项 | ch16.114（p.997-999） | 窗函数与滤波函数选择 |
| 亚像素分析（Subpixel Analysis） | ch16.94（p.910） | 相关峰亚像素插值 |

## E. 验证与矢量后处理

| 任务 | 位置 | 说明 |
|------|------|------|
| 矢量验证方法总览（有效性/状态码） | ch19（p.1088-1090） | Status Code：0 有效、1 软件拒绝、2 手动拒绝、4 越界、8 禁用、16 替代；码可叠加（如 17=1+16） |
| N-Sigma 验证（统计离群剔除） | ch16.64（p.774-776） | 建议 N=4-6；多维用多变量正态分布（协方差矩阵 Σ） |
| Peak Validation（峰值验证） | ch16.67（p.792-793） | 相关峰质量检查；可用于相分离 |
| Moving Average 验证 | ch16.62（p.763-764） | M×N 邻域平均比较，Ap=0.12-0.15，n=2-3 次迭代 |
| Range Validation（范围验证） | ch16.75（p.825） | 速度范围约束 |
| Universal Outlier Detection | ch16.99（p.936-939） | 自适应 PIV 内置通用离群检测 |
| 矢量插值（Vector Interpolation） | ch16.103（p.946） | 缺失矢量填充 |
| 矢量掩模（Vector Masking） | ch16.104（p.948） | 掩模区域矢量剔除 |
| 矢量重采样 / 算术 / 统计 | ch16.105/101/106（p.953/942/957） | 网格重采样、矢量加减、统计量 |
| 矢量去变形（Vector Dewarping） | ch16.102（p.944-945） | 设置 z/w 值做三维去变形 |
| 标量场计算（Scalar derivatives / Scalar Map / Statistics） | ch16.80-82（p.844-854） | 速度梯度（涡量等）、标量映射、统计 |
| PIV 不确定度（PIV Uncertainty） | ch16.70（p.797-806） | Rayleigh 分布方法学、扩展不确定度 |
| 压力场重构（Pressure from PIV） | ch16.71（p.807-814） | 定义对象、压力求解器、注意事项 |
| 谱分析（Spectrum） | ch16.91（p.886） | 时间序列频谱（圆柱尾流示例） |
| 模态分析（POD/sPOD/mPOD/FMD） | ch16.59（p.722-752） | 配方与设置、均值处理、离群/掩模处理、模态数、归一化、数值导出 |
| 模态滤波 / 重构与投影 | ch16.60 / 16.61（p.752/757-762） | Modal Filter；Modal Reconstruction / POD Projection |
| 波动模态分解（OPD） | ch16.66（p.782-791） | 振荡模式分解、数值导出 |
| 概率分布（Probability Distribution） | ch16.72（p.815-816） | 掩模 + ROI 分布处理 |

## F. 图像处理

| 任务 | 位置 | 说明 |
|------|------|------|
| 图像处理库（IPL：低通/高通/形态学/工具/信号滤波，可自定义） | ch16.39（p.635-654） | 各滤波器内核与参数 |
| 图像算术（Image Arithmetic） | ch16.31（p.606-608） | 与图像/常数运算、阈值化 |
| 图像 & 体积数学（Image & Volume Math） | ch16.36（p.623-630） | 标量、函数、运算符、错误处理、中间结果保存 |
| 图像均值/最小/最大/RMS | ch16.37/38/42（p.630/631/659） | 集合统计 |
| 直方图（Histogram / Image Histogram + ROI） | ch16.30/34（p.603/616-618） | 全局或 ROI 直方图、掩模 |
| 图像掩模（Image Masking / Define Mask） | ch16.35 / 16.22（p.619/571-574） | 形状添加/删除/排序/预览、矢量图叠加 |
| 动态掩模（Dynamic Masking） | ch16.69（p.797） | 时变掩模 |
| 静态掩模生成器（Intensity Statistics / Ensemble Summation） | ch16.10/11（p.510-518） | 自动掩模生成 |
| 图像去变形（Image Dewarping） | ch16.33（p.610-616） | 重采样网格、Z 坐标、重采样方案、填充色 |
| 图像重采样（Image Re sampling） | ch16.40（p.655） | 窗口与映射 |
| 图像分辨率（Image Resolution） | ch16.41（p.658） | 分辨率调整 |
| 图像平衡（Image Balancing） | ch16.32（p.608） | 多相机亮度均衡 |
| 图像拼接（Active Image Stitching） | ch16.5（p.482-485） | 多图拼接配方与坑 |
| 裁剪/提取（Extract / ROI Extract） | ch16.27 / 16.79（p.595/842-843） | 子集提取；ROI 矩形操作 |
| 背景扣除（Dynamic background removal） | ch16.25（p.584-591） | 初始 POD 分析 + 背景估计与扣除 |

## G. 特殊测量技术

| 任务 | 位置 | 说明 |
|------|------|------|
| DIC（数字图像相关，应变/位移） | ch16.24（p.577-583） | 标定 → 处理 → 结果 |
| BOS（背景纹影，密度梯度） | ch16.14（p.526-540） | 输入 → 配方 → 显示/导出；BOS Pattern Generator |
| LIF 处理 / 燃烧 LIF | ch16.47 / 16.19（p.684/565-567） | 荧光定量；OH 燃烧自由基成像 |
| LII 处理（ROI / LoS 方法） | ch16.50（p.691-693） | 激光诱导白炽光 |
| Mie-LIF SMD（粒径） | ch16.56-58（p.709-721） | 通用/标定/处理 |
| 瑞利测温（Rayleigh Thermometry） | ch16.76（p.826-836） | 瑞利理论、分析、组分库 |
| 双色测温（Two-Color Pyrometry） | ch16.98（p.925-935） | 空间标定 + 双色标定 + 处理 |
| 阴影法（Shadow 系列：尺寸标定/统计/跟踪/相关性） | ch16.83-90（p.855-885） | 粒子阴影成像定量 |
| 喷雾几何（Spray Geometry） | ch16.92（p.891-904） | 喷嘴属性、锥形几何、喷雾形态、时间演化 |
| 相位边界检测（Phase Boundary Detection） | ch16.68（p.794-796） | 全局/局部阈值、滤波、输出、相位标签 |
| 相干滤波（Coherence Filter） | ch16.17（p.560） | 信号相干性滤波 |
| 特征跟踪（Feature Tracking） | ch16.28（p.597） | 特征点跟踪 |
| 刚体跟踪与稳定（Rigid Object Tracking/Stabilization） | ch16.78（p.839-841） | 刚体运动跟踪与稳定化 |
| 曲线拟合（Curve fit processing） | ch16.20（p.567-570） | 非线性拟合模型 |
| 波形计算/提取/统计/拼接（Waveform 系列） | ch16.110-113（p.989-997） | 波形公式、内置函数、统计值、拼接 |
| 圆柱坐标变换 / 图像坐标变换 | ch16.21（p.570） | 坐标系变换 |
| 轨迹合并/平滑（Combine Tracks / Track Smoothing） | ch16.18 / 16.77 / 16.97（p.562/837/923-925） | 轨迹合并、RBF 平滑 |

## H. 脚本与外部集成

| 任务 | 位置 | 说明 |
|------|------|------|
| Python Link（自定义分析方法） | ch16.74（p.824）及 ch16 全章 | 用 Python 脚本创建自定义分析；API 访问数据 |
| MATLAB Link | ch16.54（p.696-705） | 配方、数据选择传输、工作区变量、参数串 |
| Octave Link | ch16.65（p.777-781） | 安装 Octave、配方、工作区、输出变量 |
| 远程控制命令（RC_xxx） | ch13.6.3（p.165） | 自动化采集命令集 |
| 分析序列（Analysis Sequence）创建/管理 | ch15.1-15.4（p.461-463） | 拾取序列（Ctrl 多选→右键 Add to Library）、序列库、重复/重命名/导入导出 .sequence 文件、外部依赖标记 |

## I. 数据交换与显示

| 任务 | 位置 | 说明 |
|------|------|------|
| 数据导入/导出格式 | ch17（p.1002-1012） | 各格式说明、文件格式、图像质量增强、如何导出 |
| 数值导出（Numeric Export） | ch17.3（p.1009） | 数值表格导出 |
| 分布式分析（Distributed Analysis） | ch15.6（p.463-465） | 安装分析代理、配置、运行 |
| 分布式数据库（分布式采集） | ch15.8（p.466-467） | 远程数据收集与故障排查 |
| 显示交互（缩放/平移/显示选项） | ch18（p.1013-1087） | 通用显示交互、图像/矢量/标量显示 |
| Numeric Display（数值表） | ch19（p.1088-1090） | 矢量状态码含义、表格列配置（Quantity/Decimals/Unit） |
| 剖面图（Profile plot） | ch16.73（p.817-823） | 数据剖面显示、数值获取 |

## J. 常见问题排查

| 问题 | 位置 | 说明 |
|------|------|------|
| Acquisition Manager 采集不工作 | ch13.1.6（p.141） | 先确认 Acquisition Mode + 设备就绪 |
| 未注册设备无法采集 | ch13.2（p.141） | 弹窗要求注册，或禁用/断开未注册设备 |
| 采集不停止（双相机异速） | ch14.6.4（p.351） | Image Buffer 数量未按相机实际图像数设置 |
| 标定靶标检测失败 | ch16.15.1（p.542-544） | 使用 Image-Specific 设置、特征响应过滤、虚拟标记、参考/轴标记强制网格 |
| 分布式分析故障 | ch15.8.2（p.467） | 排查分布式数据库问题 |
| 远程桌面/多显示器缩放异常 | ch6.2.1（p.28） | 重启 DynamicStudio 恢复；所有显示器统一缩放 |

## 关联文件

- `dialogs.md` — 对话框与参数速查
- `cheatsheet.md` — 决策表（相机/激光/方法选择）
- `chapters/chXX.md` — 各章节目录（含完整小节列表与页码）