import os
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

if __name__ == '__main__':
    case_path_config_file = 'case_path_config.yaml'
    case_path_config_file = os.path.join(CONFIG_PATH, case_path_config_file)

    config_dict = read_file_dict(case_path_config_file)
    config_dict = config_dict.get('05_SW_Hung')
    src_dir = config_dict.get('PATH')

    logger.info(f'src_dir: {src_dir}')
    target_file = '.dmp'
    dump_file = get_latest_file_path_by_dir(src_dir, target_file)
    # dump_file = os.path.join(src_dir, 'MEMORY.DMP')

    src_dir_list = src_dir.split('\\')
    logger.info(f'src_dir_list: {src_dir_list}')

    result_dir = os.path.join(path_dir, src_dir_list[2])
    logger.info(f'result_dir: {result_dir}')

    create_ok = create_folder(result_dir)
    if create_ok:
        one_process_run(dump_file, path_dir, step_only=16)
        copy_files(result_dir)
        post_report_process(result_dir)