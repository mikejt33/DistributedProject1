#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 17:35:04 2018

@author: Mike
"""
import csv

inFile = open("actually_cleaned_random_data_of_interest.csv","r+",encoding="utf-8")
outFile = open("Intelligent_Design_articles.csv","w+")


output = []
    
for line in inFile:
    splt = line.split("Ϭ")
    for first in splt:
        if first == "Intelligent_design":
            output.append(splt)

        
with open("Intelligent_Design_articles.csv","w") as f:
    writer = csv.writer(f)
    writer.writerows(output)
