def get_all_index_find_to(lst: list, value) -> list:
    l = lst.copy()
    indexes = list()

    while value in l:
        indexes.append(l.index(value))
        l[l.index(value)] = None

    return indexes




# list limits variable              0           1           2
limits_variable: list[tuple] = [(0, None), (None, None), (0, None)]

# basis
basis: list[int] = [1, 2]

print("horisontal label")
for i in range(len(limits_variable)):
    if limits_variable[i] != (None, None):
        print(f"x{i+1}", end=" ")
    else:
        print(f"x{i+1}' x{i+1}''", end=' ')


print("\n\nbasis")

# как определить какая это переменная учитывая что дополнительными переменными x'' могут быть только небазисные переменные
for i in basis:
    negative_value_index = get_all_index_find_to(limits_variable, (None, None))
    if i > len(limits_variable):
        print(f"x{i+1}")
    elif i in negative_value_index:
        print(f"x{i+1}'")
    elif i - 1 in negative_value_index:
        print(f"x{i}''")