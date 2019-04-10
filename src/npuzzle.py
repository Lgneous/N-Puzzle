import argparse

import a_star
import heuristics
import ida_star
import reader
import ucs

HEURISTICS_TABLE = {"manhattan": heuristics.manhattan,
                    "hamming": heuristics.hamming,
                    "nilsson": heuristics.nilsson}


ALGORITHM_TABLE = {"a_star": a_star.run, "ida": ida_star.run,
                   "uniform": ucs.run}


def display_path(node):
    accumulator = []
    length = 0
    while node:
        accumulator.append(str(node))
        node = node.parent
        length += 1
    print("\n\n".join(accumulator[::-1]))
    return length


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python3 npuzzle.py", description="Solve the n-puzzle problem"
    )
    parser.add_argument("file", metavar="FILE")
    parser.add_argument(
        "-H",
        "--heuristic",
        default="manhattan",
        choices=HEURISTICS_TABLE.keys(),
    )
    parser.add_argument("-a", "--algorithm", default="a_star",
                        choices=ALGORITHM_TABLE.keys())
    parser.add_argument("-g", "--greedy", action="store_true")
    args = parser.parse_args()
    filename = args.file
    heuristic = HEURISTICS_TABLE[args.heuristic]
    algo = ALGORITHM_TABLE[args.algorithm]
    is_greedy = args.greedy
    try:
        with open(filename) as f:
            start = reader.parse(f)
        goal, time_comp, space_comp = algo(start, heuristic, greedy=is_greedy)
        if goal is None:
            print("Invalid puzzle")
        else:
            print("Length of path: {}".format(display_path(goal)))
        print("Time complexity: {}".format(time_comp))
        print("Space complexity: {}".format(space_comp))
    except (RecursionError, MemoryError):
        print(
            "Memory usage too high: consider using IDA* algorithm (python3 npuzzle.py -a ida FILE), may take more time than usual"
        )
    except Exception as e:
        print(e)
