"""
Useful functions for AoC. Note deferred imports.

Requirements:
    * networkx
    * numpy
"""

__all__ = (
    "extract_ints",
    "extract_maze",
    "maximum_matching",
    "get_direction_enum",
    "chinese_remainder_theorem",
    "pairwise",
    "sliding_window",
    "DELTAS_4",
    "DELTAS_5",
    "DELTAS_8",
    "DELTAS_9",
)

DELTAS_4 = (0, 1), (0, -1), (1, 0), (-1, 0)
DELTAS_5 = DELTAS_4 + ((0, 0),)
DELTAS_8 = DELTAS_4 + ((1, 1), (-1, -1), (1, -1), (-1, 1))
DELTAS_9 = DELTAS_8 + ((0, 0),)

def extract_ints(raw: str):
    """
    Extract integers from a string.
    """
    import re

    return map(int, re.findall(r'(-?\d+)', raw))

def extract_maze(raw: str, wall="#", largest_component=False):
    """
    Parse an ascii maze into a networkx graph. Return a tuple `(np.array, nx.Graph)`.
    """
    import numpy as np
    import networkx as nx

    lines = raw.splitlines()
    max_width = max(map(len, lines))
    maze = np.array(
        [list(line + " " * (max_width - len(line))) for line in lines]
    )

    G = nx.grid_graph(maze.shape[::-1])

    walls = np.stack(np.where(maze == wall)).T
    G.remove_nodes_from(map(tuple, walls))

    if largest_component:
        G.remove_nodes_from(G.nodes - max(nx.connected_components(G), key=lambda g: len(g)))

    return maze, G

def maximum_matching(items: dict[list]):
    """
    Return a maximum matching from a dict of lists.
    """
    import networkx as nx

    G = nx.from_dict_of_lists(items)

    for k, v in nx.bipartite.maximum_matching(G, top_nodes=items).items():
        if k in items:  # Filter edges pointing the wrong direction.
            yield k, v

def get_direction_enum():
    """
    Return an enum for Directions with a rotate method.
    """
    from enum import IntEnum

    class Direction(IntEnum):
        EAST  = E = 0
        NORTH = N = 1
        WEST  = W = 2
        SOUTH = S = 3

        def rotate(self, steps=1, clockwise=False):
            if clockwise:
                return Direction((self - steps) % 4)
            return Direction((self + steps) % 4)

    return Direction

def chinese_remainder_theorem(moduli, residues):
    from math import prod

    N = prod(moduli)

    return sum(
        (div := (N // modulus)) * pow(div, -1, modulus) * residue
        for modulus, residue in zip(moduli, residues)
    ) % N

def pairwise(iterable, offset=1):
    """
    Return successive pairs from iterable.
    """
    from itertools import islice, tee

    a, b = tee(iterable)

    return zip(a, islice(b, offset, None))

def sliding_window(iterable, length=2):
    """
    Return a sliding window over iterable.
    """
    from itertools import islice, tee

    its = (
        islice(it, i, None)
        for i, it in enumerate(tee(iterable, length))
    )

    return zip(*its)

def oscillate_range(start=None, stop=None, step=None, /):
    """
    Yield values around start.
    """
    match start, stop, step:
        case (int(), None, None):
            start, stop, step = 0, start, 1 if start > 0 else -1
        case (int(), int(), None):
            step = 1 if start < stop else -1
        case (int(), int(), int()) if step != 0:
            pass
        case _:
            ValueError(f"non-integer values or 0 step ({start=}, {stop=}, {step=})")

    stop_n = (stop - start) // step

    if stop_n <= 0:
        return

    yield start

    n = 1
    while n < stop_n:
        yield start + step * n
        yield start - step * n
        n += 1

def int_grid(raw, np=True, separator=""):
    """
    Parse a grid of ints into a 2d list or numpy array (if np==True).
    """
    array = [
        [int(i) for i in (line.split(separator) if separator else line)]
        for line in raw.splitlines()
    ]

    if np:
        import numpy as np

        return np.array(array)

    return array

def dot_print(array):
    """
    Pretty print a binary or boolean array.
    """
    for row in array:
        print("".join(" #"[i] for i in row))

def shiftmod(n, m, shift=1):
    """
    Simlar to n % m except the result lies within [shift, m + shift).

    Example:
        shiftmod(10, 10, shift=1) == 10
        shiftmod(11, 10, shift=1) == 1
        shiftmod(11, 10, shift=2) == 11
        shiftmod(12, 10, shift=2) == 2
    """
    return (n - shift) % m + shift
