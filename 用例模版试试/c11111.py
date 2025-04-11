import time

import allure
from selenium.webdriver.common.by import By
from web_keys.seleniuum_device.keys import Keys


def convert_by_string(lst):
    new_lst = []
    for item in lst:
        if isinstance(item, str) and item.startswith('By.'):
            try:
                locator_name = item.split('.')[-1]
                new_lst.append(getattr(By, locator_name))
            except AttributeError:
                print(f"错误：By 类中不存在名为 {locator_name} 的属性。")
                new_lst.append(item)
        else:
            new_lst.append(item)
    return new_lst


#######所需变量######
url = 'https://adminplus.iviewui.com/'
user = 'admin'
pwd = 'admin'
#######所需变量######
#### 核心元素>>>> ###
user_input = ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[1]/div/div/div/input']  # 用户名输入框
user_input = convert_by_string(user_input)
pwd_input = [By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/form/div[2]/div/div/div/input']    # 密码输入框
login_button  = [By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/form/div[4]/button']  # 登陆按钮
#### 核心元素<<<< ###

#### 断言元素<<<< ###
judge_user_name = [By.XPATH,'//*[@id="app"]/div/div[2]/div/div[1]/div[4]/div[2]/a/span'] # 登陆成功后右上角的用户名

########################

@allure.epic('项目名称：内蒙古DHMP-3000版本') # 根据模板改即可，一个项目的都用这个
@allure.feature("模块名称：用户登陆模块") #  一个模块用一个名字此文件不用动
class Test_login(Keys):   # 一个模块只写一个 # 必须使用Test_开头 后边用英文翻译，比如登陆翻译后login

    @allure.story('测试用例：登陆')  # 写用例的名字
    @allure.title('测试用例名：正确-账号密码-登陆')   #写用例的名字  >>>>>每条用例从这里开始<<<<
    def test_login(self):                    #这个就是定义一个方法(用例)，换用例只需要修改test_login 中的login也用翻译
        with allure.step('第一步：打开浏览器'):  ########写步骤1干嘛的（写第一步后边：） 比如打开浏览器（固定写法）
            self.start_chrome()             # 紧接着第一步，写打开浏览器的操作  打开浏览器就这么固定写
        with allure.step('第二步：打开系统界面'):  ########写步骤2干嘛的（写第二步后边：） 以下操作根第一步一样
            self.open(url)            #  打开url
            time.sleep(1)
        with allure.step('第三步：输入用户名'):
            self.input(user_input[0],user_input[1],user)
        with allure.step('第四步：输入密码'):
            self.input(pwd_input[0], pwd_input[1],pwd)
        with allure.step('第五步：点击登陆'):
            self.click(login_button[0],login_button[1])
            time.sleep(2)
        with allure.step('第五步：断言'):
            nametest = self.text(judge_user_name[0],judge_user_name[1])
            print(nametest)
            self.quit()
        assert  nametest == user



        # raise Exception('登录出现异常了')






    #
    #
    # @allure.story('接口名称：登录接口')
    # def test_register(self):
    #     print('注册测试用例')
    # @pytest.mark.run(order=1)# 改变测试用例执行顺序
    # @allure.story('接口名称：登录接口')
    # def test_add_user(self):
    #     print('增加用户')
    #
    # @allure.story('接口名称：登录接口')
    # @pytest.mark.users
    # def test_del_user(self):
    #     print('删除用户')
    #
    # @pytest.mark.skip(reason='无条件跳过，跳过原因写这里')  # 直接跳过
    # @pytest.mark.order
    # @allure.story('接口名称：跳过接口')
    # def test_select_order(self):
    #     print('查询工单')
    #
    # @pytest.mark.skipif(age<=20,reason='有条件跳过，跳过原因写这里')  # 满足条件就跳过
    # @pytest.mark.order
    # @allure.story('接口名称：跳过接口')
    # def test_comeon_order(self):
    #     print('接收工单')
    #
    # @pytest.mark.order # 打标记
    # @allure.story('接口名称：工单接口')
    # def test_add_order(self):
    #     print('新增工单')
    #
    # @pytest.mark.order
    # @allure.story('接口名称：工单接口')
    # def test_del_order(self):
    #     print('删除工单')