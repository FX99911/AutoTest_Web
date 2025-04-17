自动化测试脚本使用说明
====================

1. Windows系统使用说明
--------------------
1.1 直接运行批处理文件
- 双击 run_web_auto_test.bat 文件即可运行
- 所有输出会显示在命令提示符窗口中

1.2 创建快捷方式
- 右键点击 run_web_auto_test.bat 文件
- 选择"创建快捷方式"
- 将创建的快捷方式移动到任意位置（如桌面）
- 双击快捷方式即可运行

2. Mac系统使用说明
----------------
2.1 直接运行Shell脚本
- 打开终端
- 进入脚本所在目录
- 执行命令：chmod +x run_web_auto_test.sh
- 执行命令：./run_web_auto_test.sh

2.2 使用Automator创建应用程序（推荐）
1) 打开 Automator（在应用程序文件夹中）
2) 选择"新建文稿" -> "应用程序"
3) 搜索并添加"运行 Shell 脚本"
4) 在脚本框中输入以下内容：
   ```
   #!/bin/bash
   nohup python3 /Users/wang/PycharmProjects/AtouTest_Web/py_bin/start.py > /dev/null 2>&1 &
   ```
5) 点击"文件" -> "存储"
6) 选择保存位置（建议桌面）
7) 输入名称（如"WebAutoTest"）
8) 点击"存储"






3. 路径修改说明
-------------
如果Python脚本路径需要修改，请按以下步骤操作：

3.1 Windows系统
- 用文本编辑器打开 run_web_auto_test.bat
- 修改以下行中的路径：
  python C:\Users\wang\PycharmProjects\AtouTest_Web\bin\run_web_auto_test.py
- 保存文件

3.2 Mac系统
- 用文本编辑器打开 WebAutoTest.app/Contents/MacOS/WebAutoTest
- 修改以下行中的路径：
  python3 /Users/wang/PycharmProjects/AtouTest_Web/bin/run_web_auto_test.py
- 保存文件








4. 注意事项
---------
- 确保系统中已安装Python
- Windows系统使用反斜杠(\)作为路径分隔符
- Mac系统使用正斜杠(/)作为路径分隔符
- 如果遇到权限问题，请确保脚本具有执行权限