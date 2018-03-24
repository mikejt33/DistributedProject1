"""Get article counts by day.

Grab roughly 1% of article titles and output them to a list.

Author: Joe
"""

from mrjob.job import MRJob
import random


class sampler(MRJob):

    def mapper(self, _, line):
        splt = line.split()
        die_roll = random.randint(0, 100)
        if die_roll == 37:
            if len(splt) > 1 and splt[0] == "REVISION":
                article = splt[3]  # Grab the title
                yield("key", article)

    def reducer(self, key, vals):
        set_o_articles = set([])  # A set ensures no diplucates are stored.
        for v in vals:
            set_o_articles.add(v)
        for stuff in set_o_articles:
            print(stuff)

if __name__ == '__main__':
    sampler.run()