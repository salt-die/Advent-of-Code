import numpy as np
from scipy.ndimage import label

import aoc_helper

CAVE_MAP = aoc_helper.utils.int_grid(aoc_helper.day(9))

def part_one():
    border_map = np.pad(CAVE_MAP, 1, mode="constant", constant_values=9)

    mask = (
          (CAVE_MAP < border_map[2:   , 1: -1])
        & (CAVE_MAP < border_map[ : -2, 1: -1])
        & (CAVE_MAP < border_map[1: -1, 2:   ])
        & (CAVE_MAP < border_map[1: -1,  : -2])
    )
    return (CAVE_MAP[mask] + 1).sum()

def part_two():
    labels, nbins = label(CAVE_MAP != 9)
    labels = labels.reshape(-1)

    return np.partition(np.bincount(labels, labels != 0), nbins - 3)[-3:].prod().astype(int)

aoc_helper.submit(9, part_one)
aoc_helper.submit(9, part_two)

# An alternative solution using networkx:

# from math import prod

# import networkx as nx

# G = nx.grid_graph((100, 100))
# for i in range(100):
#     for j in range(100):
#         G.nodes[i, j]["height"] = CAVE_MAP[i, j]

# def height(node):
#     return G.nodes[node]["height"]

# def part_one():
#     return sum(
#         height(G.nodes[u]) + 1
#         for u in G
#         if all(height(u) < height(v) for v in G[u])
#     )

# def part_two():
#     G.remove_nodes_from([node for node in G if height(node) == 9])

#     return prod(
#         sorted(map(len, nx.connected_components(G)))[-3:]
#     )
