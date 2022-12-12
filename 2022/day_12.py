import numpy as np
import networkx as nx

import aoc_lube
from aoc_lube.utils import Deltas, inbounds_steps

def parse_raw():
    lines = aoc_lube.fetch(year=2022, day=12).splitlines()
    grid = np.array([[ord(c) for c in line] for line in lines])

    start = tuple(np.argwhere(grid == ord('S'))[0])
    grid[start] = ord('a')

    end = tuple(np.argwhere(grid == ord('E'))[0])
    grid[end] = ord('z')

    lowest = np.argwhere(grid == ord('a'))

    G = nx.DiGraph()
    for old, new in inbounds_steps(Deltas.FOUR, *grid.shape):
        if grid[new] - grid[old] <= 1:
            G.add_edge(old, new)

    return G, start, end, lowest

G, start, end, lowest = parse_raw()

def part_one():
    return nx.shortest_path_length(G, start, end)

def part_two():
    lengths = dict(nx.single_target_shortest_path_length(G, end))
    return min(lengths.get((y, x), float("inf")) for y, x in lowest)

aoc_lube.submit(year=2022, day=12, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=12, part=2, solution=part_two)
