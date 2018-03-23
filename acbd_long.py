"""Get article counts by day.

Creates a three column file with date, articletitle, count. For cleaned up
version of data.

Author: Joe
"""

from mrjob.job import MRJob


class articlecounts(MRJob):

    def mapper(self, _, line):
        row = line.split("\x1f")
        splt = row.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            if splt[4][:3] == "200":
                key = splt[4]  # The date of the edit is the key
                key = key[:10]  # Cut off time stamp
                article = "\"" + splt[3] + "\""
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

if __name__ == '__main__':
    articlecounts.run()