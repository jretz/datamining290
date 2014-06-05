from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


# The simplest approach would be to group all users together in a single
# reducer and cross every user with every other user.
#
# The approach here is to duplicate the per-user data into a separate group for
# every business they reviewed. This results in a lot of data duplication, but
# we get good parallelism (we can use as many CPU cores as we have distinct
# businesses). It also let's us only compare users who have at least one
# business in common. There are some wasted iterations where users have
# multiple businesses in common.
#
# How do the number of iterations compare?
#
# There are about 45K distinct users in the dataset, so the simple approach
# would result in about 45K^2 ~= 1B iterations and no parallelism for those
# iterations. ~99% of those iterations are over user pairs with no businesses
# in common, resulting in no output.
#
# The approach here results in about 12.5M iterations, largely performed in
# parallel. About 20% of those iterations are wasted because users shared
# multiple businesses. More than 98% of the 2B iterations are skipped
# altogether because we avoid iterating over user pairs with no shared
# businesses.
#
# So, this approach runs ~100x as fast over the entire dataset when no
# parallelism is used, and adding CPU cores will speed us up nearly linearly
# with the number of CPU cores used. That is, this would run ~5,000 times as
# fast as the simple approach with a dozen quad core machines (such a cluster
# costs $5-10 per hour on AWS).


class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        """
        extraction_mapper: <None, record> =>
            <user_id, business_id> for a single review

        replicating_reducer: <user_id, [business_id, ...] =>
            <business_id, (user_id, [business_id, ...])>

        identity_mapper: yield whatever comes in,
            we don't actually have to specify this, it is the default

        similarity_reducer: <biz, [(u, [biz, ...]), (u, [biz, ...]), ...] =>
            <(user_id_1, user_id_2), similarity>
        """
        return [
            self.mr(
                mapper=self.extraction_mapper,
                reducer=self.replicating_reducer
            ),
            self.mr(
                reducer=self.similarity_reducer
            ),
        ]

    def extraction_mapper(self, _, row):
        """Extract the user and business for each review."""
        if row['type'] == 'review':
            yield row['user_id'], row['business_id']

    def replicating_reducer(self, user_id, business_ids):
        """All the businesses reviewed by a single user have now been grouped.
        Produce a new copy of (user_id, [business_id, ...]) pairs for each
        distinct business_id. Grouping by business_id in the next step means we
        only have to iterate over user pairs where both users actually reviewed
        the same business. This will result in better parallelism and reduce
        the number of user pairs we have to compare in the next step.
        """
        business_ids = list(set(business_ids))
        for business_id in business_ids:
            yield business_id, (user_id, business_ids)

    def similarity_reducer(self, business_id, user_and_business_ids):
        """Iterate over all pairs of users that reviewed business_id. If
        business_id is the smallest business_id they have in common, then
        compute and yield their similarity. This "minimum" constraint ensures
        that we only compute and yield similarity once for each pair of users.
        """
        user_and_business_ids = [(u, set(b)) for u, b in user_and_business_ids]
        for i in range(len(user_and_business_ids)):
            user_i, biz_i = user_and_business_ids[i]
            for j in range(i + 1, len(user_and_business_ids)):
                user_j, biz_j = user_and_business_ids[j]
                intersection = biz_i & biz_j
                # Only bother comparing each pair of users once
                if min(intersection) == business_id:
                    union = biz_i | biz_j
                    similarity = float(len(intersection)) / len(union)
                    yield (user_i, user_j), similarity
                    self.increment_counter('iterations', 'useful')
                else:
                    self.increment_counter('iterations', 'wasted')


if __name__ == '__main__':
    UserSimilarity.run()
