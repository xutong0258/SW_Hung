# coding=utf-8
import os
import sys
import re
import platform
import datetime

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)
base_name = os.path.basename(path_dir)

sys.path.append(path_dir)


NOT_FOUND = "Not_Found"
FOUND = 'Found'
windbgx_path = r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\WinDbgX.exe"
kdX86_path = r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\kdX86.exe"
# SYMBOL_PATH = "srv*%temp%\\SymCache*http://msdl.microsoft.com/download/symbols"
SYMBOL_PATH = "SRV*C:\Symbols*http://msdl.microsoft.com/download/symbols"
PXACmd_TOOL = r'D:\小拉\Tools\PXA_1.1.1.26_2025091014317836_rel\PXA.exe'
TIME_OUT = 3
TIME_OUT_2 = 5
TIME_OUT_5 = 5
TIME_OUT_10 = 10
TIME_OUT_ANA = 30
TIME_OUT_ANA = 18

command_sleep_map = {
    'analyze': 10,
    'storadapter': 6,
    'devstack': 15,
    'powertriage': 35, # 30
    'amli lc': 15,
    'locks': 15,
    '!WHEA': 10,
    'errrec': 10,
    'irp': 10,
    'usb_tree': 25,
    'thread': 5,
    'running': 5,
    'amli r': 15,
}