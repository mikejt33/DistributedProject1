"""Get article counts by day.

Get the mean and variance of number of edits per day for each article.

Author: Joe
Date: 03/22/2018
"""


from mrjob.job import MRJob
from datetime import date
import csv

last_date = date(2008, 1, 3)


class meansvars(MRJob):

    def mapper(self, _, line):
        row = csv.reader(line.splitlines(), quotechar='"', delimiter=',')
        splt = next(row)
        if len(splt) > 0:
            edit_date = splt[0]
            count = int(splt[2])
            count_sq = count ** 2
            title = "\""+splt[1]+"\""
            yield(title, (edit_date, count, count_sq))

    def combiner(self, key, vals):
        total = 0
        total_sq = 0
        first_date = date(2018, 3, 22)
        for v in vals:
            edit_date = v[0]
            count = v[1]
            count_sq = v[2]
            this_date = date(int(edit_date[:4]),
                             int(edit_date[5:7]),
                             int(edit_date[8:10])
                             )
            if this_date < first_date:
                first_date = this_date
            total += count
            total_sq += count_sq
        yield(key, (str(first_date), count, count_sq))

    def reducer(self, key, vals):
        total = 0
        total_sq = 0
        first_date = date(2018, 3, 22)
        for v in vals:
            edit_date = v[0]
            count = v[1]
            count_sq = v[2]
            this_date = date(int(edit_date[:4]),
                             int(edit_date[5:7]),
                             int(edit_date[8:10])
                             )
            if this_date < first_date:
                first_date = this_date
            total += count
            total_sq += count_sq
        num_days = last_date - first_date
        num_days = num_days.days
        mean = total / num_days
        mean_sq = total_sq / num_days
        var = mean_sq - mean ** 2
        out_string = key + "," + str(mean) + "," + str(var)
        print(out_string)

if __name__ == '__main__':
    meansvars.run()