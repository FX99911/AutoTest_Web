from selenium.webdriver.common.by import By
from web_keys.seleniuum_device.keys import Keys

keys = Keys()  # 这里会自动获取或创建浏览器实例
keys.start_chrome()  # 现在会优先复用现有浏览器实例
keys.open('https://www.baidu.com/')
keys.wait(1)
keys.input(By.ID,'kw','2222222')
keys.wait(1)
keys.click(By.ID,'su')
keys.wait(2)