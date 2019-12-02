class Computer:
    def __init__(self, int_code, instructions=None):
        if instructions is None:
            self.instructions = {1:lambda x, y, out: self.write(self.read(x) + self.read(y), out),
                                 2:lambda x, y, out: self.write(self.read(x) * self.read(y), out),
                                 99:None}
        else:
            self.instructions = instructions
        self.int_code = int_code

    def reset(self):
        """
        Reset our head and reinitialize our memory.
        """
        self.instruction_pointer = 0
        self.memory = self.int_code.copy()

    def read(self, address=None):
        """
        Return the value at instruction_pointer if address is None else return the value at
        address.
        """
        if address is None:
            address=self.instruction_pointer
        return self.memory[address]

    def write(self, value, address=None):
        """
        Write the value at the given address or at instruction_pointer if address is None.
        """
        if address is None:
            address=self.instruction_pointer
        self.memory[address] = value

    def move(self, incr=1, address=None):
        """
        Increment instruction_pointer by incr if address is None else change
        instruction_pointer to address.
        """
        if address is not None:
            self.instruction_pointer = address
            return True
        self.instruction_pointer += incr
        return True

    def compute_iter(self, noun=None, verb=None):
        """
        Returns an iterator, each item being current head position of the computation, except
        the last item. The last item is memory at index 0 if the program halts else -1.

        -1 indicates an error in the data. (Either an incorrect op_code,
                                            or reached end of data without halting.)
        """
        self.reset()
        if noun is not None and verb is not None:
            self.write(noun, 1)
            self.write(verb, 2)

        while True:
            try:
                op_code = self.read()
            except IndexError:
                yield -1
                break

            if op_code not in self.instructions:
                yield -1
                break

            operator = self.instructions[op_code]

            if operator is None: #Halt
                yield self.read(0)
                break

            argcount = operator.__code__.co_argcount

            try:
                operator(*(self.read() for _ in range(argcount) if self.move()))
            except IndexError:
                yield -1
                break

            yield self.instruction_pointer
            self.move()

    def compute(self, noun, verb):
        """
        Returns the last item of compute_iter
        """
        for result in self.compute_iter(noun, verb):
            pass
        return result

if __name__ == "__main__":
    from itertools import product

    with open('input', 'r') as data:
        data = list(map(int, data.read().split(',')))

    #Part1
    tape = Computer(data)
    print(tape.compute(12, 2))

    #Part2
    for i, j in product(range(100), repeat=2):
        if tape.compute(i, j) == 19690720: #Date of moon landing
            print(100 * i + j)
            break
