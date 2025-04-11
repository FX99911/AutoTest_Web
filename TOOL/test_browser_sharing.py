import time
import pytest
from web_keys.seleniuum_device.keys_2 import Keys, _global_driver

class Test_First(Keys):
    """第一个测试类"""
    
    def test_first(self):
        """第一个测试方法"""
        print("\n--- 第一个测试开始 ---")
        print(f"全局浏览器实例: {_global_driver}")
        print(f"当前浏览器实例: {self.driver}")
        
        # 打开百度
        self.open("https://www.baidu.com")
        self.wait(1)
        print(f"当前页面标题: {self.title()}")
        
        # 打印标识符，确认是同一个浏览器实例
        print(f"浏览器实例ID: {id(self.driver)}")
        print("--- 第一个测试结束 ---")

class Test_Second(Keys):
    """第二个测试类"""
    
    def test_second(self):
        """第二个测试方法"""
        print("\n--- 第二个测试开始 ---")
        print(f"全局浏览器实例: {_global_driver}")
        print(f"当前浏览器实例: {self.driver}")
        
        # 打开必应
        self.open("https://www.bing.com")
        self.wait(1)
        print(f"当前页面标题: {self.title()}")
        
        # 打印标识符，确认是同一个浏览器实例
        print(f"浏览器实例ID: {id(self.driver)}")
        print("--- 第二个测试结束 ---")
        
    def test_third(self):
        """第三个测试方法"""
        print("\n--- 第三个测试开始 ---")
        print(f"全局浏览器实例: {_global_driver}")
        print(f"当前浏览器实例: {self.driver}")
        
        # 打开谷歌
        self.open("https://www.google.com")
        self.wait(1)
        print(f"当前页面标题: {self.title()}")
        
        # 打印标识符，确认是同一个浏览器实例
        print(f"浏览器实例ID: {id(self.driver)}")
        print("--- 第三个测试结束 ---")
        
        # 最后一个测试结束后关闭浏览器
        print("测试结束，关闭浏览器")
        self.quit_browser() 