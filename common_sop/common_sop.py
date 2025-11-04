import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)
logger.info(f'path_dir: {path_dir}')

def copy_files(result_dir):
    files = ['tmp.log',
             'BSOD_Debug_Data.yaml',
             'BSOD_Debug_Report.yaml',
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

src_dir_list = [r'D:\00\05_SW_Hung\SWhang_DiskIO_MemoryDump\MemoryDump',
                ]

if __name__ == '__main__':
    for src_dir in src_dir_list:
        src_dir = src_dir.strip()
        if src_dir == '':
            continue
        logger.info(f'src_dir: {src_dir}')
        dump_file = os.path.join(src_dir, 'MEMORY.DMP')

        base_dir_1 = os.path.basename(src_dir)
        logger.info(f'base_dir_1: {base_dir_1}')
        if r'.' in base_dir_1:
            result_dir = os.path.join(path_dir, base_dir_1)
            logger.info(f'result_dir: {result_dir}')
        else:
            parent_dir = os.path.dirname(src_dir)
            # logger.info(f'parent_dir: {parent_dir}')

            base_dir_2 = os.path.basename(parent_dir)
            # logger.info(f'base_dir_2: {base_dir_2}')

            result_dir = os.path.join(path_dir, base_dir_2, base_dir_1)
            logger.info(f'result_dir: {result_dir}')

        create_ok = create_folder(result_dir)
        if create_ok:
            one_process_run(dump_file, path_dir)
            copy_files(result_dir)
            post_report_process(result_dir)