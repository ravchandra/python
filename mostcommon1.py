import operator

def most_common(l):
    return sorted(dict((i,l.count(i)) for i in l).items(),key=operator.itemgetter(1),reverse=True)[:4]

l=[
   'red', 'green', 'black', 'pink', 'black', 'white', 'black', 'eyes',
   'white', 'black', 'orange', 'pink', 'pink', 'red', 'red', 'white', 'orange',
   'white', "black", 'pink', 'green', 'green', 'pink', 'green', 'pink',
   'white', 'orange', "orange", 'red'
]
print most_common(l)
