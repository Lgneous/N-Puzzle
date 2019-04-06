import numpy as np


class Puzzle:
    def __init__(self, grid, parent=None, move="ORIGIN", goal=None):
        self.grid = np.array(grid)
        # required for hashing, also, mutability is never used
        self.grid.flags.writeable = False
        self.k = grid.shape[0]
        (self.y,), (self.x,) = np.where(grid == 0)
        if goal is None:
            self._goal = np.array(Puzzle.make_goal(self.k))
            self._goal = self._goal.reshape((self.k, self.k))
        else:
            self._goal = goal
        self.h_score = 0
        self.g_score = 0
        self.parent = parent
        self.move = move

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
        return np.array_equal(self.grid, self._goal)

    @property
    def f_score(self):
        return self.g_score + self.h_score

    def apply_heuristic(self, f):
        """Apply the heuristic function and set its value to _h_score"""
        self.h_score = f(self.grid, self._goal)

    def expand(self):
        """Yield all possible moves represented as copies of self with grid changed"""
        if self.y - 1 >= 0:
            grid = self.grid.copy()
            grid[self.y, self.x] = grid[self.y - 1, self.x]
            grid[self.y - 1, self.x] = 0
            yield Puzzle(grid, self, "UP", self._goal)
        if self.y + 1 < self.k:
            grid = self.grid.copy()
            grid[self.y, self.x] = grid[self.y + 1, self.x]
            grid[self.y + 1, self.x] = 0
            yield Puzzle(grid, self, "DOWN", self._goal)
        if self.x - 1 >= 0:
            grid = self.grid.copy()
            grid[self.y][self.x] = grid[self.y, self.x - 1]
            grid[self.y][self.x - 1] = 0
            yield Puzzle(grid, self, "LEFT", self._goal)
        if self.x + 1 < self.k:
            grid = self.grid.copy()
            grid[self.y, self.x] = grid[self.y, self.x + 1]
            grid[self.y, self.x + 1] = 0
            yield Puzzle(grid, self, "RIGHT", self._goal)

    def __str__(self):
        return "-- {} --\n{}".format(self.move, "\n".join(str(s) for s in self.grid))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return np.array_equal(self.grid, other.grid)

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return hash(self) <= hash(other)

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __ge__(self, other):
        return hash(self) >= hash(other)

    def __contains__(self, other):
        if self == other:
            return True
        if self.parent is None:
            return False
        return other in self.parent

    def __hash__(self):
        """Complex hash for set usage, f-score added for ordering in tree with
        comparison function
        """
        return hash(self.grid.tostring()) + self.f_score
