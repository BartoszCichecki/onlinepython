# -*- coding: utf-8 -*-
"""
This module is a part fo OnlinePython project created at DTU
for the course Data Mining Using Python.

The module contains helper methods that did not belong in any other module.

Created on Wed Dec 03 11:38:45 2014

@author: Harri
"""

import matplotlib
# Needed for command line usage if no X available (in linux)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from config import SALT
import db
import hashlib

def hash_password(password):
    """ Returns Hashed password using sha256 and predefined SALT.
    """
    return hashlib.sha256(SALT + password).hexdigest()

def create_plots():
    """ Creates/updates plots for all exercises.
    """
    solutions = db.get_solutions()
    megabyte = 1024*1024*1.0

    all_exercises = set([solution.exercise.id for solution in solutions])

    font = {'size': 8}

    matplotlib.rc('font', **font)

    # Loop through all exercises and create plots
    for exercise_id in all_exercises:

        # Average memory usage plots
        avg_mem_usage = [solution.memory_usage/megabyte for solution in solutions
                if solution.exercise.id == exercise_id]
        xbins = min(len(avg_mem_usage), 20)
        #Histogram
        plt.figure(figsize=(4, 4))
        plt.hist(avg_mem_usage, bins=xbins, color='blue')
        plt.xlabel("Memory (MB)")
        plt.ylabel("Number of submits")
        plt.savefig("public/plot/hist_avg_mem_ex_"+str(exercise_id)+".png")
        plt.close()
        #Line plot
        plt.figure(figsize=(4, 4))
        plt.plot(avg_mem_usage, color='blue')
        plt.xlabel("Submit")
        plt.ylabel("Memory (MB)")
        plt.savefig("public/plot/plot_avg_mem_ex_"+str(exercise_id)+".png")
        plt.close()

        # Average time usage plots
        avg_time_usage = [solution.execution_time for solution in solutions
                if solution.exercise.id == exercise_id]
 
        xbins = min(len(avg_time_usage), 20)
        #Histogram      
        plt.figure(figsize=(4, 4))
        plt.hist(avg_time_usage, bins=xbins, color='blue')
        plt.xlabel("Time (s)")
        plt.ylabel("Number of submits")
        plt.savefig("public/plot/hist_avg_time_ex_"+str(exercise_id)+".png")
        plt.close()
        #Line plot      
        plt.figure(figsize=(4, 4))
        plt.plot(avg_time_usage, color='blue')
        plt.xlabel("Submits")
        plt.ylabel("Time (s)")
        plt.savefig("public/plot/plot_avg_time_ex_"+str(exercise_id)+".png")
        plt.close()
