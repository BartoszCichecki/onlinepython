# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 20:22:11 2014

@author: Bartosz
"""

#Python modules
import datetime
from peewee import SqliteDatabase, Model, DateTimeField, CharField, TextField, IntegerField, DoubleField, BooleanField, ForeignKeyField

DB = SqliteDatabase('interviews.db', threadlocals=True)

class BaseModel(Model):
    class Meta(object):
        database = DB
    created_date = DateTimeField(null=False, default=datetime.datetime.now)

class Interview(BaseModel):
    username = TextField(null=False)
    password = CharField(max_length=10, null=False)

class Exercise(BaseModel):
    description = TextField(null=False)
    time_limit = IntegerField(null=False)
    expected_output = TextField(null=False)

class InterviewExercise(BaseModel):
    interview = ForeignKeyField(Interview)
    exercise = ForeignKeyField(Exercise)

class Solution(BaseModel):
    interview = ForeignKeyField(Interview)
    exercise = ForeignKeyField(Exercise)
    submitted_code = TextField(null=False)
    correct = BooleanField(null=False)
    execution_time = DoubleField()
    memory_usage = DoubleField()
