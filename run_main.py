import os
import time

import pytest

if __name__ == '__main__':
    pytest.main()
    time.sleep(3)
    # 根据temps下的json文件，在reports下生成报告，每次执行前清空
    os.system('allure generate ./temps -o ./reports --clean')