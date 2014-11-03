# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 19:11:58 2014

@author: Bartosz
"""

#Own created modules
from db_model import DB, Interview, Exercise, InterviewExercise, Solution

def initialize():
    DB.connect()
    DB.create_tables([Interview, Exercise, InterviewExercise, Solution], safe=True)

def check_interview_credentials(username, password):
    return Interview.select().where(Interview.username == username and Interview.password == password).count() > 0

def add_solution(solution):
    solution.save()
    