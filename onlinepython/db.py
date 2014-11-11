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

def create_exercise(desc="", limit=0, output=""):
    Exercise.create(description=desc, time_limit=limit, expected_output=output)
    
def edit_exercise(ex_id=None, desc="", limit=0, output=""):
    if ex_id == None:
        return False
    query = Exercise.update(description=desc, time_limit=limit, expected_output=output).where(Exercise.id == ex_id)
    query.execute()

def get_exercises(ex_id=None):
    if ex_id == None:
        return Exercise.select()
    else:
        return Exercise.get(Exercise.id == ex_id)
        
def get_user_exercises(user_id=None):
    return Exercise.select().join(InterviewExercise).where(InterviewExercise.id == user_id)

def create_user(username, password):
    Interview.create(username=username, password=password)

def get_users(user_id=None):
    if user_id == None:
        return Interview.select()
    else:
        return Interview.get(Interview.id == user_id)

def add_user_exercise(user_id, ex_id, add):
    InterviewExercise.create(interview=user_id, exercise=ex_id)
