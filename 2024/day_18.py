import aoc_lube
import networkx as nx
import numpy as np
from aoc_lube.utils import extract_ints

BYTES = np.fromiter(
    extract_ints(aoc_lube.fetch(year=2024, day=18)),
    int,
).reshape(-1, 2)


def to_graph(i):
    g = nx.grid_graph((71, 71))
    g.remove_nodes_from(map(tuple, BYTES[:i]))
    return g


def part_one():
    return nx.shortest_path_length(to_graph(1024), (0, 0), (70, 70))


def part_two():
    lo = 1024
    hi = len(BYTES)
    while lo < hi:
        mid = (lo + hi) // 2
        if nx.has_path(to_graph(mid), (0, 0), (70, 70)):
            lo = mid + 1
        else:
            hi = mid
    x, y = BYTES[mid]
    return f"{x},{y}"


aoc_lube.submit(year=2024, day=18, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=18, part=2, solution=part_two)


# Alternative Part 2 with Union Find:
# from itertools import count
#
# import aoc_lube
# from aoc_lube.utils import UnionFind, Vec2, chunk, extract_ints
#
# BYTES = [
#     Vec2(y, x) for x, y in chunk(extract_ints(aoc_lube.fetch(year=2024, day=18)), 2)
# ]
#
#
# def part_two():
#     uf = UnionFind()
#     uf.add("tr")
#     uf.add("bl")
#     for i in count():
#         pos = BYTES[i]
#         uf.add(pos)
#         if pos.x == 70 or pos.y == 0:
#             uf.merge(pos, "tr")
#         if pos.x == 0 or pos.y == 70:
#             uf.merge(pos, "bl")
#         for adj in pos.adj(8):
#             if adj in uf:
#                 uf.merge(adj, pos)
#         if uf.find("tr") == uf.find("bl"):
#             return f"{pos.x},{pos.y}"
