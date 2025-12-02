import os
import sys

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)

root_dir = os.path.join(path_dir, '../')
sys.path.append(root_dir)

from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *
from base.folder_file import *

path_dir = os.path.dirname(__file__)
logger.info(f'path_dir: {path_dir}')

def copy_files(result_dir):
    files = ['tmp.log',
             'result.yaml',
             'step_command.yaml',
             'command_dict.yaml',
             ]
    src_files = []
    for item in files:
        file = os.path.join(path_dir, item)
        src_files.append(file)
    copy_multiple_files(src_files, result_dir)
    return

file = r'D:\input.yaml'
src_dir_list = fileOP.get_file_content_list(file)
# logger.info(f'src_dir_list: {src_dir_list}')

# src_dir_list = [r'G:\SWHang\08_sku4-2_swhang_camear_0xe2\DumpFile\MemoryDump',
#                 ]

if __name__ == '__main__':
    for src_dir in src_dir_list:
        src_dir = src_dir.strip()
        if src_dir == '':
            continue
        logger.info(f'src_dir: {src_dir}')
        dump_file = os.path.join(src_dir, 'MEMORY.DMP')

        src_dir_list = src_dir.split('\\')
        logger.info(f'src_dir_list: {src_dir_list}')

        result_dir = path_dir
        for idx, item in enumerate(src_dir_list):
            if idx < 2:
                continue
            logger.info(f'item: {item}')

            result_dir = os.path.join(result_dir, item)
            logger.info(f'result_dir: {result_dir}')

        create_ok = create_folder(result_dir)
        if create_ok:
            one_process_run(dump_file, path_dir, step_only=16)
            copy_files(result_dir)
            post_report_process(result_dir)