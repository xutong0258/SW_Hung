from base import fileOP
from base.helper import *

if __name__ == '__main__':
    target_line = r'0 e0 ffff840dd8876030 ffff840de120fef0 fffff80ecdcc68c0-ffffb88bdc579090 Success Error Cancel'
    # target_line = target_line.replace('\t', '')
    split_list = target_line.split(' ')
    logger.info(f'split_list: {split_list}')
