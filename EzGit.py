#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import json
import logging
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
            print(f"{num.rjust(2)}. {name.ljust(12)} {cmd}")

    print_colored("\n[其他选项]", "yellow")
    print(" 0. 退出程序")
    print(" h. 显示帮助")
    print("\n" + "="*50)
    print_colored("提示：输入命令编号执行操作，输入 'h' 查看帮助", "green")

def show_help():
    """
    显示帮助信息
    @return: None
    """
    print_colored("\n=== EzGit 使用帮助 ===", "cyan")
    print_colored("Version: 1.0.0", "purple")
    print_colored("Author: SoKei", "purple")
    print_colored("GitHub: https://github.com/SoKei/EzGit", "purple")
    
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
    分支操作功能增强:
    - 查看所有分支(包括远程分支)
    - 创建新分支
    - 删除分支
    - 重命名分支
    - 合并分支
    """
    print("\n=== 分支操作 ===")
    print("1. 查看所有分支")
    print("2. 创建新分支")
    print("3. 删除分支")
    print("4. 重命名分支")
    print("5. 合并分支")
    print("0. 返回主菜单")
    
    choice = input("请选择 (0-5): ")
    
    if choice == "1":
        print("\n本地分支:")
        execute_git_command(['branch'])
        print("\n远程分支:")
        execute_git_command(['branch', '-r'])
    elif choice == "2":
        branch_name = input("请输入新分支名称: ")
        base_branch = input("请输入基础分支(直接回车使用当前分支): ").strip()
        if base_branch:
            execute_git_command(['branch', branch_name, base_branch])
        else:
            execute_git_command(['branch', branch_name])
    elif choice == "3":
        branch_name = input("请输入要删除的分支名称: ")
        force = input("是否强制删除？(y/n): ").lower() == 'y'
        if force:
            execute_git_command(['branch', '-D', branch_name])
        else:
            execute_git_command(['branch', '-d', branch_name])
    elif choice == "4":
        old_name = input("请输入要重命名的分支名称: ")
        new_name = input("请输入新的分支名称: ")
        execute_git_command(['branch', '-m', old_name, new_name])
    elif choice == "5":
        source_branch = input("请输入要合并的源分支名称: ")
        print("\n合并策略：")
        print("1. 普通合并")
        print("2. 压缩合并(squash)")
        merge_choice = input("请选择合并策略 (1/2): ")
        if merge_choice == "1":
            execute_git_command(['merge', source_branch])
        elif merge_choice == "2":
            execute_git_command(['merge', '--squash', source_branch])

def handle_clone():
    """
    处理git clone命令
    支持克隆仓库到当前目录
    """
    repo_url = input("\n请输入GitHub仓库URL: ")
    try:
        # 首先确保目录为空或只包含.git文件夹
        current_dir = os.getcwd()
        files = os.listdir(current_dir)
        if files and any(f != '.git' for f in files):
            print("警告：当前目录不为空！")
            confirm = input("是否继续？这可能会覆盖现有文件 (y/n): ")
            if confirm.lower() != 'y':
                return

        # 创建临时目录
        temp_dir = os.path.join(current_dir, 'temp_clone')
        os.makedirs(temp_dir, exist_ok=True)
        
        # 先克隆到临时目录
        subprocess.run(['git', 'clone', repo_url, temp_dir], check=True)
        
        # 移动文件到当前目录
        temp_contents = os.listdir(temp_dir)
        for item in temp_contents:
            if item != '.git':  # 不移动.git文件夹
                src = os.path.join(temp_dir, item)
                dst = os.path.join(current_dir, item)
                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        print("仓库克隆成功！")
        
    except Exception as e:
        print(f"克隆失败: {str(e)}")

def handle_config():
    """
    Git配置管理:
    - 查看当前配置
    - 设置用户名和邮箱
    """
    print("\n=== Git 配置 ===")
    print("1. 查看当前配置")
    print("2. 设置用户名和邮箱")
    choice = input("请选择 (1/2): ")
    
    if choice == "1":
        execute_git_command(['config', '--list'])
    elif choice == "2":
        username = input("请输入Git用户名: ")
        email = input("请输入Git邮箱: ")
        execute_git_command(['config', '--global', 'user.name', username])
        execute_git_command(['config', '--global', 'user.email', email])
        print("Git用户信息配置完成！")

def handle_remote():
    """
    远程仓库管理:
    - 查看远程仓库
    - 添加远程仓库
    - 修改远程仓库URL
    """
    print("\n=== 远程仓库管理 ===")
    print("1. 查看远程仓库")
    print("2. 添加远程仓库")
    print("3. 修改远程仓库URL")
    choice = input("请选择 (1/2/3): ")
    
    if choice == "1":
        execute_git_command(['remote', '-v'])
    elif choice == "2":
        remote_name = input("请输入远程仓库名称 (通常是origin): ")
        remote_url = input("请输入远程仓库URL: ")
        execute_git_command(['remote', 'add', remote_name, remote_url])
    elif choice == "3":
        remote_name = input("请输入远程仓库名称 (通常是origin): ")
        remote_url = input("请输入新的远程仓库URL: ")
        execute_git_command(['remote', 'set-url', remote_name, remote_url])

def handle_push():
    """
    处理git push命令
    - 检查是否有未提交的更改
    - 提供处理未提交更改的选项
    - 执行推送操作
    """
    try:
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
                # 暂存并正常提交
                execute_git_command(['add', '.'])
                commit_msg = input("请输入提交信息: ")
                if not execute_git_command(['commit', '-m', commit_msg]):
                    print("\n正常提交失败，是否尝试跳过检查提交？(y/n): ")
                    if input().lower() == 'y':
                        execute_git_command(['commit', '-m', commit_msg, '--no-verify'])
                    else:
                        print("操作已取消")
                        return
            elif choice == "2":
                # 暂存并跳过检查提交
                execute_git_command(['add', '.'])
                commit_msg = input("请输入提交信息: ")
                execute_git_command(['commit', '-m', commit_msg, '--no-verify'])
            elif choice == "3":
                # 储藏更改
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
        print(f"正在推送分支 '{current_branch}' 到远程仓库...")
        
        # 直接尝试推送到远程，设置上游分支
        push_result = execute_git_command(['push', '--set-upstream', 'origin', current_branch])
        
        if push_result:
            print(f"成功推送分支 '{current_branch}' 到远程仓库")
            
            # 如果之前选择了储藏更改，现在恢复它们
            if choice == "3":
                print("恢复储藏的更改...")
                execute_git_command(['stash', 'pop'])
                print("如果有冲突，请手动解决后提交")
        else:
            print("推送失败，请检查以下可能的原因：")
            print("1. 远程仓库是否已配置")
            print("2. 是否有推送权限")
            print("3. 网络连接是否正常")
            print("\n可以使用以下命令检查远程仓库配置：")
            print("选择选项 8 (git remote) 然后选择 1 查看远程仓库配置")
            
    except Exception as e:
        print(f"推送失败: {str(e)}")

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
    处理提交历史查看和还原功能
    """
    print("\n=== 提交历史 ===")
    commits = get_commit_history()
    
    if not commits:
        print("没有找到提交记录")
        return
        
    # 直接显示提交历史
    for i, (commit_hash, message) in enumerate(commits, 1):
        print(f"{i}. {commit_hash} - {message}")
    
    print("\n操作选项：")
    print("1. 还原历史提交")
    print("0. 返回主菜单")
    
    choice = input("\n请选择 (0/1): ")
    
    if choice == "0":
        return
    elif choice == "1":
        try:
            commit_choice = int(input("\n请选择要还原的提交编号 (0 取消): "))
            if commit_choice == 0:
                return
                
            if 1 <= commit_choice <= len(commits):
                selected_hash = commits[commit_choice-1][0]
                
                print("\n还原方式：")
                print("1. 硬还原 (丢弃所有更改)")
                print("2. 软还原 (保留更改在工作区)")
                print("3. 取消操作")
                
                reset_choice = input("\n请选择还原方式 (1/2/3): ")
                
                if reset_choice == "1":
                    confirm = input("\n警告：硬还原将丢失所有未提交的更改！确认继续？(y/n): ")
                    if confirm.lower() == 'y':
                        execute_git_command(['reset', '--hard', selected_hash])
                        print(f"\n已还原到提交: {selected_hash}")
                elif reset_choice == "2":
                    execute_git_command(['reset', '--soft', selected_hash])
                    print(f"\n已软还原到提交: {selected_hash}")
                    print("您的更改已保留在工作区")
            else:
                print("\n无效的选择")
        except ValueError:
            print("\n请输入有效的数字")
    else:
        print("\n无效的选择")

