import tree_set


def best_f_score(open_set):
    """Return the puzzle in the set which has the lowest f_score"""
    return min(open_set, key=lambda x: x.f_score)


def a_star(heuristic, start):
    """A* algorithm

    Takes an heuristic function and an initial state as an input.
    Return the solution to the puzzle, or None if there is no solution
    """
    open_set = {start}
    closed_set = set()

    open_set = tree_set.TreeSet()
    closed_set = tree_set.TreeSet()
    open_set.add(start)

    while open_set:
        e = best_f_score(open_set)
        if e.done():
            return e
        open_set.remove(e)
        for s in e.expand():
            s.g_score = e.g_score + 1
            s.apply_heuristic(heuristic)
            if s in open_set or s in closed_set:
                x = open_set.find_lt(s)
                y = closed_set.find_lt(s)
                if x and y:
                    raise Exception("????????????????")
                if x or y:
                    continue
            open_set.add(s)
        closed_set.add(e)
    return None


import logic
import heuristics

import numpy as np


grid = np.array([[2, 8, 3], [4, 0, 5], [1, 7, 6]])


def display_path(e):
    if e.parent is None:
        return 0
    x = 1 + display_path(e.parent)
    print(e.parent)
    return x


s = logic.Puzzle(grid)
e = a_star(heuristics.manhattan, s)
print("Manhattan distance -")
print("Total # of steps: {}".format(display_path(e)))

print("\n{}\n".format("_" * 80))

s = logic.Puzzle(grid)
e = a_star(heuristics.hamming, s)
print("Hamming distance -")
print("Total # of steps: {}".format(display_path(e)))
