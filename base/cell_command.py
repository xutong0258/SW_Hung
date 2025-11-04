# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re
import subprocess
from base.contants import *
from base.helper import *
from base.common import *
from base.AdvancedWinDbgInterface import *


def analyze_v_run(result_dict, current_step):
    # time.sleep(3)  # 等待初始化
    cmd = "!analyze -v"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step=1, timeout=15)

    # logger.info(f'cmd_output type:\n{cmd_output}')

    parse_analyze_v(cmd_output, result_dict)
    return

def thread_blocked_thread_Address(result_dict,blocked_thread_Address, current_step):
    cmd = f"!thread {blocked_thread_Address}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd_output_list = cmd_output.splitlines()
    blocked_IRP_Address = get_blocked_IRP_Address_thread(cmd_output_list, result_dict)

    count = get_list_text_count(cmd_output_list, 'nt!PopFxActivateDevice')
    # nt!PopFxActivateDevice_Status = 1
    # nt!PopFxActivateDevice_frameNo = 4
    PopFxActivateDevice_Status = 0
    PopFxActivateDevice_frameNo = 0
    if count:
        PopFxActivateDevice_Status = 1
        PopFxActivateDevice_frameNo = 4

    result_dict['nt!PopFxActivateDevice_Status'] = PopFxActivateDevice_Status
    result_dict['nt!PopFxActivateDevice_frameNo'] = PopFxActivateDevice_frameNo

    return blocked_IRP_Address

def irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step):
    cmd = f"!irp {blocked_IRP_Address}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd_output_list = cmd_output.splitlines()

    blocked_device_Address = parse_blocked_IRP_Address(cmd_output_list, result_dict)

    return blocked_device_Address

def devstack_blocked_device_Address(result_dict, blocked_device_Address, current_step):
    # !devstack blocked_device_Address
    cmd = f"!devstack {blocked_device_Address}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    # logger.info(f'cmd_output: {cmd_output}')

    cmd_output_list = cmd_output.splitlines()
    parse_devstack(cmd_output_list, result_dict)
    return

def powertriage(result_dict, current_step):
    # logger.info(f'result_dict type: {type(result_dict, current_step)}')

    # !powertriage
    cmd = f"!powertriage"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd_output_list = cmd_output.splitlines()
    parse_powertriage(cmd_output_list, result_dict)

    blocked_IRP_Driver = result_dict.get('blocked_IRP_Driver', None)
    if blocked_IRP_Driver:
        result_dict['BSOD_Suspicious_Driver'] = blocked_IRP_Driver
    logger.info(f'BSOD_Suspicious_Driver: {blocked_IRP_Driver}')

    blocked_device_ServiceName = result_dict.get('blocked_device_ServiceName', None)
    logger.info(f'blocked_device_ServiceName: {blocked_device_ServiceName}')

    blocked_device_DeviceInst = result_dict.get('blocked_device_DeviceInst', None)
    logger.info(f'blocked_device_DeviceInst: {blocked_device_DeviceInst}')

    if blocked_device_ServiceName and blocked_device_DeviceInst:
        BSOD_Suspicious_Device =  f'{blocked_device_ServiceName} {blocked_device_DeviceInst}'
        result_dict['BSOD_Suspicious_Device'] = BSOD_Suspicious_Device
        logger.info(f'BSOD_Suspicious_Device: {BSOD_Suspicious_Device}')
    return

def amli_r_ACPI_Method_Address(result_dict, current_step):
    ACPI_Method_Address = result_dict['ACPI_Method_Address']
    cmd = f"!amli r {ACPI_Method_Address}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    update_context(cmd_output, result_dict, 'ACPI_Method_Context')

    cmd_output_list = cmd_output.splitlines()
    parse_amli_r(cmd_output_list, result_dict)
    return

def amli_lc_ACPI_Method_Address(result_dict, current_step):
    cmd = f"!amli lc"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    # logger.info(f'amli lc: {cmd_output}')

    cmd_output_list = cmd_output.splitlines()
    parse_amli_lc(cmd_output_list, result_dict)
    return

