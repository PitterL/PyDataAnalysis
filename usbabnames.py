import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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
    #print type(names)
    #print names[:10]

    total_births = names.pivot_table(values='births', index='year', columns='sex', aggfunc=sum)
    #print "Total births by sex and year"
    #print total_births.tail()
    total_births.plot(kind='line', title='Total births by sex and year')
    #plt.show()

    def add_prop(group):
        """Integer division floors"""
        births = group.births.astype(float)

        group['prop'] = births / births.sum()
        return group

    names = names.groupby(['year', 'sex']).apply(add_prop)
    print "<names>:"
    print names.head()
    #print type(names2)
    #print names2[:10]
    #names3 = names2.groupby(['year', 'sex']).prop.sum()
    #print names3
    #print np.allclose(names2.groupby(['year', 'sex'])['prop'].sum(), 1)
    def get_top1000(group):
        return group.sort_values(by='births', ascending=False)[:1000]
    grouped = names.groupby(['year', 'sex'])
    i = 0
    for year, group in grouped:
        print year
        print group.head()
        i = i + 1
        if i > 2:
            break
    top1000 = grouped.apply(get_top1000)
    print("top1000 names: %s" % type(top1000))
    print top1000

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
    df = names[(names.year == 2010) & (names.sex == 'M')]
    #print df[:5]
    prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
    #print prop_cumsum[:5]
    #print prop_cumsum.searchsorted(0.5)
    def get_quantile_count(group, q=0.5):
        group = group.sort_values(by='prop', ascending=False)
        index = group['prop'].cumsum().searchsorted(q)[0]
        #print index
        prop_cumsum = index + 1
        #print type(prop_cumsum)
        return prop_cumsum

    diversity = names.groupby(['year', 'sex'])
    #print type(diversity)
    diversity = diversity.apply(get_quantile_count)
    #print type(diversity)
    diversity = diversity.unstack('sex')
    #print type(diversity)
    #print diversity[:5]
    diversity.plot(title="Order of popular name at top 50%")
    #plt.show()

    get_last_letter = lambda x: x[-1]
    last_letters = names.name.map(get_last_letter)
    #print type(last_letters)
    #last_letters.name = 'last_letter'
    #print last_letters[]

    table = names.pivot_table(values='births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)
    #print table.head()
    subtable = table.reindex(columns=[1910, 1960, 2010], level='year').fillna(0)
    print "<subtable>:"
    print subtable.head()
    print "sum:"
    #subtable_sum = subtable.sum(axis=1, level='sex')
    #print subtable_sum.head()
    subtable_sum = subtable.sum(axis=0)
    #print subtable_sum

    #print subtable_sum.head()
    #subtable_sum2 = subtable_sum.apply(lambda x: x.sum(), axis=1)
    #print subtable_sum2
    letter_prop = subtable / subtable_sum.astype(float)
    print "prop:"
    print letter_prop.head()
    fig, axes = plt.subplots(2, 1,  figsize=(10, 8))
    letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
    letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female')
    #plt.show()

    letter_prop = table /table.sum(axis=0)
    dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
    #print dny_ts
    dny_ts.plot(kind='line', title="d/n/y by years")
    #plt.show()

    all_names = top1000.reset_index(drop=True).name.unique()
    print "<all names>:"
    print all_names
    mask = np.array(['lesl' in x.lower() for x in all_names])
    lesley_like = all_names[mask]
    #print lesley_like
    filtered = top1000[top1000.name.isin(lesley_like)].reset_index(drop=True)
    print "<top1000 lesley>:"
    print filtered.head()
    #print filtered.groupby('name').apply(lambda x: x['births'].sum())
    table = filtered.pivot_table(values='births', index='year', columns='sex', aggfunc='sum')
    print table.head()
    print table.sum(1)
    table = table.div(table.sum(1), axis=0)
    print table.tail()
    table.plot(style = {'M': 'k-', 'F': 'k--'})
    plt.show()