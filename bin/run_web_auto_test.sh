#!/bin/bash

echo "开始执行自动化测试 - $(date)"
echo "当前工作目录: $(pwd)"

# 执行Python脚本
nohup python3 /Users/wang/PycharmProjects/AtouTest_Web/py_bin/start.py > /dev/null 2>&1 &

echo "测试执行完成 - $(date)"
