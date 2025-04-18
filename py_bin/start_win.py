import subprocess
import os



def get_project_root_path():
    """
    自动获取项目根目录
    从当前脚本位置开始，逐级向上查找名为 "AtouTest_Web_副本" 的目录
    如果找到则返回该目录路径，否则返回当前脚本所在目录
    """
    # 获取当前脚本的绝对路径
    current_script_path = os.path.abspath(__file__)
    print(f'当前绝对路径：{current_script_path}')
    # 项目根目录的名称
    project_root_name = "AutoTest_Web"

    # 从当前脚本路径开始，逐级向上查找项目根目录
    current_path = os.path.dirname(current_script_path)
    while current_path != os.path.dirname(current_path):
        # 获取当前路径的最后一级目录名
        base_name = os.path.basename(current_path)
        if base_name == project_root_name:
            # 若当前路径的最后一级目录名与项目根目录名一致，则找到了项目根目录
            project_root_path = current_path
            return project_root_path
        # 若未找到，继续向上一级目录查找
        current_path = os.path.dirname(current_path)

    # 如果遍历到系统根目录仍未找到，默认使用当前脚本所在目录作为项目根目录
    home = os.path.dirname(current_script_path)
    return home


# 设置项目根目录，根据实际情况修改
project_root = get_project_root_path()



# 获取当前的 PYTHONPATH
current_pythonpath = os.environ.get('PYTHONPATH', '')
print('当前的 PYTHONPATH:',current_pythonpath)


new_pythonpath = project_root

# 设置新的环境变量
new_env = os.environ.copy()
new_env['PYTHONPATH'] = new_pythonpath
print('更新 PYTHONPATH:',new_pythonpath)

# 要执行的 Python 文件路径
python_file_path = os.path.join(project_root, 'web_keys', 'window', 'start_window.py')

try:

    # 执行 Python 文件，使用通用的 python3 命令
    result = subprocess.run(['python', python_file_path], env=new_env, capture_output=True, text=True, check=True)
    print("执行成功，输出如下：")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("执行出错，错误信息如下：")
    print(e.stderr)
