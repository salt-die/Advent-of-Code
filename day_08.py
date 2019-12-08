import numpy as np
from functools import reduce

with open('input08', 'r') as data:
    data = np.fromiter(data.read().strip(), int).reshape((-1, 6, 25))

fewest_zeros = data[(data == 0).sum(axis=(1, 2)).argmin()]
print((fewest_zeros == 1).sum() * (fewest_zeros == 2).sum()) # Part 1

decoded = reduce(lambda top, bottom: np.where(top != 2, top, bottom), data) # Part 2
print(*map(''.join, decoded.astype(str)), sep='\n')

## Alternative Part 2 -- animation
#import cv2
#import imageio
#
#decoded = data[0]
#for i, layer in enumerate(data):
#    decoded = np.where(decoded != 2, decoded, layer)
#    cv2.imwrite(f'frames/{i:03d}.png',
#                cv2.resize(np.where(decoded != 1, 0, 255), (250, 60), interpolation=cv2.INTER_NEAREST))
#
#frames = [imageio.imread(f'frames/{i:03d}.png') for i in range(len(data))]
#frames[-1:] += frames[-1:] * 20 # Show last frame for longer duration
#imageio.mimsave('frames/transmission.gif', frames, duration=.1)
