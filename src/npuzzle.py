import argparse

import a_star
import heuristics
import reader

HEURISTICS_TABLE = {"manhattan": heuristics.manhattan, "hamming": heuristics.hamming}
ALGORITHM_TABLE = {"a_star": a_star.run}


def display_path(node):
    if node is None:
        return -1
    x = 1 + display_path(node.parent)
    print(node, end="\n\n")
    return x


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python3 npuzzle.py", description="Solve the n-puzzle problem"
    )
    parser.add_argument("file", metavar="FILE")
    parser.add_argument("-H", "--heuristic", metavar="NAME", default="manhattan")
    parser.add_argument("-a", "--algorithm", default="a_star")
    args = parser.parse_args()
    filename = args.file
    heuristic = HEURISTICS_TABLE[args.heuristic]
    algo = ALGORITHM_TABLE[args.algorithm]
    with open(filename) as f:
        start = reader.parse(f)
    goal, time_comp, space_comp = algo(start, heuristic)
    if goal is None:
        print("Invalid puzzle")
    else:
        print("Length of path: {}".format(display_path(goal)))
    print("Time complexity: {}".format(time_comp))
    print("Space complexity: {}".format(space_comp))
