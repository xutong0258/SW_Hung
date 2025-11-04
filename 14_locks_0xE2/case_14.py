import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\14. Locks_0xe2\14.1 SW Hung 0xEF Locks rtux64w10'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    one_process_run(dump_file, path_dir, step_only=14)