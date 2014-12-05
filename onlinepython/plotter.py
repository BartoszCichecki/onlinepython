# -*- coding: utf-8 -*-
"""
This module is a part fo OnlinePython project created at DTU
for the course Data Mining Using Python.

This module contains plotting functions.

Created on Thu Dec 04 22:31:35 2014

@author: Bartosz
"""

#Python modules
import matplotlib

#Required configuration
matplotlib.use('Agg')

#Python modules - continuation
import matplotlib.pyplot as plt
import os

#Own modules
import db

MEGABYTE = 1024*1024*1.0
FONT = {'size': 8}

# matplotlib setup
matplotlib.rc('font', **FONT)


def create_all_plots(force_update=False):
    """ Creates/updates plots for all exercises.
    """
    solutions = db.get_solutions()

    all_exercises = set([solution.exercise for solution in solutions])

    # Loop through all exercises and create plots
    for exercise in all_exercises:
        avg_mem_usage = get_avg_mem_usage(exercise, solutions)
        avg_time_usage = get_avg_time_usage(exercise, solutions)

        plot_avg_mem_usage(exercise, solutions, avg_mem_usage, force_update)
        plot_avg_time_usage(exercise, solutions, avg_time_usage, force_update)

        #All interviews that contained this exercise
        interviews = set([solution.interview for solution in solutions
            if solution.exercise == exercise])

        for interview in interviews:
            plot_mem_usage(exercise, interview, solutions, avg_mem_usage,
                           force_update)
            plot_time_usage(exercise, interview, solutions, avg_time_usage,
                            force_update)

