#!/usr/bin/env python3
import os
import subprocess
import sys

def print_colored(text, color):
    """
    打印彩色文本
    @param text: str 文本内容
    @param color: str 颜色名称
    @return: None
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'end': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def execute_git(command):
    """
    执行 Git 命令
    @param command: list Git 命令及参数
    @return: bool 是否执行成功
    """
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['LANG'] = 'en_US.UTF-8'
        
        result = subprocess.run(['git'] + command, 
                              capture_output=True, 
                              text=True,
                              encoding='utf-8',
                              env=env)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            if "no upstream branch" in result.stderr:
                print("首次推送分支，正在设置上游分支...")
                current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                             capture_output=True,
                                             text=True,
                                             encoding='utf-8').stdout.strip()
                push_result = subprocess.run(['git', 'push', '--set-upstream', 'origin', current_branch],
                                          capture_output=True,
                                          text=True,
                                          encoding='utf-8')
                if push_result.stdout:
                    print(push_result.stdout)
                if push_result.stderr:
                    print(push_result.stderr)
            else:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print_colored(f"执行出错: {str(e)}", "red")
        return False

def show_menu():
    """
    显示主菜单
    @return: None
    """
    logo = """
 _____     _____ _ _   
|  ___|   / ____(_) |  
| |__ ____| |  __ _| |_ 
|  __|_  /| | |_ | | __|
| |___/ / | |__| | | |_ 
|____/___|\_____|_|\__|
"""
    print("\n" + "="*50)
    print_colored(logo, "cyan")
    print_colored("让Git操作变得简单! 作者: SoKei", "purple")
    print("="*50)

    print_colored("\n[常用操作]", "yellow")
    print("1. 仓库状态     (git status/init/clone)")
    print("2. 暂存更改     (git add)")
    print("3. 提交更改     (git commit)")
    print("4. 历史查看     (git log)")
    print("5. 推送更改     (git push)")
    print("6. 拉取更新     (git pull)")

    print_colored("\n[分支操作]", "yellow")
    print("7. 分支管理     (git branch)")
    print("8. 切换分支     (git checkout)")
    print("9. 合并分支     (git merge)")
    print("10. 变基操作    (git rebase)")

    print_colored("\n[远程操作]", "yellow")
    print("11. 远程配置    (git remote)")
    print("12. 标签管理    (git tag)")

    print_colored("\n[高级操作]", "yellow")
    print("13. 储藏操作    (git stash)")
    print("14. 版本管理    (reset/revert/restore)")
    print("15. 仓库维护    (clean/gc)")
    print("16. 分析工具    (stats/search/diff)")
    print("17. 配置管理    (config/alias)")

    print_colored("\n[其他选项]", "yellow")
    print("h. 显示帮助")
    print("0. 退出程序")
    print("\n" + "="*50)

def show_help():
    """
    显示帮助信息
    @return: None
    """
    print_colored("\n=== EzGit 使用帮助 ===", "cyan")
    print_colored("Version: 1.0.0", "purple")
    print_colored("Author: SoKei", "purple")
    print_colored("GitHub: https://github.com/SoKeiKei/EzGit", "purple")
    print_colored("Last Update: 2025-03-09", "purple")  # 添加更新日期
    
    print("\n基本操作说明：")
    print("1. 使用数字键选择对应的功能")
    print("2. 大部分操作都有详细的子菜单和提示")
    print("3. 操作过程中可以输入 'q' 返回上级菜单")
    
    print("\n常见工作流程：")
    print_colored("1. 查看状态 -> 暂存更改 -> 提交更改 -> 推送到远程", "green")
    print_colored("2. 拉取更新 -> 创建分支 -> 修改代码 -> 提交推送", "green")
    
    print("\n注意事项：")
    print_colored("- 推送前请确保已经提交所有更改", "yellow")
    print_colored("- 建议经常使用 git status 检查仓库状态", "yellow")
    print_colored("- 重要操作前建议使用 git stash 储藏更改", "yellow")
    
    input("\n按回车键返回主菜单...")

def confirm_action(message):
    """
    通用的操作确认函数
    @param message: str 确认信息
    @return: bool 是否确认
    """
    print_colored(f"\n{message}", "yellow")
    choice = input("确认执行？(y/n): ").lower()
    return choice == 'y'

def handle_add():
    """
    处理git add命令的优化版本
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("文件暂存管理", "cyan")
        print("="*40)
        print("1. 暂存所有更改   (git add .)")
        print("2. 暂存指定文件   (git add <file>)")
        print("3. 交互式暂存     (git add -p)")
        print("\n说明: 交互式暂存可以让你逐块审查并选择要暂存的更改")
        print("     每块更改都可以选择:")
        print("     y - 暂存这块更改")
        print("     n - 不暂存这块更改")
        print("     s - 将这块拆分成更小的块")
        print("     q - 退出")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git(['add', '.'])
            print_colored("\n✓ 已暂存所有更改", "green")
        elif choice == "2":
            file_name = input("请输入要暂存的文件名(支持通配符): ")
            if execute_git(['add', file_name]):
                print_colored(f"\n✓ 已暂存 {file_name}", "green")
        elif choice == "3":
            print_colored("\n进入交互式暂存模式...", "cyan")
            print("你可以逐块审查更改并决定是否暂存")
            execute_git(['add', '-p'])
            print_colored("\n✓ 交互式暂存完成", "green")
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_commit():
    """
    处理git commit命令
    @return: None
    """
    message = input("\n请输入提交信息: ")
    if message:
        if execute_git(['commit', '-m', message]):
            print_colored("\n✓ 提交成功!", "green")
            # 显示提交详情
            execute_git(['log', '-1', '--stat'])
            # 等待用户查看提交信息
            input("\n按回车键继续...")
        else:
            if input("\n提交失败，是否跳过检查重试？(y/N): ").lower() == 'y':
                if execute_git(['commit', '-m', message, '--no-verify']):
                    print_colored("\n✓ 提交成功! (跳过检查)", "green")
                    execute_git(['log', '-1', '--stat'])
                    input("\n按回车键继续...")
                else:
                    print_colored("\n✗ 提交失败", "red")
                    input("\n按回车键继续...")

