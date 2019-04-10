import numpy as np

import puzzle


def parse(f):
    """Read a file and return the corresponding grid

    :param f: File object to read from
    :returns: Corresponding grid read from f
    :rtype: Puzzle

    """
    n = -1
    k = -1
    grid = []
    for line in f:
        line_ = line.split("#")[0].strip()
        if not line_:
            continue
        if not n:
            raise SyntaxError("Too many rows: {}".format(line))
        if n == -1:
            n = int(line)
            if n < 1:
                raise ValueError("Size of puzzle must be positive")
            k = n
            continue
        row = line_.split()
        if len(row) != k:
            raise SyntaxError("Too many columns: {}".format(line))
        grid.append([int(x) for x in row])
    final_grid = np.array(grid)
    if not np.array_equal(np.sort(final_grid.flatten()), np.arange(k ** 2)):
        raise ValueError("Invalid grid:\n{}".format("\n".join(str(s) for s in grid)))
    return puzzle.Puzzle(np.array(grid))
