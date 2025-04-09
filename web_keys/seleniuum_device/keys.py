"""
这是基类，基本常用的函数
这是关键字驱动类的封装，主要用于做Selenium常用操作行为的提取，与二次封装
    1.0pen - 打开URL
    2.send keys - 输入文本
    3.click - 点击元素
    4.find element - 查找元素
    5.quit - 关闭浏览器
    6.等待操作 - 显式和隐式等待
    7.浏览器窗口操作 - 最大化、切换等
    8.下拉框操作 - 选择选项
    9.JavaScript操作 - 执行JS脚本
    10.屏幕截图 - 保存截图
    11.警告框处理 - 接受、拒绝、获取文本
    12.iframe操作 - 切换iframe
    13.滚动操作 - 页面滚动
    14.鼠标和键盘操作 - 悬停、拖拽等
"""
import time
import os
from datetime import datetime

# ####导包#用于设置谷歌浏览器####
from selenium.webdriver.chrome.options import Options
# ####导包#用于管理驱动####
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import json
from web_keys.environment_info.montage_url import home

# ####导入常用的Selenium辅助模块####
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)
from web_keys.seleniuum_device.browser_manager import BrowserManager

# ----------#获取项目根目录#----------------------
# home = get_project_root_path()
#
# # ----------#初始参数信息#----------------------
# pc_type = None  # 电脑是win/还是mac  <<<<<<<<<<配置文件读取<<<<<<<<<<<<
# is_h5 = None  # 是不是H5界面。填写yes/no。<<<<<<<<<<配置文件读取<<<<<<<<<<<<
# note = None  # 其他信息，暂时没用
#
# # ----------#用根目录拼接目录url,#----------------------
# # 根据不同操作系统设置ChromeDriver路径
# Win_chromedriver_url = f'{home}/config/chromedriver.exe'
# Mac_chromedriver_url = f'{home}/config/chromedriver'
# config_url = f'{home}/config/start_config.json'
#
# # ----------#去配置文件读取参数#----------------------
# try:
#     # 以读取模式打开配置文件
#     with open(config_url, 'r') as f:
#         # 加载 JSON 数据到 Python 字典
#         config = json.load(f)
#         # 从字典中获取具体配置项
#         pc_type = config.get('pc_type')
#         is_h5 = config.get('is_h5')
#         note = config.get('note')
#         print(f"操作系统类型: {pc_type}")
#         print(f"是否H5项目: {is_h5}")
#         print(f"备注信息: {note}")
# except FileNotFoundError:
#     print("error:未找到配置文件，请检查文件路径。")
# except json.JSONDecodeError:
#     print("error:配置文件不是有效的 JSON 格式，请检查文件内容。")
# except Exception as e:
#     print(f"error:读取配置文件时出现其他错误: {e}")
#