def handle_branch():
    """
    处理分支管理
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("分支管理", "cyan")
        print("="*40)
        
        # 先显示当前分支状态
        execute_git(['branch', '-av'])
        
        print("\n1. 创建新分支")
        print("2. 删除分支")
        print("3. 重命名分支")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            name = input("\n请输入新分支名称: ")
            if input("切换到新分支？(Y/n): ").lower() != 'n':
                if execute_git(['checkout', '-b', name]):
                    print_colored(f"\n✓ 已创建并切换到分支 {name}", "green")
            else:
                if execute_git(['branch', name]):
                    print_colored(f"\n✓ 已创建分支 {name}", "green")
        elif choice == "2":
            name = input("\n请输入要删除的分支名: ")
            if execute_git(['branch', '-d', name]):
                print_colored(f"\n✓ 已删除分支 {name}", "green")
        elif choice == "3":
            old = input("\n请输入当前分支名: ")
            new = input("请输入新分支名: ")
            if execute_git(['branch', '-m', old, new]):
                print_colored(f"\n✓ 已将分支 {old} 重命名为 {new}", "green")
        else:
            print_colored("无效的选择", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_clone():
    """
    处理git clone命令
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("克隆仓库", "cyan")
        print("="*40)
        
        print("\n1. 克隆远程仓库")
        print("2. 克隆指定分支")
        print("3. 克隆指定标签")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            url = input("\n请输入仓库地址: ")
            if confirm_action("是否克隆到当前目录？"):
                execute_git(['clone', url, '.'])
            else:
                path = input("请输入目标目录: ")
                execute_git(['clone', url, path])
        elif choice == "2":
            url = input("\n请输入仓库地址: ")
            branch = input("请输入分支名: ")
            execute_git(['clone', '-b', branch, url])
        elif choice == "3":
            url = input("\n请输入仓库地址: ")
            tag = input("请输入标签名: ")
            execute_git(['clone', '-b', tag, url])
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_config():
    """
    处理 Git 配置
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("Git 配置", "cyan")
        print("="*40)
        print("1. 查看所有配置")
        print("2. 设置用户信息")
        print("3. 设置默认编辑器")
        print("4. 设置默认分支名")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-4): ")

        if choice == "0":
            return
        elif choice == "1":
            execute_git(['config', '--list'])
        elif choice == "2":
            username = input("\n请输入Git用户名: ")
            email = input("请输入Git邮箱: ")
            if username:
                execute_git(['config', '--global', 'user.name', username])
            if email:
                execute_git(['config', '--global', 'user.email', email])
        elif choice == "3":
            editor = input("\n请输入编辑器命令(如 vim, nano): ")
            if editor:
                execute_git(['config', '--global', 'core.editor', editor])
        elif choice == "4":
            branch = input("\n请输入默认分支名(如 main): ")
            if branch:
                execute_git(['config', '--global', 'init.defaultBranch', branch])
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_remote():
    """
    处理远程仓库管理
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("远程仓库管理", "cyan")
        print("="*40)
        
        print("\n1. 查看远程仓库")
        print("2. 添加远程仓库")
        print("3. 修改远程仓库URL")
        print("4. 删除远程仓库")
        print("5. 重命名远程仓库")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-5): ")
        
        if choice == "0":
            return
        elif choice == "1":
            # 先检查是否有远程仓库
            result = subprocess.run(['git', 'remote'], 
                                 capture_output=True, 
                                 text=True,
                                 encoding='utf-8')
            if result.stdout.strip():
                print("\n当前远程仓库列表:")
                execute_git(['remote', '-v'])
            else:
                print_colored("\n当前仓库没有配置任何远程仓库", "yellow")
                print("提示: 使用选项 2 添加远程仓库")
        elif choice == "2":
            remote_name = input("\n请输入远程仓库名称(默认 origin): ") or "origin"
            remote_url = input("请输入远程仓库URL: ")
            execute_git(['remote', 'add', remote_name, remote_url])
            print_colored(f"\n成功添加远程仓库: {remote_name}", "green")
        elif choice == "3":
            # 先检查并显示现有远程仓库
            result = subprocess.run(['git', 'remote'], 
                                 capture_output=True, 
                                 text=True,
                                 encoding='utf-8')
            if not result.stdout.strip():
                print_colored("\n当前仓库没有配置任何远程仓库", "yellow")
                print("提示: 请先添加远程仓库")
                input("\n按回车键继续...")
                continue
                
            print("\n当前远程仓库列表:")
            execute_git(['remote', '-v'])
            remote_name = input("\n请输入要修改的远程仓库名称: ")
            remote_url = input("请输入新的远程仓库URL: ")
            execute_git(['remote', 'set-url', remote_name, remote_url])
            print_colored(f"\n成功更新远程仓库 {remote_name} 的URL", "green")
        elif choice == "4":
            # 先检查并显示现有远程仓库
            result = subprocess.run(['git', 'remote'], 
                                 capture_output=True, 
                                 text=True,
                                 encoding='utf-8')
            if not result.stdout.strip():
                print_colored("\n当前仓库没有配置任何远程仓库", "yellow")
                input("\n按回车键继续...")
                continue
                
            print("\n当前远程仓库列表:")
            execute_git(['remote', '-v'])
            remote_name = input("\n请输入要删除的远程仓库名称: ")
            if confirm_action(f"确定要删除远程仓库 {remote_name} 吗？"):
                execute_git(['remote', 'remove', remote_name])
                print_colored(f"\n成功删除远程仓库: {remote_name}", "green")
        elif choice == "5":
            # 先检查并显示现有远程仓库
            result = subprocess.run(['git', 'remote'], 
                                 capture_output=True, 
                                 text=True,
                                 encoding='utf-8')
            if not result.stdout.strip():
                print_colored("\n当前仓库没有配置任何远程仓库", "yellow")
                input("\n按回车键继续...")
                continue
                
            print("\n当前远程仓库列表:")
            execute_git(['remote', '-v'])
            old_name = input("\n请输入要重命名的远程仓库名称: ")
            new_name = input("请输入新的远程仓库名称: ")
            execute_git(['remote', 'rename', old_name, new_name])
            print_colored(f"\n成功将远程仓库 {old_name} 重命名为 {new_name}", "green")
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_push():
    """
    处理推送操作
    @return: None
    """
    if execute_git(['push']):
        print_colored("\n✓ 推送成功!", "green")
        # 显示最新提交信息
        execute_git(['log', '-1', '--oneline'])
        input("\n按回车键继续...")

def handle_pull():
    """
    处理拉取操作
    @return: None
    """
    if execute_git(['pull']):
        print_colored("\n✓ 拉取成功!", "green")
        # 显示更新信息
        execute_git(['log', 'ORIG_HEAD..', '--oneline'])
        input("\n按回车键继续...")

