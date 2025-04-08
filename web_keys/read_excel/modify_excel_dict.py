from selenium.webdriver.common.by import By


def convert_to_by(by_str):
    """
    将字符串形式的定位方式转换为Selenium的By对象
    :param by_str: 字符串形式的定位方式，如 'By.ID', 'By.XPATH' 等
    :return: Selenium的By对象
    """
    try:
        if isinstance(by_str, str) and by_str.startswith('By.'):
            # 直接获取By类的属性
            return getattr(By, by_str.split('.')[-1])
        return by_str
    except AttributeError:
        print(f"错误：不支持的定位方式 - {by_str}")
        return by_str


def convert_list_to_by(by_list):
    """
    将列表中的字符串形式的定位方式转换为Selenium的By对象
    :param by_list: 包含定位方式的列表
    :return: 转换后的列表
    """
    try:
        return [convert_to_by(item) for item in by_list]
    except Exception as e:
        print(f"错误：转换列表失败 - {str(e)}")
        return by_list


def convert_dict_to_by(by_dict):
    """
    将字典中的字符串形式的定位方式转换为Selenium的By对象
    :param by_dict: 包含定位方式的字典
    :return: 转换后的字典
    """
    try:
        new_dict = {}
        for key, value in by_dict.items():
            if isinstance(value, str):
                new_dict[key] = convert_to_by(value)
            elif isinstance(value, list):
                new_dict[key] = convert_list_to_by(value)
            elif isinstance(value, dict):
                new_dict[key] = convert_dict_to_by(value)
            else:
                new_dict[key] = value
        return new_dict
    except Exception as e:
        print(f"错误：转换字典失败 - {str(e)}")
        return by_dict


# 使用示例
if __name__ == "__main__":
    # 直接使用字符串
    a = 'By.ID'
    by_obj = convert_to_by(a)  # 得到 By.ID 对象

    # 现在可以直接使用
    print(by_obj)  # 输出: id
    print(type(by_obj))  # 输出: <class 'selenium.webdriver.common.by.By'>

    # 在Selenium中使用
    # element = driver.find_element(by_obj, 'username')

    b = ['输入_密码', 'By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[2]/div/div/div/input', 'admin']
    bb = convert_list_to_by(b)
    print(bb)  # 输出: id
    print(type(bb))