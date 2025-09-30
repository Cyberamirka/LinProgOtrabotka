from copy import deepcopy
from itertools import permutations
from fractions import Fraction

def Simplex(coefs, rprts, opt):
    n = len(coefs[0])
    base = []
    for i in range(len(coefs) - 1):
        j = len(coefs[i]) - 1
        while j > 0 and abs(coefs[i][j]) != 1: j -= 1
        base.append(j)
    simplex_table = {'basis': base, 'solution': rprts, 'coefs': [[Fraction(x, 1) for x in y] for y in coefs]}
    if opt == 'min':
        check = min_check
        ind = max_index
    elif opt == 'max':
        check = max_check
        ind = min_index
    no_limit = False
    tables = [deepcopy(simplex_table)]
    while not check(simplex_table['coefs'][-1], simplex_table['basis']):
        col = ind(simplex_table['coefs'][-1])
        row = sol_row(simplex_table, col)
        if row == -1:
            no_limit = True
            break
        cell = simplex_table['coefs'][row][col]
        simplex_table['basis'][row] = col
        for i in range(n):
            simplex_table['coefs'][row][i] /= cell
        simplex_table['solution'][row] /= cell
        go = [x for x in range(len(simplex_table['solution']))]
        go.remove(row)
        for i in go:
            mult = - simplex_table['coefs'][i][col]
            for j in range(n):
                simplex_table['coefs'][i][j] = simplex_table['coefs'][i][j] + simplex_table['coefs'][row][j] * mult
            simplex_table['solution'][i] = simplex_table['solution'][i] + simplex_table['solution'][row] * mult
        if simplex_table in tables:
            break
        tables.append(deepcopy(simplex_table))
    return simplex_table, no_limit, tables


def sol_row(table, ind):
    i = 0
    while table['coefs'][i][ind] == 0:
        i += i + 1
    while i < len(table['coefs']) and table['solution'][i] / table['coefs'][i][ind] < 0:
        i += 1
        while i < len(table['coefs']) and table['coefs'][i][ind] == 0:
            i += i + 1
    if i < len(table['coefs']):
        min_row = i
        for j in range(i, len(table['solution']) - 1):
            if table['coefs'][j][ind] > 0:
                if table['solution'][j] / table['coefs'][j][ind] < table['solution'][min_row] / table['coefs'][min_row][ind] and table['solution'][j] / table['coefs'][j][ind] >= 0:
                    min_row = j
        return min_row
    else:
        return -1


def max_check(lst, basis):
    for i in lst:
        if i < 0 and i not in basis: return False
    return True

def min_check(lst, basis):
    for i in lst:
        if i > 0 and i not in basis: return False
    return True

def min_index(lst):
    min_ind = 0
    for i in range(1, len(lst)):
        if lst[i] < lst[min_ind]:
            min_ind = i
    return min_ind

def max_index(lst):
    max_ind = 0
    for i in range(1, len(lst)):
        if lst[i] > lst[max_ind]: 
            max_ind = i
    return max_ind

#Функция для приведения к стандартной форме, не используется для двойственного симплекс метода
#Вводные аргументы
# z - список состоящий из коэффициэнтов функции z Пример: [2, 1]
# opt направление оптимизации, должно иметь значение или "min", или "max"
# limits - список ограничений. Ограничения должны быть списками. Пример: [3, 0, ">=", 3].
# not_negs - список индексов переменных, которые больше либо равны 0.
# double_flag - если False, функция вернёт вид для двойственной задачи ЛП, а если True, вернёт вид для М-метода
#Функция вернёт:
# coefs - список списков коэфициентов ограничений и функции z, коэфициенты функции z находятся в конце списка
# rparts - список состоящий из правых частей ограничений и функции z
# artifs - список индексов исскуственных переменных, всегда является пустым, если double_flag имеет значение False
def standartize(z, opt, limits, not_negs, double_flag):
    i = 0
    st_z = []
    while i < len(z):
        st_z.append(z[i])
        if i not in not_negs:
            st_z.append(-z[i])
        i += 1
    z = st_z
    if opt == 'min':
        m = 1000
    else:
        m = -1000
    coefs = []
    rparts = [0 for x in range(len(limits) + 1)]
    for i in range(len(limits)):
        coefs.append([0 for x in range(len(z))])
    artifs = []
    for i in range(len(limits)):
        sync = 0
        if limits[i][-1] < 0:
            sign = -1
            if limits[i][-2] == '<=':
                limits[i][-2] = '>='
            elif limits[i][-2] == '>=':
                limits[i][-2] = '<='
        else:
            sign = 1
        for j in range(len(limits[0]) - 2):
            coefs[i][j + sync] = limits[i][j] * sign
            if j not in not_negs:
                sync += 1
                coefs[i][j + sync] = limits[i][j] * sign * -1
        rparts[i] = limits[i][-1] * sign
        if limits[i][-2] == '<=':
            for j in range(len(coefs)):
                if j != i:
                    coefs[j].append(0)
            z.append(0)
            coefs[i].append(1)
        else:
            if limits[i][-2] == '>=':
                for j in range(len(coefs)):
                    if j != i:
                        coefs[j].append(0)
                z.append(0)
                coefs[i].append(-1)
            if double_flag:
                for j in range(len(z)):
                    z[j] += coefs[i][j] * m * -1
                rparts[-1] += rparts[i] * m
                for j in range(len(coefs)):
                    if j != i:
                        coefs[j].append(0)
                z.append(0)
                coefs[i].append(1)
                artifs.append(len(z) - 1)
    coefs.append([-x for x in z])
    return coefs, rparts, artifs