def handle_log():
    """
    处理历史查看
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("历史查看", "cyan")
        print("="*40)
        print("1. 查看完整历史")
        print("2. 查看简化历史    (--oneline)")
        print("3. 查看分支历史    (--graph)")
        print("4. 查看文件历史")
        print("5. 搜索历史记录")
        print("6. 查看指定作者的提交")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-6): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git(['log', '--stat'])
        elif choice == "2":
            execute_git(['log', '--oneline'])
        elif choice == "3":
            execute_git(['log', '--graph', '--oneline', '--all'])
        elif choice == "4":
            file = input("\n请输入文件路径: ")
            execute_git(['log', '--follow', '--', file])
        elif choice == "5":
            keyword = input("\n请输入搜索关键词: ")
            execute_git(['log', '--grep', keyword, '--all'])
        elif choice == "6":
            author = input("\n请输入作者名称: ")
            execute_git(['log', '--author', author])
        else:
            print_colored("无效的选择", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_tag():
    """
    处理标签管理
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("标签管理", "cyan")
        print("="*40)
        
        print("\n1. 查看所有标签")
        print("2. 创建新标签")
        print("3. 删除标签")
        print("4. 推送标签")
        print("5. 检出标签")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-5): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git(['tag', '-l', '-n1'])
        elif choice == "2":
            tag_name = input("\n请输入标签名称: ")
            message = input("请输入标签说明: ")
            execute_git(['tag', '-a', tag_name, '-m', message])
        elif choice == "3":
            tag_name = input("\n请输入要删除的标签名称: ")
            if confirm_action(f"确定要删除标签 {tag_name} 吗？"):
                execute_git(['tag', '-d', tag_name])
        elif choice == "4":
            tag_name = input("\n请输入要推送的标签名称(回车推送所有标签): ")
            if tag_name:
                execute_git(['push', 'origin', tag_name])
            else:
                execute_git(['push', 'origin', '--tags'])
        elif choice == "5":
            tag_name = input("\n请输入要检出的标签名称: ")
            execute_git(['checkout', tag_name])
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_stash():
    """
    处理储藏管理
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("储藏管理", "cyan")
        print("="*40)
        
        print("\n1. 查看储藏列表")
        print("2. 储藏当前更改")
        print("3. 应用储藏")
        print("4. 删除储藏")
        print("5. 创建分支并应用储藏")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-5): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git(['stash', 'list'])
        elif choice == "2":
            message = input("\n请输入储藏说明(可选): ")
            if message:
                execute_git(['stash', 'save', message])
            else:
                execute_git(['stash'])
        elif choice == "3":
            print("\n储藏列表:")
            execute_git(['stash', 'list'])
            stash_id = input("\n请输入储藏ID(如 stash@{0}): ")
            if confirm_action("是否保留储藏？"):
                execute_git(['stash', 'apply', stash_id])
            else:
                execute_git(['stash', 'pop', stash_id])
        elif choice == "4":
            print("\n储藏列表:")
            execute_git(['stash', 'list'])
            stash_id = input("\n请输入要删除的储藏ID: ")
            if confirm_action(f"确定要删除储藏 {stash_id} 吗？"):
                execute_git(['stash', 'drop', stash_id])
        elif choice == "5":
            print("\n储藏列表:")
            execute_git(['stash', 'list'])
            stash_id = input("\n请输入储藏ID: ")
            branch_name = input("请输入新分支名称: ")
            execute_git(['stash', 'branch', branch_name, stash_id])
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def check_git_repo():
    """
    检查当前目录是否为Git仓库
    @return: bool 是否为Git仓库
    """
    try:
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],
                              capture_output=True,
                              text=True)
        return result.returncode == 0
    except Exception:
        return False

def init_repository():
    """
    初始化Git仓库
    @return: bool 初始化是否成功
    """
    print_colored("\n=== 初始化Git仓库 ===", "cyan")
    print("1. 在当前目录初始化")
    print("2. 在新目录初始化")
    print("0. 返回主菜单")
    
    choice = input("\n请选择 (0-2): ")
    
    if choice == "1":
        if confirm_action("将在当前目录初始化Git仓库"):
            return execute_git(['init'])
    elif choice == "2":
        dir_name = input("请输入新目录名称: ")
        try:
            os.makedirs(dir_name, exist_ok=True)
            os.chdir(dir_name)
            if execute_git(['init']):
                print_colored(f"\n已在 {dir_name} 目录初始化Git仓库", "green")
                return True
        except Exception as e:
            print_colored(f"创建目录失败: {str(e)}", "red")
    return False

def handle_status():
    """
    处理仓库状态相关操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("仓库状态管理", "cyan")
        print("="*40)
        print("1. 查看仓库状态")
        print("2. 初始化新仓库")
        print("3. 克隆远程仓库")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git(['status'])
            input("\n按回车键继续...")  # 给用户时间查看状态
        elif choice == "2":
            dir_name = input("\n请输入目录名(留空使用当前目录): ")
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
                os.chdir(dir_name)
            if execute_git(['init']):
                print_colored(f"\n✓ Git 仓库初始化成功!", "green")
                print(f"位置: {os.getcwd()}")
                input("\n按回车键继续...")
        elif choice == "3":
            url = input("\n请输入仓库地址: ")
            if url:
                dir_name = input("请输入目标目录(留空使用当前目录): ")
                if dir_name:
                    if execute_git(['clone', url, dir_name]):
                        print_colored(f"\n✓ 克隆成功! 目标目录: {dir_name}", "green")
                else:
                    if execute_git(['clone', url, '.']):
                        print_colored("\n✓ 克隆成功! 目标目录: 当前目录", "green")
                input("\n按回车键继续...")
        else:
            print_colored("无效的选择", "yellow")

def get_config_dir():
    """
    获取配置目录
    优先使用当前目录的 .ezgit，如果不存在则使用用户目录
    @return: str 配置目录路径
    """
    local_config = os.path.join(os.getcwd(), '.ezgit')
    if os.path.exists(local_config):
        return local_config
        
    # 用户目录作为备选
    user_config = os.path.expanduser('~/.ezgit')
    return user_config

def load_config():
    """
    加载配置文件
    @return: dict 配置信息
    """
    config_dir = get_config_dir()
    config_file = os.path.join(config_dir, 'config.json')
    
    # 确保配置目录存在
    os.makedirs(config_dir, exist_ok=True)
    
    # 加载或创建配置
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 默认配置
        default_config = {
            "author": "",
            "email": "",
            "default_branch": "main",
            "auto_push": False,
            "theme": "default"
        }
        # 保存默认配置
        save_config(default_config)
        return default_config

def setup_logging():
    """
    设置日志记录
    @return: logging.Logger 日志记录器
    """
    log_path = os.path.expanduser('~/.ezgit/ezgit.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logger = logging.getLogger('ezgit')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def parse_args():
    """
    解析命令行参数
    @return: argparse.Namespace 解析后的参数
    """
    parser = argparse.ArgumentParser(description='EzGit - 简单易用的Git命令行工具')
    parser.add_argument('-v', '--version', action='version', version='EzGit v1.0.0')
    parser.add_argument('-c', '--config', help='指定配置文件路径')
    parser.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
    parser.add_argument('command', nargs='?', help='直接执行指定的Git命令')
    
    return parser.parse_args()

def handle_advanced():
    """
    处理高级Git功能
    @return: None
    """
    print_colored("\n=== 高级功能 ===", "cyan")
    print("1. 查看差异 (git diff)")
    print("2. 变基操作 (git rebase)")
    print("3. 子模块管理")
    print("4. 工作流管理")
    print("5. 清理仓库")
    print("0. 返回主菜单")
    
    choice = input("\n请选择 (0-5): ")
    
    if choice == "1":
        handle_diff()
    elif choice == "2":
        handle_rebase()
    elif choice == "3":
        handle_submodule()
    elif choice == "4":
        handle_workflow()
    elif choice == "5":
        handle_clean()

def get_repo_root():
    """
    获取Git仓库根目录
    @return: str 仓库根目录路径或None
    """
    try:
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                              capture_output=True,
                              text=True,
                              encoding='utf-8')
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        return None

def get_relative_path(file_path):
    """
    将绝对路径转换为相对于仓库根目录的路径
    @param file_path: str 文件路径
    @return: str 相对路径
    """
    repo_root = get_repo_root()
    if repo_root and os.path.isabs(file_path):
        try:
            return os.path.relpath(file_path, repo_root)
        except:
            return file_path
    return file_path

