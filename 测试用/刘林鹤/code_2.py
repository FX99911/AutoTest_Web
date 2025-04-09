# from 测试用.刘林鹤.start_chrome import  start_chrome
#
# # 第二个文件调用，继续使用
# device = start_chrome()
# device.get("https://www.qq.com")


from 测试用.刘林鹤.browser_manager import browser_manager
device = browser_manager.start_browser()
device.get("https://www.qq.com")
print(">>> 已启动浏览器，打开百度")

# from web_keys.seleniuum_device.keys import browser_manager
# browser_manager.start_chrome()
# browser_manager.open('https://www.qq.com')