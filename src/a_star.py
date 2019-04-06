import tree_set


def best_f_score(open_set):
    """Return the puzzle in the set which has the lowest f_score"""
    return min(open_set, key=lambda x: x.f_score)


def run(start, heuristic):
    """A* algorithm

    Takes an heuristic function and an initial state as an input.
    Return the solution to the puzzle, or None if there is no solution
    """
    start.apply_heuristic(heuristic)

    open_set = tree_set.TreeSet()
    closed_set = tree_set.TreeSet()
    open_set.add(start)

    time_comp = 1
    space_comp = 1

    while open_set:
        e = best_f_score(open_set)
        if e.done():
            return e, time_comp, space_comp
        time_comp += 1
        open_set.remove(e)
        for s in e.expand():
            s.g_score = e.g_score + 1
            s.apply_heuristic(heuristic)
            if s in open_set or s in closed_set:
                x = open_set.find_lt(s)
                y = closed_set.find_lt(s)
                if x or y:
                    continue
            open_set.add(s)
            space_comp = max(len(open_set), space_comp)
        closed_set.add(e)
    return None, time_comp, space_comp