import os
from dotenv import load_dotenv

# 这个文件没啥用，但是不想删除
def get_env_variable(variable_name='PROJECT_ROOT'):
    """
    获取指定环境变量的值，先在当前工作目录查找.env文件，若未找到则去web_keys目录查找
    :param variable_name: 要获取的环境变量名称 默认'PROJECT_ROOT'
    :return: 环境变量的值，如果不存在则返回 None
    """
    # 获取当前工作目录
    current_working_dir = os.getcwd()
    # 指定.env文件的路径，直接在当前工作目录下查找.env文件
    env_path = os.path.join(current_working_dir, '.env')
    if os.path.exists(env_path):
        print(f"{env_path} 文件存在")
        load_dotenv(env_path)
        value = os.environ.get(variable_name)
        if value:
            return value
    elif os.path.exists(os.path.join(current_working_dir, 'web_keys', '.env')):
        web_keys_env_path = os.path.join(current_working_dir, 'web_keys', '.env')
        print(f"{web_keys_env_path} 文件存在")
        load_dotenv(web_keys_env_path)
        value = os.environ.get(variable_name)
        if value:
            return value
    else:
        print(f"{env_path} 文件不存在，且 web_keys 目录下也未找到 .env 文件")
    print(f"未找到包含 {variable_name} 的.env 文件")
    return None



print(get_env_variable('PROJECT_ROOT'))