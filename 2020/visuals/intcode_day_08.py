import curses
from curses.textpad import Textbox, rectangle
import re
import time

JMP, NOP, ACC = "JMP", "NOP", "ACC"
OP_COLOR = {}
OP_HIGHLIGHT = {}
OP_WINDOW_WIDTH = 11
INDEX_ACC_WINDOW_WIDTH = 27
VISITED_WINDOW_WIDTH = 5
DELAY = .05
CELL = " ⬤ "

with open("day_08_input.txt") as f:
    DATA = f.read()

DATA = [(addr.upper(), int(val)) for addr, val in re.findall(r"(.+) (.+)", DATA)]

def compute():
    index = acc = 0
    seen = set()
    while True:
        op, val = DATA[index]
        yield index, acc, op, val

        if index in seen:
            break
        seen.add(index)

        if op == JMP:
            index += val
        elif op == NOP:
            index += 1
        elif op == ACC:
            acc += val
            index += 1

def delayed(iter, delay=DELAY):
    for item in iter:
        yield item
        time.sleep(delay)

def init_scr(screen):
    screen.clear()
    screen.keypad(True)
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
    screen.attron(curses.color_pair(1))
    OP_COLOR.update(JMP=curses.color_pair(4), NOP=curses.color_pair(6), ACC=curses.color_pair(5))
    OP_HIGHLIGHT.update(JMP=curses.color_pair(7), NOP=curses.color_pair(9), ACC=curses.color_pair(8))

def end_curses(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.flushinp()
    curses.endwin()

def setup_windows(screen):
    height, width = screen.getmaxyx()
    width -= 1

    # Message window
    rectangle(screen, 0, 0, 2, width - INDEX_ACC_WINDOW_WIDTH - 2 - 1)
    messages = curses.newwin(1, width - INDEX_ACC_WINDOW_WIDTH - 2 - 2, 1, 1)

    # Address and accumulator window
    rectangle(screen, 0, width - INDEX_ACC_WINDOW_WIDTH - 2, 2, width)
    screen.addstr(1, width - INDEX_ACC_WINDOW_WIDTH - 1, "ADDRESS:      | ACC:")
    addr = curses.newwin(1, 5, 1, width - INDEX_ACC_WINDOW_WIDTH - 1 + 9)
    addr.attron(curses.color_pair(3))
    acc = curses.newwin(1, 7, 1, width - INDEX_ACC_WINDOW_WIDTH - 1 + 9 + 4 + 8)
    acc.attron(curses.color_pair(2))

    # Op history window
    rectangle(screen, 3, 0, height - 3, OP_WINDOW_WIDTH + 2)
    op_out = curses.newwin(height - 3 - 2 - 2, OP_WINDOW_WIDTH, 4, 1)
    op_out.scrollok(True)

    # Data window
    rectangle(screen, 3, OP_WINDOW_WIDTH + 2 + 1, height - 3, width - VISITED_WINDOW_WIDTH - 2 - 1)
    array = curses.newwin(height - 3 - 2 - 2, width - OP_WINDOW_WIDTH - 2 - VISITED_WINDOW_WIDTH - 2 - 3, 4, OP_WINDOW_WIDTH + 2 + 2)
    # Draw cell for each instruction in data
    _, w = array.getmaxyx()
    cell_per_row = w // len(CELL)
    for i, (op, _) in enumerate(DATA):
        row, col = divmod(i, cell_per_row)
        array.addstr(row, col * len(CELL), CELL, OP_COLOR[op])

    # Visited window
    rectangle(screen, 3, width - VISITED_WINDOW_WIDTH - 2, height - 3, width)
    visited = curses.newwin(height - 3 - 2 - 2, VISITED_WINDOW_WIDTH, 4, width - VISITED_WINDOW_WIDTH - 1)
    visited.attron(curses.color_pair(4))
    visited.scrollok(True)

    screen.refresh()
    array.refresh()

    return messages, addr, acc, op_out, array, visited


@curses.wrapper
def main(screen):
    init_scr(screen)
    message_win, addr_win, acc_win, op_out_win, array_win, visited_win = setup_windows(screen)

    def print_message(message, delay=DELAY):
        """Print single-line messages to the message window"""
        message_win.clear()
        for i, letter in delayed(enumerate(message), delay):
            message_win.addstr(0, i, letter)
            message_win.refresh()

    def dots(offset):
        n = 3
        while True:
            message_win.addstr(0, offset, "...   "[n: n + 3])
            message_win.noutrefresh()
            n -= 1
            n %= 4
            yield

    def update_ind_acc(ind, acc):
        addr_win.addstr(0, 0, f"{ind:04}")
        addr_win.noutrefresh()
        acc_win.addstr(0, 0, f"{acc:06}")
        acc_win.noutrefresh()

    def highlight():
        _, w = array_win.getmaxyx()
        cell_per_row = w // len(CELL)
        old_index = 0
        while True:
            index = yield

            row, col = divmod(old_index, cell_per_row)
            array_win.chgat(row, col * len(CELL) + 1, 1, OP_COLOR[DATA[old_index][0]])

            row, col = divmod(index, cell_per_row)
            array_win.chgat(row, col * len(CELL) + 1, 1, OP_HIGHLIGHT[DATA[index][0]])

            old_index = index
            array_win.noutrefresh()

    def update_ops(op, val):
        op_out_win.scroll()
        y, _ = op_out_win.getmaxyx()
        op_out_win.addstr(y - 1, 0, f"{op} {val:6}")
        op_out_win.chgat(y - 1, 0, 3, OP_COLOR[op])
        op_out_win.noutrefresh()

    def update_visited(ind):
        visited_win.scroll()
        y, _ = visited_win.getmaxyx()
        visited_win.addstr(y - 1, 0, f"{ind:4}")
        visited_win.noutrefresh()

    # Start of program
    highlighter = highlight(); next(highlighter)
    print_message("Detecting Cycle")
    dotter = dots(15)  # Generator that updates the "..." in the message window
    for ind, acc, op, val in delayed(compute(), .2):
        update_ops(op, val)
        update_ind_acc(ind, acc)
        update_visited(ind)

        highlighter.send(ind)
        next(dotter)

        curses.doupdate()

    print_message(f"Cycle detected at address {ind}. Any key to exit...")
    screen.getch()

    end_curses(screen)
