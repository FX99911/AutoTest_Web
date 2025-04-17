import os
import time
import allure
from web_keys.seleniuum_device.keys import Keys
from web_keys.read_excel.dist_to_variable import convert_dict_to_variables, get_all_steps
from web_keys.template_method.get_now_file_name import get_now_file_name
from web_keys.read_excel.modify_excel_dict import  convert_list_to_by
# 测试用例数据
project_info = {
    '项目名称': ['六代战斗机项目'],
    '模块名称': ['导航'],
    '测试点': ['导航到-美国'],
    'nan': ['nan']
}

# 操作步骤
operation_steps = {
    '打开_url_登录': ['https://www.qq.com', 'nan', 'nan'],
    '截图': ['nan', 'nan', 'nan']
}

# 后续可以在这里添加测试逻辑

# 定义项目信息变量
project_name = project_info['项目名称'][0]
test_module	= project_info['模块名称'][0]
test_points = project_info['测试点'][0]
cases_name = get_now_file_name()  #文件名
print(cases_name)

# # 步骤变量定义(暂时不需要)
# all_steps = convert_dict_to_variables(operation_steps)

# 获取列表
all_steps = get_all_steps(operation_steps)

picture_url = os.path.join("reports/cases_screenshot", project_name, test_module, test_points)
picture_name = cases_name

# =====================以下是测试用例模板====================
########################

@allure.epic(f'项目名称：{project_name}')
@allure.feature(f"模块名称：{test_module}")
@allure.description('说明：这是一个说明描述，描述写这里') # 描述

class Test_Template(Keys):

    @allure.story(f'测试点：{test_points}')
    @allure.title(f'测试用例名：{cases_name}')
    @allure.link(url='http://www.baidu.com', name='这是一个链接')

    def test_execute(self):  #这个就是定义一个(用例)，test_开头
        self.start_chrome() #单线程用这个
        # self.start_chrome_n() #多线程用这个

        time.sleep(1)
        print('等待5秒启动浏览器')
        num = 0
        for step in all_steps:
            step = convert_list_to_by(step)
            print(f'当前测试步骤信息{step}')
            num += 1

            if '打开_url' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.open(step[1])
            elif '输入' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.input(step[1], step[2], step[3])
            elif '点击' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.click(step[1], step[2])
            elif '断言' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    # 加入文件附件（错误截图）
                    picture= self.take_screenshot(picture_url,picture_name)
                    allure.attach.file(source=picture, name=f'{picture_name}',
                                       attachment_type=allure.attachment_type.JPG, extension="jpg")
                    assert self.text(step[1], step[2]) == step[3]
            elif '关闭浏览器' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.quit()
            elif '刷新页面' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.refresh()
            elif '清空输入框' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.clear_box(step[1], step[2])
            elif '强制等待' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.wait(step[1])
            elif '返回上一页' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.driver.back()
            elif '前进下一页' in step[0] :
                with allure.step(f'第{num}步：{step[0]}'):
                    self.driver.forward()
            elif '截图' in step[0]:
                with allure.step(f'第{num}步：{step[0]}'):
                    picture= self.take_screenshot(picture_url,picture_name)
                    allure.attach.file(source=picture, name=f'{picture_name}',
                                       attachment_type=allure.attachment_type.JPG, extension="jpg")



