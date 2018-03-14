"""For counting the frequencies of articles in the wiki revisions data.

Date: 3/14/2018"""

from mrjob.job import MRJob


total = 715.0  # Put output from totalrevisions.py here in place of 0.


class articlefreq(MRJob):

    def mapper(self, _, line):
        splt = line.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            key = splt[3]
            yield(key, 1)

    def combiner(self, key, vals):
        count = 0
        for v in vals:
            count += 1
        yield(key, count)

    def reducer(self, key, vals):
        count = 0
        for v in vals:
            count += float(v)
        yield(key, count / total)

if __name__ == '__main__':
    articlefreq.run()