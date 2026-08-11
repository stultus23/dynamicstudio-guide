# Chapter 13: Acquisition（数据采集）

> 完整原文：`raw/ch13.txt`（1253 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

本章描述数据采集相关操作：在 Acquisition Mode 下使用 Acquisition Manager 进行单次或网格化（Grid）采集、通过 Imaging Setup Assistant (ISA) 完成采集设置、远程采集（Remote Controller）以及数据模拟器（Simulator）等。

## 操作步骤（关键操作）

### 打开 Acquisition Manager
- **UI 路径**：Analysis → Acquisition Manager
- **快捷键**：无（通过 Ribbon 图标或数据库双击 Grid Definition）
- **前提条件**：DynamicStudio 必须处于 Acquisition Mode，所有设备必须就绪
- **说明**：进入时会弹出警告对话框，确认禁用激光警告

### 配置网格化采集
1. 点击 **Grid Generator** 按钮
2. 选择 Grid 类型：1D / 2D / 3D（轴数）
3. 设置参数：
   - Start position（起点坐标）
   - Steps（步数）
   - Step size（步长）
4. 点击 **OK** 自动生成遍历行
5. 逐行设置参数：
   - Time between pulses（激光脉冲间隔，µs）
   - Trigger rate（触发率，Hz）
   - Number of images（图像数量）
6. 点击 **Run All** 开始采集

### 使用 ISA（Imaging Setup Assistant）
- **UI 路径**：Analysis → Imaging Setup Assistant
- **说明**：15 种预置构型（空气/水、平面/立体/体视）
- **步骤**：
  1. 从开始页面加载或点击 "Add New" 创建新配置
  2. 选择预置构型（15 种可选）：
     - 空气/水作为介质
     - 平面/立体/体视配置（1/2/4 相机）
  3. 定义介质折射率（Medium Refractive Index）
     - 气体≈1，液体按实际设定
  4. 设置测量体积（Measurement Volume）
     - 中心固定 (0,0,0)
     - 光片平行 X/Y 面，厚度中心在 Z=0
  5. 配置相机/镜头参数
     - Camera-Object distance (Zo)
     - Scheimpflug 角度
  6. 设置光片位置（Light sheet Depth）
     - 与出平面速度共同决定 Δt 上限
  7. 保存配置以便将来参考
- **关键参数**：
  - Medium Bounds：介质边界 X/Y/Z（mm）
  - Medium Refractive Index：介质折射率
  - Light sheet Depth：光片厚度
  - FoV / DoF：视场与景深

### 保存/加载采集设置
- **保存**：点击 Acquisition Manager 中的 **Save** 按钮
- **加载**：数据库中双击 Grid Definition 记录
- **说明**：设置保存在当前项目的 Grid Definition 记录中

## 章节目录（含页码）

- `13` Acquisition … p.130
- `13.1` Acquisition Manager … p.130
  - `13.1.1` Opening the Acquisition Manager … p.130
  - `13.1.2` Description of possible settings … p.131
  - `13.1.3` Buttons and Check box's in the bottom of Acquisition Manager dialog … p.132
  - `13.1.4` Grid manipulation buttons to the right of the grid … p.133
  - `13.1.5` Selecting Analysis seqeunce … p.139
  - `13.1.6` Troubleshooting … p.141
- `13.2` Device registration … p.141
  - `13.2.1` Registering 3rd party devices to unlock and enable full control of them via … p.141
  - `13.2.2` Requirements … p.141
  - `13.2.3` How to register … p.141
  - `13.2.4` Receiving the “RegisteredDeviceKeys.zip” file … p.143
- `13.3` Reporting acquisition settings … p.144
- `13.4` Storing and loading acquisition settings … p.145
- `13.5` Imaging Setup Assistant (ISA) … p.146
  - `13.5.1` ISA Step-by-Step instructions … p.146
  - `13.5.2` The Medium Bounds and Medium Refractive Index … p.147
  - `13.5.3` The Measurement Volume - Center and Size … p.148
  - `13.5.4` Hardware configuration … p.149
  - `13.5.5` 2 Examples how to use ISA to configure, plan for and setup an PIV experiment. … p.156
- `3` Illustration of the camera movement in space … p.161
- `13.6` Remote Controlled Acquisition … p.162
  - `13.6.1` How to start Remote Controlled Acquisition … p.163
  - `13.6.2` Information on the Remote Control Driver … p.164
  - `13.6.3` Commands … p.165
