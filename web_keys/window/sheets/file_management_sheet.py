"""
测试用例文件管理sheet页

该模块提供了一个图形用户界面，用于管理测试用例文件，包括：
1. 上传测试用例文件
2. 显示已上传的测试用例文件
3. 删除已上传的测试用例文件
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import time
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

def get_xlsx_files_from_directory(directory):
    """
    获取指定目录下所有的xlsx文件

    Args:
        directory: 目录路径

    Returns:
        list: xlsx文件列表
    """
    xlsx_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.xlsx'):
                xlsx_files.append(os.path.join(root, file))
    return xlsx_files

def create_file_management_sheet(parent_frame, widget_dict):
    """
    创建文件管理sheet页

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
    title_label = ttk.Label(main_frame, text="测试用例文件管理", font=("Arial", 16, "bold"))
    title_label.pack(anchor="center", pady=(0, 20))

    # 创建左右两栏框架
    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill="both", expand=True)

    # 左侧框架：文件上传区域
    left_frame = ttk.LabelFrame(content_frame, text="上传测试用例文件", padding=(10, 5))
    left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))

    # 创建列表框显示已选择的文件
    files_list_frame = ttk.Frame(left_frame)
    files_list_frame.pack(fill="both", expand=True, pady=5)

    # 创建表格
    columns = ("name", "modified")
    tree = ttk.Treeview(files_list_frame, columns=columns, show="headings")
    tree.heading("name", text="文件名")
    tree.heading("modified", text="修改日期")
    tree.column("name", width=300)
    tree.column("modified", width=150)

    # 添加滚动条
    scrollbar = ttk.Scrollbar(files_list_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # 布局
    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    widget_dict['selected_files'] = []  # 存储选择的文件路径列表
    widget_dict['files_tree'] = tree

    # 按钮区域 - 文件操作按钮
    file_buttons_frame = ttk.Frame(left_frame)
    file_buttons_frame.pack(fill="x", pady=10)

    def upload_files():
        """
        处理多文件上传功能，支持选择目录
        """
        # 选择文件或目录
        selection = filedialog.askopenfilenames(
            title="选择测试用例文件或目录",
            filetypes=[("Excel文件", "*.xlsx")]
        )

        if not selection:
            return

        # 获取所有xlsx文件
        xlsx_files = []
        for path in selection:
            if os.path.isdir(path):
                xlsx_files.extend(get_xlsx_files_from_directory(path))
            elif path.lower().endswith('.xlsx'):
                xlsx_files.append(path)

        if xlsx_files:
            # 添加新选择的文件
            for file_path in xlsx_files:
                # 检查是否已经添加过相同的文件
                if file_path in widget_dict['selected_files']:
                    messagebox.showinfo("提示", f"文件 {os.path.basename(file_path)} 已在列表中")
                    continue

                # 添加到文件列表
                widget_dict['selected_files'].append(file_path)
                file_name = os.path.basename(file_path)
                modified_time = os.path.getmtime(file_path)
                modified_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified_time))
                tree.insert("", "end", values=(file_name, modified_str))

    def remove_selected_file():
        """
        从已选择列表中移除选中的文件
        """
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要移除的文件")
            return

        for item in selected_items:
            index = tree.index(item)
            widget_dict['selected_files'].pop(index)
            tree.delete(item)

    def submit_files():
        """
        上传选中的文件到cases_date目录
        """
        if not widget_dict['selected_files']:
            messagebox.showwarning("提示", "请选择至少一个测试用例文件")
            return

        # 确保cases_date目录存在
        if not os.path.exists(CASES_DATE_DIR):
            os.makedirs(CASES_DATE_DIR, exist_ok=True)

        # 复制所有选中的文件到cases_date目录
        copied_files = []
        for file_path in widget_dict['selected_files']:
            file_name = os.path.basename(file_path)
            target_file_path = os.path.join(CASES_DATE_DIR, file_name)
            try:
                shutil.copy2(file_path, target_file_path)
                copied_files.append(file_name)
            except Exception as e:
                messagebox.showerror("错误", f"复制文件时出错: {e}")

        if copied_files:
            # 清空选择列表
            tree.delete(*tree.get_children())
            widget_dict['selected_files'] = []
            # 刷新右侧列表
            refresh_list()
            messagebox.showinfo("成功", f"已成功上传 {len(copied_files)} 个文件")

    # 添加文件操作按钮
    upload_button = ttk.Button(file_buttons_frame, text="选择文件", command=upload_files, width=15)
    upload_button.pack(side=tk.LEFT, padx=5)

    remove_button = ttk.Button(file_buttons_frame, text="移除选中", command=remove_selected_file, width=15)
    remove_button.pack(side=tk.LEFT, padx=5)

    submit_button = ttk.Button(file_buttons_frame, text="上传文件", command=submit_files, width=15)
    submit_button.pack(side=tk.LEFT, padx=5)

    # 右侧框架：显示cases_date目录下的xlsx文件列表
    right_frame = ttk.LabelFrame(content_frame, text="已上传的测试用例文件", padding=(10, 5))
    right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

    # 创建表格容器框架
    table_frame = ttk.Frame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    # 创建表格
    columns = ("name", "size", "modified")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.heading("name", text="文件名")
    tree.heading("size", text="大小")
    tree.heading("modified", text="修改日期")
    tree.column("name", width=300)
    tree.column("size", width=100)
    tree.column("modified", width=150)

    # 添加滚动条
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # 布局
    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    widget_dict['listbox'] = tree

    # 按钮区域 - 右侧文件操作按钮
    right_buttons_frame = ttk.Frame(right_frame)
    right_buttons_frame.pack(fill="x", pady=10)

    def refresh_list():
        """
        刷新右侧文件列表，显示cases_date目录下的最新文件
        """
        tree.delete(*tree.get_children())
        xlsx_files = get_xlsx_files_in_cases_date()
        for file in xlsx_files:
            file_path = os.path.join(CASES_DATE_DIR, file)
            size = os.path.getsize(file_path)
            modified_time = os.path.getmtime(file_path)
            size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
            modified_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified_time))
            tree.insert("", "end", values=(file, size_str, modified_str))

    def delete_selected_file():
        """
        删除选中的已上传文件
        """
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要删除的文件")
            return

        if messagebox.askyesno("确认", "确定要删除选中的文件吗？"):
            for item in selected_items:
                file_name = tree.item(item)['values'][0]
                file_path = os.path.join(CASES_DATE_DIR, file_name)
                try:
                    os.remove(file_path)
                    tree.delete(item)
                except Exception as e:
                    messagebox.showerror("错误", f"删除文件失败: {e}")

    # 添加刷新按钮
    refresh_button = ttk.Button(right_buttons_frame, text="刷新列表", command=refresh_list, width=15)
    refresh_button.pack(side=tk.LEFT, padx=5)

    # 添加删除按钮
    delete_button = ttk.Button(right_buttons_frame, text="删除", command=delete_selected_file, width=15)
    delete_button.pack(side=tk.LEFT, padx=5)

    # 初始填充右侧列表
    refresh_list()

    return widget_dict

