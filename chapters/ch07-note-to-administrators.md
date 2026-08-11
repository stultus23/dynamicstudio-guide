# Chapter 7: Note to Administrators（管理员须知）

> 完整原文：`raw/ch07.txt`（32 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

Dantec Dynamics 的所有安装脚本均带数字签名（VeriSign 代码签名证书）以确保来源正确。安装需要管理员权限，但也可在受限/非管理员账户下运行（需以管理员身份 "Run As..." 执行安装）。安装前须禁用 Windows 用户账户控制（UAC，需重启），强烈建议安装后重新启用。为支持受限账户，安装过程会修改权限：所有用户（Everyone）对 "All Users\Shared Documents\Dantec Dynamics" 及其子文件夹拥有完全文件访问权；所有 XML 配置与库文件安装到 "All Users\Shared Documents\Dantec Dynamics\Dynamic Studio" 文件夹，供所有用户共享访问。

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