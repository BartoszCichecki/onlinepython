# -*- coding: utf-8 -*-
"""
This module is a part fo OnlinePython project created at DTU
for the course Data Mining Using Python.

This module contains functions that are useful for accessing the database and
performing operations on data.

Created on Sun Oct  5 19:11:58 2014

@author: Bartosz
"""

#Python modules
from peewee import IntegrityError

#Own created modules
from db_model import DB, Interview, Exercise, InterviewExercise, Solution
import misc
from misc import hash_password

def initialize():
    """Creates database model.
    """
    DB.connect()
    DB.create_tables([Interview, Exercise, InterviewExercise, Solution],
                     safe=True)

def check_interview_credentials(username, password):
    """Checks user credentials.

    Keyword arguments:
    username -- Username
    password -- Password

    Return values:
    True if found in database, False otherwise
    """
    return Interview.select().where((Interview.username == username) &
            (Interview.password == hash_password(password)) &
            (Interview.deleted == False) &
            (Interview.locked == False)).count() > 0

def add_solution(solution):
    """Save solution to database.

    Keyword arguments:
    solution -- Solution object
    """
    solution.save()
    misc.create_plots()

def get_solutions(exercise_id=None, interview_id=None, solution_id=None):
    """Gets solutions.

    Keyword arguments:
    exercise_id -- Exercise ID
    interview_id -- Interview ID
    solution_id -- Solution ID

    Return values:
    Pointer of solution results
    """
    if solution_id != None:
        solutions = Solution.select().where((Solution.id == solution_id) &
            (Solution.deleted == False))
    elif interview_id != None:
        solutions = Solution.select().where(Solution.interview == interview_id)
        solutions = [solution for solution in solutions
            if solution.deleted == False]
    elif exercise_id != None:
        solutions = Solution.select().where(Solution.exercise == exercise_id)
        solutions = [solution for solution in solutions
            if solution.deleted == False]
    else:
        solutions = Solution.select()
        solutions = [solution for solution in solutions
            if solution.deleted == False]
    return solutions

def has_correct_solution(exercise_id=None, interview_id=None):
    """Checks if user has correct solution for exercise.

    Keyword arguments:
    exercise_id -- Exercise ID
    interview_id -- Interviewee ID

    Return values:
    Boolean
    """

    if exercise_id == None or interview_id == None:
        return False
    else:
        return Exercise.select().join(Solution).join(Interview).where(
            (Exercise.deleted == False) &
            (Exercise.id == exercise_id) &
            (Interview.id == interview_id) &
            (Solution.correct == True)
            ).count() > 0

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
        exercise = Exercise.get((Exercise.id == exercise_id) &
            (Exercise.deleted == False))
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
        return Interview.get((Interview.id == interview_id) &
                            (Interview.deleted == False))

def create_interview(full_name="", username="", password="", locked=False,
                     exercise_ids=None):
    """Creates interview.

    Keyword arguments:
    full_name -- Interviewee's name
    username -- Interviewee's username
    password -- Interviewee's password
    locked -- if interview is locked
    exerciseIds -- Exercises open for Interviewee

    Return values:
    True if successful, False otherwise
    """

    if password == "":
        return False

    if exercise_ids is None:
        exercise_ids = []

    try:
        with DB.transaction():
            interview = Interview.create(full_name=full_name,
                         username=username, password=hash_password(password),
                         locked=locked)

            for exercise_id in exercise_ids:
                exercise = Exercise.select().where(
                    (Exercise.id == exercise_id) &
                    (Exercise.deleted == False)).limit(1).get()
                InterviewExercise.create(interview=interview, exercise=exercise)
        return True
    except IntegrityError:
        return False

def edit_interview(interview_id=None, full_name="", username="", password="",
                   locked=False, exercise_ids=None):
    """Edits interview.

    Keyword arguments:
    interview_id -- Interviewee's ID
    full_name -- Interviewee's name
    username -- Interviewee's username
    password -- Interviewee's password
    locked -- if interview is locked
    exerciseIds -- Exercises open for Interviewee

    Return values:
    True if successful, False otherwise
    """
    if interview_id == None:
        return False

    if exercise_ids is None:
        exercise_ids = []

    try:
        with DB.transaction():
            if password == "":
                query = Interview.update(full_name=full_name,
                                         username=username, locked=locked
                                         ).where(Interview.id == interview_id)
            else:
                query = Interview.update(full_name=full_name, username=username,
                                     password=hash_password(password),
                                     locked=locked).where(
                                     Interview.id == interview_id)
            query.execute()

            interview = Interview.select().where(
                (Interview.id == interview_id) &
                (Interview.deleted == False)).limit(1).get()
            query = InterviewExercise.delete().where(
                    InterviewExercise.interview == interview)
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
