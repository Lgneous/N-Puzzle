import numpy as np


def run(start, heuristic, greedy=False):
    """Iterative deepening a* algorithm

    :param start: Initial puzzle
    :param heuristic: Heuristic function that will be used to compute f scores
    :returns: Final puzzle, time complexity and space complexity
    :rtype: Puzzle, int, int

    """

    g_inc = int(not greedy)

    start.apply_heuristic(heuristic)
    path = {start}
    bound = start.f_score

    time_comp = 1
    space_comp = 1

    def search(e, g_score, bound):
        nonlocal time_comp, space_comp
        time_comp += 1
        e.g_score = g_score
        if e.f_score > bound:
            return e.f_score, e
        if e.done():
            return -1, e
        cost = np.inf
        for s in e.expand():
            if s not in path:
                path.add(s)
                space_comp = max(space_comp, len(path))
                s.apply_heuristic(heuristic)
                s_score, t = search(s, g_score + g_inc, bound)
                if s_score == -1:
                    return s_score, t
                if s_score < cost:
                    cost = s_score
                path.remove(s)
        return cost, e

    while True:
        score, node = search(start, 0, bound)
        if np.isinf(score):
            return None, 0, 0
        if score == -1:
            return node, time_comp, space_comp
        bound = score
