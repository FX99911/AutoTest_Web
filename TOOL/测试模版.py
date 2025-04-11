import time
import allure
import pytest
import logging
from web_keys.seleniuum_device.keys_2 import Keys
from web_keys.read_excel.dist_to_variable import convert_dict_to_variables, get_all_steps
from web_keys.template_method.get_now_file_name import get_now_file_name
from web_keys.read_excel.modify_excel_dict import convert_list_to_by

# 配置日志
logger = logging.getLogger("TestTemplate")

# 测试用例数据
project_info = {
    '项目名称': ['测试的项目'],
    '模块名称': ['首页'],
    '测试点': ['登陆'],
    'nan': ['nan']
}

# 操作步骤
operation_steps = {
    '打开_浏览器': ['yes', 'nan', 'nan'],
    '打开_url_登录': ['https://adminplus.iviewui.com/', 'nan', 'nan'],
    '输入_用户名': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[1]/div/div/div/input', 'admin'],
    '输入_密码': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[2]/div/div/div/input', 'admin'],
    '点击_登录按钮': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[4]/button', 'nan'],
    '断言': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[1]/span/span[2]', 'Aresn']
}

# 定义项目信息变量
project_name = project_info['项目名称'][0]
test_module = project_info['模块名称'][0]
test_points = project_info['测试点'][0]
cases_name = get_now_file_name()

# 获取列表
all_steps = get_all_steps(operation_steps)

@allure.epic(f'项目名称：{project_name}')
@allure.feature(f"模块名称：{test_module}")
@allure.description('说明：这是一个说明描述，描述写这里')  # 描述
class Test_Template(Keys):
    """
    测试模板类，直接继承Keys类
    使用共享浏览器实例
    """
    
    @classmethod
    def setup_class(cls):
        """类级别初始化，确保只执行一次"""
        logger.info("Test_Template setup_class 开始")
        super().setup_class()
        logger.info("Test_Template setup_class 结束")
    
    @classmethod
    def teardown_class(cls):
        """类级别清理，确保只执行一次"""
        logger.info("Test_Template teardown_class 开始")
        super().teardown_class()
        logger.info("Test_Template teardown_class 结束")
    
    def setup_method(self, method):
        """方法级别初始化"""
        logger.info(f"Test_Template setup_method 开始 - 方法名: {method.__name__}")
        super().setup_method(method)
        logger.info(f"Test_Template setup_method 结束 - 方法名: {method.__name__}")

    @allure.story(f'测试点：{test_points}')
    @allure.title(f'测试用例名：{cases_name}')
    @allure.link(url='http://www.baidu.com', name='这是一个链接')
    def test_execute(self):  # 这个就是定义一个(用例)，test_开头
        # 浏览器会在setup_method中自动启动或重用
        logger.info("开始执行测试用例")
        num = 0
        for step in all_steps:
            step = convert_list_to_by(step)
            logger.info(f'当前测试步骤信息: {step}')
            num += 1

            if '打开_url' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.open(step[1])
                    self.wait(1)
            elif '输入' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.input(step[1], step[2], step[3])
                    self.wait(1)
            elif '点击' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.click(step[1], step[2])
                    self.wait(1)
            elif '断言' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    assert self.text(step[1], step[2]) == step[3]
            elif '关闭浏览器' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    # 不关闭浏览器，只是清空当前页面
                    self.driver.get("about:blank")
            elif '刷新页面' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.refresh()
            elif '清空输入框' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.clear_box(step[1], step[2])
            elif '强制等待' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.wait(step[1])
            elif '返回上一页' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.driver.back()
            elif '前进下一页' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.driver.forward()
            elif '截图' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    self.refresh()
        
        logger.info("测试用例执行完成") 