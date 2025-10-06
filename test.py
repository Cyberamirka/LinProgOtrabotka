import numpy as np
from MatrixMethod.Matrix import ApproximateSolving, find_matrix_risk, Bayes_criterion
# from tabulate import tabulate
from pprint import pprint

mtrx = np.array([
    [20, 30, 15],
    [75, 20, 35],
    [25, 80, 25],
    [85, 5, 45]
])


matrix_risk = find_matrix_risk(mtrx)

q = [0.3, 0.2, 0.5]

pprint(Bayes_criterion(mtrx, matrix_risk, q)[0])
pprint(Bayes_criterion(mtrx, matrix_risk, q)[1])


print()
print()

q = [1 / mtrx.shape[1] for i in range(mtrx.shape[1])]
pprint(Bayes_criterion(mtrx, matrix_risk, q)[0])