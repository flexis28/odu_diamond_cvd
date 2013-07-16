import itertools
z = []
for i in range(0, 10):
    z.append([0]*8)
z[0][0]= 123
z[0][1]= 567
print z
a = [q for q in itertools.product(z[0],z[0])]
print a[0]