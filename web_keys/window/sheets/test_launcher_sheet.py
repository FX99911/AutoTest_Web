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
import psutil
import re
import shutil
from web_keys.environment_info.montage_url import home
from run_main import start_run_auto_test

# 测试用例文件目录路径
CASES_DATE_DIR = os.path.join(home, 'cases_date')
# 测试报告目录路径
REPORTS_DIR = os.path.join(home, 'reports')
# 目录树根路径
DIR_TREE_ROOT_PATH = os.path.join(home, 'cases_run')

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

    # 创建左右分割框架
    split_frame = ttk.Frame(main_frame)
    split_frame.pack(fill=tk.BOTH, expand=True)

    # 左侧框架
    left_frame = ttk.Frame(split_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    # 左侧上部：选择测试用例
    select_frame = ttk.LabelFrame(left_frame, text="选择测试用例", padding=(10, 5))
    select_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    # 创建目录树框架
    dir_tree_frame = ttk.Frame(select_frame)
    dir_tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    dir_tree_scrollbar = ttk.Scrollbar(dir_tree_frame)
    dir_tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    dir_tree = ttk.Treeview(dir_tree_frame, yscrollcommand=dir_tree_scrollbar.set)
    dir_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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

        # 如果选择的是文件，取消选择
        if not os.path.isdir(path):
            dir_tree.selection_remove(item)
            messagebox.showwarning("提示", "只能选择目录，不能选择文件")
            return

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

    # 选择按钮区域
    select_buttons_frame = ttk.Frame(select_frame)
    select_buttons_frame.pack(fill=tk.X, pady=5)

    def get_relative_path(full_path):
        """
        获取相对于根目录的路径
        """
        return os.path.relpath(full_path, DIR_TREE_ROOT_PATH)

    def add_to_selected():
        selected_items = dir_tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要添加的目录")
            return

        for item in selected_items:
            path = dir_tree.item(item, "values")[0]
            name = dir_tree.item(item, "text")

            # 检查是否已存在
            exists = False
            for child in selected_tree.get_children():
                if selected_tree.item(child, "values")[0] == path:
                    exists = True
                    break

            if not exists:
                # 获取相对路径
                rel_path = os.path.relpath(path, DIR_TREE_ROOT_PATH)
                parts = rel_path.split(os.sep)

                # 创建完整的目录结构
                current_parent = ""
                for part in parts:
                    # 检查是否已存在
                    exists = False
                    for child in selected_tree.get_children(current_parent):
                        if selected_tree.item(child, "text") == part:
                            current_parent = child
                            exists = True
                            break
                    if not exists:
                        # 创建目录节点
                        full_path = os.path.join(DIR_TREE_ROOT_PATH, *parts[:parts.index(part)+1])
                        current_parent = selected_tree.insert(current_parent, "end", text=part, values=(full_path, "", ""))
                        # 如果目录在展开状态中，则展开
                        if full_path in selected_expanded_items:
                            selected_tree.item(current_parent, open=True)

                # 递归添加目录下的所有.py文件
                def add_directory_contents(dir_path, parent=""):
                    try:
                        items = os.listdir(dir_path)
                        for item in items:
                            full_path = os.path.join(dir_path, item)
                            if os.path.isdir(full_path):
                                # 检查子目录是否已存在
                                exists = False
                                for child in selected_tree.get_children(parent):
                                    if selected_tree.item(child, "text") == item:
                                        exists = True
                                        break
                                if not exists:
                                    # 创建子目录节点
                                    sub_node_id = selected_tree.insert(parent, "end", text=item, values=(full_path, "", ""))
                                    add_directory_contents(full_path, sub_node_id)
                                    # 如果目录在展开状态中，则展开
                                    if full_path in selected_expanded_items:
                                        selected_tree.item(sub_node_id, open=True)
                            elif item.endswith('.py'):
                                # 检查文件是否已存在
                                exists = False
                                for child in selected_tree.get_children(parent):
                                    if selected_tree.item(child, "text") == item:
                                        exists = True
                                        break
                                if not exists:
                                    # 获取文件大小和修改时间
                                    size = os.path.getsize(full_path)
                                    modified_time = os.path.getmtime(full_path)
                                    modified_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified_time))
                                    size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
                                    selected_tree.insert(parent, "end", text=item, values=(full_path, size_str, modified_str))
                    except Exception as e:
                        print(f"添加目录内容出错: {e}")

                add_directory_contents(path, current_parent)

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

    add_button = ttk.Button(select_buttons_frame, text="添加到已选择", command=add_to_selected, width=15)
    add_button.pack(side=tk.LEFT, padx=5)

    refresh_button = ttk.Button(select_buttons_frame, text="刷新目录", command=refresh_dir_tree, width=15)
    refresh_button.pack(side=tk.LEFT, padx=5)

    # 左侧下部：已选择的测试用例
    selected_frame = ttk.LabelFrame(left_frame, text="已选择的测试用例", padding=(10, 5))
    selected_frame.pack(fill=tk.BOTH, expand=True)

    # 已选择目录树框架
    selected_tree_frame = ttk.Frame(selected_frame)
    selected_tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    selected_tree_scrollbar = ttk.Scrollbar(selected_tree_frame)
    selected_tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    selected_tree = ttk.Treeview(selected_tree_frame, yscrollcommand=selected_tree_scrollbar.set)
    selected_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    selected_tree_scrollbar.config(command=selected_tree.yview)

    # 配置已选择目录树
    selected_tree["columns"] = ("path", "size", "modified")
    selected_tree.column("#0", width=300, minwidth=200)
    selected_tree.column("path", width=0, stretch=tk.NO)
    selected_tree.column("size", width=100)
    selected_tree.column("modified", width=150)
    selected_tree.heading("#0", text="名称")
    selected_tree.heading("path", text="路径")
    selected_tree.heading("size", text="大小")
    selected_tree.heading("modified", text="修改日期")

    # 设置已选择目录树样式
    style.configure("Selected.Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
    style.configure("Selected.Treeview.Heading", background="#3c3f41", foreground="white")
    style.map("Selected.Treeview", background=[("selected", "#4a6ea9")])
    selected_tree.configure(style="Selected.Treeview")

    # 存储已选择目录树的展开状态
    selected_expanded_items = set()

    # 已选择目录树展开/折叠事件
    def on_selected_tree_expand(event):
        item = selected_tree.focus()
        path = selected_tree.item(item, "values")[0]
        selected_expanded_items.add(path)

    def on_selected_tree_collapse(event):
        item = selected_tree.focus()
        path = selected_tree.item(item, "values")[0]
        selected_expanded_items.discard(path)

    selected_tree.bind("<<TreeviewOpen>>", on_selected_tree_expand)
    selected_tree.bind("<<TreeviewClose>>", on_selected_tree_collapse)

    # 已选择目录树按钮区域
    selected_buttons_frame = ttk.Frame(selected_frame)
    selected_buttons_frame.pack(fill=tk.X, pady=5)

    def remove_selected():
        selected_items = selected_tree.selection()
        for item in selected_items:
            selected_tree.delete(item)

    def show_temporary_message(message, duration=3000):
        """
        显示临时消息，自动消失
        """
        message_window = tk.Toplevel()
        message_window.title("提示")
        message_window.geometry("300x100")
        message_window.attributes('-topmost', True)

        # 设置窗口样式
        style = ttk.Style()
        style.configure("Message.TLabel", font=("Arial", 12))

        # 显示消息
        ttk.Label(
            message_window,
            text=message,
            style="Message.TLabel"
        ).pack(expand=True)

        # 设置定时关闭
        message_window.after(duration, message_window.destroy)

    def confirm_selection():
        """
        确认选择并输出已选择的项目列表
        """
        selected_items = []

        def collect_items(item_id, parent_path=""):
            # 获取项目信息
            item_text = selected_tree.item(item_id, "text")
            item_values = selected_tree.item(item_id, "values")
            item_path = item_values[0]

            # 构建完整路径
            if parent_path:
                full_path = os.path.join(parent_path, item_text)
            else:
                full_path = item_text

            # 如果是目录且不是__pycache__，添加到选中列表
            if os.path.isdir(item_path) and not item_text.startswith("__pycache__"):
                selected_items.append({
                    "type": "directory",
                    "name": item_text,
                    "path": item_path,
                    "full_path": full_path,
                    "depth": len(os.path.relpath(item_path, DIR_TREE_ROOT_PATH).split(os.sep))
                })

            # 递归检查子节点
            for child_id in selected_tree.get_children(item_id):
                collect_items(child_id, full_path)

        # 收集所有项目
        for item_id in selected_tree.get_children():
            collect_items(item_id)

        # 检查是否选择了测试用例
        if not selected_items:
            messagebox.showwarning("警告", "请选择测试用例")
            return

        # 构建输出列表
        output_list = []

        # 找出最深的目录层级
        max_depth = max(item["depth"] for item in selected_items)

        # 只输出最深的目录
        for item in selected_items:
            if item["depth"] == max_depth:
                rel_path = os.path.relpath(item["path"], DIR_TREE_ROOT_PATH)
                full_path = os.path.join("cases_run", rel_path)
                output_list.append(full_path)

        # 输出已选择的项目列表
        print("\n已选择的项目列表：")
        print(output_list)

        # 将路径写入pytest.ini
        try:
            # 使用home变量获取项目根目录
            pytest_ini_path = os.path.join(home, "pytest.ini")

            # 读取pytest.ini文件
            with open(pytest_ini_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # 查找testpaths行
            testpaths_index = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("testpaths"):
                    testpaths_index = i
                    break

            # 构建新的testpaths行
            testpaths_line = f"testpaths = {' '.join(output_list)}\n"

            # 如果找到testpaths行，替换它；否则添加到文件末尾
            if testpaths_index != -1:
                lines[testpaths_index] = testpaths_line
            else:
                lines.append("\n" + testpaths_line)

            # 写入pytest.ini文件
            with open(pytest_ini_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            print("\n已更新pytest.ini文件")
            messagebox.showinfo("成功", "测试用例选择已成功保存！")
        except Exception as e:
            print(f"\n更新pytest.ini文件时出错: {e}")
            messagebox.showerror("错误", f"保存测试用例选择时出错：{str(e)}")

        return output_list

    remove_button = ttk.Button(selected_buttons_frame, text="取消选择", command=remove_selected, width=15)
    remove_button.pack(side=tk.LEFT, padx=5)

    confirm_button = ttk.Button(selected_buttons_frame, text="确定", command=confirm_selection, width=15)
    confirm_button.pack(side=tk.LEFT, padx=5)

    # 右侧框架
    right_frame = ttk.Frame(split_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # 创建参数配置区域
    param_frame = ttk.LabelFrame(right_frame, text="测试参数配置", padding=(10, 5))
    param_frame.pack(fill=tk.X, pady=(0, 15))

    # 添加参数配置选项
    options_frame = ttk.Frame(param_frame)
    options_frame.pack(fill=tk.X, pady=5)

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

    # 添加提交按钮区域
    submit_frame = ttk.Frame(right_frame)
    submit_frame.pack(fill=tk.X, pady=20)

    # 添加日志显示区域
    log_frame = ttk.LabelFrame(right_frame, text="执行日志", padding=(10, 5))
    log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    # 创建日志文本框
    log_text = tk.Text(log_frame, wrap=tk.WORD, height=15)
    log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # 添加滚动条
    log_scrollbar = ttk.Scrollbar(log_text)
    log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_text.config(yscrollcommand=log_scrollbar.set)
    log_scrollbar.config(command=log_text.yview)

    # 设置日志文本框样式
    log_text.config(bg="#2b2b2b", fg="white", font=("Consolas", 10))

    # 用于存储当前运行的进程
    current_process = None

    def cleanup_browser_cache():
        """
        清理浏览器缓存
        """
        try:
            # 清理Chrome缓存目录
            cache_paths = [
                os.path.expanduser("~/Library/Caches/Google/Chrome"),
                os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Cache"),
                os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Code Cache")
            ]

            for path in cache_paths:
                if os.path.exists(path):
                    shutil.rmtree(path)
                    print(f"已清理缓存目录: {path}")
        except Exception as e:
            print(f"清理缓存时出错: {str(e)}")

    def cleanup_chromedriver():
        """
        清理所有chromedriver进程
        """
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'chromedriver' in proc.info['name'].lower():
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def show_test_results():
        """
        显示测试结果统计窗口
        """
        # 解析日志获取测试结果
        log_content = log_text.get(1.0, tk.END)

        # 查找测试结果统计行
        result_line = None
        for line in log_content.split('\n'):
            if 'passed' in line.lower() and 'in' in line:
                result_line = line
                break

        if result_line:
            # 解析结果行
            passed = 0
            failed = 0
            error = 0
            skipped = 0

            # 使用正则表达式提取数字
            import re
            passed_match = re.search(r'(\d+)\s+passed', result_line)
            failed_match = re.search(r'(\d+)\s+failed', result_line)
            error_match = re.search(r'(\d+)\s+error', result_line)
            skipped_match = re.search(r'(\d+)\s+skipped', result_line)

            if passed_match:
                passed = int(passed_match.group(1))
            if failed_match:
                failed = int(failed_match.group(1))
            if error_match:
                error = int(error_match.group(1))
            if skipped_match:
                skipped = int(skipped_match.group(1))

            # 构建结果消息
            result_message = f"测试执行完成！\n\n"
            result_message += f"成功: {passed} 条\n"
            result_message += f"失败: {failed} 条\n"
            result_message += f"错误: {error} 条\n"
            if skipped > 0:
                result_message += f"跳过: {skipped} 条\n"

            # 获取最新的测试报告路径
            reports_dir = os.path.join(home, 'reports')
            latest_report = None
            latest_time = 0

            # 查找最新的HTML报告
            for root, dirs, files in os.walk(reports_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        file_time = os.path.getmtime(file_path)
                        if file_time > latest_time:
                            latest_time = file_time
                            latest_report = file_path

            if latest_report:
                def open_report():
                    try:
                        import webbrowser
                        # 使用绝对路径打开报告
                        report_url = f"file://{os.path.abspath(latest_report)}"
                        print(f"正在打开报告: {report_url}")  # 调试信息
                        webbrowser.open(report_url)
                    except Exception as e:
                        print(f"打开报告失败: {str(e)}")  # 调试信息
                        messagebox.showerror("错误", f"打开报告失败: {str(e)}")

                # 显示结果并询问是否查看报告
                if messagebox.askyesno("测试执行完成", result_message + "\n是否查看测试报告？"):
                    open_report()
            else:
                messagebox.showinfo("测试执行完成", result_message + "\n未找到测试报告文件。")

    def start_execution():
        """
        开始执行测试
        """
        # 清空日志
        log_text.delete(1.0, tk.END)

        # 启动测试进程
        def run_test():
            global current_process
            try:
                # 使用subprocess.Popen启动start_run_auto_test
                current_process = subprocess.Popen(
                    ["python", "-c", "from run_main import start_run_auto_test; start_run_auto_test()"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                # 实时读取输出
                for line in current_process.stdout:
                    # 在主线程中更新UI
                    log_text.after(0, lambda l=line: update_log(l))
                    log_text.see(tk.END)

                # 等待进程结束
                current_process.wait()

                # 清理浏览器缓存和chromedriver进程
                cleanup_browser_cache()
                cleanup_chromedriver()

                # 显示测试结果
                log_text.after(0, show_test_results)

                # 更新按钮状态
                submit_button.config(state=tk.NORMAL)
                stop_button.config(state=tk.DISABLED)

            except Exception as e:
                log_text.insert(tk.END, f"执行出错: {str(e)}\n")
                log_text.see(tk.END)
                submit_button.config(state=tk.NORMAL)
                stop_button.config(state=tk.DISABLED)

        def update_log(line):
            log_text.insert(tk.END, line)
            log_text.see(tk.END)

        # 禁用开始按钮，启用停止按钮
        submit_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

        # 在新线程中运行测试
        threading.Thread(target=run_test, daemon=True).start()

    def stop_execution():
        """
        停止执行测试
        """
        global current_process
        if current_process:
            try:
                current_process.terminate()
                log_text.insert(tk.END, "\n测试执行已停止\n")
                log_text.see(tk.END)

                # 清理浏览器缓存和chromedriver进程
                cleanup_browser_cache()
                cleanup_chromedriver()

                # 显示停止成功提示
                messagebox.showinfo("提示", "测试执行已停止")

            except Exception as e:
                log_text.insert(tk.END, f"停止执行时出错: {str(e)}\n")
                log_text.see(tk.END)
            finally:
                current_process = None
                submit_button.config(state=tk.NORMAL)
                stop_button.config(state=tk.DISABLED)

    # 执行按钮
    submit_button = ttk.Button(
        submit_frame,
        text="开始执行",
        command=start_execution,
        style="Accent.TButton",
        width=15
    )
    submit_button.pack(side=tk.LEFT, padx=10)

    # 停止按钮
    stop_button = ttk.Button(
        submit_frame,
        text="停止执行",
        command=stop_execution,
        style="Accent.TButton",
        width=15,
        state=tk.DISABLED
    )
    stop_button.pack(side=tk.LEFT, padx=10)

    return widget_dict