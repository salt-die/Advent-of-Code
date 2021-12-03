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
)

def extract_ints(raw: str):
    """
    Extract integers from a string.
    """
    import re

    for match in re.findall(r'(\d+)', raw):
        yield int(match)

def extract_maze(raw: str, empty_cell=".", largest_component=False):
    """
    Parse an ascii maze into a networkx graph. Return a tuple `(np.array, nx.Graph)`.
    """
    import numpy as np
    import networkx as nx

    maze = np.array(
        [[*line] for line in raw.splitlines()]
    )

    G = nx.grid_graph(maze.shape[::-1])

    walls = np.stack(np.where(maze != empty_cell)).T
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
