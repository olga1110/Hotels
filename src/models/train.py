lst1 = [1,2,5]
lst2 = [1,2,3, 4]

# добавление: 3: lst2> lst1
# удаление: -
# оставить: 1, 2

# add_lst = set(lst2) - set(lst1)
# delete_lst = set(lst1) - set(lst2)
# print(delete_lst)
#
# if add_lst := list(set(lst2) - set(lst1)):
#     print('создаем записи', add_lst)
# if set(lst1) - set(lst2):
#     print('записи к удалению')


my_str = 'bb'

# учесть регистр


# for i in my_str:
#     print(i)

# полином
from collections import Counter
#
# mycounter = Counter(my_str)
# print(mycounter)
#
# polynom_letters = [v if not v % 2 else v//2 * 2 for k, v in mycounter.items()]
# print(polynom_letters)
# len_polynom = sum(polynom_letters)
# print(f'{len_polynom=}')
#
# if not len_polynom:
#     len_polynom = 1
# elif len_polynom < len(my_str):
#     len_polynom += 1
#
# print(len_polynom)
#
# # пересечение массивов
# num1 = [1,2,2, 3, 1]
# num2 = [2,2,3]
#
# print(set(num1) & set(num2))


# 2.
s = 'counttit'
cur_let = s[0]
counter = 0
res = dict()

# for i, val in enumerate(s):
#     if val == cur_let:
#         counter += 1
#     else:
#         res[cur_let] = counter
#         cur_let = val
#         counter = 1
#     if i + 1 == len(s):
#         res[cur_let] = counter
# print(res)


for val in s:
    if val == cur_let:
        counter += 1
    else:
        if (res.get(cur_let) and res.get(cur_let) < counter) or not res.get(cur_let):
            res[cur_let] = counter
        cur_let = val
        counter = 1
else:
    if (res.get(cur_let) and res.get(cur_let) < counter) or not res.get(cur_let):
        res[cur_let] = counter
print(res)






# my_counter = dict(Counter(my_str))
# a = {'a': 1, 'b': 2, 'c': 3}
#
# print([k for k, v in a.items() if v == max(a.values())])
#
# print(max(a.items(), key=lambda k_v: k_v[1])[0])











