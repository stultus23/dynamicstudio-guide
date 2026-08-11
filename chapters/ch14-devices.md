# Chapter 14: Devices（设备）

> 完整原文：`raw/ch14.txt`（7563 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

Devices（设备）指所有连接到 DynamicStudio 的外部硬件，包括相机、激光器、同步器、AD 板等，通过设备树注册与管理。

## 操作步骤（关键操作）

### 添加/注册设备
- **UI 路径**：Devices → 设备类型 → 右键添加
- **说明**：未注册设备无法采集，需要获得 RegisteredDeviceKeys.zip
- **步骤**：
  1. 连接硬件设备
  2. 在设备树中查找设备
  3. 右键设备选择注册
  4. 导入注册密钥文件

### 配置相机参数
- **UI 路径**：Devices → Cameras → 相机型号 → Properties
- **关键参数**：
  - Resolution（分辨率）：图像尺寸（如 1600×1200）
  - Exposure Time（曝光时间）：相机曝光时间（ms）
  - Interframe time（帧间隔）：双帧模式的时间间隔
  - FPS（帧率）：每秒帧数
  - Double frame（双帧模式）：启用/禁用双帧采集
  - Bit Depth（位深度）：8/10/12 位
  - Pixel Size（像素大小）：传感器像素尺寸
- **说明**：
  - 不同相机型号参数可能不同
  - UI 有三种视图：Standard、Advanced、Expert
  - 只有 Expert 视图显示所有可能的设置
- **典型型号**：
  - FlowSense CX（高分辨率）
  - FlowSense EO（通用）
  - SpeedSense（高速）
  - HiSense（低光/荧光）
  - NanoSense（微型）

### 配置同步器
- **UI 路径**：Devices → Synchronizers → Properties
- **步骤**：
  1. 使用 **Create Default Connections** 自动接线
  2. 配置触发模式（Internal/External sync）
  3. 设置触发率（Trigger rate）
  4. 配置激光脉冲间隔（Time between pulses）
- **典型配置**：双腔激光 + CCD 相机的 PIV 接线

### 配置遍历系统
- **UI 路径**：Devices → Traverse Systems → Traverse Control
- **步骤**：
  1. 连接遍历控制器
  2. 配置轴参数（Name/Min/Max/Type）
  3. 设置移动速度和精度
  4. 测试移动功能

### 使用 Active Target 标定
- **UI 路径**：Devices → Active Target → Properties
- **步骤**：
  1. 连接 Active Target
  2. 配置标记开关模式
  3. 采集标定图像
  4. 自动标定流程

## 章节目录（含页码）

- `14` Devices … p.186
- `14.1` Lens Mounts … p.186
  - `14.1.1` Remote lens control … p.186
  - `14.1.2` SpeedSense Ethernet camera Canon lens mount … p.189
- `14.2` 1-Axis Scheimpflug mounts … p.191
  - `14.2.1` Instructions for mounting the FlowSense EO cameras 192 … p.191
  - `14.2.2` Scheimpflug 1-Axis 194 … p.191
  - `14.2.3` Instructions for mounting the SpeedSense 1040 cameras 196 … p.191
  - `14.2.4` Scheimpflug 1-Axis 198 … p.191
  - `14.2.1` Instructions for mounting the FlowSense EO cameras … p.191
  - `14.2.2` Scheimpflug 1-Axis … p.191
  - `14.2.3` Instructions for mounting the SpeedSense 1040 cameras … p.191
  - `14.2.4` Scheimpflug 1-Axis … p.191
- `14.3` Image Intensifiers … p.200
  - `14.3.1` Custom Image Intensifier … p.201
  - `14.3.2` Hamamatsu Image Intensifier … p.203
- `14.4` Analog Input … p.205
  - `14.4.1` Analog Input … p.205
  - `14.4.2` Installation … p.205
  - `14.4.3` Connecting hardware for acquisition … p.206
  - `14.4.4` Preparing software for acquisition … p.207
  - `14.4.5` Acquiring data … p.210
- `14.5` Cameras … p.210
  - `14.5.1` Basler ACA1920-155um camera … p.210
  - `14.5.2` HiSense Mk I … p.213
  - `14.5.3` HiSense Mk II Camera … p.214
  - `14.5.4` HiSense NEO and Zyla Camera … p.215
