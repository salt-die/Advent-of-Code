from dataclasses import dataclass

TYPE_NAMES = {
    0: "sum",
    1: "prod",
    2: "min",
    3: "max",
    5: "gt",
    6: "lt",
    7: "eq",
}

def _snake(head, tail, text):
    first, *rest = text.splitlines()
    yield head + first
    yield from (tail + line for line in rest)

def _tree_printer(root, children):
    yield root

    if not children:
        return

    *children, last = children

    for child in children:
        yield from _snake('├─', '│ ', str(child))

    yield from _snake('╰─', '  ', str(last))


@dataclass
class Packet:
    version: int
    type_id: int
    value: int | list["Packet"]

    def __str__(self):
        if self.type_id == 4:
            return str(self.value)

        return "\n".join(_tree_printer(TYPE_NAMES[self.type_id], self.value))
