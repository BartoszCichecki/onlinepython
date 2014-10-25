# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 16:55:02 2014

@author: Harri
"""

"""
Python modules
"""
import psutil
import subprocess
import time
from pprint import pprint

"""
Own created files
"""
from pypy_config import *
from pypy_stats import *

def run_file(script_file):
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
    
    
    return tot_time, memory_usage


#print("Memory used: " + str(memory_usage/1024/1024*1.0) + " megabytes")
#print("Time used: " + str(tot_time) + "s")

tot_time, memory_usage = run_file('test.py')

add_id = addStats(memory_usage, tot_time)

print("ID: " + str(add_id))

print("Memory used: " + str(memory_usage/1024/1024*1.0) + " megabytes")
print("Time used: " + str(tot_time) + "s")

