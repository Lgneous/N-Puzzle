import numpy as np


class Puzzle:
    hash = 0

    def __init__(self, grid, parent=None):
        self.grid = np.array(grid)
        self.grid.flags.writeable = (
            False
        )  # required for hashing, also, mutability is never used
        self.k = grid.shape[0]
        (self.y,), (self.x,) = np.where(grid == 0)
        self._true_grid = np.arange(1, self.k * self.k + 1)
        self._true_grid[self.k * self.k - 1] = 0
        self._true_grid.reshape((self.k, self.k))
        self.g_score = 0
        self.h_score = 0
        self.parent = parent

    def done(self):
        return np.array_equal(self.grid, self._true_grid)

    @property
    def f_score(self):
        return self.g_score + self.h_score

    def apply_heuristic(self, f):
        """Apply the heuristic function and set its value to _h_score"""
        self.h_score = f(self.grid, self._true_grid, self.k)

    def expand(self):
        """Return a set of all possible moves represented as copies of self with grid changed"""
        if self.y - 1 >= 0:
            grid = self.grid.copy()
            grid[self.y][self.x] = grid[self.y - 1][self.x]
            grid[self.y - 1][self.x] = 0
            yield Puzzle(grid, self.grid)
        if self.y + 1 < self.k:
            grid = self.grid.copy()
            grid[self.y][self.x] = grid[self.y + 1][self.x]
            grid[self.y + 1][self.x] = 0
            yield Puzzle(grid, self.grid)
        if self.x - 1 >= 0:
            grid = self.grid.copy()
            grid[self.y][self.x] = grid[self.y][self.x - 1]
            grid[self.y][self.x - 1] = 0
            yield Puzzle(grid, self.grid)
        if self.x + 1 < self.k:
            grid = self.grid.copy()
            grid[self.y][self.x] = grid[self.y][self.x + 1]
            grid[self.y][self.x + 1] = 0
            yield Puzzle(grid, self.grid)

    def __str__(self):
        return "{}\nscore: {}".format(self.grid, self.f_score)

    def __eq__(self, other):
        return np.array_equal(self.grid, other.grid)

    def __hash__(self):
        return hash(self.grid.tostring())
