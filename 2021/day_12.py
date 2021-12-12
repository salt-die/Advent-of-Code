from itertools import combinations_with_replacement

import networkx as nx

import aoc_helper

CAVES = nx.MultiGraph(line.split("-") for line in aoc_helper.day(12).splitlines())

# For each big_cave in _BIG_CAVES and for each u, v in the neighborhood of big_cave,
# add an edge (u, v) to CAVES. Afterwards, remove all big caves.  The remaining
# edges between the small caves now have multiplicity that can be used to count paths.
_BIG_CAVES = list(filter(str.isupper, CAVES))

CAVES.add_edges_from(
    edge
    for big_cave in _BIG_CAVES
    for edge in combinations_with_replacement(CAVES[big_cave], 2)
)
CAVES.remove_nodes_from(_BIG_CAVES)

def npaths(u, revisited, seen=()):
    return u == "end" or sum(
        len(CAVES[u][v]) * npaths(v, revisited | (v in seen), {*seen, v})
        for v in CAVES[u]
        if v != "start"
        if not revisited or v not in seen
    )

def part_one():
    return npaths("start", True)

def part_two():
    return npaths("start", False)

aoc_helper.submit(12, part_one)
aoc_helper.submit(12, part_two)
