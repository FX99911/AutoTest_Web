from selenium.webdriver.common.devtools.v132.debugger import step_into

from web_keys.open_excel_data import read_excel

# 使用原始字符串表示路径
file_path = 'cases_date/test_excel.xlsx'
# 调用read_excel函数读取Excel文件数据
result = read_excel(file_path)
# 遍历结果字典，打印每个变量名及其对应的值（可能是字符串或列表）
for key, value in result.items():
    globals()[key] = value
    print(f"变量名: {key}, 变量值: {value}")


#######所需变量######
url = 'http://www.baidu.com'
user = 'administrator'
pwd = 'asb#1234'
#######所需变量######