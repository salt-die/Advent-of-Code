"""
Thermal Environment Supervision Terminal
"""
from collections import deque
from computer import Computer
import curses
from curses.textpad import rectangle
import time
from time import sleep

SLEEP = .01 # For char-by-char printing in output window
SLEEP2 = .1 # For highlighting points and parameters
COMPSLEEP = .5 # Longer sleep to show interpreted parameters

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
                          '09':'BASE-INCR',
                          '99':'HALT',
                          '0':'P',
                          '0o':'P',
                          '1':'I',
                          '2':'R',
                          '2o':'R'}
        self.old_pointer = self.old_nparams = 0
        self.old_write = -1

    def start(self):
        self.setup()
        running = True
        while running:
            #This odd loop is because Computer yields before instructions have executed.
            last_yield = next(self.operation_iterator)
            for computation in self.operation_iterator:
                self.show_computation(*last_yield)
                last_yield = computation
            self.show_computation(*last_yield)
            self.output_win("Press 'q' to quit or any key to continue.")

            is_quitting = self.output_box.getch()

            running = is_quitting not in (ord('q'), ord('Q'))
            if running:
                self.old_pointer = self.old_nparams = self.old_write = 0
                self.pre_compute()
                self.screen.refresh()

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

    def load_intcode(self, message):
        self.output_win(message)

        for i, item in enumerate(self.computer.int_code):
            self.write_to(i, item)
            dots = 3 - round(2*time.time()) % 4
            self.output_box.addstr(0, len(message), "...   "[dots:dots + 3])
            self.output_box.refresh()
            self.screen.refresh()
            sleep(SLEEP)

    def fetch(self, times=1):
        self.output_box.refresh()
        curses.echo()
        curses.curs_set(1)
        system_id = "".join(chr(self.output_box.getch()) for _ in range(times))
        curses.noecho()
        curses.curs_set(0)
        sleep(1)
        return system_id

    def file_open(self, filename):
        with open(f'input{filename}', 'r') as data:
            data = list(map(int, data.read().split(',')))
        self.computer.int_code = data

    def setup(self):
        self.out_win_setup()
        self.output_win("Welcome to the Thermal Environment Supervision Terminal (TEST). Press any key to continue.")
        self.screen.getch()
        self.pre_compute()

    def out_win_setup(self):
        self.height, self.width = self.screen.getmaxyx()
        self.boxes_per_row = self.width // 9
        data_len = len(self.computer.int_code)
        self.out_win_row_start = data_len // self.boxes_per_row + (4 if data_len else 1)

        self.output_box = curses.newwin(self.height - self.out_win_row_start - 1,
                                        self.width - 4, self.out_win_row_start, 1)
        self.output_buffer = deque(maxlen=self.height - self.out_win_row_start - 1)
        self.screen.clear()
        self.output_box.clear()
        self.output_box.refresh()
        rectangle(self.screen, self.out_win_row_start - 1, 0, self.height - 1, self.width - 2)
        self.screen.refresh()

        for i in range(data_len + (-data_len % self.boxes_per_row)):
            self.write_to(i, 0)
            self.screen.refresh()
            sleep(SLEEP)

    def pre_compute(self):
        self.output_win("Please enter two-digit filename: ")
        filename = self.fetch(2)
        self.file_open(filename)
        self.out_win_setup()
        self.load_intcode("Loading Intcode")
        if filename == '02': # 12, 02 for part 1; 70, 14 for part 2
            self.output_win("Enter two-digit noun: ", save=False)
            noun = self.fetch(2)
            self.output_win(f"Enter two-digit noun: {noun}", pause=False)
            noun = int(noun)
            self.write_to(1, noun)
            self.screen.refresh()
            self.output_win("Enter two-digit verb: ", save=False)
            verb = self.fetch(2)
            self.output_win(f"Enter two-digit verb: {verb}", pause=False)
            verb = int(verb)
            self.write_to(2, verb)
            self.screen.refresh()
            self.output_win("Intcode Loaded. Any key to continue.")
            self.output_box.getch()
            self.operation_iterator = self.computer.compute_iter(noun=noun, verb=verb)
        else:
            self.output_win("Intcode Loaded. Enter System ID to begin Diagnostic: ", save=False)
            sys_ID = self.fetch()
            self.output_win(f"Intcode Loaded. Enter System ID to begin Diagnostic: {sys_ID}", pause=False)
            self.operation_iterator = self.computer.compute_iter(feed=int(sys_ID))

    def show_computation(self, pointer, op_code, modes, params, moded_params):
        self.output_win('', pause=False, save=False)
        sleep(SLEEP2)

        op_code = self.translate[op_code]

        if op_code == 'HALT':
            self.output_win("HALT")
            return

        for i in range(self.old_nparams + 1): #Un-highlight
                self.highlight(self.old_pointer + i, 1)
        if self.old_write != -1:
            self.highlight(self.old_write, 5)

        #Highlight pointer and parameters
        self.highlight(pointer, 2)
        if op_code != 'HALT':
            self.output_win(f'{op_code}:', pause=False, save=False)
            self.screen.refresh()
            sleep(SLEEP2)
        for i, mode in enumerate(modes, start=1):
            self.highlight(pointer + i, 3 + int(mode[0]))
            params = ' '.join(f'{self.translate[modes[j]]}{param}'
                              for j, param in enumerate(params[:i]))
            self.output_win(f'{op_code}: {params}', pause=False, save=False)
            self.screen.refresh()
            sleep(SLEEP2)

        #Interpret parameter modes
        for i, mode in enumerate(modes, start=1):
            self.highlight(pointer + i, 2)
        params = ' '.join(f'{moded_param}' for moded_param in moded_params)
        if op_code != 'HALT':
            self.output_win(f'{op_code}: {params}', pause=False)
            self.screen.refresh()
            sleep(COMPSLEEP)

        if op_code == 'OUT':
            self.output_win(f'DIAGNOSTIC CODE: {self.computer.pop()}. Press any key to continue.')
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

    def output_win(self, out, pause=True, save=True):
        self.output_box.clear()

        if save:
            if len(self.output_buffer) and self.output_buffer[-1] == '':
                self.output_buffer[-1] = out
            else:
                self.output_buffer.append(out)
        elif self.output_buffer[-1] != '':
            self.output_buffer.append('')

        last_line = len(self.output_buffer) - 1
        for i, line in enumerate(self.output_buffer):
            if i != last_line:
                self.output_box.addstr(i, 0, line)

        if pause:
            for i, char in enumerate(out):
                self.output_box.addstr(last_line, i, char)
                self.output_box.refresh()
                sleep(SLEEP)
        else:
            self.output_box.addstr(last_line, 0, out)
            self.output_box.refresh()


if __name__=="__main__":
    TEST(Computer(int_code=[], memory=0)).start()
