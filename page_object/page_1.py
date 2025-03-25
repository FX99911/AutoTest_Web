from selenium.webdriver.common.by import By
from web_keys.keys import Keys

keys = Keys()

keys.start_chrome()
keys.open('https://www.baidu.com/')
keys.wait(1)
keys.input(By.ID,'kw','马克思主义核心思想')

keys.wait(1)
keys.click(By.ID,'su')
keys.wait(2)
keys.quit()