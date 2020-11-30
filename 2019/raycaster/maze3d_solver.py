import networkx as nx
from computer import Computer
from vector import Vec

WALL, PATH =  0, 1
UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
START = Vec((0, 0))

directions = {Vec((-1,  0)): UP,
              Vec(( 1,  0)): DOWN,
              Vec(( 0, -1)): LEFT,
              Vec(( 0,  1)): RIGHT}

def reduce_path(path):
    for start, end in zip(path, path[1:]):
        yield end - start

class Robot:
    def __init__(self):
        self.G = nx.Graph()
        self.stack = []
        with open('input15', 'r') as data:
            self.brain = Computer(int_code=list(map(int, data.read().split(','))))
        self.computation = self.brain.compute_iter()

        self.location = self.previous =  START
        self.grid = {START: PATH}
        self.G.add_node(START)

    def ahead(self, direction=None):
        """Return location of cell ahead of Robot."""
        if direction is None:
            direction = self.direction
        return self.location + direction

    def update_pos(self, wall_ahead):
        self.previous = self.location
        if not wall_ahead:
            self.location = self.location + self.direction

    def update_grid(self):
        """Add new cells or walls to self.grid."""
        output = self.brain.pop()
        self.update_pos(output == WALL)
        if output == WALL:
            self.grid[self.ahead()] = WALL
        elif self.location not in self.G:
            self.stack.append(self.location)
            self.G.add_node(self.location)
            self.G.add_edge(self.previous, self.location)
            self.grid[self.location] = PATH

    def run_until_next_input(self, direction):
        self.direction = direction
        self.brain << (direction := directions[direction])
        for _, op, _, _, _ in self.computation:
            if self.brain:
                self.update_grid()
            if op == '03':
                yield direction
                return

    __rshift__ = run_until_next_input

    def discover_maze(self):
        """
        Move to next unchecked cell on the stack and check it until all cells have been checked.
        """
        self.check()
        while self.stack:
            yield from self.move_to_node(self.stack.pop())
            self.check()

    def move_to_node(self, node):
        for direction in reduce_path(nx.shortest_path(self.G, self.location, node)):
            yield from self >> direction

    def check(self):
        """
        Move in each direction from current location, returning immediately if we don't
        encounter a wall.
        """
        for direction in directions:
            if self.ahead(direction) not in self.grid:
                next(self >> direction)
                if self.previous != self.location:
                    next(self >> -direction)

