"""Press `q` to quit early!
  ::Warning:: Still getting a different answer than my day 3 submission, so there's a bug somewhere!
"""
import curses
from curses.textpad import Textbox, rectangle
import re
import time
import numpy as np


SLOPE_RE = r"(\d+)"  # For grabbing slope integers from input box
INPUT_FILE = "day_03_input.txt"
INPUT_OFFSET = 3  # Vertical offset of input box
INPUT_PADDING = 30  # More padding will shrink the input box horizontally
ART_DIM = 4, 6  # Dimensions of ascii art below
DELAY = .06  # Time between frames
LANDING_TIME = .3  # Time we show skiier has landed safely or splatted, in seconds

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


\ o /
'\ /.
"""

def array_from_(art):
    """Convert ascii art to numpy array.
       ::Warning:: Hard coded ascii-art dimensions!
    """
    lines = []
    for line in art.splitlines()[1:]:
        line = list(line) + (6 - len(line)) * [" "]
        lines.append(line)
    return np.array(lines)

skiier_1, skiier_2, tree, splat = map(array_from_, (skiier_1, skiier_2, tree, splat))

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

        self.screen.attron(curses.color_pair(2))

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
        screen.addstr(h // 2 - INPUT_OFFSET, INPUT_PADDING + 1, "Enter Slope:")
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

        h, w = screen.getmaxyx()  # will shadow h, w a few times
        ski_win = curses.newwin(h - 2, w - 4, 1, 2)
        ski_win.nodelay(1)
        ski_win.attron(curses.color_pair(2))

        # Calculate how large our view can be...
        h, w = ski_win.getmaxyx()
        vh, vw = h // ART_DIM[0], w // ART_DIM[1]  # View height, View width
        vh, vw = vh - (1 if vh % 2 == 0 else 0), vw - (1 if vw % 2 == 0 else 0)  # Make dimensions odd so we can center skiier

        # SETUP BUFFER AND BIOME
        with open(INPUT_FILE) as f:
            biome = np.array([[char == "#" for char in line] for line in f.readlines()])

        sx, sy = self.slope
        # We have enough buffer to store our view plus trees to the right and down within slope of us.
        buffer = np.full(((vh + sy) * ART_DIM[0], (vw + sx) * ART_DIM[1]), " ")
        ski_y, ski_x = vh // 2, vw // 2  # Skiier coordinates
        ski_slope = np.roll(biome, (ski_y, ski_x), (0, 1))  # Note biome is rolled back so we can slice a view around the skiier
        h, w = ART_DIM  # Last shadow of h, w

        count = 0
        for _ in range(0, len(biome), sy):
            # Push trees to buffer
            it = np.nditer(ski_slope[: vh + sy, : vw + sx], flags=["multi_index"])
            for is_tree in it:
                if is_tree:
                    y, x = it.multi_index
                    buffer[y * h: (y + 1) * h, x * w: (x + 1) * w] = tree

            # This loop will "smooth-scroll" our buffer until we reach the next landing.
            x_pix = sx * w
            y_pix = sy * h
            for offset in range(max(x_pix, y_pix)):
                if x_pix > y_pix:
                    shift_x = offset
                    shift_y = round(offset * y_pix / x_pix)
                else:
                    shift_x = round(offset * x_pix / y_pix)
                    shift_y = offset
                # Buffer to Screen
                for i, line in enumerate(buffer[shift_y: (vh * h) + shift_y, shift_x: (vw * w) + shift_x]):
                    ski_win.addstr(i, 0, "".join(line))

                # Add Skiier
                skiier = (splat if ski_slope[ski_y, ski_x] else skiier_1) if offset * DELAY <= LANDING_TIME else skiier_2
                for i, line in enumerate(skiier, start=ski_y * h):
                    ski_win.addstr(i, ski_x * w, "".join(line), curses.color_pair(1))

                ski_win.refresh()
                if ski_win.getch() == ord("q"): return
                time.sleep(DELAY)

            # Reset buffer, update our count
            buffer[:] = " "
            count += ski_slope[ski_y, ski_x]
            ski_slope = np.roll(ski_slope, (-sy, -sx), (0, 1))

        ski_win.erase()
        ski_win.addstr(0, 0, str(count))
        ski_win.refresh()
        screen.getch() # Blocking getch

if __name__ == "__main__":
    Skiing()