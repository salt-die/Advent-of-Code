import numpy as np

with open('input08', 'r') as data:
    data = np.fromiter(data.read().strip(), int).reshape((-1, 6, 25))

fewest_zeros = data[(data == 0).sum(axis=(1, 2)).argmin()]
print((fewest_zeros == 1).sum() * (fewest_zeros == 2).sum()) # Part 1

row, col = np.mgrid[:6, :25]
decoded = data[(data != 2).argmax(axis=0), row, col]
print(*map(''.join, decoded.astype(str)), sep='\n') # Part 2

## Alternative Part 2 -- animation
#import cv2
#import imageio
#from stitch import stitch
#
#decoded = data[0]
#for i, layer in enumerate(data):
#    decoded = np.where(decoded != 2, decoded, layer)
#    cv2.imwrite(f'frames/{i:03d}.png',
#                cv2.resize(np.where(decoded != 1, 0, 255), (250, 60), interpolation=cv2.INTER_NEAREST))
#
#stitch(filename='transmission')
