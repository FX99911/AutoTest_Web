import os
import tkinter as tk
from tkinter import ttk
import webbrowser
from web_keys.environment_info.montage_url import home


def create_report_sheet(parent):
    """创建测试报告页面"""
    frame = ttk.Frame(parent)

    # 创建表格
    tree = ttk.Treeview(frame, columns=("序号", "执行日期", "报告链接", "操作"), show="headings")
    tree.heading("序号", text="序号")
    tree.heading("执行日期", text="执行日期")
    tree.heading("报告链接", text="报告链接")
    tree.heading("操作", text="操作")

    # 设置列宽
    tree.column("序号", width=50, anchor="center")
    tree.column("执行日期", width=150, anchor="center")
    tree.column("报告链接", width=300, anchor="w")
    tree.column("操作", width=150, anchor="center")

    # 添加滚动条
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # 布局
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # 设置网格权重
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # 创建底部按钮框架
    bottom_frame = ttk.Frame(frame)
    bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

    # 左侧分页控件
    pagination_frame = ttk.Frame(bottom_frame)
    pagination_frame.pack(side="left", padx=5)

    # 上一页按钮
    prev_button = ttk.Button(pagination_frame, text="上一页")
    prev_button.pack(side="left", padx=5)

    # 页码标签
    page_label = ttk.Label(pagination_frame, text="")
    page_label.pack(side="left", padx=5)

    # 下一页按钮
    next_button = ttk.Button(pagination_frame, text="下一页")
    next_button.pack(side="left", padx=5)

    # 右侧操作按钮
    button_frame = ttk.Frame(bottom_frame)
    button_frame.pack(side="right", padx=5)

    # 刷新按钮
    refresh_button = ttk.Button(button_frame, text="刷新")
    refresh_button.pack(side="left", padx=5)

    # 加载报告数据
    reports_dir = os.path.join(home, "reports_record")
    reports_data = []
    current_page = 1
    page_size = 10

    def load_reports():
        nonlocal reports_data
        reports_data = []
        if os.path.exists(reports_dir):
            for dir_name in os.listdir(reports_dir):
                dir_path = os.path.join(reports_dir, dir_name)
                if os.path.isdir(dir_path):
                    report_path = os.path.join(dir_path, "index.html")
                    if os.path.exists(report_path):
                        reports_data.append({
                            "date": dir_name,
                            "path": report_path
                        })

        # 按日期降序排序
        reports_data.sort(key=lambda x: x["date"], reverse=True)
        show_page(1)

    def show_page(page):
        nonlocal current_page
        current_page = page
        tree.delete(*tree.get_children())

        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(reports_data))

        for i, report in enumerate(reports_data[start_idx:end_idx], start=start_idx + 1):
            report_url = f"file://{os.path.abspath(report['path'])}"
            tree.insert("", "end", values=(
                i,
                report["date"],
                report_url,
                "查看 | 删除"
            ))

        update_pagination()

    def update_pagination():
        total_pages = (len(reports_data) + page_size - 1) // page_size
        page_label.config(text=f"第 {current_page} 页 / 共 {total_pages} 页")

        prev_button.config(state="normal" if current_page > 1 else "disabled")
        next_button.config(state="normal" if current_page < total_pages else "disabled")

    def prev_page():
        if current_page > 1:
            show_page(current_page - 1)

    def next_page():
        total_pages = (len(reports_data) + page_size - 1) // page_size
        if current_page < total_pages:
            show_page(current_page + 1)

    def delete_report(report_path):
        try:
            # 删除报告目录
            report_dir = os.path.dirname(report_path)
            if os.path.exists(report_dir):
                import shutil
                shutil.rmtree(report_dir)
                load_reports()  # 重新加载数据
                # tk.messagebox.showinfo("成功", "报告已删除")
        except Exception as e:
            tk.messagebox.showerror("错误", f"删除报告失败: {str(e)}")

    def on_click(event):
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            column = tree.identify_column(event.x)
            item = tree.identify_row(event.y)
            values = tree.item(item, "values")

            if column == "#4":  # 操作列
                idx = int(values[0]) - 1
                report = reports_data[idx]
                x = event.x - tree.bbox(item, column)[0]  # 获取点击位置相对于单元格的x坐标

                if x < 50:  # 点击"查看"
                    try:
                        report_url = f"file://{os.path.abspath(report['path'])}"
                        webbrowser.open(report_url)
                    except Exception as e:
                        tk.messagebox.showerror("错误", f"打开报告失败: {str(e)}")
                else:  # 点击"删除"
                    if tk.messagebox.askyesno("确认", "确定要删除此报告吗？"):
                         delete_report(report['path'])

    # 绑定事件
    tree.bind("<Button-1>", on_click)
    prev_button.config(command=prev_page)
    next_button.config(command=next_page)
    refresh_button.config(command=load_reports)

    # 加载数据
    load_reports()

    return frame