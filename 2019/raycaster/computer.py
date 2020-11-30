from collections.abc import Iterable
from collections import deque

class Computer:
    def __init__(self, int_code, memory=10000):
        self.parameter_modes = {'0':lambda x: self.read(x),
                                '0o': lambda x: x,
                                '1':lambda x: x,
                                '2':lambda x: self.read(x + self.relative_base),
                                '2o':lambda x: x + self.relative_base}

        self.instructions = {'01':lambda x, y, out: self.write(x + y, out),
                             '02':lambda x, y, out: self.write(x * y, out),
                             '03':lambda out: self.write(self.feed.pop(), out),
                             '04':lambda x: self.out.appendleft(x),
                             '05':lambda x, y: self.move(address=y) if x else None,
                             '06':lambda x, y: self.move(address=y) if not x else None,
                             '07':lambda x, y, out: self.write(int(x < y), out),
                             '08':lambda x, y, out: self.write(int(x == y), out),
                             '09':lambda x: self.move(relative_base_incr=x),
                             '99':None}

        self.int_code = int_code + [0] * memory
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
        If address is given, move instruction_pointer to address
        Else if relative_base_incr is given, increment relative_base by relative_base_incr
        Else increment instruction_pointer by incr

        Passing multiple keywords to this method not suggested.
        """
        if address is not None:
            self.instruction_pointer = address
        elif relative_base_incr is not None:
            self.relative_base += relative_base_incr
        else:
            self.instruction_pointer += incr

    def parse_modes(self, read_str, instruction):
        """
        Parse modes by filling read_str with leading '0's so that len(modes) == number of
        instruction parameters.

        If instruction writes out, the mode corresponding to an out parameter has 'o' appended
        to it. (We take into account that self.write already interprets out parameters as
        positions.)
        """
        names = instruction.__code__.co_varnames
        modes = reversed(read_str.zfill(len(names)))
        return [mode + 'o'[name != 'out':] for mode, name in zip(modes, names)]

    def connect(self, new_feed):
        """
        If new_feed is a Computer we'll connect that Computer's *out* to our *in*.

        If new_feed is a deque, we'll move existing items in feed to new_feed then set
        self.feed to new_feed.

        Else if new_feed is an iterable we'll move items from that iterable into our feed.

        Else we'll place new_feed on top of the stack.
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

    __lshift__ = connect # '<<' functionality for connect method

    def pop(self):
        """
        Shortcut to retrieve oldest output.
        """
        return self.out.pop()

    def last(self):
        """
        Shortcut to retrieve newest output.
        """
        return self.out.popleft()

    def __len__(self):
        """
        Shortcut to check length of self.out.
        """
        return len(self.out)

    def __bool__(self):
        """
        Shortcut for checking if we've produced output.
        """
        return bool(self.out)

    def compute_iter(self, feed=None):
        """
        Returns an iterator, each item being (instruction_pointer, op_code, modes, parameters,
        pamaraters with modes applied) of the current state of computation.
        """
        self.reset()

        if feed is not None:
            self << feed

        while True:
            unparsed = str(self.read())
            op_code = unparsed[-2:].zfill(2)

            instruction = self.instructions[op_code]

            if instruction is None: # Halt
                yield self.instruction_pointer - 1, op_code, [], [], []
                break

            modes = self.parse_modes(unparsed[:-2], instruction)
            mapped_modes = map(self.parameter_modes.get, modes)
            params = [self.read() for _ in modes]
            moded_params = [mode(param) for mode, param in zip(mapped_modes, params)]

            yield self.instruction_pointer - len(modes) - 1, op_code, modes, params, moded_params
            instruction(*moded_params)

    def __iter__(self):
        """
        Iterator functionality.
        """
        return self.compute_iter()

    def compute(self, feed=None):
        """
        Returns the last item of compute_iter.
        """
        for result in self.compute_iter(feed):
            pass
        return result

    def compute_n(self, niter, feed=None):
        """
        Run self.compute niter times.
        """
        all_outs = []
        if feed is not None:
            self << feed
        for _ in range(niter):
            self.compute()
            all_outs.extend(reversed(self.out))
        return all_outs
