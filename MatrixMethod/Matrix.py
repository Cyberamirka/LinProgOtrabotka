"""
    Matrix - модуль для решения задач
"""

import numpy as np
import csv
from .MatrixTypes import ApproximateResult



def maxmin(a: np.ndarray):
    return np.max([np.min(i) for i in a])


def minmax(a: np.ndarray):
    return np.min([np.max(i) for i in a.T])


def saddle_point(pay_matrix: np.ndarray) -> float|int|None:
    return minmax(pay_matrix) if minmax(pay_matrix) == maxmin(pay_matrix) else None

# смешанные методы
def MixStrategy(pay_matrix: np.ndarray, A: np.ndarray, B: np.ndarray) -> tuple:
    """ Решение игры при помощи смешанных стратегий"""
    return A.dot(pay_matrix).dot(B.T)



def incA(a: int) -> str: return f"A{a+1}"
def incB(b: int) -> str: return f"B{b+1}"




# приближенные значения
# на вход таблица типа np.ndarray и кол-во итераций, на выходе таблица с готовым ответом
def ApproximateSolving(pay_matrix: np.ndarray, count_step: int) -> ApproximateResult:
    """
        Решение матричных игр при помощи приближённым методом
    """

    # список выбранных стратегий игрока А и В
    selected_strategy_a: list[int] = list()
    selected_strategy_b: list[int] = list()

    tmp = np.array([np.min(i) for i in pay_matrix])
    selected_strategy_a.append( int(np.where(np.isclose(tmp, max(tmp)))[0][0]) )
    # print(selected_strategy_a)

    tmp = pay_matrix[selected_strategy_a[-1]]
    selected_strategy_b.append( int(np.where(np.isclose(tmp, min(tmp)))[0][0]) )
    # print(selected_strategy_b)

    for i in range(count_step):
        tmp = pay_matrix[:, selected_strategy_b[-1]]
        selected_strategy_a.append( int(np.where(np.isclose(tmp, max(tmp)))[0][0]) )

        tmp = pay_matrix[selected_strategy_a[-1]]
        selected_strategy_b.append( int(np.where(np.isclose(tmp, min(tmp)))[0][0]) )

    #   сборка ответа
    #   учесть что надо сложить каждый новый результат и добавлять его в таблицу
    table: list[list[str]] = list()

    title = ["N", "Стратегии игрока А"] + \
            [f"B{i + 1}" for i in range(pay_matrix.shape[1])] + \
            ["Стратегии игрока B"] + \
            [f"A{i + 1}" for i in range(pay_matrix.shape[0])] + \
            ["V'n", "V''n", "Vср n"]

    # добавление тайтла
    table.append(title)


    sum_a: np.ndarray = pay_matrix[selected_strategy_a[0]].copy()
    sum_b: np.ndarray = pay_matrix[:, selected_strategy_b[0]].copy()
    v_n: np.float64 = np.min(sum_a)
    v__n: np.float64 = np.max(sum_b)
    v_avg_n: np.float64 = (v_n + v__n) / 2
    item_table = ["1"] + [incA(selected_strategy_a[0])] + sum_a.tolist() + [incB(selected_strategy_b[0])] + sum_b.tolist() + [v_n, v__n, v_avg_n]
    table.append(item_table)


    # формирование результата, формирую его как строки для простой вставки в таблицу
    for i in range(2, len(selected_strategy_a)):
        sum_a += pay_matrix[selected_strategy_a[i-1]].copy()
        sum_b += pay_matrix[:, selected_strategy_b[i-1]].copy()
        v_n: np.float64 = np.min(sum_a) / i
        v__n: np.float64 = np.max(sum_b) / i
        v_avg_n: np.float64 = (v_n + v__n) / 2
        item_table = [str(i)] + [incA(selected_strategy_a[i-1])] + sum_a.tolist() + [incB(selected_strategy_b[i-1])] + sum_b.tolist() + [v_n, v__n, v_avg_n]
        table.append(item_table)

    result = ApproximateResult()
    result.table = np.array(table)
    result.count_clean_strategy_a = np.array([ selected_strategy_a.count(i) for i in range(0, pay_matrix.shape[1]) ])
    result.count_clean_strategy_b = np.array([ selected_strategy_b.count(i) for i in range(0, pay_matrix.shape[0]) ])
    result.frequency_a = result.count_clean_strategy_a / count_step
    result.frequency_b = result.count_clean_strategy_b / count_step
    result.price = v_avg_n

    return result




def save_approxima_solving(path: str, table: np.ndarray[np.ndarray[str]]) -> None:
    """
        Сохранение результата в файл решённый приближённым методом
        path - путь до файла, именно путь, а не название
        table - таблица, желательно что-бы все элементы имели тип str
    """
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(table)



def find_matrix_risk(mtrx: np.ndarray[np.ndarray[float]]):
    b = np.array([np.max(i) for i in mtrx.copy().T])
    return np.array( [b - i for i in mtrx.copy()] )



def Bayes_criterion(matrixA, matrixP, pos):
    # Преобразуем в numpy arrays
    A = np.array(matrixA)
    P = np.array(matrixP)
    q = np.array(pos)

    # Вычисляем суммы для каждой стратегии
    sums_A: np.ndarray = A @ q  # матричное умножение = sum(x*y for x,y in zip(row, pos))
    sums_P: np.ndarray = P @ q


    # Собираем результаты
    tableA = [[incA(i), *row, sum_val] for i, (row, sum_val) in enumerate(zip(matrixA, sums_A))]
    tableA = [["Стратегия А"] + [f"П{i + 1}" for i in range(len(matrixA))] + ["Средний выйгрыш А"]] + tableA
    tableA.append(["qj", *pos, ""])

    tableP = [[incA(i), *row, sum_val] for i, (row, sum_val) in enumerate(zip(matrixP, sums_P))]
    tableP = [["Стратегия B"] + [f"П{i + 1}" for i in range(len(matrixA))] + ["Средний риск"]] + tableP
    tableP.append(["qj", *pos, ""])

    return tableA, tableP, sums_A.tolist().index(max(sums_A)), sums_P.tolist().index(min(sums_P))



def Wild_criterion(matrix):
    table = [["Стратегии А"] + [f"П{i+1}" for i in range(len(matrix[0]))] + ["a"]]
    maxVal = 0
    index = 0

    for i in range(len(matrix)):
        item = min(matrix[i])
        if item > maxVal:
            maxVal = item
            index = i
        table.append([f"A{i + 1}", *matrix[i], min(matrix[i])])
    return table, index


def Savage_criterion(matrix):
    table = [["Стратегии А"] + [f"П{i + 1}" for i in range(len(matrix[0]))] + ["p"]]
    maxVal = matrix[0][0]
    index = 0

    for i in range(len(matrix)):
        item = max(matrix[i])
        if item < maxVal:
            maxVal = item
            index = i
        table.append([f"A{i + 1}", *matrix[i], max(matrix[i])])
    return table, index


def Hurwitz_criterion(matrix):
    table = [["Стратегии А"] + [f"П{i+1}" for i in range(len(matrix[0]))] + ["a", "w", "h"]]
    k = 0.6
    maxVal = 0
    index = 0

    for i in range(len(matrix)):
        item = k*min(matrix[i]) + (1 - k)*max(matrix[i])
        if item > maxVal:
            maxVal = item
            index = i
        table.append([f"A{i + 1}", *matrix[i], min(matrix[i]), max(matrix[i]), k*min(matrix[i]) + (1 - k)*max(matrix[i])])
    return table, index
