"""
测试用例导入sheet页

该模块提供了一个图形用户界面，用于查看已上传的测试用例文件和目录，包括：
1. 显示已上传的测试用例文件
2. 显示目录结构
3. 导入测试用例功能
"""


import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import shutil
from web_keys.environment_info.montage_url import home
from web_keys.read_excel.run_excel_to_py import run_excel_to_py
import time

# 测试用例文件目录路径
CASES_DATE_DIR = os.path.join(home, 'cases_date')
# 配置文件目录路径
CONFIG_DIR = os.path.join(home, 'config')
# 配置文件路径
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, 'directory_config.jsrunon')
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


def get_directories_in_path(path):
    """
    获取指定路径下的所有目录

    Args:
        path: 目录路径

    Returns:
        list: 目录列表，如果路径不存在返回空列表
    """
    if not os.path.exists(path):
        return []

    try:
        items = os.listdir(path)
        directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
        return sorted(directories)
    except Exception as e:
        print(f"获取目录列表出错: {e}")
        return []


def get_config_path():
    """
    获取配置文件路径

    Returns:
        str: 配置文件路径
    """
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

    return CONFIG_FILE_PATH


def load_directory_config():
    """
    加载目录配置

    Returns:
        str: 配置的目录路径，默认为home目录
    """
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('directory_path', home)
        except Exception as e:
            print(f"加载目录配置出错: {e}")

    return home


def save_directory_config(directory_path):
    """
    保存目录配置

    Args:
        directory_path: 要保存的目录路径
    """
    config_path = get_config_path()
    try:
        with open(config_path, 'w') as f:
            json.dump({'directory_path': directory_path}, f)
        return True
    except Exception as e:
        print(f"保存目录配置出错: {e}")
        return False


def create_test_case_import_sheet(parent_frame, widget_dict):
    """
    创建测试用例导入sheet页

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
    title_label = ttk.Label(main_frame, text="测试用例导入", font=("Arial", 16, "bold"))
    title_label.pack(anchor="center", pady=(0, 20))

    # 创建左右两栏框架
    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill="both", expand=True)

    # 左侧框架：已上传的测试用例文件
    left_frame = ttk.LabelFrame(content_frame, text="已上传的测试用例文件", padding=(10, 5))
    left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))

    # 创建列表框显示已上传的测试用例文件
    files_list_frame = ttk.Frame(left_frame)
    files_list_frame.pack(fill="both", expand=True, pady=5)

    files_scrollbar = ttk.Scrollbar(files_list_frame)
    files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 设置多选模式
    files_listbox = tk.Listbox(files_list_frame, yscrollcommand=files_scrollbar.set, height=15, selectmode=tk.MULTIPLE)
    files_listbox.pack(side=tk.LEFT, fill="both", expand=True)
    files_scrollbar.config(command=files_listbox.yview)

    # 填充列表框，显示当前已有的Excel文件
    xlsx_files = get_xlsx_files_in_cases_date()
    for file in xlsx_files:
        files_listbox.insert(tk.END, file)

    widget_dict['import_files_listbox'] = files_listbox

    # 按钮区域 - 左侧文件操作按钮
    left_buttons_frame = ttk.Frame(left_frame)
    left_buttons_frame.pack(fill="x", pady=10)

    # 添加刷新按钮
    def refresh_files_list():
        """
        刷新文件列表，显示cases_date目录下的最新文件
        """
        files_listbox.delete(0, tk.END)  # 清空列表
        xlsx_files = get_xlsx_files_in_cases_date()  # 重新获取文件列表
        for file in xlsx_files:
            files_listbox.insert(tk.END, file)  # 重新填充列表

    refresh_button = ttk.Button(left_buttons_frame, text="刷新列表", command=refresh_files_list, width=15)
    refresh_button.pack(side=tk.LEFT, padx=5)

    # 导入测试用例按钮
    def import_test_case():
        """
        导入测试用例功能

        该函数实现了从已上传的测试用例文件中选择并导入测试用例的功能：
        1. 获取用户在文件列表中选中的文件索引
        2. 检查是否有选中的文件，如果没有则提示用户
        3. 将选中的文件路径存入selected_files列表
        4. 显示已选择的文件数量（目前仅显示提示信息，实际导入功能待实现）

        后续开发计划：
        - 实现将Excel文件中的测试用例数据解析并导入到系统中
        - 支持批量导入多个测试用例文件
        - 添加导入进度显示
        - 添加导入结果反馈
        """
        # 获取用户在文件列表中选中的索引
        selected_indices = files_listbox.curselection()

        # 检查是否有选中的文件
        if not selected_indices:
            messagebox.showinfo("提示", "请先选择要导入的测试用例文件")
            return

        else:
            # 定义一个变量来接收选中的文件列表
            selected_files = [files_listbox.get(i) for i in selected_indices]
            print(selected_files)
            run_excel_to_py(selected_files)  # 循环运行文件

            # 显示已选择的文件数量（目前仅显示提示信息，实际导入功能待实现）
            messagebox.showinfo("提示", f"已选择 {len(selected_files)} 个文件，导入测试用例功能暂未实现，后续开发")

            # 导入完成后刷新右侧目录树
            refresh_dir_tree()

    import_button = ttk.Button(left_buttons_frame, text="导入测试用例", command=import_test_case, width=15)
    import_button.pack(side=tk.LEFT, padx=5)

    # 右侧框架：目录结构
    right_frame = ttk.LabelFrame(content_frame, text="目录结构", padding=(10, 5))
    right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

    # 创建目录树框架
    dir_tree_frame = ttk.Frame(right_frame)
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

    # 右侧按钮区域
    right_buttons_frame = ttk.Frame(right_frame)
    right_buttons_frame.pack(fill="x", pady=10)

    # 刷新目录树按钮
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

    refresh_dir_button = ttk.Button(right_buttons_frame, text="刷新目录", command=refresh_dir_tree, width=15)
    refresh_dir_button.pack(side=tk.LEFT, padx=5)

    # 删除按钮
    def delete_selected():
        """
        删除选中的文件或目录
        """
        selected_items = dir_tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要删除的项目")
            return

        if messagebox.askyesno("确认", "确定要删除选中的项目吗？"):
            for item in selected_items:
                path = dir_tree.item(item, "values")[0]
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)  # 使用shutil.rmtree递归删除目录
                    else:
                        os.remove(path)
                except Exception as e:
                    messagebox.showerror("错误", f"删除失败: {str(e)}")
            refresh_dir_tree()

    delete_button = ttk.Button(right_buttons_frame, text="删除", command=delete_selected, width=15)
    delete_button.pack(side=tk.LEFT, padx=5)

    return widget_dict 