def handle_recovery():
    """
    处理恢复操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("恢复操作", "cyan")
        print("="*40)
        print("1. 恢复工作区文件")
        print("2. 恢复暂存区文件")
        print("3. 恢复已删除的文件")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-3): ")

        if choice == "0":
            return
        elif choice == "1":
            file = input("\n请输入要恢复的文件路径(回车恢复所有): ")
            if file:
                execute_git(['restore', file])
            else:
                execute_git(['restore', '.'])
        elif choice == "2":
            file = input("\n请输入要恢复的文件路径(回车恢复所有): ")
            if file:
                execute_git(['restore', '--staged', file])
            else:
                execute_git(['restore', '--staged', '.'])
        elif choice == "3":
            print("\n查找已删除的文件...")
            execute_git(['ls-files', '--deleted'])
            file = input("\n请输入要恢复的文件路径: ")
            if file:
                execute_git(['checkout', '--', file])
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def check_update():
    """
    检查程序更新
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("检查更新", "cyan")
        print("="*40)
        
        print("\n1. 立即检查更新")
        print("2. 访问项目主页")
        print("3. 查看当前版本")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            try:
                # 先检查是否安装了 requests
                try:
                    import requests
                except ImportError:
                    print_colored("\n检查更新需要安装 requests 模块", "yellow")
                    print("\n您可以：")
                    print("1. 手动访问项目主页检查更新")
                    print("2. 安装 requests 模块启用自动检查")
                    print("\n项目主页：")
                    print_colored("https://github.com/SoKeiKei/EzGit/releases", "cyan")
                    print("\n安装命令：")
                    print_colored(f"{sys.executable} -m pip install requests", "cyan")
                    continue

                print_colored("\n正在检查更新...", "cyan")
                
                try:
                    # 获取最新版本信息
                    api_url = "https://api.github.com/repos/SoKeiKei/EzGit/releases/latest"
                    response = requests.get(api_url, timeout=5)
                    response.raise_for_status()  # 检查响应状态
                    
                    latest = response.json()
                    latest_version = latest.get('tag_name', '').lstrip('v')
                    current_version = "1.0.0"  # 当前版本号
                    
                    if not latest_version:
                        print_colored("\n暂无发布版本", "yellow")
                        return
                        
                    # 比较版本号
                    if latest_version > current_version:
                        print_colored(f"\n发现新版本: v{latest_version}", "green")
                        print(f"当前版本: v{current_version}")
                        print("\n更新内容:")
                        print(latest.get('body', '暂无更新说明'))
                        print("\n下载地址:")
                        print(latest.get('html_url', 'https://github.com/SoKeiKei/EzGit/releases'))
                    else:
                        print_colored("\n当前已是最新版本！", "green")
                        print(f"版本号: v{current_version}")
                        
                except requests.exceptions.RequestException as e:
                    if "404" in str(e):
                        print_colored("\n暂无发布版本", "yellow")
                    else:
                        print_colored(f"\n检查更新失败: 网络错误", "red")
                        print(f"错误信息: {str(e)}")
                except Exception as e:
                    print_colored(f"\n检查更新失败: {str(e)}", "red")
                    
            except Exception as e:
                print_colored(f"\n检查更新功能异常: {str(e)}", "red")
        elif choice == "2":
            print_colored("\n项目主页：", "cyan")
            print("https://github.com/SoKeiKei/EzGit")
            print("\n发布页面：")
            print("https://github.com/SoKeiKei/EzGit/releases")
        elif choice == "3":
            print_colored("\n当前版本信息：", "cyan")
            print("版本号: v1.0.0")
            print("发布日期: 2024-03-09")
            print("\n主要功能：")
            print("- 基本的 Git 操作功能")
            print("- 交互式菜单界面")
            print("- 自定义菜单配置")
            print("- 多种菜单模式")
            print("- 彩色输出支持")
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def check_dependencies():
    """
    检查必要的依赖是否已安装
    @return: bool 是否所有依赖都已安装
    """
    required_packages = ['requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("\n缺少必要的依赖包:")
        for package in missing_packages:
            print(f"- {package}")
        print("\n请使用以下命令安装依赖:")
        print("pip install " + " ".join(missing_packages))
        return False
    return True

def handle_settings():
    """
    处理工具设置
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("工具设置", "cyan")
        print("="*40)
        print("1. 显示设置")
        print("2. 操作确认设置")
        print("3. 输出颜色设置")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-3): ")

        if choice == "0":
            return
        elif choice == "1":
            print("\n当前显示设置:")
            print("1. 显示命令输出")
            print("2. 显示错误信息")
            print("3. 显示操作提示")
            if input("\n是否修改设置？(y/N): ").lower() == 'y':
                # 这里可以添加设置修改逻辑
                pass
        elif choice == "2":
            print("\n当前确认设置:")
            print("1. 危险操作确认")
            print("2. 批量操作确认")
            if input("\n是否修改设置？(y/N): ").lower() == 'y':
                # 这里可以添加设置修改逻辑
                pass
        elif choice == "3":
            print("\n当前颜色设置:")
            print("1. 成功消息: 绿色")
            print("2. 警告消息: 黄色")
            print("3. 错误消息: 红色")
            print("4. 提示消息: 青色")
            if input("\n是否修改设置？(y/N): ").lower() == 'y':
                # 这里可以添加设置修改逻辑
                pass
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_custom_menu():
    """
    处理自定义菜单设置
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("自定义菜单设置", "cyan")
        print("="*40)
        print_colored("\n说明：", "yellow")
        print("1. 自定义菜单会保留常用操作(编号1-5)")
        print("2. 自定义菜单项从编号6开始添加")
        print("3. 建议将相关功能放在同一分类下")
        print("4. 编号1-5为系统保留，不可使用")
        print("\n选项：")
        print("1. 查看当前菜单")
        print("2. 添加菜单项")
        print("3. 删除菜单项")
        print("4. 重置为默认菜单")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-4): ")
        
        config_path = os.path.expanduser('~/.ezgit/menu_config.json')
        menu_config = load_custom_menu()
        
        if choice == "0":
            return
        elif choice == "1":
            print_colored("\n当前自定义菜单：", "cyan")
            print_colored("\n[常用操作] (固定项，不可修改)", "yellow")
            for num, name, cmd in menu_config['custom_menu']["常用操作"]:
                print(f"{num}. {name} ({cmd})")
            
            for category, items in menu_config['custom_menu'].items():
                if category != "常用操作":
                    print_colored(f"\n[{category}]", "yellow")
                    for num, name, cmd in items:
                        print(f"{num}. {name} ({cmd})")
            
        elif choice == "2":
            # 显示可用的功能列表
            print_colored("\n可添加的功能列表：", "cyan")
            available_commands = {
                "基础操作": [
                    ("6", "查看历史", "git log"),
                ],
                "远程操作": [
                    ("7", "克隆仓库", "git clone"),
                    ("8", "远程配置", "git remote")
                ],
                "分支管理": [
                    ("9", "分支操作", "git branch"),
                    ("10", "切换分支", "git checkout"),
                    ("11", "合并分支", "git merge")
                ],
                "其他功能": [
                    ("12", "配置信息", "git config"),
                    ("13", "标签管理", "git tag"),
                    ("14", "储藏操作", "git stash")
                ]
            }
            
            print_colored("\n提示：编号1-5已被常用操作占用", "yellow")
            for category, items in available_commands.items():
                print_colored(f"\n[{category}]", "yellow")
                for num, name, cmd in items:
                    print(f"{num}. {name} ({cmd})")
            
            print_colored("\n请选择要添加的功能：", "green")
            print("1. 从列表中选择")
            print("2. 自定义新功能")
            add_choice = input("\n请选择 (1/2): ")
            
            if add_choice == "1":
                print_colored("\n请从上面的列表中选择：", "cyan")
                num = input("请输入菜单编号 (6-14): ")
                
                # 验证输入的编号是否有效
                all_commands = [item for items in available_commands.values() for item in items]
                selected_command = next((cmd for cmd in all_commands if cmd[0] == num), None)
                
                if selected_command:
                    print("\n可用的分类：")
                    categories = [cat for cat in menu_config['custom_menu'].keys() if cat != "常用操作"]
                    if categories:
                        print("现有分类：")
                        for i, cat in enumerate(categories, 1):
                            print(f"{i}. {cat}")
                        print("0. 创建新分类")
                    else:
                        print("(暂无分类)")
                        print("0. 创建新分类")
                    
                    cat_choice = input("\n请选择分类编号(0表示创建新分类): ")
                    
                    if cat_choice == "0":
                        category = input("请输入新分类名称: ")
                    else:
                        try:
                            category = categories[int(cat_choice)-1]
                        except:
                            print_colored("\n无效的分类编号！", "red")
                            continue
                    
                    if category not in menu_config['custom_menu']:
                        menu_config['custom_menu'][category] = []
                    menu_config['custom_menu'][category].append(selected_command)
                    print_colored("\n功能添加成功！", "green")
                else:
                    print_colored("\n无效的菜单编号！", "red")
                    continue
                    
            elif add_choice == "2":
                print_colored("\n创建自定义功能：", "cyan")
                print("提示：编号必须从6开始，1-5为系统保留编号")
                while True:
                    num = input("请输入菜单编号 (6+): ")
                    if not num.isdigit() or int(num) < 6:
                        print_colored("错误：编号必须是大于5的数字！", "red")
                        continue
                    # 检查编号是否已被使用
                    used = False
                    for cat, items in menu_config['custom_menu'].items():
                        if any(item[0] == num for item in items):
                            used = True
                            break
                    if used:
                        print_colored("错误：该编号已被使用！", "red")
                        continue
                    break
                
                name = input("请输入功能名称: ")
                cmd = input("请输入Git命令: ")
                
                print("\n可用的分类：")
                categories = [cat for cat in menu_config['custom_menu'].keys() if cat != "常用操作"]
                if categories:
                    print("现有分类：")
                    for i, cat in enumerate(categories, 1):
                        print(f"{i}. {cat}")
                    print("0. 创建新分类")
                else:
                    print("(暂无分类)")
                    print("0. 创建新分类")
                
                cat_choice = input("\n请选择分类编号(0表示创建新分类): ")
                
                if cat_choice == "0":
                    category = input("请输入新分类名称: ")
                else:
                    try:
                        category = categories[int(cat_choice)-1]
                    except:
                        print_colored("\n无效的分类编号！", "red")
                        continue
                
                if category not in menu_config['custom_menu']:
                    menu_config['custom_menu'][category] = []
                menu_config['custom_menu'][category].append((num, name, cmd))
                print_colored("\n功能添加成功！", "green")
            
        elif choice == "3":
            # 显示当前菜单项
            print_colored("\n当前自定义菜单：", "cyan")
            print_colored("\n[常用操作] (固定项，不可删除)", "yellow")
            for num, name, cmd in menu_config['custom_menu']["常用操作"]:
                print(f"{num}. {name} ({cmd})")
            
            # 收集可删除的项目
            deletable_items = []
            categories_to_delete = []
            
            for category, items in menu_config['custom_menu'].items():
                if category != "常用操作":
                    print_colored(f"\n[{category}]", "yellow")
                    for item in items:
                        if item[0] not in ["1", "2", "3", "4", "5"]:  # 只显示可删除的项目
                            deletable_items.append((category, item))
                            print(f"{item[0]}. {item[1]} ({item[2]})")
            
            if not deletable_items:
                print_colored("\n没有可删除的菜单项！", "yellow")
                continue
                
            print_colored("\n请选择要删除的菜单项：", "cyan")
            num = input("请输入菜单编号: ")
            
            # 验证是否是保留编号
            if num in ["1", "2", "3", "4", "5"]:
                print_colored("\n错误：不能删除系统保留的菜单项！", "red")
                continue
            
            # 删除选中的项目
            deleted = False
            for category in list(menu_config['custom_menu'].keys()):  # 使用list创建副本进行遍历
                if category != "常用操作":
                    items = menu_config['custom_menu'][category]
                    new_items = [item for item in items if item[0] != num]
                    if len(new_items) < len(items):
                        deleted = True
                        if new_items:  # 如果分类还有其他项目
                            menu_config['custom_menu'][category] = new_items
                        else:  # 如果分类为空，删除整个分类
                            del menu_config['custom_menu'][category]
            
            if deleted:
                print_colored("\n菜单项删除成功！", "green")
            else:
                print_colored("\n未找到指定的菜单项！", "red")
            
        elif choice == "4":
            if confirm_action("确定要重置为默认菜单吗？这将删除所有自定义项！"):
                # 获取默认菜单配置
                default_menu = {
                    "常用操作": [
                        ("1", "查看状态", "git status"),
                        ("2", "暂存更改", "git add"),
                        ("3", "提交更改", "git commit"),
                        ("4", "推送更改", "git push"),
                        ("5", "拉取更新", "git pull")
                    ]
                }
                
                # 清除所有自定义项，只保留默认菜单
                menu_config['custom_menu'] = default_menu
                
                try:
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(menu_config, f, indent=4)
                    print_colored("\n菜单已重置为默认设置！", "green")
                except Exception as e:
                    print_colored(f"\n保存配置失败: {str(e)}", "red")
                
                # 显示重置后的菜单
                print_colored("\n当前菜单设置：", "cyan")
                print_colored("\n[常用操作]", "yellow")
                for num, name, cmd in menu_config['custom_menu']["常用操作"]:
                    print(f"{num}. {name} ({cmd})")
        
        # 保存配置
        if choice in ["2", "3", "4"]:
            try:
                # 更新菜单模式和内容
                menu_config['mode'] = 'custom'  # 设置为自定义模式
                
                # 如果是重置操作，确保模式也重置为默认
                if choice == "4":
                    menu_config['mode'] = 'full'
                
                # 一次性保存所有更改
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(menu_config, f, indent=4)
                
                if choice == "4":
                    print_colored("\n菜单已重置为默认设置！", "green")
                else:
                    print_colored("\n菜单已更新，已切换到自定义菜单模式！", "green")
            except Exception as e:
                print_colored(f"\n保存配置失败: {str(e)}", "red")
        
        input("\n按回车键继续...")

