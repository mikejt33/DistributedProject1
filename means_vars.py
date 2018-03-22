"""Get article counts by day.

Get the mean and variance of number of edits per day for each article

Author: Joe
Date: 03/22/2018
"""


from mrjob.job import MRJob
from datetime import date

last_date = date(2008, 1, 3)




class meansvars(MRJob):

    def mapper(self, _, line):
        splt = line.split(",")
        date = splt[0]
        title = splt[1]
        count = int(splt[2])
        count_sq = int(splt[2]) ** 2
        yield(title, (date, count, count_sq))

    def combiner(self, key, vals):
        total = 0
        total_sq = 0
        first_date = date(2018, 3, 22)
        for v in vals:
            date = v[0]
            count = v[1]
            count_sq = v[2]
            this_date = date(int(date[:4]),
                             int(date[5:7]),
                             int(date[8:10])
                             )
            if this_date < first_date:
                first_date = this_date
            total += count
            total_sq += count_sq
        yield(key, (date, count, count_sq))

    def reducer(self, key, vals):
        total = 0
        total_sq = 0
        first_date = date(2018, 3, 22)
        for v in vals:
            date = v[0]
            count = v[1]
            count_sq = v[2]
            this_date = date(int(date[:4]),
                             int(date[5:7]),
                             int(date[8:10])
                             )
            if this_date < first_date:
                first_date = this_date
            total += count
            total_sq += count_sq
        num_days = last_date - first_date
        mean = total / num_days
        mean_sq = total_sq / num_days
        var = mean_sq - mean ** 2
        out_string = key + "," + str(mean) + "," + str(var)
        print(out_string)

if __name__ == '__main__':
    meansvars.run()