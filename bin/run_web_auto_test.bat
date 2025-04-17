@echo off
pythonw C:\Users\wang\PycharmProjects\AtouTest_Web\bin\start.py

echo 开始执行自动化测试 - %date% %time%
echo 当前工作目录: %cd%

:: 执行Python脚本
start /min cmd /c "python C:\Users\wang\PycharmProjects\AtouTest_Web\py_bin\run_web_auto_test.py & pause"

echo 测试执行完成 - %date% %time% 