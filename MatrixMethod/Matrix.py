"""
    Matrix - модуль для решения задач
"""
from math import isclose

import numpy as np



def maxmin(a: np.ndarray):
    return np.max([np.min(i) for i in a])

def minmax(a: np.ndarray):
    return np.min([np.max(i) for i in a.T])


def saddle_point(pay_matrix: np.ndarray) -> float|int|None:
    return minmax(pay_matrix) if minmax(pay_matrix) == maxmin(pay_matrix) else None

# смешанные методы
def MixStrategy(pay_matrix: np.ndarray, A: np.ndarray, B: np.ndarray) -> tuple:
    return A.dot(pay_matrix).dot(B.T)


def incA(a: int) -> str: return f"A{a+1}"
def incB(b: int) -> str: return f"B{b+1}"




# приближенные значения
# на вход таблица типа np.ndarray и кол-во итераций, на выходе таблица с готовым ответом
def ApproximateSolving(pay_matrix: np.ndarray, count_step: int) -> list[list[str]]:
    # список выбранных стратегий игрока А и В
    selected_strategy_a: list[int] = list()
    selected_strategy_b: list[int] = list()


    tmp = np.array([np.min(i) for i in pay_matrix])
    selected_strategy_a.append( int(np.where(np.isclose(tmp, max(tmp)))[0][0]) )
    print(selected_strategy_a)

    tmp = pay_matrix[selected_strategy_a[-1]]
    selected_strategy_b.append( int(np.where(np.isclose(tmp, min(tmp)))[0][0]) )
    print(selected_strategy_b)

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

    


    return [[""]]
