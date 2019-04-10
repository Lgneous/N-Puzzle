import a_star


def run(start, _, greedy=False):
    def heuristic(*_, **__):
        return 0
    return a_star.run(start, heuristic, greedy)
