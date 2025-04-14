import os
import shutil
from typing import Optional
from datetime import datetime


def create_timestamp_dir(base_dir: str,timestamp ,prefix: str = "") -> str:
    """
    在指定目录下创建一个以当前时间命名的目录

    Args:
        base_dir: 基础目录路径
        prefix: 目录名前缀，可选

    Returns:
        str: 新创建的目录的完整路径
    """
    try:
        # 生成时间戳格式的目录名
        # timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        timestamp = timestamp
        dir_name = f"{prefix}{timestamp}" if prefix else timestamp

        # 构建完整路径
        new_dir = os.path.join(base_dir, dir_name)

        # 创建目录
        os.makedirs(new_dir, exist_ok=True)

        print(f"成功: 已创建目录 {new_dir}")
        return new_dir

    except Exception as e:
        print(f"错误: 创建目录时出错 - {str(e)}")
        return ""


def copy_directory(src_dir: str, dst_dir: str, ignore_patterns: Optional[list] = None) -> bool:
    """
    递归复制目录及其所有内容

    Args:
        src_dir: 源目录路径
        dst_dir: 目标目录路径
        ignore_patterns: 要忽略的文件或目录模式列表，例如 ['__pycache__', '*.pyc']

    Returns:
        bool: 复制是否成功
    """
    try:
        # 检查源目录是否存在
        if not os.path.exists(src_dir):
            print(f"错误: 源目录 {src_dir} 不存在")
            return False

        # 如果目标目录不存在，创建它
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        # 使用shutil.copytree进行复制
        # 如果ignore_patterns不为None，则使用自定义的ignore函数
        if ignore_patterns:
            def ignore_func(dir, files):
                ignored = []
                for pattern in ignore_patterns:
                    for file in files:
                        if pattern in file:
                            ignored.append(file)
                return set(ignored)

            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True, ignore=ignore_func)
        else:
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

        # print(f"成功: 目录 {src_dir} 已复制到 {dst_dir}")
        return True

    except Exception as e:
        print(f"错误: 复制目录时出错 - {str(e)}")
        return False


# 使用示例
if __name__ == "__main__":
    # 示例1：基本复制
    copy_directory("source_dir", "destination_dir")

    # 示例2：复制时忽略特定文件
    copy_directory(
        "source_dir",
        "destination_dir",
        ignore_patterns=['__pycache__', '*.pyc', '.git']
    )

    # 示例3：创建带时间戳的目录
    new_dir = create_timestamp_dir("backup")
    print(f"新创建的目录: {new_dir}")

    # 示例4：创建带前缀的目录
    new_dir = create_timestamp_dir("backup", prefix="test_")
    print(f"新创建的目录: {new_dir}") 