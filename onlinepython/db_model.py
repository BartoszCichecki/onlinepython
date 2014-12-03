# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 20:22:11 2014

@author: Bartosz
"""

#Python modules
import datetime
from peewee import SqliteDatabase, Model, DateTimeField, CharField, TextField
from peewee import IntegerField, DoubleField, BooleanField, ForeignKeyField

DB = SqliteDatabase('interviews.db', threadlocals=True)

class BaseModel(Model):
    """ Base class for all model classes,
    which objects are stored in database.
    """
    class Meta(object):
        """ Required by peewee framework."""
        database = DB
    created_date = DateTimeField(null=False, default=datetime.datetime.now)

class Interview(BaseModel):
    """ Represents a single interview."""
    full_name = TextField(null=False)
    username = CharField(max_length=100, null=False)
    password = CharField(max_length=65, null=False)
    started = BooleanField(default=False)
    deleted = BooleanField(default=False)

class Exercise(BaseModel):
    """ Represents a single exercise. """
    friendly_name = CharField(max_length=50, null=False)
    description = TextField(null=False)
    time_limit = IntegerField(null=False)
    expected_output = TextField(null=False)
    deleted = BooleanField(default=False)

class InterviewExercise(BaseModel):
    """ Represents many-to-many relation between
    interview and exercise. """
    interview = ForeignKeyField(Interview)
    exercise = ForeignKeyField(Exercise)
    completed = BooleanField(default=False)

class Solution(BaseModel):
    """ Represents solution to an exercise in a specific interview. """
    interview = ForeignKeyField(Interview)
    exercise = ForeignKeyField(Exercise)
    submitted_code = TextField(null=False)
    correct = BooleanField(null=False)
    execution_time = DoubleField()
    memory_usage = DoubleField()
    deleted = BooleanField(default=False)
