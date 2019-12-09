from collections.abc import Iterable
from collections import deque

input_str = 'DIAGNOSTICS\nEnter System ID: '

def output_msg(x):
    print(f'DIAGNOSTIC CODE: {x}') if x else print('OK')


class Computer:
    def __init__(self, int_code, verbose=False):
        self.parameter_modes = {'0':lambda x: self.read(x),
                                '1':lambda x: x,
                                '2':lambda x: self.read(x + self.relative_base),
                                '2o':lambda x: x + self.relative_base}

        self.instructions = {'01':lambda x, y, out: self.write(x + y, out),
                             '02':lambda x, y, out: self.write(x * y, out),
                             '03':lambda out: self.write(int(input(input_str)), out),
                             '04':output_msg,
                             '05':lambda x, y: self.move(address=y) if x else None,
                             '06':lambda x, y: self.move(address=y) if not x else None,
                             '07':lambda x, y, out: self.write(int(x < y), out),
                             '08':lambda x, y, out: self.write(int(x == y), out),
                             '09':lambda x: self.move(relative_base_incr=x),
                             '99':None}

        self.int_code = int_code + [0] * 10000
        self.verbose = verbose
        self.last_write_to = -1
        self.feed = deque()
        self.out = deque()

    def reset(self):
        """
        Set instruction_pointer to 0, reinitialize our memory, and dump self.out.
        """
        self.relative_base = 0
        self.instruction_pointer = 0
        self.memory = self.int_code.copy()
        self.out.clear()

    def read(self, address=None):
        """
        Return the value at instruction_pointer and increment_instruction pointer if address
        is None else return the value at address.
        """
        if address is None:
            address = self.instruction_pointer
            self.move()
        return self.memory[address]

    def write(self, value, address=None):
        """
        Write the value at the given address or at instruction_pointer if address is None.
        """
        if address is None:
            address = self.instruction_pointer
        self.memory[address] = value
        self.last_write_to = address

    def move(self, *, incr=1, address=None, relative_base_incr=None):
        """
        Increment instruction_pointer by incr if address is None else change
        instruction_pointer to address.
        """
        if relative_base_incr is not None:
            self.relative_base += relative_base_incr
            return
        self.instruction_pointer = address if address else self.instruction_pointer + incr

    def parse_modes(self, read_str, instruction):
        """
        Parse modes by filling read_str with leading '0's so that len(modes) == number of
        instruction parameters.

        If instruction writes out, the mode corresponding to out variable is replaced with '1'
        if '0' or '2o' if '2'.
        (self.write already interprets out values as positions.)
        """
        modes = list(reversed(read_str.zfill(instruction.__code__.co_argcount)))
        var_names = instruction.__code__.co_varnames
        if 'out' in var_names:
            index = var_names.index('out')
            modes[index] = '2o' if modes[index] == '2' else '1'
        return modes

    def connect(self, new_feed):
        """
        If new_feed is a Computer we'll connect that Computer's *out* to our *in*.

        If new_feed is a deque, we'll move existing items in feed to new_feed then set
        self.feed to new_feed.

        Else if new_feed is an iterable we'll move items from that iterable into our feed.

        Else we'll place new_feed on top of the stack.

        Lastly, we change the default *out* and *in* that we write/print to.
        """
        if isinstance(new_feed, Computer):
            self << new_feed.out
        elif isinstance(new_feed, deque):
            new_feed.extend(self.feed)
            self.feed = new_feed
        elif isinstance(new_feed, Iterable):
            for item in new_feed:
                self.feed.appendleft(item)
        else:
            self.feed.append(new_feed) # We may appendleft in the future.

        self.instructions['03'] = lambda out: self.write(self.feed.pop(), out)
        self.instructions['04'] = lambda x: self.out.appendleft(x)

    __lshift__ = connect # '<<' functionality for connect method

    def pop(self):
        """
        Shortcut to retrieve oldest output.
        """
        return self.out.pop()

    def __bool__(self):
        """
        Shortcut for checking if we've produced output.
        """
        return bool(self.out)

    def compute_iter(self, *, noun=None, verb=None, feed=None):
        """
        Returns an iterator, each item being (instruction_pointer, op_code, modes)
        except, possibly, the last item.

        The last item is:
            -1: if we reach end of data without halting
            -2: if we receive an incorrect op_code or parameter mode
        """
        self.reset()

        if not (noun is None or verb is None):
            self.write(noun, 1)
            self.write(verb, 2)

        if feed is not None:
            self << feed

        try:
            while True:
                unparsed = str(self.read())
                op_code = unparsed[-2:].zfill(2)

                instruction = self.instructions[op_code]

                if instruction is None: # Halt
                    if self.verbose:
                        print('Exitcode: 0')
                    yield self.instruction_pointer - 1, op_code, []
                    break

                modes = self.parse_modes(unparsed[:-2], instruction)

                mapped_modes = map(self.parameter_modes.get, modes)

                parameters = (mode(self.read()) for mode in mapped_modes)

                yield self.instruction_pointer - 1, op_code, modes

                instruction(*parameters)

        except IndexError:
            if self.verbose:
                print('Exitcode: -1')
            yield -1, '', []

        except KeyError:
            if self.verbose:
                print('Exitcode: -2')
            yield -2, '', []

    def compute(self, *args, **kwargs):
        """
        Returns the last item of compute_iter
        """
        for result in self.compute_iter(*args, **kwargs):
            pass
        return result
