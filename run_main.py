import pytest
import subprocess
import time
from web_keys.file_tool.file_utils import *
from web_keys.environment_info.montage_url import home

# 获取执行开始时间：

run_time  = datetime.now().strftime("%Y-%m-%d-%H%M")

def start_run_auto_test():

    print('当前启动Pytest路径：',os.getcwd())
    os.chdir(home)
    print('切换到项目根目录：', home)

    # 执行 pytest 测试
    pytest.main()

    # 等待一段时间，确保测试结果文件生成
    time.sleep(3)

    # 构建命令列表
    # 此列表为 allure generate 命令及其参数，用于生成 Allure 报告
    # --single-file 表示生成单文件报告
    # allure-results 是测试结果的来源目录
    # -o 指定输出目录，这里有两个输出目录，分别是变量 output_directory 和 ./reports
    # ./temps 也是测试结果的来源目录
    # --clean 表示在生成报告前清空输出目录
    command = ['allure', 'generate', '--single-file', 'allure-results','./temps', '-o', './reports', '--clean']

    try:
        # 执行命令
        # 使用 subprocess.run 函数执行命令列表
        # check=True 表示如果命令执行失败（返回非零退出码），则抛出 CalledProcessError 异常
        # text=True 表示以文本模式处理输入输出
        # capture_output=True 表示捕获命令的标准输出和标准错误输出
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("命令执行成功，输出信息：")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：{e.stderr}")

    # 创建一个时间目录：
    # reports_record_path = create_timestamp_dir(f'{home}/reports_record',run_time)
    reports_record_path = os.path.join(home, 'reports_record', run_time)

    time.sleep(1)
    # 复制报告到这
    rp_path = os.path.join(home, 'reports')

    copy_directory(rp_path,reports_record_path)

    print(f'测试报告记录在：{reports_record_path}')
    return reports_record_path


# start_run_auto_test()