def handle_diff():
    """
    处理git diff命令
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("查看差异", "cyan")
        print("="*40)
        print("1. 查看工作区和暂存区的差异")
        print("2. 查看暂存区和最新提交的差异")
        print("3. 查看指定文件的差异")
        print("4. 查看指定提交的差异")
        print("5. 查看分支之间的差异")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-5): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git(['diff'])
        elif choice == "2":
            execute_git(['diff', '--cached'])
        elif choice == "3":
            file_name = input("请输入要查看的文件名: ")
            execute_git(['diff', file_name])
        elif choice == "4":
            commit = input("请输入提交ID (可以是部分ID或HEAD~n): ")
            execute_git(['diff', commit])
        elif choice == "5":
            branch1 = input("请输入第一个分支名: ")
            branch2 = input("请输入第二个分支名: ")
            execute_git(['diff', branch1, branch2])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        # 操作完成后暂停
        input("\n按回车键继续...")

def handle_logs():
    """
    处理日志查看功能
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("查看日志", "cyan")
        print("="*40)
        print("1. 查看操作日志")
        print("2. 清理日志文件")
        print("3. 设置日志级别")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            log_file = os.path.expanduser('~/.ezgit/ezgit.log')
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print_colored("暂无日志记录", "yellow")
        elif choice == "2":
            if confirm_action("确定要清理日志文件吗？"):
                try:
                    log_file = os.path.expanduser('~/.ezgit/ezgit.log')
                    if os.path.exists(log_file):
                        os.remove(log_file)
                        print_colored("日志文件已清理", "green")
                    else:
                        print_colored("没有找到日志文件", "yellow")
                except Exception as e:
                    print_colored(f"清理失败: {str(e)}", "red")
        elif choice == "3":
            print("\n日志级别:")
            print("1. DEBUG")
            print("2. INFO")
            print("3. WARNING")
            print("4. ERROR")
            level = input("\n请选择日志级别 (1-4): ")
            levels = {
                "1": "DEBUG",
                "2": "INFO",
                "3": "WARNING",
                "4": "ERROR"
            }
            if level in levels:
                config = load_config()
                config['log_level'] = levels[level]
                save_config(config)
                print_colored(f"日志级别已设置为: {levels[level]}", "green")
            else:
                print_colored("无效的选择", "yellow")
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_submodule():
    """
    处理子模块管理功能
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("子模块管理", "cyan")
        print("="*40)
        print("1. 添加子模块")
        print("2. 更新子模块")
        print("3. 删除子模块")
        print("4. 列出子模块")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-4): ")
        
        if choice == "0":
            return
        elif choice == "1":
            url = input("请输入子模块仓库地址: ")
            path = input("请输入子模块路径: ")
            execute_git(['submodule', 'add', url, path])
        elif choice == "2":
            execute_git(['submodule', 'update', '--init', '--recursive'])
        elif choice == "3":
            path = input("请输入要删除的子模块路径: ")
            if confirm_action(f"确定要删除子模块 {path} 吗？"):
                execute_git(['submodule', 'deinit', '-f', path])
                execute_git(['rm', '-f', path])
                shutil.rmtree(os.path.join('.git', 'modules', path), ignore_errors=True)
        elif choice == "4":
            execute_git(['submodule', 'status'])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_workflow():
    """
    处理工作流管理功能
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("工作流管理", "cyan")
        print("="*40)
        print("1. 创建功能分支")
        print("2. 完成功能开发")
        print("3. 创建发布分支")
        print("4. 完成发布")
        print("5. 创建修复分支")
        print("6. 完成修复")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-6): ")
        
        if choice == "0":
            return
        elif choice == "1":
            name = input("请输入功能名称: ")
            execute_git(['checkout', '-b', f'feature/{name}', 'develop'])
        elif choice == "2":
            branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
            if branch.startswith('feature/'):
                execute_git(['checkout', 'develop'])
                execute_git(['merge', '--no-ff', branch])
                if confirm_action("是否删除功能分支？"):
                    execute_git(['branch', '-d', branch])
            else:
                print_colored("当前不在功能分支上", "yellow")
        elif choice == "3":
            version = input("请输入版本号: ")
            execute_git(['checkout', '-b', f'release/{version}', 'develop'])
        elif choice == "4":
            branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
            if branch.startswith('release/'):
                execute_git(['checkout', 'main'])
                execute_git(['merge', '--no-ff', branch])
                execute_git(['tag', '-a', branch.split('/')[-1], '-m', f'Release {branch.split("/")[-1]}'])
                execute_git(['checkout', 'develop'])
                execute_git(['merge', '--no-ff', branch])
                if confirm_action("是否删除发布分支？"):
                    execute_git(['branch', '-d', branch])
            else:
                print_colored("当前不在发布分支上", "yellow")
        elif choice == "5":
            name = input("请输入修复名称: ")
            execute_git(['checkout', '-b', f'hotfix/{name}', 'main'])
        elif choice == "6":
            branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
            if branch.startswith('hotfix/'):
                execute_git(['checkout', 'main'])
                execute_git(['merge', '--no-ff', branch])
                version = input("请输入修复版本号: ")
                execute_git(['tag', '-a', version, '-m', f'Hotfix {version}'])
                execute_git(['checkout', 'develop'])
                execute_git(['merge', '--no-ff', branch])
                if confirm_action("是否删除修复分支？"):
                    execute_git(['branch', '-d', branch])
            else:
                print_colored("当前不在修复分支上", "yellow")
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_clean():
    """
    处理清理操作
    @return: None
    """
    print("\n即将清理的文件:")
    execute_git(['clean', '-n', '-d'])  # 先显示要清理的文件
    
    if input("\n确认清理这些文件？(y/N): ").lower() == 'y':
        execute_git(['clean', '-f', '-d'])

