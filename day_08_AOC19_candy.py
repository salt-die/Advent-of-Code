import numpy as np
import os
from random import shuffle
from itertools import count
import cv2
import imageio

l = np.array([[0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
              [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
              [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
              [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
              [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
              [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0]])

start = np.zeros_like(l)
random_indices=np.dstack(np.where(l==1)).tolist()[0]
shuffle(random_indices)
counter = count()
while random_indices:
    if np.random.random() > .9:
        start[tuple(random_indices.pop())] = 1
    if round(np.random.random()):
        start[tuple(random_indices.pop())] = 1

    cv2.imwrite(f'frames/{next(counter):03d}.png',
                cv2.resize(np.where(start != 1, 0, 255), (250, 60), interpolation=cv2.INTER_NEAREST))

frames = [imageio.imread(os.path.join('frames/', file))
          for file in sorted(os.listdir('frames/'))]
frames[-1:] += frames[-1:] * 20 # Show last frame for longer duration
imageio.mimsave('frames/AOC19.gif', frames, duration=.1)