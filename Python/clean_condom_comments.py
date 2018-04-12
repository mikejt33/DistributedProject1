#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 19:48:17 2018

@author: Mike
"""
#  0 - outlier  1 - random
import pandas as pd

inFile = open("Outputs/actually_cleaned_random_data_of_interest.csv","r+",encoding="utf-8")
outFile = open("clean_condoms_comments.csv","w+")


output = []
    
for line in inFile:
    splt = line.split("Ϭ")
    for first in splt:
        if first == "Condom":
            output.append(splt)

df = pd.DataFrame(output)

df.to_csv("clean_condoms_comments.csv",index = False, header = False)

