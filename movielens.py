import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def hello():
    path = os.sys.path[0]
    path += r"\pydata-book-master\ch02\movielens"

    unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
    users = pd.read_table(path + r"\users.dat", sep='::', header=None, names=unames, engine='python')

    rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_table(path + r'\ratings.dat', sep='::', header=None, names=rnames, engine='python')

    mnames = ['movie_id', 'title', 'genres']
    movies = pd.read_table(path + r'\movies.dat', sep='::', header=None, names=mnames, engine='python')

    #print "%d users:" % (len(users))
    #print users[:3]
    #print "%d ratings:" % (len(ratings))
    #print ratings[:3]
    #print "%d movies:" % (len(movies))
    #print movies[:3]

    mg1 = pd.merge(ratings, users)
    #print mg1[:5]
    mg2 = pd.merge(mg1, movies)
    #print mg2[:5]
    data = mg2
    print data[:5]

    print data.columns
    #dframe = data.groupby(list(data.columns))
    #print dframe.size()
    #print data[:5]
    #print data[-5:]
    mean_ratings = data.pivot_table(values='rating', index='title', columns='gender', aggfunc=np.mean)
    #print mean_ratings[:5]
    #print mean_ratings.columns
    ratings_by_title = data.groupby('title').size()
    active_titles = ratings_by_title.index[ratings_by_title >= 250]
    mean_ratings = mean_ratings.ix[active_titles]
    #print mean_ratings[:5]
    #top_female_rating = mean_ratings.sort_values(by='F', ascending=False)
    #print top_female_rating[:5]
    rating_top_index_a = mean_ratings.sum(0)
    rating_top_index_b = mean_ratings.sum(1)
    rating_top_index = rating_top_index_b #column value added together
    rating_top_index = rating_top_index.argsort()[::-1]
    rating_top = mean_ratings.take(rating_top_index)
    mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
    #sorted_by_diff = mean_ratings.sort_values(by='diff', ascending=False)
    #print sorted_by_diff[:5]
    print ("rating_top:(%s)" % type(rating_top))
    print rating_top[:5]
    rating_top[:20].plot(kind='barh', stacked=True)
    #plt.show()

    ratings_by_title = data.groupby('title')
    #print ratings_by_title.count()[:5]
    rating_std_by_title = ratings_by_title['rating'].std()
    rating_std_by_title = rating_std_by_title.ix[active_titles]
    rating_std_by_title.sort_values(ascending=False, inplace=True)
    print ("rating_std_by_title(%s):" % type(rating_std_by_title))
    print rating_std_by_title[:5]
    rating_std_by_title[:20].plot(kind='barh')
    plt.show()