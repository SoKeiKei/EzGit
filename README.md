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

## 基本功能

- 仓库状态查看
- 文件暂存管理
- 提交更改
- 历史记录查看
- 远程仓库操作
- 分支管理
- 标签管理

## 高级功能

- 储藏管理
- 配置信息管理
- 错误恢复
- 差异比较
- 工作流管理
- 子模块管理

## 安装说明

1. 克隆仓库：
```
git clone https://github.com/SoKeiKei/EzGit.git
```

2. 安装可选依赖（推荐但不是必需）：
```
pip install -r requirements.txt
```
- requests: 用于检查更新（可选）
- colorama: Windows系统下的彩色输出支持（可选）

3. 运行程序：
```
python EzGit.py
```

## 使用说明

### 基本操作
- 使用数字键选择对应功能
- 按 'h' 查看帮助信息
- 按 '0' 退出程序
- 按 'm' 切换菜单模式
- 按 'c' 自定义菜单

### 菜单模式
1. 完整模式
   - 显示所有可用功能
   - 适合熟悉 Git 的用户
2. 简单模式
   - 仅显示常用功能
   - 适合新手用户
3. 自定义模式
   - 根据个人需求定制菜单
   - 可添加/删除功能项

### 配置说明
- 配置文件位置：~/.ezgit/
  - config.json：工具配置
  - menu_config.json：菜单配置
- 可配置项：
  - 主题颜色
  - 默认分支
  - 自动推送
  - 作者信息

## 开发说明

### 环境要求
- Python 3.6+
- Git 命令行工具

### 测试运行
- 运行测试：python test_ezgit.py
- 测试内容：
  - 文件结构完整性
  - 基本功能可用性
  - 高级功能实现
  - 工具功能正常
  - 辅助函数可用

### 代码规范
- 遵循 PEP 8 规范
- 使用 JSDoc 风格注释
- 函数必须有明确的返回值

## 依赖项目

- requests：用于检查更新和网络请求
- colorama：用于 Windows 系统下的彩色输出

## 贡献指南

1. Fork [本仓库](https://github.com/SoKeiKei/EzGit)
2. 创建特性分支
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
