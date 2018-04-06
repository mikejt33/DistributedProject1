"""Get article counts by day.

Create a csv whose rows are dates over the date range of the wiki data
and whose columns are article titles. Values in each cell are the number
of edits of the given article on the given date in the data.

Outputs in clean csv form to article_counts_by_day.txt

Author: Joe
"""

# Create a dictionary of article titles from distinct.txt

from mrjob.job import MRJob
import numpy as np

outFile = open("article_counts_by_day.csv", "w+")
articles = {}

articlesFile = open("distinct.txt", "r+")

# Creating a dictionary of indices of articles so that counts
# always go in the same place. Also creating a header
i = 0  # i will be used later as the total number of articles.
header = "Date,"
for line in articlesFile:
    row = line.split()
    key = row[0][1:-1]
    header = header + key + ","
    articles[key] = i
    i += 1

# Cut off trailing comma, add line break and write header to file
header = header[:-1] + "\n"
outFile.write(header)
outFile.close()


class articlecounts(MRJob):

    def mapper(self, _, line):
        splt = line.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            key = splt[4]  # The date of the edit is the key
            key = key[:10]  # Cut off time stamp
            article = splt[3]
            yield(key, article)

    def reducer(self, key, vals):
        counts = np.zeros(i)  # i is the number of articles.
        out_string = key + ","
        for v in vals:
            # Get the place in the array for the count of this article (v)
            ind = articles[str(v)]
            # Increase the count for this day for this article
            counts[ind] += 1
        # Now format the output nicely
        for revisions in counts:
            out_string = out_string + str(int(revisions)) + ","
        out_string = out_string[:-1]  # Ditch last comma, add linebreak
        print(out_string)

if __name__ == '__main__':
    articlecounts.run()

"""
outFile.close()
roughFile = """