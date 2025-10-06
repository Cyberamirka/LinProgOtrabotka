import numpy as np


class ApproximateResult:
    def __init__(self):
        self.table: np.ndarray = np.array([])
        self.count_clean_strategy_a: np.ndarray = np.array([])
        self.count_clean_strategy_b: np.ndarray = np.array([])
        self.frequency_a: np.ndarray = np.array([])
        self.frequency_b: np.ndarray = np.array([])
        self.price: float = 0