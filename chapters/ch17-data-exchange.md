# Chapter 17: Data Exchange（数据交换）

> 完整原文：`raw/ch17.txt`（386 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

You can import images into DynamicStudio using the Image Import option from the File Menu.
Data can be exported from DynamicStudio to disk through different methods:
l
Image export: The dataset is exported as an image that can be viewed and processed by
external programs
l Numeric data: The data is exported as a numeric representation to a file. The data rep-
resentation is similar to that shown in the numeric view.
l Ensemble zip export: The selected ensembles can be zipped into zip file representing a sub set
of the existing database.
l Dataset export: Specific datasets can be selected from the content list to a zip file.
l Dataset export with dependencies: The selected dataset and its dependencies are com-
pressed in a zip file.

## 操作步骤（关键操作）

### 导入图像
- **UI 路径**：右键数据库/项目/运行/集合 → Import images → Import as single-frame/double-frame
- **支持格式**：
  - .bmp（Windows 位图）
  - .tif/.tiff（TIFF 格式）
  - .jpg/.jpeg（JPEG 格式）
  - .png（PNG 格式）
  - .raw（原始格式）
  - .im7/.imx（DaVis 二进制图像）
- **步骤**：
  1. 右键选择导入位置
  2. 选择 "Import as single-frame" 或 "Import as double-frame"
  3. 选择图像文件
  4. 配置导入选项（Timing parameters、Ensemble name）
  5. 点击 Import
- **说明**：JPEG/PNG/BMP 自动转换为 8 位灰度图像

### 导出图像
- **UI 路径**：右键数据 → Export → Image Export
- **支持格式**：TIFF、BMP、JPEG、PNG
- **步骤**：
  1. 选择要导出的数据
  2. 右键选择 "Export"
  3. 选择 "Image Export"
  4. 选择导出格式
  5. 配置导出选项
  6. 点击 Export

### 导出数值数据
- **UI 路径**：右键数据 → Export → Numeric Export
- **步骤**：
  1. 选择要导出的数据
  2. 右键选择 "Export"
  3. 选择 "Numeric Export"
  4. 配置导出格式和参数
  5. 点击 Export
- **说明**：数值表格导出，类似 Numeric Display 布局

### 导出数据集
- **UI 路径**：右键数据 → Export → Dataset Export
- **导出类型**：
  - Dataset export：导出特定数据集
  - Dataset export with dependencies：导出数据集及其依赖
  - Ensemble zip export：导出集合作为 ZIP 文件
- **步骤**：
  1. 选择要导出的数据
  2. 右键选择 "Export"
  3. 选择导出类型
  4. 选择保存位置
  5. 点击 Export

## 章节目录（含页码）

- `17` Data Exchange … p.1002
- `17.1` Image Import … p.1002
  - `17.1.1` Formats … p.1002
  - `17.1.2` How to Import Images … p.1003
  - `17.1.3` Note … p.1006
- `17.2` Image Export … p.1006
  - `17.2.1` Formats … p.1006
  - `17.2.2` File Format … p.1007
  - `17.2.3` Enhanced image quality … p.1008
  - `17.2.4` How to Export Data … p.1008
- `17.3` Numeric Export … p.1009

## 注意事项 / 警告

- same position in the two listswillbe matched together to create a single double-frame image. Note that if the imported images are already double-frame images, likedouble-frame TIFF files,then the "Frame 2" listwillnot appear and the two frames will be taken from the same file. Above each list of images, a text is added with "Image count: " to show how many images are in the
- shown in Figure 5. Note that when importing to an existing ensemble, the camera selection will be disabled as the camera from the existing ensemble is used.
- There are two different timing parameters, "Time between pulses" and "Trigger rate".Note that the time between pulses is only available for double-frame import and only when creating a new run. If you are importing to an existing run, the time between pulses for the existing run is used. Similarly, if you are importing to an existing ensemble with at least two images in it,the trigger rate will be
- alternative name. Note that if you are importing to an existing ensemble, itis not possible to change the ensemble name here. Finally, press the import button to begin the import of the images.
- 17.1.3 Note If you want to use your imported images as calibration images you can move them to a calibration ensemble afterwards.
- Note Most image viewers and tools in Windows does not support 16-bit integer or 32-bit floating point tiff images. An example ofa image processing tool that do support these tiffformats is Image J (http://rsbweb.nih.gov/ij/)

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示