# -*- coding: utf-8 -*-
"""
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
        mem_usage = [solution.memory_usage/megabyte for solution in solutions
                if solution.exercise.id == exercise_id]
        time_usage = [solution.execution_time for solution in solutions
                if solution.exercise.id == exercise_id]
        # Memory usage plots
        xbins = min(len(mem_usage), 20)
        plt.figure(figsize=(3, 3))
        plt.hist(mem_usage, bins=xbins, color='blue')
        plt.savefig("public/plot/plot_mem_"+str(exercise_id)+".png")
        plt.close()
        # Time usage plots
        xbins = min(len(time_usage), 20)
        plt.figure(figsize=(3, 3))
        plt.hist(time_usage, bins=xbins, color='blue')
        plt.savefig("public/plot/plot_time_"+str(exercise_id)+".png")
        plt.close()
