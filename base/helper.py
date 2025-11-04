# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re
import cv2
import subprocess
from pathlib import Path
from base.logger import *
from base import fileOP

# file = os.path.abspath(__file__)
path_dir = os.path.dirname(__file__)


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

def update_Context_Memory_Corruption_Status(input_list, result_dict):
    Context_Memory_Corruption_Status = 0

    content_count = get_list_text_count(input_list, '=?')
    logger.info(f'content_count:{content_count}')
    if content_count:
        Context_Memory_Corruption_Status = 1

    if input_list and len(input_list) > 2:
        target_list = input_list[-3:]
        count = get_list_text_count(target_list, '?')
        # logger.info(f'target_list:{target_list}')
        # logger.info(f'count:{count}')
        if count:
            Context_Memory_Corruption_Status = 1
    result_dict['Context_Memory_Corruption_Status'] = Context_Memory_Corruption_Status
    return

def update_Trap_Frame_Context(cmd_output_list, result_dict):
    # Trap_Frame_Context
    start_text = f'CONTEXT:'
    end_text = 'Resetting default scope'
    result = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)
    result_dict['Context_Memory_Corruption_Status'] = 0
    if result:
        update_context_with_list(result, result_dict, 'Trap_Frame_Context')
        update_Context_Memory_Corruption_Status(result, result_dict)

    start_text = f'TRAP_FRAME'
    end_text = 'Resetting default scope'
    result = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)
    if result:
        update_context_with_list(result, result_dict, 'Trap_Frame_Context')
        update_Context_Memory_Corruption_Status(result, result_dict)
    return

def get_address_by_list(input_list):
    adress = None
    for item in input_list:
        if len(item) > 3:
            adress = item
            break
    return adress

def get_stack_begin_index(input_list):
    index = None
    for idx, line in enumerate(input_list):
        line = line.strip()
        # logger.info(f'line: {line}, idx: {idx}')
        if '>' in line and 'kd>' not in line:
            index = idx
            break
    return index

def is_address(obj):
    # 排除布尔类型（虽然bool是int的子类，但通常不视为数字）
    if 'ffff' in obj:
        return True
    else:
        return False

def get_storadapter_driver_and_address(input_line, result_dict, index):
    storadapter_adapter_driver = None
    storadapter_adapter_address = None

    if '\Driver' in input_line:
        split_list = input_line.split(' ')
        # logger.info(f'split_list: {split_list}')

        storadapter_adapter_driver = split_list[0]
        result_dict[f'storadapter_adapter{index}_driver'] = storadapter_adapter_driver
        logger.info(f'storadapter_adapter{index}_driver: {storadapter_adapter_driver}')

        for idx, line in enumerate(split_list):
            if '' != line and idx > 0:
                result_dict[f'storadapter_adapter{index}_address'] = line
                logger.info(f'storadapter_adapter_address: {line}')
                break
    return storadapter_adapter_driver, storadapter_adapter_address

def parse_storadapter_driver_and_address(input_list, result_dict):
    # logger.info(f'input_list: {input_list}')
    get_storadapter_driver_and_address(input_list[0], result_dict, 1)
    if len(input_list) > 1:
        get_storadapter_driver_and_address(input_list[1], result_dict, 2)
    return


def update_dict_by_parse(cmd_output_list, item_list, result_dict):
    for item in item_list:
        value = get_list_text_line(cmd_output_list, f'{item}')
        value = value.replace(f'{item}:', '').strip()
        result_dict[f'{item}'] = value
    # logger.info(f'result_dict:{result_dict}')
    return

