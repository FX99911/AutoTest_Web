import time
import allure
import pytest
from selenium.webdriver.common.by import By
from web_keys.keys import Keys
from web_keys.open_excel_data import excel_variables

cases_url = 'cases_date/test_excel.xlsx'
data_dict = excel_variables(cases_url)
print(data_dict)

#######所需变量######
try:
    project_name = data_dict['project_name']
    test_module_name = data_dict['test_module']
    case_name = data_dict['case_name']

    #### 核心元素>>>> ###
    url = data_dict['step1'][1]
    user_name = data_dict['step2'][4]
    user_pwd = data_dict['step3'][4]
    print('-----------',user_name)
    print('-----------',user_pwd)
    #### 核心元素>>>> ###
    user_input = [data_dict['step2'][2], data_dict['step2'][3]]  # 用户名输入框
    print('-----------',user_input)
    pwd_input = [data_dict['step3'][2], data_dict['step3'][3]]    # 密码输入框
    login_button  = [data_dict['step4'][2],data_dict['step4'][3]]  # 登陆按钮
    #### 核心元素<<<< ###


except (KeyError, IndexError):
    print("【error】：未找到，用例中的 足够的元素。")
#######-------------------------------------所需变量------------------------------######
#### 断言元素<<<< ###
judge_user_name = [By.XPATH,''] # 登陆成功后右上角的用户名

########################

@allure.epic(f'项目名称：{project_name}') # 根据模板改即可，一个项目的都用这个
@allure.feature(f"模块名称：{test_module_name}") #  一个模块用一个名字此文件不用动
class Test_login(Keys):   # 一个模块只写一个 # 必须使用Test_开头 后边用英文翻译，比如登陆翻译后login

    @allure.story(f'测试用例：{case_name}')  # 写用例的名字
    #@allure.title('测试用例名：正确-账号密码-登陆')   #更下一集  >>>>>每条用例从这里开始<<<<
    def test_login(self):                    #这个就是定义一个方法(用例)，换用例只需要修改test_login 中的login也用翻译
        with allure.step('第一步：打开浏览器'):  ########写步骤1干嘛的（写第一步后边：） 比如打开浏览器（固定写法）
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



