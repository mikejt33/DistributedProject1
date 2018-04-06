"""Get article counts by day.

Grab date,article_title,# edits but only for titles in the list of article
titles included in "sample.csv"

Author: Joe
"""

from mrjob.job import MRJob

iFile = open("sample.csv", "r+")
sample = set([])
for line in iFile:
    sample.add(line)


class articlecounts(MRJob):

    def mapper(self, _, line):
        splt = line.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            try:
                if splt[4][:3] == "200":
                    key = splt[4]  # The date of the edit is the key
                    key = key[:10]  # Cut off time stamp
                    if splt[3] in sample:
                        article = "\"" + splt[3] + "\""
                        yield(key, article)
            except:
                pass

    def reducer(self, key, vals):
        try:
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
        except:
            pass

if __name__ == '__main__':
    articlecounts.run()