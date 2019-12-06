import networkx as nx

with open('input06', 'r') as data:
    G = nx.Graph( item.strip().split(')') for item in data.readlines())

print(sum(nx.shortest_path_length(G, node, 'COM') for node in G))

print(nx.shortest_path_length(G, 'YOU', 'SAN') - 2)