def upload_selected_files(widget_dict):
    """
    上传选中的文件到cases_date目录

    Args:
        widget_dict: 包含控件引用的字典

    Returns:
        list: 成功上传的文件名列表
    """
    selected_files = widget_dict.get('selected_files', [])

    # 验证文件是否选择
    if not selected_files:
        messagebox.showwarning("提示", "请选择至少一个测试用例文件")
        return []

    # 确保cases_date目录存在
    if not os.path.exists(CASES_DATE_DIR):
        os.makedirs(CASES_DATE_DIR, exist_ok=True)

    # 复制所有选中的文件到cases_date目录
    copied_files = []
    for file_path in selected_files:
        file_name = os.path.basename(file_path)
        target_file_path = os.path.join(CASES_DATE_DIR, file_name)
        try:
            shutil.copy2(file_path, target_file_path)
            copied_files.append(file_name)
        except Exception as e:
            messagebox.showerror("错误", f"复制文件时出错: {e}")

    # 如果有文件成功复制，则更新状态
    if copied_files:
        # 更新文件列表显示
        tree = widget_dict['listbox']
        tree.delete(*tree.get_children())
        xlsx_files = get_xlsx_files_in_cases_date()
        for file in xlsx_files:
            file_path = os.path.join(CASES_DATE_DIR, file)
            size = os.path.getsize(file_path)
            modified_time = os.path.getmtime(file_path)
            size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
            modified_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified_time))
            tree.insert("", "end", values=(file, size_str, modified_str))

        messagebox.showinfo("成功", f"已成功上传 {len(copied_files)} 个文件")
    else:
        messagebox.showwarning("提示", "没有文件被上传")

    return copied_files