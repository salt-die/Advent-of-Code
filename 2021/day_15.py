from itertools import product

import networkx as nx

import aoc_helper
from aoc_helper.utils import int_grid, DELTAS_4

def parse_raw():
    grid = int_grid(aoc_helper.day(15))

    G = nx.DiGraph()
    for i, j in product(range(500), repeat=2):
        weight = grid[i % 100, j % 100] + i // 100 + j // 100

        for u, v in DELTAS_4:
            G.add_edge((i + u, j + v), (i , j), weight=weight % 9 or weight)

    return G

CAVE = parse_raw()

def part_one():
    return nx.dijkstra_path_length(CAVE, (0, 0), (99, 99))

def part_two():
    return nx.dijkstra_path_length(CAVE, (0, 0), (499, 499))

aoc_helper.submit(15, part_one)
aoc_helper.submit(15, part_two)
