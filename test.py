import os
import shutil
import sys
import logging
import time
import datetime
import re
from base.helper import *
from base import fileOP


if __name__ == '__main__':
    result_dict = {}
    result_yaml_file = 'result.yaml'
    result_dict['Ndis_netadapter1_name'] = 'Microsoft Wi-Fi Direct Virtual Adapter #2'
    result_dict['Ndis_netadapter12name'] = 'Realtek 8821CE Wireless LAN 802.11ac PCI-E NIC'
    fileOP.dump_file(result_yaml_file, result_dict)
    pass
