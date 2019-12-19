from computer import Computer
from display import Display
import numpy as np

with open('input19', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data)
screen = Display()
pixels = np.zeros((50, 50), dtype=int)
coordinates = np.nditer(pixels, flags=['multi_index'])

for _ in coordinates:
    tape << (coordinate := coordinates.multi_index)
    tape.compute()
    pixels[coordinate] = tape.pop()
    screen(pixels.T)

screen.text(f'Number of pixels is: {pixels.sum()}') # Part 1
screen.stop()

# By inspection the slope of the outer lines is roughly 5/3 and 10/7, so y-coordinate should
# be roughly in the 1000 range to fit a 100x100 box in the tractor beam, begin search there:

def is_beam(x, y):
    tape.compute(feed=(x, y))
    return tape.pop()

def find_edge(x, y):
    while is_beam(x, y):
        x += 1
    return x - 1

x = 681
y = 1000
while True:
    x = find_edge(x, y)
    if is_beam(x - 99, y + 99):
        x = x - 99
        break
    else:
        y += 1

print(x * 10000 + y) # Part 2: 10671712
