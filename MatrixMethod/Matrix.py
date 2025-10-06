"""
    Matrix - модуль для решения задач
"""

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


# приближенные значения
# на вход таблица типа np.ndarray и кол-во итераций, на выходе таблица с готовым ответом
def ApproximateSolving(pay_matrix: np.ndarray, count_step: int) -> list[list[str]]:
    # последне использованная стратегия А
    last_a_strategy: list = list()
    # последне использованная стратегия В
    last_b_strategy: list = list()

    # список выбранных стратегий игрока А и В
    selected_strategy_a: list = list()
    selected_strategy_b: list = list()

    # приближенные значения игры
    vn: list = list()
    v_n: list = list()
    avg_v_n: list = list()





