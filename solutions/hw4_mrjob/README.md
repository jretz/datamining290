Evaluation Comments
====================

## Jimmy's solution
- Added Jimmy's solution to this homework. Please read the docstring and the comment at the top where he explains in detail each step of the process.
```

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
```


## Student Solution

@faye_ip 's MultiStep map-reduce job with __output caching__ to yield only at the right time. She has kindly provided [her reference for code at the mrJOB documenations](https://pythonhosted.org/mrjob/guides/writing-mrjobs.html#setup-and-teardown-of-tasks)

Take a look at her __not yielding__ in the first step, only initializing the variables while the second step yields into those variables. According to @jretz this has caching properties as the variable value is stored on the mapper and yields only when a step is complete. It brings down the network traffic, etc ..

