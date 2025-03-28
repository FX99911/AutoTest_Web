import os


def concatenate_path(env_variable_value, path_to_concat):
    """
    将环境变量的值与给定路径进行拼接
    :param env_variable_value: 环境变量的值
    :param path_to_concat: 要拼接的路径
    :return: 拼接后的完整路径，如果环境变量值为空则返回 None
    """
    if env_variable_value:
        # 使用os.path.join函数拼接路径，确保路径格式正确
        full_path = os.path.join(env_variable_value, path_to_concat)

        return full_path

    else:
        return None


