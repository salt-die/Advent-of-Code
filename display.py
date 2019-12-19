import curses
import numpy as np

def array_from_dict(pixels):
    xs = [x for x, _ in pixels]
    ys = [y for _, y in pixels]

    min_xy = min(xs), min(ys)
    width = np.ptp(xs) + 1
    height = np.ptp(ys) + 1

    display = np.zeros([width, height], dtype=int)
    for location, pixel in pixels.items():
        location = tuple(np.array(location) - min_xy)
        display[location] = pixel

    return display

def center(length_1, length_2):
    return ((length_1 - length_2) // 2 - 1) if length_1 > length_2 else 0


class Display:
    def __init__(self):
        self.init_scr()
        self.buffer = []

    def init_scr(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.keypad(True)
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.screen.attron(curses.color_pair(1))
        self.screen.refresh()

    def stop(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.flushinp()
        curses.endwin()

    def show(self, pixels, **kwargs):
        screen_h, screen_w = self.screen.getmaxyx()
        pixels_h, pixels_w = pixels.shape
        pad = curses.newpad(pixels_h + 1, 2 * pixels_w + 1)

        for i, line in enumerate(pixels):
            for j, pixel in enumerate(line):
                pad.addstr(i, 2 * j, 2 * " █"[pixel > 0], curses.color_pair(1 + pixel))

        pad_u = center(pixels_h, screen_h)
        pad_l = center(pixels_w, screen_w)
        screen_u = center(screen_h, pixels_h)
        screen_l = center(screen_w,  2 * pixels_w)

        pad.refresh(pad_u, pad_l, screen_u, screen_l, screen_h - 1, screen_w - 1)

        if kwargs:
            info = f"{' | '.join(f'{key}: {value}' for key, value in kwargs.items())}{' ' * 20}"
            self.screen.addstr(max(0, screen_u - 1), screen_l, info, curses.A_BOLD)
            self.screen.refresh()

    __call__ = show # Shortcut to show method

    def text(self, message='Any key to continue...', blink=False):
        screen_h, screen_w = self.screen.getmaxyx()
        prop = curses.A_BOLD | (curses.A_BLINK if blink else 0)
        self.screen.addstr(screen_h - 1, center(screen_w, len(message)), message, prop)
        self.screen.refresh()
        self.screen.getch()

    def textpad(self, text, getch=False):
        if text != '\n':
            self.buffer.append(text.strip())
        else:
            screen_h, screen_w = self.screen.getmaxyx()
            self.screen.erase()
            for i, line in enumerate(self.buffer):
                self.screen.addstr(center(screen_h, len(self.buffer)) + i,
                                   center(screen_w, len(line)), line)
            self.screen.refresh()
            self.buffer = []
            if getch:
                self.screen.getch()