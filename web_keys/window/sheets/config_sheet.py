"""
自动化测试配置信息sheet页

该模块提供了一个图形用户界面，用于设置自动化测试的各项配置，包括：
1. 选择电脑类型（Windows/Mac）
2. 指定项目是否为H5项目
3. 添加备注信息
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from web_keys.environment_info.montage_url import home

# 配置文件路径
CONFIG_FILE_PATH = os.path.join(home, 'config', 'start_config.json')

def get_start_config_url():
    """
    获取配置文件的路径

    Returns:
        str: 配置文件的完整路径
    """
    return CONFIG_FILE_PATH


def create_config_sheet(parent_frame, widget_dict):
    """
    创建配置信息sheet页

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
    title_label = ttk.Label(main_frame, text="自动化测试配置", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

    # 定义下拉选项
    options = ["window", "mac"]  # 电脑类型选项
    options2 = ["yes", "no"]  # 是否H5选项

    # 第一个选择框相关 - 电脑类型
    option_label = ttk.Label(main_frame, text="1. 电脑类型:")
    option_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
    option_var = tk.StringVar(parent_frame)
    option_var.set(options[0])  # 默认选择第一项
    option_menu = ttk.Combobox(main_frame, textvariable=option_var, values=options, width=30, state="readonly")
    option_menu.grid(row=2, column=0, sticky="w", pady=(0, 15))
    widget_dict['option_var'] = option_var

    # 第二个选择框相关 - 项目是否为H5
    option_label2 = ttk.Label(main_frame, text="2. 项目是否为H5:")
    option_label2.grid(row=3, column=0, sticky="w", pady=(0, 5))
    option_var2 = tk.StringVar(parent_frame)
    option_var2.set(options2[1])  # 默认选择第二项
    option_menu2 = ttk.Combobox(main_frame, textvariable=option_var2, values=options2, width=30, state="readonly")
    option_menu2.grid(row=4, column=0, sticky="w", pady=(0, 15))
    widget_dict['option_var2'] = option_var2

    # 输入框相关 - 备注信息
    input_label = ttk.Label(main_frame, text="3. 备注信息:")
    input_label.grid(row=5, column=0, sticky="w", pady=(0, 5))
    entry = ttk.Entry(main_frame, width=30)
    entry.grid(row=6, column=0, sticky="w", pady=(0, 15))
    widget_dict['entry'] = entry

    # 加载已有配置
    load_config(widget_dict)

    # 添加按钮区域
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=7, column=0, columnspan=2, pady=20)

    # 提交按钮 - 保存配置
    submit_button = ttk.Button(
        button_frame,
        text="保存配置",
        command=lambda: submit_config(widget_dict),
        style="Accent.TButton",
        width=15
    )
    submit_button.pack(side=tk.LEFT, padx=10)

    # 重置按钮 - 重置配置
    reset_button = ttk.Button(
        button_frame,
        text="重置",
        command=lambda: reset_config(widget_dict),
        width=15
    )
    reset_button.pack(side=tk.LEFT, padx=10)

    return widget_dict


def load_config(widget_dict):
    """
    从配置文件加载已有配置

    Args:
        widget_dict: 包含控件引用的字典
    """
    config_path = get_start_config_url()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                
            # 设置电脑类型
            if 'pc_type' in data and data['pc_type'] in ["window", "mac"]:
                widget_dict['option_var'].set(data['pc_type'])
                
            # 设置是否H5
            if 'is_h5' in data and data['is_h5'] in ["yes", "no"]:
                widget_dict['option_var2'].set(data['is_h5'])
                
            # 设置备注信息
            if 'note' in data:
                widget_dict['entry'].delete(0, tk.END)
                widget_dict['entry'].insert(0, data['note'])
        except Exception as e:
            print(f"加载配置文件时出错: {e}")


def save_config(widget_dict):
    """
    保存配置到配置文件

    Args:
        widget_dict: 包含控件引用的字典

    Returns:
        bool: 是否保存成功
    """
    # 获取用户选择的配置
    selected_option = widget_dict['option_var'].get()
    selected_option2 = widget_dict['option_var2'].get()
    input_text = widget_dict['entry'].get()

    # 准备保存到配置文件的数据
    data = {
        "pc_type": selected_option,
        "is_h5": selected_option2,
        "note": input_text
    }

    # 确保配置目录存在
    config_dir = os.path.dirname(get_start_config_url())
    os.makedirs(config_dir, exist_ok=True)

    # 保存配置到JSON文件
    try:
        with open(get_start_config_url(), 'w') as f:
            json.dump(data, f)
        print("配置信息已成功保存到配置文件中。")
        return True
    except Exception as e:
        error_msg = f"保存配置信息时出现错误: {e}"
        print(error_msg)
        messagebox.showerror("错误", error_msg)
        return False


def submit_config(widget_dict):
    """
    处理配置页面的提交按钮点击事件

    Args:
        widget_dict: 包含控件引用的字典
    """
    # 保存配置
    if save_config(widget_dict):
        messagebox.showinfo("成功", "配置信息已成功保存")
    else:
        messagebox.showerror("错误", "保存配置信息失败")


def reset_config(widget_dict):
    """
    重置配置到默认值

    Args:
        widget_dict: 包含控件引用的字典
    """
    # 重置电脑类型
    widget_dict['option_var'].set("window")
    
    # 重置是否H5
    widget_dict['option_var2'].set("no")
    
    # 重置备注信息
    widget_dict['entry'].delete(0, tk.END)
    
    messagebox.showinfo("提示", "配置已重置为默认值") 