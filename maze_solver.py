from computer import Computer
from display import Display, array_from_dict
import networkx as nx
import numpy as np

WALL, PATH, OXYGEN, ROBOT, START = 1, 2, 3, 4, 5
UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

directions = {(-1, 0):UP,
              (1, 0):DOWN,
              (0, -1):LEFT,
              (0, 1):RIGHT}

def reduce_path(path):
    for start, end in zip(path, path[1:]):
        yield np.array(end) - start

class Robot:
    def __init__(self, data):
        self.START = self.previous =  0, 0
        self.END = None
        self.map = {self.START: START}
        self.G = nx.Graph()
        self.G.add_node(self.START, checked=False)
        self.brain = Computer(int_code=data)
        self.computation = self.brain.compute_iter()
        self.location = np.array([0, 0])
        self.display = Display()

    @property
    def loc(self):
        return tuple(self.location)

    def ahead(self, direction=None):
        if direction is None:
            direction = self.direction
        return tuple(self.location + direction)

    def show(self):
        real_color = self.map[self.loc]
        self.map[self.loc] = ROBOT
        self.display(pixels=array_from_dict(self.map))
        self.map[self.loc] = real_color

    def update_pos(self, output):
        self.previous = tuple(self.location)
        if output != WALL:
            self.location += self.direction

    def update_map(self):
        output = self.brain.pop() + 1
        self.update_pos(output)
        if output == WALL:
            self.map[self.ahead()] = output
        else:
            if self.loc not in self.G:
                self.G.add_node(self.loc, checked=False)
                self.G.add_edge(self.previous, self.loc)
            if self.loc != self.START:
                self.map[self.loc] = output
            if output == OXYGEN:
                self.END = self.loc

    def run_until_next_input(self, direction):
        self.direction = direction
        self.brain << directions[tuple(direction)]
        for _, op, _, _, _ in self.computation:
            if self.brain:
                self.update_map()
                self.show()
            if op == '03':
                return

    __rshift__ = run_until_next_input

    def path_length(self, node):
        return nx.shortest_path_length(self.G, self.loc, node)

    def discover_maze(self):
        unchecked = [node for node, checked in self.G.nodes(data='checked') if not checked]
        if not unchecked:
            return False
        node = min(unchecked, key=self.path_length)
        if node != self.loc:
            self.move_to_node(node)
        self.check()
        return True

    def move_to_node(self, node):
        path = nx.shortest_path(self.G, self.loc, node)
        for direction in reduce_path(path):
            self >> direction

    def check(self):
        for direction in directions:
            if self.ahead(direction) not in self.map:
                self >> np.array(direction)
                if self.previous != self.loc:
                    self >> -np.array(direction)
        self.G.add_node(self.loc, checked=True)

    def start(self):
        while self.discover_maze():
            pass
        start_oxy = nx.shortest_path_length(self.G, self.START, self.END)
        fill_time = max(nx.shortest_path_length(self.G, source=self.END).values())
        self.display.text(f'Distance from START to OXYGEN is {start_oxy}. Fill time is {fill_time}.')
        self.display.stop()
        print(start_oxy, fill_time, sep='\n')