def handle_tag():
    """
    标签管理功能
    @return: None
    """
    while True:
        print("\n" + "="*40)
        print_colored("标签管理", "cyan")
        print("="*40)
        print("1. 查看所有标签")
        print("2. 创建新标签")
        print("3. 删除标签")
        print("4. 推送标签到远程")
        print("\n0. 返回主菜单")
        
        choice = input("\n请选择 (0-4): ")
        
        if choice == "0":
            return
        elif choice == "1":
            execute_git_command(['tag', '-l'])
        elif choice == "2":
            tag_name = input("请输入标签名称: ")
            tag_message = input("请输入标签说明(可选): ")
            if tag_message:
                execute_git_command(['tag', '-a', tag_name, '-m', tag_message])
            else:
                execute_git_command(['tag', tag_name])
        elif choice == "3":
            tag_name = input("请输入要删除的标签名称: ")
            execute_git_command(['tag', '-d', tag_name])
        elif choice == "4":
            tag_name = input("请输入要推送的标签名称(直接回车推送所有标签): ").strip()
            if tag_name:
                execute_git_command(['push', 'origin', tag_name])
            else:
                execute_git_command(['push', 'origin', '--tags'])
        else:
            print_colored("无效的选择", "yellow")
            continue
            
        input("\n按回车键继续...")

