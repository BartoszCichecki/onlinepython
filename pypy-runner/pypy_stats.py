# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 13:18:10 2014

@author: Harri
"""

"""
Python modules
"""
from peewee import *
import datetime

"""
Own created files
"""
from pypy_config import *


db = SqliteDatabase(script_dir + 'stats.db')

class Stats(Model):
#    id = IntegerField()
    submit_time = DateTimeField()
    mem_amount = DoubleField()
    time_amount = DoubleField()

    class Meta:
        database = db # This model uses the "people.db" database.

# Create database (one time)
#db.create_tables([Stats])

def addStats(mem, time):
    stat = Stats.create(submit_time=datetime.datetime.now(), mem_amount=mem, time_amount=time)
#    stat.save()
    return stat.id

