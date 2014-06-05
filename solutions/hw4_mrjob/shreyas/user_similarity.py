###
### This code was inspired by last year's student
### Max Gutman
###

from __future__ import division
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from itertools import combinations


class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches,
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def extract(self, _, record):
            """
            Take in 1 record from JSON file and yield <user_id, business_id>
            """
            if record['type'] == 'review':
                yield [record['user_id'], record['business_id']]


    def combine(self, usr_id, biz_id):
        yield [usr_id, list(set(biz_id))]


    def distribute(self, usr_id, biz_id):
        yield 'all', [usr_id, biz_id]



    def similarity(self, _, usr_biz_pairs):
        """
        find similarity of users given they are aggregated as lists of
        users and businesses
        """
        for (usr_a, biz_a), (usr_b, biz_b) in combinations(usr_biz_pairs, r=2):
            sim = UserSimilarity.jaccard(biz_a, biz_b)

            if sim >= 0.5:
                yield [usr_a, usr_b], sim


    ## Measure similarity
    @staticmethod
    def jaccard(biz_a, biz_b):
        return float(len(set(biz_a) & set(biz_b))) / len(set(biz_a) | set(biz_b))


    def steps(self):
        """
        mapper1: <line, record> => <user_id, business_id>
        reducer1: <user_id, business_id> => <user_id, [business_ids]>
        mapper2: <user_id, [business_ids]> => <KEY, [user_id, business_ids]>
        reducer2: <KEY, [user_id, business_ids]> => <[user_a, user_b], jaccard>
        """
        return [
            self.mr(mapper=self.extract, reducer=self.combine),
            self.mr(mapper=self.distribute, reducer=self.similarity)
        ]


if __name__ == '__main__':
    UserSimilarity.run()
