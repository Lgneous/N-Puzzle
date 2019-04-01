import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python3 npuzzle.py", description="Solve the n-puzzle problem"
    )
    parser.add_argument("-f", "--file", metavar="FILE")
    parser.add_argument("-H", "--heuristic", metavar="NAME")
    parser.parse_args()
