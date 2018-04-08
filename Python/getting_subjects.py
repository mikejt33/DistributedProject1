#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:14:21 2018

@author: Mike

Getting Category columns for visualization
"""
    data.append(d)
    
import re

inFile = open("Intelligent_Design_articles.csv","r")

output =[]
data = []

for line in inFile:
    output.append(line)

for o in output:
    start = "/*"
    end = "*/"
    result = re.search('%s(.*)%s' % (start, end), o).group(1)
    print (result)