def get_Stack_Memory_Operation_Status(result):
    Stack_Memory_Operation_Status = 0
    for idx, line in enumerate(result):
        if 'nt!KeBugCheck' in line:
            # logger.info(f'line: {line}')
            target_line = result[idx + 1]
            target_line = target_line.lower()
            # logger.info(f'last_line: {last_line}')
            if 'nt!mi' in target_line or 'nt!kipagefault' in target_line or 'nt!mm' in target_line:
                Stack_Memory_Operation_Status = 1
                break
            target_line = result[idx + 2]
            target_line = target_line.lower()
            # logger.info(f'last_line: {last_line}')
            if 'nt!mi' in target_line or 'nt!kipagefault' in target_line or 'nt!mm' in target_line:
                Stack_Memory_Operation_Status = 1
                break
    return Stack_Memory_Operation_Status

def get_list_first_valide_value(result):
    return_value = None
    for item in result:
        if len(item) > 3:
            return item
    return return_value

def get_list_first_valide_adress(result):
    return_value = None
    for item in result:
        if len(item) > 4 and 'ffff' in item:
            return item
    return return_value

def get_list_text_line_last_index(input_list, text):
    index = None
    if input_list is None:
        return index

    for idx, line in enumerate(input_list):
        if text in line:
            index = idx
    return index

def get_Device_State_Context_last_index(input_list):
    index = None
    if input_list is None:
        return index

    for idx, line in enumerate(input_list):
        # logger.info(f'line: {line}')
        if 'Error' in line:
            index = idx
        if '+' in line:
            break
    logger.info(f'index: {index}')
    return index

def get_list_text_line_first_index(input_list, text):
    index = None
    if input_list is None:
        return index

    for idx, line in enumerate(input_list):
        if text in line:
            index = idx
            break
    return index

def get_list_text_line(result, text):
    text_line = ''
    if result is None:
        return text_line

    for item in result:
        if text in item:
            text_line = item
            break
    return text_line

def get_list_strip(result):
    text_lines = []
    if result is None:
        return text_lines

    for item in result:
        item = item.strip('\n')
        item = item.strip()
        if item:
            # logger.info(f'item:{item}')
            text_lines.append(f'{item}')
    return text_lines

def get_list_text_lines(result, text):
    text_lines = []
    if result is None:
        return text_lines
    for item in result:
        value = item.strip('\n')
        value = item.strip()
        if value and text in value:
            text_lines.append(value)
    return text_lines

def is_list_has_target_text(text_list, target_text):
    has_target_text = False
    for item in text_list:
        if target_text in item:
            has_target_text = True
            break
    return has_target_text

def get_list_text_count(result, text):
    text_line = None
    count = 0
    if result is None:
        return count

    for item in result:
        if text in item:
            count = count + 1
    return count

def remove_list_text_with_target_text(input_list, remove_target_text_1, remove_target_text_2):
    new_list = []
    if input_list is None:
        return new_list

    for item in input_list:
        item = item.replace(remove_target_text_1, '').strip()
        item = item.replace(remove_target_text_2, '').strip()
        if item :
            new_list.append(item)
    return new_list

def update_context(input_str, result_dict, key):
    cmd_output_list = input_str.splitlines()
    index = get_list_text_line_first_index(cmd_output_list, 'kd>')
    if index is not None:
        target_list = cmd_output_list[index+1:]
        target_str = '\n'.join(target_list)
        result_dict[key] = target_str
    else:
        result_dict[key] = input_str
    return

def update_context_with_list(cmd_output_list, result_dict, key):
    target_str = None
    index = get_list_text_line_first_index(cmd_output_list, 'kd>')
    if index is not None:
        target_list = cmd_output_list[index+1:]
        target_str = '\n'.join(target_list)
    else:
        if cmd_output_list:
            target_str = '\n'.join(cmd_output_list)

    if target_str:
        result_dict[key] = target_str
    return

if __name__ == '__main__':
    obj = 'ffffe00167eea1c0'
    value = is_address(obj)
    logger.info(value)
    # cmd = " ".join(args)
    # result, errors, return_code = cmd_excute(cmd)
    # logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')
    #
    # cmd = 'qqd'
    # result, errors, return_code = cmd_excute(cmd)
    # logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')
    pass
