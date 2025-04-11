"""
测试启动sheet页

该模块提供了一个图形用户界面，用于启动测试执行，包括：
1. 选择要执行的测试用例文件
2. 配置测试执行参数
3. 启动测试执行
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import threading
import time
from web_keys.environment_info.montage_url import home

# 测试用例文件目录路径
CASES_DATE_DIR = os.path.join(home, 'cases_date')
# 测试报告目录路径
REPORTS_DIR = os.path.join(home, 'reports')
# 目录树根路径
DIR_TREE_ROOT_PATH = os.path.join(home, 'cases_run')

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


def create_test_launcher_sheet(parent_frame, widget_dict):
    """
    创建测试启动sheet页

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
    title_label = ttk.Label(main_frame, text="测试启动", font=("Arial", 16, "bold"))
    title_label.pack(anchor="center", pady=(0, 20))

    # 创建文件选择区域
    file_frame = ttk.LabelFrame(main_frame, text="选择测试用例文件", padding=(10, 5))
    file_frame.pack(fill="both", expand=True, pady=(0, 15))

    # 创建目录树框架
    dir_tree_frame = ttk.Frame(file_frame)
    dir_tree_frame.pack(fill="both", expand=True, pady=5)

    # 创建目录树
    dir_tree_scrollbar = ttk.Scrollbar(dir_tree_frame)
    dir_tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    dir_tree = ttk.Treeview(dir_tree_frame, yscrollcommand=dir_tree_scrollbar.set)
    dir_tree.pack(side=tk.LEFT, fill="both", expand=True)
    dir_tree_scrollbar.config(command=dir_tree.yview)

    # 配置目录树
    dir_tree["columns"] = ("path", "size", "modified")
    dir_tree.column("#0", width=300, minwidth=200)
    dir_tree.column("path", width=0, stretch=tk.NO)
    dir_tree.column("size", width=100)
    dir_tree.column("modified", width=150)
    dir_tree.heading("#0", text="名称")
    dir_tree.heading("path", text="路径")
    dir_tree.heading("size", text="大小")
    dir_tree.heading("modified", text="修改日期")

    # 设置目录树样式
    style = ttk.Style()
    style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
    style.configure("Treeview.Heading", background="#3c3f41", foreground="white")
    style.map("Treeview", background=[("selected", "#4a6ea9")])

    # 存储当前路径和展开状态
    current_path = [DIR_TREE_ROOT_PATH]
    expanded_items = set()

    # 填充目录树
    def populate_dir_tree(path, parent=""):
        """
        填充目录树，只显示.py文件
        """
        if parent == "":
            for item in dir_tree.get_children():
                dir_tree.delete(item)

        try:
            items = os.listdir(path)
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    node_id = dir_tree.insert(parent, "end", text=item, values=(full_path, "", ""))
                    populate_dir_tree(full_path, node_id)
                    if full_path in expanded_items:
                        dir_tree.item(node_id, open=True)
                elif item.endswith('.py'):  # 只显示.py文件
                    # 获取文件大小和修改时间
                    size = os.path.getsize(full_path)
                    modified_time = os.path.getmtime(full_path)
                    modified_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified_time))
                    size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
                    dir_tree.insert(parent, "end", text=item, values=(full_path, size_str, modified_str))
        except Exception as e:
            print(f"填充目录树出错: {e}")

    # 初始填充目录树
    populate_dir_tree(DIR_TREE_ROOT_PATH)

    # 目录树点击事件
    def on_dir_tree_select(event):
        """
        处理目录树选择事件
        """
        selected_items = dir_tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        path = dir_tree.item(item, "values")[0]
        current_path[0] = path

    dir_tree.bind("<<TreeviewSelect>>", on_dir_tree_select)

    # 目录树展开/折叠事件
    def on_tree_expand(event):
        item = dir_tree.focus()
        path = dir_tree.item(item, "values")[0]
        expanded_items.add(path)

    def on_tree_collapse(event):
        item = dir_tree.focus()
        path = dir_tree.item(item, "values")[0]
        expanded_items.discard(path)

    dir_tree.bind("<<TreeviewOpen>>", on_tree_expand)
    dir_tree.bind("<<TreeviewClose>>", on_tree_collapse)

    # 按钮区域
    buttons_frame = ttk.Frame(file_frame)
    buttons_frame.pack(fill="x", pady=10)

    def refresh_dir_tree():
        """
        刷新目录树，保持当前展开状态
        """
        current_selection = dir_tree.selection()
        current_path = [DIR_TREE_ROOT_PATH]
        if current_selection:
            current_path[0] = dir_tree.item(current_selection[0], "values")[0]

        populate_dir_tree(DIR_TREE_ROOT_PATH)

        # 恢复展开状态
        for path in expanded_items:
            for item in dir_tree.get_children():
                if dir_tree.item(item, "values")[0] == path:
                    dir_tree.item(item, open=True)
                    break

    refresh_button = ttk.Button(buttons_frame, text="刷新目录", command=refresh_dir_tree, width=15)
    refresh_button.pack(side=tk.LEFT, padx=5)

    # 创建参数配置区域
    param_frame = ttk.LabelFrame(main_frame, text="测试参数配置", padding=(10, 5))
    param_frame.pack(fill="x", pady=(0, 15))

    # 添加参数配置选项
    options_frame = ttk.Frame(param_frame)
    options_frame.pack(fill="x", pady=5)

    # 添加-v选项（详细输出）
    verbose_var = tk.BooleanVar(value=True)
    verbose_check = ttk.Checkbutton(options_frame, text="-v (详细输出)", variable=verbose_var)
    verbose_check.pack(side=tk.LEFT, padx=10)

    # 添加-s选项（显示print输出）
    show_output_var = tk.BooleanVar(value=True)
    show_output_check = ttk.Checkbutton(options_frame, text="-s (显示print输出)", variable=show_output_var)
    show_output_check.pack(side=tk.LEFT, padx=10)

    # 添加--html选项（生成HTML报告）
    html_report_var = tk.BooleanVar(value=True)
    html_report_check = ttk.Checkbutton(options_frame, text="--html (生成HTML报告)", variable=html_report_var)
    html_report_check.pack(side=tk.LEFT, padx=10)

    # 创建执行区域
    execution_frame = ttk.LabelFrame(main_frame, text="执行测试", padding=(10, 5))
    execution_frame.pack(fill="x", pady=(0, 15))

    # 添加状态标签
    status_label = ttk.Label(execution_frame, text="就绪")
    status_label.pack(pady=5)

    # 添加输出文本框
    output_frame = ttk.Frame(execution_frame)
    output_frame.pack(fill="both", expand=True, pady=5)

    output_scrollbar = ttk.Scrollbar(output_frame)
    output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_text = tk.Text(output_frame, yscrollcommand=output_scrollbar.set, height=10, wrap=tk.WORD)
    output_text.pack(side=tk.LEFT, fill="both", expand=True)
    output_scrollbar.config(command=output_text.yview)

    widget_dict['output_text'] = output_text
    widget_dict['status_label'] = status_label

    # 添加执行按钮
    def start_execution():
        """
        开始执行测试
        """
        selected_items = dir_tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要执行的测试用例文件")
            return

        item = selected_items[0]
        file_path = dir_tree.item(item, "values")[0]
        file_name = dir_tree.item(item, "text")

        # 更新状态标签
        status_label.config(text="正在执行...")
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"开始执行测试用例: {file_name}\n\n")

        # 构建pytest命令
        cmd = ["pytest"]

        # 添加参数
        if verbose_var.get():
            cmd.append("-v")

        if show_output_var.get():
            cmd.append("-s")

        if html_report_var.get():
            report_path = os.path.join(REPORTS_DIR, f"{os.path.splitext(file_name)[0]}_report.html")
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            cmd.extend(["--html", report_path])

        # 添加测试文件路径
        cmd.append(file_path)

        # 在新线程中执行命令，避免界面卡死
        def run_command():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )

                # 实时读取输出
                for line in process.stdout:
                    output_text.insert(tk.END, line)
                    output_text.see(tk.END)
                    output_text.update_idletasks()

                process.wait()

                # 更新状态标签
                if process.returncode == 0:
                    status_label.config(text="执行完成")
                    messagebox.showinfo("成功", f"测试用例 {file_name} 执行完成")
                else:
                    status_label.config(text="执行失败")
                    messagebox.showerror("错误", f"测试用例 {file_name} 执行失败")

            except Exception as e:
                # 更新状态标签
                status_label.config(text="执行失败")
                error_msg = f"执行测试用例时出错: {e}"
                output_text.insert(tk.END, f"\n{error_msg}\n")
                messagebox.showerror("错误", error_msg)

        # 启动线程
        threading.Thread(target=run_command, daemon=True).start()

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
        command=lambda: dir_tree.selection_clear(),
        width=15
    )
    cancel_button.pack(side=tk.LEFT, padx=10)

    return widget_dict 