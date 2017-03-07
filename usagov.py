import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from collections import defaultdict
from collections import Counter

def get_counts(seq):
    counts = defaultdict(int)
    for x in seq:
        counts[x] += 1
    return counts

def get_top_counts(dic_list, n = 10):
    list_a = [(k, v) for v, k in dic_list.items()]
    list_a.sort()
    return list_a[-n:]

def hello():
    path = os.sys.path[0]
    file = path + r"\pydata-book-master\ch02\usagov_bitly_data2012-03-16-1331923249.txt"
    print file
    records = [json.loads(lines) for lines in open(file)]

    """ CHECK DICT"""
    #print records
    #print records[0]['tz']
    time_zone = [rec['tz'] for rec in records if 'tz' in rec]
    counts = get_counts(time_zone)
    top_counts = get_top_counts(counts)
    #print top_counts
    sort_counts = Counter(time_zone)
    #print sort_counts.most_common(3)

    """ CHECK FRAME"""
    frame = pd.DataFrame(records)
    #print frame
    #print frame.columns
    #print frame['tz'].value_counts()
    clean_tz = frame['tz'].fillna('Missing')
    #print clean_tz
    clean_tz[clean_tz == ''] = 'Unknown'
    tz_counts = clean_tz.value_counts()
    print "tz series[:10]:"
    print tz_counts[:10]
    #tz_counts[:10].plot(kind='barh', rot = 0)
    #plt.show()

    """Series"""
    "a : 'Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/535.11 (KHTML, like Gecko) Chrome\/17.0.963.78 Safari\/535.11'"
    results = pd.Series([x.split()[0] for x in frame['a'].dropna()])
    print "Explorer type"
    print type(results)
    cframe = frame[frame.a.notnull()]
    operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Non windows')
    #print operating_system[:10]
    #print type(operating_system)
    by_tz_os = cframe.groupby(['tz', operating_system])
    print "cframe.groupby(['tz', operating_system])"
    #print type(by_tz_os)
    #print by_tz_os.size()
    agg_counts = by_tz_os.size().unstack().fillna(0)
    print ("Unstack above group %s" %(type(agg_counts)))
    print agg_counts
    print "Sum the unstack group (to a Series)"
    agg_counts_sum = agg_counts.sum(1)
    print type(agg_counts_sum)
    #print agg_counts_sum.sort_values(ascending=False)
    #print agg_counts_sum.argsort()
    #indexer = agg_counts_sum.sort_values()
    indexer = agg_counts_sum.argsort()
    print ("sort the unstack group by index")
    #print list(indexer[:10])
    print ("take the agg_counts by indexer")
    count_subset = agg_counts.take(indexer)[-10:]
    print count_subset
    print ("plot the sequence")
    count_subset.plot(kind='barh', stacked=True)
    count_normalize = count_subset.div(count_subset.sum(1), axis=0)
    count_normalize.plot(kind='barh', stacked=True)
    plt.show()