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

# Alternative numpy solution:
#
# from itertools import count
#
# import aoc_lube
# import numpy as np
# from aoc_lube.utils import Vec2
#
# GRID = np.array([list(line) for line in aoc_lube.fetch(year=2024, day=20).splitlines()])
# DISTANCES = np.zeros_like(GRID, int)
# START = Vec2(*np.argwhere(GRID == "S").flatten().tolist())
# DISTANCES[START] = 1
#
# u = START
# for i in count(2):
#     for adj in u.adj():
#         if GRID[adj] != "#" and DISTANCES[adj] == 0:
#             DISTANCES[adj] = i
#             u = adj
#             break
#     else:
#         break
#
#
# def ncheats(cheat_duration):
#     ys, xs = np.indices(GRID.shape, sparse=True)
#     path_y, path_x = np.where(DISTANCES)
#     distances = np.abs(path_y - ys[..., None]) + np.abs(path_x - xs[..., None])
#     cheat_dist = DISTANCES[..., None] - DISTANCES[path_y, path_x] - distances
#     return (cheat_dist[distances <= cheat_duration] >= 100).sum()