def plot_avg_mem_usage(exercise, solutions=None, avg_mem_usage=None,
                       force_update=False):
    """ Plots histograph and line plot for defined exercise of memory usage.

    Keyword arguments:
    exercise -- exercise for which plots will be created
    solutions -- list of all solutions
    avg_mem_usage -- avg memory usage data
    force_update -- if plots should be updated even if they are present
    """
    if solutions is None:
        solutions = db.get_solutions()

    if avg_mem_usage is None:
        avg_mem_usage = get_avg_mem_usage(exercise, solutions)

    xbins = min(len(avg_mem_usage), 20)

    #Histogram
    file_path = "public/plot/hist_avg_mem_ex_"+str(exercise.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.hist(avg_mem_usage, bins=xbins, color='blue')
        plt.xlabel("Memory (MB)")
        plt.ylabel("Number of submits")
        plt.savefig(file_path)
        plt.close()

    #Line plot
    file_path = "public/plot/plot_avg_mem_ex_"+str(exercise.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.plot(avg_mem_usage, color='blue')
        plt.xlabel("Submit")
        plt.ylabel("Memory (MB)")
        plt.savefig("public/plot/plot_avg_mem_ex_"+str(exercise.id)+".png")
        plt.close()

def plot_mem_usage(exercise, interview, solutions=None, avg_mem_usage=None,
                   force_update=False):
    """ Plots histograph and line plot for defined exercise and interview
    of memory usage.

    Keyword arguments:
    exercise -- exercise for which plots will be created
    interview -- interview for which plots will be created
    solutions -- list of all solutions
    avg_mem_usage -- avg memory usage data
    force_update -- if plots should be updated even if they are present
    """

    if solutions is None:
        solutions = db.get_solutions()

    if avg_mem_usage is None:
        avg_mem_usage = get_avg_mem_usage(exercise, solutions)

    mem_usage = get_mem_usage(exercise, interview, solutions)

    xbins = min(max(len(mem_usage), len(avg_mem_usage)), 20)

    #Histogram
    file_path = "public/plot/hist_mem_ex_"+str(exercise.id)+"_in_"\
                +str(interview.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.hist(mem_usage, bins=xbins, color='blue')
        plt.hist(avg_mem_usage, bins=xbins, histtype='step', color='red')
        plt.xlabel("Memory (MB)")
        plt.ylabel("Number of submits")
        plt.savefig(file_path)
        plt.close()

    #Line plot
    file_path = "public/plot/plot_mem_ex_"+str(exercise.id)+"_in_"\
                +str(interview.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.plot(mem_usage, color='blue')
        plt.plot(avg_mem_usage, color='red')
        plt.xlabel("Submit")
        plt.ylabel("Memory (MB)")
        plt.savefig(file_path)
        plt.close()


def plot_avg_time_usage(exercise, solutions=None, avg_time_usage=None,
                        force_update=False):
    """ Plots histograph and line plot for defined exercise of time usage.

    Keyword arguments:
    exercise -- exercise for which plots will be created
    solutions -- list of all solutions
    avg_time_usage -- avg time usage data
    force_update -- if plots should be updated even if they are present
    """
    if solutions is None:
        solutions = db.get_solutions()

    if avg_time_usage is None:
        avg_time_usage = get_avg_time_usage(exercise, solutions)

    xbins = min(len(avg_time_usage), 20)

    #Histogram
    file_path = "public/plot/hist_avg_time_ex_"+str(exercise.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.hist(avg_time_usage, bins=xbins, color='blue')
        plt.xlabel("Time (s)")
        plt.ylabel("Number of submits")
        plt.savefig(file_path)
        plt.close()

    #Line plot
    file_path = "public/plot/plot_avg_time_ex_"+str(exercise.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.plot(avg_time_usage, color='blue')
        plt.xlabel("Submits")
        plt.ylabel("Time (s)")
        plt.savefig(file_path)
        plt.close()

def plot_time_usage(exercise, interview, solutions=None, avg_time_usage=None,
                    force_update=False):
    """ Plots histograph and line plot for defined exercise and interview
    of time usage.

    Keyword arguments:
    exercise -- exercise for which plots will be created
    interview -- interview for which plots will be created
    solutions -- list of all solutions
    avg_time_usage -- avg time usage data
    force_update -- if plots should be updated even if they are present
    """

    if solutions is None:
        solutions = db.get_solutions()

    if avg_time_usage is None:
        avg_time_usage = get_avg_time_usage(exercise, solutions)

    time_usage = get_time_usage(exercise, interview, solutions)

    xbins = min(max(len(time_usage), len(avg_time_usage)), 20)

    #Histogram
    file_path = "public/plot/hist_time_ex_"+str(exercise.id)+"_in_"\
                +str(interview.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.hist(avg_time_usage, bins=xbins, color='blue')
        plt.hist(time_usage, bins=xbins, histtype='step', color='red')
        plt.xlabel("Time (s)")
        plt.ylabel("Number of submits")
        plt.savefig(file_path)
        plt.close()

    #Line plot
    file_path = "public/plot/plot_time_ex_"+str(exercise.id)+"_in_"\
                +str(interview.id)+".png"
    if force_update or not os.path.exists(file_path):
        plt.figure(figsize=(4, 4))
        plt.plot(avg_time_usage, color='blue')
        plt.plot(time_usage, color='red')
        plt.xlabel("Submits")
        plt.ylabel("Time (s)")
        plt.savefig(file_path)
        plt.close()

def get_avg_mem_usage(exercise, solutions=None):
    """ Return averagae memory usage data for specified exercise.

    Keyword arguments:
    exercise -- exercise for which data will be computed
    solutions --- list of all solutions

    Returns:
    Memory usage data.
    """
    if solutions is None:
        solutions = db.get_solutions()
    return [solution.memory_usage/MEGABYTE for solution in solutions
                if solution.exercise == exercise]

def get_mem_usage(exercise, interview, solutions=None):
    """ Returns memory usage data for specified exercise and interview.

    Keyword arguments:
    exercise -- exercise for which data will be computed
    interview -- interview for which data will be computed
    solutions --- list of all solutions

    Returns:
    Memory usage data.
    """
    if solutions is None:
        solutions = db.get_solutions()
    return [solution.memory_usage/MEGABYTE for solution in solutions
                if solution.exercise == exercise
                and solution.interview == interview]

def get_avg_time_usage(exercise, solutions=None):
    """ Return average time usage data for specified exercise.

    Keyword arguments:
    exercise -- exercise for which data will be computed
    solutions --- list of all solutions

    Returns:
    Time usage data.
    """
    if solutions is None:
        solutions = db.get_solutions()
    return [solution.execution_time for solution in solutions
                if solution.exercise == exercise]

def get_time_usage(exercise, interview, solutions=None):
    """ Return time usage data for specified exercise.

    Keyword arguments:
    exercise -- exercise for which data will be computed
    interview -- interview for which data will be computed
    solutions --- list of all solutions

    Returns:
    Time usage data.
    """
    if solutions is None:
        solutions = db.get_solutions()
    return [solution.execution_time for solution in solutions
               if solution.exercise == exercise
               and solution.interview == interview]
