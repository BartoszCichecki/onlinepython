# -*- coding: utf-8 -*-
"""
This module is a part fo OnlinePython project created at DTU
for the course Data Mining Using Python.

The module contains helper methods that did not belong in any other module.

Created on Wed Dec 03 11:38:45 2014

@author: Harri
"""

#Pytohn modules
import hashlib

#Own modules
from config import SALT

def hash_password(password):
    """ Returns Hashed password using sha256 and predefined SALT.
    """
    return hashlib.sha256(SALT + password).hexdigest()
