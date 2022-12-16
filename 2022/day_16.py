import re
from functools import cache

import aoc_lube
import networkx as nx

def parse_raw():
    parsed = re.findall(
        r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)",
        aoc_lube.fetch(year=2022, day=16),
    )
    G = nx.DiGraph()
    valves = {}
    for tunnel, flow, neighbors in parsed:
        if flow != "0":
            valves[tunnel] = int(flow)
        for neighbor in neighbors.split(", "):
            G.add_edge(tunnel, neighbor)

    return dict(nx.all_pairs_shortest_path_length(G)), valves

PATH_LENGTHS, FLOWS = parse_raw()

@cache
def dfs(time, source='AA', closed=frozenset(FLOWS), elephant=False):
    max_released = dfs(26, closed=closed) if elephant else 0
    for target in closed:
        if (length := PATH_LENGTHS[source][target]) < time:
            time_left = time - length - 1
            released = FLOWS[target] * time_left + dfs(time_left, target, closed - {target}, elephant)
            max_released = max(max_released, released)
    return max_released

def part_one():
    return dfs(30)

def part_two():
    return dfs(26, elephant=True)

aoc_lube.submit(year=2022, day=16, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=16, part=2, solution=part_two)
