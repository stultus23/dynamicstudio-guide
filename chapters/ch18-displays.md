# Chapter 18: Displays（显示）

> 完整原文：`raw/ch18.txt`（1224 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

Displays（显示窗口）用于在屏幕上绘制、制图与可视化数据，在 DynamicStudio 内以多个窗口呈现。显示类型有多种，分别针对不同类型的数据：少数专用于展示特定分析结果，多数为通用显示，可展示多种分析方法的结果，常用类型如 Image map（图像图）、Vector map（矢量图）、Scalar map（标量图）。大多数数据也可数值化显示：在数据库树中右键数据 ensemble 选择 "Open as Numeric"，或选中 ensemble 后点击工具栏对应图标；数值显示的实际内容取决于父数据集与数据类型。

## 操作步骤（关键操作）

### 打开显示窗口
- **UI 路径**：右键数据 → Open as → 选择显示类型
- **显示类型**：
  - Image Map（图像显示）
  - Vector Map（矢量显示）
  - Scalar Map（标量显示）
  - Numeric（数值显示）

### 调整显示选项
- **UI 路径**：显示窗口 → 右键 → Display Options
- **操作**：
  - Zoom（缩放）：鼠标滚轮或工具栏
  - Pan（平移）：鼠标中键拖动
  - Color map（颜色映射）：右键选择
  - Histogram（直方图）：查看数据分布

### 使用数值显示
- **UI 路径**：右键数据 → Open as Numeric
- **说明**：显示矢量状态码、坐标、速度等数值信息

## 章节目录（含页码）

- `18` Displays … p.1013
- `18.1` General Display Interaction … p.1013
- `18.2` Zoom and Pan … p.1013
  - `18.2.1` Zooming … p.1013
  - `18.2.2` Panning … p.1015
- `18.3` Display Rulers … p.1015
- `18.4` Using the display from within an analysis method … p.1017
  - `18.4.1` Zoom … p.1018
  - `18.4.2` Pan … p.1018
  - `18.4.3` Magnifying glass … p.1018
  - `18.4.4` Color map … p.1018
  - `18.4.5` Adjusting the ellipse … p.1019
  - `18.4.6` Adjusting the polygon … p.1020
  - `18.4.7` Adjusting the rectangle … p.1021
- `18.5` Image Map Display … p.1022
  - `18.5.1` Color map and Histogram … p.1026
  - `18.5.2` Particle Density Probe … p.1030
  - `18.5.3` Correlation Map Display … p.1034
- `18.6` Vector Map Display … p.1037
  - `18.6.1` Vector Map display options … p.1037
  - `18.6.2` Examples of realizable displays … p.1043
- `18.7` Scalar Map Display … p.1045
  - `18.7.1` More visualization methods… … p.1045
- `18.8` Overlays … p.1048
- `18.9` Group Displays … p.1055
  - `18.9.1` Create and edit a group display … p.1056
- `18.10` 3D Display … p.1057
  - `18.10.1` 3D Voxel Display … p.1058
  - `18.10.2` Interacting with the voxel volume display … p.1058
  - `18.10.3` The display options for voxel volumes … p.1059
  - `18.10.4` Images … p.1062
  - `18.10.5` Vectors … p.1063
  - `18.10.6` Iso-surfaces … p.1067
  - `18.10.7` Contours … p.1069
  - `18.10.8` Streamlines … p.1071
  - `18.10.9` Legends … p.1072
  - `18.10.10` Stereo Rendering … p.1073
  - `18.10.11` Animation … p.1073
  - `18.10.12` Camera … p.1073
  - `18.10.13` Export … p.1074
- `18.11` XY-Plot … p.1074
  - `18.11.1` Graphical user interface … p.1074
  - `18.11.2` Legend … p.1075
  - `18.11.3` Info Box … p.1076
  - `18.11.4` Zooming … p.1076
  - `18.11.5` Probe … p.1077
  - `18.11.6` Default setup … p.1077
  - `18.11.7` Display Options … p.1078
  - `18.11.8` Data Selection … p.1078
  - `18.11.9` Plot Setup … p.1079
  - `18.11.10` Axis Setup … p.1079
  - `18.11.11` Line Style … p.1080
- `18.12` Numeric Display … p.1081

## 注意事项 / 警告

- Note that the grayscale depth in the firstlineis now 32-bits, a single precision floating point with 24bitmantissa and 8-bitexponent (both signed). Double precision 64-bit floating point would have been possible, but takes up twice as much storage space and is rarely justified with the limited 8-, 10- or 12-bit resolution of the acquired images. The info box can be turned off (or back on) via the Context menu (right-clicksomewhere in the display window). This can be useful when multiple display windows are open and you wish to use
- "Vector map" on page 1039 ).Note that for a better visualization, all the measured vectors are not plotted using the "Index skipping" feature.
- Please Note: When a data set isfirstoverlaid on top of another, the overlaid data set will always be the firstdataset from its ensemble, regardless if the parent data set onto which itisoverlaid is not the first in its ensemble. As soon as you browse forward or back in the parent ensemble the system will however try to synchronize the overlaid data set(s).
- space the grey values shall be 0. Note that they will rarely reallyshow 0 because ghost values are always introduced during the reconstruction. By a right mouse click the numerical values of the zintensity profile, or the diagram can be exported The “Show probe” hides the voxels in the volume, and can also be selected from the displays right click menu.
- Note, all settings can be applied without closing the display options dialog.

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示