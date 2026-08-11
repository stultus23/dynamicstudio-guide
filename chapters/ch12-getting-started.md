# Chapter 12: Getting Started（快速入门）

> 完整原文：`raw/ch12.txt`（1431 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

DynamicStudio 图像采集系统由软件及在线图像采集功能构成，可按需配置参数集进行数据采集、预览与存盘；采集完成后可调用大量数据处理方法进行后续分析。控制相机与照明系统（通常为激光）、硬件同步及数据采集/传输的采集硬件通常与软件安装在同一台 PC 上。系统支持多种相机，可配置单台或多台相机（通常为多台同型号），并由同步单元为所有相机、光源及/或快门设备产生触发脉冲。支持的设备参见 "Cameras"（p.210）、"Synchronizers"（p.315）、"Illumination Systems"（p.405）。

## 操作步骤（关键操作）

### 创建数据库
- **UI 路径**：File → New Database
- **步骤**：
  1. 选择数据库保存位置
  2. 输入数据库名称
  3. 点击 Create
- **说明**：数据库是所有实验数据和配置的集中存储

### 配置坐标系统
- **UI 路径**：Database → Properties → Coordinate System
- **关键参数**：
  - Bounds（坐标范围）
  - Axis definition（轴定义）
  - Scale factor（比例因子）
- **步骤**：
  1. 定义全局坐标系
  2. 设置坐标范围（Bounds）
  3. 配置轴方向
  4. 设置比例因子（mm/pixel）
- **说明**：标定前必须定义坐标系统

### 使用用户界面
- **主要组件**：
  - System Control 面板（系统控制）
  - Device tree（设备树）
  - Database view（数据库视图）
  - Ribbon 工具栏
- **操作模式**：
  - Free run（自由运行）
  - Preview（预览）
  - Acquire（采集）

### 配置设备
- **UI 路径**：Devices → 设备类型
- **步骤**：
  1. 连接硬件设备
  2. 在设备树中查找设备
  3. 配置设备参数
  4. 测试设备功能

### 使用 Demo 数据
- **UI 路径**：File → Open Database → Demo Data
- **说明**：包含示例数据，用于学习和测试

## 章节目录（含页码）

- `12` Getting Started … p.51
- `12.1` Warranties and Disclaimers … p.51
  - `12.1.1` Camera Sensor Warranty … p.51
- `12.2` Installation … p.51
  - `12.2.1` Multiple installations of DynamicStudio … p.51
- `12.3` Using DynamicStudio … p.52
  - `12.3.1` User Interface … p.52
  - `12.3.2` Normal Use … p.63
  - `12.3.3` Database Access … p.73
  - `12.3.4` Delete and Restore … p.77
  - `12.3.5` Working with the Database … p.79
  - `12.3.6` Coordinate System … p.83
  - `12.3.7` DynamicStudio Agent Setup … p.106
  - `12.3.8` Light Source Wizard … p.106
  - `12.3.9` Image Buffer resources … p.111
  - `12.3.10` Ensemble Linking … p.111
  - `12.3.11` Calibration Images … p.115
  - `12.3.12` AgentHost service … p.117
  - `12.3.13` Known issues … p.118
  - `12.3.14` Database with Demo Data … p.120
  - `12.3.15` Combined PIV-DIC measurements … p.122
  - `12.3.16` Dantec Dynamics Feedback Tool … p.125

## 注意事项 / 警告

- l Calibration: is the tab used for spatial calibration, scales factor computation and coordinate system layout. Note it is important to measure scale factors, or perform calibration before data ana- tem layout. Note it is important to measure scale factors, or perform calibration before data analysis! l Analysis: is used to process data, from pre-prpcessing until exportation of a final video.
- tem layout. Note it is important to measure scale factors, or perform calibration before data analysis! l Analysis: is used to process data, from pre-prpcessing until exportation of a final video.
- Note Common to all run modes is that acquired data can be saved to the database. After selecting "Acquire" or "Preview" it might be needed that cameras or other sensors might need calibration. Therefore DynamicStudio automatically checks if the calibration of one or more devices is needed and will warn the user, in case not all sensors are calibrated which is described in the following section.
- when selecting "Define axes" the following dialog will appear. Note that you can not assign axis directions, these are set up in the interfaces of the "Multi Camera Calibration", the "Measure Scale Factor" or the "Field of View" together with the scale factor. When axes are re assigned, itis of importance that in record properties, and in allot her parts of
- But Note if you change the settings for the Axis definition or your scalefactor after you have processed images you have to re compute your results to make the changes beeing affective. Storing and Evaluating Acquired Images Whether acquisition stops automatically or because you click Stop, the last images acquired will remain in the buffer for evaluation and storage.
- Note: For some cameras -especially High-Speed cameras -preview mode will result in bursts of measurements. While each burst will have the correct frame rate, the overall data rate may not be the same as when using the "acquire" mode. Acquire
- Note: In all run modes acquired data can be saved to the database. Storing and evaluating and Acquired Images Whether acquisition stops automatically or because you click Stop, the last images acquired will remain in the buffer for evaluation and storage.
- Warning: Moving data around in the database may lead to loss of information, such as dependency between various datasets and it may thus corrupt the database. Moving ensembles is entirely the users responsibility, not recommended and should be done only in extreme necessity. PAGE | 76
- Note: Even if you set up the system to delete items older than 7 days the waste bin may in factcontainitems that are older. This is because the clean-up takes place when the database is closed, not when it is opened. Imagine that you close a database and decide to keep deleted items that are less than 7 days old. If two weeks pass before the database is opened again it may then contain deleted items that are 3 weeks old.
- In DynamicStudio, by default each set of acquired images is given a right handed coordinate system in pixels with it´s0|0|0 -location in the upper leftcorner of an image. Note, the center location is not the corner of a pixel, but it´s center, as shown in the next image:
- Also Note, the X-direction is towards the right hand side and the y-direction is vertical direction. By default when looking on the same image in metric scaling, still with the default properties, it´s coordinate 0|0|0 - location now is on the lower left corner. By default the scaling of a pixel is 1 mm /pixel and the right handed coordinate system is positive to the right and the top of the image, see
- Note: The value of the scale factor represents the magnification of the lens system. Therefore the physical size of a pixel element (pixel pitch) is needed to perform the conversion into metric units. The formula is:unitsmm = Scale Factor * Pixel_Pitchmm. To leave the dialog and save the current settings press the OK -button.

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示