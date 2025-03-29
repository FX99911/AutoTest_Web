import tkinter as tk
from tkinter import ttk, filedialog
import json
from web_keys.montage_url import home


def get_start_config_url():
    """
    获取配置文件的路径
    :return: 配置文件的完整路径
    """
    return f'{home}/config/start_config.json'


def create_widgets(root, options, options2):
    """
    创建并布局窗口中的各种控件
    :param root: 主窗口对象
    :param options: 第一个选择框的选项列表
    :param options2: 第二个选择框的选项列表
    :return: 包含选项变量、输入框对象的字典
    """
    widget_dict = {}

    # 第一个选择框相关
    option_label = tk.Label(root, text="1.电脑是win还是mac:")
    option_label.pack(pady=10)
    option_var = tk.StringVar(root)
    option_var.set(options[0])
    option_menu = ttk.Combobox(root, textvariable=option_var, values=options)
    option_menu.pack(pady=5)
    widget_dict['option_var'] = option_var

    # 第二个选择框相关
    option_label2 = tk.Label(root, text="2.项目是否为H5")
    option_label2.pack(pady=10)
    option_var2 = tk.StringVar(root)
    option_var2.set(options2[1])
    option_menu = ttk.Combobox(root, textvariable=option_var2, values=options2)
    option_menu.pack(pady=5)
    widget_dict['option_var2'] = option_var2

    # 输入框相关
    input_label = tk.Label(root, text="输入一些文本备注:")
    input_label.pack(pady=10)
    entry = tk.Entry(root)
    entry.pack(pady=5)
    widget_dict['entry'] = entry

    # 上传文件按钮相关
    file_label = tk.Label(root, text="")  # 创建一个空标签用于显示文件路径

    def upload_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            widget_dict['test_case_file'] = file_path
            print(f"选择的测试用例文件: {file_path}")
            file_label.config(text=file_path)  # 更新标签文本为文件路径
        else:
            print("未选择文件")
            file_label.config(text="")  # 若未选择文件，清空标签文本

    upload_button = tk.Button(root, text="请上传测试用例", command=upload_file)
    upload_button.pack(pady=20)
    file_label.pack(pady=5)  # 将标签放置在按钮下方

    return widget_dict


def submit(widget_dict, start_config_url):
    """
    处理提交按钮的点击事件
    :param widget_dict: 包含选项变量和输入框对象的字典
    :param start_config_url: 配置文件的路径
    """
    selected_option = widget_dict['option_var'].get()
    selected_option2 = widget_dict['option_var2'].get()
    input_text = widget_dict['entry'].get()
    test_case_file = widget_dict.get('test_case_file', '')
    print(f"pc还是mac: {selected_option}")
    print(f"是否H5: {selected_option2}")
    print(f"输入的文本: {input_text}")
    print(f"选择的测试用例文件: {test_case_file}")

    data = {
        "pc_type": selected_option,
        "is_h5": selected_option2,
        "note": input_text,
        "test_case_file": test_case_file
    }
    try:
        with open(start_config_url, 'w') as f:
            json.dump(data, f)
        print("信息已成功保存到 config.json 文件中。")
    except Exception as e:
        print(f"保存信息到配置文件时出现错误: {e}")


def on_close(root, is_closed_by_x):
    """
    处理窗口关闭事件
    :param root: 主窗口对象
    :param is_closed_by_x: 用于记录窗口关闭方式的标志变量
    """
    is_closed_by_x[0] = True
    root.destroy()


def start_windown_config():
    root = tk.Tk()
    root.title("自动化测试参数信息选择")
    root.geometry("500x400")

    is_closed_by_x = [False]
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, is_closed_by_x))

    options = ["win", "mac"]
    options2 = ["yes", "no"]
    widget_dict = create_widgets(root, options, options2)

    submit_button = tk.Button(root, text="提交", command=lambda: submit(widget_dict, get_start_config_url()))
    submit_button.pack(pady=20)

    root.mainloop()

    if is_closed_by_x[0]:
        print("窗口点击X号关闭,取消提交")
    else:
        print("窗口点击了提交,提交成功")

    return is_closed_by_x[0]


# 调用函数
start_windown_config()
