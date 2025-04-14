import os
import time
import pytest
from web_keys.environment_info.montage_url import home

def start_run_auto_test():
    print('当前启动Pytest路径：',os.getcwd())
    os.chdir(home)
    print('切换到项目根目录：', home)

    pytest.main()
    time.sleep(3)
    # 根据temps下的json文件，在reports下生成报告，每次执行前清空
    os.system('allure generate --single-file allure-results ./temps -o ./reports --clean')

start_run_auto_test()