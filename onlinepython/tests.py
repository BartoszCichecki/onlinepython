# -*- coding: utf-8 -*-
"""
This module is a part fo OnlinePython project created at DTU
for the course Data Mining Using Python.

This module contains tests for the system.

Created on Sat Nov 29 21:08:36 2014

@author: Harri
"""

#Python modules
import os
import string
import random
import unittest

#Own modules
import db
import pypy_runner as pyrun

def generate_string(length=5):
    """ Generates random string of length (default: 5). """
    # http://stackoverflow.com/questions/2257441/
    # random-string-generation-with-upper-case-letters-and-digits-in-python
    return ''.join(random.choice(string.ascii_lowercase + string.digits)
                    for _ in range(length))

class TestSequenceFunctions(unittest.TestCase):
    """ Class implementing all the test cases. """

    def setUp(self):
        """ Sets up the test before each method. """
        self.seq = range(10)

    def test_credentials_wrong(self):
        """ Tests credential checking with wrong credentials. """
        # Generate some random credentials
        username = generate_string()
        password = generate_string()
        self.assertEqual(False, db.check_interview_credentials(username,
                                                               password))

    def test_credentials_corr(self):
        """ Tests credential checking with correct credentials. """
        username = generate_string()
        password = generate_string()
        db.create_interview("Test name", username, password)
        self.assertEqual(True, db.check_interview_credentials(username,
                                                              password))
    def test_output_wrong(self):
        """ Tests if wrong output is catched correctly from pypy_runner. """
        sfilename = "testscript.py"
        output = generate_string(20)
        script = 'print("'+output+'")'
        sfile = open(sfilename, "w")
        sfile.write(script)
        sfile.close()
        result = pyrun.check_output(sfilename, output+"wrong")
        os.remove(sfilename)
        self.assertEqual(False, result['correct'])

    def test_output_corr(self):
        """ Tests if correct output is catched correctly from pypy_runner. """
        sfilename = "testscript.py"
        output = generate_string(20)
        script = 'print("'+output+'")'
        sfile = open(sfilename, "w")
        sfile.write(script)
        sfile.close()
        result = pyrun.check_output(sfilename, output)
        os.remove(sfilename)
        self.assertEqual(True, result['correct'])

    def test_sample(self):
        """ Sample test. """
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
