import numpy as np


def hamming(grid, goal):
    """Hamming distance, return the number of element in grid different than goal"""
    _grid = grid != goal
    _grid[goal == 0] = False
    return np.count_nonzero(_grid)


def manhattan(grid, goal, cache=[]):
    def populate(goal, cache):
        cache.append(np.zeros_like(goal))
        k = goal.shape[0]

        def _move(y, x):
            yield max(0, y - 1), x
            yield y + 1, x
            yield y, max(0, x - 1)
            yield y, x + 1

        def _populate(coord, v=1):
            if weights[coord] == -1:
                weights[coord] = 0
            for y, x in _move(*coord):
                try:
                    if weights[y, x] == -1 or v < weights[y, x]:
                        weights[y, x] = v
                        _populate((y, x), v + 1)
                except IndexError:
                    pass

        for i in range(1, k * k):
            weights = np.full_like(goal, -1)
            (y,), (x,) = np.where(goal == i)
            _populate((y, x))
            cache.append(weights)

    if not cache:
        populate(goal, cache)

    return int(np.sum(cache[e][coord] for coord, e in np.ndenumerate(grid)))
