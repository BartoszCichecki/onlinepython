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
    """Creates database model.
    """
    DB.connect()
    DB.create_tables([Interview, Exercise, InterviewExercise, Solution],
                     safe=True)

def check_interview_credentials(username, password):
<<<<<<< HEAD
    """Checks user credentials.

    Keyword arguments:
    username -- Username
    password -- Password

    Return values:
    True if found in database, False otherwise
    """
    return Interview.select().where((Interview.username == username) &
                                    (Interview.password == password) &
                                    (Interview.deleted == False)).count() > 0
=======
    return Interview.select().where((Interview.username == username) & (Interview.password == password) & (Interview.deleted == False)).count() > 0
>>>>>>> origin/master

def add_solution(solution):
    """Save solution to database.

    Keyword arguments:
    solution -- Solution object
    """
    solution.save()
    solutions = get_solutions()
    megabyte = 1024*1024*1.0

    all_exercises = set([solution.exercise.id for solution in solutions])

    for exercise_id in all_exercises:
<<<<<<< HEAD
        mem_usage = [solution.memory_usage/megabyte for solution in solutions
                if solution.exercise.id == exercise_id]
        xbins = min(len(mem_usage), 20)
        plt.hist(mem_usage, bins=xbins, color='blue')
=======
        x = [solution.memory_usage/mb for solution in solutions if solution.exercise.id == exercise_id]
        xbins=min(len(x), 20)
        plt.hist(x, bins=xbins, color='blue')
>>>>>>> origin/master
        plt.savefig("public/plot/plot_"+str(exercise_id)+".png")
        plt.close()

def get_solutions(exercise_id=None, solution_id=None):
    """Gets solutions.

    Keyword arguments:
    exercise_id -- Exercise ID
    solution_id -- Solution ID

    Return values:
    Pointer of solution results
    """
    if solution_id != None:
<<<<<<< HEAD
        solutions = Solution.select().where((Solution.id == solution_id) &
            (Solution.deleted == False))
=======
        solutions = Solution.select().where((Solution.id == solution_id) & (Solution.deleted == False))
>>>>>>> origin/master
    elif exercise_id != None:
        solutions = Solution.select().where(Solution.exercise == exercise_id)
        solutions = [solution for solution in solutions
            if solution.deleted == False]
    else:
        solutions = Solution.select()
        solutions = [solution for solution in solutions
            if solution.deleted == False]
    return solutions

def get_exercises(exercise_id=None):
    """Gets exercises.

    Keyword arguments:
    exercise_id -- Exercise ID

    Return values:
    Pointer of exercise results
    """
    if exercise_id == None:
        return Exercise.select().where(Exercise.deleted == False)
    else:
<<<<<<< HEAD
        exercise = Exercise.get((Exercise.id == exercise_id) &
            (Exercise.deleted == False))
=======
        exercise = Exercise.get((Exercise.id == exercise_id) & (Exercise.deleted == False))
>>>>>>> origin/master
        return exercise

def create_exercise(friendly_name="", description="", expected_output="",
                    time_limit=0):
    """Creates exercise.

    Keyword arguments:
    friendly_name -- Name of exercise
    description -- Description of exercise
    expected_output -- Sample output
    time_limit -- Maximum amount of time to use

    Return values:
    True if successful, False otherwise
    """
    try:
        with DB.transaction():
            Exercise.create(friendly_name=friendly_name,
                            description=description,
                            expected_output=expected_output,
                            time_limit=time_limit)
        return True
    except IntegrityError:
        return False

def edit_exercise(exercise_id=None, friendly_name="", description="",
                  expected_output="", time_limit=0):
    """Edits exercise.

    Keyword arguments:
    exercise_id -- Exercise ID
    friendly_name -- Name of exercise
    description -- Description of exercise
    expected_output -- Sample output
    time_limit -- Maximum amount of time to use

    Return values:
    True if successful, False otherwise
    """
    if exercise_id == None:
        return False

    try:
        with DB.transaction():
            query = Exercise.update(friendly_name=friendly_name,
                                    description=description,
                                    expected_output=expected_output,
                                    time_limit=time_limit).where(
                                        Exercise.id == exercise_id)
            query.execute()
            return True
    except IntegrityError:
        return False

def delete_exercise(exercise_id):
    """Deletes exercise.

    Keyword arguments:
    exercise_id -- Exercise ID

    Return values:
    True if successful, False otherwise
    """
    if exercise_id == None:
        return False

    try:
        with DB.transaction():
            query = Exercise.update(deleted=True).where(
                Exercise.id == exercise_id)
            query.execute()
            return True
    except IntegrityError:
        return False

