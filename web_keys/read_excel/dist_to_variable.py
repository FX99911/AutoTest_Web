def convert_dict_to_variables(data_dict: dict) -> dict:
    """
    将字典数据转换为步骤字典

    Args:
        data_dict (dict): 包含操作步骤的字典，格式如：
            {
                '打开_浏览器': ['nan', 'nan', 'nan'],
                '打开_url_登录': ['https://adminplus.iviewui.com/', 'nan', 'nan'],
                ...
            }

    Returns:
        dict: 包含所有步骤的字典，格式如：
            {
                'step1': ['打开_浏览器', 'nan', 'nan', 'nan'],
                'step2': ['打开_url_登录', 'https://adminplus.iviewui.com/', 'nan', 'nan'],
                ...
            }
    """
    try:
        steps = {}
        # 遍历字典中的每个步骤
        for i, (step_name, step_data) in enumerate(data_dict.items(), 1):
            # 创建变量名（step1, step2, ...）
            var_name = f"step{i}"
            # 创建列表数据 [步骤名称, 定位方式, 定位值, 输入值]
            step_list = [step_name] + step_data
            # 添加到步骤字典
            steps[var_name] = step_list
        return steps
    except Exception as e:
        print(f"转换数据时发生错误: {str(e)}")
        return {}


# 使用示例
if __name__ == "__main__":
    # 示例数据
    test_data = {
        '打开_浏览器': ['nan', 'nan', 'nan'],
        '打开_url_登录': ['https://adminplus.iviewui.com/', 'nan', 'nan'],
        '输入_用户名': ['xpath', '//input[@placeholder="请输入用户名"]', 'admin'],
        '输入_密码': ['xpath', '//input[@placeholder="请输入密码"]', '123456'],
        '点击_登录按钮': ['xpath', '//button[@type="button"]', 'nan'],
        '断言_登录成功': ['xpath', '//span[text()="欢迎回来"]', 'nan']
    }

    # 转换数据并获取步骤字典
    steps = convert_dict_to_variables(test_data)

    # 打印所有步骤
    print("所有步骤：")
    for step_name, step_data in steps.items():
        print(f"{step_name}: {step_data}")

    # 使用步骤
    print("\n使用步骤：")
    print(steps['step1'])  # 输出: ['打开_浏览器', 'nan', 'nan', 'nan']