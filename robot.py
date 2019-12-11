from collections import defaultdict
from itertools import count

from computer import Computer
import cv2
import numpy as np

class Robot:
    def __init__(self, data, *, animate=False):
        self.brain = Computer(int_code=data)
        self.direction = -1 + 0j
        self.location = np.array([0, 0])
        self.painted_locations = set()
        self.colors = defaultdict(int)

        self.animate = animate
        if animate: # Only works for part two (We know how large the array needs to be.)
            self.counter = count()
            self.array = np.zeros((6, 43))

    @property
    def loc(self):
        return tuple(self.location)

    def paint(self, color):
        self.colors[self.loc] = color
        self.painted_locations.add(self.loc)
        if self.animate:
            self.array[self.loc] = color * 255

    def turn(self, clockwise):
        self.direction *= 1j * (-1)**(clockwise)

    def move(self):
        self.location += int(self.direction.real), int(self.direction.imag)
        if self.animate:
            color = self.array[self.loc]
            self.array[self.loc] = 127
            cv2.imwrite(f'frames/{next(self.counter):03d}.png',
                        cv2.resize(self.array, (430, 60), interpolation=cv2.INTER_NEAREST))
            self.array[self.loc] = color

    def start(self):
        for _, op, _, _, _ in self.brain.compute_iter():
            if len(self.brain) == 2:
                self.paint(self.brain.pop())
                self.turn(self.brain.pop())
                self.move()
            if op == '03':
                self.brain << self.colors[self.loc]
