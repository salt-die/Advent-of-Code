"""
Network simulator for D7P2 of Advent of Code 2019.
"""
from collections import deque
from computer import Computer
import curses
from curses.textpad import Textbox, rectangle
from itertools import cycle
import time

computers=[
'    / ======= \         / ======= \         / ======= \         / ======= \         / ======= \    ',
'   / __________\       / __________\       / __________\       / __________\       / __________\   ',
'  | ___________ |     | ___________ |     | ___________ |     | ___________ |     | ___________ |  ',
'  | |         | |     | |         | |     | |         | |     | |         | |     | |         | |  ',
'  | |         | |     | |         | |     | |         | |     | |         | |     | |         | |  ',
'  | |_________| |=-,  | |_________| |=-,  | |_________| |=-,  | |_________| |=-,  | |_________| |  ',
"  \\=____________/   '=\\=____________/   '=\\=____________/   '=\\=____________/   '=\\=____________/  ",
'  / """"""""""" \\     / """"""""""" \\     / """"""""""" \\     / """"""""""" \\     / """"""""""" \\  ',
' / ::::::::::::: \\   / ::::::::::::: \\   / ::::::::::::: \\   / ::::::::::::: \\   / ::::::::::::: \\ ',
'(_________________) (_________________) (_________________) (_________________) (_________________)']

class Window:
    def __init__(self):
        self.deques = [deque(maxlen=2) for i in range(5)]
        self.init_scr()
        self.setup()
        self.start()
        self.end_curses()

    def start(self):
        time.sleep(1)
        self.display('Welcome to the Intcode Network Tester (INT). Any key to continue...')
        self.input_win.getch()
        self.display('Setting up Network')
        self.draw_network()
        self.display('Network Configured.')
        time.sleep(.5)
        self.pre_compute(first_time=True)
        self.display('Network Ready. Any key to continue...')
        self.input_win.getch()
        running = True
        while running:
            self.display('Computing')
            for i, program, computer in cycle(zip(range(5), self.programs, self.network)):
                self.dots(self.title_win, 0, 9)
                for _ in program:
                    if computer: # Produced output
                        self.computer_display(i, f'{computer.out[-1]}')
                        self.send(i)
                        break
                else:
                    result = self.network[-1].pop()
                    self.computer_display(4, f'{result}')
                    self.display(f"Computation complete. Final result: {result}. 'q' to quit or any key to continue...")
                    break
                time.sleep(.5)
            running = self.input_win.getch() not in (ord('q'), ord('Q'))
            if running:
                self.pre_compute()

    def send(self, computer):
        if computer == 5:
            return
        for col in range(17, 20):
            self.network_win.chgat(self.top + 5, self.left + col + 20 * computer, 1, curses.A_BOLD)
            self.network_win.refresh()
            time.sleep(.05)
        for col in range(20, 22):
            self.network_win.chgat(self.top + 6, self.left + col + 20 * computer, 1, curses.A_BOLD)
            self.network_win.refresh()
            time.sleep(.05)
        for col in range(17, 20):
            self.network_win.chgat(self.top + 5, self.left + col + 20 * computer, 1, curses.color_pair(1))
            self.network_win.refresh()
            time.sleep(.05)
        for col in range(20, 22):
            self.network_win.chgat(self.top + 6, self.left + col + 20 * computer, 1, curses.color_pair(1))
            self.network_win.refresh()
            time.sleep(.05)

    def dots(self, win, row, column, n=3, attributes=None):
        dots = n - round(2 * time.time()) % (n + 1)
        dot_str = '.' * n + ' ' * n
        if attributes is None:
            win.addstr(row, column, dot_str[dots:dots + n])
        else:
            win.addstr(row, column, dot_str[dots:dots + n], attributes)
        win.refresh()

    def draw_network(self):
        height, width = self.network_win.getmaxyx()
        self.top = top = (height - len(computers)) // 2
        self.left = left = (width - len(computers[0])) // 2
        self.network_win.erase()
        for row, line in enumerate(computers, start=top):
            for col, char in enumerate(line, start=left):
                self.network_win.addstr(row, col, char)
                self.network_win.refresh()
                self.dots(self.title_win, 0, 18)
                time.sleep(.003)

    def pre_compute(self, first_time=False):
        if first_time:
            with open(self.ask('Please Enter filename: ').strip(), 'r') as data:
                    self.data = list(map(int, data.read().split(',')))

        self.network = [Computer(int_code=self.data) for _ in range(5)]
        for i in range(5): # Setup network
            self.network[i] << self.network[i - 1]

        if first_time:
            self.display('Loading')
            self.boot_sequence()

        phase_settings = self.ask('Please enter phase setting: ').replace(' ', '')
        self.programs = [pc.compute_iter(feed=int(digit))
                         for pc, digit in zip(self.network, phase_settings)]
        self.network[0] << 0

        for i, setting in enumerate(phase_settings):
            self.computer_display(i, f'{setting}')
            self.network_win.refresh()
            time.sleep(.1)

    def boot_sequence(self):
        for i in range(5):
            self.network_win.chgat(self.top + 6, self.left + 3 + 20 * i, 1, curses.color_pair(3))
            self.network_win.refresh()
            time.sleep(.01)
            self.computer_display(i, 'Loading')

        now = time.time()
        while time.time() - now < 3:
            self.dots(self.title_win, 0, 7)
            for i in range(5):
                self.dots(self.network_win, self.top + 3, self.left + 12 + 20 * i, 2, curses.A_BOLD)
        for i in range(5):
            self.computer_display(i, 'Ready...')
            self.network_win.chgat(self.top + 6, self.left + 3 + 20 * i, 1, curses.color_pair(2))
        time.sleep(.5)
        self.network_win.refresh()

    def init_scr(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.keypad(True)
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.screen.attron(curses.color_pair(1))

    def end_curses(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.flushinp()
        curses.endwin()

    def setup(self):
        screen = self.screen
        height, width = self.screen.getmaxyx()

        # Title
        rectangle(screen, 0, 0, 2, width - 2)
        self.title_win = curses.newwin(1, width - 4, 1, 2)

        # Network Vis
        rectangle(screen, 3, 0, height - 4, width - 2)
        self.network_win = curses.newwin(height - 8, width - 4, 4, 2)
        self.network_win.attron(curses.color_pair(1))

        # Input
        rectangle(screen, height - 3,  0, height - 1, width - 2)
        self.input_win = curses.newwin(1, width - 4, height - 2, 2)
        self.text_in = Textbox(self.input_win)

        self.screen.refresh()
        curses.doupdate()

    def display(self, out):
        self.title_win.erase()
        for col, char in enumerate(out):
            self.title_win.addstr(0, col, char)
            self.title_win.refresh()
            time.sleep(.01)

    def computer_display(self, computer, output):
        self.deques[computer].append(output)
        for row, line in enumerate(self.deques[computer]):
            self.network_win.addstr(self.top + 3 + row, self.left + 5 + 20 * computer, ' ' * 9)
        for row, line in enumerate(self.deques[computer]):
            self.network_win.addstr(self.top + 3 + row, self.left + 5 + 20 * computer,
                                    line, curses.A_BOLD)
            self.network_win.refresh()
            time.sleep(.1)
        self.network_win.addstr(self.top + 3 + len(self.deques[computer]) - 1,
                                self.left + 5 + 20 * computer + len(output), '_',
                                curses.A_BOLD | curses.A_BLINK)
        self.network_win.refresh()
        time.sleep(.1)

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

if __name__ == '__main__':
    Window()
