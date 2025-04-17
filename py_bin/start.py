import subprocess
import os

# 设置项目根目录，根据实际情况修改
project_root = '/Users/wang/PycharmProjects/AtouTest_Web'

# 获取当前的 PYTHONPATH
current_pythonpath = os.environ.get('PYTHONPATH', '')

# 如果 PYTHONPATH 不为空，添加分隔符
if current_pythonpath:
    new_pythonpath = f"{current_pythonpath}:{project_root}"
else:
    new_pythonpath = project_root

# 设置新的环境变量
new_env = os.environ.copy()
new_env['PYTHONPATH'] = new_pythonpath

# 要执行的 Python 文件路径
python_file_path = os.path.join(project_root, 'web_keys', 'window', 'start_window.py')

try:
    # 执行 Python 文件，使用通用的 python3 命令
    result = subprocess.run(['python3', python_file_path], env=new_env, capture_output=True, text=True, check=True)
    print("执行成功，输出如下：")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("执行出错，错误信息如下：")
    print(e.stderr)
