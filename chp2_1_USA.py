# -*- coding: utf-8 -*-
"""
Created on Mon May 15 20:26:23 2017
@author: renke
"""
#import os

import json
from collections import defaultdict
import pandas as pd
from pandas import DataFrame, Series
import numpy as np

chp2='D:/Python/Books/Python_for_Data_Analysis_Source/ch02/'
filename=chp2 + 'usagov_bitly_data2012-03-16-1331923249.txt'
records=[json.loads(line) for line in open(filename)]
#print (records)
#print(records[0])
#print(records[0]['tz'])
time_zone=[rec['tz'] for rec in records if 'tz' in rec]
#print(time_zone)
#print(time_zone[:10])

def get_counts(sequence):
    counts=defaultdict(int)
    for x in sequence:
        counts[x]+=1
    return counts

counts=get_counts(time_zone)
#print(counts)
#print(counts['America/New_York'])

#print(len(time_zone))

def top_counts(count_dict,n=10):
    value_key_pairs=[(count,tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

#print(top_counts(counts))

frame=DataFrame(records)
#print(frame)

#print(frame['tz'][:10])

tz_counts=frame['tz'].value_counts()

#print(tz_counts)
clean_tz=frame['tz'].fillna('Missing')
clean_tz[clean_tz=='']='Unknown'

#thanks for http://www.jelekinn.com/python-data-analysis-3-mac.html,
# which tell me the problem of Empty 'DataFrame': no numeric data to plot
#tz_counts=clean_tz.value_counts().astype(float)
#print(tz_counts[:10])


#tz_counts[:10].plot(kind='barh',rot=0)

#print(frame['a'][1])
#print(frame['a'][50])
#print(frame['a'][51])
results=Series(x.split()[0] for x in frame.a.dropna())
#print(results)
#print(results.value_counts()[:8])

cframe=frame[frame.a.notnull()]
# attention, Upper case in Windows
operating_system=np.where(cframe['a'].str.contains('Windows'),
                          'Windows','Not Windows')

#print(operating_system[:5])
by_tz_os=cframe.groupby(['tz',operating_system])
agg_counts=by_tz_os.size().unstack().fillna('0')
#print(agg_counts[:10])
indexer=agg_counts.sum(1).argsort()
#print(indexer[:10])
count_subset=agg_counts.take(indexer)[-10:].astype(float) 
#print(count_subset)
#count_subset.plot(kind='barh',stacked=True)
normed_subset=count_subset.div(count_subset.sum(1),axis=0).astype(float)
normed_subset.plot(kind='barh',stacked=True)