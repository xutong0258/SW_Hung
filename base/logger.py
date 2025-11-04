# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re


# file = os.path.abspath(__file__)
path_dir = os.path.dirname(__file__)

LOG_DIR = os.path.join(path_dir, f"../../auto_test_log")
# print(f'LOG_DIR:{LOG_DIR}')

if not os.path.exists(LOG_DIR):
    # print(f'os.mkdir:{LOG_DIR}')
    os.mkdir(LOG_DIR)


time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
filename = f'test_{time_stamp}.log'

# 获取日志文件的绝对路径
log_file = os.path.join(LOG_DIR, filename)

formatter2 = logging.Formatter(
    '[%(asctime)s]'
    '%(filename)s'
    '[Line:%(lineno)d]: '
    '%(message)s'
)

CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)
CH.setFormatter(formatter2)

global current_enable
current_enable = False

if current_enable:
    LOG = logging.getLogger(__file__)
    LOG.setLevel (logging.DEBUG)
    LOG.addHandler (CH)

_format =('[%(asctime)s][%(filename)s][%(funcName)s][%(lineno)s]'
' %(levelname)s: %(message)s')

# for differnt module, different log

def init_logger(loggername, file=None):
    logger = logging.getLogger(loggername)
    logger.setLevel(level=logging.DEBUG)
    if not logger.handlers and file:
        file_handler = logging.FileHandler(file, encoding="utf8")
        file_format = logging.Formatter(_format)
        file_handler.setFormatter(file_format)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(CH)
    return logger

print(f'log_file:{log_file}')
logger = init_logger('HELLO', log_file)
# logger.info('hello')

# os.system
def cmd_excute(cmd, logger=None, outfile=None, errfile=None):
    if outfile is None and errfile is None:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())
        # result = stdout.decode('utf-8').strip('\r\n')
        result = stdout
        errors = stderr
        return_code = process.returncode
        msg = result if not stderr else errors
        if logger:
            logger.info(cmd)
            logger.debug(return_code)
            if return_code != 0:
                logger.error(errors)

        return result, errors, return_code
    else:
        f_out = open(outfile, 'w')
        f_err = open(errfile, 'w')
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=f_out,
            stderr=f_err)
        output, errors = process.communicate()
        return_code = process.returncode
        if logger:
            logger.info(cmd)
            logger.debug(return_code)
        if return_code != 0:
            logger.error(errors)

        return return_code


if __name__ == '__main__':
    pass