- `2160` 28.2 30.8 … p.220
- `1040` 74.6 75.0 … p.220
- `512` 152 152 … p.220
- `256` 300 301 … p.220
- `128` 358 592 … p.220
- `48` 566 1396 … p.220
- `512` 201 … p.220
- `128` 716 … p.220
- `512` 201 … p.220
- `128` 716 … p.220
  - `14.5.5` FlowSense 2M Camera … p.220
  - `14.5.6` FlowSense 4M Camera … p.222
  - `14.5.7` FlowSense CM 12M-70 … p.224
  - `14.5.8` FlowSense CX 4M-563 … p.227
  - `14.5.9` Parameters for the camera … p.229
  - `14.5.10` FlowSense CX 12M-160 … p.232
  - `14.5.11` Parameters for the camera … p.234
  - `14.5.12` FlowSense CX 25M-80 … p.236
  - `14.5.13` Parameters for the camera … p.238
  - `14.5.14` FlowSense CX2 21M-230 … p.241
  - `14.5.15` FlowSense EO Camera series … p.244
- `4` Tap cameras can only run in4 Tab mode., where as other cameras can run in single or dual tap … p.249
  - `14.5.16` FlowSense FCX series … p.249
  - `14.5.17` FlowSense GigE Camera series … p.255
  - `14.5.18` FlowSense USB 2M-165 … p.258
- `3` Controller might not provide the bandwidth needed to run the camera at maximum frame rate. … p.262
  - `14.5.19` HiSense 4M Camera … p.262
  - `14.5.20` HiSense 11M Camera … p.262
  - `14.5.21` HiSense 6XX cameras … p.263
  - `14.5.22` Image buffer resources … p.264
  - `14.5.23` MSpeed DIC … p.265
  - `14.5.24` Parameters for the camera … p.266
  - `14.5.25` NanoSense Camera Series … p.269
  - `14.5.26` PCO Dimax … p.272
  - `14.5.27` Photron Nova … p.274
  - `14.5.28` Photron camera series … p.276
  - `14.5.29` SpeedSense 10XX series … p.287
  - `14.5.30` SpeedSense 1040 camera … p.290
  - `14.5.31` Parameters for the camera … p.292
  - `14.5.32` SpeedSense Ethernet Cameras … p.294
- `9020` 1152 x 896 8, 10, n/a n/a 1000 11.5 … p.295
- `9030` 800 x 600 8, 10, n/a n/a 6688 22 … p.295
- `9040` 1632 x 1200 8, 12, n/a 1500 1016/508 11.5 … p.295
- `9041` 1600 x 1200 8,12, n/a n/a 1000/500 11.5 … p.296
- `9050` 2400 x 1800 8,12, n/a 1500 480/240 11.5 … p.296
- `9060` 1280 x 800 8,12 n/a n/a 6242/3121 20 yes … p.296
- `9070` 1280 x 800 8,12 n/a n/a 3140/1570 20 yes … p.296
- `9072` 1280 x 800 8,12 n/a n/a 2190/1095 20 yes … p.296
- `9080` 2560 x 1600 8,12 n/a n/a 1514/757 10 yes … p.296
- `9084` 2560 x 1600 12 n/a n/a 1450/725 10 yes … p.296
- `9090` 1280 x 800 8,12 n/a n/a 7500/3750 20 yes … p.296
- `211` 1280 x 800 8,12 1 700 2190 20 yes … p.296
- `311` 1280 x 800 8,12 1 700 3250 20 yes … p.296
- `611` 1280 x 800 8,12 1 500 6242 20 yes … p.296
- `711` 1280 x 800 8,12 1 500 7530 20 yes … p.296
- `341` 2560 x 1600 8,12 1 400 12000 10 yes … p.296
- `641` 2560 x 1600 12 1 400 16000 10 yes … p.296
- `1210` 1280 x 800 12 1 400 12700/6350 28 yes … p.296
- `1610` 1280 x 800 12 1 400 16600/8300 28 yes … p.296
- `1211` 1280 x 800 12 1 725 12600/6300 28 yes … p.296
- `1611` 1280 x 800 12 1 525 16600/8300 28 yes … p.296
- `2511` 1280 x 800 12 1 375 25600/12800 28 yes … p.296
- `2512` 1280 x800 12 1 375 25700/12850 28 yes … p.297
- `1840` 2048 x1952 12 .5 142ns fast 4510 /17240 13.5 yes … p.297
- `2640` 2048 x1952 12 .5 142ns fast 6600/ 25030 13.5 yes … p.297
  - `14.5.33` Web camera support … p.309
  - `14.5.34` Streaming to disk … p.311