# -----------------------
class Keys:
    """
    Selenium操作封装类，提供常用的浏览器操作方法
    """

    # def __init__(self):
    #     # 在初始化时启动浏览器，并保存 driver 到实例属性
    #     self.driver = self.start_chrome()
    #
    # def start_chrome(self):
    #     """
    #     启动Chrome浏览器并返回WebDriver实例
    #     根据配置文件中的pc_type决定使用哪个驱动路径
    #
    #     Returns:
    #         WebDriver: 配置好的Chrome WebDriver实例
    #     """
    #     if pc_type == 'win':
    #         try:
    #             # 创建设置浏览器对象
    #             self.opt1 = Options()
    #             # 禁用沙盒模式(增加兼容性)
    #             self.opt1.add_argument('--no-sandbox')
    #             # 保持浏览器打开状态
    #             self.opt1.add_experimental_option('detach', True)
    #             # 设置浏览器缩放比例70%
    #             self.opt1.add_argument('--force-device-scale-factor=0.7')
    #             # 配置启动文件路径，并且使用opt1的设置，启动浏览器
    #             self.driver = webdriver.Chrome(service=Service(Win_chromedriver_url), options=self.opt1)
    #             # 隐性等待时间配置10s
    #             self.driver.implicitly_wait(10)
    #             return self.driver
    #         except Exception as e:
    #             print(f"【error:】打开浏览器失败: {e}")
    #
    #     elif pc_type == 'mac':
    #         try:
    #             # 创建设置浏览器对象
    #             self.opt1 = Options()
    #             # 保持浏览器打开状态
    #             self.opt1.add_experimental_option('detach', True)
    #             # 配置启动文件路径，并且使用opt1的设置，启动浏览器
    #             self.driver = webdriver.Chrome(service=Service(Mac_chromedriver_url), options=self.opt1)
    #             # 隐性等待时间配置10s
    #             self.driver.implicitly_wait(10)
    #             return self.driver
    #         except Exception as e:
    #             print(f"【出现错误】打开浏览器失败: {e}")
    #
    #



    def start_chrome(self):
        self.driver = BrowserManager().start_browser()

    def open(self, url):
        """
        访问指定URL
        """
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"错误：打开URL失败 - {str(e)}")

    def locator(self, by, value):
        """
        查找元素
        """
        try:
            return self.driver.find_element(by, value)
        except Exception as e:
            print(f"错误：查找元素失败 - {str(e)}")
            return None

    def find_elements(self, by, value):
        """
        查找多个元素

        Args:
            by: 定位方式，如By.ID, By.XPATH等
            value: 定位值

        Returns:
            list: 找到的所有元素列表
        """
        return self.driver.find_elements(by, value)

    def input(self, by, value, txt):
        """
        在指定元素中输入文本
        """
        try:
            self.locator(by, value).send_keys(txt)
        except Exception as e:
            print(f"错误：输入文本失败 - {str(e)}")

    def clear_box(self, by, value):
        """
        清空元素中的内容

        Args:
            by: 定位方式
            value: 定位值
        """
        element = self.locator(by, value)
        element.clear()

    def click(self, by, value):
        """
        点击指定元素
        """
        try:
            self.locator(by, value).click()
        except Exception as e:
            print(f"错误：点击元素失败 - {str(e)}")

    def quit(self):
        """
        关闭浏览器并清理资源
        只有在浏览器正在运行时才会执行关闭操作。
        """
        browser_manager.close_browser()

    def close(self):
        """
        关闭当前窗口，但保持浏览器会话
        """
        self.driver.close()

    def switch_window(self, close=None, num=1):
        """
        切换到指定的浏览器窗口

        Args:
            close: 是否关闭当前窗口
            num: 要切换到的窗口索引
        """
        handles = self.driver.window_handles
        if close is not None:
            self.driver.close()
        self.driver.switch_to.window(handles[num])

    def wait(self, _time):
        """
        强制等待指定秒数

        Args:
            _time: 等待的秒数
        """
        time.sleep(int(_time))

    def title(self):
        """
        获取当前页面标题

        Returns:
            str: 页面标题
        """
        return self.driver.title

    def text(self, by, value):
        """
        获取元素的文本内容

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            str: 元素的文本内容
        """
        text = self.driver.find_element(by, value).text
        return text

    def wait_for_element(self, by, value, timeout=10):
        """
        显式等待元素出现
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"错误：等待元素失败 - {str(e)}")
            return None

    def wait_for_element_clickable(self, by, value, timeout=10):
        """
        等待元素可点击
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except Exception as e:
            print(f"错误：等待元素可点击失败 - {str(e)}")
            return None

    def wait_for_element_visible(self, by, value, timeout=10):
        """
        等待元素可见
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"错误：等待元素可见失败 - {str(e)}")
            return None

    def maximize_window(self):
        """
        最大化浏览器窗口
        """
        self.driver.maximize_window()

    def refresh(self):
        """
        刷新当前页面
        """
        self.driver.refresh()

    def back(self):
        """
        返回上一页
        """
        self.driver.back()

    def forward(self):
        """
        前进到下一页
        """
        self.driver.forward()

    def execute_script(self, script, *args):
        """
        执行JavaScript脚本

        Args:
            script: 要执行的JavaScript代码
            *args: 传递给JavaScript的参数

        Returns:
            执行JavaScript后的返回值
        """
        return self.driver.execute_script(script, *args)

    def take_screenshot(self, file_name=None):
        """
        截取当前页面的屏幕截图

        Args:
            file_name: 截图文件名，如果为None则使用当前时间戳

        Returns:
            str: 保存的截图文件路径
        """
        if file_name is None:
            time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"screenshot_{time_str}.png"

        # 确保截图目录存在
        screenshot_dir = os.path.join(home, 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)

        file_path = os.path.join(screenshot_dir, file_name)
        self.driver.save_screenshot(file_path)
        print(f"截图已保存: {file_path}")
        return file_path

    def select_by_text(self, by, value, text):
        """
        通过文本选择下拉框选项

        Args:
            by: 定位方式
            value: 定位值
            text: 要选择的选项文本
        """
        select = Select(self.locator(by, value))
        select.select_by_visible_text(text)

    def select_by_value(self, by, value, option_value):
        """
        通过value属性选择下拉框选项

        Args:
            by: 定位方式
            value: 定位值
            option_value: 选项的value属性值
        """
        select = Select(self.locator(by, value))
        select.select_by_value(option_value)

    def select_by_index(self, by, value, index):
        """
        通过索引选择下拉框选项

        Args:
            by: 定位方式
            value: 定位值
            index: 选项的索引
        """
        select = Select(self.locator(by, value))
        select.select_by_index(index)

    def get_selected_option_text(self, by, value):
        """
        获取下拉框中已选选项的文本

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            str: 已选选项的文本
        """
        select = Select(self.locator(by, value))
        return select.first_selected_option.text

    def get_all_options(self, by, value):
        """
        获取下拉框中所有选项

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            list: 所有选项元素的列表
        """
        select = Select(self.locator(by, value))
        return select.options

    def accept_alert(self):
        """
        接受警告框
        """
        alert = self.driver.switch_to.alert
        alert.accept()

    def dismiss_alert(self):
        """
        取消警告框
        """
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def get_alert_text(self):
        """
        获取警告框文本

        Returns:
            str: 警告框中的文本
        """
        alert = self.driver.switch_to.alert
        return alert.text

    def send_text_to_alert(self, text):
        """
        向警告框发送文本

        Args:
            text: 要发送的文本
        """
        alert = self.driver.switch_to.alert
        alert.send_keys(text)

    def switch_to_frame(self, frame_reference):
        """
        切换到指定的iframe

        Args:
            frame_reference: iframe的引用，可以是id、name、index或WebElement
        """
        self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self):
        """
        切换回主文档
        """
        self.driver.switch_to.default_content()

    def hover(self, by, value):
        """
        鼠标悬停在元素上

        Args:
            by: 定位方式
            value: 定位值
        """
        element = self.locator(by, value)
        ActionChains(self.driver).move_to_element(element).perform()

    def drag_and_drop(self, source_by, source_value, target_by, target_value):
        """
        拖放操作

        Args:
            source_by: 源元素定位方式
            source_value: 源元素定位值
            target_by: 目标元素定位方式
            target_value: 目标元素定位值
        """
        source = self.locator(source_by, source_value)
        target = self.locator(target_by, target_value)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def scroll_to_element(self, by, value):
        """
        滚动到指定元素

        Args:
            by: 定位方式
            value: 定位值
        """
        element = self.locator(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_position(self, x, y):
        """
        滚动到指定位置

        Args:
            x: x坐标
            y: y坐标
        """
        self.driver.execute_script(f"window.scrollTo({x}, {y});")

    def scroll_to_bottom(self):
        """
        滚动到页面底部
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self):
        """
        滚动到页面顶部
        """
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_attribute(self, by, value, attribute):
        """
        获取元素的属性值

        Args:
            by: 定位方式
            value: 定位值
            attribute: 要获取的属性名

        Returns:
            str: 属性值
        """
        element = self.locator(by, value)
        return element.get_attribute(attribute)

    def is_element_present(self, by, value):
        """
        检查元素是否存在

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            bool: 元素存在返回True，否则返回False
        """
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def is_element_displayed(self, by, value):
        """
        检查元素是否可见

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            bool: 元素可见返回True，否则返回False
        """
        try:
            return self.driver.find_element(by, value).is_displayed()
        except NoSuchElementException:
            return False

    def is_element_enabled(self, by, value):
        """
        检查元素是否启用

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            bool: 元素启用返回True，否则返回False
        """
        try:
            return self.driver.find_element(by, value).is_enabled()
        except NoSuchElementException:
            return False

    def is_element_selected(self, by, value):
        """
        检查元素是否被选中（如复选框、单选按钮）

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            bool: 元素被选中返回True，否则返回False
        """
        try:
            return self.driver.find_element(by, value).is_selected()
        except NoSuchElementException:
            return False

    def get_page_source(self):
        """
        获取当前页面的源代码

        Returns:
            str: 页面源代码
        """
        return self.driver.page_source

    def get_current_url(self):
        """
        获取当前页面的URL

        Returns:
            str: 当前页面URL
        """
        return self.driver.current_url

    def get_browser(self):
        """
        获取浏览器实例
        """
        if not self.is_browser_running():
            try:
                self.driver = self.start_chrome()
                self.is_browser_open = True
                return self.driver
            except Exception as e:
                print(f"错误：启动浏览器失败 - {str(e)}")
                return None
        return self.driver

    def is_browser_running(self):
        """
        检查浏览器是否正在运行
        """
        return self.is_browser_open and self.driver is not None


# A = Keys()
# A.start_chrome()
# A.open('https://www.baidu.com/')