- `13.7` PIV Simulator … p.167
  - `13.7.1` Running the experiment. … p.167
  - `13.7.2` Configuring … p.168
  - `13.7.3` Adjusting the particle engine properties … p.168
  - `13.7.4` Adjusting the camera … p.170
  - `13.7.5` Calibration images … p.171
- `13.8` Online Vectors … p.172
  - `13.8.1` Adding Online Vectors to be performed during Acquisition … p.172
  - `13.8.2` Parameters for Online Vectors … p.173
- `13.9` Adding the Focus Assist online analysis function to the … p.173
- `13.10` Understanding the resulting image from Online Focus Assist … p.174
- `13.11` Using Online Focus Assist to set up a stereo PIV system … p.177
- `13.12` Parameters for the device Online Focus Assist … p.180
  - `13.12.1` Pixel dilation Diameter … p.180
- `13.13` Synthetic image generator … p.181
  - `13.13.1` Introduction: … p.181

## 注意事项 / 警告

- Note: When entering Acquisition Manager a dialog will appear stating a warning that the Laser warning dialog will be disabled. This dialog normally appears justbefore starting an acquisition and pulsing the laser
- NOTE: You can open the Grid Definition record in Acquisition Manager by double clicking the Grid definition record in the database. Run all Clicking Run Allwillstart the acquisition specified in Acquisition Manager.
- NOTE:External dependencies must be marked as Input for Analysis before opening the Acquisition Manager. Removing a selected Analysis sequence from a row To remove a selected analysis sequence from a row in the Acquisition Manager, just select the
- NOTE: If you instead ignore the warning that you have unregistered devices connected to your system, and try to run the system by either Free run, Preview or Acquire, the system will not start acquisition,but a message box will appear asking to register the device. If you wish to continue with image acquisition without registering any device, please disable or disconnect all unregistered devices to
- shortest Camera-Object distance possible at which the object can still be focused. This will also correspond to the maximum magnification possible of the given camera /Lens configuration. Note that for small field of views a macro lens is the best option. The Focal length of the lens and the Camera-Object distance (Zo) determine the Magnification of the system as M=f/(Zo-f). The user can testdifferent settings in ISA to investigate this further before
- Note: When looking at a lightsheet at an angle instead of head on, the lens and image plane need to be tilted as illustrated below. This is known as the Scheimpflug condition and ensures proper focusing across the light sheet and over the entire Fo V. To achieve this so called Scheimpflug adaptors are mounted between the camera and the lens. Scheimpflug adaptors can be of two types
- while the camera axis follows the color of the camera. Note the 'Crosshair' that is drawn on the back end of the camera ; If the optical axis exits the camera on the horizontal line of the crosshair only Scheimpflug Pan is nonzero. In a 'Tiltonly'scenario the optical axis would exit the camera on the vertical crosshair line and in this setup, where Scheimpflug Pan & Tilt are both nonzero, it exits in
- Note: If/When the camera is looking through a window that is not normal to the optical axis Scheimpflug correction is not predicted and near/far focal planes not shown. PAGE | 152
- Note: The light sheet is always parallel to X/Y plane with a sheet depth centered on Z=0. The Light sheet Depth (or thickness) is an important parameter as it,together with information about the estimated Out-of-plane velocity, is used to calculate upper limit of the time between laser pulses (Δt) to be used in the PIV acquisition. Δt_limited by out-of-planevelocity= [¼ x Light sheet Depth
- and Depth). Note also that depending on the propagation direction of the lightsheet the light scattered from the particles will be stronger in the forward direction (i.e.in the direction of the laser propagation) than in the backward direction. This means that if the laser propagates in the positive X-direction, in the images below, both cameras in the right image (cameras on opposite side of the lightsheet) collects light scattered in the
- Note that positive Pan angles will position the camera at positive x-coordinates, while negative Pan angles will correspond to negative x-coordinates. Similarly an absolute value of the Pan angle below 90° will position the camera at positive z-coordinates (i.e.normal "Front View" with the camera in front of the light sheet), while absolute
- NOTE: The right sequence ID can be found in the "Analysis Sequence Library" RC_DELETE_RUN Can be called to delete the just acquired Run and all data below. No command string..

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示