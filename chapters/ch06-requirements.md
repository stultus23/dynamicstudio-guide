# Chapter 6: Requirements（系统要求）

> 完整原文：`raw/ch06.txt`（52 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

系统最低要求：64 位 PC，现代多核 Intel 处理器；64 位 Windows 10（含最新服务包与更新）；Windows Installer v3.5 或更高；.NET 4.8；8 GB 内存；FHD（1920×1080）或更高分辨率、数百万色显示器；鼠标或兼容指点设备。GPU 加速处理要求：NVIDIA GPU（Compute Capability 5.2 及以上，显存至少 2 GB），NVIDIA 驱动 ≥ 516.94。

## 操作步骤（关键操作）

### 检查系统要求
- **最低要求**：
  - 64 位 Windows 10
  - 8 GB RAM
  - FHD 显示器
  - NVIDIA GPU CC≥5.2（GPU 处理）
- **推荐配置**：
  - 多核 Intel 处理器
  - 16 GB+ RAM
  - NVIDIA GPU CC≥5.2 且 ≥2GB 内存

### 安装 DynamicStudio
- **步骤**：
  1. 移除所有 USB 加密狗
  2. 以管理员身份运行安装程序
  3. 关闭 UAC（用户账户控制）
  4. 按照安装向导完成安装
  5. 安装完成后重新插入 USB 加密狗

## 章节目录（含页码）

- `6` Requirements … p.27
- `6.1` Minimum requirements … p.27
- `6.2` Recommended configuration … p.27
  - `6.2.1` High DPI monitors … p.28

## 注意事项 / 警告

- Warning: All USB dongles must be removed during the installation! During the installation,additional third-party products are installed: Rainbow Sentinel System Driver: This driver can be updated or removed using the add/remove pane in the Windows Control Panel. For more information or driverupdates please visitwww.rainbow.com.

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示