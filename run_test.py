import os

from web_keys.montage_url import concatenate_path
from web_keys.py_variables import get_env_variable
from web_keys.start_windown import start_windown_config
import pytest
import sys
from web_keys.log_window import LogWindow, StdoutRedirector
import io

#----------#获取环境变量#----------------------
home = get_env_variable()
#----------#用环境变量 拼接url,#----------------------

arrure_report_url = concatenate_path(home,'reports/index.html')


swc = start_windown_config()

if __name__ == '__main__':
    if swc:
        print('关闭窗口')
    else:
        # 设置要打开的文件路径为 allure 生成的报告的 index.html 文件
        file_to_open = arrure_report_url

        # 重定向输出到内存缓冲区
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        try:
            # 执行 pytest 测试框架，运行项目中的自动化测试用例
            pytest.main()
        except Exception as e:
            print(f"执行测试时出现错误: {e}")

        # 生成报告
        os.system('allure generate ./temps -o ./reports --clean')

        # 获取测试输出
        test_output = new_stdout.getvalue()
        # 恢复标准输出
        sys.stdout = old_stdout

        # 创建日志窗口实例，用于显示测试相关日志
        log_window = LogWindow(file_to_open)
        # 将标准输出流重定向到自定义的 StdoutRedirector 类实例
        sys.stdout = StdoutRedirector(log_window)

        # 打印测试输出到日志窗口
        print(test_output)

        # 启动日志窗口的主事件循环，显示之前收集到的所有日志信息
        log_window.start()