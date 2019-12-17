import curses
import os
import signal
import numpy as np
from maze3d_solver import Robot

UP, DOWN, LEFT, RIGHT, PAD = 1, 2, 3, 4, 50

to_vector = {UP:    np.array([  0, -1]),
             DOWN:  np.array([  0,  1]),
             LEFT:  np.array([ -1,  0]),
             RIGHT: np.array([  1,  0])}

to_angle = {UP:    3 * np.pi / 2,
            DOWN:      np.pi / 2,
            LEFT:      np.pi,
            RIGHT:       0}

def rotation_matrix(theta):
    """
    Returns a 2-dimensional rotation array of a given angle.
    """
    return np.array([[np.cos(theta), np.sin(theta)],
                     [-np.sin(theta), np.cos(theta)]])

class Map:
    """
    A helper class for easy loading of maps.
    """
    def __init__(self, file_name):
        self._load(file_name)

    def _load(self, file_name):
        with open(file_name + '.txt', 'r') as file:
            map_ = [list(line.strip()) for line in file]
            self.map = np.array(map_, dtype=int).T

    def __getitem__(self, key):
        return self.map[key]


class Player:
    field_of_view = .6  # Somewhere between 0 and 1 is reasonable

    def __init__(self, game_map, pos=np.array([21.5, 21.5]), angle=np.pi / 2):
        self.game_map = game_map
        self.pos = pos
        self.angle = angle
        self.cam = np.array([[1, 0], [0, self.field_of_view]]) @ rotation_matrix(angle)

    def turn(self, angle):
        self.angle = angle
        self.cam = np.array([[1, 0], [0, self.field_of_view]]) @ rotation_matrix(angle)

class Renderer:
    """
    The Renderer class is responsible for everything drawn on the screen.
    """
    max_hops = 20  # How far rays are cast.

    # Shading constants -- Modifying ascii_map should be safe.
    ascii_map = np.array(list(' .,:;<+*LtCa4U80dQM@'))
    shades = len(ascii_map) - 1
    side_shade = (shades + 1) // 5
    shade_dif = shades - side_shade

    def __init__(self, screen, player, textures):
        self.screen = screen
        self.resize()

        self.player = player
        self.game_map = player.game_map
        self.mini_map = np.pad(np.where(self.game_map.map == 0, ' ', '#'), PAD, constant_values=' ')
        self._load_textures(textures)

    def resize(self):
        self.width, self.height = os.get_terminal_size()
        curses.resizeterm(self.height, self.width)
        self.angle_increment = 1 / self.width
        self.floor_y = self.height // 2

    def _load_textures(self, textures):
        self.textures = []
        for name in textures:
            with open(name + '.txt', 'r') as texture:
                pre_load = [list(line.strip()) for line in texture]
                self.textures.append(np.array(pre_load, dtype=int).T)

    def cast_ray(self, column):
        """
        Cast rays and draw columns whose heights correspond to the distance a ray traveled
        until it hit a wall.
        """
        ray_angle = self.player.cam.T @ np.array((1, 2 * column * self.angle_increment - 1))
        map_pos = self.player.pos.astype(int)
        with np.errstate(divide='ignore'):
            delta = abs(1 / ray_angle)
        step = 2 * np.heaviside(ray_angle, 1) - 1  # Same as np.sign except 0 is mapped to 1
        side_dis = step * (map_pos + (step + 1) / 2 - self.player.pos) * delta

        # Cast a ray until we hit a wall or hit max_range
        for hops in range(self.max_hops):
            side = 0 if side_dis[0] < side_dis[1] else 1
            side_dis[side] += delta[side]
            map_pos[side] += step[side]
            if self.game_map[tuple(map_pos)]:
                break
        else:  # No walls in range
            return 0, 0, []

        # Avoiding euclidean distance, to avoid fish-eye effect.
        wall_dis = (map_pos[side] - self.player.pos[side] + (1 - step[side]) / 2) / ray_angle[side]

        line_height = int(self.height / wall_dis) if wall_dis else self.height
        if line_height == 0:
            return 0, 0, []  # Draw nothing

        line_start = max(0, int((-line_height + self.height) / 2))
        line_end = min(self.height, int((line_height + self.height) / 2))
        line_height = line_end - line_start  # Correct off-by-one errors

        shade = min(line_height, self.shade_dif)
        shade += 0 if side else self.side_shade  # One side is brighter

        shade_buffer = np.full(line_height, shade)

        tex_num = self.game_map[tuple(map_pos)] - 1
        texture_width, texture_height = self.textures[tex_num].shape

        wall_x = (self.player.pos[1 - side] + wall_dis * ray_angle[1 - side]) % 1
        tex_x = int(wall_x * texture_width)
        if (-1)**side * ray_angle[side] > 0:
            tex_x = texture_width - tex_x - 1

        tex_ys = (np.arange(line_height) * (texture_height / line_height)).astype(int)
        shade_buffer += 2 * self.textures[tex_num][tex_x, tex_ys] - 12
        np.clip(shade_buffer, 1, self.shades, out=shade_buffer)

        self.buffer[line_start:line_end, -column] = self.ascii_map[shade_buffer]

    def draw_minimap(self):
        start_col = 2 * (self.width // 3) - 3
        start_row = 2 * (self.height // 3) - 3
        x, y = self.player.pos.astype(int) + PAD
        half_w = self.width // 3 // 2
        half_h = self.height // 3 // 2

        self.buffer[start_row: start_row + 2 * half_h,
                    start_col: start_col + 2 * half_w] = self.mini_map[x - half_h: x + half_h,
                                                                       y - half_w: y + half_w]
        self.buffer[start_row + half_h, start_col + half_w] = '@'

    def update(self):
        self.buffer = np.full((self.height, self.width), ' ') # Clear buffer

        self.buffer[self.floor_y:, :] = self.ascii_map[1] # Draw floor

        for column in range(1, self.width + 1): # Draw walls
            self.cast_ray(column)

        self.draw_minimap()

        self.render()

    def render(self):
        for row_num, row in enumerate(self.buffer):
            self.screen.addstr(row_num, 0, ''.join(row[:-1]))
        self.screen.refresh()


class Controller():
    """
    Controller class handles user input and updates all other objects.
    """
    running = True
    resized = False

    def __init__(self, renderer, robot):
        self.player = renderer.player
        self.renderer = renderer
        self.player = renderer.player
        self.robot = robot
        self.commands = robot.discover_maze()
        signal.signal(signal.SIGWINCH, self.resize) # Our solution to curses resize bug

    def resize(self, *args):
        self.resized = True

    def movement(self, direction):
        if direction == UP and self.player.angle == 0:
            self.player.angle = 2 * np.pi
        elif direction == RIGHT and self.player.angle == to_angle[UP]:
            self.player.angle = -np.pi / 2

        frames = 10 if abs((angle := to_angle[direction]) - self.player.angle) < np.pi else 20
        if angle != self.player.angle:
            for theta in np.linspace(self.player.angle, angle, frames):
                self.player.turn(theta)
                self.update()

        for position in np.linspace(self.player.pos, self.player.pos + to_vector[direction], 10):
            self.player.pos = position
            self.update()

    def start(self):
        while self.running:
            self.update()
            self.movement(next(self.commands))

    def update(self):
        if self.resized:
            self.renderer.resize()
            self.resized = False
        self.renderer.update()


def main(screen):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    screen.attron(curses.color_pair(1))

    game_map = Map('map')
    player = Player(game_map)
    textures = ['wall']

    Controller(Renderer(screen, player, textures), Robot()).start()

    curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
