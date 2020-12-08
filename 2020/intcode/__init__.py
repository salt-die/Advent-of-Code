ACC = "acc"
JMP = "jmp"
NOP = "nop"

class CycleError(Exception):
    ...

class Computer:
    def __init__(self, data):
        self.data = data

    def load(self):
        head = acc = 0
        while True:
            op, value = yield head, acc
            if op == ACC:
                acc += value
                head += 1
            elif op == JMP:
                head += value
            elif op == NOP:
                head += 1
            else:
                raise ValueError("Bad OP: ", op)

    def run(self):
        data = self.data
        cycle_detector = set()
        program = self.load()
        head, acc = next(program)

        while True:
            if head in cycle_detector:
                raise CycleError(acc)
            if head == len(data):
                raise EOFError(acc)
            cycle_detector.add(head)
            head, acc = program.send(data[head])

    def fsck(self):
        """File-system check and repair."""
        data = self.data
        for address, (instruction, value) in enumerate(data):
            if instruction == ACC:
                continue

            data[address] = (NOP, value) if instruction == JMP else (JMP, value)
            try:
                self.run()
            except CycleError:
                pass
            except EOFError as e:
                return e.args[0]
            data[address] = (instruction, value)
