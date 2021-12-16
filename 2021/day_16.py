from dataclasses import dataclass
from io import StringIO
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

PACKET = StringIO(
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

def decode(packet: StringIO):
    version = decimal(packet.read(3))
    type_id = decimal(packet.read(3))

    if type_id == 4:
        value = ""

        while packet.read(1) == "1":
            value += packet.read(4)

        value += packet.read(4)

        return Packet(version, type_id, decimal(value))

    match packet.read(1):
        case "0":
            bit_length = decimal(packet.read(15))
            subpacket = StringIO(packet.read(bit_length))

            subpackets = [ ]
            while subpacket.tell() != bit_length:
                subpackets.append(decode(subpacket))

            return Packet(version, type_id, subpackets)

        case "1":
            npackets = decimal(packet.read(11))

            return Packet(version, type_id, [decode(packet) for _ in range(npackets)])

DECODED = decode(PACKET)

def part_one():
    return sum(DECODED.versions())

def part_two():
    return DECODED.evaluate()

aoc_helper.submit(16, part_one)
aoc_helper.submit(16, part_two)
