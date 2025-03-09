#!/usr/bin/env python3
import os
import sys
import json
import logging
import subprocess
import shutil
import argparse

def execute_git_command(command):
    """
    执行git命令的通用函数
    - 使用subprocess.run执行git命令
    - 处理命令输出和错误
    - 特殊处理首次推送分支的情况
    """
    try:
        # 添加环境变量设置来强制使用 UTF-8 编码
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['LANG'] = 'en_US.UTF-8'
        
        # 添加 encoding 参数并使用环境变量
        result = subprocess.run(['git'] + command, 
                             capture_output=True, 
                             text=True,
                             encoding='utf-8',
                             errors='replace',
                             env=env)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            # 检查是否是首次推送的错误
            if "no upstream branch" in result.stderr:
                print("首次推送分支，正在设置上游分支...")
                current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                             capture_output=True, 
                                             text=True,
                                             encoding='utf-8',
                                             errors='replace',
                                             env=env).stdout.strip()
                # 使用 --set-upstream 选项设置上游分支
                push_result = subprocess.run(['git', 'push', '--set-upstream', 'origin', current_branch],
                                          capture_output=True,
                                          text=True,
                                          encoding='utf-8',
                                          errors='replace',
                                          env=env)
                if push_result.stdout:
                    print(push_result.stdout)
                if push_result.stderr:
                    print(push_result.stderr)
            else:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"执行出错: {str(e)}")
        return False

