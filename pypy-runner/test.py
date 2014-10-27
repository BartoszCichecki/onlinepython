# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 17:00:37 2014

@author: Harri
"""

#Python modules
from __future__ import print_function
import sys

#Own created files

def run_test(max_primes=10000):
    """Prints prime numbers until max_primes

    Keyword arguments:
    max_primes -- Limit maximum number
    """
    primes = []

    for i in range(1, max_primes):
        prime = True
        for j in range(2, i):
            if i % j == 0:
                #print(str(i)+"\n")
                #primes.append(i)
                prime = False
                break
        if prime == True:
            print(str(i)+"\n")
            primes.append(i)

def main():
    """Run program
    """
    run_test(10000)

if __name__ == "__main__":
    main()
