# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re

from base.helper import *
from base import fileOP
from base.contants import *

def update_Automatic_debug_data(result_dict):
    dict_str = 'Automatic Analysis: \n'
    content_list = ['BUGCHECK_CODE',
                    'BUGCHECK_P1',
                    'BUGCHECK_P2',
                    'BUGCHECK_P3',
                    'BUGCHECK_P4',
                    'FAILURE_BUCKET_ID',
                    'MODULE_NAME',
                    'Disk_Status_Abnormal',
                    'Memory_Status_Abnormal',
                    'DISK_HARDWARE_ERROR_Status',
                    'Context_Memory_Corruption_Status',
                    'Stack_Memory_Operation_Status',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_Automatic_debug_report(result_dict):
    tmp_dict = {}
    step_dict = {}
    content_list = ['Bugcheck_Analysis',
                    'FAILURE_BUCKET_ID',
                    'MODULE_NAME',
                    'Disk_Status_Abnormal',
                    'Memory_Status_Abnormal',
                    'DISK_HARDWARE_ERROR_Status',
                    'Context_Memory_Corruption_Status',
                    'Stack_Memory_Operation_Status',
                    'Trap_Frame_Context',
                    'STACK_TEXT',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        if 'STACK_TEXT' in content:
            value = value.replace('STACK_TEXT', '\n')
        tmp_dict[content] = value
    step_dict['Automatic Analysis'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)

    return log_lines_str

def update_Sysinfo_debug_data(result_dict):
    dict_str = 'Sysinfo: \n'
    content_list = ['OS_Version_ID',
                    'CPUID']
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_Sysinfo_debug_report(result_dict):
    tmp_dict = {}
    step_dict = {}
    content_list = ['OS_Version_ID',
                    'CPUID']
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['Sysinfo'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_Current_Thread_report(result_dict):
    tmp_dict = {}
    step_dict = {}
    content_list = ['Current_Thread_Power_Status_Abnormal',
                    'blocked_IRP_address_status',
                    'nt!PopFxActivateDevice_Status',
                    'BSOD_Suspicious_Driver',
                    'BSOD_Suspicious_Device',
                    'thread_Context',
                    'running_Context',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['Current Thread'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)

    return log_lines_str

def update_Storage_debug_data(result_dict):
    dict_str = 'Storage: \n'
    content_list = ['Disk1_Status_Abnormal',
                    'Disk2_Status_Abnormal',
                    'BSOD_Suspicious_Device',
                    'Storclass_FDO1_DeviceID',
                    'Storclass_FDO1_Failed_Requests_Status',
                    'storadapter_adapter1_SurpriseRemoval_Status',
                    'storadapter_storunit1_Outstanding_IRP_Status',
                    'Storclass_FDO2_DeviceID',
                    'Storclass_FDO2_Failed_Requests_Status',
                    'storadapter_adapter2_SurpriseRemoval_Status',
                    'storadapter_storunit2_Outstanding_IRP_Status',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_Storage_debug_report(result_dict):
    tmp_dict = {}
    step_dict = {}
    content_list = ['Disk1_Status_Abnormal',
                    'Storclass_FDO1_DeviceID',
                    'Storclass_FDO1_Failed_Requests_Status',
                    'storadapter_adapter1_SurpriseRemoval_Status',
                    'storadapter_storunit1_Outstanding_IRP_Status',
                    'Disk2_Status_Abnormal',
                    'Storclass_FDO2_DeviceID',
                    'Storclass_FDO2_Failed_Requests_Status',
                    'storadapter_adapter2_SurpriseRemoval_Status',
                    'storadapter_storunit2_Outstanding_IRP_Status',
                    'storadapter_adapter1_driver',
                    'storadapter_adapter1_Context',
                    'storadapter_adapter2_driver',
                    'storadapter_adapter2_Context',
                    'Storclass_FDO1_DeviceID',
                    'Storclass_FDO1_Context',
                    'Storclass_FDO2_DeviceID',
                    'Storclass_FDO2_Context',
                    'storadapter_storunit1_Context',
                    'storadapter_storunit2_Context'
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['Storage'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)

    return log_lines_str

def update_PnP_debug_data(result_dict):
    dict_str = 'PnP: \n'
    content_list = ['PnP_Status_Abnormal',
                    'PnP_blocked_IRP_address_status',
                    'pending_Removal_status',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_PnP_debug_report(result_dict):
    content_list = ['Pending_Removal_Context',
                    'BSOD_Suspicious_Driver',
                    'BSOD_Suspicious_Device',
                    'System_State_Context',
                    'Device_State_Context',
                    ]
    tmp_dict = {}
    step_dict = {}
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['PnP'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)

    return log_lines_str

def update_ACPI_debug_data(result_dict):
    dict_str = 'ACPI: \n'
    content_list = ['ACPI_Status_Abnormal',
                    'ACPI_Method_Object',
                    'ACPI_Method_Status',
                    'ACPI_Method_AMLPointer']
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_ACPI_debug_report(result_dict):
    content_list = ['Pending_Removal_Context',
                    'BSOD_Suspicious_Driver',
                    'BSOD_Suspicious_Device',
                    'System_State_Context',
                    'Device_State_Context',
                    ]
    tmp_dict = {}
    step_dict = {}
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['ACPI'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)

    return log_lines_str

def update_NDIS_debug_data(result_dict):
    dict_str = 'NDIS: \n'
    content_list = ['NDIS_Status_Abnormal',
                    'NDIS_OID_Pending_Status',
                    'Ndis_netadapter1_name',
                    'Ndis_netadapter2_name',]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_NDIS_debug_report(result_dict):
    tmp_dict = {}
    step_dict = {}
    content_list = ['NDIS_Status_Abnormal',
                    'NDIS_OID_Pending_Status',
                    'Ndis_netadapter1_name',
                    'Ndis_netadapter2_name',
                    'NDIS_OID_Context',
                    'NDIS_netadapter1_Context',
                    'NDIS_netadapter2_Context',]
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['NDIS'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_usb_debug_report(result_dict):
    tmp_dict = {}
    step_dict = {}
    content_list = ['usb_tree_Context',]
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['USB'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_WHEA_0x124_debug_data(result_dict):
    dict_str = 'WHEA_0x124: \n'
    content_list = ['WHEA_Status_Abnormal',
                    'BSOD_Suspicious_Device',
                    'WHEA_ERROR_RECORD_Type',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_WHEA_0x124_debug_report(result_dict):
    content_list = ['WHEA_Status_Abnormal',
                    'CPU_Status_Abnormal',
                    'BSOD_Suspicious_Device',
                    'WHEA_ERROR_RECORD_Type',
                    'WHEA_ERROR_RECORD_Context',
                    'WHEA_Context',
                    ]
    tmp_dict = {}
    step_dict = {}
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['WHEA_0x124'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_Power_0x9f_3_debug_data(result_dict):
    dict_str = 'Power_0x9f_3: \n'
    content_list = ['The_Power_Management_Status_Abnormal',
                    'BSOD_Suspicious_Device',
                    'BSOD_Suspicious_Driver',
                    'blocked_device_ServiceName',
                    'blocked_device_DeviceInst',
                    'blocked_IRP_Driver',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_Power_0x9f_3_debug_report(result_dict):
    content_list = ['The_Power_Management_Status_Abnormal',
                    'BSOD_Suspicious_Device',
                    'BSOD_Suspicious_Driver',
                    'blocked_device_ServiceName',
                    'blocked_device_DeviceInst',
                    'blocked_IRP_Driver',
                    'blocked_device_Context',
                    'blocked_irp_context',
                    'System_State_Context',
                    'Device_State_Context',
                    ]
    tmp_dict = {}
    step_dict = {}
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['Power_0x9f_3'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_Power_0x9f_4_debug_data(result_dict):
    dict_str = 'Power_0x9f_4: \n'
    content_list = ['The_Power_Management_Status_Abnormal',
                    'nt!PopFxActivateDevice_Status',
                    'blocked_IRP_address_status',
                    'BSOD_Suspicious_Device',
                    'BSOD_Suspicious_Driver',
                    'blocked_device_ServiceName',
                    'blocked_device_DeviceInst',
                    'blocked_IRP_Driver',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_Power_0x9f_4_debug_report(result_dict):
    content_list = ['The_Power_Management_Status_Abnormal',
                    'nt!PopFxActivateDevice_Status',
                    'blocked_IRP_address_status',
                    'BSOD_Suspicious_Device',
                    'BSOD_Suspicious_Driver',
                    'blocked_device_ServiceName',
                    'blocked_device_DeviceInst',
                    'blocked_IRP_Driver',
                    'blocked_device_Context',
                    'blocked_irp_context',
                    'System_State_Context',
                    'Device_State_Context',
                    ]
    tmp_dict = {}
    step_dict = {}
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['Power_0x9f_4'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_dpc_debug_report(result_dict):
    content_list = ['The_DPC_Status_Abnormal',
                    'swd_DPCTimeout_CPU',
                    'swd_DPCTimeout_Context',
                    'dpcwatchdog_context',
                    'DPCTimeout_thread_Context',
                    ]
    tmp_dict = {}
    step_dict = {}
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['DPC_0x133'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_locks_0xE2_debug_data(result_dict):
    dict_str = 'locks_0xE2: \n'
    content_list = ['locks_thread_Status_Abnormal',
                    'blocked_IRP_address_status',
                    'nt!PopFxActivateDevice_Status',
                    'BSOD_Suspicious_Device',
                    'BSOD_Suspicious_Driver',
                    'blocked_device_ServiceName',
                    'blocked_device_DeviceInst',
                    'blocked_IRP_Driver',
                    ]
    for content in content_list:
        value = result_dict.get(content, '')
        value = str(value)
        dict_str = dict_str + f'  {content}: ' + value + '\n'
    return dict_str

def update_locks_0xE2_debug_report(result_dict):
    content_list = ['locks_thread_Status_Abnormal',
                    'blocked_IRP_address_status',
                    'nt!PopFxActivateDevice_Status',
                    'BSOD_Suspicious_Device',
                    'BSOD_Suspicious_Driver',
                    'blocked_device_ServiceName',
                    'blocked_device_DeviceInst',
                    'blocked_IRP_Driver',
                    'blocked_thread_context',
                    ]
    tmp_dict = {}
    step_dict = {}
    for content in content_list:
        value = result_dict.get(content, '')
        tmp_dict[content] = value
    step_dict['locks_0xE2'] = tmp_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    return log_lines_str

def update_summary_report(result_dict):
    step_dict = {}
    step_dict['Summary'] = result_dict

    result_yaml_file = 'tmp.yaml'
    result_yaml_file = os.path.join('./', result_yaml_file)
    fileOP.dump_file(result_yaml_file, step_dict)

    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)

    return log_lines_str

def dump_result_yaml(result_dict, BSOD_Debug_Data_str, dir_name, BSOD_Debug_report_str=None):
    # last dump
    result_yaml_file = 'result.yaml'
    result_yaml_file = os.path.join(dir_name, result_yaml_file)
    fileOP.dump_file(result_yaml_file, result_dict)

    # remove multiply line issue
    log_lines = fileOP.get_file_content_list_remove_empty_line(result_yaml_file)
    log_lines_str = ''.join(log_lines)
    fileOP.wrtie_file(result_yaml_file, log_lines_str)

    result_yaml_file = 'BSOD_Debug_Data.yaml'
    result_yaml_file = os.path.join(dir_name, result_yaml_file)
    fileOP.wrtie_file(result_yaml_file, BSOD_Debug_Data_str)

    if BSOD_Debug_report_str:
        result_yaml_file = 'BSOD_Debug_Report.yaml'
        result_yaml_file = os.path.join(dir_name, result_yaml_file)
        fileOP.wrtie_file(result_yaml_file, BSOD_Debug_report_str)

    return

def parse_blocked_IRP_Address(cmd_output_list, result_dict):
    blocked_device_Address = None
    # logger.info(f'cmd_output_list: {cmd_output_list}')
    if cmd_output_list:
        result_str = '\n' + '\n'.join(cmd_output_list)
        result_dict['blocked_irp_context'] = result_str

        index = get_stack_begin_index(cmd_output_list)
        if index is not None:
            # 偏移3行
            blocked_IRP_Driver = cmd_output_list[index+2].strip()
            logger.info(f'blocked_IRP_Driver: {blocked_IRP_Driver}')
            split_list = blocked_IRP_Driver.split('\t')
            blocked_IRP_Driver = split_list[0]
            logger.info(f'blocked_IRP_Driver: {blocked_IRP_Driver}')
            last_index = get_list_text_line_last_index(blocked_IRP_Driver, '\\')
            blocked_IRP_Driver = blocked_IRP_Driver[last_index+1:]
            logger.info(f'blocked_IRP_Driver: {blocked_IRP_Driver}')
            if ',' in blocked_IRP_Driver:
                split_list = blocked_IRP_Driver.split(',')
                blocked_IRP_Driver = split_list[0]
                logger.info(f'blocked_IRP_Driver: {blocked_IRP_Driver}')
            result_dict['blocked_IRP_Driver'] = blocked_IRP_Driver

            # 偏移2行
            blocked_device_Address = cmd_output_list[index+1].strip()
            logger.info(f'blocked_device_Address: {blocked_device_Address}')
            split_list = blocked_device_Address.split(' ')
            # logger.info(f'split_list: {split_list}')
            blocked_device_Address = get_address_by_list(split_list)

            logger.info(f'blocked_device_Address: {blocked_device_Address}')
            result_dict['blocked_device_Address'] = blocked_device_Address

    return blocked_device_Address

def get_blocked_IRP_Address_thread(cmd_output_list, result_dict):
    blocked_IRP_Address = None
    blocked_IRP_address_status = 0
    if cmd_output_list:
        result_str = '\n' + '\n'.join(cmd_output_list)
        result_dict['Locks_thread_context'] = result_str

        for idx, line in enumerate(cmd_output_list):
            line = line.strip()
            if 'IRP List' in line:
                logger.info(f'IRP List: {cmd_output_list[idx + 1]}')
                blocked_IRP_Address = cmd_output_list[idx + 1].split(':')[0]
                logger.info(f'blocked_IRP_Address: {blocked_IRP_Address}')
                result_dict['blocked_IRP_Address'] = blocked_IRP_Address
                blocked_IRP_address_status = 1

    result_dict['blocked_IRP_address_status'] = blocked_IRP_address_status
    logger.info(f'blocked_IRP_address_status: {blocked_IRP_address_status}')

    return blocked_IRP_Address

def get_blocked_IRP_Address_pnp(cmd_output_list, result_dict):
    blocked_IRP_Address = None
    PnP_blocked_IRP_address_status = 0
    if cmd_output_list:
        result_str = '\n' + '\n'.join(cmd_output_list)
        result_dict['Locks_thread_context'] = result_str

        for idx, line in enumerate(cmd_output_list):
            line = line.strip()
            if 'IRP List' in line:
                logger.info(f'IRP List: {cmd_output_list[idx + 1]}')
                blocked_IRP_Address = cmd_output_list[idx + 1].split(':')[0]
                logger.info(f'blocked_IRP_Address: {blocked_IRP_Address}')
                result_dict['blocked_IRP_Address'] = blocked_IRP_Address
                PnP_blocked_IRP_address_status = 1

    result_dict['PnP_blocked_IRP_address_status'] = PnP_blocked_IRP_address_status
    logger.info(f'PnP_blocked_IRP_address_status: {PnP_blocked_IRP_address_status}')
    return blocked_IRP_Address

def parse_locks_info(cmd_output_list, result_dict):
    new_result = get_list_strip(cmd_output_list)
    result_dict['Locks_Context'] = new_result

    # 执行解析
    # logger.info(f'file_content_new: {file_content_new}')
    thread_contention_pairs,Locks_thread_Address = fileOP.parse_locks_content(new_result)
    logger.info(f'thread_contention_pairs: {thread_contention_pairs}')
    if Locks_thread_Address is not None:
        Locks_thread_Address = Locks_thread_Address.replace('-01<*>', '').strip()
        logger.info(f'Locks_thread_Address: {Locks_thread_Address}')

        result_dict['Locks_thread_Address'] = Locks_thread_Address
        result_dict['blocked_thread_Address'] = Locks_thread_Address

    if Locks_thread_Address:
        result_dict['Locks_thread_Status'] = 1
    else:
        result_dict['Locks_thread_Status'] = 0

    return Locks_thread_Address


def parse_vertarget(cmd_output, result_dict):
    result_dict['vertarget_Context'] = cmd_output

    cmd_output_list = cmd_output.splitlines()
    OS_Version_ID = None
    if cmd_output_list:
        OS_Version_ID = get_list_text_line(cmd_output_list, 'Edition build lab')

        match = re.search(r'\d+\.\d+', OS_Version_ID)

        if match:
            OS_Version_ID = match.group()
            logger.info(f"OS_Version_ID：{OS_Version_ID}")  # 输出：9600.17238

        else:
            logger.info("未找到OS_Version_ID")

    if OS_Version_ID:
        result_dict['OS_Version_ID'] = float(OS_Version_ID)
    else:
        result_dict['OS_Version_ID'] = OS_Version_ID
    return

def parse_sysinfo_cpuspeed(cmd_output, result_dict):
    result_dict['cpuspeed_context'] = cmd_output

    cmd_output_list = cmd_output.splitlines()
    CPUID = None
    if cmd_output_list:
        CPUID = get_list_text_line(cmd_output_list, 'CPUID:')
        # logger.info(f'CPUID: {CPUID}')
        match = re.search(r'CPUID:(.*)', CPUID)
        if match:
            CPUID = match.group()
            # logger.info(f"CPUID：{CPUID}")
        else:
            logger.info("未找到数字部分")
        CPUID = CPUID.replace('CPUID:', '')
        CPUID = CPUID.replace('"', '').strip()
        logger.info(f'CPUID: {CPUID}')

    result_dict['CPUID'] = CPUID
    return

def parse_amli_r(cmd_output_list, result_dict):
    ACPI_Method_AMLPointer = ''
    # new_result = get_list_strip(cmd_output_list)
    # # logger.info(f'new_result: {new_result}')
    # result_dict['ACPI_Method_Context'] = new_result

    ACPI_Method_AMLPointer = get_list_text_line(cmd_output_list, 'Next AML Pointer:')

    # 使用正则表达式匹配 [ 和 + 之间的内容
    match = re.search(r'\[(.*?)\+', ACPI_Method_AMLPointer)

    if match:
        ACPI_Method_AMLPointer = match.group(1)
    else:
        logger.info(f'can\'t find ACPI_Method_AMLPointer')

    result_dict['ACPI_Method_AMLPointer'] = ACPI_Method_AMLPointer
    logger.info(f'ACPI_Method_AMLPointer: {ACPI_Method_AMLPointer}')
    return

def parse_ndiskd_oid(cmd_output_list, result_dict):
    Ndis_netadapter1_address = None
    Ndis_netadapter2_address = None
    NDIS_OID_Pending_Status = 0

    text_lines = get_list_text_lines(cmd_output_list, 'NetAdapter')
    if text_lines:
        # logger.info(f'NetAdapter text_lines: {text_lines}')
        NDIS_OID_Pending_Status = 1
        Ndis_netadapter1_name = None
        text_line = text_lines[0].replace('NetAdapter', '').strip()

        match = re.search(r' - (.*)', text_line)
        if match:
            Ndis_netadapter1_name = match.group()
            # logger.info(f"Ndis_netadapter1_name：{Ndis_netadapter1_name}")
            Ndis_netadapter1_name = Ndis_netadapter1_name.replace(' - ', '').strip()
            # logger.info(f"Ndis_netadapter1_name：{Ndis_netadapter1_name}")
        else:
            logger.info("未找到: Ndis_netadapter1_name")

        temp_list = text_line.split('-')
        Ndis_netadapter1_address = temp_list[0].strip()
        # Ndis_netadapter1_name = temp_list[1].strip() # NG

        logger.info(f'NDIS_netadapter1_address: {Ndis_netadapter1_address}')
        logger.info(f'Ndis_netadapter1_name: {Ndis_netadapter1_name}')

        result_dict['Ndis_netadapter1_address'] = Ndis_netadapter1_address
        result_dict['Ndis_netadapter1_name'] = Ndis_netadapter1_name

    if len(text_lines)>=2:
        text_line = text_lines[1].replace('NetAdapter', '').strip()
        temp_list = text_line.split('-')
        Ndis_netadapter2_address = temp_list[0].strip()
        # Ndis_netadapter2_name = temp_list[1].strip() # NG

        match = re.search(r' - (.*)', text_line)
        if match:
            Ndis_netadapter2_name = match.group()
            # logger.info(f"Ndis_netadapter2_name：{Ndis_netadapter2_name}")
            Ndis_netadapter2_name = Ndis_netadapter2_name.replace(' - ', '').strip()
            # logger.info(f"Ndis_netadapter2_name：{Ndis_netadapter2_name}")
        else:
            logger.info("未找到: Ndis_netadapter2_name")

        logger.info(f'Ndis_netadapter2_address: {Ndis_netadapter2_address}')
        logger.info(f'Ndis_netadapter2_name: {Ndis_netadapter2_name}')

        result_dict['Ndis_netadapter2_address'] = Ndis_netadapter2_address
        result_dict['Ndis_netadapter2_name'] = f'{Ndis_netadapter2_name}'


    result_dict['NDIS_OID_Pending_Status'] = NDIS_OID_Pending_Status

    return Ndis_netadapter1_address, Ndis_netadapter2_address

def parse_analyze_v(cmd_output, result_dict):
    cmd_output_list = cmd_output.splitlines()

    start_text = f'***************************'
    end_text = 'Debugging Details:'

    result_list = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)
    new_list = remove_list_text_with_target_text(result_list, '*', 'Bugcheck Analysis')

    # remove Debugging Details:
    new_list = new_list[:-1]

    result_str = '\n' + '\n'.join(new_list)
    result_dict['Bugcheck_Analysis'] = result_str

    item_list = ['BUGCHECK_CODE', 'BUGCHECK_P1', 'BUGCHECK_P2', 'BUGCHECK_P3', 'BUGCHECK_P4', 'FAILURE_BUCKET_ID', 'MODULE_NAME']

    update_dict_by_parse(cmd_output_list, item_list, result_dict)

    DISK_HARDWARE_ERROR_Status = 0
    Disk_Status_Abnormal = 0
    count = get_list_text_count(cmd_output_list, 'DISK_HARDWARE_ERROR')

    if count:
        DISK_HARDWARE_ERROR_Status = 1
        Disk_Status_Abnormal = 1


    result_dict['DISK_HARDWARE_ERROR_Status'] = DISK_HARDWARE_ERROR_Status
    result_dict['Disk_Status_Abnormal'] = Disk_Status_Abnormal

    # Trap_Frame_Context
    update_Trap_Frame_Context(cmd_output_list, result_dict)

    # STACK_TEXT
    start_text = f'STACK_TEXT:'
    end_text = 'SYMBOL_NAME:'
    result = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)
    update_context_with_list(result, result_dict, 'STACK_TEXT')

    Stack_Memory_Operation_Status = 0
    if result:
        Stack_Memory_Operation_Status = get_Stack_Memory_Operation_Status(result)

    logger.info(f'Stack_Memory_Operation_Status: {Stack_Memory_Operation_Status}')
    result_dict['Stack_Memory_Operation_Status'] = Stack_Memory_Operation_Status

    Memory_Status_Abnormal = 0
    Context_Memory_Corruption_Status = result_dict.get('Context_Memory_Corruption_Status')
    if Context_Memory_Corruption_Status or Stack_Memory_Operation_Status:
        Memory_Status_Abnormal = 1

    result_dict['Memory_Status_Abnormal'] = Memory_Status_Abnormal

    return

def get_driver(input_str):
    # 定义要匹配的前缀
    prefix = '\\Driver\\'

    # 检查字符串是否包含目标前缀
    if prefix in input_str:
        # 找到前缀结束的位置
        prefix_end_index = input_str.find(prefix) + len(prefix)

        # 从 prefix 结束位置开始，截取到制表符(\t)出现的位置
        # 因为原字符串中 igfx 后面是制表符分隔
        tab_index = input_str.find('\t', prefix_end_index)

        # 提取目标字段
        if tab_index != -1:
            target_field = input_str[prefix_end_index:tab_index]
            # logger.info(f"提取到的字段: {target_field}")  # 输出: igfx
        else:
            # 如果没有制表符，直接取剩余全部内容
            target_field = input_str[prefix_end_index:]
            # logger.info(f"提取到的字段: {target_field}")
    else:
        logger.info(f"字符串中不包含前缀: {prefix}")

    return target_field

def parse_amli_lc(cmd_output_list, result_dict):
    ACPI_Method_Address = ''
    ACPI_Method_Object = ''
    ACPI_Method_Status = 0
    for item in cmd_output_list:
        logger.info(f"item: {item}")
        if 'Ctxt=' in item:
            ACPI_Method_Address = re.findall(r'Ctxt=(.*?),', item)
            ACPI_Method_Address = ACPI_Method_Address[0]
            ACPI_Method_Status = 1
        if 'Obj=' in item:
            prefix = "Obj="
            # 查找前缀在字符串中的位置
            prefix_index = item.find(prefix)
            if prefix_index != -1:
                # 提取前缀后面的所有内容（从prefix结束位置开始截取）
                ACPI_Method_Object = item[prefix_index + len(prefix):]
                ACPI_Method_Object = ACPI_Method_Object.strip()
                logger.info(f"提取到的Obj字段值: {ACPI_Method_Object}")  # 输出: _SB,hello
            else:
                logger.info(f"字符串中未找到 '{prefix}'")
            ACPI_Method_Status = 1

    result_dict['ACPI_Method_Status'] = ACPI_Method_Status
    result_dict['ACPI_Method_Address'] = ACPI_Method_Address
    result_dict['ACPI_Method_Object'] = ACPI_Method_Object

    logger.info(f"ACPI_Method_Address: {ACPI_Method_Address}")
    logger.info(f"ACPI_Method_Object: {ACPI_Method_Object}")
    logger.info(f"ACPI_Method_Status: {ACPI_Method_Status}")
    return


def parse_storadapter_storadapter_adapter_address1_sub(cmd_output_list, result_dict):
    first_index = get_list_text_line_first_index(cmd_output_list, 'Product')
    if first_index:
        target_line = cmd_output_list[first_index + 3]
        # logger.info(f'target_line:{target_line}')

        split_list = target_line.split(' ')
        # logger.info(f'split_list:{split_list}')
        storadapter_storunit1_address = get_list_first_valide_adress(split_list)
        # logger.info(f'storadapter_storunit1_address: {storadapter_storunit1_address}')
        if storadapter_storunit1_address:
            result_dict['storadapter_storunit1_address'] = storadapter_storunit1_address
            logger.info(f'storadapter_storunit1_address: {storadapter_storunit1_address}')

    last_index = get_list_text_line_last_index(cmd_output_list, 'Product')
    if last_index and last_index != first_index:
        target_line = cmd_output_list[last_index + 3]
        # logger.info(f'target_line:{target_line}')

        split_list = target_line.split(' ')
        # logger.info(f'split_list:{split_list}')
        storadapter_storunit2_address = get_list_first_valide_adress(split_list)
        if storadapter_storunit2_address:
            result_dict['storadapter_storunit2_address'] = storadapter_storunit2_address
            logger.info(f'storadapter_storunit2_address: {storadapter_storunit2_address}')
    return

def parse_storadapter_storadapter_adapter_address2_sub(cmd_output_list, result_dict):
    first_index = get_list_text_line_first_index(cmd_output_list, 'Product')
    if first_index:
        target_line = cmd_output_list[first_index + 3]
        # logger.info(f'target_line:{target_line}')

        split_list = target_line.split(' ')
        # logger.info(f'split_list:{split_list}')
        storadapter_storunit1_address = get_list_first_valide_value(split_list)
        result_dict['storadapter_storunit1_address'] = storadapter_storunit1_address
    return

def parse_storadapter_storadapter_adapter1_address(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['storadapter_adapter1_Context'] = result_str

    count = get_list_text_count(cmd_output_list, 'SurpriseRemoval')
    if count:
        storadapter_adapter1_SurpriseRemoval_Status = 1
    else:
        storadapter_adapter1_SurpriseRemoval_Status = 0
    result_dict['storadapter_adapter1_SurpriseRemoval_Status'] = storadapter_adapter1_SurpriseRemoval_Status

    parse_storadapter_storadapter_adapter_address1_sub(cmd_output_list, result_dict)

    return

def parse_storadapter_storadapter_adapter2_address(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['storadapter_adapter2_Context'] = result_str

    count = get_list_text_count(cmd_output_list, 'SurpriseRemoval')
    if count:
        storadapter_adapter2_SurpriseRemoval_Status = 1
    else:
        storadapter_adapter2_SurpriseRemoval_Status = 0
    result_dict['storadapter_adapter2_SurpriseRemoval_Status'] = storadapter_adapter2_SurpriseRemoval_Status

    parse_storadapter_storadapter_adapter_address2_sub(cmd_output_list, result_dict)
    return

def parse_storadapter(cmd_output_list, result_dict):
    for idx, line in enumerate(cmd_output_list):
        # logger.info(f'line: {line}')

        if 'Driver' in line and 'Object' in line:
            parse_storadapter_driver_and_address(cmd_output_list[idx + 2], result_dict)
    return

def parse_storagekd_storclass(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['Storclass_FDO1_Context'] = result_str
    # need logic
    count = get_list_text_count(cmd_output_list, 'Retried')
    if count > 4:
        Storclass_FDO1_Failed_Requests_Status = 1
    else:
        Storclass_FDO1_Failed_Requests_Status = 0

    result_dict['Storclass_FDO1_Failed_Requests_Status'] = Storclass_FDO1_Failed_Requests_Status

    return

def parse_storclass(result_list, result_dict):
    for idx, line in enumerate(result_list):
        if 'FDO' in line and '# Device ID' in line:
            Storclass_FDO1_address = result_list[idx + 2]
            # logger.info(f'Storclass_FDO1: {Storclass_FDO1_address}')
            split_list = Storclass_FDO1_address.split(' ')
            # logger.info(f'split_list: {split_list}')

            Storclass_FDO1_address = split_list[0]
            Storclass_FDO1_DeviceID = f'{split_list[5]} {split_list[6]}'

            Storclass_0_FL = split_list[-1]
            logger.info(f'Storclass_0_FL: {Storclass_0_FL}')

            # logger.info(f'Storclass_FDO1_DeviceID: {Storclass_FDO1_DeviceID}')
            # logger.info(f'Storclass_FDO1_address: {Storclass_FDO1_address}')

            result_dict['Storclass_FDO1_address'] = Storclass_FDO1_address
            result_dict['Storclass_FDO1_DeviceID'] = Storclass_FDO1_DeviceID
            result_dict['Storclass_0_FL'] = Storclass_0_FL

            logger.info(f'result_dict: {result_dict}')

            Storclass_FDO2_address = result_list[idx + 3]
            split_list = Storclass_FDO2_address.split(' ')
            Storclass_FDO2_address = split_list[0]
            if is_address(Storclass_FDO2_address):
                Storclass_FDO2_DeviceID = f'{split_list[5]} {split_list[6]}'

                Storclass_1_FL = split_list[-1]
                logger.info(f'Storclass_1_FL: {Storclass_1_FL}')

                # logger.info(f'Storclass_FDO1_DeviceID: {Storclass_FDO1_DeviceID}')
                # logger.info(f'Storclass_FDO1_address: {Storclass_FDO1_address}')

                result_dict['Storclass_FDO2_address'] = Storclass_FDO2_address
                result_dict['Storclass_FDO2_DeviceID'] = Storclass_FDO2_DeviceID
                result_dict['Storclass_1_FL'] = Storclass_1_FL
    return


def parse_powertriage(cmd_output_list, result_dict):
    # logger.info(f'result_dict type: {type(result_dict, current_step)}')
    # System_State_Context
    index = get_list_text_line_first_index(cmd_output_list, 'Power Action:')
    start_idx = index + 1
    end_idx = start_idx + 6
    System_State_Context = cmd_output_list[start_idx: end_idx]
    System_State_Context = '\n'.join(System_State_Context).strip()
    result_dict['System_State_Context'] = System_State_Context
    logger.info(f'System_State_Context: {System_State_Context}')


    index = get_list_text_line_first_index(cmd_output_list, '+')
    logger.info(f'index: {index}')
    start_idx = index + 1

    # logger.info(f'cmd_output_list: {cmd_output_list}')
    offset_index = get_Device_State_Context_last_index(cmd_output_list[start_idx:])
    if offset_index is None:
        offset_index = 3
        logger.info(f'offset_index: {offset_index}')

    end_idx = start_idx + offset_index

    Device_State_Context = cmd_output_list[start_idx: end_idx]
    Device_State_Context = '\n'.join(Device_State_Context).strip()
    result_dict['Device_State_Context'] = Device_State_Context
    logger.info(f'Device_State_Context: {Device_State_Context}')
    return

def parse_devstack(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['blocked_device_Context'] = result_str

    line = get_list_text_line(cmd_output_list, 'ServiceName is')
    if line:
        line = line.replace('ServiceName is', '')
        line = line.replace('"', '').strip()
        result_dict['blocked_device_ServiceName'] = line

    line = get_list_text_line(cmd_output_list, 'DeviceInst is')
    if line:
        line = line.replace('DeviceInst is', '')
        line = line.replace('"', '').strip()
        result_dict['blocked_device_DeviceInst'] = line

    line = get_list_text_line(cmd_output_list[1:], '>')
    # logger.info(f'line: {line}')
    if line:
         split_list = line.split(' ')
         # logger.info(f'split_list: {split_list}')

         new_list = get_list_strip(split_list)
         # logger.info(f'new_list: {new_list}')

         blocked_device_DevExta_address = new_list[3]
         logger.info(f'blocked_device_DevExta_address: {blocked_device_DevExta_address}')
         result_dict['blocked_device_DevExta_address'] = blocked_device_DevExta_address
    return



if __name__ == '__main__':
    logger.info('common hello')
    pass
