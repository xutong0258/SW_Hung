import shutil
import os
from base.fileOP import *
from base.logger import *

BASEDIR = os.path.dirname(__file__)

def delete_folder(folder_path):
    try:
        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            logger.info(f"错误: 文件夹 '{folder_path}' 不存在")
            return
            
        # 检查是否是文件夹
        if not os.path.isdir(folder_path):
            logger.info(f"错误: '{folder_path}' 不是一个文件夹")
            return
            
        # 删除文件夹及其内容
        shutil.rmtree(folder_path)
        logger.info(f"文件夹 '{folder_path}' 已成功删除")
        
    except PermissionError:
        logger.info(f"错误: 没有权限删除 '{folder_path}'")
    except Exception as e:
        logger.info(f"删除文件夹时发生错误: {str(e)}")

def create_folder(folder_path):
    try:
        # 检查文件夹是否已存在
        if not os.path.exists(folder_path):
            # 创建文件夹，parents=True表示如果父目录不存在也会一起创建
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"文件夹创建成功: {folder_path}")
            return True
        else:
            logger.info(f"文件夹已存在: {folder_path}")
            return True
    except PermissionError:
        logger.info(f"权限错误: 无法在 {folder_path} 创建文件夹，请检查权限")
    except OSError as e:
        logger.info(f"创建文件夹时发生错误: {e}")
    return False

def copy_single_file(src_path, dest_path, overwrite=True):
    try:
        # 检查源文件是否存在
        if not os.path.isfile(src_path):
            logger.info(f"错误: 源文件不存在 - {src_path}")
            return False

        # 处理目标路径，如果是目录则保留原文件名
        if os.path.isdir(dest_path):
            file_name = os.path.basename(src_path)
            dest_path = os.path.join(dest_path, file_name)

        # # 检查目标文件是否存在
        # if os.path.exists(dest_path) and not overwrite:
        #     logger.info(f"错误: 目标文件已存在，未进行覆盖 - {dest_path}")
        #     return False

        # 复制文件
        shutil.copy2(src_path, dest_path)  # copy2会保留文件元数据
        logger.info(f"文件复制成功: {src_path} -> {dest_path}")
        return True

    except PermissionError:
        logger.info(f"错误: 权限不足，无法复制文件 - {src_path}")
    except Exception as e:
        logger.info(f"复制文件时发生错误: {str(e)}")
    return False

def copy_multiple_files(src_files, dest_dir, overwrite=False):
    success_count = 0
    fail_count = 0

    # 确保目标目录存在
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            logger.info(f"创建目标目录: {dest_dir}")
        except Exception as e:
            logger.info(f"无法创建目标目录: {str(e)}")
            return (0, len(src_files))

    # 逐个复制文件
    for file_path in src_files:
        if copy_single_file(file_path, dest_dir, overwrite):
            success_count += 1
        else:
            fail_count += 1

    logger.info(f"批量复制完成: 成功 {success_count} 个, 失败 {fail_count} 个")
    return (success_count, fail_count)

def clean_file():
    C1_Time = datetime.datetime.now ()
    logger.info(f'curreent:{C1_Time}')
    time_stamp = datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S")
    logger.info(f'time_stamp:{time_stamp}')

    # current_dir = os.getcwd()
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if '.mp4' not in file:
                continue
            file = os.path.join(root, file)

            c2_Time = os.path.getmtime(file)
            c2_Time = datetime.datetime.fromtimestamp(c2_Time)
            delta = C1_Time.__sub__ (c2_Time)
            logger.info(f'delta.days:{delta.days}')
            if delta.days > 5:
                logger.info (f"remove file:{file} delta.days:{delta.days}")
                cmd = f'sudo rm -rf {file}'
                cmd_excute(file)
    return

def change_file_name():
    dir = r'D:\0_慧务农\发票\bak\11'
    # /home/yskj/data/sport-ci/conf
    # dir = r'/home/yskj/data/sport-ci/conf'
    tmp_list = os.listdir (dir)
    for item in tmp_list:
        full_path = os.path.join(dir, item)
        new_path = full_path.replace('.pdf', '_33.pdf')
        command = f'mv {full_path} {new_path}'
        # cmd_excute(command, logger)
        os.rename(full_path, new_path)
    return

def replace_file():
    wait_str = ''
    target_str = ''
    current_dir = r'D:\00_stone_project-237\0_17_stress_cases'
    target_dirs = os.listdir(current_dir)
    final_list = []
    for item in target_dirs:
        path = os.path.join(current_dir, item)
        command = f"cd {path} && sed -i 's/{wait_str}/{target_str}/g' *.yaml"
        cmd_excute(command)
    return

def get_file_path_by_dir(folder_path, target_file_name):
    # 要遍历的文件路径
    file_path = None
    target_file_path = None
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            path = os.path.join(root, dir)
            if '.' in path and '.git' not in path and '.idea' not in path:
                # print(f"del: {path}")
                pass

        for file in files:
            file_path = os.path.join(root, file)
            # print(file_path)
            if target_file_name.lower() in file_path.lower() :
                # logger.info(f"target file: {file_path}")
                target_file_path = file_path
                break
    logger.info(f"target_file_path: {target_file_path}")
    return target_file_path

def get_latest_file_path_by_dir(folder_path, target_file):
    # 要遍历的文件路径
    target_file_path = None
    file_list = []
    file_dict = {}
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            path = os.path.join(root, dir)
            if '.' in path and '.git' not in path and '.idea' not in path:
                # print(f"del: {path}")
                pass

        for file in files:
            file_path = os.path.join(root, file)
            # logger.info(f'file_path:{file_path}')
            # print(file_path)
            if target_file.lower() in file_path.lower() :
                c2_Time = os.path.getmtime(file_path)
                # logger.info(f"c2_Time: {c2_Time}")
                file_dict[file_path] = c2_Time

    max_time = 0
    latest_file = None
    for key, value in file_dict.items():
        if value > max_time:
            max_time = value
            latest_file = key
    logger.info(f"latest_file: {latest_file}")
    return latest_file
# 使用示例
if __name__ == "__main__":
    # 要删除的文件夹路径
    folder_path = r'D:\hello\DumpFile\ApplicationDumps'
    target_file = '.dmp'
    get_latest_file_path_by_dir(folder_path, target_file)
