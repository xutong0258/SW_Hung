import json
from base.common import *
from base import fileOP
from base.helper import *
from base.componet import *
from base.AdvancedWinDbgInterface import *
from base.cell_command import *
from base.util import *

def one_process_run(dump_file, path_dir, step_only=15):
    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    try:
        step_dict = {}
        Automatic_dict = {}
        debug_data_str = ''
        sumarry_dict = {}

        debug_report_str = ''

        #default
        sumarry_dict['BSOD_Suspicious_Driver'] = ''
        sumarry_dict['BSOD_Suspicious_Device'] = ''

        content_list = ['Current_Thread_Power_Status_Abnormal',
                        'Locked_Thread_Power_Status_Abnormal',
                        'The_Power_Management_Status_Abnormal',
                        'CPU_Status_Abnormal',
                        'Memory_Status_Abnormal',
                        'Disk_Status_Abnormal',
                        'WHEA_Status_Abnormal',
                        'PnP_Status_Abnormal',
                        'ACPI_Status_Abnormal',
                        'NDIS_Status_Abnormal',
                        ]
        for item in content_list:
            sumarry_dict[item] = 0

        sumarry_dict['CPUID'] = ''

        # 1. Automatic
        logger.info(f'1.Automatic')
        analyze_v_run(Automatic_dict, current_step=1)

        step_dict_str = update_Automatic_debug_data(Automatic_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'

        sumarry_dict['Memory_Status_Abnormal'] = Automatic_dict.get('Memory_Status_Abnormal', '')
        sumarry_dict['Disk_Status_Abnormal'] = Automatic_dict.get('Disk_Status_Abnormal', '')

        step_dict_str = update_Automatic_debug_report(Automatic_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'

        BUGCHECK_CODE = Automatic_dict.get('BUGCHECK_CODE', None)
        BUGCHECK_P1 = Automatic_dict.get('BUGCHECK_P1', None)
        BUGCHECK_P2 = Automatic_dict.get('BUGCHECK_P2', None)
        MODULE_NAME = Automatic_dict.get('MODULE_NAME', None)

        # logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
        # logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')
        # logger.info(f'MODULE_NAME: {MODULE_NAME}')

        # 2. Sysinfo
        # if step_only == 15 or step_only == 2:
        Sysinfo_dict = {}
        logger.info(f'2.Sysinfo')
        system_info_run(Sysinfo_dict, current_step=2)

        sumarry_dict['CPUID'] = Sysinfo_dict.get('CPUID', '')
        # logger.info(f'sumarry_dict:{sumarry_dict}')

        step_dict_str = update_Sysinfo_debug_data(Sysinfo_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'

        step_dict_str = update_Sysinfo_debug_report(Sysinfo_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'

        # 3. Current Thread
        # if step_only == 16 or step_only == 3:
        Current_Thread_dict = {}
        logger.info(f'3.Current Thread')
        current_thread_run(Current_Thread_dict, current_step=3)

        step_dict_str = update_Current_Thread_report(Current_Thread_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'

        # 4. Process
        # if step_only == 16 or step_only == 4:
        Process_dict = {}
        logger.info(f'4.Process')
        process_vm_run(Process_dict, current_step=4)

        # 5. Storage, Disk
        # if step_only == 15 or step_only == 5:
        Storage_dict = {}
        logger.info(f'5.Storage')
        storage_run(Storage_dict, Automatic_dict, current_step=5)

        step_dict_str = update_Storage_debug_data(Storage_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'

        Disk1_Status_Abnormal = Storage_dict.get('Disk1_Status_Abnormal')
        Disk2_Status_Abnormal = Storage_dict.get('Disk2_Status_Abnormal')
        if Disk1_Status_Abnormal ==1 or Disk2_Status_Abnormal == 1:
            step_dict_str = update_Storage_debug_report(Storage_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 14. locks_0xE2
        # if BUGCHECK_CODE == 'e2' and (step_only == 15 or step_only == 14):
        locks_dict = {}
        logger.info(f'14.locks_0xE2')
        locks_run(locks_dict, current_step=14)

        step_dict_str = update_locks_0xE2_debug_data(locks_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'
        BSOD_Suspicious_Driver = locks_dict.get('BSOD_Suspicious_Driver', None)
        if BSOD_Suspicious_Driver is not None:
            sumarry_dict['BSOD_Suspicious_Driver'] = BSOD_Suspicious_Driver

        step_dict_str = update_locks_0xE2_debug_report(locks_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'
    finally:
        windbg.stop(path_dir)

    step_dict_str = update_summary_report(sumarry_dict)
    debug_report_str = step_dict_str + '\n' +debug_report_str

    total_dict = {}

    total_dict['Summary'] = sumarry_dict
    total_dict['Automatic'] = Automatic_dict
    total_dict['Sysinfo'] = Sysinfo_dict
    total_dict['Storage'] = Storage_dict
    total_dict['locks'] = locks_dict

    dump_result_yaml(total_dict, debug_data_str, path_dir, debug_report_str)
    return