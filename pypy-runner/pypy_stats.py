# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 13:18:10 2014

@author: Harri
"""

"""
Python modules
"""
from peewee import SqliteDatabase, DateTimeField, DoubleField, BooleanField
from peewee import Model
import datetime

"""
Own created files
"""
from pypy_config import SCRIPT_DIR


DB = SqliteDatabase(SCRIPT_DIR + 'stats.db')

class Stats(Model):
#    id = IntegerField()
    submit_time = DateTimeField()
    mem_amount = DoubleField()
    time_amount = DoubleField()
    correct_output = BooleanField()

    class Meta:
        database = DB # This model uses the "people.db" database.

# Create database (one time)
#db.create_tables([Stats])

def add_stats(mem, time, correct):
    """Adds a row to database.

    Keyword arguments:
    mem -- Maximum amount of memory used
    time -- Time used to run the script
    correct -- Script ran successfully
    
    Returns:
    id of the inserted row
    """
    stat = Stats.create(submit_time=datetime.datetime.now(), mem_amount=mem,
                        time_amount=time, correct_output=correct)
#    stat.save()
    return stat.id

