from data import BUSINESSES

Bs = BUSINESSES
cities = []
d = set()

for i in Bs:
    cities.append(i)

must_dict = ['Ambiance', 'GoodForMeal', 'BusinessParking', 'Music']


for i in cities:
    for j in Bs[i]:
        atts = j['attributes']
        print(atts)
        if atts != None:
            for n in atts:
                d.add(n)


print(d)