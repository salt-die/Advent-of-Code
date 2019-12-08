import numpy as np
from functools import reduce
import matplotlib.pyplot as plt

with open('input08', 'r') as data:
    data = np.fromiter(data.read().strip(), int).reshape((-1, 6, 25))

fewest_zeros = data[np.argmin((data == 0).sum(axis=(1, 2)))]
print((fewest_zeros == 1).sum() * (fewest_zeros == 2).sum()) # Part 1

decoded = reduce(lambda top, bottom: np.where(top != 2, top, bottom), data)
plt.axis('off'); plt.tight_layout(pad=0); plt.imshow(decoded); plt.show() # Part 2
