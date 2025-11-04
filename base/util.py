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

def solution_check_run(path_dir,input_dict):
    rule_count = 10
    check_result_list = []
    for idx in range(1, rule_count):
        function_name = f'check_rule_{idx}'
        return_dict = eval(function_name)(input_dict)
        if return_dict:
            check_result_list.append(return_dict)
            continue
    return check_result_list

def check_rule_1(input_dict):
    logger.info(f'check_rule_1')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_1',
                'Exception': 'Intel CPU',
                'Debug Solution': 'Intel CPU BSOD Pre-Debug List'}
    CPUID = input_dict.get('CPUID', None)
    Intel_Platform_Status = 0
    if CPUID is not None and 'intel' in CPUID.lower():
        Intel_Platform_Status = 1

    CPU_Status_Abnormal = input_dict.get('CPU_Status_Abnormal', None)
    if CPU_Status_Abnormal and CPU_Status_Abnormal == 1 and Intel_Platform_Status == 1:
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_2(input_dict):
    logger.info(f'check_rule_2')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_2',
                'Exception': 'AMD CPU',
                'Debug Solution': 'Intel CPU BSOD Pre-Debug List'}
    CPUID = input_dict.get('CPUID', None)
    AMD_Platform_Status = 0
    if CPUID is not None and 'amd' in CPUID.lower():
        AMD_Platform_Status = 1

    CPU_Status_Abnormal = input_dict.get('CPU_Status_Abnormal', None)
    if CPU_Status_Abnormal and CPU_Status_Abnormal == 1 and AMD_Platform_Status == 1:
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_3(input_dict):
    logger.info(f'check_rule_3')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_3',
                'Exception': 'Intel Memory',
                'Debug Solution': 'Intel Memory BSOD Pre-Debug List'}
    CPUID = input_dict.get('CPUID', None)
    Intel_Platform_Status = 0
    if CPUID is not None and 'intel' in CPUID.lower():
        Intel_Platform_Status = 1

    Memory_Status_Abnormal = input_dict.get('Memory_Status_Abnormal', None)
    if Memory_Status_Abnormal and Memory_Status_Abnormal == 1 and Intel_Platform_Status == 1:
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_4(input_dict):
    logger.info(f'check_rule_4')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_4',
                'Exception': 'AMD Memory',
                'Debug Solution': 'AMD Memory BSOD Pre-Debug List'}
    CPUID = input_dict.get('CPUID', None)
    AMD_Platform_Status = 0
    if CPUID is not None and 'amd' in CPUID.lower():
        AMD_Platform_Status = 1

    CPU_Status_Abnormal = input_dict.get('CPU_Status_Abnormal', None)
    if CPU_Status_Abnormal and CPU_Status_Abnormal == 1 and AMD_Platform_Status == 1:
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_5(input_dict):
    logger.info(f'check_rule_5')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_5',
                'Exception': 'Disk',
                'Debug Solution': 'Disk BSOD Pre-Debug List'}

    Disk_Status_Abnormal = input_dict.get('Disk_Status_Abnormal', None)
    logger.info(f"Disk_Status_Abnormal: {Disk_Status_Abnormal}")
    if Disk_Status_Abnormal and Disk_Status_Abnormal == 1:
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_6(input_dict):
    logger.info(f'check_rule_6')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_6',
                'Exception': 'Intel Platform',
                'Debug Solution': '3rd Common BSOD Pre-Debug List'}
    CPUID = input_dict.get('CPUID', None)
    Intel_Platform_Status = 0
    if CPUID is not None and 'intel' in CPUID.lower():
        Intel_Platform_Status = 1
        return_dict = out_dict

    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_7(input_dict):
    logger.info(f'check_rule_7')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_7',
                'Exception': 'AMD Platform',
                'Debug Solution': '3rd Common BSOD Pre-Debug List'}
    CPUID = input_dict.get('CPUID', None)
    if CPUID is not None and 'amd' in CPUID.lower():
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_8(input_dict):
    logger.info(f'check_rule_8')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_8',
                'Exception': 'ACPI',
                'Debug Solution': 'Intel CPU BSOD Pre-Debug List'}
    ACPI_Status_Abnormal = input_dict.get('ACPI_Status_Abnormal', None)
    if ACPI_Status_Abnormal is not None and ACPI_Status_Abnormal == 1:
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_9(input_dict):
    logger.info(f'check_rule_9')
    return_dict = None
    out_dict = {'rule_name': 'check_rule_9',
                'Exception': 'OS',
                'Debug Solution': '3rd Common BSOD Pre-Debug List'}
    OS_Status_Abnormal = input_dict.get('OS_Status_Abnormal', None)
    if OS_Status_Abnormal is not None and OS_Status_Abnormal == 1:
        return_dict = out_dict
    logger.info(f"return_dict: {return_dict}")
    return return_dict

def Suspicious_Driver_Check(BSOD_Suspicious_Driver, final_dict):
    file_name = 'BSOD_Cause_Driver_Matrix.json'
    file_name = os.path.join(BASEDIR, file_name)
    data_dic = read_file_dict(file_name)
    solution_Categories = data_dic.get('Categories')

    tmp_dict = data_dic.get('Groups', [])
    # logger.info(f"tmp_dict:{tmp_dict}")

    out_Category = None
    for key, cell_dict in tmp_dict.items():
        # logger.info(f"key:{key}, value:{cell_dict}")
        Category = cell_dict.get('Category', None)
        # logger.info(f"Category: {Category}")

        Drivers = cell_dict.get('Drivers', [])
        # logger.info(f"Drivers: {Drivers}")

        for driver in Drivers:
            if BSOD_Suspicious_Driver in driver:
                out_Category = Category
                break
        if out_Category is not None:
            break

    solution = solution_Categories.get(out_Category, None)
    logger.info(f"solution: {solution}")
    final_dict['BSOD_Suspicious_Driver_Solution'] = solution
    return

def find_solution(path_dir, file_name):
    final_dict = {}
    file_name = os.path.join(path_dir, file_name)
    logger.info(f'file_name:{file_name}')

    result_dic = read_file_dict(file_name)
    summary_dic = result_dic.get('Summary', {})
    logger.info(f"summary_dic: {summary_dic}")

    check_result_list = solution_check_run(path_dir, summary_dic)
    final_dict['check_result_list'] = check_result_list

    BSOD_Suspicious_Driver = summary_dic.get('BSOD_Suspicious_Driver', None)
    logger.info(f'BSOD_Suspicious_Driver:{BSOD_Suspicious_Driver}')

    if BSOD_Suspicious_Driver is not None and BSOD_Suspicious_Driver.strip() != '':
        Suspicious_Driver_Check(BSOD_Suspicious_Driver, final_dict)

    result_yaml_file = 'solution.yaml'
    result_yaml_file = os.path.join(path_dir, result_yaml_file)
    dump_file(result_yaml_file, final_dict)
    logger.info(f'final_dict:{final_dict}')
    return

def post_report_process(folder_path=None):
    logger.info(f"post_report_process: {folder_path}")
    # folder_path = r'D:\0_LOG_VIP\0_Result_1019'
    # folder_path = r'D:\0_LOG_VIP\test'

    for root, dirs, files in os.walk(folder_path):
        target_file = 'BSOD_Debug_Report.yaml'
        for file in files:
            if file == target_file:
                logger.info(f"root: {root}")
                find_solution(root, file)

    return

# 使用示例
if __name__ == "__main__":
    # 要删除的文件夹路径
    folder_path = r'D:\0_LOG_VIP\Result_10_28'
    post_report_process(folder_path)
