class Computer:
    input_str = 'RUNNING DIAGNOSTIC...\nEnter System ID: '

    def __init__(self, int_code, verbose=False):
        self.parameter_modes = {'0':lambda x: self.read(x),
                                '1':lambda x: x}

        self.instructions = {'01':lambda x, y, out: self.write(x + y, out),
                             '02':lambda x, y, out: self.write(x * y, out),
                             '03':lambda out: self.write(int(input(self.input_str)), out),
                             '04':lambda x: print(self.output_msg(x)),
                             '05':lambda x, y: self.move(address=y) if x else None,
                             '06':lambda x, y: self.move(address=y) if not x else None,
                             '07':lambda x, y, out: self.write(int(x < y), out),
                             '08':lambda x, y, out: self.write(int(x == y), out),
                             '99':None}

        self.int_code = int_code
        self.verbose = verbose

    def output_msg(self, out):
        return  f'DIAGNOSTIC CODE: {out}' if out else 'OK'

    def reset(self):
        """
        Set instruction_pointer to 0 and reinitialize our memory.
        """
        self.instruction_pointer = 0
        self.memory = self.int_code.copy()

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

    def move(self, incr=1, *, address=None):
        """
        Increment instruction_pointer by incr if address is None else change
        instruction_pointer to address.
        """
        self.instruction_pointer = address if address else self.instruction_pointer + incr

    def parse_modes(self, read_str, instruction):
        """
        Parse modes by filling read_str with leading '0's so that len(modes) == n_params.

        If instruction writes out, the mode corresponding to out variable is replaced with '1'.
        (Writes must be in immediate mode.)
        """
        n_params = instruction.__code__.co_argcount
        modes = list(reversed(read_str.zfill(n_params)))
        if 'out' in instruction.__code__.co_varnames:
            modes[instruction.__code__.co_varnames.index('out')] = '1'

        return map(self.parameter_modes.get, modes)

    def compute_iter(self, *, noun=None, verb=None):
        """
        Returns an iterator, each item being current instruction_pointer of the computation,
        except the last item.

        The last item is:
            self.read(0): if the computation halts and noun and verb aren't None
                       0: if the computation halts and noun or verb is None
                      -1: if we reach end of data without halting
                      -2: if we receive an incorrect op_code or parameter mode
        """
        self.reset()
        if not (noun is None or verb is None):
            self.write(noun, 1)
            self.write(verb, 2)

        try:
            while True:
                unparsed = str(self.read())
                op_code = unparsed[-2:].zfill(2)

                instruction = self.instructions[op_code]

                if instruction is None: # Halt
                    if self.verbose:
                        print('Exitcode: 0')
                    if noun and verb:
                        yield self.read(0)
                    else:
                        yield 0
                    break

                modes = self.parse_modes(unparsed[:-2], instruction)

                parameters = (mode(self.read()) for mode in modes)

                instruction(*parameters)

                yield self.instruction_pointer

        except IndexError:
            if self.verbose:
                print('Exitcode: -1')
            yield -1

        except KeyError:
            if self.verbose:
                print('Exitcode: -2')
            yield -2

    def compute(self, *, noun=None, verb=None):
        """
        Returns the last item of compute_iter
        """
        for result in self.compute_iter(noun=noun, verb=verb):
            pass
        return result
