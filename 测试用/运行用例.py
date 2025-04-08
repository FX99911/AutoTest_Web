import time
import allure
from web_keys.seleniuum_device.keys import Keys
from web_keys.read_excel.dist_to_variable import convert_dict_to_variables, get_all_steps
from web_keys.template_method.get_now_file_name import get_now_file_name

# 测试用例数据
# 项目信息
project_info = {
    '项目名称': ['测试的项目'],
    '模块名称': ['首页'],
    '测试点': ['登陆'],
    'nan': ['nan']
}
# 操作步骤
operation_steps = {
    '打开_浏览器': ['no', 'nan', 'nan'],
    '打开_url_登录': ['https://adminplus.iviewui.com/', 'nan', 'nan'],
    '输入_用户名': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[1]/div/div/div/input', 'admin'],
    '输入_密码': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[2]/div/div/div/input', 'admin'],
    '点击_登录按钮': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[4]/button', 'nan'],
    '断言': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[4]/button', '登陆成功']
}

# 后续可以在这里添加测试逻辑

# 定义项目信息变量
project_name = project_info['项目名称'][0]
test_module	= project_info['模块名称'][0]
test_points = project_info['测试点'][0]
cases_name = get_now_file_name()


# 步骤变量定义
all_steps = get_all_steps(operation_steps)
print('===========================测试步骤变量如下========================================')
print(all_steps)  #示例
# step1 = ['打开_浏览器', 'no', 'nan', 'nan']
# step2 = ['打开_url_登录', 'https://adminplus.iviewui.com/', 'nan', 'nan']
print('===========================测试步骤变量如上========================================')


for x in all_steps:
    print(x)
    print(type(x))