def print_colored(text, color):
    """
    打印带颜色的文本
    @param text: str 要打印的文本
    @param color: str 颜色代码
    @return: None
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def show_menu():
    """
    显示优化后的主菜单选项
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

    # 加载菜单配置
    menu_config = load_custom_menu()
    menu_mode = menu_config['mode']

    if menu_mode == 'simple':
        # 显示简单菜单
        print_colored("\n[常用操作]", "yellow")
        simple_menu = [
            ("1", "查看状态", "git status"),
            ("2", "暂存更改", "git add"),
            ("3", "提交更改", "git commit"),
            ("4", "推送更改", "git push"),
            ("5", "拉取更新", "git pull")
        ]
        for num, name, cmd in simple_menu:
            print(f"{num}. {name.ljust(12)} {cmd}")
    elif menu_mode == 'custom':
        # 显示自定义菜单
        custom_menu = menu_config['custom_menu']
        for category, items in custom_menu.items():
            print_colored(f"\n[{category}]", "yellow")
            for num, name, cmd in items:
                print(f"{num}. {name.ljust(12)} {cmd}")
    else:
        # 显示完整菜单
        menu_items = {
            "常用操作": [
                ("1", "查看仓库状态", "git status"),
                ("2", "暂存更改", "git add"),
                ("3", "提交更改", "git commit"),
                ("4", "查看历史", "git log")
            ],
            "远程操作": [
                ("5", "推送更改", "git push"),
                ("6", "拉取更新", "git pull"),
                ("7", "克隆仓库", "git clone"),
                ("8", "远程配置", "git remote")
            ],
            "分支管理": [
                ("9", "分支操作", "git branch"),
                ("10", "切换分支", "git checkout"),
                ("11", "合并分支", "git merge")
            ],
            "高级功能": [
                ("12", "配置信息", "git config"),
                ("13", "标签管理", "git tag"),
                ("14", "储藏管理", "git stash"),
                ("15", "高级操作", "advanced"),
                ("16", "错误恢复", "recovery")
            ],
            "工具设置": [
                ("17", "配置工具", "settings"),
                ("18", "查看日志", "logs"),
                ("19", "检查更新", "update")
            ]
        }
        for category, items in menu_items.items():
            print_colored(f"\n[{category}]", "yellow")
            for num, name, cmd in items:
                print(f"{num}. {name.ljust(12)} {cmd}")

    print_colored("\n[其他选项]", "yellow")
    print(" m. 切换菜单模式")
    print(" c. 自定义菜单")
    print(" h. 显示帮助")
    print(" 0. 退出程序")
    print("\n" + "="*50)
    print_colored("提示：输入命令编号执行操作，输入 'm' 切换菜单模式", "green")

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
    @return: bool 是否返回主菜单
    """
    while True:
        print("\n" + "="*40)
        print_colored("文件暂存管理", "cyan")
        print("="*40)
        print("1. 暂存所有更改 (git add .)")
        print("2. 暂存指定文件")
        print("3. 交互式暂存")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return True
        elif choice == "1":
            if confirm_action("即将暂存所有更改"):
                execute_git_command(['add', '.'])
        elif choice == "2":
            file_name = input("请输入要暂存的文件名(支持通配符): ")
            execute_git_command(['add', file_name])
        elif choice == "3":
            execute_git_command(['add', '-i'])
        else:
            print_colored("无效的选择，请重试", "yellow")
        
        # 操作完成后暂停
        input("\n按回车键继续...")

def handle_commit():
    """
    处理git commit命令
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("提交更改", "cyan")
        print("="*40)
        print("1. 正常提交")
        print("2. 跳过检查提交 (--no-verify)")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-2): ")
        
        if choice == "0":
            return
            
        if choice == "1":
            commit_message = input("\n请输入提交信息: ")
            result = execute_git_command(['commit', '-m', commit_message])
        elif choice == "2":
            commit_message = input("\n请输入提交信息: ")
            result = execute_git_command(['commit', '-m', commit_message, '--no-verify'])
        else:
            print_colored("无效的选择", "yellow")
            continue
            
        if result:
            print_colored("提交成功！", "green")
        else:
            print("\n提交失败！请选择：")
            print("1. 使用 --no-verify 重试")
            print("2. 重新输入信息")
            print("0. 返回上级菜单")
            retry = input("请选择 (0-2): ")
            
            if retry == "1":
                if execute_git_command(['commit', '-m', commit_message, '--no-verify']):
                    print_colored("提交成功！", "green")
            elif retry == "2":
                continue
            elif retry == "0":
                return
                
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
        
        print("\n1. 查看所有分支")
        print("2. 创建新分支")
        print("3. 删除分支")
        print("4. 重命名分支")
        print("5. 查看分支详情")
        print("6. 设置上游分支")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-6): ")
        
        if choice == "0":
            return
        elif choice == "1":
            print("\n分支列表:")
            execute_git_command(['branch', '-av'])
        elif choice == "2":
            name = input("\n请输入新分支名称: ")
            if confirm_action(f"是否切换到新分支 {name}？"):
                execute_git_command(['checkout', '-b', name])
            else:
                execute_git_command(['branch', name])
        elif choice == "3":
            name = input("\n请输入要删除的分支名: ")
            if confirm_action(f"确定要删除分支 {name} 吗？"):
                try:
                    execute_git_command(['branch', '-d', name])
                except:
                    if confirm_action("分支可能未完全合并，是否强制删除？"):
                        execute_git_command(['branch', '-D', name])
        elif choice == "4":
            old_name = input("\n请输入当前分支名: ")
            new_name = input("请输入新分支名: ")
            execute_git_command(['branch', '-m', old_name, new_name])
        elif choice == "5":
            name = input("\n请输入分支名(回车查看当前分支): ") or 'HEAD'
            execute_git_command(['show-branch', name])
        elif choice == "6":
            local = input("\n请输入本地分支名: ")
            remote = input("请输入远程分支名: ")
            execute_git_command(['branch', '-u', f'origin/{remote}', local])
        else:
            print_colored("\n无效的选择，请重试", "yellow")
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
                execute_git_command(['clone', url, '.'])
            else:
                path = input("请输入目标目录: ")
                execute_git_command(['clone', url, path])
        elif choice == "2":
            url = input("\n请输入仓库地址: ")
            branch = input("请输入分支名: ")
            execute_git_command(['clone', '-b', branch, url])
        elif choice == "3":
            url = input("\n请输入仓库地址: ")
            tag = input("请输入标签名: ")
            execute_git_command(['clone', '-b', tag, url])
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_config():
    """
    Git配置管理
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("Git 配置管理", "cyan")
        print("="*40)
        
        print("\n1. 查看当前配置")
        print("2. 设置用户名和邮箱")
        print("3. 设置默认编辑器")
        print("4. 设置默认分支名")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-4): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git_command(['config', '--list'])
        elif choice == "2":
            username = input("\n请输入Git用户名: ")
            email = input("请输入Git邮箱: ")
            execute_git_command(['config', '--global', 'user.name', username])
            execute_git_command(['config', '--global', 'user.email', email])
            print_colored("\nGit用户信息配置完成！", "green")
        elif choice == "3":
            editor = input("\n请输入编辑器命令(如 vim, nano): ")
            execute_git_command(['config', '--global', 'core.editor', editor])
            print_colored("\n默认编辑器设置完成！", "green")
        elif choice == "4":
            branch = input("\n请输入默认分支名(如 main, master): ")
            execute_git_command(['config', '--global', 'init.defaultBranch', branch])
            print_colored("\n默认分支名设置完成！", "green")
        else:
            print_colored("\n无效的选择，请重试", "yellow")
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
                execute_git_command(['remote', '-v'])
            else:
                print_colored("\n当前仓库没有配置任何远程仓库", "yellow")
                print("提示: 使用选项 2 添加远程仓库")
        elif choice == "2":
            remote_name = input("\n请输入远程仓库名称(默认 origin): ") or "origin"
            remote_url = input("请输入远程仓库URL: ")
            execute_git_command(['remote', 'add', remote_name, remote_url])
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
            execute_git_command(['remote', '-v'])
            remote_name = input("\n请输入要修改的远程仓库名称: ")
            remote_url = input("请输入新的远程仓库URL: ")
            execute_git_command(['remote', 'set-url', remote_name, remote_url])
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
            execute_git_command(['remote', '-v'])
            remote_name = input("\n请输入要删除的远程仓库名称: ")
            if confirm_action(f"确定要删除远程仓库 {remote_name} 吗？"):
                execute_git_command(['remote', 'remove', remote_name])
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
            execute_git_command(['remote', '-v'])
            old_name = input("\n请输入要重命名的远程仓库名称: ")
            new_name = input("请输入新的远程仓库名称: ")
            execute_git_command(['remote', 'rename', old_name, new_name])
            print_colored(f"\n成功将远程仓库 {old_name} 重命名为 {new_name}", "green")
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_push():
    """
    处理git push命令
    @return: None
    """
    try:
        # 先检查是否有远程仓库配置
        result = subprocess.run(['git', 'remote'], 
                             capture_output=True, 
                             text=True,
                             encoding='utf-8')
        if not result.stdout.strip():
            print_colored("\n错误: 未配置远程仓库", "red")
            print("提示: 请先使用 'git remote add' 添加远程仓库")
            return

        # 检查是否有未提交的更改
        status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                    capture_output=True, text=True)
        
        if status_result.stdout.strip():
            print("\n检测到未提交的更改！请选择处理方式：")
            print("1. 暂存并提交更改")
            print("2. 暂存并提交更改 (跳过检查)")
            print("3. 暂时储藏更改(stash)")
            print("4. 取消操作")
            
            choice = input("请选择 (1-4): ")
            
            if choice == "1":
                execute_git_command(['add', '.'])
                commit_msg = input("请输入提交信息: ")
                if not execute_git_command(['commit', '-m', commit_msg]):
                    print("\n正常提交失败，是否尝试跳过检查提交？(y/n): ")
                    if input().lower() == 'y':
                        execute_git_command(['commit', '-m', commit_msg, '--no-verify'])
                    else:
                        return
            elif choice == "2":
                execute_git_command(['add', '.'])
                commit_msg = input("请输入提交信息: ")
                execute_git_command(['commit', '-m', commit_msg, '--no-verify'])
            elif choice == "3":
                print("储藏当前更改...")
                execute_git_command(['stash'])
            elif choice == "4":
                print("操作已取消")
                return
            else:
                print("无效的选择")
                return

        # 获取当前分支名
        current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                     capture_output=True, text=True).stdout.strip()
        print(f"\n正在推送分支 '{current_branch}' 到远程仓库...")
        
        # 尝试推送
        push_result = subprocess.run(['git', 'push', 'origin', current_branch],
                                  capture_output=True,
                                  text=True,
                                  encoding='utf-8')
        
        if push_result.returncode != 0:
            error_msg = push_result.stderr.lower()
            if "no upstream branch" in error_msg:
                print_colored("\n首次推送分支，需要设置上游分支...", "yellow")
                if confirm_action(f"是否将本地分支 '{current_branch}' 推送并设置为远程分支？"):
                    execute_git_command(['push', '--set-upstream', 'origin', current_branch])
            elif "repository not found" in error_msg:
                print_colored("\n错误: 远程仓库不存在", "red")
                print("可能的原因:")
                print("1. 远程仓库URL配置错误")
                print("2. 没有访问权限")
                print("3. 仓库已被删除")
                print("\n建议:")
                print("- 检查远程仓库URL: git remote -v")
                print("- 确认是否有访问权限")
                print("- 联系仓库管理员")
            elif "permission denied" in error_msg:
                print_colored("\n错误: 没有推送权限", "red")
                print("可能的原因:")
                print("1. SSH密钥未配置")
                print("2. 没有仓库的写入权限")
                print("\n建议:")
                print("- 检查SSH密钥配置")
                print("- 确认仓库访问权限")
            elif "non-fast-forward" in error_msg:
                print_colored("\n错误: 远程分支有新的提交", "red")
                print("建议:")
                print("1. 先拉取远程更新: git pull")
                print("2. 解决冲突后重新推送")
                if confirm_action("是否立即拉取远程更新？"):
                    execute_git_command(['pull'])
            else:
                print_colored(f"\n推送失败: {push_result.stderr}", "red")
        else:
            print_colored("\n推送成功！", "green")
            
    except Exception as e:
        print_colored(f"\n推送过程出错: {str(e)}", "red")
        print("请检查网络连接和远程仓库配置")

def handle_pull():
    """
    处理git pull命令
    """
    try:
        # 首先检查是否有未提交的更改
        status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                    capture_output=True, text=True)
        
        if status_result.stdout.strip():
            print("\n检测到未提交的更改！请选择处理方式：")
            print("1. 暂存并提交更改")
            print("2. 暂时储藏更改(stash)")
            print("3. 放弃更改")
            print("4. 取消操作")
            
            choice = input("请选择 (1-4): ")
            
            if choice == "1":
                # 暂存并提交
                execute_git_command(['add', '.'])
                commit_msg = input("请输入提交信息: ")
                execute_git_command(['commit', '-m', commit_msg])
            elif choice == "2":
                # 储藏更改
                print("储藏当前更改...")
                execute_git_command(['stash'])
            elif choice == "3":
                # 放弃更改
                print("放弃所有本地更改...")
                execute_git_command(['reset', '--hard'])
            elif choice == "4":
                print("操作已取消")
                return
            else:
                print("无效的选择")
                return
        
        # 获取当前分支名
        current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                     capture_output=True, text=True).stdout.strip()
        print(f"正在拉取分支 '{current_branch}' 的更新...")
        
        # 设置跟踪信息
        print("设置分支跟踪信息...")
        subprocess.run(['git', 'branch', '--set-upstream-to', f'origin/{current_branch}', current_branch], 
                      capture_output=True, text=True)
        
        # 设置 pull 策略
        print("配置 pull 策略...")
        subprocess.run(['git', 'config', 'pull.rebase', 'true'], 
                      capture_output=True, text=True)
        
        # 拉取更新
        execute_git_command(['pull'])
        
        # 如果之前选择了储藏更改，现在恢复它们
        if choice == "2":
            print("恢复储藏的更改...")
            execute_git_command(['stash', 'pop'])
            print("如果有冲突，请手动解决后提交")
            
    except Exception as e:
        print(f"拉取失败: {str(e)}")

def get_commit_history():
    """
    获取提交历史并返回提交记录列表
    @return: list 提交记录列表，每个元素为 (commit_hash, commit_message) 的元组
    """
    try:
        result = subprocess.run(['git', 'log', '--oneline'],
                              capture_output=True,
                              text=True,
                              encoding='utf-8')
        if result.returncode == 0:
            commits = []
            for line in result.stdout.splitlines():
                if line.strip():
                    commit_hash = line.split()[0]
                    commit_message = ' '.join(line.split()[1:])
                    commits.append((commit_hash, commit_message))
            return commits
        return []
    except Exception as e:
        print(f"获取提交历史失败: {str(e)}")
        return []

def handle_log():
    """
    处理git log命令
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("历史记录", "cyan")
        print("="*40)
        
        print("\n1. 查看完整历史")
        print("2. 查看简洁历史")
        print("3. 查看图形化历史")
        print("4. 查看指定文件历史")
        print("5. 查看指定作者提交")
        print("6. 搜索提交信息")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-6): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git_command(['log'])
        elif choice == "2":
            execute_git_command(['log', '--oneline'])
        elif choice == "3":
            execute_git_command(['log', '--graph', '--oneline', '--all'])
        elif choice == "4":
            file = input("\n请输入文件名: ")
            execute_git_command(['log', '--follow', file])
        elif choice == "5":
            author = input("\n请输入作者名称: ")
            execute_git_command(['log', '--author', author])
        elif choice == "6":
            pattern = input("\n请输入搜索关键词: ")
            execute_git_command(['log', '--grep', pattern])
        else:
            print_colored("\n无效的选择，请重试", "yellow")
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
            execute_git_command(['tag', '-l', '-n1'])
        elif choice == "2":
            tag_name = input("\n请输入标签名称: ")
            message = input("请输入标签说明: ")
            execute_git_command(['tag', '-a', tag_name, '-m', message])
        elif choice == "3":
            tag_name = input("\n请输入要删除的标签名称: ")
            if confirm_action(f"确定要删除标签 {tag_name} 吗？"):
                execute_git_command(['tag', '-d', tag_name])
        elif choice == "4":
            tag_name = input("\n请输入要推送的标签名称(回车推送所有标签): ")
            if tag_name:
                execute_git_command(['push', 'origin', tag_name])
            else:
                execute_git_command(['push', 'origin', '--tags'])
        elif choice == "5":
            tag_name = input("\n请输入要检出的标签名称: ")
            execute_git_command(['checkout', tag_name])
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
            execute_git_command(['stash', 'list'])
        elif choice == "2":
            message = input("\n请输入储藏说明(可选): ")
            if message:
                execute_git_command(['stash', 'save', message])
            else:
                execute_git_command(['stash'])
        elif choice == "3":
            print("\n储藏列表:")
            execute_git_command(['stash', 'list'])
            stash_id = input("\n请输入储藏ID(如 stash@{0}): ")
            if confirm_action("是否保留储藏？"):
                execute_git_command(['stash', 'apply', stash_id])
            else:
                execute_git_command(['stash', 'pop', stash_id])
        elif choice == "4":
            print("\n储藏列表:")
            execute_git_command(['stash', 'list'])
            stash_id = input("\n请输入要删除的储藏ID: ")
            if confirm_action(f"确定要删除储藏 {stash_id} 吗？"):
                execute_git_command(['stash', 'drop', stash_id])
        elif choice == "5":
            print("\n储藏列表:")
            execute_git_command(['stash', 'list'])
            stash_id = input("\n请输入储藏ID: ")
            branch_name = input("请输入新分支名称: ")
            execute_git_command(['stash', 'branch', branch_name, stash_id])
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
            return execute_git_command(['init'])
    elif choice == "2":
        dir_name = input("请输入新目录名称: ")
        try:
            os.makedirs(dir_name, exist_ok=True)
            os.chdir(dir_name)
            if execute_git_command(['init']):
                print_colored(f"\n已在 {dir_name} 目录初始化Git仓库", "green")
                return True
        except Exception as e:
            print_colored(f"创建目录失败: {str(e)}", "red")
    return False

