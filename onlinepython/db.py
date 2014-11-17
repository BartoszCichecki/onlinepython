# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 19:11:58 2014

@author: Bartosz
"""

#Python modules
from peewee import IntegrityError

#Own created modules
from db_model import DB, Interview, Exercise, InterviewExercise, Solution

def initialize():
    DB.connect()
    DB.create_tables([Interview, Exercise, InterviewExercise, Solution], safe=True)

def check_interview_credentials(username, password):
    return Interview.select().where(Interview.username == username and Interview.password == password and Interview.deleted == False).count() > 0

def get_interview_id(username):
    interview = Interview.get(Interview.username == username and Interview.deleted == False)
    return interview.id

def add_solution(solution):
    solution.save()

def get_exercises(exercise_id=None):
    if exercise_id == None:
        return Exercise.select().where(Exercise.deleted == False)
    else:
        exercise = Exercise.get(Exercise.id == exercise_id)
        if exercise.deleted == True:
            return False
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

def get_interviews(interview_id=None):
    if interview_id == None:
        return Interview.select().where(Interview.deleted == False)
    else:
        return Interview.get(Interview.id == interview_id and Interview.deleted == False)

def get_interview_exercise_ids(interview_id):
        matches = Exercise.select().join(InterviewExercise).join(Interview).where(Exercise.deleted == False and Interview.id == interview_id and Interview.deleted == False)
        return [match.id for match in matches]

def create_interview(full_name="", username="", password="", exerciseIds=[]):
    try:
        with DB.transaction():
            interview = Interview.create(full_name=full_name, username=username, password=password)

            for exerciseId in exerciseIds:
                exercise = Exercise.select().where(Exercise.id == exerciseId and Exercise.deleted == False).limit(1).get()
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

            interview = Interview.select().where(Interview.id == interview_id and Interview.deleted == False).limit(1).get()
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
