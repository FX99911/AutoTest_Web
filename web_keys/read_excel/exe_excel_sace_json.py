import os
import pandas as pd
from typing import Dict, List

from web_keys.read_excel.red_excel_sace_json import *
from web_keys.environment_info.montage_url import home

# 使用示例
if __name__ == "__main__":
    # 文件目录
    excel_url = f"{home}/cases_date/test_excel.xlsx"

    # 读取Excel文件（前两行）
    data = read_single_excel(excel_url)
    print("Excel前两行数据:")
    print(data)

    # 读取Excel文件（从第四行开始）
    data_from_fourth = read_excel_from_fourth_row(excel_url)
    print("\nExcel从第四行开始的数据:")
    for test_case in data_from_fourth:
        print(test_case)
        print()  # 添加空行分隔不同的测试用例

    # 创建第一级目录（使用默认的BASE_DIR）
    first_dir = create_first_directory(data)
    print(f"\n第一级目录路径: {first_dir}")

    # 创建第二级目录
    second_dir = create_second_directory(data, first_dir)
    print(f"第二级目录路径: {second_dir}")

    # 创建第三级目录
    third_dir = create_third_directory(data, second_dir)
    print(f"第三级目录路径: {third_dir}")

    # 在第三级目录中创建测试文件
    created_files = create_test_files(data_from_fourth, third_dir)
    print("\n创建的文件列表:")
    for file_path in created_files:
        print(file_path)
