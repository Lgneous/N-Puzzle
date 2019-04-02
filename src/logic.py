import numpy as np


class Puzzle:
    def __init__(self, grid, parent=None):
        self.grid = np.array(grid)
        # required for hashing, also, mutability is never used
        self.grid.flags.writeable = False
        self.k = grid.shape[0]
        (self.y,), (self.x,) = np.where(grid == 0)
        self._true_grid = np.array(Puzzle.make_goal(self.k))
        self._true_grid = self._true_grid.reshape((self.k, self.k))
        self.h_score = 0
        self.g_score = 0
        self.parent = parent

    @staticmethod
    def make_goal(s):
        ts = s * s
        puzzle = [-1 for i in range(ts)]
        cur = 1
        x = 0
        ix = 1
        y = 0
        iy = 0
        while True:
            puzzle[x + y * s] = cur
            if cur == 0:
                break
            cur += 1
            if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * s] != -1):
                iy = ix
                ix = 0
            elif (
                y + iy == s
                or y + iy < 0
                or (iy != 0 and puzzle[x + (y + iy) * s] != -1)
            ):
                ix = -iy
                iy = 0
            x += ix
            y += iy
            if cur == s * s:
                cur = 0
        return puzzle

    def done(self):
        return np.array_equal(self.grid, self._true_grid)

    @property
    def f_score(self):
        return self.g_score + self.h_score

    def apply_heuristic(self, f):
        """Apply the heuristic function and set its value to _h_score"""
        self.h_score = f(self.grid, self._true_grid, self.k)

    def expand(self):
        """Yield all possible moves represented as copies of self with grid changed"""
        if self.y - 1 >= 0:
            grid = self.grid.copy()
            grid[self.y, self.x] = grid[self.y - 1, self.x]
            grid[self.y - 1, self.x] = 0
            yield Puzzle(grid, self)
        if self.y + 1 < self.k:
            grid = self.grid.copy()
            grid[self.y, self.x] = grid[self.y + 1, self.x]
            grid[self.y + 1, self.x] = 0
            yield Puzzle(grid, self)
        if self.x - 1 >= 0:
            grid = self.grid.copy()
            grid[self.y][self.x] = grid[self.y, self.x - 1]
            grid[self.y][self.x - 1] = 0
            yield Puzzle(grid, self)
        if self.x + 1 < self.k:
            grid = self.grid.copy()
            grid[self.y, self.x] = grid[self.y, self.x + 1]
            grid[self.y, self.x + 1] = 0
            yield Puzzle(grid, self)

    def __str__(self):
        return "{} - {}".format(self.grid, self.f_score)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        """Compare the 2 grids"""
        return np.array_equal(self.grid, other.grid)

    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        return hash(self) <= hash(other)

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __ge__(self, other):
        return hash(self) >= hash(other)

    def __hash__(self):
        """Complex hash for set usage, f-score added for ordering in tree with comparison functions"""
        return hash(self.grid.tostring()) + self.f_score
