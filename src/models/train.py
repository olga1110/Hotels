lst1 = [1,2,5]
lst2 = [1,2,3, 4]

# добавление: 3: lst2> lst1
# удаление: -
# оставить: 1, 2

# add_lst = set(lst2) - set(lst1)
delete_lst = set(lst1) - set(lst2)
print(delete_lst)

if add_lst := list(set(lst2) - set(lst1)):
    print('создаем записи', add_lst)
if set(lst1) - set(lst2):
    print('записи к удалению')








