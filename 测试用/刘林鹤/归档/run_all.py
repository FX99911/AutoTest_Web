import subprocess
import sys
import time

def main():
    """
    先启动脚本A，给它一点时间初始化浏览器端口，
    再启动脚本B，最后根据需要管理脚本A和B的生命周期。
    """
    # 1) 启动脚本A
    print(">>> 运行脚本A：start_browser.py")
    pA = subprocess.Popen([sys.executable, "start_browser.py"])
    
    # 等待几秒，让脚本A能够完成对Chrome的启动
    time.sleep(5)

    # 2) 启动脚本B
    print(">>> 运行脚本B：attach_browser.py")
    pB = subprocess.Popen([sys.executable, "attach_browser.py"])
    
    # 等待脚本B执行完（它会在用户按回车时退出）
    pB.wait()
    print(">>> 脚本B结束了")

    # 3) 结束脚本A
    #    如果脚本A 也在等待用户回车，可以选择自动发信号终止，
    #    或让用户手动去终端按回车。这取决于你的需求
    print(">>> 现在结束脚本A")
    pA.terminate()
    # 如果希望脚本A先行结束后再判断是否需要 kill 或者 continue：
    # pA.wait()
    # print(">>> 脚本A已退出")

if __name__ == "__main__":
    main()
