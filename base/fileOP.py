# coding=utf-8

import yaml
import json
import os
import platform
import re
from base.helper import *
from base.contants import *

def get_DPC_Timeout_Cout_cpu_P1_0(input_list):
    # logger.info(f'input_list:{input_list}')
    cpu_num = None
    Period_line = input_list[2]
    logger.info(f'Period_line:{Period_line}')

    split_list = Period_line.split(' ')
    split_list = get_list_strip(split_list)
    Period = split_list[3]
    logger.info(f'Period:{Period}')

    DPC_Timeout_Cout_line = input_list[3]
    logger.info(f'DPC_Timeout_Cout_line:{DPC_Timeout_Cout_line}')

    split_list = DPC_Timeout_Cout_line.split(' ')
    split_list = get_list_strip(split_list)
    logger.info(f'split_list:{split_list}')
    DPC_Timeout_Cout = split_list[3]
    logger.info(f'DPC_Timeout_Cout:{DPC_Timeout_Cout}')

    if eval(DPC_Timeout_Cout) > eval(Period):
        colon_index = Period_line.index(':')
        cpu_num = Period_line[0:colon_index]
        logger.info(f'cpu_num:{cpu_num}')
    return cpu_num

def get_DPC_Timeout_Cout_cpu_P1_1(input_list):
    # logger.info(f'input_list:{input_list}')
    cpu_num = None
    DPC_Count_line = input_list[1]
    logger.info(f'DPC_Count_line:{DPC_Count_line}')

    split_list = DPC_Count_line.split(' ')
    split_list = get_list_strip(split_list)
    DPC_Count = split_list[3]
    logger.info(f'DPC_Count:{DPC_Count}')

    DPC_Timeout_Period_line = input_list[2]
    logger.info(f'DPC_Timeout_Period_line:{DPC_Timeout_Period_line}')

    split_list = DPC_Timeout_Period_line.split(' ')
    split_list = get_list_strip(split_list)
    logger.info(f'split_list:{split_list}')
    DPC_Timeout_Period = split_list[3]
    logger.info(f'DPC_Timeout_Period:{DPC_Timeout_Period}')

    if eval(DPC_Count) > eval(DPC_Timeout_Period):
        colon_index = DPC_Count_line.index(':')
        cpu_num = DPC_Count_line[0:colon_index]
        logger.info(f'cpu_num:{cpu_num}')
    return cpu_num

def get_cpu_index(input_list):
    index = None
    for idx, line in enumerate(input_list):
        if 'CPU Type' in line:
            index = idx + 1
            logger.info(f'CPU Type index:{index}')
    return index

def get_swd_DPCTimeout_CPU_P1_0(log_lines):
    log_lines = get_list_strip(log_lines[1:])
    # logger.info(f'log_lines:{log_lines}')

    # logger.info(f'log_lines len:{len(log_lines)}')

    index = get_cpu_index(log_lines)
    # logger.info(f'index:{log_lines[index]}')

    cpu_group_list = log_lines[index:]
    # logger.info(f'cpu_group_list:{cpu_group_list}')

    len_cpu_group_list = len(cpu_group_list)
    logger.info(f'len_cpu_group_list:{len_cpu_group_list}')

    cpu_group_count = len_cpu_group_list/5
    logger.info(f'cpu_group_count:{cpu_group_count}')

    cpu_num = None
    for idx in range(int(cpu_group_count)):
        # logger.info(f'idx:{idx}')
        start_idx = idx * 5
        end_idx = (idx + 1) * 5
        tmp_group_list = cpu_group_list[start_idx:end_idx]
        tmp_cpu_num = get_DPC_Timeout_Cout_cpu_P1_0(tmp_group_list)
        logger.info(f'tmp_cpu_num:{tmp_cpu_num}')
        if tmp_cpu_num:
            cpu_num = int(tmp_cpu_num)
    return cpu_num

def get_swd_DPCTimeout_CPU_P1_1(log_lines):
    log_lines = get_list_strip(log_lines[1:])
    # logger.info(f'log_lines:{log_lines}')

    # logger.info(f'log_lines len:{len(log_lines)}')

    index = get_cpu_index(log_lines)
    # logger.info(f'index:{log_lines[index]}')

    cpu_group_list = log_lines[index:]
    # logger.info(f'cpu_group_list:{cpu_group_list}')

    len_cpu_group_list = len(cpu_group_list)
    logger.info(f'len_cpu_group_list:{len_cpu_group_list}')

    cpu_group_count = len_cpu_group_list/5
    logger.info(f'cpu_group_count:{cpu_group_count}')

    cpu_num = None
    for idx in range(int(cpu_group_count)):
        # logger.info(f'idx:{idx}')
        start_idx = idx * 5
        end_idx = (idx + 1) * 5
        tmp_group_list = cpu_group_list[start_idx:end_idx]
        tmp_cpu_num = get_DPC_Timeout_Cout_cpu_P1_1(tmp_group_list)
        logger.info(f'tmp_cpu_num:{tmp_cpu_num}')
        if tmp_cpu_num:
            cpu_num = int(tmp_cpu_num)
    return cpu_num