- `14.6` Synchronizers … p.315
  - `14.6.1` High Performance Synchronizer and Performance Synchronizer … p.315
  - `14.6.2` Setting up the Synchronizer for PIV measurements … p.345
  - `14.6.3` Synchronization setup … p.347
  - `14.6.4` Running two cameras synchronized but at different trigger rate … p.351
  - `14.6.5` Additional settings … p.354
  - `14.6.6` How to use the TrueTime Add-on and the Light Trap … p.354
  - `14.6.7` Mini Synchronizer … p.358
  - `14.6.8` Scanning Light Sheet controller … p.369
  - `14.6.9` Synchronization … p.372
  - `14.6.10` USB Timing HUB … p.374
  - `14.6.11` Start options … p.375
  - `14.6.12` Mode options … p.377
  - `14.6.13` Limitations … p.378
  - `14.6.14` High Resolution Synchronizer … p.378
  - `14.6.15` Timer Box … p.382
  - `14.6.16` Installing the TimerBox … p.382
  - `14.6.17` Connecting the timer box … p.383
  - `14.6.18` Synchronization setup … p.384
  - `14.6.19` Synchronizing two Timer Boxes … p.386
  - `14.6.20` Additional settings … p.387
  - `14.6.21` Cyclic Synchronizer and Linear Synchronizer … p.388
  - `14.6.22` Using Two Synchronizers … p.403
  - `14.6.23` Pulse Receiver … p.403
- `14.7` Illumination Systems … p.405
  - `14.7.1` Brilliant B laser … p.406
  - `14.7.2` DualPower Lasers … p.407
  - `14.7.3` Time resolved lasers … p.409
  - `14.7.4` Evergreen Laser … p.410
  - `14.7.5` Lee Lasers … p.411
  - `14.7.6` Microstrobe … p.411
  - `14.7.7` New Wave Lasers … p.412
  - `14.7.8` Pulsed Lasers … p.413
  - `14.7.9` Dual Cavity pulsed lasers … p.413
  - `14.7.10` Shutter Devices … p.413
  - `14.7.11` Tunable Dye Laser … p.413
  - `14.7.12` Quantel Q-smart laser … p.415
- `14.8` Microscopes … p.418
  - `14.8.1` Leica M165FC microscope … p.418
- `14.9` Traverse systems … p.423
  - `14.9.1` Traverse Control … p.423
- `3` 20,-4 loop the last4 lines 20 times … p.437
- `14.10` Other Devices … p.439
  - `14.10.1` Active Target … p.440
  - `14.10.2` Active Target Control … p.440
  - `14.10.3` Active Target … p.443
  - `14.10.4` Active PC Screen Target … p.444
  - `14.10.5` Synchronizer … p.447
  - `14.10.6` Acquiring calibration images with the Active Target … p.447
  - `14.10.7` Measuring … p.450
  - `14.10.8` Active Target Traverse … p.450
  - `14.10.9` Calibration Control … p.451
  - `14.10.10` DualScope … p.455
  - `14.10.11` HFSB Generator … p.456
  - `14.10.12` Image format … p.457

## 注意事项 / 警告

- Reset Warning/Error State The Hamamatsu image intensifier needs to be reset ifawarning has been issued or an error has occurred. This drop-down reveals a button that has to be pressed to perform a reset. Camera attached
- Note: the UI shown above has three different options. Standard, Advanced, and Expert. Only in Expert view will all the possible settings be available. When selecting a Device Property in the list window a small explanation is shown at the bottom. Specification, Image Sensor and Device information are informal only.
- Note that the trigger settings are only needed if the camera is triggered remotely with a Dantec Dynamics Synchronization device. Image Sensor Calibration> PAGE | 212
- Note that if the data should be streamed to disc an SSD with at least 1200MB/s writing speed is needed. Furthermore it should not be more than half full.
- Note: Synchronization The camera is triggered via the Frame grabber. The frame grabber can control up to 4 cameras that all can be triggered through the frame grabber. Connect the Sync output on the synchronizer to Trig
- but can be deactivated Note: If Pixel Reset Mode is switched on, the maximum frame rate for ROIs with a width <3200 pixel is limited. In practical use this does not cause any problem as this mode is not used with higher frame rates ---
- Note: The Black reference and Flat fieldcorrection must be performed while images are acquired by the camera and shown in the user interface. Do a Free run or Preview to perform the calibration. Black reference
- Note: Synchronization The camera is triggered via the Frame grabber. The frame grabber can control up to 4 cameras that all can be triggered through the frame grabber. Connect the Sync output on the synchronizer to Trig
- Note: The Black reference and Flat field correction must be performed while images are acquired by the camera and shown in the user interface. Do a Free run or Preview to perform the calibration. Black reference
- Note: Synchronization The camera is triggered via the Frame grabber. The frame grabber can control up to4 cameras that all can be triggered through the frame grabber. Connect the Sync output on the synchronizer to Trig
- but can be deactivated Note: If PixelResetMode is switched on, the maximum frame rate for ROIs with a width <3200 pixel is limited. In practical use this does not cause any problem as this mode is not used with higher frame rates Fixed Pattern Noise Reduction:
- Note: The Black reference and Flat field correction must be performed while images are acquired by the camera and shown in the user interface. Do a Free run or Preview to perform the calibration. Semi Automatic Sensor calibration

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示