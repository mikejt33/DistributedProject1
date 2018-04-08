#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 15:33:40 2018

@author: Mike
"""

#  0 - outlier  1 - random
import csv
import pandas as pd

inFile = open("actually_cleaned_random_data_of_interest.csv","r+",encoding="utf-8")
outFile = open("Down_syndrome_articles.csv","w+")


output = []
    
for line in inFile:
    splt = line.split("Ϭ")
    for first in splt:
        if first == "Down_syndrome":
            output.append(splt)

df = pd.DataFrame(output)

df.to_csv('Down_syndrome_articles.csv',index = False, header = False)

