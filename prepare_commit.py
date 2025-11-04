import os
import shutil
from base.util import *

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


def file_walk():
    # 要遍历的文件路径
    folder_path = BASEDIR
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            path = os.path.join(root, dir)
            if '.' in path and '.git' not in path and '.idea' not in path:
                print(f"del: {path}")
                delete_folder(path)
        for file in files:
            file_path = os.path.join(root, file)
            # print(file_path)
            if '.log' in file_path or '.yaml' in file_path:
                os.remove(file_path)
                print(f"del: {file_path}")
    return

def clean_dir(folder_path):
    if not os.path.exists(folder_path):
       return
    shutil.rmtree(folder_path)
    # os.mkdir(folder_path)

if __name__ == '__main__':
    file_walk()
    remove_cache(BASEDIR, dst_dir='cache__')
   # remove_cache(BASEDIR, dst_dir='report')
   # remove_cache(BASEDIR, dst_dir='.pytest_cache')
   # clean_dir(folder_path='../auto_test_log')
