from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS, get_reviews, get_business
from helpers import  get_attributes, new_atts
import ast
import pandas as pd




cities = []

for i in BUSINESSES:
    cities.append(i)

revs = []

for i in cities:
    r = get_reviews(i)
    for j in r:
        l = []
        l.append(j['user_id'])
        l.append(j['business_id'])
        l.append(j['stars'])
        revs.append(l)


unique_u = set()


for i in cities:
    u = USERS[i]
    for j in range(len(u)):
        this = u[j]
        unique_u.add(this['user_id'])

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
    a = new_atts(get_attributes(b_c_pair[i][0], i))
    if len(a) > 0:
        for j in a.keys():
            if a[j] == 'True':
                df.loc[i,j] = 1

print(df)


