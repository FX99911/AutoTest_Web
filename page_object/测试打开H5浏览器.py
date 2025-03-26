from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 配置 Chrome 选项
chrome_options = Options()
# 启动时直接打开开发者工具
chrome_options.add_argument("--auto-open-devtools-for-tabs")

# 创建 Chrome 浏览器实例
driver = webdriver.Chrome(service=Service('/Users/wang/PycharmProjects/AtouTest_Web/config/chromedriver'),
                          options=chrome_options)

try:
    # 打开网页
    driver.get('http://10.1.64.85/zjh5/')

    # 使用显式等待定位并点击响应式设计模式按钮
    # 尝试使用 XPath 选择器，不同 Chrome 版本可能需要调整
    responsive_button_xpath = '//button[@aria-label="Toggle device toolbar"]'
    wait = WebDriverWait(driver, 10)
    responsive_button = wait.until(EC.element_to_be_clickable((By.XPATH, responsive_button_xpath)))
    responsive_button.click()

    # 等待响应式设计模式加载
    time.sleep(2)

    # 可以在这里添加更多的自动化操作

    # 等待用户输入，防止浏览器立即关闭
    input("按回车键退出...")

except Exception as e:
    print(f"发生错误: {e}")

finally:
    # 关闭浏览器
    driver.quit()
