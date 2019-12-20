from collections import defaultdict
from itertools import chain
import networkx as nx
import numpy as np

with open('input20', 'r') as data:
    maze = np.array([list(row.strip('\n')) for row in data])

height, width = maze.shape
G = nx.grid_graph([width, height])

walls = np.vstack(np.where(maze != '.')).T
G.remove_nodes_from(map(tuple, walls)) # Remove walls from graph

def is_portal(portal):
    A, B, C = portal
    return A.isupper() and B.isupper() and C == '.'

mapping = defaultdict(tuple)
maze_iter = np.nditer(maze, flags=['multi_index'])
for char in maze_iter: # This awful loop is just to find indices of portals.
    if str(char).isupper():
        y, x = maze_iter.multi_index
        if y < height - 2 and is_portal((portal := maze[y: y + 3, x])): # Check down
            mapping[''.join(portal[:-1])] += ((y + 2, x), )
        elif y > 1 and is_portal((portal := maze[y: y - 3: -1, x])): # Check up
            mapping[''.join(portal[1::-1])] += ((y - 2, x), )
        elif x < width - 2 and is_portal((portal := maze[y, x: x + 3])): # Check right
            mapping[''.join(portal[:-1])] += ((y, x + 2), )
        elif x > 1 and is_portal((portal := maze[y, x: x - 3: -1])): # Check left
             mapping[''.join(portal[1::-1])] += ((y, x - 2), )

portals = set(chain(*mapping.values()))
while True: # Prune dead-ends and isolated nodes that aren't portals.
    dead = [node for node, degree in nx.degree(G) if node not in portals and degree <= 1]
    if not dead:
        break
    G.remove_nodes_from(dead)

(AA, ), (ZZ, ) = mapping.pop('AA'), mapping.pop('ZZ')
G.add_edges_from(mapping.values())
nx.set_edge_attributes(G, 1, name='weight')
while True: # Contract paths, adding adjacent weights.
    for node, degree in nx.degree(G):
        if degree == 2 and node not in portals:
            (*_, w1), (*_, w2) = G.edges(node, data='weight')
            G.add_edge(*G.neighbors(node), weight=w1 + w2)
            G.remove_node(node)
            break
    else:
        break

print(nx.shortest_paths.dijkstra_path_length(G, AA, ZZ)) # Part 1
G.remove_edges_from(mapping.values())

inner, outer, outer_coords = {}, {}, set((2, height - 3, width - 3))
for portal, nodes in mapping.items():
    for node in nodes:
        (inner if set(node).isdisjoint(outer_coords) else outer)[portal] = node

H = nx.Graph()
for level in range(26):
    for start, end, weight in G.edges(data='weight'):
        H.add_edge((*start, level), (*end, level), weight=weight)
    for portal, location in inner.items():
        H.add_edge((*location, level), (*outer[portal], level + 1), weight=1)

print(nx.shortest_paths.dijkstra_path_length(H, (*AA, 0), (*ZZ, 0))) # Part 2