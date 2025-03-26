"""
这是基类，基本常用的函数
这是关键字驱动类的封装，主要用于做Selenium常用操作行为的提取，与二次封装
    1.0pen
    2.send keys
    3.click
    4.find element
    5.quit
    6. .......


"""
import time

# ####导包#用于设置谷歌浏览器####
from selenium.webdriver.chrome.options import Options
# ####导包#用于管理驱动####
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
#-----------------------
pc = 'mac' #电脑是win/还是mac  <<<<<<<<<<这里需要修改电脑是啥<<<<<<<<<<<<
isH5 = 'yes' # 是不是H5界面。填写yes/no。<<<<<<<<<<这里需要修改界面是不是H5<<<<<<<<<<<<

Win_chromedriver_url = '/Users/wang/PycharmProjects/AtouTest_Web/config/chromedriver.exe' 
Mac_chromedriver_url = '/Users/wang/PycharmProjects/AtouTest_Web/config/chromedriver'
#-----------------------
class Keys:

    # def __init__(self):
    #     # 在初始化时启动浏览器，并保存 driver 到实例属性
    #     self.driver = self.start_chrome()


    # 打开chrome浏览器
    def start_chrome(self):

        if pc == 'win' and isH5 == 'no':
            #### 创建设置浏览器对象(不需要动)####
            self.opt1 = Options()
            #### 禁用沙盒模式(不需要动)(可用可不用，增加兼容性，不兼容可添加)####
            self.opt1.add_argument('--no-sandbox')
            #### 保持浏览器打开状态(不需要动)####
            self.opt1.add_experimental_option('detach', True)
            #### 设置浏览器缩放比例70%####
            self.opt1.add_argument('--force-device-scale-factor=0.7')
            #### 配置启动文件路径，并且使用opt1的设置，启动浏览器####
            self.driver = webdriver.Chrome(service=Service(Win_chromedriver_url), options=self.opt1)
            #### 隐性等待时间配置10s
            self.driver.implicitly_wait(10)
            return self.driver

        elif pc == 'mac' and isH5 == 'no':
            #### 创建设置浏览器对象(不需要动)####
            self.opt1 = Options()
            #### 保持浏览器打开状态(不需要动)####
            self.opt1.add_experimental_option('detach', True)
            #### 配置启动文件路径，并且使用opt1的设置，启动浏览器####
            self.driver = webdriver.Chrome(service=Service(Mac_chromedriver_url), options=self.opt1)
            #### 隐性等待时间配置10s
            self.driver.implicitly_wait(10)
            return self.driver

        elif pc == 'mac' and isH5 == 'yes':
            #### 创建设置浏览器对象(不需要动)####
            self.opt1 = Options()
            #### 保持浏览器打开状态(不需要动)####
            self.opt1.add_experimental_option('detach', True)
            #### 设置H5模式
            self.opt1.add_experimental_option("mobileEmulation",{"deviceName": "iPhone 15"} )
            #### 配置启动文件路径，并且使用opt1的设置，启动浏览器####
            self.driver = webdriver.Chrome(service=Service(Mac_chromedriver_url), options=self.opt1)
            #### 隐性等待时间配置10s
            self.driver.implicitly_wait(10)
            return self.driver
        elif pc == 'win' and isH5 == 'yes':
            #### 创建设置浏览器对象(不需要动)####
            self.opt1 = Options()
            #### 禁用沙盒模式(不需要动)(可用可不用，增加兼容性，不兼容可添加)####
            self.opt1.add_argument('--no-sandbox')
            #### 保持浏览器打开状态(不需要动)####
            self.opt1.add_experimental_option('detach', True)
            #### 设置浏览器缩放比例70%####
            self.opt1.add_argument('--force-device-scale-factor=0.7')
            #### 设置H5模式
            self.opt1.add_experimental_option("mobileEmulation", {"deviceName": "iPhone 15"})
            #### 配置启动文件路径，并且使用opt1的设置，启动浏览器####
            self.driver = webdriver.Chrome(service=Service(Win_chromedriver_url), options=self.opt1)
            #### 隐性等待时间配置10s
            self.driver.implicitly_wait(10)
            return self.driver

        else:
            print('pc只能输入：win/mac ，isH5只能输入：yes/no且必须为字符串')

    # 访问URL
    def open(self,url):
        self.driver.get(url)

    # 查找元素，能满足不同场景下的不同元素定位方法
    # def locator(self,by,value):
    #     return self.driver.find_element(by,value)
    def locator(self,by,value):
        return self.driver.find_element(by,value)   #

    # 输入
    def input(self,by,value,txt):
        self.locator(by,value).send_keys(txt)


    # 点击
    def click(self,by,value):
        self.locator(by,value).click()


    # 关闭浏览器
    def quit(self):
        self.driver.quit()

    # 切换句柄
    def switch_window(self,close=None,num=1):
        handles = self.driver.window_handles
        if close is not None:
            self.driver.close()
        self.driver.switch_to.window(handles[num])

    # 强制等待
    def wait(self,_time):
        time.sleep(int(_time))

    #
    def title(self):
        return self.driver.title

    # 获取元素的文本内容
    def text(self,by,value):
        text = self.driver.find_element(by,value).text
        return text