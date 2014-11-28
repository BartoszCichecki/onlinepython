# -*- coding: utf-8 -*-
"""
Created on Sun Nov  16 20:22:11 2014

@author: Bartosz
"""

def exists(selectquery):
    """ Jinja2 filter for checking if SelectQuery is empty.

    Keyword arguments:
    selectquery - query to check
    """
    return selectquery.exists()
