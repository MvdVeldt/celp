from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS, get_reviews, get_business
import ast
import pandas as pd
import sklearn.metrics.pairwise as pw
import numpy as np

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
                if a[j] == True or a[j] == 'free' or a[j] == 2:
                    df.loc[i,j] = 1
                else:
                    df.loc[i,j] = 0

    return df

def create_similarity_matrix_categories(matrix):
    npu = matrix.values
    m1 = npu @ npu.T
    diag = np.diag(m1)
    m2 = m1 / diag
    m3 = np.minimum(m2, m2.T)
    return pd.DataFrame(m3, index = matrix.index, columns = matrix.index)


u_matrix = make_utility_matrix(get_cities())


s_matrix = create_similarity_matrix_categories(u_matrix)



def sorted_similarity(s_matrix, business_id):

    df = s_matrix.loc[business_id].sort_values(ascending=False)

    return df

sorted_s = sorted_similarity(s_matrix, 'DGOWO87MQmA4-2swRLK2DA')
print(sorted_s)