import os
import pandas as pd
from typing import Dict, List, Union


# 设置默认基础路径
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cases_date")


# =========================================================
def read_single_excel(file_path: str) -> Dict[str, List[str]]:
    """
    读取单个Excel文件并返回字典格式的数据

    Args:
        file_path (str): Excel文件的路径

    Returns:
        Dict[str, List[str]]: 字典格式的数据，键为第一行标题，值为第二行内容

    Example:
        >>> data = read_single_excel("example.xlsx")
        >>> print(data)
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


# =========================================================
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


# =========================================================
def create_first_directory(data: Dict[str, List[str]], base_dir: str = BASE_DIR) -> str:
    """
    创建第一级目录，目录名为字典的第一个value

    Args:
        data (Dict[str, List[str]]): read_single_excel函数返回的字典
        base_dir (str): 基础目录路径，默认为项目根目录下的cases_date

    Returns:
        str: 创建的目录路径
    """
    try:
        if not data:
            raise ValueError("字典为空")

        # 获取第一个value作为目录名
        first_value = list(data.values())[0][0]
        dir_path = os.path.join(base_dir, first_value)

        # 创建目录
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    except Exception as e:
        print(f"创建第一级目录时发生错误: {str(e)}")
        return ""


# =========================================================
def create_second_directory(data: Dict[str, List[str]], parent_dir: str) -> str:
    """
    在父目录下创建第二级目录，目录名为字典的第二个value

    Args:
        data (Dict[str, List[str]]): read_single_excel函数返回的字典
        parent_dir (str): 父目录路径

    Returns:
        str: 创建的目录路径
    """
    try:
        if not data or len(data) < 2:
            raise ValueError("字典中至少需要两个value")

        # 获取第二个value作为目录名
        second_value = list(data.values())[1][0]
        dir_path = os.path.join(parent_dir, second_value)

        # 创建目录
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    except Exception as e:
        print(f"创建第二级目录时发生错误: {str(e)}")
        return ""


# =========================================================
def create_third_directory(data: Dict[str, List[str]], parent_dir: str) -> str:
    """
    在父目录下创建第三级目录，目录名为字典的第三个value

    Args:
        data (Dict[str, List[str]]): read_single_excel函数返回的字典
        parent_dir (str): 父目录路径

    Returns:
        str: 创建的目录路径
    """
    try:
        if not data or len(data) < 3:
            raise ValueError("字典中至少需要三个value")

        # 获取第三个value作为目录名
        third_value = list(data.values())[2][0]
        dir_path = os.path.join(parent_dir, third_value)

        # 创建目录
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    except Exception as e:
        print(f"创建第三级目录时发生错误: {str(e)}")
        return ""


# =========================================================
def create_test_files(test_cases: List[Dict[str, Dict[str, List[str]]]], output_dir: str) -> List[str]:
    """
    根据测试用例字典创建对应的Python文件

    Args:
        test_cases (List[Dict[str, Dict[str, List[str]]]]): 测试用例字典列表
        output_dir (str): 输出目录路径

    Returns:
        List[str]: 创建的文件路径列表
    """
    created_files = []
    try:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        for test_case in test_cases:
            # 获取测试用例名称（字典的key）
            test_name = list(test_case.keys())[0]
            # 创建文件名（替换特殊字符）
            file_name = f"test_{test_name.replace('-', '_')}.py"
            file_path = os.path.join(output_dir, file_name)

            # 获取测试用例数据（字典的value）
            test_data = test_case[test_name]

            # 创建文件内容
            content = f"""# 测试用例数据
test_data = {test_data}

# 后续可以在这里添加测试逻辑
"""

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            created_files.append(file_path)
            print(f"已创建文件: {file_path}")

        return created_files
    except Exception as e:
        print(f"创建测试文件时发生错误: {str(e)}")
        return []