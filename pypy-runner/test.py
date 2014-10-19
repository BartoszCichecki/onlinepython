# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 17:00:37 2014

@author: Harri
"""

#import sys

all = []

for i in range(1, 10000):
    prime = True
    for j in range(2, i):
        if i % j == 0:
            #print(str(i)+"\n")
            #all.append(i)
            prime = False
            break
    if prime == True:
        print(str(i)+"\n")
        all.append(i)