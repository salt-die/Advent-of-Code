from collections import deque
from math import log
import time
import curses
from curses.textpad import Textbox, rectangle
from computer import Computer

OUTPUT_WIDTH = 46
CELL_WIDTH = 2
BASE_2 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

class TEST:
    translate = {'01':'ADD',
                 '02':'MULTIPLY',
                 '03':'IN',
                 '04':'OUT',
                 '05':'JUMP-IF-TRUE',
                 '06':'JUMP-IF-FALSE',
                 '07':'LESS-THAN',
                 '08':'EQUALS',
                 '09':'BASE-INCR',
                 '99':'HALT',
                 '0':'POS',
                 '0o':'POS',
                 '1':'IMM',
                 '2':'REL',
                 '2o':'REL'}
    old_pointer = old_nparams = 0
    old_write = -1

    def __init__(self):
        self.init_scr()
        self.setup()
        self.computer = Computer(int_code=[], memory=0)
        self.start()
        self.end_curses()

    def start(self):
        self.display('Welcome to TESTv2.AoC.19')
        self.draw_cells(init=True, slow=True)
        self.display('Memory initialized...')

        running = True
        while running:
            with open(self.ask('Please Enter filename: ').strip(), 'r') as data:
                data = list(map(int, data.read().split(',')))
                self.computer.int_code = data + [0] * (self.cells - len(data))

            self.output.clear()
            self.output_win.erase()
            self.pointer_win.erase()
            self.output_win.refresh()
            self.pointer_win.refresh

            self.draw_cells(init=True, slow=False)
            self.draw_cells(slow=True)
            self.display('Intcode Loaded...')
            self.display('Any key to continue...')
            self.input_win.getch()

            feed = map(int, self.ask('Enter integer inputs separated by space: ').strip().split())
            self.operation_iterator = self.computer.compute_iter(feed=feed)
            #This odd loop is because Computer yields before instructions have executed.
            last_yield = next(self.operation_iterator)
            for computation in self.operation_iterator:
                self.show_computation(*last_yield)
                last_yield = computation
            self.show_computation(*last_yield)

            self.display("'q' to quit or any key to continue...")
            running = self.input_win.getch() not in (ord('q'), ord('Q'))

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
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)
        self.screen.attron(curses.color_pair(1))

    def end_curses(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.flushinp()
        curses.endwin()

    def setup(self):
        screen = self.screen
        height, width = self.height, self.width = self.screen.getmaxyx()

        # Instruction Pointer and Relative Base
        rectangle(screen, 0, OUTPUT_WIDTH + 3, 2, width - 2)
        self.pointer_win = curses.newwin(1, width - OUTPUT_WIDTH - 6, 1, OUTPUT_WIDTH + 4)

        # Output
        rectangle(screen, 0, 0, height - 1, OUTPUT_WIDTH + 2)
        self.output_win = curses.newwin(height - 2, OUTPUT_WIDTH, 1, 1)
        self.output = deque(maxlen=height - 2)

        # Array Vis
        rectangle(screen, 3, OUTPUT_WIDTH + 3, height - 4, width - 2)
        self.array_win = curses.newwin(height - 8, width - OUTPUT_WIDTH - 8, 4, OUTPUT_WIDTH + 5)
        self.array_win.attron(curses.color_pair(1))
        self.cells_per_row = (width - OUTPUT_WIDTH - 8) // CELL_WIDTH
        self.cells = self.cells_per_row * (height - 8)

        # Input
        rectangle(screen, height - 3, OUTPUT_WIDTH + 3, height - 1, width - 2)

        # Input line
        self.input_win = curses.newwin(1, width - OUTPUT_WIDTH - 6, height - 2, OUTPUT_WIDTH + 4)
        self.text_in = Textbox(self.input_win)

        self.screen.refresh()
        curses.doupdate()


    def display(self, out, pause=True, save=True):
        self.output_win.erase()
        if save:
            if len(self.output) and self.output[-1] == '':
                self.output[-1] = out
            else:
                self.output.append(out)
        elif self.output[-1] != '':
            self.output.append('')

        last_line = len(self.output) - 1
        for row, line in enumerate(self.output):
            if row != last_line:
                self.output_win.addstr(row, 0, line)

        if pause:
            for col, char in enumerate(out):
                self.output_win.addstr(last_line, col, char)
                self.output_win.refresh()
                time.sleep(.01)
        else:
            self.output_win.addstr(last_line, 0, out)
            self.output_win.refresh()

    def draw_cells(self, init=False, slow=False):
        message = ('Loading Intcode', 'Initializing Memory')[init]
        if slow:
            self.display(message)
        col = len(message)

        for cell in range(self.cells):
            if init or not self.computer.int_code[cell]:
                fill = BASE_2[0]
            else:
                fill = BASE_2[int(log(abs(self.computer.int_code[cell]), 2))]
            if init or self.computer.int_code[cell]:
                self.write_to(cell, fill)
                if slow:
                    dots = 3 - round(2*time.time()) % 4
                    self.output_win.addstr(len(self.output) - 1, col, '...   '[dots:dots + 3])
                    self.output_win.refresh()
                    time.sleep(.001)

    def show_computation(self, pointer, op_code, modes, params, moded_params):
        self.pointer_win.erase()
        self.pointer_win.addstr(0, 0,
                                (f' POS | IMM | REL | OUT | Instruction Pointer {pointer:5} |'
                                 f' Relative Base {self.computer.relative_base:5} | '
                                 f'{sum(bool(i) for i in self.computer.memory):4} Used/'
                                 f'{self.cells} Total Memory | TESTv2.AoC.19'))
        self.pointer_win.chgat(0, 1, 3, curses.color_pair(3))
        self.pointer_win.chgat(0, 7, 3, curses.color_pair(4))
        self.pointer_win.chgat(0, 13, 3, curses.color_pair(5))
        self.pointer_win.chgat(0, 19, 3, curses.color_pair(9))
        self.pointer_win.chgat(0, 25, 25, curses.color_pair(2))
        self.pointer_win.refresh()

        op_code = self.translate[op_code]

        if op_code == 'HALT':
            self.display("HALT")
            return

        self.display('', pause=False, save=False)

        for i in range(self.old_nparams + 1): #Un-highlight
                self.highlight(self.old_pointer + i, 1)
        if self.old_write != -1: #Keep last write highlighted
            self.highlight(self.old_write, 9)

        #Highlight pointer and parameters
        self.highlight(pointer, 2)
        self.display(f'{op_code:>13}', pause=False, save=False)
        time.sleep(.1)
        trans_modes = list(map(self.translate.get, modes))
        for i in range(1, len(modes) + 1):
            self.highlight(pointer + i, 3 + int(modes[i - 1][0]))
            param_str = ' '.join(f'{trans_modes[j]}{params[j]}' for j in range(i))
            self.display(f'{op_code:>13} {param_str}', pause=False, save=False)
            time.sleep(.1)
        self.display(f'{op_code:>13} {param_str}', pause=False)

        #Interpret parameter modes
        for i, mode in enumerate(modes, start=1):
            self.highlight(pointer + i, 6 + int(mode[0]))
        param_str = ' '.join(f'{moded_param}' for moded_param in moded_params)
        self.display(f'{"":^13} {param_str}', pause=False)
        time.sleep(.1)

        #Highlight writes
        last_write = self.computer.last_write_to
        if self.old_write != -1:
            self.highlight(self.old_write, 1)
        value = self.computer.read(last_write)
        fill = BASE_2[0 if not value else int(log(value, 2))]
        self.write_to(last_write, fill)
        self.highlight(last_write, 9)
        time.sleep(.1)

        if op_code == 'OUT':
            self.display(f'DIAGNOSTIC CODE: {self.computer.pop()}')
            self.display('Any key to continue...')
            self.input_win.getch()

        self.old_pointer = pointer
        self.old_nparams = len(modes)
        self.old_write = last_write

    def ask(self, question):
        self.display(question)
        self.input_win.refresh()
        curses.curs_set(1)
        self.text_in.edit()
        answer = self.text_in.gather()
        curses.curs_set(0)
        self.input_win.erase()
        self.input_win.refresh()
        return answer

    def write_to(self, index, value):
        row, col = divmod(index, self.cells_per_row)
        self.array_win.addstr(row, col * CELL_WIDTH, value)
        self.array_win.refresh()

    def highlight(self, index, color_pair):
        row, col = divmod(index, self.cells_per_row)
        self.array_win.chgat(row, col * CELL_WIDTH, 1, curses.color_pair(color_pair))
        self.array_win.refresh()

if __name__ == '__main__':
    TEST()
