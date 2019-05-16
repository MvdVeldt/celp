from data import BUSINESSES, get_business
import ast

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
        for j in i:
            copy[j] = i[j]

    return copy

