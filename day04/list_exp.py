from __future__ import annotations
lst = [1, 2, 3, 4, 5]

for item in lst:
    if item == 3:
        lst.append(item - 1)
    if item == 4:
        lst.append(3)


print(lst)
