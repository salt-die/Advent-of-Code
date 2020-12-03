from collections import deque
import curses
from curses.textpad import Textbox, rectangle
import time

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

class Skiing:
    def __init__(self):
        self.init_scr()
        self.setup()
        self.start()
        self.end_curses()

    def init_scr(self):
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

    def end_curses(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.flushinp()
        curses.endwin()

    def setup(self):
        screen = self.screen
        height, width = self.screen.getmaxyx()

        # Ski Slope
        rectangle(screen, 0, 0, height - 4, width - 2)
        self.ski_win = curses.newwin(height - 5, width - 4, 1, 2)

        # Input
        rectangle(screen, height - 3,  0, height - 1, width - 2)
        self.input_win = curses.newwin(1, width - 4, height - 2, 2)
        self.input_win.attron(curses.color_pair(2))
        self.text_in = Textbox(self.input_win)

        self.screen.refresh()
        curses.doupdate()

    def start(self):
        self.input_win.refresh()
        curses.curs_set(1)
        self.text_in.edit()
        answer = self.text_in.gather()
        curses.curs_set(0)
        self.input_win.erase()
        self.input_win.refresh()


if __name__ == "__main__":
    Skiing()