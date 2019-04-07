import heapq


def run(start, heuristic, greedy=False):
    """Run the a* algorithm

    :param start: Initial puzzle
    :param heuristic: Heuristic function that will be used to compute f scores
    :returns: Final puzzle, time complexity and space complexity
    :rtype: Puzzle, int, int

    """
    start.apply_heuristic(heuristic)
    open_set = {start}
    closed_set = set()

    heap = []
    heapq.heappush(heap, (start.f_score, start))

    time_comp = 0
    space_comp = 0

    g_inc = int(not greedy)

    while open_set:
        _, e = heapq.heappop(heap)
        closed_set.add(e)
        if e.done():
            return e, time_comp, space_comp
        open_set.remove(e)
        for s in e.expand():
            if s not in closed_set:
                s.apply_heuristic(heuristic)
                s.g_score = e.g_score + g_inc
                if s not in open_set:
                    open_set.add(s)
                    space_comp = max(len(open_set), len(closed_set), space_comp)
                    heapq.heappush(heap, (s.f_score, s))
                    time_comp += 1
    return None, time_comp, space_comp