def get_interview_exercise_ids(interview_id):
<<<<<<< HEAD
    """Gets interviewee's exercises.

    Keyword arguments:
    interview_id -- Interview ID

    Return values:
    List of interviewee's exercises
    """
    matches = Exercise.select().join(InterviewExercise).join(Interview).where(
        (Exercise.deleted == False) &
        (Interview.id == interview_id) &
        (Interview.deleted == False))
    return [match.id for match in matches]

def get_interview_id(username):
    """Gets interviewee's ID.

    Keyword arguments:
    username -- Username

    Return values:
    Interviewee's ID
    """
    interview = Interview.select().where((Interview.username == username) &
                                (Interview.deleted == False)).limit(1).get()
=======
    matches = Exercise.select().join(InterviewExercise).join(Interview).where((Exercise.deleted == False) & (Interview.id == interview_id) & (Interview.deleted == False))
    return [match.id for match in matches]

def get_interview_id(username):
    interview = Interview.select().where((Interview.username == username) & (Interview.deleted == False)).limit(1).get()
>>>>>>> origin/master
    return interview.id

def get_interviews(interview_id=None):
    """Gets Interviews.

    Keyword arguments:
    interview_id -- Interviewee's ID

    Return values:
    Pointer for results
    """
    if interview_id == None:
        return Interview.select().where(Interview.deleted == False)
    else:
<<<<<<< HEAD
        return Interview.get((Interview.id == interview_id) &
                            (Interview.deleted == False))
=======
        return Interview.get((Interview.id == interview_id) & (Interview.deleted == False))
>>>>>>> origin/master

def create_interview(full_name="", username="", password="", exercise_ids=[]):
    """Creates interview.

    Keyword arguments:
    full_name -- Interviewee's name
    username -- Interviewee's username
    password -- Interviewee's password
    exerciseIds -- Exercises open for Interviewee

    Return values:
    True if successful, False otherwise
    """
    try:
        with DB.transaction():
            interview = Interview.create(full_name=full_name,
                                         username=username, password=password)

<<<<<<< HEAD
            for exercise_id in exercise_ids:
                exercise = Exercise.select().where(
                    (Exercise.id == exercise_id) &
                    (Exercise.deleted == False)).limit(1).get()
=======
            for exerciseId in exerciseIds:
                exercise = Exercise.select().where((Exercise.id == exerciseId) & (Exercise.deleted == False)).limit(1).get()
>>>>>>> origin/master
                InterviewExercise.create(interview=interview, exercise=exercise)
        return True
    except IntegrityError:
        return False

def edit_interview(interview_id=None, full_name="", username="", password="",
                   exercise_ids=[]):
    """Edits interview.

    Keyword arguments:
    interview_id -- Interviewee's ID
    full_name -- Interviewee's name
    username -- Interviewee's username
    password -- Interviewee's password
    exerciseIds -- Exercises open for Interviewee

    Return values:
    True if successful, False otherwise
    """
    if interview_id == None:
        return False

    try:
        with DB.transaction():
            query = Interview.update(full_name=full_name, username=username,
                                     password=password).where(
                                         Interview == interview_id)
            query.execute()

<<<<<<< HEAD
            interview = Interview.select().where(
                (Interview.id == interview_id) &
                (Interview.deleted == False)).limit(1).get()
            query = InterviewExercise.delete().where(
                    InterviewExercise.interview == interview)
=======
            interview = Interview.select().where((Interview.id == interview_id) & (Interview.deleted == False)).limit(1).get()
            query = InterviewExercise.delete().where(InterviewExercise.interview == interview)
>>>>>>> origin/master
            query.execute()

            for exercise_id in exercise_ids:
                exercise = Exercise.get(Exercise.id == exercise_id)
                if exercise.deleted == True:
                    continue
                InterviewExercise.create(interview=interview, exercise=exercise)
        return True
    except IntegrityError:
        return False

def delete_interview(interview_id):
    """Deletes interview.

    Keyword arguments:
    interview_id -- Interviewee's ID

    Return values:
    True if successful, False otherwise
    """
    if interview_id == None:
        return False

    try:
        with DB.transaction():
            query = Interview.update(deleted=True).where(
                Interview.id == interview_id)
            query.execute()
            return True
    except IntegrityError:
        return False
