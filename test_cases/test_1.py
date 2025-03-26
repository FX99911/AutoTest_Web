import allure
import pytest

@allure.epic('项目名称：奥里给科技自动化测试报告')
@allure.feature("模块名称：用户管理模块")
class TestApi:
    age = 18

    # def setup_class(self):   #类-前置操作固定名字
    #     print('每个类之[前]的操作，每个类只执行一次')
    #
    # def teardown_class(self):   #类-后置操作固定名字
    #     print('每个类之[后]的操作，每个类只执行一次')
    #
    # def setup_method(self):  # 用例的-前置操作固定名字
    #     print('每个用例之[前]的操作，每个用例只执行一次')
    #
    # def teardown_method(self):  #用例的-后置操作固定名字
    #     print('每个用例之[后]的操作，每个用例只执行一次')

    #@pytest.fixture(scope='作用域',autouse='自动/手动',params='参数化',ids='参数化时参数的别名')
    @allure.story('接口名称：登录接口')
    def test_login(self):
        print('登录测试用例')
        raise Exception('登录出现异常了')

    @allure.story('接口名称：登录接口')
    def test_register(self):
        print('注册测试用例')
    @pytest.mark.run(order=1)# 改变测试用例执行顺序
    @allure.story('接口名称：登录接口')
    def test_add_user(self):
        print('增加用户')

    @allure.story('接口名称：登录接口')
    @pytest.mark.users
    def test_del_user(self):
        print('删除用户')

    @pytest.mark.skip(reason='无条件跳过，跳过原因写这里')  # 直接跳过
    @pytest.mark.order
    @allure.story('接口名称：跳过接口')
    def test_select_order(self):
        print('查询工单')

    @pytest.mark.skipif(age<=20,reason='有条件跳过，跳过原因写这里')  # 满足条件就跳过
    @pytest.mark.order
    @allure.story('接口名称：跳过接口')
    def test_comeon_order(self):
        print('接收工单')

    @pytest.mark.order # 打标记
    @allure.story('接口名称：工单接口')
    def test_add_order(self):
        print('新增工单')

    @pytest.mark.order
    @allure.story('接口名称：工单接口')
    def test_del_order(self):
        print('删除工单')
