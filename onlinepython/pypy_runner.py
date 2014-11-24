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
    """Run a python script.

    Keyword arguments:
    interview -- Interview object
    exercise -- Exercise object
    submitted_code -- The script to run (string)
    """
    temp_dir_path = tempfile.mkdtemp(prefix='pyinterviews_')

    script_file = open(temp_dir_path + os.sep + 'script.py', 'w')
    script_filename = script_file.name
    script_file.write(submitted_code)
    script_file.close()

    expected_output = exercise.expected_output

    result = check_output(script_filename, expected_output)

#    if correct:
    execution_time, memory_usage = measure_usage(script_filename)
    result['execution_time'] = execution_time
    result['memory_usage'] = memory_usage

    solution = Solution()
    solution.interview = interview
    solution.exercise = exercise
    solution.submitted_code = submitted_code
    solution.correct = result['correct']
    solution.execution_time = execution_time
    solution.memory_usage = memory_usage
    db.add_solution(solution)
    result['expected_output'] = expected_output
    return result

def check_output(script_file, expected_output):
    """Check output of a python script.

    Keyword arguments:
    script_file -- Filename of python script
    expected_output -- Output to compare to
    """
    exec_string = [cmd for cmd in PYPY_EXEC]
    exec_string.append(script_file)

    proc = subprocess.Popen(exec_string, stdout=subprocess.PIPE)
    output, error = proc.communicate()
    result = {}
    result['output'] = output
    result['correct'] = True

    if error is not None:
        result['correct'] = False
        return result

    output_lines = [str(line.strip()) for line
                    in output.splitlines() if len(line) > 0]
    expected_output_lines = [str(line.strip()) for line
                             in expected_output.split('\n') if len(line) > 0]
    if len(output_lines) != len(expected_output_lines):
        result['correct'] = False
        return result
    for i in range(len(output_lines)):
        if expected_output_lines[i] != output_lines[i]:
            result['correct'] = False
            return result

    return result

def measure_usage(script_file):
    """Check resource usage of a python script.

    Keyword arguments:
    script_file -- Filename of python script
    """
    exec_string = [cmd for cmd in PYPY_EXEC]
    exec_string.append(script_file)

    start_time = time.time()
    proc = subprocess.Popen(exec_string)

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
