import numpy as np


def run(start, heuristic):
    start.apply_heuristic(heuristic)
    bound = start.f_score
    while True:
        t, p = search(start, 0, bound, heuristic)
        if t == np.inf:
            return None, 0, 0
        if t == -1:
            return p, 0, 0
        bound = t


def search(node, g, bound, heuristic):
    node.g_score = g
    if node.f_score > bound:
        return node.f_score, node
    if node.done():
        return -1, node
    min_cost = np.inf
    for succ in node.expand():
        if succ not in node:
            succ.apply_heuristic(heuristic)
            t, path = search(succ, g + 1, bound, heuristic)
            if t == -1:
                return t, path
            if t < min_cost:
                min_cost = t
    return min_cost, node
