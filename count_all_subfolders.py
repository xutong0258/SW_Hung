import os
import argparse
from base.logger import *

def count_all_subfolders(folder_path):
    """
    统计指定文件夹下所有层级的子文件夹数量（包括嵌套文件夹）

    参数:
        folder_path: 要统计的文件夹路径

    返回:
        所有子文件夹的总数量，如果路径无效则返回-1
    """
    # 检查路径是否存在
    if not os.path.exists(folder_path):
        print(f"错误: 路径 '{folder_path}' 不存在")
        return -1

    # 检查路径是否是一个文件夹
    if not os.path.isdir(folder_path):
        print(f"错误: '{folder_path}' 不是一个文件夹")
        return -1

    # 检查是否有访问权限
    if not os.access(folder_path, os.R_OK):
        print(f"错误: 没有访问 '{folder_path}' 的权限")
        return -1

    total_count = 0

    # 使用os.walk递归遍历所有目录
    for root, dirs, files in os.walk(folder_path):
        # 跳过根目录本身，只统计子文件夹
        if root != folder_path:
            logger.info(f'root:{root}, dirs:{dirs}')
            # 当前目录下的子文件夹数量
            current_dir_count = len(dirs)
            total_count += current_dir_count

            # 可选：打印每个目录下的子文件夹数量，用于调试
            # print(f"目录 '{root}' 包含 {current_dir_count} 个子文件夹")

    return total_count

if __name__ == "__main__":
    # # 设置命令行参数
    # parser = argparse.ArgumentParser(description='统计文件夹下所有层级的子文件夹数量（包括嵌套文件夹）')
    # parser.add_argument(r'D:\0_RESULT_1011', help='要统计的文件夹路径')
    # args = parser.parse_args()

    # 统计所有子文件夹数量
    folder_path = r'G:\BSOD_Debug_SOP_0911'
    count = count_all_subfolders(folder_path)

    # 输出结果
    if count >= 0:
        print(f"文件夹 '{folder_path}' 及其子文件夹中，所有层级的子文件夹总数为: {count}")
    