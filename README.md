# EzGit - 让 Git 操作变得简单

EzGit 是一个用 Python 编写的 Git 命令行工具，旨在简化 Git 的日常操作，让版本控制变得更加简单和友好。
## 功能特点
- 🌟 交互式菜单界面
- 🎨 彩色命令输出
- 🔧 常用 Git 操作封装
- 📝 详细的操作提示
- 🛠️ 自定义菜单配置
- 🔄 多种菜单模式
  
![image](https://github.com/user-attachments/assets/cba8bad3-b49a-4b1a-8e72-6cd3824471bc)

## 完全新手指南

### 第一步：安装必要软件

1. 安装 Python
   - 访问 [Python官网](https://www.python.org/downloads/)
   - 点击"Download Python"下载最新版本
   - 运行安装程序
   - ⚠️ 重要：安装时勾选"Add Python to PATH"选项
   - 点击"Install Now"开始安装
   - 等待安装完成

2. 安装 Git
   - 访问 [Git官网](https://git-scm.com/downloads)
   - 下载对应系统的版本
   - 运行安装程序，一路点"Next"即可
   - 等待安装完成

### 第二步：下载 EzGit

方法一：使用 Git（推荐）
```bash
# 打开命令提示符(CMD)或PowerShell，输入：
git clone https://github.com/SoKeiKei/EzGit.git
```

方法二：直接下载
- 访问 [EzGit主页](https://github.com/SoKeiKei/EzGit)
- 点击绿色的"Code"按钮
- 选择"Download ZIP"
- 解压下载的文件

### 第三步：运行 EzGit

1. 进入程序目录
```bash
# 在命令提示符(CMD)或PowerShell中输入：
cd EzGit  # 如果你在其他目录，需要输入完整路径
```

2. 安装可选依赖（推荐但不是必需）
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python EzGit.py
```

### 基本操作说明

1. 选择功能
   - 使用数字键选择对应功能
   - 按回车确认

2. 常用操作
   - 1：查看仓库状态
   - 2：暂存更改
   - 3：提交更改
   - 4：推送更改
   - 5：拉取更新

3. 其他操作
   - h：显示帮助
   - 0：退出程序

## 常见问题解答

### 1. 提示"python不是内部或外部命令"
- 原因：Python未添加到系统PATH
- 解决方法：重新安装Python，记得勾选"Add Python to PATH"

### 2. 提示"git不是内部或外部命令"
- 原因：Git未添加到系统PATH
- 解决方法：重新安装Git

### 3. 提示"pip不是内部或外部命令"
- 解决方法：使用 `python -m pip` 替代 `pip`
```bash
python -m pip install -r requirements.txt
```

### 4. 运行时显示乱码
- 解决方法：在命令提示符中输入：
```bash
chcp 65001
```

### 5. 其他问题
- 访问 [Issues页面](https://github.com/SoKeiKei/EzGit/issues) 寻求帮助

## 进阶使用

当你熟悉了基本操作后，可以尝试：
- 分支管理
- 远程仓库操作
- 标签管理
- 配置管理
- 自定义菜单

## 贡献代码

1. Fork 本仓库
2. 创建新分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License

## 作者

[SoKei](https://github.com/SoKeiKei)

## 更新日志

### v1.0.0 (2025-03-09)
- 初始版本发布
- 实现基本的 Git 操作功能
- 添加交互式菜单界面
- 支持自定义菜单配置
- 添加多种菜单模式
- 实现彩色输出支持

## 使用方法

### 方法一：作为独立工具使用（推荐新手）

按照上面的"完全新手指南"操作即可。

### 方法二：在任意项目中快速使用（推荐）

1. 复制单文件版本
   - 只需要复制 `EzGit.py` 文件到你的项目目录
   - 特点：
     * 单文件，无需安装，无需配置
     * 即复制即用，不生成任何配置文件
     * 轻量级，仅包含核心 Git 操作
     * 可以复制到任何项目目录独立使用

```bash
# 使用方法
# 1. 复制 EzGit.py 到任意项目目录
# 2. 在该目录下运行：
python EzGit.py
```

2. 创建命令行别名（可选）
   
Windows (在 PowerShell 中):
```powershell
# 添加别名到 PowerShell 配置
Set-Alias -Name git-tool -Value "python C:\完整路径\EzGit.py"

# 之后可以在任何目录使用：
git-tool
```

Linux/Mac:
```bash
# 添加别名到 .bashrc 或 .zshrc
alias git-tool="python /完整路径/EzGit.py"

# 之后可以在任何目录使用：
git-tool
```

### 功能说明

1. 核心功能
   - ✅ 基本的 Git 操作（status, add, commit, push, pull 等）
   - ✅ 分支管理（创建、切换、合并等）
   - ✅ 远程仓库操作（clone, remote 等）
   - ✅ 交互式菜单界面
   - ✅ 彩色输出支持

2. 不包含的功能
   - ❌ 配置文件管理
   - ❌ 自动更新检查
   - ❌ 自定义菜单
   - ❌ 日志记录
   - ❌ 多语言支持

3. 优点
   - 轻量级，单文件
   - 无需配置
   - 不生成额外文件
   - 可以复制到任何项目使用
   - 启动速度快

4. 使用建议
   - 适合日常 Git 操作
   - 适合快速部署到新项目
   - 适合团队共享使用
   - 适合教学演示