def locks(result_dict, current_step):
    cmd = "!locks"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd_output_list = cmd_output.splitlines()

    blocked_thread_Address = parse_locks_info(cmd_output_list, result_dict)

    return blocked_thread_Address

def pnptriage(result_dict, current_step):
    cmd = "!pnptriage"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd_output_list = cmd_output.splitlines()
    get_blocked_IRP_Address_pnp(cmd_output_list, result_dict)
    return

def frame_r_nt_PopFxActivateDevice_frameNo(result_dict, current_step):
    PopFxActivateDevice_frameNo = result_dict.get('nt!PopFxActivateDevice_frameNo', None)
    if PopFxActivateDevice_frameNo is None:
        return

    cmd = f".frame /r {PopFxActivateDevice_frameNo}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd_output_list = cmd_output.splitlines()

    target_line = get_list_text_line(cmd_output_list, 'rbx=')
    logger.info(f'target_line: {target_line}')

    match = re.search(r'rbx=(.*) ', target_line)

    if match:
        PopFxActivateDevice = match.group()
        logger.info(f"PopFxActivateDevice：{PopFxActivateDevice}")
        PopFxActivateDevice = PopFxActivateDevice.replace('rbx=', '')
        PopFxActivateDevice = PopFxActivateDevice.strip()
        logger.info(f"PopFxActivateDevice：{PopFxActivateDevice}")
        result_dict['nt!PopFxActivateDevice'] = PopFxActivateDevice
        result_dict['nt!PopFxActivateDevice_address'] = PopFxActivateDevice
    else:
        logger.info("未找到: (.*)_IRP")

    return

# dt _pop_fx_device nt!PopFxActivateDevice_address
# dt_pop_fx_device_nt_PopFxActivateDevice_address
def dt_pop_fx_device_nt_PopFxActivateDevice_address(result_dict, current_step):
    PopFxActivateDevice_address = result_dict.get('nt!PopFxActivateDevice_address', None)
    if PopFxActivateDevice_address is None:
        return
    cmd = f"dt _pop_fx_device {PopFxActivateDevice_address}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd_output_list = cmd_output.splitlines()

    target_line = get_list_text_line(cmd_output_list, 'Irp')
    logger.info(f'target_line: {target_line}')

    match = re.search(r': (.*) _IRP', target_line)

    if match:
        blocked_IRP_Address = match.group()
        blocked_IRP_Address = blocked_IRP_Address.replace(': ', '')
        blocked_IRP_Address = blocked_IRP_Address.replace('_IRP', '')
        blocked_IRP_Address = blocked_IRP_Address.strip()
        logger.info(f"blocked_IRP_Address：{blocked_IRP_Address}")
        result_dict['blocked_IRP_Address'] = blocked_IRP_Address
    else:
        logger.info("未找到: (.*)_IRP")

    target_line = get_list_text_line(cmd_output_list, 'DeviceObject')
    logger.info(f'target_line: {target_line}')

    match = re.search(r': (.*) _DEVICE_OBJECT', target_line)

    if match:
        blocked_device_Address = match.group()
        blocked_device_Address = blocked_device_Address.replace(': ', '')
        blocked_device_Address = blocked_device_Address.replace('_DEVICE_OBJECT', '')
        blocked_device_Address = blocked_device_Address.strip()
        logger.info(f"blocked_device_Address：{blocked_device_Address}")
        result_dict['blocked_device_Address'] = blocked_device_Address
    else:
        logger.info("未找到:': (.*) _DEVICE_OBJECT'")

    return

if __name__ == '__main__':
    # cmd = " ".join(args)
    # result, errors, return_code = cmd_excute(cmd)
    # logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')
    #
    # cmd = 'qqd'
    # result, errors, return_code = cmd_excute(cmd)
    # logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')
    pass
