import numpy as np


def hamming(grid, true_grid, k):
    _grid = grid != true_grid
    _grid[true_grid == 0] = False
    return np.count_nonzero(_grid)


def manhattan(grid, true_grid, k):
    return 0
