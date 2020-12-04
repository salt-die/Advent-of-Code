import curses
from curses.textpad import Textbox, rectangle
from itertools import cycle
import re
import time
import numpy as np


SLOPE_RE = r"(\d+)"
INPUT_FILE = "day_03_input.txt"
INPUT_OFFSET = 3
INPUT_PADDING = 30
ART_DIM = 4, 6


skiier_1 = r"""
 ,_ o
/ //\,
 \>> |
  \\,
"""

skiier_2 = r"""
  X__O
\ (\(
 \/ `
  \,
"""

tree = r"""
   ^
  ^ ^
 ^ ^ ^
   |
"""

splat = r"""
 \ O ^
   ^ ^
 ^ ^ ^
  /\\
"""

def array_from_(art):
    lines = []
    for line in art.splitlines():
        if not line: continue
        line = list(line) + (6 - len(line)) * [" "]
        lines.append(line)
    return np.array(lines)

skiier_1, skiier_2, tree, splat = map(array_from_, (skiier_1, skiier_2, tree, splat))
skiier = cycle((skiier_1, skiier_2))

class Skiing:
    def __init__(self):
        self.init_curses()
        self.draw_border()
        self.ask()
        self.ski()
        self.end_curses()

    def init_curses(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.keypad(True)

        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

        self.screen.attron(curses.color_pair(4))

    def draw_border(self):
        h, w = self.screen.getmaxyx()
        rectangle(self.screen, 0, 0, h - 1, w - 2)

    def end_curses(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.flushinp()
        curses.endwin()

    def ask(self):
        """Get Slope"""
        screen = self.screen
        h, w = screen.getmaxyx()

        rectangle(screen, h // 2 - INPUT_OFFSET,  INPUT_PADDING, h // 2 - (INPUT_OFFSET - 2), w - INPUT_PADDING)
        input_win = curses.newwin(1, w - (2 * INPUT_PADDING + 2), h // 2 - (INPUT_OFFSET - 1), INPUT_PADDING + 1)
        input_win.attron(curses.color_pair(2))
        screen.addstr(h // 2 - INPUT_OFFSET, INPUT_PADDING + 1, "Enter Slope:", curses.color_pair(2))
        screen.refresh()

        curses.curs_set(1)
        text_in = Textbox(input_win)
        text_in.edit()
        x, y, *_ = re.findall(SLOPE_RE, text_in.gather())
        self.slope = int(x), int(y)
        curses.curs_set(0)

    def ski(self):
        # INIT
        screen = self.screen
        screen.erase()
        self.draw_border()
        screen.refresh()

        h, w = screen.getmaxyx()
        ski_win = curses.newwin(h - 2, w - 4, 1, 2)
        ski_win.attron(curses.color_pair(2))

        # Calculate how large our view can be...
        h, w = ski_win.getmaxyx()
        vh, vw = h // ART_DIM[0], w // ART_DIM[1]  # View height, View width
        vh, vw = vh - (1 if vh % 2 == 0 else 0), vw - (1 if vw % 2 == 0 else 0)  # Make dimensions odd so we can center skiier

        # SETUP BUFFER AND BIOME
        with open(INPUT_FILE) as f:
            biome = np.array([[char == "#" for char in line] for line in f.readlines()])

        buffer = np.full((vh * ART_DIM[0], vw * ART_DIM[1]), " ")
        sy, sx = vh // 2, vw // 2  # Skiier coordinates
        ski_slope = np.roll(biome, (sy, sx), (0, 1))  # Note biome is rolled back so we can slice a view around the skiier
        h, w = ART_DIM  # Last shadow of h, w

        count = 0
        for _ in range(0, len(biome), self.slope[1]):
            # Push trees to buffer
            it = np.nditer(ski_slope[: vh, : vw], flags=["multi_index"])
            for is_tree in it:
                y, x = it.multi_index
                if is_tree:
                    buffer[y * h: (y + 1) * h, x * w: (x + 1) * w] = tree

            # Buffer to Screen
            for i, line in enumerate(buffer):
                ski_win.addstr(i, 0, "".join(line))

            # Add Skiier
            for i, line in enumerate(splat if ski_slope[sy, sx] else next(skiier), start=sy * h):
                ski_win.addstr(i, sx * w, "".join(line), curses.color_pair(1))

            ski_win.refresh()
            time.sleep(.1)
            buffer[:] = " "
            count += ski_slope[sy, sx]
            ski_slope = np.roll(ski_slope, (-self.slope[1], -self.slope[0]), (0, 1))
            ski_win.erase()
        ski_win.addstr(0, 0, str(count))
        ski_win.refresh()
        screen.getch()

if __name__ == "__main__":
    Skiing()