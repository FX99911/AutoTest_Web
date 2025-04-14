# import os
# import time
# import pytest
#
#
# def start_run_auto_test():
#     pytest.main()
#     time.sleep(3)
#     # 根据temps下的json文件，在reports下生成报告，每次执行前清空
#     os.system('allure generate ./temps -o ./reports --clean')

import os
import time
import pytest
from web_keys.environment_info.montage_url import home

def start_run_auto_test():
    pytest.main()
    time.sleep(3)
    # 使用home变量确保路径一致性
    temps_dir = os.path.join(home, "temps")
    reports_dir = os.path.join(home, "reports")
    os.system(f'allure generate {temps_dir} -o {reports_dir} --clean')

# start_run_auto_test()