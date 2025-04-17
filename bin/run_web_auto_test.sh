#!/bin/bash

echo "开始执行自动化测试 - $(date)"
echo "当前工作目录: $(pwd)"

# 执行Python脚本
nohup python3 ../py_bin/start.py > /dev/null 2>&1 &

echo "测试执行完成 - $(date)"

# 使用AppleScript关闭当前终端窗口，但保持程序运行
# osascript -e 'tell application "Terminal" to close (every window whose name contains "run_web_auto_test.sh")' &
