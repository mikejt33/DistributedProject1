"""Get article counts by day.

Print rows that were breaking acbdl_redo

Author: Joe
"""

from mrjob.job import MRJob

outlistFile = open("outlist.csv", "r+")
randomlistFile = open("randomlist.csv", "r+")

outlist = []
randomlist = []

for line in outlistFile:
    splt = line.split(",")
    outlist.append((splt[0], splt[1]))

for line in outlistFile:
    splt = line.split(",")
    randomlist.append((splt[0], splt[1]))

class dataget(MRJob):

    def mapper(self, _, line):
        splt = line.split("\x1f")
        row1 = splt[0].split()
        thedate = row1[4][:10]
        title = row1[3]
        if (thedate, title) in outlist:
            print(line + ", 0")
        elif (thedate, title) in randomlist:
            print(line + ", 1")

if __name__ == '__main__':
    dataget.run()