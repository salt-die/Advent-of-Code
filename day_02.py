from itertools import product

with open('input', 'r') as data:
    data = list(map(int, data.read().split(',')))

class TuringTape:
    def __init__(self):
        self.translate = {1:lambda x, y, out: self.write(self.read(x) + self.read(y), out),
                          2:lambda x, y, out: self.write(self.read(x) * self.read(y), out),
                          99:None}

    def reset(self, data=data):
        """
        Reset our head and reinitialize our memory.
        """
        self.head_position = 0
        self.memory = data.copy()

    def read(self, address=None):
        """
        Return the value at current head position if address is None

        Else return the value at address
        """
        if address is None:
            address=self.head_position
        return self.memory[address]

    def write(self, value, address=None):
        """
        Write the value at the given address or at head_position if address is None.
        """
        if address is None:
            address=self.head_position
        self.memory[address] = value

    def move(self, incr=1, address=None):
        """
        Increment head_position by incr if address is None else move head to address.
        """
        if address is not None:
            self.head_position = address
            return True
        self.head_position += incr
        return True

    def compute_iter(self, noun, verb):
        """
        Returns an iterator, each item being current head position of the computation, except
        the last item. The last item is memory at index 0 if the program halts else -1.

        -1 indicates an error in the data. (Either an incorrect op_code,
                                            or reached end of data without halting.)
        """
        self.reset()
        self.write(noun, 1)
        self.write(verb, 2)

        while True:
            try:
                op_code = self.read()
            except IndexError:
                yield -1
                break

            if op_code not in self.translate:
                yield -1
                break

            operator = self.translate[op_code]

            if operator is None: #Halt
                yield self.read(0)
                break

            argcount = operator.__code__.co_argcount

            try:
                args = [self.read() for _ in range(argcount) if self.move()]
                operator(*args)
            except IndexError:
                yield -1
                break

            yield self.head_position
            self.move()

    def compute(self, noun, verb):
        """
        Returns the last item of compute_iter
        """
        for result in self.compute_iter(noun, verb):
            pass
        return result


#Part1
tape = TuringTape()
print(tape.compute(12, 2))

#Part2
for i, j in product(range(100), repeat=2):
    if tape.compute(i, j) == 19690720: #Date of moon landing
        print(100 * i + j)
        break
