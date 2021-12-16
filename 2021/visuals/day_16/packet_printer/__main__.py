from io import StringIO

from . import BITS
from .packet import Packet

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


print(decode(StringIO(BITS)))
