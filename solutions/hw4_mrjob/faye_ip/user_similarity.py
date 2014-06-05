from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches,
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    """
    Outline of Steps:
    #1 - yield [ user_id, [list of all businesses reviewed] ]
    #2 - loop through user pairs:
        for i in range(number_of_users):
            for j in range(i, number_of_users):
    #3 - for each pair of users: jaccard = intersection / union
    #4 - if jaccard >= 0.5, yield [ jaccard, [user1, user2] ]
    """

    def init_mapper(self):
        self.user_ids = []
        self.users_businesses = {}

    def mapper(self, _, record):
        self.user_ids.append( record['user_id'] )
        self.users_businesses.setdefault( record['user_id'], [] )
        self.users_businesses[record['user_id']].append(record['business_id'])

    def final_mapper(self):
        for i in range(len(self.user_ids)):
            for j in range(i+1, len(self.user_ids)):
                yield [ [self.user_ids[i], self.user_ids[j]], [self.users_businesses[self.user_ids[i]], self.users_businesses[self.user_ids[j]]]]

    def reducer(self, user_id_pair, businesses_pair):
        for bp in businesses_pair:
            biz_pair = bp
        businesses_set_A = set(biz_pair[0])
        businesses_set_B = set(biz_pair[1])
        unionAB = businesses_set_A | businesses_set_B
        intersectionAB = businesses_set_A & businesses_set_B
        jaccard = float(len(intersectionAB)) / float(len(unionAB))
        if jaccard >= 0.5:
            yield [ jaccard, user_id_pair ]


    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper: <line, record> => <[pair of keys], [pair of values]>
        reducer: <key, [pair of values]>
        """
        return [self.mr(mapper_init=self.init_mapper,
                        mapper=self.mapper,
                        mapper_final=self.final_mapper,
                        reducer=self.reducer)]
        # return [
        #     self.mr(mapper=self.mapper1, reducer=self.reducer1),
        #     self.mr(mapper=...),
        # ]


if __name__ == '__main__':
    UserSimilarity.run()
