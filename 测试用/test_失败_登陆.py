# 后续可以在这里添加测试逻辑
import time
import allure
from selenium.webdriver.common.by import By
from web_keys.seleniuum_device.keys import Keys
test_project_info = {'项目名称': ['测试的项目'], '模块名称': ['首页'], '测试点': ['登陆'], 'nan': ['nan']}

# 测试用例数据
test_data = {'打开_浏览器': ['nan', 'nan', 'nan'], '打开_url_登录': ['https://adminplus.iviewui.com/', 'nan', 'nan'], '输入_用户名': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[1]/div/div/div/input', 'admin'], '输入_密码': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[2]/div/div/div/input', 'admin'], '点击_登录按钮': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[4]/button', 'nan'], '断言': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[4]/button', '登陆成功']}

for x in test_project_info:
    print(test_data)

for y in test_data:
    print(test_data)




