import allure
import pytest

@allure.epic('项目名称：王亚辉科技自动化测试报告')
@allure.feature("模块名称：用户管理模块")
class Test2:
    age = 18

    @allure.story('接口名称：登录接口')
    @allure.title('验证登录成功')
    def test_1(self):
        print('测试用例1')
        assert 1==1

    @allure.story('接口名称：登录接口')
    @allure.title('验证登录失败')
    @allure.severity(allure.severity_level.BLOCKER) # .BLOCKER（严重级别）
    @allure.description('说明：这是一个说明描述，加载这里')
    @allure.link(url='http://www.baidu.com',name='接口访问链接')
    @allure.testcase('http://www.baidu.com','测试用例链接')
    @allure.issue('http://www.baidu.com','这个是bug链接')
    def test_2(self):
        #allure.dynamic.story('接口名称：登录接口')  #接口名称，也可以加这里
        # allure.dynamic.title('验证登录失败')  用例名称，也可以这么些
        #allure.dynamic.severity(allure.severity_level.BLOCKER) # .BLOCKER（严重级别），也可以加这里
        #allure.dynamic.description('说明：这是一个说明描述，也可以加载这里')
        with allure.step('第一步：测试步骤1'):  # 加入测试用例的写法
                 # 加入文件附件（错误截图）
                allure.attach.file(source="cases_screenshot/p1.jpg",name='输入用户名截图',attachment_type=allure.attachment_type.JPG,extension="jpg")
        with allure.step('第二步：测试步骤2'):
                allure.attach.file(source="cases_screenshot/p1.jpg",name='输入用户名截图',attachment_type=allure.attachment_type.JPG,extension="jpg")
        with allure.step('第三步：测试步骤3'): pass

        print('测试用例2')
        assert 1==1


    @allure.story('接口名称：登录接口')
    @allure.title('验证错误密码')
    def test_3(self):
        print('测试用例3')
        assert '奥特曼' in '迪迦奥特曼'