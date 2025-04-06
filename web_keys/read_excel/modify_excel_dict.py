from selenium.webdriver.common.by import By


def convert_by_string(lst):
    """
    此函数用于将列表中以 'By.' 开头的字符串转换为 By 类对应的属性
    :param lst: 待处理的列表，列表元素可能包含以 'By.' 开头的字符串
    :return: 处理后的新列表，其中以 'By.' 开头的字符串已转换为 By 类的属性
    """
    # 初始化一个空列表，用于存储转换后的元素
    new_lst = []
    # 遍历输入列表中的每个元素
    for item in lst:
        # 检查元素是否为字符串类型，并且是否以 'By.' 开头
        if isinstance(item, str) and item.startswith('By.'):
            try:
                # 通过分割字符串，提取出定位方式的名称，例如 'id'
                locator_name = item.split('.')[-1]
                # 使用 getattr 函数从 By 类中获取对应的属性
                # 例如，如果 locator_name 为 'id'，则获取 By.ID
                new_lst.append(getattr(By, locator_name))
            except AttributeError:
                # 如果 By 类中不存在指定名称的属性，捕获 AttributeError 异常
                # 并打印错误信息，提示用户 By 类中没有该属性
                print(f"错误：By 类中不存在名为 {locator_name} 的属性。")
                # 将原字符串添加到新列表中，保持元素不变
                new_lst.append(item)
        else:
            # 如果元素不是以 'By.' 开头的字符串，直接添加到新列表中
            new_lst.append(item)
    # 返回处理后的新列表
    return new_lst


def convert_dict(dictionary):
    """
    此函数用于处理字典，将字典中值为列表的元素里以 'By.' 开头的字符串转换为 By 类对应的属性
    :param dictionary: 待处理的字典
    :return: 处理后的字典
    """
    new_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, list):
            new_dict[key] = convert_by_string(value)
        else:
            new_dict[key] = value
    return new_dict
