from computer import Computer
from display import Display, array_from_dict
import networkx as nx
from vector import Vec

WALL, OXYGEN, ROBOT, START = 1, 3, 4, 5
UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

directions = {Vec((-1,  0)): UP,
              Vec(( 1,  0)): DOWN,
              Vec(( 0, -1)): LEFT,
              Vec(( 0,  1)): RIGHT}

def reduce_path(path):
    for start, end in zip(path, path[1:]):
        yield end - start

class Robot:
    def __init__(self, data):
        self.START = self.previous =  0, 0
        self.END = None
        self.map = {self.START: START}
        self.G = nx.Graph()
        self.G.add_node(self.START, checked=False)
        self.brain = Computer(int_code=data)
        self.computation = self.brain.compute_iter()
        self.location = Vec((0, 0))
        self.display = Display()

    def ahead(self, direction=None):
        """Return location of cell ahead of Robot."""
        if direction is None:
            direction = self.direction
        return self.location + direction

    def show(self):
        """Recolor current location, show map, and un-color current location."""
        real_color = self.map[self.location]
        self.map[self.location] = ROBOT
        self.display(pixels=array_from_dict(self.map))
        self.map[self.location] = real_color

    def update_pos(self, wall_ahead):
        self.previous = self.location
        if not wall_ahead:
            self.location = self.location + self.direction

    def update_map(self):
        """Add new cells or walls to self.map."""
        output = self.brain.pop() + WALL
        self.update_pos(is_wall:= output == WALL)
        if is_wall:
            self.map[self.ahead()] = output
        elif self.location not in self.G:
            self.G.add_node(self.location, checked=False)
            self.G.add_edge(self.previous, self.location)
            self.map[self.location] = output
            if output == OXYGEN:
                self.END = self.location

    def run_until_next_input(self, direction):
        self.direction = direction
        self.brain << directions[direction]
        for _, op, _, _, _ in self.computation:
            if self.brain:
                self.update_map()
                self.show()
            if op == '03':
                return

    __rshift__ = run_until_next_input

    def path_length(self, node):
        return nx.shortest_path_length(self.G, self.location, node)

    def discover_maze(self):
        """
        Move to closest unchecked cell and check it until there are no more unchecked cells.
        """
        try:
            while True:
                unchecked = (node for node, checked in self.G.nodes(data='checked') if not checked)
                closest = min(unchecked, key=self.path_length)
                if closest != self.location:
                    self.move_to_node(closest)
                self.check()
        except ValueError: # All cells checked.
            return

    def move_to_node(self, node):
        for direction in reduce_path(nx.shortest_path(self.G, self.location, node)):
            self >> direction

    def check(self):
        """
        Move in each direction from a specific cell, returning to the cell if we don't
        encounter a wall.
        """
        for direction in directions:
            if self.ahead(direction) not in self.map:
                self >> direction
                if self.previous != self.location:
                    self >> -direction
        self.G.add_node(self.location, checked=True)

    def start(self):
        self.discover_maze()
        start_oxy = nx.shortest_path_length(self.G, self.START, self.END)
        fill_time = max(nx.shortest_path_length(self.G, source=self.END).values())
        self.display.text(f'Distance from START to OXYGEN is {start_oxy}. Fill time is {fill_time}.')
        self.display.stop()
        print(start_oxy, fill_time, sep='\n')