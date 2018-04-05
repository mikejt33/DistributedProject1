"""For counting the total number of revisions in the wiki data. Output of this
file should be put in for the variable "total" in the file frequency.py
to serve as the denominator in calculating the articles' appearance frequency
in the data.

Date: 3/14/2018"""

from mrjob.job import MRJob


class totalcount(MRJob):

    def mapper(self, _, line):
        splt = line.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            yield("key", 1)

    def combiner(self, key, vals):
        count = 0
        for v in vals:
            count += 1
        yield(key, count)

    def reducer(self, key, vals):
        count = 0
        for v in vals:
            count += float(v)
        yield(key, count)

if __name__ == '__main__':
    totalcount.run()