#Функция для двойственной задачи программирования
#Вводные аргументы:
# coefs - смотреть вывод функции standartize
# rparts - смотреть вывод функции standartize
# opt направление оптимизации, должно иметь значение или "min", или "max"
#Вывод функции:
# w - смотреть ввод функции z в функции standartize
# opt
# limits - смотреть ввод функции standartize
def dual_LP(coefs, rparts, opt):
    coefs[-1] = [-x for x in coefs[-1]]
    if opt == 'max':
        opt = 'min'
        compr = '>='
    else:
        opt = 'max'
        compr = '<='
    w = rparts[:-1]
    limits = []
    not_neg = set()
    not_pos = set()
    i = 0
    while i < len(coefs[0]):
        lim_coefs = [x[i] for x in coefs[:-1]]
        if lim_coefs.count(0) == len(lim_coefs) - 1 and (sum(lim_coefs) == 1 and compr == '>=' or sum(lim_coefs) == -1 and compr == '<='):
            if sum(lim_coefs) == 1:
                not_neg.add(lim_coefs.index(1))
            else:
                not_neg.add(lim_coefs.index(-1))
        elif lim_coefs.count(0) == len(lim_coefs) - 1 and (sum(lim_coefs) == -1 and compr == '>=' or sum(lim_coefs) == 1 and compr == '<='):
            if sum(lim_coefs) == 1:
                not_pos.add(lim_coefs.index(1))
            else:
                not_pos.add(lim_coefs.index(-1))
        else:
            if i > 0:
                if [-x for x in lim_coefs] == limits[-1][:-2] and -coefs[-1][i] == coefs[-1][i - 1]:
                    limits[-1][-2] = '='
                else:
                    limits.append(lim_coefs + [compr, coefs[-1][i]])
            else:
                limits.append(lim_coefs + [compr, coefs[-1][i]])
        i += 1
    return w, opt, limits, not_neg, not_pos

#Функция для приведения к стандартному виду для двойственного симплекс-метода
#Объяснение значений ввода и вывода смотреть в функции standartize
def dual_standartize(z, limits, not_negs):
    i = 0
    st_z = []
    while i < len(z):
        st_z.append(z[i])
        if i not in not_negs:
            st_z.append(-z[i])
        i += 1
    z = st_z
    coefs = []
    rparts = [0 for x in range(len(limits) + 1)]
    for i in range(len(limits)):
        coefs.append([0 for x in range(len(z))])
    for i in range(len(limits)):
        sync = 0
        if limits[i][-1] < 0:
            sign = -1
        else:
            sign = 1
        for j in range(len(limits[0]) - 2):
            coefs[i][j + sync] = limits[i][j] * sign
            if j not in not_negs:
                sync += 1
                coefs[i][j + sync] = limits[i][j] * sign * -1
        rparts[i] = limits[i][-1] * sign
        if limits[i][-2] == '<=' or limits[i][-2] == '>=':
            for j in range(len(coefs)):
                if j != i:
                    coefs[j].append(0)
            z.append(0)
            coefs[i].append(1)
            if limits[i][-2] == '>=':
                for j in range(len(coefs[i]) - 1):
                    coefs[i][j] *= -1
                rparts[i] *= -1
    coefs.append([-x for x in z])
    return coefs, rparts

