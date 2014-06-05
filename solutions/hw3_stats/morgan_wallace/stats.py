# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""
from __future__ import division
import fileinput
import csv

#Added imports to make calculations with standard libraries
# from numpy import std,sqrt,average,median

# <codecell>

amounts= [float(i[14]) for i in csv.reader(fileinput.input("itpas2.txt"), delimiter='|')]

# <codecell>

#get rid of negative amounts (refunds) and a positive record of equal magnitude.
negs=[i for i in amounts if i<0]
print len(amounts)
print len(negs)

# <codecell>

#Get rid of the refunds and their positive counter parts
#In a couple dozen cases, the negative amounts do not have an
# exact matching positive amount. Those negatives are still removed,
# leaving extra positives that skew the data but hopefully not by much.

while len(negs)>0:
    n=negs.pop()
    del amounts[amounts.index(n)]
    try:
        del amounts[amounts.index(n*-1)]
    except:
        print str(n) + " does not have a positive counterpart"

# <codecell>

len(amounts)

# <codecell>

total = sum(amounts)
min1 = min (amounts)
max1 = max (amounts)

# <codecell>

def get_mean(l):
    return sum(l)/len(l)
mean = get_mean(amounts)

# <codecell>

def get_median(l):
    l.sort()
    if len(l)%2==1: #odd
        i=int((len(l)-1)/2)
        return l[i]
    else: #even
        i=int(len(l)/2)
        i2=i-1
        return (l[i]+l[i2])/2
median=get_median(amounts)

# <codecell>

def get_sd(l):
    squared_deviations=[(abs(i-mean))**2 for i in l]
    sd=get_mean(squared_deviations)**.5
    return sd
sd = get_sd(amounts)

# <codecell>

candidates = []
for row in csv.reader(fileinput.input("itpas2.txt"), delimiter='|'):
    if row[16] not in candidates:
        candidates.append(row[16])

# <codecell>

##### Print out the stats
print "Total: %s" % total
print "Minimum: %s" % min1
print "Maximum: %s" % max1
print "Mean: %s" %mean
print "Median: %s" %median
print "Standard Deviation: %s" % sd

##### Comma separated list of unique candidate ID numbers
# print "Candidates: %s" % candidates

# <codecell>

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
#     new_max = max(amounts+[value])
#     new_min = min(amounts+[value])
    norm = ((value - min1)/(max1 -min1))
    ###/

    return norm

# <codecell>

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])

