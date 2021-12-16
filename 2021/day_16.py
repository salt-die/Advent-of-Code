from dataclasses import dataclass
from io import StringIO
from itertools import islice
from math import prod
from operator import gt, lt, eq

import aoc_helper

TYPE_IDS = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda args: gt(*args),
    6: lambda args: lt(*args),
    7: lambda args: eq(*args),
}

BIT_STREAM = StringIO(
    bin(int(aoc_helper.day(16), 16))[2:]
)


@dataclass
class Packet:
    version: int
    type_id: int
    value: int | list["Packet"]

    def versions(self):
        yield self.version

        if self.type_id != 4:
            for packet in self.value:
                yield from packet.versions()

    def evaluate(self):
        if self.type_id == 4:
            return self.value

        return TYPE_IDS[self.type_id](packet.evaluate() for packet in self.value)


def decimal(bits):
    return int(bits, 2)

def decoder(stream: StringIO):
    version = decimal(stream.read(3) or "0")
    type_id = decimal(stream.read(3) or "0")

    if type_id == 4:
        value = ""

        while stream.read(1) == "1":
            value += stream.read(4)

        value += stream.read(4)

        yield Packet(version, type_id, decimal(value))

    else:
        match stream.read(1):
            case "":
                return

            case "0":
                bit_length = decimal(stream.read(15))
                sub_stream = StringIO(stream.read(bit_length))

                yield Packet(
                    version,
                    type_id,
                    list(decoder(sub_stream)),
                )

            case "1":
                npackets = decimal(stream.read(11))

                yield Packet(
                    version,
                    type_id,
                    list(islice(decoder(stream), npackets)),
                )

    yield from decoder(stream)

DECODED = next(decoder(BIT_STREAM))

def part_one():
    return sum(DECODED.versions())

def part_two():
    return DECODED.evaluate()

aoc_helper.submit(16, part_one)
aoc_helper.submit(16, part_two)