#Функция для двойсвенного симплекс-метода
#Вводные аргументы:
# coefs - смотреть вывод функции dual_standartize
# rparts - смотреть вывод функции dual_standartize
# opt направление оптимизации, должно иметь значение или "min", или "max"
#Вывод функции:
# simplex_table - словарь с ключами:
#       basis - индексы находящиеся в базисе симплекс-таблицы
#       solution - список состоящий из столбца решение в симплекс таблице
#       coefs - с этим ключом хранится список аналогичный списку coefs в вводе функции
# simplex_table является последней таблицей из всех итераций симплекс таблицы и находится в конце списка tables
# no_limit - если имеет значение True, функция неограничена
# no_accept - если имеет значение True, функция не имеет допустимых решений
# tables - список всех итераций симплекс таблицы simplex_table
def dual_simplex(coefs, rprts, opt):
    n = len(coefs[0])
    base = find_basis(coefs[:-1], rprts[:-1])
    solution = []
    for i in range(len(base)):
        solution.append(Fraction(rprts[i], coefs[i][base[i]]))
    solution.append(Fraction(-sum(coefs[-1][x] if x in base else 0 for x in range(len(coefs[0]))), 1))
    simplex_table = {'basis': base, 'solution': solution, 'coefs': [[Fraction(x, 1) for x in y] for y in coefs]}
    if opt == 'min':
        check = min_check
        ind = max_index
    elif opt == 'max':
        check = max_check
        ind = min_index
    no_limit = False
    no_accept = False
    tables = [deepcopy(simplex_table)]
    while (row := dual_sol_row(simplex_table['solution'][:-1])) + 1:
        if not (col := dual_sol_col(simplex_table['coefs'][row], simplex_table['coefs'][-1], opt, simplex_table['basis'])) + 1:
            no_accept = True
            return simplex_table, no_limit, no_accept, tables
        cell = simplex_table['coefs'][row][col]
        simplex_table['basis'][row] = col
        for i in range(n):
            simplex_table['coefs'][row][i] /= cell
        simplex_table['solution'][row] /= cell
        go = [x for x in range(len(simplex_table['solution']))]
        go.remove(row)
        for i in go:
            mult = - simplex_table['coefs'][i][col]
            for j in range(n):
                simplex_table['coefs'][i][j] = simplex_table['coefs'][i][j] + simplex_table['coefs'][row][j] * mult
            simplex_table['solution'][i] = simplex_table['solution'][i] + simplex_table['solution'][row] * mult
        if simplex_table in tables:
            break
        tables.append(deepcopy(simplex_table))
    while not check(simplex_table['coefs'][-1], simplex_table['basis']):
        col = ind(simplex_table['coefs'][-1])
        row = sol_row(simplex_table, col)
        if row == -1:
            no_limit = True
            return simplex_table, no_limit, no_accept, tables
        cell = simplex_table['coefs'][row][col]
        simplex_table['basis'][row] = col
        for i in range(n):
            simplex_table['coefs'][row][i] /= cell
        simplex_table['solution'][row] /= cell
        go = [x for x in range(len(simplex_table['solution']))]
        go.remove(row)
        for i in go:
            mult = - simplex_table['coefs'][i][col]
            for j in range(n):
                simplex_table['coefs'][i][j] = simplex_table['coefs'][i][j] + simplex_table['coefs'][row][j] * mult
            simplex_table['solution'][i] = simplex_table['solution'][i] + simplex_table['solution'][row] * mult
        if simplex_table in tables:
            break
        tables.append(deepcopy(simplex_table))
    return simplex_table, no_limit, no_accept, tables

def dual_sol_row(lst):
    ind = -1
    i = 0
    while i < len(lst) and ind == -1:
        if lst[i] < 0:
            ind = i
        i += 1
    while i < len(lst):
        if lst[ind] > lst[i]:
            ind = i
        i += 1
    return ind

def dual_sol_col(row, z, opt, base):
    col = -1
    i = 0
    while i < len(row) and col == -1:
        if row[i] < 0 and i not in base:
            col = i
        i += 1
    while i < len(row):
        if row[i] < 0:
            if ((opt == 'min' and z[col] / row[col] > z[i] / row[i]) or (opt == 'max' and abs(z[col] / row[col]) > abs(z[i] / row[i]))) and i not in base:
                col = i
        i += 1
    return col

def find_basis(coefs, rparts):
    combos = permutations(reversed(range(len(coefs[0]))), len(coefs))
    max_match = 0
    basis = 0
    for i in combos:
        combo = []
        for j in i:
            combo.append(j)
        if 0 not in [coefs[j][combo[j]] for j in range(len(combo))]:
            match = 0
            for j in range(len(combo)):
                if rparts[j] % coefs[j][combo[j]] == 0:
                    match += 1
            if match > max_match:
                max_match = match
                basis = combo
    return basis