def handle_checkout():
    """
    处理分支切换操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("切换分支", "cyan")
        print("="*40)
        print("1. 切换到已有分支")
        print("2. 创建并切换到新分支")
        print("3. 切换到指定提交")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            branch = input("请输入要切换到的分支名: ")
            execute_git(['checkout', branch])
        elif choice == "2":
            branch = input("请输入新分支名: ")
            execute_git(['checkout', '-b', branch])
        elif choice == "3":
            commit = input("请输入提交ID: ")
            execute_git(['checkout', commit])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_merge():
    """
    处理合并操作
    @return: None
    """
    # 显示可用分支
    execute_git(['branch', '-av'])
    
    branch = input("\n请输入要合并的分支名: ")
    if branch:
        if input("是否压缩提交？(y/N): ").lower() == 'y':
            if execute_git(['merge', '--squash', branch]):
                print_colored(f"\n✓ 已压缩合并分支 {branch}", "green")
                print("\n请记得提交更改!")
        else:
            if execute_git(['merge', branch]):
                print_colored(f"\n✓ 已合并分支 {branch}", "green")
                # 显示合并后的提交信息
                execute_git(['log', '-1', '--stat'])
        input("\n按回车键继续...")

def handle_rebase():
    """
    处理变基操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("变基操作", "cyan")
        print("="*40)
        print("1. 变基到指定分支")
        print("2. 交互式变基")
        print("3. 中止变基")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            branch = input("请输入目标分支名: ")
            execute_git(['rebase', branch])
        elif choice == "2":
            commit = input("请输入起始提交 (HEAD~n): ")
            execute_git(['rebase', '-i', commit])
        elif choice == "3":
            execute_git(['rebase', '--abort'])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_init():
    """
    处理仓库初始化
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("初始化仓库", "cyan")
        print("="*40)
        print("1. 在当前目录初始化")
        print("2. 在新目录初始化")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-2): ")
        
        if choice == "0":
            return
        elif choice == "1":
            if confirm_action("确定要在当前目录初始化 Git 仓库吗？"):
                execute_git(['init'])
        elif choice == "2":
            dir_name = input("请输入目录名: ")
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
                os.chdir(dir_name)
                execute_git(['init'])
                print_colored(f"\n已在 {dir_name} 目录初始化 Git 仓库", "green")
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def get_commit_by_index(commits, index):
    """
    根据序号获取提交ID
    @param commits: list 提交列表
    @param index: str 序号或提交ID
    @return: str 提交ID或None
    """
    try:
        # 尝试作为序号处理
        idx = int(index) - 1
        if 0 <= idx < len(commits):
            return commits[idx].split()[0]  # 返回提交ID
    except ValueError:
        # 如果不是数字，作为提交ID处理
        if any(index in commit for commit in commits):
            return index
    return None

def handle_revert():
    """
    处理还原操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("还原操作", "cyan")
        print("="*40)
        print("1. 还原指定提交")
        print("2. 还原最近的提交")
        print("3. 还原合并提交")
        print("\n说明: 还原操作会创建新的提交来撤销之前的更改")
        print("     不同于 reset，revert 是安全的操作")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        
        # 检查工作区状态
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, 
                              text=True,
                              encoding='utf-8')
        if result.stdout.strip():
            print_colored("\n⚠ 工作区有未提交的更改", "yellow")
            print("请先提交或储藏(stash)这些更改")
            print("\n可选操作:")
            print("1. 提交更改")
            print("2. 储藏更改")
            print("3. 放弃操作")
            
            op = input("\n请选择 (1-3): ")
            if op == "1":
                message = input("请输入提交信息: ")
                if not execute_git(['commit', '-am', message]):
                    print_colored("\n✗ 提交失败，请手动处理更改", "red")
                    input("\n按回车键继续...")
                    continue
            elif op == "2":
                if not execute_git(['stash', 'save']):
                    print_colored("\n✗ 储藏失败，请手动处理更改", "red")
                    input("\n按回车键继续...")
                    continue
            else:
                continue
        
        if choice == "1":
            while True:
                # 获取并显示提交历史
                result = subprocess.run(['git', 'log', '--oneline', '-n', '10'], 
                                     capture_output=True, 
                                     text=True,
                                     encoding='utf-8')
                if result.stdout:
                    commits = result.stdout.strip().split('\n')
                    print("\n最近的提交记录:")
                    for i, commit in enumerate(commits, 1):
                        print(f"{i}. {commit}")
                    
                    print("\n0. 返回上级菜单")
                    index = input("\n请输入序号或提交ID: ")
                    
                    if index == "0":
                        break
                    
                    commit_id = get_commit_by_index(commits, index)
                    
                    if commit_id:
                        if execute_git(['revert', commit_id]):
                            print_colored(f"\n✓ 已还原提交 {commit_id}", "green")
                            # 显示还原后的状态
                            execute_git(['log', '-1', '--stat'])
                            input("\n按回车键继续...")
                            break
                    else:
                        print_colored("\n无效的序号或提交ID", "yellow")
                        continue
        elif choice == "2":
            if execute_git(['revert', 'HEAD']):
                print_colored("\n✓ 已还原最近的提交", "green")
                # 显示还原后的状态
                execute_git(['log', '-1', '--stat'])
            else:
                print_colored("\n✗ 还原失败", "red")
        elif choice == "3":
            while True:
                # 获取并显示合并提交
                result = subprocess.run(['git', 'log', '--merges', '--oneline', '-n', '5'],
                                     capture_output=True,
                                     text=True,
                                     encoding='utf-8')
                if result.stdout:
                    commits = result.stdout.strip().split('\n')
                    print("\n最近的合并提交:")
                    for i, commit in enumerate(commits, 1):
                        print(f"{i}. {commit}")
                    
                    print("\n0. 返回上级菜单")
                    index = input("\n请输入序号或提交ID: ")
                    
                    if index == "0":
                        break
                    
                    commit_id = get_commit_by_index(commits, index)
                    
                    if commit_id:
                        parent = input("请输入要保留的父提交编号(1 或 2): ")
                        if execute_git(['revert', '-m', parent, commit_id]):
                            print_colored(f"\n✓ 已还原合并提交 {commit_id}", "green")
                            # 显示还原后的状态
                            execute_git(['log', '-1', '--stat'])
                            input("\n按回车键继续...")
                            break
                    else:
                        print_colored("\n无效的序号或提交ID", "yellow")
                        continue
        else:
            print_colored("无效的选择", "yellow")
            continue
        
        if choice in ["1", "2", "3"]:
            input("\n按回车键继续...")

