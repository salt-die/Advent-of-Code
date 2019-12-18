from functools import lru_cache
import string
import networkx as nx
import numpy as np

with open('input18', 'r') as data:
    maze = np.array([list(row.strip()) for row in data])

G = nx.grid_graph(list(maze.shape))

walls = np.vstack(np.where(maze == '#')).T
for coordinate in walls: # Remove walls from graph
    G.remove_node(tuple(coordinate))

mapping = {node: name for node in G if (name := str(maze[node])) != '.'}
G = nx.relabel_nodes(G, mapping, copy=False) # Nodes are named after their keys

###### This section isn't necessary, but greatly reduces the size of our maze.######
while True: # Prune dead-ends without keys
    for node, degree in nx.degree(G):
        if degree == 1 and not isinstance(node, str):
            G.remove_node(node)
            break
    else:
        break

nx.set_edge_attributes(G, 1, name='weight')
while True: # Contract paths, adding adjacent weights
    for node, degree in nx.degree(G):
        if degree == 2 and not isinstance(node, str):
            weight = sum(weight for _, _, weight in G.edges(node, data='weight'))
            G.add_edge(*G.neighbors(node), weight=weight)
            G.remove_node(node)
            break
    else:
        break
###################################################################################

# At this point maze is very small with 75 nodes and 78 edges.
KEYS = set(string.ascii_lowercase)
DOORS = set(string.ascii_uppercase)

@lru_cache(maxsize=None)
def reachable(node, keys):
    """
    Return a dictionary of {reachable_key: distance, keys + keys on path} from node
    given keys.
    """
    can_reach = {}
    for key in KEYS:
        if key not in keys:
            try: # Added for part 2
                distance, path = nx.shortest_paths.single_source_dijkstra(G, node, key)
            except nx.NetworkXNoPath:
                continue
            new_keys = set(keys)
            for cell in path:
                if cell in KEYS:
                    new_keys.add(cell)
                if cell in DOORS and cell.lower() not in new_keys:
                    break
            else:
                can_reach[key] = distance, ''.join(new_keys)
    return can_reach

@lru_cache(maxsize=None)
def best_walk(node, keys):
    keys = ''.join(sorted(keys))

    if not (possible_walks := reachable(node, keys)):
        return 0

    distances = []
    for key, (distance, new_keys) in possible_walks.items():
        distances.append(distance + best_walk(key, new_keys))
    return min(distances)

print(best_walk(node='@', keys='')) # Part 1: 4700

# Split Graph into 4 components and relabel new entrances.
mapping = {(39, 39): '@1', (39, 41): '@2', (41, 39): '@3', (41, 41): '@4'} # Found by inspection.
G = nx.relabel_nodes(G, mapping, copy=False)
for node in list(G.neighbors('@')):
    G.remove_node(node)
G.remove_node('@')

@lru_cache(maxsize=None)
def reachable_by_robot(nodes, keys):
    can_reach = {}
    for robot, node in enumerate(nodes):
        for key, (distance, new_keys) in reachable(node, keys).items():
            can_reach[key] = distance, new_keys, robot
    return can_reach

@lru_cache(maxsize=None)
def best_walk_robots(nodes, keys): # Nearly identical to best_walk
    keys = ''.join(sorted(keys))

    if not (possible_walks := reachable_by_robot(nodes, keys)):
        return 0

    distances = []
    for key, (distance, new_keys, robot) in possible_walks.items():
        new_nodes = tuple(node if robot != i else key for i, node in enumerate(nodes))
        distances.append(distance + best_walk_robots(new_nodes, new_keys))
    return min(distances)

reachable.cache_clear() # Graph changed, need to clear cache
print(best_walk_robots(nodes=('@1','@2','@3','@4'), keys='')) # Part 2: 2260