import os


def get_project_root_path():
    # 获取当前脚本的绝对路径
    current_script_path = os.path.abspath(__file__)
    # print(f'当前绝对路径：{current_script_path}')
    # 项目根目录的名称
    project_root_name = "AtouTest_Web"

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


home = get_project_root_path()

# # 调用函数获取项目根目录的绝对路径
# project_root = get_project_root_path()
# # 使用replace方法将反斜杠替换为斜杠
# formatted_path = project_root.replace("\\", "/")
# # 或者使用f字符串格式化输出
# print(f"项目根目录的绝对路径是: {formatted_path}")


print(f'home={home}')
