import numpy as np
import scipy.ndimage as nd
from collections import defaultdict

KERNEL = np.array([[0, 1, 0],
                   [1, 0, 1],
                   [0, 1, 0]], dtype=np.uint8)

with open('input24', 'r') as data:
    data = [[1 if char == '#' else 0 for char in line] for line in data.read().splitlines()]

def new_state(universe):
    neighbor_count = nd.convolve(universe, KERNEL, mode="constant")
    still_alive = np.where((universe == 1) & (neighbor_count == 1), 1, 0)
    new_borns = np.where((universe == 0) & ((neighbor_count == 2) | (neighbor_count == 1)), 1, 0)
    return still_alive + new_borns

universe = np.array(data)
states = set()
states.add(universe.tostring())

while True:
    universe = new_state(universe)
    if (as_string := universe.tostring()) in states:
        break
    states.add(as_string)

powers = np.nditer(universe, flags=['c_index'])
print(sum(2**powers.index for cooef in powers if cooef)) # Part 1: 18842609

levels = defaultdict(lambda:np.zeros_like(universe), {0: np.array(data)})
levels[-1]; levels[1] # Outer and inner level
def new_states_recursive():
    #Add two new levels

    new_states = defaultdict(lambda:np.zeros_like(universe))    
    for level in list(levels):
        current = levels[level]
        neighbor_count = nd.convolve(current, KERNEL, mode="constant")
        #outer sums
        neighbor_count[0] += levels[level - 1][1, 2]
        neighbor_count[4] += levels[level - 1][3, 2]
        neighbor_count[:,0] += levels[level - 1][2, 1]
        neighbor_count[:,4] += levels[level - 1][2, 3]
        
        #inner sums
        neighbor_count[1, 2] += levels[level + 1][0].sum()
        neighbor_count[3, 2] += levels[level + 1][4].sum()
        neighbor_count[2, 1] += levels[level + 1][:,0].sum()
        neighbor_count[2, 3] += levels[level + 1][:,4].sum()
        
        still_alive = np.where((current == 1) & (neighbor_count == 1), 1, 0)
        new_borns = np.where((current == 0) & ((neighbor_count == 2) | (neighbor_count == 1)), 1, 0)
        new_levels[level] = still_alive + new_borns
        new_levels[level][2, 2] = 0
    levels.update(new_states)
        
for _ in range(200):
    new_state_recursive()
    
print(sum(array.sum() for array in levels.values())) # Part 2: 2059
