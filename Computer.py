class Computer:
    input_str = 'RUNNING DIAGNOSTIC\nEnter System ID: '

    def __init__(self, int_code, verbose=False):
        self.parameter_modes = {'0':lambda x:self.read(x),
                                '1':lambda x:x}

        self.instructions = {'01':lambda x, y, out: self.write(x + y, out),
                             '02':lambda x, y, out: self.write(x * y, out),
                             '03':lambda out: self.write(int(input(self.input_str)), out),
                             '04':lambda out: print(self.output_msg(out)),
                             '05':lambda x, y: self.move(address=y) if x else None,
                             '06':lambda x, y: self.move(address=y) if not x else None,
                             '07':lambda x, y, out: self.write(int(x < y), out),
                             '08':lambda x, y, out: self.write(int(x == y), out),
                             '99':None}

        self.int_code = int_code
        self.verbose = verbose

    def output_msg(self, out):
        return  f'Test Complete\nDIAGNOSTIC CODE: {out}' if out else 'OK'

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

    def move(self, incr=1, address=None):
        """
        Increment instruction_pointer by incr if address is None else change
        instruction_pointer to address.
        """
        self.instruction_pointer = address if address else self.instruction_pointer + incr

    def parse_modes(self, read_str, n_params, op_code):
        """
        Parse modes by filling read_str with leading '0's so that len(modes) == n_params.
        Leading '0' replaced with '1' if op_code instruction writes. (Writes must be in
        immediate mode.)
        """
        if op_code in '040506':
            return read_str.zfill(n_params)
        return f'1{read_str.zfill(n_params - 1)}'

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

                # Account for an arbitrary number of instruction parameters.
                parameter_count = instruction.__code__.co_argcount

                modes = self.parse_modes(unparsed[:-2], parameter_count, op_code)

                parameters = (self.parameter_modes[mode](self.read()) for mode in reversed(modes))

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
