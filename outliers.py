"""Get article counts by day.

Grab dates/article pairs with edit counts in the 95th percentile.

Author: Joe
Date: 03/22/2018
"""


from mrjob.job import MRJob
import csv

t_crit = {}  # Dictionary to store 95% confint critical values.

iFile = open("means_vars.csv", "r+")

# Append each title to the dictionary along with its 95% critical value.
for line in iFile:
    row = csv.reader(line.splitlines(), quotechar='"', delimiter=',')
    splt = next(row)
    if len(splt) > 0:
        title = "\"" + splt[0] + "\""
        mean = splt[1]
        var = splt[2]
        t_crit[title] = mean + 1.96 * var


class outliers(MRJob):

    def mapper(self, _, line):
        row = csv.reader(line.splitlines(), quotechar='"', delimiter=',')
        splt = next(row)
        if len(splt) > 0:
            edit_date = splt[0]
            count = int(splt[2])
            # csv.reader strips quotes from title, so put them back.
            title = "\"" + splt[1] + "\""
            yield("key", (edit_date, title, count))

    """def combiner(self, key, vals):
        for v in vals:
            cutoff = t_crit[v[1]]
            if v[2] >= cutoff:
                output = v[0] + "," + v[1] + "," + v[2]
                print(output)"""

    def reducer(self, key, vals):
        for v in vals:
            cutoff = t_crit[v[1]]
            if v[2] >= cutoff:
                output = v[0] + "," + v[1] + "," + v[2]
                print(output)

if __name__ == '__main__':
    outliers.run()