import numpy as np

import aoc_lube

from nurses_2.app import App
from nurses_2.colors import gradient, AWHITE, AColor
from nurses_2.widgets.graphic_widget import GraphicWidget, composite
from nurses_2.widgets.text_widget import TextWidget

def parse_raw():
    lines = aoc_lube.fetch(year=2022, day=12).splitlines()
    grid = np.array([[ord(c) for c in line] for line in lines])

    start = tuple(np.argwhere(grid == ord('S'))[0])
    grid[start] = ord('a')

    end = tuple(np.argwhere(grid == ord('E'))[0])
    grid[end] = ord('z')

    return grid - ord('a'), start, end

GRID, START, END = parse_raw()
GREEN_TO_YELLOW = np.array(
    gradient(AColor.from_hex("26a812"), AColor.from_hex("35200a"), 26)
)


class MazeWidget(GraphicWidget):
    def __init__(self, info, **kwargs):
        super().__init__(size=(21, 83), **kwargs)
        self._otexture = GREEN_TO_YELLOW[GRID]
        self._cursortexture = np.zeros((3, 3, 4), np.uint8)
        self._steps = -1
        self.info = info
        self.current_pos = START

    @property
    def current_pos(self):
        return self._current_pos

    @current_pos.setter
    def current_pos(self, pos):
        self._current_pos = y, x = pos
        self.valid_directions = {
            (dy, dx)
            for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1))
            if 0 <= y + dy < 41
            if 0 <= x + dx < 83
            if GRID[y + dy, x + dx] - GRID[pos] <= 1
        }

        self.texture[:-1] = self._otexture

        self._cursortexture[:] = 0
        for dy, dx in self.valid_directions:
            self._cursortexture[1 + dy, 1 + dx] = AWHITE
        self._cursortexture[..., 3] //= 2  # Half transparency
        self._cursortexture[1, 1] = AWHITE

        composite(self._cursortexture, self.texture, (y - 1, x - 1))

        self._steps += 1

        self.info.add_text(f"Position: {str(pos).ljust(8)}")
        self.info.add_text(f"Elevation: {GRID[pos]:<2}", row=1)
        self.info.add_text(f"Steps: {self._steps:<4}", row=2)

    def on_key(self, key_event):
        keys = dict(up=(-1, 0), left=(0, -1), right=(0, 1), down=(1, 0))
        if key_event.key in keys and keys[key_event.key] in self.valid_directions:
            dy, dx = keys[key_event.key]
            y, x = self.current_pos
            self.current_pos = y + dy, x + dx
            return True

        if key_event.key == "r":  # Reset
            self._steps = -1
            self.current_pos = START
            return True


class HillClimbingApp(App):
    async def on_start(self):
        info = TextWidget(size=(3, 18), pos_hint=(None, .5), anchor="center")
        maze = MazeWidget(info, pos_hint=(.5, .5), anchor="center")
        info.subscribe(maze, "pos", lambda: setattr(info, "bottom", maze.top))
        self.add_widgets(maze, info)


HillClimbingApp(title="Hill Climbing").run()