def handle_stats():
    """
    处理 Git 仓库统计分析
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("仓库统计分析", "cyan")
        print("="*40)
        print("1. 提交统计")
        print("2. 贡献者统计") 
        print("3. 文件变更统计")
        print("4. 代码行数统计")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-4): ")

        if choice == "0":
            return
        elif choice == "1":
            # 提交统计
            print("\n提交统计:")
            execute_git(['shortlog', '-sn', '--all'])
            print("\n每月提交数:")
            execute_git(['log', '--format="%ad"', '--date=format:%Y-%m', '--all', '|', 'sort', '|', 'uniq', '-c'])
        elif choice == "2":
            # 贡献者统计
            print("\n贡献者列表:")
            execute_git(['shortlog', '-sne', '--all'])
            print("\n活跃时间段:")
            execute_git(['log', '--format="%ad"', '--date=format:%H', '--all', '|', 'sort', '|', 'uniq', '-c'])
        elif choice == "3":
            # 文件变更统计
            print("\n文件变更排名:")
            execute_git(['log', '--pretty=format:', '--name-only', '|', 'sort', '|', 'uniq', '-c', '|', 'sort', '-rg', '|', 'head', '-10'])
        elif choice == "4":
            # 代码行数统计
            print("\n代码行数统计:")
            result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, encoding='utf-8')
            if result.stdout:
                files = result.stdout.strip().split('\n')
                total_lines = 0
                for file in files:
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            lines = len(f.readlines())
                            print(f"{file}: {lines} 行")
                            total_lines += lines
                    except:
                        continue
                print(f"\n总计: {total_lines} 行")
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_search():
    """
    处理 Git 仓库搜索功能
    @return: None 
    """
    while True:
        print("\n" + "="*40)
        print_colored("仓库搜索", "cyan")
        print("="*40)
        print("1. 搜索提交信息")
        print("2. 搜索提交内容")
        print("3. 搜索文件")
        print("4. 搜索作者提交")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-4): ")

        if choice == "0":
            return
        elif choice == "1":
            keyword = input("\n请输入搜索关键词: ")
            execute_git(['log', '--all', '--grep', keyword])
        elif choice == "2":
            keyword = input("\n请输入搜索关键词: ")
            execute_git(['log', '-p', '--all', '-S', keyword])
        elif choice == "3":
            pattern = input("\n请输入文件名模式(如 *.py): ")
            execute_git(['ls-files', '*' + pattern])
        elif choice == "4":
            author = input("\n请输入作者邮箱或名称: ")
            execute_git(['log', '--author', author])
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_compare():
    """
    处理 Git 比较功能
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("版本比较", "cyan")
        print("="*40)
        print("1. 比较两个分支")
        print("2. 比较两个提交")
        print("3. 比较工作区与暂存区")
        print("4. 比较暂存区与最新提交")
        print("5. 查看文件历史变更")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-5): ")

        if choice == "0":
            return
        elif choice == "1":
            branch1 = input("\n请输入第一个分支名: ")
            branch2 = input("请输入第二个分支名: ")
            print("\n1. 查看文件差异")
            print("2. 只看改动统计")
            print("3. 查看提交差异")
            sub_choice = input("\n请选择比较方式 (1-3): ")
            if sub_choice == "1":
                execute_git(['diff', branch1, branch2])
            elif sub_choice == "2":
                execute_git(['diff', '--stat', branch1, branch2])
            elif sub_choice == "3":
                execute_git(['log', f'{branch1}..{branch2}', '--oneline'])
        elif choice == "2":
            commit1 = input("\n请输入第一个提交ID: ")
            commit2 = input("请输入第二个提交ID: ")
            execute_git(['diff', commit1, commit2])
        elif choice == "3":
            file = input("\n请输入文件路径(回车比较所有): ")
            if file:
                execute_git(['diff', file])
            else:
                execute_git(['diff'])
        elif choice == "4":
            file = input("\n请输入文件路径(回车比较所有): ")
            if file:
                execute_git(['diff', '--cached', file])
            else:
                execute_git(['diff', '--cached'])
        elif choice == "5":
            file = input("\n请输入文件路径: ")
            execute_git(['log', '-p', file])
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_alias():
    """
    处理 Git 别名管理
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("别名管理", "cyan")
        print("="*40)
        print("1. 查看所有别名")
        print("2. 添加别名")
        print("3. 删除别名")
        print("4. 常用别名推荐")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-4): ")

        if choice == "0":
            return
        elif choice == "1":
            execute_git(['config', '--global', '--get-regexp', '^alias\.'])
        elif choice == "2":
            alias = input("\n请输入别名(不含 alias.): ")
            command = input("请输入对应的Git命令: ")
            execute_git(['config', '--global', f'alias.{alias}', command])
            print_colored(f"\n已添加别名: git {alias} => git {command}", "green")
        elif choice == "3":
            alias = input("\n请输入要删除的别名(不含 alias.): ")
            execute_git(['config', '--global', '--unset', f'alias.{alias}'])
            print_colored(f"\n已删除别名: {alias}", "green")
        elif choice == "4":
            print("\n推荐的常用别名:")
            aliases = {
                'st': 'status',
                'co': 'checkout',
                'br': 'branch',
                'ci': 'commit',
                'unstage': 'reset HEAD --',
                'last': 'log -1 HEAD',
                'lg': 'log --color --graph --pretty=format:"%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset" --abbrev-commit'
            }
            for alias, cmd in aliases.items():
                print(f"git {alias} => git {cmd}")
                if input("\n是否添加此别名？(y/N): ").lower() == 'y':
                    execute_git(['config', '--global', f'alias.{alias}', cmd])
                    print_colored("已添加", "green")
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_version():
    """
    处理版本管理相关操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("版本管理", "cyan")
        print("="*40)
        print("1. 重置操作    (git reset)")
        print("2. 还原操作    (git revert)")
        print("3. 恢复操作    (git restore)")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-3): ")

        if choice == "0":
            return
        elif choice == "1":
            handle_reset()
        elif choice == "2":
            handle_revert()
        elif choice == "3":
            handle_recovery()
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_maintenance():
    """
    处理仓库维护相关操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("仓库维护", "cyan")
        print("="*40)
        print("1. 清理未跟踪文件    (git clean)")
        print("2. 压缩仓库          (git gc)")
        print("3. 文件系统检查      (git fsck)")
        print("4. 引用完整性检查    (git prune)")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-4): ")

        if choice == "0":
            return
        elif choice == "1":
            handle_clean()
        elif choice == "2":
            execute_git(['gc', '--aggressive', '--prune=now'])
        elif choice == "3":
            execute_git(['fsck'])
        elif choice == "4":
            execute_git(['prune', '-v'])
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_analysis():
    """
    处理分析工具相关操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("分析工具", "cyan")
        print("="*40)
        print("1. 统计分析    (git stats)")
        print("2. 仓库搜索    (git search)")
        print("3. 版本比较    (git diff)")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-3): ")

        if choice == "0":
            return
        elif choice == "1":
            handle_stats()
        elif choice == "2":
            handle_search()
        elif choice == "3":
            handle_compare()
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_settings_menu():
    """
    处理配置管理相关操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("配置管理", "cyan")
        print("="*40)
        print("1. Git配置     (git config)")
        print("2. 别名管理    (git alias)")
        print("3. 工具设置")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-3): ")

        if choice == "0":
            return
        elif choice == "1":
            handle_config()
        elif choice == "2":
            handle_alias()
        elif choice == "3":
            handle_settings()
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def handle_reset():
    """
    处理重置操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("重置操作", "cyan")
        print("="*40)
        print("1. 软重置 (保留工作区和暂存区)")
        print("2. 混合重置 (保留工作区，清空暂存区)")
        print("3. 硬重置 (完全重置到指定版本)")
        print("\n0. 返回主菜单")

        choice = input("\n请选择 (0-3): ")

        if choice == "0":
            return
        elif choice in ["1", "2", "3"]:
            print("\n当前分支的提交历史:")
            execute_git(['log', '--oneline', '-10'])
            
            commit = input("\n请输入要重置到的提交ID (输入 HEAD^ 回退一个版本): ")
            if not commit:
                continue
                
            if choice == "1":
                if confirm_action("确定要执行软重置吗？这将保留工作区和暂存区的修改"):
                    execute_git(['reset', '--soft', commit])
            elif choice == "2":
                if confirm_action("确定要执行混合重置吗？这将清空暂存区但保留工作区的修改"):
                    execute_git(['reset', '--mixed', commit])
            elif choice == "3":
                if confirm_action("警告：硬重置将丢失所有未提交的修改！确定要继续吗？"):
                    execute_git(['reset', '--hard', commit])
        else:
            print_colored("无效的选择", "yellow")
            continue

        input("\n按回车键继续...")

