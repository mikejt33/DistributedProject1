# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 2018

#runfile('C:/Users/Lilianne/mrjobtest2.py',args='example_sanderson.txt')
#runfile('C:/Users/Lilianne/mrjob_RandomArticle.py',args='C:/Users/Lilianne/colleges1.csv')

@author: Lilianne Raud
"""

# MapReduce program that picks random list of N Names.

from mrjob.job import MRJob
import random

class RandomName(MRJob):

    def mapper(self, _, line):
      name = line.split(",")
      name = name[0]
      yield ("",name)
       
      print(name)

    def reducer(self, _, name):
        N = 67
        yield ("",random.sample(set(name), N))
        

if __name__ == '__main__':
    RandomName.run()


#mrjob_RandomArticle.py