def handle_stash():
    """
    储藏管理功能:
    - 储藏当前更改
    - 查看储藏列表
    - 应用储藏
    - 删除储藏
    """
    print("\n=== 储藏管理 ===")
    print("1. 储藏当前更改")
    print("2. 查看储藏列表")
    print("3. 应用储藏")
    print("4. 删除储藏")
    print("0. 返回主菜单")
    
    choice = input("请选择 (0-4): ")
    
    if choice == "1":
        stash_message = input("请输入储藏说明(可选): ")
        if stash_message:
            execute_git_command(['stash', 'save', stash_message])
        else:
            execute_git_command(['stash'])
    elif choice == "2":
        execute_git_command(['stash', 'list'])
    elif choice == "3":
        execute_git_command(['stash', 'list'])
        stash_index = input("\n请输入要应用的储藏索引(如 stash@{0} 输入0): ")
        pop = input("是否在应用后删除该储藏？(y/n): ").lower() == 'y'
        if pop:
            execute_git_command(['stash', 'pop', f'stash@{{{stash_index}}}'])
        else:
            execute_git_command(['stash', 'apply', f'stash@{{{stash_index}}}'])
    elif choice == "4":
        execute_git_command(['stash', 'list'])
        stash_index = input("\n请输入要删除的储藏索引(如 stash@{0} 输入0): ")
        execute_git_command(['stash', 'drop', f'stash@{{{stash_index}}}'])

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
    处理仓库状态查看
    - 检查是否为Git仓库
    - 提供初始化选项
    @return: None
    """
    if not check_git_repo():
        print_colored("\n当前目录不是Git仓库！", "yellow")
        print("\n是否要初始化Git仓库？")
        print("1. 是")
        print("2. 否")
        
        choice = input("\n请选择 (1/2): ")
        
        if choice == "1":
            if init_repository():
                print_colored("\n初始化成功！现在可以开始使用Git了", "green")
                # 显示新仓库的状态
                execute_git_command(['status'])
            else:
                print_colored("\n初始化失败，请检查权限或目录状态", "red")
        return
    
    # 是Git仓库，显示状态信息
    print_colored("\n=== 仓库状态 ===", "cyan")
    execute_git_command(['status'])

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
    检查工具更新
    @return: bool 是否有更新
    """
    try:
        # 尝试导入 requests
        import requests
        
        response = requests.get('https://api.github.com/repos/SoKei/EzGit/releases/latest')
        latest_version = response.json()['tag_name']
        current_version = "1.0.0"  # 当前版本
        
        if latest_version > current_version:
            print_colored(f"\n发现新版本: {latest_version}", "green")
            print("更新内容:")
            print(response.json()['body'])
            return True
        return False
    except ImportError:
        print_colored("\n提示: 如需使用自动更新检查功能，请安装 requests 库", "yellow")
        print_colored("pip install requests", "yellow")
        print_colored("您也可以直接访问 GitHub 页面检查更新:", "yellow")
        print_colored("https://github.com/SoKei/EzGit/releases", "blue")
        print("\n请选择操作：")
        print("1. 安装 requests 库")
        print("2. 访问 GitHub 页面手动检查更新")
        print("0. 返回主菜单")
        
        choice = input("\n请选择 (0-2): ")
        
        if choice == "1":
            try:
                print_colored("\n正在安装 requests 库...", "cyan")
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests'],
                                     capture_output=True,
                                     text=True)
                if result.returncode == 0:
                    print_colored("安装成功！", "green")
                    print("请重新执行检查更新操作")
                else:
                    print_colored("安装失败，请手动执行:", "red")
                    print("pip install requests")
            except Exception as e:
                print_colored(f"安装过程出错: {str(e)}", "red")
        elif choice == "2":
            print_colored("\n请访问以下地址检查更新:", "cyan")
            print_colored("https://github.com/SoKei/EzGit/releases", "blue")
        
        return False
    except Exception as e:
        print_colored(f"检查更新失败: {str(e)}", "red")
        return False

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
            else:
                print_colored("无效的选择，请重试", "yellow")
                continue
            
            # 每个操作后暂停
            if choice not in ['0', 'h']:
                input("\n按回车键继续...")
            
            # 清屏
            os.system('cls' if os.name == 'nt' else 'clear')
            
    except KeyboardInterrupt:
        print_colored("\n\n程序被中断，正在安全退出...", "yellow")
        sys.exit(0)

if __name__ == "__main__":
    main() 