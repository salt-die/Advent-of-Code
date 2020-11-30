from collections import defaultdict
from computer import Computer
from display import Display, array_from_dict
import numpy as np

class Robot:
    def __init__(self, data, *, animate=False):
        self.brain = Computer(int_code=data)
        self.direction = -1 + 0j
        self.location = np.array([0, 0])
        self.painted_locations = set()
        self.colors = defaultdict(int)
        self.animate = animate
        if animate:
            self.display = Display()

    def show(self):
        self.display(pixels=array_from_dict(self.colors))

    @property
    def loc(self):
        return tuple(self.location)

    def paint(self, color):
        self.colors[self.loc] = color
        self.painted_locations.add(self.loc)

    def turn(self, clockwise):
        self.direction *= 1j * (-1)**(clockwise)

    def move(self):
        self.location += int(self.direction.real), int(self.direction.imag)
        if self.animate:
            self.show()

    def start(self):
        for _, op, _, _, _ in self.brain:
            if len(self.brain) == 2:
                self.paint(self.brain.pop())
                self.turn(self.brain.pop())
                self.move()
            if op == '03':
                self.brain << self.colors[self.loc]

        if self.animate:
            self.show()
            self.display.text('FINISHED')
            self.display.stop()
