import inspect
import os


# def get_now_file_name():
#     """
#     获取当前 Python 脚本文件的文件名（不包含扩展名）。
#
#     此函数通过 `__file__` 属性获取当前脚本文件的完整路径，
#     接着使用 `os.path.basename()` 函数从完整路径中提取文件名（包含扩展名），
#     最后利用 `os.path.splitext()` 函数将扩展名分离，得到不包含扩展名的文件名。
#
#     返回:
#         str: 当前脚本文件的文件名（不包含扩展名）。
#     """
#     file_path = __file__
#     file_name_with_ext = os.path.basename(file_path)
#     file_name, _ = os.path.splitext(file_name_with_ext)
#     return file_name




def get_now_file_name():
    """
    获取调用此函数的文件名（不含后缀）

    Returns:
        str: 当前文件名（不含后缀）
    """
    # 获取调用者的栈帧
    frame = inspect.currentframe()
    try:
        # 获取调用者的文件名
        caller_frame = frame.f_back
        file_path = caller_frame.f_code.co_filename
        # 获取文件名（不含路径和后缀）
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        return file_name
    finally:
        # 确保释放栈帧
        del frame

