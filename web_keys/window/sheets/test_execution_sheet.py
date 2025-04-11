"""
测试执行sheet页

该模块提供了一个图形用户界面，用于选择测试用例文件并启动自动化测试执行，包括：
1. 显示可用的测试用例文件
2. 选择要执行的测试用例文件
3. 启动自动化测试执行
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from web_keys.environment_info.montage_url import home

# 测试用例文件目录路径
CASES_DATE_DIR = os.path.join(home, 'cases_date')

def get_xlsx_files_in_cases_date():
    """
    获取cases_date目录下所有的xlsx文件

    Returns:
        list: xlsx文件列表，如果目录不存在会先创建
    """
    if not os.path.exists(CASES_DATE_DIR):
        os.makedirs(CASES_DATE_DIR, exist_ok=True)
        return []

    files = os.listdir(CASES_DATE_DIR)
    xlsx_files = [f for f in files if f.lower().endswith('.xlsx')]
    return xlsx_files


def create_test_execution_sheet(parent_frame, widget_dict):
    """
    创建测试执行sheet页

    Args:
        parent_frame: 父框架对象
        widget_dict: 用于存储控件引用的字典

    Returns:
        dict: 更新后的widget_dict
    """
    # 创建主框架
    main_frame = ttk.Frame(parent_frame, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建标题
    title_label = ttk.Label(main_frame, text="测试执行", font=("Arial", 16, "bold"))
    title_label.pack(anchor="w", pady=(0, 20))

    # 创建文件选择区域
    file_frame = ttk.LabelFrame(main_frame, text="选择测试用例文件", padding=(10, 5))
    file_frame.pack(fill="x", pady=(0, 15))

    # 创建列表框显示可用的测试用例文件
    list_frame = ttk.Frame(file_frame)
    list_frame.pack(fill="both", expand=True, pady=5)

    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
    listbox.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    # 填充列表框，显示当前已有的Excel文件
    xlsx_files = get_xlsx_files_in_cases_date()
    for file in xlsx_files:
        listbox.insert(tk.END, file)

    widget_dict['test_execution_listbox'] = listbox

    # 添加刷新按钮
    def refresh_list():
        """
        刷新文件列表，显示cases_date目录下的最新文件
        """
        listbox.delete(0, tk.END)  # 清空列表
        xlsx_files = get_xlsx_files_in_cases_date()  # 重新获取文件列表
        for file in xlsx_files:
            listbox.insert(tk.END, file)  # 重新填充列表

    refresh_button = ttk.Button(file_frame, text="刷新列表", command=refresh_list)
    refresh_button.pack(pady=10)

    # 创建执行区域
    execution_frame = ttk.LabelFrame(main_frame, text="执行测试", padding=(10, 5))
    execution_frame.pack(fill="x", pady=(0, 15))

    # 添加状态标签
    status_label = ttk.Label(execution_frame, text="就绪")
    status_label.pack(pady=5)

    # 添加执行按钮
    def start_execution():
        """
        开始执行测试
        """
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("提示", "请先选择要执行的测试用例文件")
            return

        selected_index = selected_indices[0]
        file_name = listbox.get(selected_index)
        file_path = os.path.join(CASES_DATE_DIR, file_name)

        # 更新状态标签
        status_label.config(text="正在执行...")

        try:
            # 这里添加实际的测试执行代码
            # 例如：调用测试执行模块
            print(f"开始执行测试用例: {file_path}")
            
            # 模拟测试执行
            import time
            time.sleep(2)  # 模拟测试执行时间
            
            # 更新状态标签
            status_label.config(text="执行完成")
            messagebox.showinfo("成功", f"测试用例 {file_name} 执行完成")
        except Exception as e:
            # 更新状态标签
            status_label.config(text="执行失败")
            messagebox.showerror("错误", f"执行测试用例时出错: {e}")

    # 添加提交按钮区域
    submit_frame = ttk.Frame(main_frame)
    submit_frame.pack(fill="x", pady=20)

    # 执行按钮
    submit_button = ttk.Button(
        submit_frame,
        text="开始执行",
        command=start_execution,
        style="Accent.TButton",
        width=15
    )
    submit_button.pack(side=tk.LEFT, padx=10)

    # 取消按钮 - 清空选择
    cancel_button = ttk.Button(
        submit_frame,
        text="取消选择",
        command=lambda: listbox.selection_clear(0, tk.END),
        width=15
    )
    cancel_button.pack(side=tk.LEFT, padx=10)

    return widget_dict 