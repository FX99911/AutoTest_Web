from selenium.webdriver.common.by import By
from web_keys.seleniuum_device.keys import Keys

'''
这是一个测试类（模板）
-百度搜索页面的对象，用于实现百度搜索的业务流程
-由：url、 核心元素 、核心业务 组成
'''

class Search(Keys): #模板

    #### url ####
    url = 'https://www.baidu.com/'

    #### 核心元素 ###
    el_input = [By.ID,'kw'] #使用ID定位，元素：kw
    el_button = [By.ID,'su']

        #### 核心业务  #### （百度搜索）
    def baiduSearch(self,txt):
        self.start_chrome('mac')
        self.open(self.url)
        self.input(self.el_input[0],self.el_input[1],txt)
        self.click(self.el_button[0],self.el_button[1])
        self.wait(2)
        title = self.title()
        print(title)
        self.quit()

        return title


Search().baiduSearch('123465')