def main():
    """
    主函数
    @return: None
    """
    try:
        while True:
            show_menu()
            choice = input("\n请输入选项: ").lower()
            
            if choice == '0':
                print_colored("\n感谢使用，再见！", "green")
                break
            
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # 处理选项
            if choice == "1":
                handle_status()
            elif choice == "2":
                handle_add()
            elif choice == "3":
                handle_commit()
            elif choice == "4":
                handle_log()
            elif choice == "5":
                handle_push()
            elif choice == "6":
                handle_pull()
            elif choice == "7":
                handle_branch()
            elif choice == "8":
                handle_checkout()
            elif choice == "9":
                handle_merge()
            elif choice == "10":
                handle_rebase()
            elif choice == "11":
                handle_remote()
            elif choice == "12":
                handle_tag()
            elif choice == "13":
                handle_stash()
            elif choice == "14":
                handle_version()
            elif choice == "15":
                handle_maintenance()
            elif choice == "16":
                handle_analysis()
            elif choice == "17":
                handle_settings_menu()
            elif choice == "h":
                show_help()
            elif choice == "s":
                handle_stats()
            elif choice == "t":
                handle_search()
            elif choice == "c":
                handle_compare()
            elif choice == "a":
                handle_alias()
            else:
                print_colored("无效的选择", "yellow")
                continue
            
            # 只在需要时显示继续提示
            if choice not in ['0', 'h', 's', 't', 'c', 'a', '16', '17', '18', '19', '20'] and not choice.isdigit():
                input("\n按回车键继续...")
            
            os.system('cls' if os.name == 'nt' else 'clear')
            
    except KeyboardInterrupt:
        print_colored("\n\n正在退出...", "yellow")
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n错误: {str(e)}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main() 