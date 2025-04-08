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


# # 步骤变量定义(暂时不需要)
# all_steps = convert_dict_to_variables(operation_steps)
# print('===========================测试步骤变量如下========================================')
# print(all_steps)  #示例
# # step1 = ['打开_浏览器', 'no', 'nan', 'nan']
# # step2 = ['打开_url_登录', 'https://adminplus.iviewui.com/', 'nan', 'nan']
# print('===========================测试步骤变量如上========================================')
# 获取列表
all_steps = get_all_steps(operation_steps)
# =====================以下是测试用例模板====================

########################

@allure.epic(f'项目名称：{project_name}')
@allure.feature(f"模块名称：{test_module}")
@allure.description('说明：这是一个说明描述，描述写这里') # 描述

class Test_Template(Keys):

    @allure.story(f'测试点：{test_points}')
    @allure.title(f'测试用例名：{cases_name}')
    @allure.link(url='http://www.baidu.com', name='这是一个链接')

    def test_execute(self):                    #这个就是定义一个(用例)，test_开头
        num = 0
        for step in all_steps:
            print(f'当前测试步骤信息{step}')
            num += 1
            if '打开_浏览器' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.start_chrome()
            if '打开_url' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.open(step[1])
            if '输入' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.input(step[1], step[2], step[3])
            if '点击' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.click(step[1], step[2])
            if '断言' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    assert self.text(step[1], step[2]) == step[0]
            if '关闭浏览器' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.quit()
            if '刷新页面' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.refresh()






