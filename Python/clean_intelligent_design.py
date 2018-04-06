#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 17:35:04 2018

@author: Mike
"""

inFile = open("actually_cleaned_random_data_of_interest.csv")
outFile = open("Intelligent_Design_articles.csv")

for line in inFile:
    output = ""
    splt = line.split("Ϭ")
    
    if splt[0] == "Intelligent_design":
        output = splt
        
outFile.write(output)