from functools import lru_cache
import string
import networkx as nx
import numpy as np

with open('input18', 'r') as data:
    maze = np.array([list(row.strip()) for row in data])

G = nx.grid_graph(list(maze.T.shape))

walls = np.vstack(np.where(maze == '#')).T
G.remove_nodes_from(map(tuple, walls)) # Remove walls from graph

mapping = {node: name for node in G if (name := str(maze[node])) != '.'}
G = nx.relabel_nodes(G, mapping, copy=False) # Nodes are named after their keys

while True: # Prune dead-ends without keys
    dead = [node for node, degree in nx.degree(G) if degree == 1 and not isinstance(node, str)]
    if not dead:
        break
    G.remove_nodes_from(dead)

nx.set_edge_attributes(G, 1, name='weight')
while True: # Contract paths, adding adjacent weights
    for node, degree in nx.degree(G):
        if degree == 2 and not isinstance(node, str):
            (*_, w1), (*_, w2) = G.edges(node, data='weight')
            G.add_edge(*G.neighbors(node), weight=w1 + w2)
            G.remove_node(node)
            break
    else:
        break

# At this point maze is very small with 75 nodes and 78 edges.
KEYS = set(string.ascii_lowercase)
DOORS = set(string.ascii_uppercase)

@lru_cache(maxsize=None)
def reachable(start, keys):
    """
    Return a dictionary of {reachable_key: distance, keys + keys on path} from start
    given keys.
    """
    reachable_keys = {}
    for key in KEYS:
        if key not in keys:
            try: # Added for part 2
                distance, path = nx.shortest_paths.single_source_dijkstra(G, start, key)
            except nx.NetworkXNoPath:
                continue
            new_keys = set(keys)
            for node in path:
                if node in KEYS:
                    new_keys.add(node)
                elif node in DOORS and node.lower() not in new_keys:
                    break
            else:
                reachable_keys[key] = distance, ''.join(sorted(new_keys))
    return reachable_keys

@lru_cache(maxsize=None)
def best_walk(start='@', keys=''):
    if not (paths := reachable(start, keys)):
        return 0
    return min(distance + best_walk(key, new_keys) for key, (distance, new_keys) in paths.items())

print(best_walk()) # Part 1: 4700

# Split Graph into 4 components and relabel new entrances.
mapping = {(39, 39): '@1', (39, 41): '@2', (41, 39): '@3', (41, 41): '@4'} # Found by inspection.
G = nx.relabel_nodes(G, mapping, copy=False)
G.remove_nodes_from(list(G.neighbors('@')) + ['@'])

@lru_cache(maxsize=None)
def reachable_by_robot(starts, keys):
    can_reach = {}
    for robot, start in enumerate(starts):
        for key, (distance, new_keys) in reachable(start, keys).items():
            can_reach[key] = distance, new_keys, robot
    return can_reach

@lru_cache(maxsize=None)
def new_starts(starts, key, robot):
    return tuple(start if robot != i else key for i, start in enumerate(starts))

@lru_cache(maxsize=None)
def best_walk_robots(starts=('@1', '@2', '@3', '@4'), keys=''): # Nearly identical to best_walk
    if not (paths := reachable_by_robot(starts, keys)):
        return 0
    return min(distance + best_walk_robots(new_starts(starts, key, robot), new_keys)
               for key, (distance, new_keys, robot) in paths.items())

reachable.cache_clear() # Graph changed, need to clear cache
print(best_walk_robots()) # Part 2: 2260