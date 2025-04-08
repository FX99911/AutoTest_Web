import os


def get_now_file_name():
    """
    获取当前 Python 脚本文件的文件名（不包含扩展名）。

    此函数通过 `__file__` 属性获取当前脚本文件的完整路径，
    接着使用 `os.path.basename()` 函数从完整路径中提取文件名（包含扩展名），
    最后利用 `os.path.splitext()` 函数将扩展名分离，得到不包含扩展名的文件名。

    返回:
        str: 当前脚本文件的文件名（不包含扩展名）。
    """
    file_path = __file__
    file_name_with_ext = os.path.basename(file_path)
    file_name, _ = os.path.splitext(file_name_with_ext)
    return file_name

