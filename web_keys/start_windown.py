import tkinter as tk
from tkinter import ttk
import json


def start_windown_config():
    # 创建主窗口对象，这是整个 GUI 应用的基础
    root = tk.Tk()
    # 设置主窗口的标题
    root.title("自动化测试参数信息选择")
    # 设置窗口大小，这里设置宽度为 500 像素，高度为 400 像素
    root.geometry("500x400")

    # 定义一个标志变量，用于记录窗口是否是通过点击 X 号关闭的
    is_closed_by_x = False

    def on_close():
        nonlocal is_closed_by_x
        is_closed_by_x = True
        root.destroy()

    # 绑定窗口关闭事件
    root.protocol("WM_DELETE_WINDOW", on_close)

    # 定义一个函数，用于处理提交操作
    def submit():
        # 获取选择框中当前选中的选项（电脑是 win 还是 mac）
        selected_option = option_var.get()
        # 获取第二个选择框中当前选中的选项（项目是否为 H5）
        selected_option2 = option_var2.get()
        # 获取输入框中用户输入的文本（备注信息）
        input_text = entry.get()
        print(f"选择的选项1: {selected_option}")
        print(f"选择的选项2: {selected_option2}")
        print(f"输入的文本: {input_text}")

        # 创建一个字典，用于存储要保存到配置文件中的数据
        data = {
            "pc_type": selected_option,  # 将电脑类型选项存入字典
            "is_h5": selected_option2,  # 将项目是否为 H5 的选项存入字典
            "note": input_text  # 将输入的备注信息存入字典
        }
        try:
            # 尝试以写入模式打开名为 'config.json' 的文件
            # 如果文件不存在，Python 会自动创建它
            # 文件路径如果只写文件名，默认是在当前运行脚本的工作目录下创建
            with open('/Users/wang/PycharmProjects/AtouTest_Web/config/start_config.json', 'w') as f:
                # 将字典数据以 JSON 格式写入文件
                json.dump(data, f)
            print("信息已成功保存到 config.json 文件中。")
            print("准备关闭窗口。")
            root.destroy()  # 关闭窗口
        except Exception as e:
            # 打印具体的异常信息
            print(f"保存信息到配置文件时出现错误: {e}")

    # ---------------------选项1------------------------------------
    # 创建一个标签，用于提示用户选择一个选项（电脑是 win 还是 mac）
    option_label = tk.Label(root, text="1.电脑是win还是mac:")
    # 使用 pack 布局管理器将标签放置在主窗口中，并在垂直方向上留出 10 像素的间距
    option_label.pack(pady=10)

    # 定义一个列表，包含可供选择的选项
    options = ["win", "mac"]
    # 创建一个字符串变量，用于存储选择框中当前选中的选项
    option_var = tk.StringVar(root)
    # 设置选择框的默认选中选项为列表中的第一个选项
    option_var.set(options[0])
    # 创建一个下拉选择框（Combobox），并将其与 option_var 变量关联
    option_menu = ttk.Combobox(root, textvariable=option_var, values=options)
    # 使用 pack 布局管理器将选择框放置在主窗口中，并在垂直方向上留出 5 像素的间距
    option_menu.pack(pady=5)

    # ---------------------选项2------------------------------------
    # 创建一个标签，用于提示用户选择一个选项（项目是否为 H5）
    option_label2 = tk.Label(root, text="2.项目是否为H5")
    # 使用 pack 布局管理器将标签放置在主窗口中，并在垂直方向上留出 10 像素的间距
    option_label2.pack(pady=10)
    # 定义一个列表，包含可供选择的选项
    options2 = ["yes", "no"]
    # 创建一个字符串变量，用于存储选择框中当前选中的选项
    option_var2 = tk.StringVar(root)
    # 设置选择框的默认选中选项为列表中的第一个选项
    option_var2.set(options2[1])
    # 创建一个下拉选择框（Combobox），并将其与 option_var2 变量关联
    option_menu = ttk.Combobox(root, textvariable=option_var2, values=options2)
    # 使用 pack 布局管理器将选择框放置在主窗口中，并在垂直方向上留出 5 像素的间距
    option_menu.pack(pady=5)

    # ---------------------输入框1------------------------------------
    # 创建一个标签，用于提示用户输入一些文本（备注信息）
    input_label = tk.Label(root, text="输入一些文本备注:")
    # 使用 pack 布局管理器将标签放置在主窗口中，并在垂直方向上留出 10 像素的间距
    input_label.pack(pady=10)

    # 创建一个输入框，用于让用户输入文本
    entry = tk.Entry(root)
    # 使用 pack 布局管理器将输入框放置在主窗口中，并在垂直方向上留出 5 像素的间距
    entry.pack(pady=5)

    # ---------------------提交按钮------------------------------------
    # 创建一个提交按钮，当用户点击该按钮时会调用 submit 函数
    submit_button = tk.Button(root, text="提交", command=submit)
    # 使用 pack 布局管理器将提交按钮放置在主窗口中，并在垂直方向上留出 20 像素的间距
    submit_button.pack(pady=20)

    # 启动主事件循环，等待用户操作
    root.mainloop()

    # 判断窗口是否是通过点击 X 号关闭的
    if is_closed_by_x:
        print("窗口是通过点击X号关闭的")
    else:
        print("窗口不是通过点击X号关闭的,取消运行")

    return is_closed_by_x

# 调用函数
# start_windown_config()