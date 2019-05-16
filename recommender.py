from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
from helpers import get_business, get_attributes, new_atts
import random
import ast


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
    return random.sample(BUSINESSES[city], n)
