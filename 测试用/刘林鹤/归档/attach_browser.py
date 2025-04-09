from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def attach_chrome():
    chrome_options = Options()
    # 注意要与 start_browser.py 所指定端口一致
    chrome_options.debugger_address = "127.0.0.1:9222"
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print(">>> 脚本B：已连接到正在远程调试的Chrome。")
    
    driver.get("https://www.zhihu.com")
    print(">>> 在同一个浏览器窗口里跳转到知乎。")
    
    input("脚本B等待输入，不会调用quit()。按回车后脚本结束，浏览器保持不关闭\n")

if __name__ == "__main__":
    attach_chrome()
