import aoc_lube
import networkx as nx
import numpy as np
from aoc_lube.utils import extract_maze

GRID, MAZE = extract_maze(aoc_lube.fetch(year=2024, day=20))
S = tuple(np.argwhere(GRID == "S").reshape(-1).tolist())
E = tuple(np.argwhere(GRID == "E").reshape(-1).tolist())
TARGET_LENGTH = nx.shortest_path_length(MAZE, S, E) - 100


def ncheats(cheat_duration):
    cost_from_start = nx.shortest_path_length(MAZE, S)
    cost_from_end = nx.shortest_path_length(MAZE, E)
    total = 0
    for (y1, x1), start_cost in cost_from_start.items():
        for (y2, x2), end_cost in cost_from_end.items():
            manhattan = abs(y2 - y1) + abs(x2 - x1)
            if manhattan <= cheat_duration:
                total += start_cost + manhattan + end_cost <= TARGET_LENGTH
    return total


def part_one():
    return ncheats(2)


def part_two():
    return ncheats(20)


aoc_lube.submit(year=2024, day=20, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=20, part=2, solution=part_two)
