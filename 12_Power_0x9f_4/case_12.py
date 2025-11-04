import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\12. Power_0x9f_4\12.1 0x9f_4_IRP\开发样本_0x9f_4_IRP_Intel WLAN'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    one_process_run(dump_file, path_dir, step_only=12)