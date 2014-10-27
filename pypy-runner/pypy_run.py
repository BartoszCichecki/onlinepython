# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 16:55:02 2014

@author: Harri
"""

#Python modules
from __future__ import print_function
import psutil
import subprocess
import time
import sys
#from pprint import pprint

#Own created files

from pypy_config import PYPY_EXEC, SCRIPT_DIR
from pypy_stats import add_stats

#CONSTANTS
#How often memory usage is checked (seconds)
CHECK_TIME = 0.05

def check_output(script_file, check_file):
    """Check python script's output.

    Keyword arguments:
    script_file -- The file to be run
    check_file -- The file to check output against
    """
    try:
        check_file = open(SCRIPT_DIR + check_file, 'r')
    except IOError:
        return False
    lines = []
    for line in check_file:
        if len(line.strip()) > 0:
            lines.append(line.strip())
    check_file.close()
    proc = subprocess.Popen(PYPY_EXEC + ' "' + SCRIPT_DIR + script_file + '"',
                            stdout=subprocess.PIPE)
    out, err = proc.communicate()
    outputlines = [line.strip() for line in out.splitlines() if len(line) > 0]
    if len(outputlines) != len(lines):
        return False
    for i in range(len(outputlines)):
#        print("Line1: " + str(lines[i]) + " - Line2: " + str(outputlines[i]))
        if lines[i] != outputlines[i]:
            return False
    return True


def run_file(script_file):
    """Run a python script.

    Keyword arguments:
    script_file -- The file to be run
    """
    start_time = time.time()
    proc = subprocess.Popen(PYPY_EXEC + ' "' + SCRIPT_DIR + script_file + '"')
    memory_usage = []
    try:
        while proc.poll() == None:
            memory_usage.append(psutil.Process(proc.pid).get_memory_info())
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

def main(argv):
    """Run program
    """
    correct = check_output('test.py', 'test.txt')

    tot_time, memory_usage = run_file('test.py')

    add_id = add_stats(memory_usage, tot_time, correct)

    print("ID: " + str(add_id))

    print("Memory used: " + str(memory_usage/1024/1024*1.0) + " megabytes")
    print("Time used: " + str(tot_time) + "s")
    print("Correct output: " + str(correct))

if __name__ == "__main__":
    main(sys.argv)


