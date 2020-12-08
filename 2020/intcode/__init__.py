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
                raise CycleError(acc, cycle_detector)
            if head == len(data):
                raise EOFError(acc)
            cycle_detector.add(head)
            head, acc = program.send(data[head])

    def fsck(self):
        """File-system check and repair."""
        data = self.data

        # Corruption must happen in some address we visit during the first run.
        # We create a stack of these addresses:
        try:
            self.run()
        except CycleError as e:
            needs_check = list(e.args[1])

        while needs_check:
            address = needs_check.pop()
            op, val = data[address]
            if op == ACC:
                continue

            data[address] = (NOP, val) if op == JMP else (JMP, val)
            try:
                self.run()
            except CycleError:
                pass
            except EOFError as e:
                return e.args[0]
            data[address] = op, val