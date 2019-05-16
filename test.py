from data import BUSINESSES
import ast



Bs = BUSINESSES
w = Bs['westlake']

s = w[5]

atts = s['attributes']

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




print(copy)



