"""For counting the number of distinct articles in the wiki revisions data.

This sends every line beginning with "Revision" straight to the mapper.
It uses the article title as the key, so that each unique title gets a reducer.
The reducer counts 1 for the first line it receives and does nothing otherwise.
Send this output to a file called distinct.txt and count the lines in that file
for a count of the number of distinct article titles in the data.


To output to a file run (in bash):

python distinct.py [datafilenamehere] > distinct.txt

Date: 3/14/2018"""

from mrjob.job import MRJob


class distinct(MRJob):

    def mapper(self, _, line):
        splt = line.split()
        if len(splt) > 1 and splt[0] == "REVISION":
            key = splt[3]
            yield(key, 1)

    def combiner(self, key, vals):
        count = 0
        for v in vals:
            if count == 0:
                count += 1
                yield(key, 1)
            else:
                yield(key, 0)

    def reducer(self, key, vals):
        count = 0
        for v in vals:
            if count == 0:
                count += 1
        yield(key, count)

if __name__ == '__main__':
    distinct.run()