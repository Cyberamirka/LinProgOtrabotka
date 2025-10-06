import numpy as np
from MatrixMethod.Matrix import ApproximateSolving



PayMatrix = np.array([
    [4, 2, 2],
    [2, 5, 0],
    [0, 2, 5]
])

ApproximateSolving(PayMatrix, 5)