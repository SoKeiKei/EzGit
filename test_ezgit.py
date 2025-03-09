#!/usr/bin/env python3
import sys
import os
import datetime

def log_to_file(msg, level="INFO"):
    """
    将消息写入日志文件
    @param msg: str 要记录的消息
    @param level: str 日志级别
    @return: None
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("test_log.txt", "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] [{level}] {msg}\n")
        f.flush()

def test_basic_functions():
    """
    测试基本功能函数
    @return: bool 测试是否通过
    """
    functions = {
        "handle_status": "查看状态",
        "handle_add": "暂存更改",
        "handle_commit": "提交更改",
        "handle_log": "查看历史",
        "handle_push": "推送更改",
        "handle_pull": "拉取更新"
    }
    return test_functions("基本功能", functions)

def test_advanced_functions():
    """
    测试高级功能函数
    @return: bool 测试是否通过
    """
    functions = {
        "handle_branch": "分支操作",
        "handle_checkout": "切换分支",
        "handle_merge": "合并分支",
        "handle_rebase": "变基操作",
        "handle_tag": "标签管理",
        "handle_stash": "储藏管理",
        "handle_config": "配置信息",
        "handle_remote": "远程配置",
        "handle_clone": "克隆仓库"
    }
    return test_functions("高级功能", functions)

def test_tool_functions():
    """
    测试工具相关函数
    @return: bool 测试是否通过
    """
    functions = {
        "handle_settings": "配置工具",
        "handle_logs": "查看日志",
        "handle_menu_mode": "菜单模式",
        "handle_custom_menu": "自定义菜单",
        "handle_advanced": "高级操作",
        "handle_recovery": "错误恢复",
        "handle_diff": "查看差异",
        "handle_submodule": "子模块管理",
        "handle_workflow": "工作流管理",
        "handle_clean": "清理仓库"
    }
    return test_functions("工具功能", functions)

def test_helper_functions():
    """
    测试辅助函数
    @return: bool 测试是否通过
    """
    functions = {
        "print_colored": "彩色输出",
        "confirm_action": "确认操作",
        "execute_git_command": "执行Git命令",
        "load_config": "加载配置",
        "load_custom_menu": "加载菜单",
        "check_dependencies": "检查依赖"
    }
    return test_functions("辅助功能", functions)

def test_functions(category, functions):
    """
    通用函数测试
    @param category: str 功能分类
    @param functions: dict 要测试的函数
    @return: bool 测试是否通过
    """
    log_to_file(f"\n开始测试{category}...", "TEST")
    
    try:
        with open("EzGit.py", "r", encoding='utf-8') as f:
            content = f.read()
        
        missing = []
        for func, desc in functions.items():
            if f"def {func}(" in content:  # 更精确的函数定义匹配
                log_to_file(f"[√] 找到函数: {func} ({desc})")
            else:
                log_to_file(f"[×] 缺失函数: {func} ({desc})", "WARN")
                missing.append(func)
        
        if missing:
            log_to_file(f"{category}测试完成: 发现 {len(missing)} 个缺失的函数", "WARN")
            for func in missing:
                log_to_file(f"- {func}", "WARN")
            log_to_file(f"{category}测试结果: 失败", "INFO")
            return False
        else:
            log_to_file(f"{category}测试完成: 所有功能已实现！", "INFO")
            log_to_file(f"{category}测试结果: 通过", "INFO")
            return True
            
    except Exception as e:
        log_to_file(f"{category}测试出错: {str(e)}", "ERROR")
        import traceback
        log_to_file(traceback.format_exc(), "ERROR")
        return False

def test_file_structure():
    """
    测试文件结构
    @return: bool 测试是否通过
    """
    log_to_file("\n开始测试文件结构...", "TEST")
    
    try:
        # 检查必要文件是否存在
        required_files = {
            "EzGit.py": "主程序文件",
            "README.md": "说明文档",
            "requirements.txt": "依赖列表"
        }
        
        missing_files = []
        for file, desc in required_files.items():
            if os.path.exists(file):
                log_to_file(f"[√] 找到文件: {file} ({desc})")
            else:
                log_to_file(f"[×] 缺失文件: {file} ({desc})", "WARN")
                missing_files.append(file)
        
        # 检查配置目录
        config_dir = os.path.expanduser('~/.ezgit')
        if os.path.exists(config_dir):
            log_to_file(f"[√] 找到配置目录: {config_dir}")
        else:
            log_to_file(f"[×] 缺失配置目录: {config_dir}", "WARN")
            missing_files.append(config_dir)
        
        if missing_files:
            log_to_file("文件结构测试结果: 失败", "INFO")
            return False
        else:
            log_to_file("文件结构测试结果: 通过", "INFO")
            return True
        
    except Exception as e:
        log_to_file(f"文件结构测试出错: {str(e)}", "ERROR")
        return False

def run_test():
    """
    运行所有测试
    @return: bool 测试是否通过
    """
    log_to_file("正在启动测试...")
    log_to_file(f"当前工作目录: {os.getcwd()}")
    log_to_file(f"Python版本: {sys.version}")
    log_to_file("="*50)
    
    # 检查 EzGit.py 是否存在
    if not os.path.exists("EzGit.py"):
        log_to_file("错误: 找不到 EzGit.py 文件", "ERROR")
        return False
    
    log_to_file(f"找到 EzGit.py 文件: {os.path.abspath('EzGit.py')}")
    
    # 运行所有测试
    tests = [
        ("文件结构测试", test_file_structure),
        ("基本功能测试", test_basic_functions),
        ("高级功能测试", test_advanced_functions),
        ("工具功能测试", test_tool_functions),
        ("辅助功能测试", test_helper_functions)
    ]
    
    results = []
    for name, test_func in tests:
        log_to_file(f"\n开始{name}...", "TEST")
        result = test_func()
        results.append((name, result))
        log_to_file(f"{name}结果: {'通过' if result else '失败'}")
        log_to_file("="*50)
    
    # 汇总测试结果
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    log_to_file(f"\n测试总结:", "SUMMARY")
    log_to_file(f"总计测试项: {total}")
    log_to_file(f"通过测试项: {passed}")
    log_to_file(f"失败测试项: {total - passed}")
    
    for name, result in results:
        status = "通过" if result else "失败"
        log_to_file(f"- {name}: {status}")
    
    return passed == total

if __name__ == "__main__":
    # 清空之前的日志
    with open("test_log.txt", "w", encoding='utf-8') as f:
        f.write("")
    
    log_to_file("\n开始执行测试脚本...")
    success = run_test()
    log_to_file(f"\n最终测试结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1) 