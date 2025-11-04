import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\5. Storage\5.1 Disk_0x7A_SurpriseRemoval'

    dump_file = os.path.join(src_dir, 'MEMORY.DMP')

    one_process_run(dump_file, path_dir, step_only=5)