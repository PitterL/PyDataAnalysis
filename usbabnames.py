import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def add_prop(group):
    """Integer division floors"""
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group

def hello():
    path = os.sys.path[0]
    path += r"\pydata-book-master\ch02\names"
    names1880 = pd.read_csv(path + r"/yob1880.txt", names=['name', 'sex', 'birth'])
    #print names1880[:10]
    #sexsum = names1880.groupby('sex')['birth'].sum()
    #print sexsumfilefile
    years = range(1880, 2011)
    pieces = []
    columns = ['name', 'sex', 'births']
    for year in years:
        file = '/yob%d.txt' % year
        frame = pd.read_csv(path + file, names=columns)
        frame['year'] = year
        pieces.append(frame)
    names = pd.concat(pieces, ignore_index=True)
    print type(names)
    print names[:10]

    total_births = names.pivot_table(values='births', index='year', columns='sex', aggfunc=sum)
    #print "Total births by sex and year"
    #print total_births.tail()
    total_births.plot(kind='line', title='Total births by sex and year')
    #plt.show()

    names = names.groupby(['year', 'sex']).apply(add_prop)
    #print type(names2)
    #print names2[:10]
    #names3 = names2.groupby(['year', 'sex']).prop.sum()
    #print names3
    #print np.allclose(names2.groupby(['year', 'sex'])['prop'].sum(), 1)
    def get_top1000(group):
        return group.sort_values(by='births', ascending=False)[:1000]
    grouped = names.groupby(['year', 'sex'])
    top1000 = grouped.apply(get_top1000)
    print("top1000 names: %s" % type(top1000))
    print top1000[:5]
    name_births = top1000.pivot_table(values='births', index='year', columns='name', aggfunc=sum)
    subset = name_births[['John', 'Harry', 'Mary', 'Marilyn']]
    #print type(subset)
    #print subset[:5]
    subset.plot(subplots=True, figsize=(10, 10), grid=True, title="Number of births per year")
    table = top1000.pivot_table(values='prop', index='year', columns='sex', aggfunc=sum)
    #print type(table)
    #print table[:5]
    table.plot(yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10), title='sum of prop by year and sex')
    #plt.show()
    df = names[names.year == 2010][names.sex == 'M']
    #print df[:5]
    prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
    #print prop_cumsum[:5]
    #print prop_cumsum.searchsorted(0.5)
    def get_quantile_count(group, q=0.5):
        group = group.sort_values(by='prop', ascending=False)
        prop_cumsum = group.prop.cumsum().searchsorted(q) + 1
        return prop_cumsum

    diversity = names.groupby(['year', 'sex']).apply(get_quantile_count)
    #print type(diversity)
    diversity = diversity.unstack('sex')
    print type(diversity)
    print diversity
    diversity.plot(title="Order of popular name at top 50%")
    plt.show()