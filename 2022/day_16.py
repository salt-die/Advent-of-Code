import re
from functools import cache

import aoc_lube
import networkx as nx

def parse_raw():
    parsed = re.findall(
        r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)",
        aoc_lube.fetch(year=2022, day=16),
    )
    tunnels = nx.DiGraph()
    flows = {}
    for tunnel, flow, neighbors in parsed:
        if flow != "0":
            flows[tunnel] = int(flow)
        for neighbor in neighbors.split(", "):
            tunnels.add_edge(tunnel, neighbor)

    return dict(nx.all_pairs_shortest_path_length(tunnels)), flows

DISTANCES, FLOWS = parse_raw()

def _dfs(time, source, closed, leftover):
    for target in closed:
        if DISTANCES[source][target] < time:
            time_left = time - DISTANCES[source][target] - 1
            yield FLOWS[target] * time_left + dfs(time_left, target, closed - {target}, leftover)

@cache
def dfs(time, source='AA', closed=frozenset(FLOWS), leftover=0):
    if len(closed) == leftover:
        return dfs(26, closed=closed)
    return max(_dfs(time, source, closed, leftover), default=0)

def part_one():
    return dfs(30)

def part_two():
    return dfs(26, leftover=9)

aoc_lube.submit(year=2022, day=16, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=16, part=2, solution=part_two)
