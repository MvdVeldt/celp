from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS, get_reviews, get_business
from helpers import get_attributes, new_atts, get_cities, make_utility_matrix, create_similarity_matrix_categories, sorted_similarity, top_5
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

    u_matrix = make_utility_matrix(get_cities())
    s_matrix = create_similarity_matrix_categories(u_matrix)

    if not city:
        city = random.choice(CITIES)
        return random.sample(BUSINESSES[city], n)

    else:

