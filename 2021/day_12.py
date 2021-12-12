from itertools import combinations_with_replacement

import networkx as nx

import aoc_helper

def small_caves_multigraph():
    """
    For each `big_cave` in `big_caves` and for each u, v in the neighborhood of `big_cave`,
    add an edge (u, v) to `caves`. Afterwards, remove all big caves.  The remaining
    edges between the small caves now have multiplicity that can be used to count paths.
    """
    caves = nx.MultiGraph(line.split("-") for line in aoc_helper.day(12).splitlines())

    big_caves = list(filter(str.isupper, caves))

    caves.add_edges_from(
        edge
        for big_cave in big_caves
        for edge in combinations_with_replacement(caves[big_cave], 2)
    )

    caves.remove_nodes_from(big_caves)

    return caves

CAVES = small_caves_multigraph()

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