def handle_status():
    """
    处理git status命令
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("仓库状态", "cyan")
        print("="*40)
        
        print("\n1. 查看完整状态")
        print("2. 查看简短状态")
        print("3. 查看未跟踪文件")
        print("4. 查看已忽略文件")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-4): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git_command(['status'])
        elif choice == "2":
            execute_git_command(['status', '-s'])
        elif choice == "3":
            execute_git_command(['status', '--untracked-files=all'])
        elif choice == "4":
            execute_git_command(['status', '--ignored'])
        else:
            print_colored("\n无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def load_config():
    """
    加载配置文件
    @return: dict 配置信息
    """
    config_path = os.path.expanduser('~/.ezgit/config.json')
    default_config = {
        'theme': 'default',
        'language': 'zh_CN',
        'auto_push': False,
        'default_branch': 'main',
        'author': {
            'name': '',
            'email': ''
        }
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 创建配置目录和文件
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    except Exception as e:
        print_colored(f"加载配置文件失败: {str(e)}", "red")
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

def handle_recovery():
    """
    处理错误恢复
    @return: None
    """
    print_colored("\n=== 错误恢复 ===", "cyan")
    print("1. 撤销最后一次提交")
    print("2. 恢复删除的文件")
    print("3. 修复损坏的仓库")
    print("4. 查看操作历史")
    print("0. 返回主菜单")
    
    choice = input("\n请选择 (0-4): ")
    # ... 实现各种恢复功能 ...

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
    处理工具配置设置
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("工具配置设置", "cyan")
        print("="*40)
        print("1. 查看当前配置")
        print("2. 修改主题颜色")
        print("3. 设置默认分支")
        print("4. 设置自动推送")
        print("5. 设置作者信息")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-5): ")
        
        config = load_config()
        config_path = os.path.expanduser('~/.ezgit/config.json')
        
        if choice == "0":
            return
        elif choice == "1":
            print("\n当前配置:")
            print(f"主题: {config['theme']}")
            print(f"默认分支: {config['default_branch']}")
            print(f"自动推送: {'是' if config['auto_push'] else '否'}")
            print(f"作者名称: {config['author']['name']}")
            print(f"作者邮箱: {config['author']['email']}")
        elif choice == "2":
            print("\n可用主题:")
            print("1. default (默认)")
            print("2. dark (深色)")
            print("3. light (浅色)")
            theme = input("\n请选择主题 (1-3): ")
            themes = {
                "1": "default",
                "2": "dark",
                "3": "light"
            }
            if theme in themes:
                config['theme'] = themes[theme]
                print_colored("\n主题已更新！", "green")
        elif choice == "3":
            branch = input("\n请输入默认分支名称 (如 main 或 master): ")
            config['default_branch'] = branch
            print_colored("\n默认分支已更新！", "green")
        elif choice == "4":
            auto_push = input("\n是否启用自动推送？(y/n): ").lower() == 'y'
            config['auto_push'] = auto_push
            print_colored("\n自动推送设置已更新！", "green")
        elif choice == "5":
            name = input("\n请输入作者名称: ")
            email = input("请输入作者邮箱: ")
            if name:
                config['author']['name'] = name
            if email:
                config['author']['email'] = email
            print_colored("\n作者信息已更新！", "green")
        else:
            print_colored("无效的选择", "yellow")
            continue
            
        # 保存配置
        if choice in ["2", "3", "4", "5"]:
            try:
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
            except Exception as e:
                print_colored(f"\n保存配置失败: {str(e)}", "red")
        
        input("\n按回车键继续...")

def load_custom_menu():
    """
    加载用户自定义菜单配置
    @return: dict 自定义菜单配置
    """
    config_path = os.path.expanduser('~/.ezgit/menu_config.json')
    default_menu = {
        'mode': 'full',  # 'full' 或 'simple' 或 'custom'
        'custom_menu': {
            "常用操作": [
                ("1", "查看状态", "git status"),
                ("2", "暂存更改", "git add"),
                ("3", "提交更改", "git commit"),
                ("4", "推送更改", "git push"),
                ("5", "拉取更新", "git pull")
            ]
        }
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 确保配置文件包含所有必要字段
                if 'mode' not in config:
                    config['mode'] = default_menu['mode']
                if 'custom_menu' not in config:
                    config['custom_menu'] = default_menu['custom_menu']
                # 确保常用操作分类存在
                if '常用操作' not in config['custom_menu']:
                    config['custom_menu']['常用操作'] = default_menu['custom_menu']['常用操作']
                return config
        else:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_menu, f, indent=4)
            return default_menu
    except Exception as e:
        print_colored(f"加载菜单配置失败: {str(e)}", "red")
        return default_menu

def handle_menu_mode():
    """
    处理菜单模式切换
    @return: None
    """
    print_colored("\n=== 菜单模式设置 ===", "cyan")
    print("1. 完整模式 (显示所有功能)")
    print("2. 简单模式 (仅显示常用功能)")
    print("3. 自定义模式 (使用自定义菜单)")
    print("0. 返回主菜单")
    
    choice = input("\n请选择 (0-3): ")
    
    config_path = os.path.expanduser('~/.ezgit/menu_config.json')
    menu_config = load_custom_menu()
    
    if choice == "1":
        menu_config['mode'] = 'full'
    elif choice == "2":
        menu_config['mode'] = 'simple'
    elif choice == "3":
        menu_config['mode'] = 'custom'
    elif choice == "0":
        return
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(menu_config, f, indent=4)
        print_colored("\n菜单模式已更新！", "green")
    except Exception as e:
        print_colored(f"\n保存配置失败: {str(e)}", "red")

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
                    ("14", "储藏管理", "git stash")
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
            execute_git_command(['diff'])
        elif choice == "2":
            execute_git_command(['diff', '--cached'])
        elif choice == "3":
            file_name = input("请输入要查看的文件名: ")
            execute_git_command(['diff', file_name])
        elif choice == "4":
            commit = input("请输入提交ID (可以是部分ID或HEAD~n): ")
            execute_git_command(['diff', commit])
        elif choice == "5":
            branch1 = input("请输入第一个分支名: ")
            branch2 = input("请输入第二个分支名: ")
            execute_git_command(['diff', branch1, branch2])
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
            execute_git_command(['submodule', 'add', url, path])
        elif choice == "2":
            execute_git_command(['submodule', 'update', '--init', '--recursive'])
        elif choice == "3":
            path = input("请输入要删除的子模块路径: ")
            if confirm_action(f"确定要删除子模块 {path} 吗？"):
                execute_git_command(['submodule', 'deinit', '-f', path])
                execute_git_command(['rm', '-f', path])
                shutil.rmtree(os.path.join('.git', 'modules', path), ignore_errors=True)
        elif choice == "4":
            execute_git_command(['submodule', 'status'])
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
            execute_git_command(['checkout', '-b', f'feature/{name}', 'develop'])
        elif choice == "2":
            branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
            if branch.startswith('feature/'):
                execute_git_command(['checkout', 'develop'])
                execute_git_command(['merge', '--no-ff', branch])
                if confirm_action("是否删除功能分支？"):
                    execute_git_command(['branch', '-d', branch])
            else:
                print_colored("当前不在功能分支上", "yellow")
        elif choice == "3":
            version = input("请输入版本号: ")
            execute_git_command(['checkout', '-b', f'release/{version}', 'develop'])
        elif choice == "4":
            branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
            if branch.startswith('release/'):
                execute_git_command(['checkout', 'main'])
                execute_git_command(['merge', '--no-ff', branch])
                execute_git_command(['tag', '-a', branch.split('/')[-1], '-m', f'Release {branch.split("/")[-1]}'])
                execute_git_command(['checkout', 'develop'])
                execute_git_command(['merge', '--no-ff', branch])
                if confirm_action("是否删除发布分支？"):
                    execute_git_command(['branch', '-d', branch])
            else:
                print_colored("当前不在发布分支上", "yellow")
        elif choice == "5":
            name = input("请输入修复名称: ")
            execute_git_command(['checkout', '-b', f'hotfix/{name}', 'main'])
        elif choice == "6":
            branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
            if branch.startswith('hotfix/'):
                execute_git_command(['checkout', 'main'])
                execute_git_command(['merge', '--no-ff', branch])
                version = input("请输入修复版本号: ")
                execute_git_command(['tag', '-a', version, '-m', f'Hotfix {version}'])
                execute_git_command(['checkout', 'develop'])
                execute_git_command(['merge', '--no-ff', branch])
                if confirm_action("是否删除修复分支？"):
                    execute_git_command(['branch', '-d', branch])
            else:
                print_colored("当前不在修复分支上", "yellow")
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_clean():
    """
    处理仓库清理功能
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("清理仓库", "cyan")
        print("="*40)
        print("1. 清理未跟踪文件")
        print("2. 清理已忽略文件")
        print("3. 清理所有未跟踪文件")
        print("4. 预览清理效果")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-4): ")
        
        if choice == "0":
            return
        elif choice == "1":
            if confirm_action("确定要清理未跟踪的文件吗？"):
                execute_git_command(['clean', '-f'])
        elif choice == "2":
            if confirm_action("确定要清理已忽略的文件吗？"):
                execute_git_command(['clean', '-f', '-X'])
        elif choice == "3":
            if confirm_action("确定要清理所有未跟踪的文件和目录吗？"):
                execute_git_command(['clean', '-f', '-d'])
        elif choice == "4":
            print("\n预览清理效果:")
            execute_git_command(['clean', '-n', '-d'])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

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
            execute_git_command(['checkout', branch])
        elif choice == "2":
            branch = input("请输入新分支名: ")
            execute_git_command(['checkout', '-b', branch])
        elif choice == "3":
            commit = input("请输入提交ID: ")
            execute_git_command(['checkout', commit])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def handle_merge():
    """
    处理分支合并操作
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("合并分支", "cyan")
        print("="*40)
        print("1. 合并指定分支")
        print("2. 合并并压缩提交")
        print("3. 中止合并")
        print("\n0. 返回上级菜单")
        
        choice = input("\n请选择 (0-3): ")
        
        if choice == "0":
            return
        elif choice == "1":
            branch = input("请输入要合并的分支名: ")
            execute_git_command(['merge', branch])
        elif choice == "2":
            branch = input("请输入要合并的分支名: ")
            execute_git_command(['merge', '--squash', branch])
        elif choice == "3":
            execute_git_command(['merge', '--abort'])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
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
            execute_git_command(['rebase', branch])
        elif choice == "2":
            commit = input("请输入起始提交 (HEAD~n): ")
            execute_git_command(['rebase', '-i', commit])
        elif choice == "3":
            execute_git_command(['rebase', '--abort'])
        else:
            print_colored("无效的选择，请重试", "yellow")
            continue
        
        input("\n按回车键继续...")

def main():
    """
    主函数
    @return: None
    """
    try:
        # 清屏
        os.system('cls' if os.name == 'nt' else 'clear')
        
        while True:
            show_menu()
            choice = input("\n请输入选项: ").lower()
            
            # 清屏
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if choice == 'h':
                show_help()
            elif choice == '0':
                if confirm_action("确定要退出程序吗？"):
                    print_colored("\n感谢使用，再见！", "green")
                    break
            elif choice == "1":
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
                handle_clone()
            elif choice == "8":
                handle_remote()
            elif choice == "9":
                handle_branch()
            elif choice == "10":
                handle_checkout()
            elif choice == "11":
                handle_merge()
            elif choice == "12":
                handle_config()
            elif choice == "13":
                handle_tag()
            elif choice == "14":
                handle_stash()
            elif choice == "15":
                handle_advanced()
            elif choice == "16":
                handle_recovery()
            elif choice == "17":
                handle_settings()
            elif choice == "18":
                handle_logs()
            elif choice == "19":
                check_update()
            elif choice == "m":
                handle_menu_mode()
            elif choice == "c":
                handle_custom_menu()
            else:
                print_colored("无效的选择，请重试", "yellow")
                continue
            
            # 每个操作后暂停
            if choice not in ['0', 'h', 'm', 'c']:
                input("\n按回车键继续...")
            
            # 清屏
            os.system('cls' if os.name == 'nt' else 'clear')
            
    except KeyboardInterrupt:
        print_colored("\n\n程序被中断，正在安全退出...", "yellow")
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n程序出错: {str(e)}", "red")
        input("\n按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main() 