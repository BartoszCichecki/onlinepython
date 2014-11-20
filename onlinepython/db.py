# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 19:11:58 2014

@author: Bartosz
"""

#Python modules
from peewee import IntegrityError
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#Own created modules
from db_model import DB, Interview, Exercise, InterviewExercise, Solution

def initialize():
    DB.connect()
    DB.create_tables([Interview, Exercise, InterviewExercise, Solution], safe=True)

def check_interview_credentials(username, password):
    return Interview.select().where((Interview.username == username) & (Interview.password == password) & (Interview.deleted == False)).count() > 0

def add_solution(solution):
    solution.save()
    solutions = get_solutions()
    mb = 1024*1024*1.0
    
    all_exercises = set([solution.exercise.id for solution in solutions])
    
    for exercise_id in all_exercises:
        x = [solution.memory_usage/mb for solution in solutions if solution.exercise.id == exercise_id]
        xbins=min(len(x), 20)
        plt.hist(x, bins=xbins, color='blue')
        plt.savefig("public/plot/plot_"+str(exercise_id)+".png")
        plt.close()

def get_solutions(exercise_id=None, solution_id=None):
    if solution_id != None:
        solutions = Solution.select().where((Solution.id == solution_id) & (Solution.deleted == False))
    elif exercise_id != None:
        solutions = Solution.select().where(Solution.exercise == exercise_id)
        solutions = [solution for solution in solutions if solution.deleted == False]
    else:
        solutions = Solution.select()
        solutions = [solution for solution in solutions if solution.deleted == False]
    return solutions

def get_exercises(exercise_id=None):
    if exercise_id == None:
        return Exercise.select().where(Exercise.deleted == False)
    else:
        exercise = Exercise.get((Exercise.id == exercise_id) & (Exercise.deleted == False))
        return exercise

def create_exercise(friendly_name="", description="", expected_output="", time_limit=0):
    try:
        with DB.transaction():
            Exercise.create(friendly_name=friendly_name, description=description, expected_output=expected_output, time_limit=time_limit)
        return True
    except IntegrityError:
        return False

def edit_exercise(exercise_id=None, friendly_name="", description="", expected_output="", time_limit=0):
    if exercise_id == None:
        return False

    try:
        with DB.transaction():
            query = Exercise.update(friendly_name=friendly_name, description=description, expected_output=expected_output, time_limit=time_limit).where(Exercise.id == exercise_id)
            query.execute()
            return True
    except IntegrityError:
        return False

def delete_exercise(exercise_id):
    if exercise_id == None:
        return False

    try:
        with DB.transaction():
            query = Exercise.update(deleted=True).where(Exercise.id == exercise_id)
            query.execute()
            return True
    except IntegrityError:
        return False

def get_interview_exercise_ids(interview_id):
    matches = Exercise.select().join(InterviewExercise).join(Interview).where((Exercise.deleted == False) & (Interview.id == interview_id) & (Interview.deleted == False))
    return [match.id for match in matches]

def get_interview_id(username):
    interview = Interview.select().where((Interview.username == username) & (Interview.deleted == False)).limit(1).get()
    return interview.id

def get_interviews(interview_id=None):
    if interview_id == None:
        return Interview.select().where(Interview.deleted == False)
    else:
        return Interview.get((Interview.id == interview_id) & (Interview.deleted == False))

def create_interview(full_name="", username="", password="", exerciseIds=[]):
    try:
        with DB.transaction():
            interview = Interview.create(full_name=full_name, username=username, password=password)

            for exerciseId in exerciseIds:
                exercise = Exercise.select().where((Exercise.id == exerciseId) & (Exercise.deleted == False)).limit(1).get()
                InterviewExercise.create(interview=interview, exercise=exercise)
        return True
    except IntegrityError:
        return False

def edit_interview(interview_id=None, full_name="", username="", password="", exerciseIds=[]):
    if interview_id == None:
        return False

    try:
        with DB.transaction():
            query = Interview.update(full_name=full_name, username=username, password=password).where(Interview == interview_id)
            query.execute()

            interview = Interview.select().where((Interview.id == interview_id) & (Interview.deleted == False)).limit(1).get()
            query = InterviewExercise.delete().where(InterviewExercise.interview == interview)
            query.execute()

            for exerciseId in exerciseIds:
                exercise = Exercise.get(Exercise.id == exerciseId)
                if exercise.deleted == True:
                    continue
                InterviewExercise.create(interview=interview, exercise=exercise)
        return True
    except IntegrityError:
        return False

def delete_interview(interview_id):
    if interview_id == None:
        return False

    try:
        with DB.transaction():
            query = Interview.update(deleted=True).where(Interview.id == interview_id)
            query.execute()
            return True
    except IntegrityError:
        return False
