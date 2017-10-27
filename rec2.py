def recsum(l):
    sum=0
    for i in l:
        if type(i)==int:
            sum +=i
        elif type(i)==list:
            sum += recsum(i)
    return sum

t=[1, 2, [3,4], [5,6]]
print recsum(t)
