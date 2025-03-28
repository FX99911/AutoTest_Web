import tkinter as tk
from tkinter import ttk
import os


class LogWindow:
    def __init__(self, file_to_open):
        # 创建主窗口
        self.root = tk.Tk()
        # 设置窗口标题
        self.root.title("测试日志")
        # 设置窗口大小
        self.root.geometry("800x600")

        # 创建垂直滚动条
        self.scrollbar = ttk.Scrollbar(self.root)
        # 将滚动条放置在窗口右侧，并使其在垂直方向填充
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建文本框用于显示日志内容，设置其垂直滚动条与创建的滚动条关联
        self.text = tk.Text(self.root, yscrollcommand=self.scrollbar.set)
        # 将文本框填充整个窗口并在水平和垂直方向扩展
        self.text.pack(fill=tk.BOTH, expand=True)

        # 配置滚动条，使其能控制文本框的垂直滚动
        self.scrollbar.config(command=self.text.yview)

        # 要打开的文件路径
        self.file_to_open = file_to_open

        # 创建打开文件的按钮
        self.open_file_button = tk.Button(self.root, text="打开文件", command=self.open_file)
        self.open_file_button.pack(pady=10)

    def append_log(self, message):
        # 在文本框的末尾插入日志信息，并添加换行符
        self.text.insert(tk.END, message + '\n')
        # 自动滚动到文本框的末尾，以便显示最新的日志
        self.text.see(tk.END)

    def start(self):
        # 启动窗口的主事件循环，使窗口保持显示并响应用户操作
        self.root.mainloop()

    def open_file(self):
        try:
            # 尝试打开指定的文件
            if os.path.exists(self.file_to_open):
                os.startfile(self.file_to_open) if os.name == 'nt' else os.system(f'open {self.file_to_open}')
            else:
                self.append_log(f"文件 {self.file_to_open} 不存在。")
        except Exception as e:
            self.append_log(f"打开文件时出现错误: {e}")


class StdoutRedirector:
    def __init__(self, log_window):
        """
        初始化 StdoutRedirector 类的实例。
        :param log_window: LogWindow 类的实例，用于将标准输出重定向到该日志窗口。
        """
        self.log_window = log_window

    def write(self, text):
        """
        实现标准输出的 write 方法，将输出的文本添加到日志窗口中。
        当调用 print 函数时，实际上会调用 sys.stdout.write 方法，
        这里将文本传递给 LogWindow 实例的 append_log 方法，实现输出重定向。
        :param text: 要输出的文本内容。
        """
        self.log_window.append_log(text)

    def flush(self):
        """
        实现标准输出的 flush 方法，用于刷新输出缓冲区。
        在当前场景下，不需要进行特殊的刷新操作，所以该方法为空。
        """
        pass

    def isatty(self):
        """
        实现 isatty 方法，用于判断输出是否连接到终端设备。
        由于输出已被重定向到日志窗口，返回 False。
        """
        return False