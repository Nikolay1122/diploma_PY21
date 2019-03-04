from typing import Set

a = [1,2,3,4,5,6,7]
print(a)
print(len(a))
a = set(a)
print(a)
print(len(a))
b = [4,5]
print(b)
b = set(b)
print(b)
print(len(b))
a -= b
print(a)


print(a.isdisjoint(b))