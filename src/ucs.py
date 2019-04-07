import a_star


def run(start, _, greedy=False):
    heuristic = lambda *args, **kwargs: 0
    return a_star.run(start, heuristic, greedy)
