#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:28:15 2018

@author: Mike
"""

from mrjob.job import MRJob

inputFile = open("output.txt","r+")

class min_timestamp(MRJob):
    
    def mapper(self, _, line):
        splt = line.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            time = splt[4]
            val = time[:10]           
            yield("date", val)
            
    def reducer (self, key, vals):
        v = list(vals)
        yield("min_date",min(v))
        yield("max_date", max(v))

if __name__ == '__main__':
    min_timestamp.run()
    
