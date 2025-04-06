"""
自动化测试配置窗口模块

该模块提供了一个图形用户界面，用于设置自动化测试的各项配置，包括：
1. 选择电脑类型（Windows/Mac）
2. 指定项目是否为H5项目
3. 添加备注信息
4. 上传和管理测试用例文件

配置完成后，相关设置将保存到配置文件中，并将测试用例文件复制到指定目录。
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
from web_keys.environment_info.montage_url import home


def get_start_config_url():
    """
    获取配置文件的路径

    Returns:
        str: 配置文件的完整路径
    """
    return f'{home}/config/start_config.json'


def get_xlsx_files_in_cases_date():
    """
    获取cases_date目录下所有的xlsx文件

    Returns:
        list: xlsx文件列表，如果目录不存在会先创建
    """
    cases_date_dir = os.path.join(home, 'cases_date')
    if not os.path.exists(cases_date_dir):
        os.makedirs(cases_date_dir, exist_ok=True)
        return []

    files = os.listdir(cases_date_dir)
    xlsx_files = [f for f in files if f.lower().endswith('.xlsx')]
    return xlsx_files


def create_widgets(root, options, options2, is_closed_by_x):
    """
    创建并布局窗口中的各种控件

    Args:
        root: 主窗口对象
        options: 第一个选择框的选项列表 (pc_type)
        options2: 第二个选择框的选项列表 (is_h5)
        is_closed_by_x: 窗口关闭方式的标志变量

    Returns:
        dict: 包含控件引用和状态变量的字典
    """
    widget_dict = {}

    # 创建主框架
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建标题
    title_label = ttk.Label(main_frame, text="自动化测试配置", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

    # 创建左侧和右侧框架
    left_frame = ttk.Frame(main_frame)
    left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

    right_frame = ttk.Frame(main_frame)
    right_frame.grid(row=1, column=1, sticky="nsew")

    # 设置列权重，使左右两栏能够平均分配空间
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    # 左侧框架：配置选项
    # 第一个选择框相关 - 电脑类型
    option_label = ttk.Label(left_frame, text="1. 电脑类型:")
    option_label.pack(anchor="w", pady=(0, 5))
    option_var = tk.StringVar(root)
    option_var.set(options[0])  # 默认选择第一项
    option_menu = ttk.Combobox(left_frame, textvariable=option_var, values=options, width=30, state="readonly")
    option_menu.pack(anchor="w", pady=(0, 15))
    widget_dict['option_var'] = option_var

    # 第二个选择框相关 - 项目是否为H5
    option_label2 = ttk.Label(left_frame, text="2. 项目是否为H5:")
    option_label2.pack(anchor="w", pady=(0, 5))
    option_var2 = tk.StringVar(root)
    option_var2.set(options2[1])  # 默认选择第二项
    option_menu2 = ttk.Combobox(left_frame, textvariable=option_var2, values=options2, width=30, state="readonly")
    option_menu2.pack(anchor="w", pady=(0, 15))
    widget_dict['option_var2'] = option_var2

    # 输入框相关 - 备注信息
    input_label = ttk.Label(left_frame, text="3. 备注信息:")
    input_label.pack(anchor="w", pady=(0, 5))
    entry = ttk.Entry(left_frame, width=30)
    entry.pack(anchor="w", pady=(0, 15))
    widget_dict['entry'] = entry

    # 文件选择区域 - 上传测试用例文件
    file_frame = ttk.LabelFrame(left_frame, text="上传测试用例文件", padding=(10, 5))
    file_frame.pack(fill="x", pady=(0, 15))

    # 创建列表框显示已选择的文件
    files_list_frame = ttk.Frame(file_frame)
    files_list_frame.pack(fill="x", expand=True, pady=5)

    files_scrollbar = ttk.Scrollbar(files_list_frame)
    files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    files_listbox = tk.Listbox(files_list_frame, yscrollcommand=files_scrollbar.set, height=3)
    files_listbox.pack(side=tk.LEFT, fill="x", expand=True)
    files_scrollbar.config(command=files_listbox.yview)

    widget_dict['selected_files'] = []  # 存储选择的文件路径列表

    # 按钮区域 - 文件操作按钮
    file_buttons_frame = ttk.Frame(file_frame)
    file_buttons_frame.pack(fill="x", pady=5)

    def upload_files():
        """
        处理多文件上传功能，追加而不是替换已选择的文件
        """
        file_paths = filedialog.askopenfilenames(
            title="选择测试用例文件(可多选)",
            filetypes=[("Excel文件", "*.xlsx")]
        )
        if file_paths:
            # 添加新选择的文件（不清空之前的选择）
            for file_path in file_paths:
                # 验证文件格式
                if not file_path.lower().endswith('.xlsx'):
                    messagebox.showerror("格式错误", f"{os.path.basename(file_path)}: 只能上传Excel(.xlsx)格式的文件")
                    continue

                # 检查是否已经添加过相同的文件
                if file_path in widget_dict['selected_files']:
                    messagebox.showinfo("提示", f"文件 {os.path.basename(file_path)} 已在列表中")
                    continue

                # 添加到文件列表
                widget_dict['selected_files'].append(file_path)
                files_listbox.insert(tk.END, os.path.basename(file_path))
                print(f"选择的测试用例文件: {file_path}")

            # 更新第一个文件作为主文件（如果还没有设置）
            if widget_dict['selected_files'] and not widget_dict.get('test_case_file'):
                widget_dict['test_case_file'] = widget_dict['selected_files'][0]
        else:
            print("未选择文件")

    def clear_selected_files():
        """
        清空已选择的文件列表
        """
        files_listbox.delete(0, tk.END)
        widget_dict['selected_files'] = []
        if 'test_case_file' in widget_dict:
            del widget_dict['test_case_file']
        print("已清空选择的文件")

    def remove_selected_file():
        """
        从已选择列表中移除选中的文件
        """
        selected_indices = files_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("提示", "请先选择要移除的文件")
            return

        selected_index = selected_indices[0]
        file_path = widget_dict['selected_files'][selected_index]
        file_name = os.path.basename(file_path)

        # 从列表和数据中移除
        files_listbox.delete(selected_index)
        widget_dict['selected_files'].pop(selected_index)

        # 如果删除的是主文件，需要更新主文件引用
        if widget_dict.get('test_case_file') == file_path:
            if widget_dict['selected_files']:
                widget_dict['test_case_file'] = widget_dict['selected_files'][0]
            else:
                if 'test_case_file' in widget_dict:
                    del widget_dict['test_case_file']

        print(f"已移除文件: {file_name}")

    # 添加文件操作按钮
    upload_button = ttk.Button(file_buttons_frame, text="选择文件(可多选)", command=upload_files)
    upload_button.pack(side=tk.LEFT, padx=5)

    remove_button = ttk.Button(file_buttons_frame, text="移除选中", command=remove_selected_file)
    remove_button.pack(side=tk.LEFT, padx=5)

    clear_button = ttk.Button(file_buttons_frame, text="清空选择", command=clear_selected_files)
    clear_button.pack(side=tk.LEFT, padx=5)

    # 右侧框架：显示cases_date目录下的xlsx文件列表
    files_label = ttk.Label(right_frame, text="已上传的测试用例文件:")
    files_label.pack(anchor="w", pady=(0, 5))

    # 创建一个框架来包含列表和滚动条
    list_frame = ttk.Frame(right_frame)
    list_frame.pack(fill="both", expand=True)

    # 创建滚动条
    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建列表框显示已上传的文件
    xlsx_files = get_xlsx_files_in_cases_date()
    listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
    listbox.pack(side=tk.LEFT, fill="both", expand=True)

    # 配置滚动条
    scrollbar.config(command=listbox.yview)

    # 填充列表框，显示当前已有的Excel文件
    for file in xlsx_files:
        listbox.insert(tk.END, file)

    widget_dict['listbox'] = listbox

    # 添加刷新按钮 - 更新右侧已上传文件列表
    def refresh_list():
        """
        刷新右侧文件列表，显示cases_date目录下的最新文件
        """
        listbox.delete(0, tk.END)  # 清空列表
        xlsx_files = get_xlsx_files_in_cases_date()  # 重新获取文件列表
        for file in xlsx_files:
            listbox.insert(tk.END, file)  # 重新填充列表

    refresh_button = ttk.Button(right_frame, text="刷新列表", command=refresh_list)
    refresh_button.pack(pady=10)

    # 右侧添加删除按钮 - 删除已上传的文件
    def delete_selected_file():
        """
        删除选中的已上传文件
        """
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("提示", "请先选择要删除的文件")
            return

        selected_index = selected_indices[0]
        file_name = listbox.get(selected_index)
        file_path = os.path.join(home, 'cases_date', file_name)

        try:
            os.remove(file_path)  # 删除文件
            listbox.delete(selected_index)  # 从列表中移除
            messagebox.showinfo("成功", f"文件 {file_name} 已删除")
        except Exception as e:
            messagebox.showerror("错误", f"删除文件失败: {e}")

    delete_button = ttk.Button(right_frame, text="删除选中文件", command=delete_selected_file)
    delete_button.pack(pady=5)

    # 按钮区域 - 提交和取消按钮
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=20)

    # 提交按钮 - 保存配置并上传文件
    submit_button = ttk.Button(
        button_frame,
        text="提交",
        command=lambda: submit(widget_dict, get_start_config_url(), root, is_closed_by_x),
        style="Accent.TButton",
        width=15
    )
    submit_button.pack(side=tk.LEFT, padx=10)

    # 取消按钮 - 关闭窗口不保存设置
    cancel_button = ttk.Button(
        button_frame,
        text="取消",
        command=lambda: on_close(root, is_closed_by_x),
        width=15
    )
    cancel_button.pack(side=tk.LEFT, padx=10)

    # 状态栏 - 显示操作状态
    status_frame = ttk.Frame(root)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    status_label = ttk.Label(status_frame, text="准备就绪", relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(fill=tk.X)
    widget_dict['status_label'] = status_label

    return widget_dict


def submit(widget_dict, start_config_url, root, is_closed_by_x):
    """
    处理提交按钮的点击事件，保存配置和上传文件

    Args:
        widget_dict: 包含控件引用和状态变量的字典
        start_config_url: 配置文件的路径
        root: 主窗口对象
        is_closed_by_x: 窗口关闭方式的标志变量
    """
    # 获取用户选择的配置
    selected_option = widget_dict['option_var'].get()
    selected_option2 = widget_dict['option_var2'].get()
    input_text = widget_dict['entry'].get()
    selected_files = widget_dict.get('selected_files', [])

    # 更新状态栏
    widget_dict['status_label'].config(text="正在处理...")

    # 打印选择的配置信息
    print(f"pc还是mac: {selected_option}")
    print(f"是否H5: {selected_option2}")
    print(f"输入的文本: {input_text}")
    print(f"选择的测试用例文件数量: {len(selected_files)}")

    # 验证文件是否选择
    if not selected_files:
        messagebox.showwarning("提示", "请选择至少一个测试用例文件")
        widget_dict['status_label'].config(text="请选择测试用例文件")
        return

    # 确保cases_date目录存在
    cases_date_dir = os.path.join(home, 'cases_date')
    os.makedirs(cases_date_dir, exist_ok=True)

    # 复制所有选中的文件到cases_date目录
    copied_files = []
    for file_path in selected_files:
        # 获取文件名
        file_name = os.path.basename(file_path)
        # 构建目标文件路径
        target_file_path = os.path.join(cases_date_dir, file_name)
        try:
            # 复制文件
            shutil.copy2(file_path, target_file_path)
            copied_files.append(file_name)
            print(f"文件已成功复制到: {target_file_path}")
        except Exception as e:
            error_msg = f"复制文件时出错: {e}"
            print(error_msg)
            messagebox.showerror("错误", error_msg)
            widget_dict['status_label'].config(text="部分文件复制失败")

    # 如果有文件成功复制，则更新状态
    if copied_files:
        widget_dict['status_label'].config(text=f"已复制 {len(copied_files)} 个文件")

        # 更新文件列表显示
        listbox = widget_dict['listbox']
        listbox.delete(0, tk.END)
        xlsx_files = get_xlsx_files_in_cases_date()
        for file in xlsx_files:
            listbox.insert(tk.END, file)
    else:
        widget_dict['status_label'].config(text="没有文件被复制")
        return

    # 准备保存到配置文件的数据
    # 不将文件路径保存到配置文件，只保存其他配置信息
    data = {
        "pc_type": selected_option,
        "is_h5": selected_option2,
        "note": input_text
    }

    # 确保配置目录存在
    config_dir = os.path.dirname(start_config_url)
    os.makedirs(config_dir, exist_ok=True)

    # 保存配置到JSON文件
    try:
        with open(start_config_url, 'w') as f:
            json.dump(data, f)
        print("信息已成功保存到 config.json 文件中。")
        widget_dict['status_label'].config(text="配置已保存")
        messagebox.showinfo("成功", f"已成功上传 {len(copied_files)} 个文件，并保存配置信息")
        is_closed_by_x[0] = False  # 标记为正常关闭（通过提交）
        root.destroy()  # 关闭窗口
    except Exception as e:
        error_msg = f"保存信息到配置文件时出现错误: {e}"
        print(error_msg)
        messagebox.showerror("错误", error_msg)
        widget_dict['status_label'].config(text="配置保存失败")


def on_close(root, is_closed_by_x):
    """
    处理窗口关闭事件

    Args:
        root: 主窗口对象
        is_closed_by_x: 用于记录窗口关闭方式的标志变量
    """
    if messagebox.askokcancel("退出", "确定要取消配置并退出吗？"):
        is_closed_by_x[0] = True  # 标记为取消关闭
        root.destroy()  # 关闭窗口


def start_windown_config():
    """
    创建并显示配置窗口

    Returns:
        bool: 窗口是否被取消关闭的标志，True表示取消关闭
    """
    # 创建主窗口
    root = tk.Tk()
    root.title("自动化测试配置")
    root.geometry("800x600")  # 设置窗口初始大小

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

    # 定义下拉选项
    options = ["win", "mac"]  # 电脑类型选项
    options2 = ["yes", "no"]  # 是否H5选项

    # 创建窗口控件
    widget_dict = create_widgets(root, options, options2, is_closed_by_x)

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
    start_windown_config()
