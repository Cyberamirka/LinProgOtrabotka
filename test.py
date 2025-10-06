import numpy as np
from MatrixMethod.Matrix import ApproximateSolving
from tabulate import tabulate


PayMatrix = np.array([
    [4, 1, 3],
    [2, 5, 2]
])

table = ApproximateSolving(PayMatrix, 20).tolist()
print(tabulate(table[1:], headers=table[0]))