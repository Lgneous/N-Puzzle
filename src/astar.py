from functools import reduce


def best_f(open_set):
    """Returns the puzzle in the set which has the lowest f_score"""
    return min(open_set, key=lambda x: x.f_score)


def a_star(heuristic, start):
    """A* algorithm

    Takes an heuristic function and an initial state as an input.
    Return the solution to the puzzle, or None if there is no solution
    """
    open_set = {start}
    closed_set = set()

    while open_set:
        e = best_f(open_set)
        print(e)
        if e.done():
            return e
        open_set.remove(e)
        closed_set.add(e)
        for s in e.expand(closed_set):
            if s in closed_set:
                continue
            g_score = s.g_score + 1
            if s in open_set:
                if g_score < s.g_score:
                    s.g_score = g_score
                    s.parent = e
            else:
                s.g_score = g_score
                s.apply_heuristic(heuristic)
                s.parent = e
                open_set.add(s)


import logic
import heuristics

import numpy as np


grid = np.array([[1, 4, 7], [6, 0, 3], [5, 2, 8]])
s = logic.Puzzle(grid)
final_state = a_star(heuristics.manhattan, s)
t = final_state.parent
nmoves = 0
while t:
    nmoves += 1
    print(t.grid)
    t = t.parent
print("Length: " + str(nmoves))
