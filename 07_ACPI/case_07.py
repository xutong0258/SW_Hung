import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)

# OK
src_dir = r'D:\0_LOG_VIP\1_Automatic\1.1_0x3b_Context_Memory_Corruption'
src_dir = r'D:\0_LOG_VIP\2_Sysinfo\2.1_0x124_0_Machine_Check_Error'
src_dir = r'D:\0_LOG_VIP\4_Process\4.1_SW Hung_0xEF_Locks_rtux64w10'
src_dir = r'D:\0_LOG_VIP\5_Storage\5.1_Disk_0x7A_SurpriseRemoval'
src_dir = r'D:\0_LOG_VIP\6_PnP\6.1_SW_Hung_0xEF_Locks_NTFS_Disk_Retried_Failed_Request'

if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\7. ACPI\7.2 DPC 0x133 1 ACPI\开发样本_DPC 0x133 1 ACPI'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')

    one_process_run(dump_file, path_dir, step_only=7)