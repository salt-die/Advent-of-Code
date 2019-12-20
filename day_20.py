from collections import defaultdict
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
        # Check down:
        if y < height - 2 and is_portal((portal := maze[y: y + 3, x])):
            mapping[''.join(portal[:-1])] += ((y + 2, x), )
        # Check up:
        elif y > 1 and is_portal((portal := maze[y: y - 3: -1, x])):
            mapping[''.join(portal[1::-1])] += ((y - 2, x), )
        # Check right:
        elif x < width - 2 and is_portal((portal := maze[y, x: x + 3])):
            mapping[''.join(portal[:-1])] += ((y, x + 2), )
        # Check left:
        elif x > 1 and is_portal((portal := maze[y, x: x - 3: -1])):
             mapping[''.join(portal[1::-1])] += ((y, x - 2), )

(AA, ), (ZZ, ) = mapping.pop('AA'), mapping.pop('ZZ')
G.add_edges_from(mapping.values())
print(nx.shortest_path_length(G, AA, ZZ)) # Part 1
G.remove_edges_from(mapping.values())

inner, outer = {}, {}
for name, locations in mapping.items():
    for location in locations:
        y, x = location
        (outer if 2 in location or y == height - 3 or x == width - 3 else inner)[name] = location

H = nx.Graph()
for level in range(26):
    for start, end in G.edges:
        H.add_edge((*start, level), (*end, level))
    for name, location in inner.items():
        H.add_edge((*location, level), (*outer[name], level + 1))
print(nx.shortest_path_length(H, (*AA, 0), (*ZZ, 0))) # Part 2