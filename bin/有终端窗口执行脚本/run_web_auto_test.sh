#!/bin/bash

echo "开始执行自动化测试 - $(date)"
echo "当前工作目录: $(pwd)"

# 执行Python脚本
python3 /Users/wang/PycharmProjects/AtouTest_Web/bin/run_web_auto_test.py

echo "测试执行完成 - $(date)"
