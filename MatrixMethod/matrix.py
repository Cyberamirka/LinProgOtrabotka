def matrix_multiplication(a, b):
    if len(a[0]) == len(b):
        result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*b)] for A_row in a]
        return result
    else: return 0

def saddle_point(matrix):
    k = minmax(matrix)
    if k == maxmin(matrix):
        return k
    return None

def maxmin(matrix):
    return max(min(x) for x in matrix)

def minmax(matrix):
    maxs = []
    for i in range(len(matrix[0])):
        maxs.append(max(matrix[x][i] for x in range(len(matrix))))
    return min(maxs)

def find_in_matrix(matrix, element):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if element == matrix[i][j]:
                return (i, j)
    return -1

def max_index(lst):
    ind = 0
    for i in range(1, len(lst)):
        if lst[ind] < lst[i]:
            ind = i
    return ind

def min_index(lst):
    ind = 0
    for i in range(1, len(lst)):
        if lst[ind] > lst[i]:
            ind = i
    return ind

def approximate(matrix):
    table = []
    strA = find_in_matrix(matrix, maxmin(matrix))[0]
    new_line = [1, f'A{strA + 1}', *matrix[strA]]
    cols_strA = (2, len(matrix[strA])+ 2)
    strB = min_index(matrix[strA])
    strB_values = [matrix[x][strB] for x in range(len(matrix))]
    new_line += [f'B{strB + 1}'] + strB_values
    cols_strB = (cols_strA[1] + 1, cols_strA[1] + 1 + len(matrix))
    new_line += [min(new_line[cols_strA[0]:cols_strA[1]]) / new_line[0], max(new_line[cols_strB[0]:cols_strB[1]]) / new_line[0]]
    new_line.append((new_line[-1] + new_line[-2]) / 2)
    table.append(new_line)
    line = new_line
    for i in range(1, 20):
        new_line = [i + 1]
        strA = max_index(strB_values)
        new_line += [f'A{strA + 1}'] + [x + y for x, y in zip(matrix[strA], line[cols_strA[0]:cols_strA[1]])]
        strB = min_index(matrix[strA])
        strB_values = [matrix[x][strB] for x in range(len(matrix))]
        new_line += [f'B{strB + 1}'] + [x + y for x, y in zip(strB_values, line[cols_strB[0]:cols_strB[1]])]
        new_line += [min(new_line[cols_strA[0]:cols_strA[1]]) / new_line[0],
                     max(new_line[cols_strB[0]:cols_strB[1]]) / new_line[0]]
        new_line.append((new_line[-1] + new_line[-2]) / 2)
        table.append(new_line)
        line = new_line
    return table

def Bayes_criterion(matrixA, matrixP, pos):
    tableA = []
    for i in range(len(matrixA)):
        tableA.append([f"A{i + 1}", *matrixA[i], sum(x * y for x, y in zip(matrixA[i], pos))])
    tableA.append(["qj", *pos, ""])
    tableP = []
    for i in range(len(matrixP)):
        tableP.append([f"A{i + 1}", *matrixP[i], sum(x * y for x, y in zip(matrixP[i], pos))])
    tableP.append(["qj", *pos, ""])
    return tableA, tableP

def Wild_criterion(matrix):
    table = []
    for i in range(len(matrix)):
        table.append([f"A{i + 1}", *matrix[i], min(matrix[i])])
    return table

def Savage_criterion(matrix):
    table = []
    for i in range(len(matrix)):
        table.append([f"A{i + 1}", *matrix[i], max(matrix[i])])
    return table

def Hurwitz_criterion(matrix):
    table = []
    k = 0.6
    for i in range(len(matrix)):
        table.append([f"A{i + 1}", *matrix[i], min(matrix[i]), max(matrix[i]), k*min(matrix[i]) + (1 - k)*max(matrix[i])])
    return table