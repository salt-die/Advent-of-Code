"""
Thermal Environment Supervision Terminal
"""
from Computer import Computer
import curses
from curses.textpad import rectangle
import time
from time import sleep

SLEEP = .005

class TEST:
    def __init__(self, computer):
        self.init_scr()
        self.computer = computer
        self.translate = {'01':'ADD',
                          '02':'MUL',
                          '03':'IN>>',
                          '04':'OUT>>',
                          '05':'JUMP-IF-TRUE',
                          '06':'JUMP-IF-FALSE',
                          '07':'LT',
                          '08':'EQ',
                          '99':'HALT',
                          '0':'POSITION',
                          '1':'IMMEDIATE'}

    def start(self):
        self.setup()
        for computation in self.operation_iterator:
            self.show_computation(*computation)
            sleep(SLEEP)
        self.end_curses()

    def init_scr(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.keypad(True)
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        self.screen.attron(curses.color_pair(1))

    def end_curses(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.flushinp()
        curses.endwin()

    def setup(self):
        self.height, self.width = self.screen.getmaxyx()
        self.boxes_per_row = self.width // 9

        for i in range(len(self.computer.int_code)):
            row, col = divmod(i, self.boxes_per_row)
            self.screen.addstr(row + 2, col * 9, f'{0:>9}')
            self.screen.refresh()
            sleep(SLEEP)

        self.out_win_row_start = row + 4

        for col in range(col + 1, self.boxes_per_row):
            self.screen.addstr(row + 2, col * 9, f'{0:>9}')
            self.screen.refresh()
            sleep(SLEEP)

        rectangle(self.screen, self.out_win_row_start - 1, 0, self.height - 1, self.width - 2)
        self.screen.refresh()

        self.output_box = curses.newwin(self.height - row - 6, self.width - 4,
                                        self.out_win_row_start, 1)

        self.output_win("Welcome to Thermal Environment Supervision Terminal (TEST). Press any key to continue.")
        self.screen.getch()
        self.output_win("Loading Intcode")

        for i, item in enumerate(self.computer.int_code):
            row, col = divmod(i, self.boxes_per_row)
            self.screen.addstr(row + 2, col * 9, f'{item:>9}')
            dots = 3 - round(2*time.time()) % 4
            self.output_box.addstr(0, 15, "...   "[dots:dots + 3])
            self.output_box.refresh()
            self.screen.refresh()
            sleep(SLEEP)

        self.output_win("Intcode Loaded. Enter System ID to start diagnostic: ")
        curses.echo()
        curses.curs_set(1)
        system_id = int(chr(self.output_box.getch())) #TODO: try/except for bad inputs
        curses.noecho()
        curses.curs_set(0)
        self.operation_iterator = self.computer.compute_iter(sys_id=system_id)
        self.old_pointer = 0

    def show_computation(self, pointer, op_code, modes):
        op_code = self.translate[op_code]
        modes = map(self.translate.get, modes)
        old_row, old_col = divmod(self.old_pointer, self.boxes_per_row)
        row, col = divmod(pointer, self.boxes_per_row)

        self.screen.chgat(old_row + 2, old_col * 9, 9, curses.color_pair(1))
        self.screen.chgat(row + 2, col * 9, 9, curses.color_pair(2))
        self.screen.refresh()
        sleep(.1)

        self.old_pointer = pointer

    def output_win(self, out):
        self.output_box.clear()
        for i, char in enumerate(out):
            self.output_box.addstr(0, i, char)
            self.output_box.refresh()
            sleep(SLEEP)


if __name__=="__main__":
    with open('input05', 'r') as data:
        data = list(map(int, data.read().split(',')))

    tape = Computer(int_code=data)
    TEST(tape).start()
