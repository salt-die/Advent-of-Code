"""
Thermal Environment Supervision Terminal
"""
from Computer import Computer
import curses
from curses.textpad import rectangle
import time
from time import sleep

SLEEP = .005
SLEEP2 = .1

class TEST:
    def __init__(self, computer):
        self.init_scr()
        self.computer = computer
        self.translate = {'01':'ADD',
                          '02':'MUL',
                          '03':'IN',
                          '04':'OUT',
                          '05':'JUMP-IF-TRUE',
                          '06':'JUMP-IF-FALSE',
                          '07':'LT',
                          '08':'EQ',
                          '99':'HALT',
                          '0':'P',
                          '1':'I'}
        self.old_pointer = self.old_nparams = self.old_write = 0

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
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)

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

        data_len = len(self.computer.int_code)
        for i in range(data_len + (-data_len % self.boxes_per_row)):
            self.write_to(i, 0)
            self.screen.refresh()
            sleep(SLEEP)

        self.out_win_row_start = data_len // self.boxes_per_row + 4

        rectangle(self.screen, self.out_win_row_start - 1, 0, self.height - 1, self.width - 2)
        self.screen.refresh()

        self.output_box = curses.newwin(self.height - self.out_win_row_start - 6,
                                        self.width - 4, self.out_win_row_start, 1)

        self.output_win("Welcome to the Thermal Environment Supervision Terminal (TEST). Press any key to continue.")
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


    def show_computation(self, pointer, op_code, modes):
        op_code = self.translate[op_code]

        for i in range(self.old_nparams + 1): #Un-highlight
            self.highlight(self.old_pointer + i, 1)

        #Highlight pointer and parameters
        self.highlight(pointer, 2)
        self.output_win(f'{op_code}:', pause=False)
        self.screen.refresh()
        sleep(SLEEP2)
        for i, mode in enumerate(modes, start=1):
            self.highlight(pointer + i, 3 + int(mode))
            params = " ".join(f"{self.translate[mode]}{self.computer.read(pointer + j)}"
                              for j, mode in enumerate(modes[:i], start=1))
            self.output_win(f'{op_code}: {params}', pause=False)
            self.screen.refresh()
            sleep(SLEEP2)

        for i, mode in enumerate(modes, start=1):
            self.highlight(pointer + i, 2)

        params = " ".join(f"{self.computer.parameter_modes[mode](self.computer.read(pointer + j))}"
                          for j, mode in enumerate(modes, start=1))
        self.output_win(f'{op_code}: {params}', pause=False)
        self.screen.refresh()
        sleep(SLEEP2)

        if op_code == 'OUT':
            self.output_win(f'DIAGNOSTIC CODE: {self.computer.parameter_modes[mode](self.computer.read(pointer + 1))}. Press any key to continue.')
            self.screen.getch()
        if op_code == 'HALT':
            self.output_win('HALT. Press any key to exit.')
            self.screen.getch()

        #Highlight writes
        last_write = self.computer.last_write_to
        self.highlight(self.old_write, 1)
        self.write_to(last_write, self.computer.read(last_write))
        self.highlight(last_write, 5)
        self.screen.refresh()
        sleep(SLEEP2)

        self.old_pointer = pointer
        self.old_nparams = len(modes)
        self.old_write = self.computer.last_write_to

    def write_to(self, index, value):
        row, col = divmod(index, self.boxes_per_row)
        self.screen.addstr(row + 2, col * 9, f'{value:>9}')

    def highlight(self, index, color_pair):
        row, col = divmod(index, self.boxes_per_row)
        self.screen.chgat(row + 2, col * 9, 9, curses.color_pair(color_pair))

    def output_win(self, out, pause=True):
        self.output_box.clear()
        if pause:
            for i, char in enumerate(out):
                self.output_box.addstr(0, i, char)
                self.output_box.refresh()
                sleep(SLEEP)
        else:
            self.output_box.addstr(0, 0, out)
            self.output_box.refresh()


if __name__=="__main__":
    with open('input05', 'r') as data:
        data = list(map(int, data.read().split(',')))

    tape = Computer(int_code=data)
    TEST(tape).start()
