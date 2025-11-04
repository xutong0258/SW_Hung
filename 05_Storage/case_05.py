import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'D:\00\05_SW_Hung\SWhang_DiskIO_MemoryDump\MemoryDump'

    dump_file = os.path.join(src_dir, 'MEMORY.DMP')

    one_process_run(dump_file, path_dir, step_only=5)