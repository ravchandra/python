a = [(1, 2, 3, 4), (5, 6, 7, 8), (9,10,11,12)]
k = ("id","var","v3","v4")
d = []
for i in a:
	d.append({j:i[k.index(j)] for j in k})