def parse_locks_content(log_lines):
    thread_contention_pairs = {}
    max_count = 0
    max_thread_name = None
    for idx, line in enumerate(log_lines):
        if 'Contention Count =' in line:
            # logger.info(f'line {line}')
            Contention_Count = line.split('Contention Count =')[1]
            if 'Threads:' in log_lines[idx+2]:
                thread_idx = idx+2
            else:
                thread_idx = idx + 1
            thread = log_lines[thread_idx]
            # logger.info(f'thread: {thread}')
            thread = thread.split('Threads:')[1]
            thread_contention_pairs[thread] = Contention_Count

            if int(Contention_Count) > max_count:
                max_count = int(Contention_Count)
                max_thread_name = thread

    return thread_contention_pairs, max_thread_name

def get_text_with_start_text_to_end(log_lines, start_text, end_text='kd>'):
    # logger.info(f'log_lines: {log_lines}')
    # 2. 定位目标片段的起始行（包含"!devstack"的首行，即命令行起始）
    start_idx = None
    for idx, line in enumerate(log_lines):
        if start_text in line:  # 匹配起始标记
            start_idx = idx
            # logger.info(f'start_idx: {start_idx}')
            break
    if start_idx is None:
        logger.info(f"❌ 未在日志中找到起始标记:{start_text}")
        return None

    # 3. 定位目标片段的结束行（包含"ServiceName is"的行）
    end_idx = None
    # 从起始行之后开始查找，避免跨片段匹配
    for idx, line in enumerate(log_lines[start_idx+1:]):
        if end_text in line:
            end_idx = start_idx + idx  # 转换为全局索引
            break
    if end_idx is None:
        target_segment = log_lines[start_idx:]
    else:
        target_segment = log_lines[start_idx:end_idx + 1]
    # logger.info(f'target_segment:\n{target_segment}')
    final_list = list()
    for item in target_segment:
        item = item.strip()
        if item:
            final_list.append(item)
    return final_list


def get_text_with_start_text_with_offset(str_list, start_text, start_index_offset=0):
    """
    解析日志文件中从!devstack开始到ServiceName is结束的目标片段
    :param log_file: 日志文件路径（如level_2_log.txt）
    :return: 目标解析片段（字符串格式），若解析失败返回None
    """
    # logger.info('get_text_with_start_and_end')
    start_idx = None

    # 2. 定位目标片段的起始行（包含"!devstack"的首行，即命令行起始）
    for idx, line in enumerate(str_list):
        if start_text in line:  # 匹配起始标记
            start_idx = idx
            # logger.info(f'start_idx: {start_idx}')
            break
    if start_idx is None:
        logger.info(f"❌ 未在日志中找到起始标记:{start_text}")
        return None
    else:
        end_idx = start_idx + start_index_offset  # 转换为全局索引

    target_segment = str_list[start_idx:end_idx + 1]
    # logger.info(f'target_segment:\n{target_segment}')
    final_list = list()
    for item in target_segment:
        item = item.strip()
        if item:
            final_list.append(item)
    return final_list


def get_text_with_start_and_end(str_list, start_text, end_text):
    """
    解析日志文件中从!devstack开始到ServiceName is结束的目标片段
    :param log_file: 日志文件路径（如level_2_log.txt）
    :return: 目标解析片段（字符串格式），若解析失败返回None
    """
    # logger.info(f'log_file:{log_file}')
    # 2. 定位目标片段的起始行（包含"!devstack"的首行，即命令行起始）
    start_idx = None
    for idx, line in enumerate(str_list):
        if start_text in line:  # 匹配起始标记
            start_idx = idx
            # logger.info(f'start_idx: {start_idx}')
            break
    if start_idx is None:
        logger.info(f"❌ 未在日志中找到起始标记:{start_text}")
        # logger.info(f'str_list:{str_list}')
        return None

    # 3. 定位目标片段的结束行（包含"ServiceName is"的行）
    end_idx = None
    # 从起始行之后开始查找，避免跨片段匹配
    for idx, line in enumerate(str_list[start_idx+1:]):
        if end_text in line:
            end_idx = start_idx + idx  # 转换为全局索引
            break
    if end_idx is None:
        logger.info(f"❌ 未在日志中找到结束标记{end_text}")
        target_segment = str_list[start_idx:]
    else: # case 1.3 include end text
        target_segment = str_list[start_idx:end_idx + 2]

    # logger.info(f'target_segment:\n{target_segment}')
    final_list = list()
    for item in target_segment:
        item = item.strip()
        if item:
            final_list.append(item)
    return final_list

def append_file_content(source_file, target_file):
    """
    将源文件的内容追加到目标文件的末尾

    参数:
        source_file: 源文件路径
        target_file: 目标文件路径
    """
    try:
        # 以只读模式打开源文件
        with open(source_file, 'r', encoding="utf-8") as src:
            # 读取源文件内容
            content = src.read()

        # 以追加模式打开目标文件，如果文件不存在则创建
        with open(target_file, 'a', encoding="utf-8") as dest:
            # 追加内容到目标文件
            dest.write(content)

        # logger.info(f"成功将 {source_file} 的内容追加到 {target_file}")

    except FileNotFoundError:
        logger.info(f"错误: 文件 {source_file} 不存在")
    except Exception as e:
        logger.info(f"发生错误: {str(e)}")
    return

