# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 16:55:02 2014
@author: Harri
"""

#Python modules
import os
import psutil
import subprocess
import tempfile
import time

#Own created files
import db
from config import PYPY_EXEC, PYPY_CHECK_TIME
from db_model import Solution

def run_file(interview, exercise, submitted_code):
    temp_dir_path = tempfile.mkdtemp(prefix='pyinterviews_')

    script_file = open(temp_dir_path + os.sep + 'script.py', 'w')
    script_file.write(submitted_code)
    script_file.close()

    expected_output = exercise.expected_output

    correct = check_output(script_file, expected_output)

    if correct:    
        execution_time, memory_usage = measure_usage(script_file)
    
    solution = Solution()
    solution.interview = interview
    solution.exercise = exercise
    solution.submitted_code = submitted_code
    solution.correct = correct
    solution.execution_time = execution_time
    solution.memory_usage = memory_usage
    db.add_solution(solution)

def check_output(script_file, expected_output):
    proc = subprocess.Popen(PYPY_EXEC + ' "' + script_file.name + '"',
                            stdout=subprocess.PIPE)
    output, error = proc.communicate()

    if error is not None:
        return False

    output_lines = [line.strip() for line in output.splitlines() if len(line) > 0]
    expected_output_lines = [line.strip() for line in expected_output.split('\n') if len(line) > 0]

    if len(output_lines) != len(expected_output_lines):
        return False
    for i in range(len(output_lines)):
        if expected_output[i] != output_lines[i]:
            return False

    return True

def measure_usage(script_file):
    start_time = time.time()
    proc = subprocess.Popen(PYPY_EXEC + ' "' + script_file.name + '"')

    memory_usage = []
    try:
        while proc.poll() == None:
            memory_usage.append(psutil.Process(proc.pid).get_memory_info())
            time.sleep(PYPY_CHECK_TIME)

    except psutil.NoSuchProcess:
        pass

    execution_time = time.time() - start_time
    memory_usage = max([x[1] for x in memory_usage])

    return execution_time, memory_usage
