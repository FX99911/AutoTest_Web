from web_keys.environment_info.montage_url import home
from web_keys.template_method.get_now_file_name import get_now_file_name
import os


# 测试用例数据
project_info = {
    '项目名称': ['测试的项目1'],
    '模块名称': ['首页'],
    '测试点': ['登陆'],
    'nan': ['nan']
}


# 操作步骤
operation_steps = {
    '打开_url_登录': ['https://adminplus.iviewui.com/', 'nan', 'nan'],
    '输入_用户名': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[1]/div/div/div/input', 'admin'],
    '输入_密码': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[2]/div/div/div/input', 'admin'],
    '点击_登录按钮': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[2]/form/div[4]/button', 'nan'],
    '断言': ['By.XPATH', '//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[1]/span/span[2]', 'Aresn'],
    '关闭浏览器': ['nan', 'nan', 'nan']
}

# 后续可以在这里添加测试逻辑

# 定义项目信息变量
project_name = project_info['项目名称'][0]
test_module	= project_info['模块名称'][0]
test_points = project_info['测试点'][0]
cases_name = get_now_file_name()  #文件名


# # 步骤变量定义(暂时不需要)
# all_steps = convert_dict_to_variables(operation_steps)

# 获取列表

# picture_url = f'/cases_screenshot/{project_name}/{test_module}/{test_points}'
picture_url = os.path.join('cases_screenshot', project_name, test_module, test_points )
picture_name = f'{cases_name}.jpg'
# =====================以下是测试用例模板====================
########################

def sace_picture_url(config_dict):
    #接收字典
    project_name = project_info['项目名称'][0]
    test_module = project_info['模块名称'][0]
    test_points = project_info['测试点'][0]


def crate_picture_url(picture_url):
    """
    此函数用于检查指定的目录是否存在，若不存在则创建该目录。
    参数:
    picture_url (str): 需要检查或创建的目录的路径
    返回:
    无
    """
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(picture_url):
        # 若目录不存在，使用 os.makedirs 方法创建该目录
        os.makedirs(picture_url)
        # 打印成功创建目录的提示信息
        print(f"成功创建目录: {picture_url}")
    else:
        # 若目录已经存在，打印目录已存在的提示信息
        print(f"目录 {picture_url} 已经存在。")
