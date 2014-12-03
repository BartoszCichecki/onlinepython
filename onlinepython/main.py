# -*- coding: utf-8 -*-
"""
This module is a part fo OnlinePython project created at DTU
for the course Data Mining Using Python.

This is the main module that initializes and starts up the whole program.

Created on Sun Oct  5 19:09:58 2014

@author: Bartosz
"""

#Own created modules
import db
import web

if __name__ == '__main__':
    db.initialize()
    web.initialize()
