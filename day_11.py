from computer import Computer
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

with open('input11', 'r') as data:
    data = list(map(int, data.read().split(',')))

class Robot:
    def __init__(self, data=data):
        self.brain = Computer(int_code=data)
        self.direction = -1 + 0j
        self.location = np.array([0, 0])
        self.painted_locations = set()
        self.colors = defaultdict(int)

    def paint(self, color):
        self.colors[tuple(self.location)] = color

    def turn(self, clockwise):
        self.direction *= 1j * (-1)**(clockwise)

    def move(self):
        self.location += int(self.direction.real), int(self.direction.imag)

    def start(self):
        for _, op, _, _, _ in self.brain.compute_iter():
            if len(self.brain.out)==2:
                self.painted_locations.add(tuple(self.location))
                self.paint(self.brain.pop())
                self.turn(self.brain.pop())
                self.move()
            if op == '03':
                self.brain << self.colors[tuple(self.location)]


bad_robot = Robot()
bad_robot.start()
print(len(bad_robot.painted_locations)) # Part 1

good_robot = Robot()
good_robot.colors[tuple(good_robot.location)] = 1
good_robot.start()

# Construct picture from dictionary
height = max(good_robot.colors)[0] + 1
width = max(good_robot.colors, key=lambda tup:tup[1])[1] + 1

registration_identifier = np.zeros([height, width])
for location, color in good_robot.colors.items():
    registration_identifier[location] = color

plt.imshow(registration_identifier) # Part 2