"""Get article counts by day.

Creates a three column file with date, articletitle, count

Author: Joe
"""

# Create a dictionary of article titles from distinct.txt

from mrjob.job import MRJob
from copy import deepcopy

# outFile = open("article_counts_by_day.csv", "w+")
articles = {}

# articlesFile = open("distinct.txt", "r+")

"""for line in articlesFile:
    row = line.split()
    key = row[0][1:-1]
    articles[key] = 0"""

class articlecounts(MRJob):

    def mapper(self, _, line):
        splt = line.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            key = splt[4]  # The date of the edit is the key
            key = key[:10]  # Cut off time stamp
            article = splt[3]
            yield(key, article)

    def reducer(self, key, vals):
        counts = {}
        for v in vals:
            try:
                counts[str(v)] += 1
            except:
                counts[str(v)] = 1
        for entry in counts:
            if counts[entry] > 0:
                out_string = str(key) + "," + str(entry) + "," + str(counts[entry])
                print(out_string)
        # outFile.write(output_string)

if __name__ == '__main__':
    articlecounts.run()