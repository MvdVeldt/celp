from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS, get_reviews, get_business
from helpers import get_attributes, new_atts, get_cities, b_c_pair, make_utility_matrix, create_similarity_matrix_categories, sorted_similarity, top_5, pivot_ratings, create_similarity_matrix_cosine, predict_ratings, predict_ids, predict_vectors, mse
import ast
import pandas as pd
import sklearn.metrics.pairwise as pw
import numpy as np


def recommend(user_id=None, business_id=None, city=None, n=10):
    """
    Returns n recommendations as a list of dicts. fdfdfdfd
    Optionally takes in a user_id, business_id and/or city.
    A recommendation is a dictionary in the form of:
        {
            business_id:str
            stars:str
            name:str
            city:str
            adress:str
        }
    """
    if not city:
        city = random.choice(CITIES)

    if not business_id:
        business_id = random.choice(BUSINESSES[city]['business_id'])

    b_c = b_c_pair(get_cities())
    u_matrix = make_utility_matrix(get_cities())
    u_matrix = u_matrix.fillna(0)
    s_matrix = create_similarity_matrix_categories(u_matrix)
    s_matrix = s_matrix.fillna(0)
    sorted_s = sorted_similarity(s_matrix, business_id)
    t_list = list(top_5(sorted_s, n).index)
    a_list = []

    for i in t_list:
        some = get_business(b_c[i][0], i)
        some_dict = {}
        some_dict['business_id'] = some['business_id']
        some_dict['stars'] = some['stars']
        some_dict['name'] = some['name']
        some_dict['city'] = some['city']
        some_dict['address'] = some['address']
        a_list.append(some_dict)

    if a_list == None:
        return random.sample(BUSINESSES[city], n)
    else:
        return a_list

ree = recommend(user_id=None, business_id='S9BSFX03TBqAHFF1M4c08g', city='sun city', n=5)

wew = []
0  EXFAB-c4qgqCNfk_T78oxw  EOzsAFr7eF8D4C3a4ZQicw     4.0               0.9
1  dQJH6y1VcStslYCyYTWJSw  uXCPUES8-cafSN_4oALhOQ     1.0               4.8
2  -S1dz92Q3RPfHomiqEeP8Q  ARPF656yM6oeEDSCnLhzIg     5.0               2.4
3  6r4J79yfO4eyItfbSsGP1w  vfsbLhXGiXm8lqI12abrbQ     4.0               1.8
4  vJ5wrLnxSOPcR8a8jScGkQ

pls = []
for i in ree:
    l = ['S9BSFX03TBqAHFF1M4c08g',i['business_id'], i['stars']]
    pls.append(l)

df = pd.DataFrame(pls, columns=['user_id','business_id','stars'])

print(mse(df))