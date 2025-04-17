import json
import os
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from web_keys.environment_info.montage_url import home


class BrowserManager:
    """
    浏览器管理器类，使用单例模式确保全局只有一个浏览器实例。
    负责浏览器的启动、连接和关闭操作。
    """
    # ----------#初始参数信息#----------------------
    pc_type = None  # 电脑是win/还是mac  <<<<<<<<<<配置文件读取<<<<<<<<<<<<
    is_h5 = None  # 是不是H5界面。填写yes/no。<<<<<<<<<<配置文件读取<<<<<<<<<<<<
    note = None  # 其他信息，暂时没用

    # ----------#用根目录拼接目录url,#----------------------
    # 根据不同操作系统设置ChromeDriver路径
    # Win_chromedriver_url = f'{home}/config/chromedriver.exe'
    Win_chromedriver_url = os.path.join(home, 'config', 'chromedriver.exe')
    print(f'win浏览器驱动{Win_chromedriver_url}')
    # Mac_chromedriver_url = f'{home}/config/chromedriver'
    Mac_chromedriver_url = os.path.join(home, 'config', 'chromedriver')
    print(f'mac浏览器驱动{Mac_chromedriver_url}')
    # config_url = f'{home}/config/start_config.json'
    config_url = os.path.join(home, 'config', 'start_config.json')
    print(f'配置文件{config_url}')
    # ----------#去配置文件读取参数#----------------------
    try:
        # 以读取模式打开配置文件
        with open(config_url, 'r') as f:
            # 加载 JSON 数据到 Python 字典
            config = json.load(f)
            # 从字典中获取具体配置项
            pc_type = config.get('pc_type')
            is_h5 = config.get('is_h5')
            note = config.get('note')
            print(f"操作系统类型: {pc_type}")
            print(f"是否H5项目: {is_h5}")
            print(f"备注信息: {note}")
    except FileNotFoundError:
        print("error:未找到配置文件，请检查文件路径。")
    except json.JSONDecodeError:
        print("error:配置文件不是有效的 JSON 格式，请检查文件内容。")
    except Exception as e:
        print(f"error:读取配置文件时出现其他错误: {e}")

    _instance = None  # 单例实例
    driver = None  # 浏览器驱动实例
    _is_browser_running = False  # 浏览器运行状态标志
    _port = 9222  # 远程调试端口号

    def __new__(cls):
        """
        实现单例模式，确保全局只有一个浏览器管理器实例。

        Returns:
            BrowserManager: 浏览器管理器实例
        """
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化浏览器管理器，设置chromedriver路径。
        使用initialized标志确保只初始化一次。
        """
        if not hasattr(self, 'initialized'):

            # 根据操作系统选择chromedriver路径
            if self.pc_type == 'window':
                self.chromedriver_path = self.Win_chromedriver_url
            elif self.pc_type == 'mac':
                self.chromedriver_path = self.Mac_chromedriver_url
            self.initialized = True

    @classmethod
    def get_instance(cls):
        """
        获取浏览器管理器实例的类方法。

        Returns:
            BrowserManager: 浏览器管理器实例
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _is_port_in_use(self):
        """
        检查远程调试端口是否被使用，用于判断浏览器是否已经运行。

        Returns:
            bool: 如果端口被使用返回True，否则返回False
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', self._port)) == 0

    def start_browser(self):
        """
        启动或连接浏览器。
        如果检测到已有浏览器运行，则连接到该浏览器；
        否则启动新的浏览器实例。

        Returns:
            webdriver.Chrome: Chrome浏览器驱动实例
        """
        if not self._is_browser_running:
            print(">>> 正在检查浏览器状态...")
            chrome_options = Options()
            # 基本浏览器设置
            # chrome_options.add_argument('--force-device-scale-factor=0.7')  #
            chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
            chrome_options.add_argument('--no-sandbox')  # 禁用沙盒模式

            # 根据是否为H5项目设置不同的选项
            if self.is_h5.lower() == 'yes':
                print(">>> 检测到H5项目，设置移动设备模拟...")
                # 设置移动设备模拟
                mobile_emulation = {
                    "deviceMetrics": {"width": 430, "height": 930, "pixelRatio": 2.0},
                    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
                }
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                # 设置窗口大小与设备尺寸一致
                chrome_options.add_argument('--window-size=500,1000')

            if self._is_port_in_use():
                # 连接到已运行的浏览器
                print(">>> 检测到已运行的浏览器，正在连接...")
                chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self._port}")
            else:
                # 启动新的浏览器
                print(">>> 未检测到运行中的浏览器，正在启动新浏览器...")
                chrome_options.add_argument(f'--remote-debugging-port={self._port}')
                chrome_options.add_experimental_option("detach", True)  # 保持浏览器在程序结束后继续运行

            # 创建浏览器驱动实例
            service = Service(self.chromedriver_path)
            BrowserManager.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            self._is_browser_running = True
            print(">>> 浏览器已就绪")
        else:
            print(">>> 使用已打开的浏览器")

        return BrowserManager.driver

    def close_browser(self):
        """
        关闭浏览器并清理资源。
        只有在浏览器正在运行时才会执行关闭操作。
        """
        if self._is_browser_running and BrowserManager.driver:
            print(">>> 正在关闭浏览器...")
            BrowserManager.driver.quit()
            BrowserManager.driver = None
            self._is_browser_running = False
            print(">>> 浏览器已关闭")
        else:
            self.driver.quit()

    def is_browser_running(self):
        """
        检查浏览器是否正在运行。

        Returns:
            bool: 如果浏览器正在运行返回True，否则返回False
        """
        return self._is_browser_running

    def open(self, url):
        """
        访问指定URL
        """
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"错误：打开URL失败 - {str(e)}")


    def start_chrome_1(self):
        """
        启动Chrome浏览器并返回WebDriver实例
        根据配置文件中的pc_type决定使用哪个驱动路径

        Returns:
            WebDriver: 配置好的Chrome WebDriver实例
        """
        if self.pc_type == 'window':
            try:
                # 创建设置浏览器对象
                self.opt1 = Options()
                # 禁用沙盒模式(增加兼容性)
                self.opt1.add_argument('--no-sandbox')
                # 保持浏览器打开状态
                self.opt1.add_experimental_option('detach', True)
                # 设置浏览器缩放比例70%
                self.opt1.add_argument('--force-device-scale-factor=0.7')
                if self.is_h5 == 'yes':
                    # 配置模拟移动设备
                    mobile_emulation = {
                        "deviceName": "iPhone 14 Pro Max"
                    }
                    self.opt1.add_experimental_option("mobileEmulation", mobile_emulation)
                # 配置启动文件路径，并且使用opt1的设置，启动浏览器
                self.driver = webdriver.Chrome(service=Service(self.Win_chromedriver_url), options=self.opt1)
                # 隐性等待时间配置10s
                self.driver.implicitly_wait(10)
                return self.driver
            except Exception as e:
                print(f"【error:】打开浏览器失败: {e}")

        elif self.pc_type == 'mac':
            try:
                # 创建设置浏览器对象
                self.opt1 = Options()
                # 保持浏览器打开状态
                self.opt1.add_experimental_option('detach', True)
                if self.is_h5 == 'yes':
                    # 配置模拟移动设备
                    mobile_emulation = {
                        "deviceName": "iPhone 14 Pro Max"
                    }
                    self.opt1.add_experimental_option("mobileEmulation", mobile_emulation)
                # 配置启动文件路径，并且使用opt1的设置，启动浏览器
                self.driver = webdriver.Chrome(service=Service(self.Mac_chromedriver_url), options=self.opt1)
                # 隐性等待时间配置10s
                self.driver.implicitly_wait(10)
                return self.driver
            except Exception as e:
                print(f"【出现错误】打开浏览器失败: {e}")

# 创建全局浏览器管理器实例
browser_manager = BrowserManager.get_instance()

