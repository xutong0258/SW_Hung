import os
import shutil
from base.folder_file import *

BASEDIR = os.path.dirname(__file__)
print(f'BASEDIR:{BASEDIR}')


def remove_cache(folder_path, dst_dir='cache__'):
    for root, dirs, files in os.walk(folder_path):
        # print (f"root: {root}")
        # print (f"dirs: {dirs}")
        for dir in dirs:
            if dst_dir in dir:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)
                print(f"del: {dir_path}")
    return

if __name__ == '__main__':
    file_walk_delete_file(file_format='.log')
    remove_cache(BASEDIR, dst_dir='cache__')
