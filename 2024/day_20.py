from itertools import combinations

import aoc_lube
import networkx as nx
from aoc_lube.utils import extract_maze

_, MAZE, POINTS = extract_maze(aoc_lube.fetch(year=2024, day=20))
SHORTEST_PATH = nx.shortest_path(MAZE, POINTS["S"][0], POINTS["E"][0])
COST_FROM_START = {node: i for i, node in enumerate(SHORTEST_PATH)}
COST_FROM_END = {node: i for i, node in enumerate(reversed(SHORTEST_PATH))}
TARGET_LENGTH = len(SHORTEST_PATH) - 101


def ncheats(cheat_duration):
    return sum(
        COST_FROM_START[u] + manhattan + COST_FROM_END[v] <= TARGET_LENGTH
        for u, v in combinations(SHORTEST_PATH, r=2)
        if (manhattan := abs(v - u)) <= cheat_duration
    )


def part_one():
    return ncheats(2)


def part_two():
    return ncheats(20)


aoc_lube.submit(year=2024, day=20, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=20, part=2, solution=part_two)
