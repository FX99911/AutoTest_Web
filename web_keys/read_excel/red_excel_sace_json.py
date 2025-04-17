import os
import pandas as pd
from typing import Dict, List
from web_keys.environment_info.montage_url import home

#####################################################################
####################【此模块的方法用于读取excel】#########################
#####################################################################


# 设置默认基础路径(存放测试用例的路径)<<<<<<<<<<<
# BASE_DIR = f'{home}/cases_date' #<<<<<<<配置
BASE_DIR = os.path.join(home, 'cases_date')
print("--测试用例保存路径 = ", BASE_DIR)

# 设置默认基础路径(存放测试用例的路径)<<<<<<<<<<<
# BASE_RUN_DIR = f'{home}/cases_run' #<<<<<<<配置
BASE_RUN_DIR = os.path.join(home, 'cases_run')
print("--测试用例保存路径 = ", BASE_RUN_DIR)

# 设置默认基础路径(存放截图的路径)
# PICTURE_DIR = f'{home}/reports/screenshot'#<<<<<<<配置
PICTURE_DIR = os.path.join(home, 'reports', 'screenshot')
print("--测试截图保存路径 = ", PICTURE_DIR)


def read_single_excel(file_path: str) -> Dict[str, List[str]]:
    """
    读取单个Excel文件并返回字典格式的数据

    Args:
        file_path (str): Excel文件的路径

    Returns:
        Dict[str, List[str]]: 字典格式的数据，键为第一行标题，值为第二行内容

    Example:
        # >>> data = read_single_excel("example.xlsx")
        # >>> print(data)
        {'标题1': ['内容1'], '标题2': ['内容2']}
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path, header=None)

        # 确保至少有两行数据
        if len(df) < 2:
            raise ValueError("Excel文件必须至少包含两行数据")

        # 获取标题行和内容行
        headers = df.iloc[0].tolist()
        content = df.iloc[1].tolist()

        # 创建字典
        result = {}
        for header, value in zip(headers, content):
            result[str(header)] = [str(value)]

        return result
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误: {str(e)}")
        return {}


def read_excel_from_fourth_row(file_path: str) -> List[Dict[str, Dict[str, List[str]]]]:
    """
    从Excel的第四行开始读取数据，为每个测试用例生成独立的字典

    Args:
        file_path (str): Excel文件的路径

    Returns:
        List[Dict[str, Dict[str, List[str]]]]: 每个测试用例的字典列表，结构如下：
        [
            {
                '测试用例名称1': {
                    '操作步骤1': ['URL/定位方法', '定位Value', '输入/断言内容'],
                    '操作步骤2': ['URL/定位方法', '定位Value', '输入/断言内容'],
                    ...
                }
            },
            {
                '测试用例名称2': {
                    '操作步骤1': ['URL/定位方法', '定位Value', '输入/断言内容'],
                    '操作步骤2': ['URL/定位方法', '定位Value', '输入/断言内容'],
                    ...
                }
            }
        ]
    """
    try:
        # 读取Excel文件，跳过前三行
        df = pd.read_excel(file_path, header=None, skiprows=3)

        if len(df) < 1:
            raise ValueError("Excel文件从第四行开始没有数据")

        # 初始化结果列表
        result_list = []

        # 获取所有唯一的测试用例名称，保持原始顺序
        test_cases = []
        for value in df[0]:
            if value not in test_cases and str(value) != '测试用例名称':
                test_cases.append(value)

        # 按原始顺序处理数据
        for test_case in test_cases:
            # 获取当前测试用例的所有行
            group = df[df[0] == test_case]
            group_dict = {}

            # 遍历每一行
            for _, row in group.iterrows():
                # 第二列的值作为子键
                second_col_value = str(row[1])
                # 从第三列开始的值作为列表
                values = [str(x) for x in row[2:]]
                group_dict[second_col_value] = values

            # 为每个测试用例创建独立的字典
            test_case_dict = {str(test_case): group_dict}
            result_list.append(test_case_dict)

        return result_list
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误: {str(e)}")
        return []


def create_directories(data: Dict[str, List[str]], base_dir: str = BASE_RUN_DIR) -> str:
    """
    创建三级目录结构（测试用例的）
    """
    try:
        if not data or len(data) < 3:
            raise ValueError("字典中至少需要三个value")
        # 创建第一级目录
        first_dir = os.path.join(base_dir, list(data.values())[0][0])
        os.makedirs(first_dir, exist_ok=True)
        # 创建第二级目录
        second_dir = os.path.join(first_dir, list(data.values())[1][0])
        os.makedirs(second_dir, exist_ok=True)
        # 创建第三级目录
        third_dir = os.path.join(second_dir, list(data.values())[2][0])
        os.makedirs(third_dir, exist_ok=True)
        return third_dir
    except Exception as e:
        print(f"创建用例目录时发生错误: {str(e)}")
        return ""

def create_picture_directories(data: Dict[str, List[str]], picture_dir: str = PICTURE_DIR) -> str:
    """
    创建三级目录结构（测试截图的）
    """
    try:
        if not data or len(data) < 3:
            raise ValueError("字典中至少需要三个value")
        # 创建第一级目录
        first_dir = os.path.join(picture_dir, list(data.values())[0][0])
        os.makedirs(first_dir, exist_ok=True)
        # 创建第二级目录
        second_dir = os.path.join(first_dir, list(data.values())[1][0])
        os.makedirs(second_dir, exist_ok=True)
        # 创建第三级目录
        third_dir = os.path.join(second_dir, list(data.values())[2][0])
        os.makedirs(third_dir, exist_ok=True)
        return third_dir
    except Exception as e:
        print(f"创建截图目录时发生错误: {str(e)}")
        return ""



def create_test_files_from_template(test_cases: List[Dict[str, Dict[str, List[str]]]],
                                  output_dir: str,
                                  first_two_rows: Dict[str, List[str]],
                                  template_path: str) -> List[str]:
    """
    根据模板创建测试文件，并添加序号前缀以确保执行顺序
    """
    created_files = []
    try:
        # 读取模板文件
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 遍历测试用例，添加序号前缀
        for index, test_case in enumerate(test_cases, start=1):
            # 获取测试用例名称
            test_name = list(test_case.keys())[0]
            # 添加序号前缀，格式化为两位数（01, 02, ...）
            file_name = f"test_{index:02d}_{test_name.replace('-', '_')}.py"
            file_path = os.path.join(output_dir, file_name)

            # 获取测试用例数据
            test_data = test_case[test_name]

            # 格式化项目信息
            formatted_project_info = "{\n"
            for key, value in first_two_rows.items():
                formatted_project_info += f"    '{key}': {value},\n"
            formatted_project_info = formatted_project_info.rstrip(',\n') + "\n}"

            # 格式化操作步骤
            formatted_operation_steps = "{\n"
            for key, value in test_data.items():
                formatted_operation_steps += f"    '{key}': {value},\n"
            formatted_operation_steps = formatted_operation_steps.rstrip(',\n') + "\n}"

            # 替换空字典为实际数据
            content = template_content.replace("project_info = {}", f"project_info = {formatted_project_info}")
            content = content.replace("operation_steps = {}", f"operation_steps = {formatted_operation_steps}")

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            created_files.append(file_path)
            print(f"{'更新' if os.path.exists(file_path) else '创建'}文件: {file_path}")

        return created_files
    except Exception as e:
        print(f"处理测试文件时发生错误: {str(e)}")
        return []


# 使用示例
if __name__ == "__main__":
    # 文件路径
    excel_url = f"{home}/cases_date/test_excel.xlsx"
    template_path = f"{home}/cases_date/test_case_template.py"

    # 读取Excel文件（前两行）
    data = read_single_excel(excel_url)
    print("Excel前两行数据:")
    print(data)

    # 读取Excel文件（从第四行开始）
    data_from_fourth = read_excel_from_fourth_row(excel_url)
    print("\nExcel从第四行开始的数据:")
    for test_case in data_from_fourth:
        print(test_case)
        print()

    # 创建测试用例目录结构
    third_dir = create_directories(data)
    print(f"\n测试用例-第三级目录路径: {third_dir}")

    # 创建截图目录结构
    picture_dir = create_picture_directories(data)
    print(f"\n测试截图-第三级目录路径: {picture_dir}")

    # 使用模板创建测试文件
    created_files = create_test_files_from_template(data_from_fourth, third_dir, data, template_path)
    print("\n创建的文件列表:")
    for file_path in created_files:
        print(file_path)

