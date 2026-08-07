# Chapter 7: Note to Administrators（管理员须知）

> 完整原文：`raw/ch07.txt`（32 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

All installation scripts from Dantec Dynamics A/S contain a digital signature (code signing cer-
tificate) issued by (CA) VeriSign, Inc. (http://www.verisign.com) ensuring correct identity.
Installation requires administrative privileges, but running can also be done under restricted/limited
(non-admin) user-accounts. When installing under a restricted/limited user account, the user is
requested to run (Run As...) the installation as an administrative user.
Installation requires disabling of User Access Control (UAC). Go to the Windows Control Panel and
search for UAC to turn it off before installing (requires reboot). It is however highly recommended to
turn it on again after the installation.
To accomplish restricted/limited user account support, the following permissions are altered during
installation:
l All users ("Everyone") are permitted full file access to the "All Users\Shared Documents\Dantec
Dynamics" folder including all sub folders.
l All XML configuration and library files are installed in the "All Users\Shared Documents\Dantec
Dynamics\Dynamic Studio" folder, allowing shared access for all users.

## 操作步骤（关键操作）

### 安装要求
- **权限**：需要管理员权限
- **UAC**：安装前禁用 UAC，安装后建议重新启用
- **步骤**：
  1. 以管理员身份运行安装程序
  2. 禁用 UAC（控制面板 → UAC）
  3. 重启计算机
  4. 完成安装
  5. 重新启用 UAC

### Windows 防火墙配置
- **说明**：配置防火墙允许 DynamicStudio 通信

### BCDEDIT.exe
- **说明**：用于释放保留内存（truncatememory）

## 章节目录（含页码）

- `7` Note to Administrators … p.29
  - `7.0.1` Installation … p.29
- `7.1` Windows Firewall … p.29
- `7.2` BCDEDIT.exe … p.29

## 注意事项 / 警告

- 7 Note to Administrators

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示