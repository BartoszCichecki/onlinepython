# -*- coding: utf-8 -*-
"""
This module is a part fo OnlinePython project created at DTU
for the course Data Mining Using Python.

This module contains custom jinja2 filters.

Created on Sun Nov  16 20:22:11 2014

@author: Bartosz
"""

def exists(selectquery):
    """ Jinja2 filter for checking if SelectQuery is empty.

    Keyword arguments:
    selectquery - query to check
    """
    return selectquery.exists()
