def convert_dict_to_variables(data_dict: dict) -> str:
    """
    将字典数据转换为单独的变量，并返回生成的变量内容

    Args:
        data_dict (dict): 包含操作步骤的字典，格式如：
            {
                '打开_浏览器': ['nan', 'nan', 'nan'],
                '打开_url_登录': ['https://adminplus.iviewui.com/', 'nan', 'nan'],
                ...
            }

    Returns:
        str: 生成的变量内容
    """
    try:
        # 获取调用者的全局命名空间
        import inspect
        frame = inspect.currentframe()
        caller_globals = frame.f_back.f_globals

        # 初始化结果字符串
        result = ""

        # 遍历字典中的每个步骤
        for i, (step_name, step_data) in enumerate(data_dict.items(), 1):
            # 创建变量名（step1, step2, ...）
            var_name = f"step{i}"

            # 创建列表数据 [步骤名称, 定位方式, 定位值, 输入值]
            step_list = [step_name] + step_data

            # 在调用者的全局命名空间中创建变量
            caller_globals[var_name] = step_list

            # 添加到结果字符串
            result += f"{var_name} = {step_list}\n"

        return result
    except Exception as e:
        print(f"转换数据时发生错误: {str(e)}")
        return ""


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

    # 转换数据并获取生成的变量内容
    variables_content = convert_dict_to_variables(test_data)

    # 打印生成的变量内容
    print("生成的变量内容：")
    print(variables_content)

    # 现在可以直接使用变量
    print("\n使用变量：")
    print(step1)  # 输出: ['打开_浏览器', 'nan', 'nan', 'nan']