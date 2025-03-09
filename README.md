# EzGit - 让 Git 操作变得简单

EzGit 是一个用 Python 编写的 Git 命令行工具，旨在简化 Git 的日常操作，让版本控制变得更加简单和友好。

## 功能特点

- 🌟 交互式菜单界面
- 🎨 彩色命令输出
- 🔧 常用 Git 操作封装
- 📝 详细的操作提示
- 🛠️ 高级功能支持

## 功能列表

### 常用操作
- 仓库状态 (status/init/clone)
- 暂存更改 (add)
- 提交更改 (commit)
- 历史查看 (log)
- 推送更改 (push)
- 拉取更新 (pull)

### 分支操作
- 分支管理 (branch)
- 切换分支 (checkout)
- 合并分支 (merge)
- 变基操作 (rebase)

### 远程操作
- 远程配置 (remote)
- 标签管理 (tag)

### 高级操作
- 储藏操作 (stash)
- 版本管理 (reset/revert/restore)
- 仓库维护 (clean/gc)
- 分析工具 (stats/search/diff)
- 配置管理 (config/alias)

## 安装说明

### 前置要求

1. Python 3.6+
2. Git

### 安装步骤

1. 下载程序
```bash
git clone https://github.com/SoKeiKei/EzGit.git
```

2. 运行程序
```bash
cd EzGit
python EzGit.py
```

## 使用方法

### 方法一：作为独立工具使用

直接运行 `EzGit.py` 文件，通过交互式菜单进行操作。

### 方法二：在任意项目中使用

1. 复制 `EzGit.py` 到项目目录
2. 在该目录下运行 `python EzGit.py`

### 快捷方式设置（可选）

Windows (PowerShell):
```powershell
Set-Alias -Name git-tool -Value "python 路径\EzGit.py"
```

Linux/Mac:
```bash
alias git-tool="python /路径/EzGit.py"
```

## 功能说明

### 1. 版本管理
- 重置操作 (git reset)
- 还原操作 (git revert)
- 恢复操作 (git restore)

### 2. 仓库维护
- 清理未跟踪文件 (git clean)
- 压缩仓库 (git gc)
- 文件系统检查 (git fsck)
- 引用完整性检查 (git prune)

### 3. 分析工具
- 统计分析 (提交统计、贡献者统计等)
- 仓库搜索 (提交、内容、文件搜索)
- 版本比较 (分支、提交、文件比较)

### 4. 配置管理
- Git 配置
- 别名管理
- 工具设置

## 常见问题

### 1. 提示"python不是内部或外部命令"
- 确保 Python 已正确安装并添加到系统 PATH

### 2. 提示"git不是内部或外部命令"
- 确保 Git 已正确安装并添加到系统 PATH

### 3. 显示乱码
```bash
chcp 65001  # Windows 命令提示符中执行
```

## 作者

[SoKei](https://github.com/SoKeiKei)

## 许可证

MIT License
