



import os



def open_file(file_path):
    try:
        if os.path.exists(file_path):
            if os.name == 'nt':  # Windows 系统
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS 和 Linux 系统
                os.system(f'open {file_path}' if os.name == 'darwin' else f'xdg-open {file_path}')
            else:
                print(f"不支持的操作系统: {os.name}")
        else:
            print(f"文件 {file_path} 不存在。")
    except Exception as e:
        print(f"打开文件时出现错误: {e}")


# 这里你可以替换成你要打开的文件路径
file_path = '/Users/wang/PycharmProjects/AtouTest_Web/reports/index.html'
open_file(file_path)