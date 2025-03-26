from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 配置 Chrome 选项
chrome_options = Options()

service = Service(ChromeDriverManager().install())

# 创建 Chrome 浏览器实例
driver = webdriver.Chrome(service=Service('/Users/wang/PycharmProjects/AtouTest_Web/config/chromedriver'), options=chrome_options)

try:

    driver.get('https://www.baidu.com')

    # CDP命令
    # 设置移动端设备参数
    device_metrics = {
        "width": 375,
        "height": 812,
        "deviceScaleFactor": 3,
        "mobile": True
    }
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", device_metrics)
    driver.execute_cdp_cmd("Emulation.setUserAgentOverride", {
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                     "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"})

    # 验证页面是否正常加载
    print("当前页面标题:", driver.title)
    print("当前页面URL:", driver.current_url)

    # 等待用户输入，防止浏览器立即关闭
    input("按回车键退出...")

except Exception as e:
    print(f"发生错误: {e}")

finally:
    # 关闭浏览器
    driver.quit()