def is_string_present(file_path: str, target_string: str, case_sensitive: bool = True) -> bool:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 处理大小写（若不区分，转为小写）
            if not case_sensitive:
                target_string = target_string.lower()

            for line in f:
                # 逐行检查（避免读取大文件占用过多内存）
                current_line = line if case_sensitive else line.lower()
                if target_string in current_line:
                    return True  # 找到匹配，立即返回
        # 循环结束未找到，返回False
        return False

    except FileNotFoundError:
        logger.info(f"警告: 文件未找到 - {file_path}")
        return False
    except PermissionError:
        logger.info(f"警告: 无权限读取文件 - {file_path}")
        return False
    except Exception as e:
        logger.info(f"警告: 读取文件失败 - {file_path}，错误信息: {str(e)}")
        return False

def read_file_by_line(file_name: str) -> list:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    with open (file_name, "r") as file:
        for line in file:
            # my_log.info (line.strip ())
            pass
    return


def read_file_dict(file_name: str) -> dict:
    record_dic = {}
    if '.yaml' in file_name:
        with open(file_name, 'r', encoding='utf-8') as wf:
            record_dic = yaml.safe_load(wf)
    elif '.json' in file_name:
        with open (file_name, 'r') as wf:
            record_dic = json.load (wf)
    else:
        # my_log.info(f'file not support:{read_file_dict}')
        pass
    return record_dic

def dump_file(file_name, data) -> int:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    # file_name = os.path.join(file_path, file_name)
    with open(file_name, 'w', encoding='utf-8') as wf:
        yaml.safe_dump(data, wf, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return 0

def read_file_str(file_name):
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    # 打开文件，返回一个文件对象
    with open(file_name, 'r', encoding='gbk') as file:
        # 读取文件的全部内容
        content = file.read()
        # my_log.info(content)
    return content

def wrtie_file(file_name, content) -> None:
    # 打开文件，如果文件不存在，会创建文件；'a' 表示追加模式，如果文件已存在，则会在文件末尾追加内容
    with open (file_name, 'w') as file:
        # 追加文本数据
        file.write(content)
    return

def add_string_to_first_line(file_path, new_string):
    try:
        # 以只读模式打开文件并读取所有内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 在内容开头插入新的字符串，并添加换行符
        lines.insert(0, new_string + '\n')

        # 以写入模式打开文件并将更新后的内容写回
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        # logger.info(f"成功在文件 {file_path} 的第一行添加字符串。")
    except FileNotFoundError:
        logger.info(f"未找到文件: {file_path}")
    except Exception as e:
        logger.info(f"发生错误: {e}")
    return

def get_file_content_list(file_path):
    log_lines = []
    try:
        # 以只读模式打开文件并读取所有内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_lines = f.readlines()  # 列表形式存储每一行日志，保留换行符
    except FileNotFoundError:
        logger.info(f"未找到文件: {file_path}")
    except Exception as e:
        logger.info(f"发生错误: {e}")
    return log_lines

def get_file_content_list_remove_empty_line(file_path):
    log_lines = []
    try:
        # 以只读模式打开文件并读取所有内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_lines = f.readlines()  # 列表形式存储每一行日志，保留换行符
    except FileNotFoundError:
        logger.info(f"未找到文件: {file_path}")
    except Exception as e:
        logger.info(f"发生错误: {e}")
    if log_lines:
        for line in log_lines:
            new_line = line.replace('\n', '').strip()
            # logger.info(f"new_line: {new_line}")
            if new_line == '':
                log_lines.remove(line)
                # logger.info(f"removed_line:")

    # logger.info(f"log_lines:{log_lines}")
    return log_lines


if __name__ == '__main__':
    file_name = 'BSOD_Debug_Report.yaml'
    result_dic = read_file_dict(file_name)
    summary_dic = result_dic.get('Summary', {})
    BSOD_Suspicious_Driver = summary_dic.get('BSOD_Suspicious_Driver', {})
    logger.info(f'BSOD_Suspicious_Driver:{BSOD_Suspicious_Driver}')

    file_name = 'BSOD_Cause_Driver_Matrix.json'
    data_dic = read_file_dict(file_name)
    solution_Categories = data_dic.get('Categories')

    tmp_dict = data_dic.get('Groups', [])
    logger.info(f"tmp_dict:{tmp_dict}")

    out_Category = None
    for key, cell_dict in tmp_dict.items():
        logger.info(f"key:{key}, value:{cell_dict}")
        Category = cell_dict.get('Category', None)
        logger.info(f"Category: {Category}")

        Drivers = cell_dict.get('Drivers', [])
        logger.info(f"Drivers: {Drivers}")

        for driver in Drivers:
            if BSOD_Suspicious_Driver in driver:
                out_Category = Category
                break
        if out_Category is not None:
            break

    solution = solution_Categories.get(out_Category, None)
    logger.info(f"solution: {solution}")


