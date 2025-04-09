from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def start_chrome():
    # 创建 ChromeOptions
    chrome_options = Options()
    # 指定远程调试端口，比如 9222
    chrome_options.add_argument("--remote-debugging-port=9222")
    # 指定一个独立的用户数据目录，避免和手动打开的Chrome冲突
    chrome_options.add_argument("--user-data-dir=/tmp/selenium_profile")
    
    # 如果 chromedriver 在 PATH 里，可以 Service() 直接用；否则传入绝对路径
    service = Service('/Users/wang/PycharmProjects/AtouTest_Web/config/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get("https://www.baidu.com")
    print(">>> 脚本A：已启动浏览器，打开百度，远程调试端口 9222。")
    print(">>> 此脚本将暂停等待，不会调用 driver.quit()，确保浏览器保持打开状态。")
    
    input("按下回车后结束脚本A，但浏览器仍保持不关闭（因为我们没调用 driver.quit()）\n")


