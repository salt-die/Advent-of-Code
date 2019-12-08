import numpy as np
from functools import reduce

with open('input08', 'r') as data:
    data = np.fromiter(data.read().strip(), int).reshape((-1, 6, 25))

fewest_zeros = data[(data == 0).sum(axis=(1, 2)).argmin()]
print((fewest_zeros == 1).sum() * (fewest_zeros == 2).sum()) # Part 1

decoded = reduce(lambda top, bottom: np.where(top != 2, top, bottom), data) # Part 2
print(*("".join(row) for row in decoded.astype(str)), sep='\n')

#Alternative part 2 for creating animation
#import os
#import cv2
#import imageio

#decoded = data[-1]
#for i, layer in enumerate(data[::-1]):
#    decoded = np.where(layer != 2, layer, decoded)
#    cv2.imwrite(f'frames/{i:03d}.png',
#                cv2.resize(np.where(decoded != 0, 255, 0),
#                           (250, 60),
#                           interpolation=cv2.INTER_NEAREST))
#
#frames = [imageio.imread(os.path.join('frames/', file_name))
#          for file_name in sorted(os.listdir('frames/'))]
#imageio.mimsave('frames/transmission.gif', frames, duration = .1)
