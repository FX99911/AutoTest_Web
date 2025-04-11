"""
自动化测试配置窗口启动模块

该模块提供了一个图形用户界面，用于设置自动化测试的各项配置，包括四个sheet页：
1. 配置信息sheet页：用于设置自动化测试的基本配置
2. 文件管理sheet页：用于管理测试用例文件
3. 测试用例导入sheet页：用于查看已上传的测试用例文件和目录
4. 测试启动sheet页：用于启动测试执行
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from web_keys.environment_info.montage_url import home

# 导入四个sheet页模块
from sheets.config_sheet import create_config_sheet, save_config
from sheets.file_management_sheet import create_file_management_sheet, upload_selected_files
from sheets.test_case_import_sheet import create_test_case_import_sheet
from sheets.test_launcher_sheet import create_test_launcher_sheet


def create_widgets(root, is_closed_by_x):
    """
    创建并布局窗口中的各种控件

    Args:
        root: 主窗口对象
        is_closed_by_x: 窗口关闭方式的标志变量

    Returns:
        dict: 包含控件引用的字典
    """
    widget_dict = {}

    # 创建主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建选项卡控件
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # 创建四个sheet页
    config_frame = ttk.Frame(notebook)
    file_management_frame = ttk.Frame(notebook)
    test_case_import_frame = ttk.Frame(notebook)
    test_launcher_frame = ttk.Frame(notebook)

    notebook.add(config_frame, text="配置信息")
    notebook.add(file_management_frame, text="文件管理")
    notebook.add(test_case_import_frame, text="测试用例导入")
    notebook.add(test_launcher_frame, text="测试启动")

    # 创建各个sheet页的内容
    create_config_sheet(config_frame, widget_dict)
    create_file_management_sheet(file_management_frame, widget_dict)
    create_test_case_import_sheet(test_case_import_frame, widget_dict)
    create_test_launcher_sheet(test_launcher_frame, widget_dict)

    # 状态栏 - 显示操作状态
    status_frame = ttk.Frame(root)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    status_label = ttk.Label(status_frame, text="准备就绪", relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(fill=tk.X)
    widget_dict['status_label'] = status_label

    return widget_dict


def on_close(root, is_closed_by_x):
    """
    处理窗口关闭事件

    Args:
        root: 主窗口对象
        is_closed_by_x: 用于记录窗口关闭方式的标志变量
    """
    if messagebox.askokcancel("退出", "确定要退出吗？"):
        is_closed_by_x[0] = True  # 标记为取消关闭
        root.destroy()  # 关闭窗口


def start_window_config():
    """
    创建并显示配置窗口

    Returns:
        bool: 窗口是否被取消关闭的标志，True表示取消关闭
    """
    # 创建主窗口
    root = tk.Tk()
    root.title("自动化测试配置")
    root.geometry("1200x700")  # 设置窗口初始大小

    # 设置窗口图标（如果有）
    try:
        root.iconbitmap(os.path.join(home, "assets", "icon.ico"))
    except:
        pass  # 如果图标不存在，忽略错误

    # 应用现代主题样式
    style = ttk.Style()

    # 为不同平台设置不同主题
    if root.tk.call('tk', 'windowingsystem') == 'win32':
        # Windows平台
        try:
            # 尝试加载自定义主题
            root.tk.call("source", os.path.join(home, "assets", "azure.tcl"))
            root.tk.call("set_theme", "light")
        except:
            # 如果没有自定义主题，使用内置主题
            style.theme_use('vista')
    else:
        # macOS或Linux
        style.theme_use('clam')

    # 自定义按钮样式
    style.configure("Accent.TButton", font=("Arial", 10, "bold"))

    # 用于跟踪窗口关闭方式的标志
    is_closed_by_x = [False]

    # 设置窗口关闭事件处理
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, is_closed_by_x))

    # 创建窗口控件
    widget_dict = create_widgets(root, is_closed_by_x)

    # 设置初始焦点
    root.after(100, lambda: root.focus_force())

    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # 启动主循环
    root.mainloop()

    # 窗口关闭后的处理
    if is_closed_by_x[0]:
        print("窗口点击X号或取消按钮关闭,取消提交")
    else:
        print("窗口点击了提交,提交成功")

    return is_closed_by_x[0]


# 当作为主程序运行时，启动配置窗口
if __name__ == "__main__":
    start_window_config() 