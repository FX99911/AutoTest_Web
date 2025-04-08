import time
import allure
from web_keys.seleniuum_device.keys import Keys
from web_keys.read_excel.dist_to_variable import convert_dict_to_variables
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
steps = convert_dict_to_variables(operation_steps)
print('===========================测试步骤变量如下========================================')
print(steps)  #示例
# step1 = ['打开_浏览器', 'no', 'nan', 'nan']
# step2 = ['打开_url_登录', 'https://adminplus.iviewui.com/', 'nan', 'nan']
# step3 = ['输入_用户名', 'By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[1]/div/div/div/input', 'admin']
print('===========================测试步骤变量如上========================================')

# =====================以下是测试用例模板====================

########################

@allure.epic(f'项目名称：{project_name}') # 根据模板改即可，一个项目的都用这个
@allure.feature(f"模块名称：{test_module}") #  一个模块用一个名字此文件不用动
@allure.description('说明：这是一个说明描述，描述写这里') # 描述

class Test_Template(Keys):

    @allure.story(f'测试点：{test_points}')  # 写用例的测试点名字
    @allure.title(f'测试用例名：{cases_name}')   #测试用例名字 >>>>>每条用例从这里开始<<<<
    @allure.link(url='http://www.baidu.com', name='这是一个链接')

    def test_execute(self):                    #这个就是定义一个(用例)，test_开头

        with allure.step(f'第一步：{stp}'):  ########写步骤1干嘛的（写第一步后边：） 比如打开浏览器（固定写法）
            self.start_chrome()             # 紧接着第一步，写打开浏览器的操作  打开浏览器就这么固定写
        with allure.step('第二步：打开系统界面'):  ########写步骤2干嘛的（写第二步后边：） 以下操作根第一步一样
            self.open(url)            #  打开url
            time.sleep(1)
        with allure.step('第三步：输入用户名'):
            self.input(user_input[0],user_input[1],user_name)
        with allure.step('第四步：输入密码'):
            self.input(pwd_input[0], pwd_input[1],user_pwd)
        with allure.step('第五步：点击登陆'):
            self.click(login_button[0],login_button[1])
            time.sleep(2)
        with allure.step('第五步：断言'):
            title = self.title()
            self.quit()
        assert  title == '主控台 - Admin Plus'



        # raise Exception('登录出现异常了')


