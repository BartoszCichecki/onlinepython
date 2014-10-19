# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 16:55:02 2014

@author: Harri
"""

import psutil
import subprocess
import time
from pprint import pprint

from pypy_config import *

script_file = 'test.py'

#How often memory usage is checked (seconds)
CHECK_TIME = 0.05
start_time = time.time()
p = subprocess.Popen(prog + ' "' + script_dir + script_file + '"')
memory_usage = []
try:
    while p.poll() == None:
        memory_usage.append(psutil.Process(p.pid).get_memory_info())
        time.sleep(CHECK_TIME)
#Sometimes process dies before stats are fetched
except psutil.NoSuchProcess:
    pass
    #print("Error")

#Total run time for script
tot_time = time.time() - start_time

#pprint(memory_usage)

#Get maximum of memory usage
memory_usage = max([x[1] for x in memory_usage])


#for result in resultTable[-1]:
#    pprint(result)

print("Memory used: " + str(memory_usage/1024/1024*1.0) + " megabytes")
print("Time used: " + str(tot_time) + "s")
