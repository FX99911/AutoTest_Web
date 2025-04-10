from web_keys.read_excel.red_excel_sace_json import *

# 使用示例
if __name__ == "__main__":
    # 导入文件的路径文件路径
    excel_url = f"{home}/cases_date/test_excel.xlsx"
    # 测试用例运行模板路径
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

