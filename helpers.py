from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS, get_reviews, get_business, get_userreviews
import ast
import pandas as pd
import sklearn.metrics.pairwise as pw
import numpy as np
import random

def get_attributes(city, business_id):

    """
    Given a city name and a business id, return that business's atributes as a dict

    """
    business = get_business(city, business_id)
    return business['attributes']

def new_atts(atts):

    """
    Restructures the attributes into a more practical format

    """
    must_dict = ['Ambience', 'GoodForMeal', 'BusinessParking', 'Music']
    L = []
    L2 = []
    copy = atts

    if atts!=None:
        for i in atts:
            if i in must_dict:
                L.append(atts[i])

        for i in must_dict:
            if i in copy:
                del copy[i]
        for i in L:
            i = ast.literal_eval(i)
            L2.append(i)


        for i in L2:
            if i!=None:
                for j in i:
                    copy[j] = i[j]

        return copy

    else:
        l = {}
        return l

def get_cities():
    cities = []

    for i in BUSINESSES:
        cities.append(i)

    return cities


def all_revs(cities):

    revs = []

    for i in cities:
        r = get_reviews(i)
        for j in r:
            l = []
            l.append(j['user_id'])
            l.append(j['business_id'])
            l.append(j['stars'])
            revs.append(l)

    return revs

def b_c_pair(cities):

    b_c_pair = {}

    for i in cities:
        b = BUSINESSES[i]
        for j in b:
            b_c_pair[j['business_id']] = [i]

    return b_c_pair


def make_utility_matrix(cities):


    b_c_pair = {}

    for i in cities:
        b = BUSINESSES[i]
        for j in b:
            b_c_pair[j['business_id']] = [i]

    all_atts = set()

    for i in cities:
        for j in BUSINESSES[i]:
            b_id = j['business_id']
            ats = new_atts(get_attributes(i, b_id))
            for k in ats:
                all_atts.add(k)

    df = pd.DataFrame( columns=all_atts, index=b_c_pair.keys())

    for i in df.index:
        for j in df.columns:
            df.loc[i,j] = 0

    for i in df.index:
        a = new_atts(get_attributes(b_c_pair[i][0], i))
        if len(a) > 0:
            for j in a.keys():
                if a[j] == True or a[j] == 'free' or a[j] == 2 or a[j] == 'True':
                    df.loc[i,j] = 1
                else:
                    df.loc[i,j] = 0

    return df

def create_similarity_matrix_categories(matrix):
    np.seterr(divide='ignore', invalid='ignore')
    npu = matrix.values
    m1 = npu @ npu.T
    diag = np.diag(m1)
    m2 = m1 / diag
    m3 = np.minimum(m2, m2.T)
    return pd.DataFrame(m3, index = matrix.index, columns = matrix.index)


def sorted_similarity(s_matrix, business_id):

    df = s_matrix.loc[business_id].sort_values(ascending=False)

    return df



def top_5(df, n):

    top_5 = df.nlargest(n)

    return top_5



u_matrix = make_utility_matrix(get_cities())

s_matrix = create_similarity_matrix_categories(u_matrix)

r = all_revs(get_cities())

df = pd.DataFrame(r, columns = ['user_id', 'business_id', 'rating'])



def pivot_ratings(df):
    """Creates a utility matrix for user ratings for movies

    Arguments:
    df -- a dataFrame containing at least the columns 'movieId' and 'genres'

    Output:
    a matrix containing a rating in each cell. np.nan means that the user did not rate the movie
    """
    return df.pivot(values='rating', columns='user_id', index='business_id')

def create_similarity_matrix_cosine(matrix):
    """Creates a adjusted(/soft) cosine similarity matrix.

    Arguments:
    matrix -- a utility matrix

    Notes:
    Missing values are set to 0. This is technically not a 100% correct, but is more convenient
    for computation and does not have a big effect on the outcome.
    """
    mc_matrix = matrix - matrix.mean(axis = 0)
    return pd.DataFrame(pw.cosine_similarity(mc_matrix.fillna(0)), index = matrix.index, columns = matrix.index)

def predict_ratings(similarity, utility, to_predict):
    """Predicts the predicted rating for the input test data.

    Arguments:
    similarity -- a dataFrame that describes the similarity between items
    utility    -- a dataFrame that contains a rating for each user (columns) and each movie (rows).
                  If a user did not rate an item the value np.nan is assumed.
    to_predict -- A dataFrame containing at least the columns movieId and userId for which to do the predictions
    """
    # copy input (don't overwrite)
    ratings_test_c = to_predict.copy()
    # apply prediction to each row
    ratings_test_c['predicted rating'] = to_predict.apply(lambda row: predict_ids(similarity, utility, row['user_id'], row['business_id']), axis=1)
    return ratings_test_c

### Helper functions for predict_ratings_item_based ###

def predict_ids(similarity, utility, userId, itemId):
    # select right series from matrices and compute
    if userId in utility.columns and itemId in similarity.index:
        return predict_vectors(utility.loc[:,userId], similarity[itemId])
    return 0

def predict_vectors(user_ratings, similarities):
    # select only movies actually rated by user
    relevant_ratings = user_ratings.dropna()

    # select corresponding similairties
    similarities_s = similarities[relevant_ratings.index]

    # select neighborhood
    similarities_s = similarities_s[similarities_s > 0.0]
    relevant_ratings = relevant_ratings[similarities_s.index]

    # if there's nothing left return a prediction of 0
    norm = similarities_s.sum()
    if(norm == 0):
        return 0

    # compute a weighted average (i.e. neighborhood is all)
    return np.dot(relevant_ratings, similarities_s)/norm

def mse(predicted_ratings):
    """Computes the mean square error between actual ratings and predicted ratings

    Arguments:
    predicted_ratings -- a dataFrame containing the columns rating and predicted rating
    """
    diff = predicted_ratings['rating'] - predicted_ratings['predicted rating']
    return (diff**2).mean()


# make copy
copy_test = df.copy()

# make list wiht random numbers between 0.5 and 5.0
randoms = []
for i in range(len(copy_test['rating'])):
    randoms.append(round(random.uniform(0.5, 5.0),1))


# make new column
copy_test['predicted rating'] = [2.0, 3.5, 3.0, 4.0, 3.0]
display(copy_test.head())

# make mse
mse_random = mse(copy_test)


print(f'mse for random prediction: {mse_random:.2f}')