import heapq
import itertools

import numpy as np


def hamming(grid, goal):
    """Hamming distance, number of element in grid different than goal

    :param grid: Puzzle to be tested
    :param goal: Goal puzzle
    :returns: Hamming distance between goal and grid
    :rtype: int

    """
    _grid = grid != goal
    _grid[goal == 0] = False
    return np.count_nonzero(_grid)


def manhattan(grid, goal, cache=[]):
    """Manhattan distance, cached

    :param grid: Puzzle to be tested
    :param goal: Goal puzzle
    :param cache: Weight matrix, cached
    :returns: L1 distance between goal and grid
    :rtype: int

    """

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


def nilsson(grid, goal, cache=[]):
    """Nilsson heuristic, cached

    Computes the amount of cell not followed by their successor * 3,
    This is called the s_score.

    :param grid: Puzzle to be tested
    :param goal: Goal puzzle
    :param cache: Coordinate list, cached
    :returns: Manhattan + s_score
    :rtype: int

    """
    k = grid.shape[0]

    def cache_coord():
        def _gen():
            for i in range(k * k):
                (y,), (x,) = np.where(goal == k)
                (y_,), (x_,) = np.where(goal == k + 1)
                yield (y, x), (y_, x_)
            yield (y_, x_), (0, 0)
        for coord in _gen():
            cache.append(coord)

    if not cache:
        cache_coord()

    score = 0
    max_k = k * k - 1

    for c1, c2 in cache:
        if grid[c1] == max_k:
            score += 3
        elif grid[c1] != (grid[c2] + 1) % max_k:
            score += 6

    return manhattan(grid, goal) + score
