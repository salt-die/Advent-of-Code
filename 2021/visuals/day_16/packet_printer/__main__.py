from io import StringIO
from itertools import islice

from . import BITS
from .packet import Packet

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

print(next(decoder(StringIO(BITS))))
