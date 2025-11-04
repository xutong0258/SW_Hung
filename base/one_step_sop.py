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
        total_dict = {}
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
        total_dict['Automatic Analysis'] = Automatic_dict

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
        if step_only == 15 or step_only == 2:
            logger.info(f'2.Sysinfo')
            system_info_run(step_dict, current_step=2)
            total_dict['Sysinfo'] = step_dict
            # logger.info(f'total_dict:{total_dict}')

            sumarry_dict['CPUID'] = step_dict.get('CPUID', '')
            # logger.info(f'sumarry_dict:{sumarry_dict}')

            step_dict_str = update_Sysinfo_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'

            step_dict_str = update_Sysinfo_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 3. Current Thread
        if step_only == 15 or step_only == 3:
            step_dict = {}
            logger.info(f'3.Current Thread')
            current_thread_run(step_dict, current_step=3)
            total_dict['Current Thread'] = step_dict

            step_dict_str = update_Current_Thread_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 4. Process
        if step_only == 15 or step_only == 4:
            step_dict = {}
            logger.info(f'4.Process')
            process_vm_run(step_dict, current_step=4)
            total_dict['Process'] = step_dict

        # 5. Storage, Disk
        if step_only == 15 or step_only == 5:
            step_dict = {}
            logger.info(f'5.Storage')
            storage_run(step_dict, Automatic_dict, current_step=5)
            total_dict['Storage'] = step_dict

            step_dict_str = update_Storage_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'

            Disk1_Status_Abnormal = step_dict.get('Disk1_Status_Abnormal')
            Disk2_Status_Abnormal = step_dict.get('Disk2_Status_Abnormal')
            if Disk1_Status_Abnormal ==1 or Disk2_Status_Abnormal == 1:
                step_dict_str = update_Storage_debug_report(step_dict)
                debug_report_str = debug_report_str + step_dict_str + '\n'
        
        # 6. PnP
        if step_only == 15 or step_only == 6:
            step_dict = {}
            logger.info(f'6.PnP')
            PnP_run(step_dict, current_step=6)
            total_dict['PnP'] = step_dict

            step_dict_str = update_PnP_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'

            PnP_Status_Abnormal = step_dict.get('PnP_Status_Abnormal')

            sumarry_dict['PnP_Status_Abnormal'] = PnP_Status_Abnormal

            if PnP_Status_Abnormal == 1:
                step_dict_str = update_PnP_debug_report(step_dict)
                debug_report_str = debug_report_str + step_dict_str + '\n'

        # 7. ACPI
        if step_only == 15 or step_only == 7:
            step_dict = {}
            logger.info(f'7.ACPI')
            ACPI_run(step_dict, current_step=7)
            total_dict['ACPI'] = step_dict

            step_dict_str = update_ACPI_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'

            ACPI_Status_Abnormal = step_dict.get('ACPI_Status_Abnormal')
            sumarry_dict['ACPI_Status_Abnormal'] = ACPI_Status_Abnormal

            if ACPI_Status_Abnormal == 1:
                step_dict_str = update_ACPI_debug_report(step_dict)
                debug_report_str = debug_report_str + step_dict_str + '\n'

        # 8. NDIS
        if step_only == 15 or step_only == 8:
            step_dict = {}
            logger.info(f'8.NDIS')
            ndis_run(step_dict, current_step=8)
            total_dict['NDIS'] = step_dict

            step_dict_str = update_NDIS_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'

            NDIS_Status_Abnormal = step_dict.get('NDIS_Status_Abnormal')
            sumarry_dict['NDIS_Status_Abnormal'] = NDIS_Status_Abnormal

            if NDIS_Status_Abnormal ==1:
                step_dict_str = update_NDIS_debug_report(step_dict)
                debug_report_str = debug_report_str + step_dict_str + '\n'

        # 9. USB
        if step_only == 15 or step_only == 9:
            step_dict = {}
            logger.info(f'9.USB')
            usb_run(step_dict, current_step=9)
            total_dict['USB'] = step_dict

            step_dict_str = update_usb_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'


        # 10. WHEA_0x124
        if BUGCHECK_CODE == '124' and (step_only == 15 or step_only == 10):
            step_dict = {}
            logger.info(f'10.WHEA_0x124')
            WHEA_0x124_run(step_dict, BUGCHECK_P2, current_step=10)
            total_dict['WHEA_0x124'] = step_dict

            step_dict_str = update_WHEA_0x124_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'

            step_dict_str = update_WHEA_0x124_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

            sumarry_dict['CPU_Status_Abnormal'] = step_dict.get('CPU_Status_Abnormal', '')
            sumarry_dict['WHEA_Status_Abnormal'] = step_dict.get('WHEA_Status_Abnormal', '')

        # 11. Power_0x9f_3
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '3' and (step_only == 15 or step_only == 11):
            step_dict = {}
            logger.info(f'11.Power_0x9f_3')
            Power_0x9f_3_run(step_dict, Automatic_dict,current_step=11)
            total_dict['Power_0x9f_3'] = step_dict

            step_dict_str = update_Power_0x9f_3_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'
            sumarry_dict['BSOD_Suspicious_Driver'] = step_dict.get('BSOD_Suspicious_Driver', '')
            sumarry_dict['BSOD_Suspicious_Device'] = step_dict.get('BSOD_Suspicious_Device', '')
            sumarry_dict['The_Power_Management_Status_Abnormal'] = step_dict.get('The_Power_Management_Status_Abnormal', '')

            step_dict_str = update_Power_0x9f_3_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 12. Power_0x9f_4
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '4' and (step_only == 15 or step_only == 12):
            step_dict = {}
            logger.info(f'12.Power_0x9f_4')
            Power_0x9f_4_run(step_dict, Automatic_dict, current_step=12)
            total_dict['Power_0x9f_3'] = step_dict

            step_dict_str = update_Power_0x9f_4_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'
            sumarry_dict['BSOD_Suspicious_Driver'] = step_dict.get('BSOD_Suspicious_Driver', '')
            sumarry_dict['BSOD_Suspicious_Device'] = step_dict.get('BSOD_Suspicious_Device', '')
            
            step_dict_str = update_Power_0x9f_4_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 13. DPC_0x133
        if BUGCHECK_CODE == '133' and (step_only == 15 or step_only == 13):
            step_dict = {}
            step_dict['BSOD_Suspicious_Driver'] = MODULE_NAME
            logger.info(f'13.dpc')
            dpc_run(step_dict, Automatic_dict, current_step=13)

            total_dict['dpc'] = step_dict
            sumarry_dict['BSOD_Suspicious_Driver'] = step_dict.get('BSOD_Suspicious_Driver', '')
            sumarry_dict['BSOD_Suspicious_Device'] = step_dict.get('BSOD_Suspicious_Device', '')

            step_dict_str = update_dpc_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 14. locks_0xE2
        if BUGCHECK_CODE == 'e2' and (step_only == 15 or step_only == 14):
            step_dict = {}
            logger.info(f'14.locks_0xE2')
            locks_run(step_dict, current_step=14)
            total_dict['locks_0xE2'] = step_dict

            step_dict_str = update_locks_0xE2_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'
            BSOD_Suspicious_Driver = step_dict.get('BSOD_Suspicious_Driver', None)
            if BSOD_Suspicious_Driver is not None:
                sumarry_dict['BSOD_Suspicious_Driver'] = BSOD_Suspicious_Driver
            
            step_dict_str = update_locks_0xE2_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'
    finally:
        windbg.stop(path_dir)

    step_dict_str = update_summary_report(sumarry_dict)
    debug_report_str = step_dict_str + '\n' +debug_report_str

    dump_result_yaml(total_dict, debug_data_str, path_dir, debug_report_str)

    # post_report_process(path_dir)
    return