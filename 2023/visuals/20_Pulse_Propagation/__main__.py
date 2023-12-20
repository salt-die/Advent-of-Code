import asyncio
from collections import deque
from itertools import count
from math import lcm

import aoc_lube
from aoc_theme import AOC_GREY, AOC_PRIMARY
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets.text import Text

RED = Color.from_hex("dd3330")
GREEN = Color.from_hex("22cc39")
BLUE = Color.from_hex("3268d3")


def parse_input():
    for line in aoc_lube.fetch(year=2023, day=20).splitlines():
        name, outputs = line.split(" -> ")
        yield name[1:], (name[0], outputs.split(", "))


def inputs(module):
    return (in_ for in_, (_, outs) in MODULES.items() if module in outs)


def init_states():
    return {
        module: 0 if type_ == "%" else dict.fromkeys(inputs(module), 0)
        for module, (type_, _) in MODULES.items()
        if type_ != "b"
    }


async def cycle(states, on_progress):
    queue = deque([("button", "broadcaster", 0)])

    while queue:
        src, dst, signal = queue.popleft()
        await on_progress(src, dst, signal)

        if dst not in MODULES:
            continue

        type_, outs = MODULES[dst]
        if type_ == "%":
            if signal:
                continue

            states[dst] ^= 1
            output_signal = states[dst]
        elif type_ == "&":
            memory = states[dst]
            memory[src] = signal
            output_signal = not all(memory.values())
        else:
            output_signal = signal

        queue.extend((dst, out, output_signal) for out in outs)


MODULES = dict(parse_input())
MODULES["broadcaster"] = MODULES["roadcaster"]
UP = "⇧"
DN = "⇩"
CYCLER_TEMPLATE = """\
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│    │⇨│    │⇨│    │⇨│    │⇨│    │⇨│    │⇨│    │⇨│    │⇨│    │⇨│    │⇨│    │⇨│    │
└────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘
  ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧     ⇩⇧
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘"""


class PulseApp(App):
    async def on_start(self):
        states = init_states()
        cyclers = {
            module
            for module, state in states.items()
            if isinstance(state, dict) and len(state) > 4
        }

        cycler_labels = [
            Text(pos=(i * 7, 22), default_color_pair=AOC_PRIMARY)
            for i in range(len(cyclers))
        ]
        for label in cycler_labels:
            label.set_text(CYCLER_TEMPLATE)

        positions = {}
        for cycler, label in zip(cyclers, cycler_labels):
            positions[cycler] = label
            label.colors[..., :3] = RED
            label.colors[1, 6::7, :3] = AOC_GREY
            label.colors[3, :, :3] = AOC_GREY
            label.add_str(cycler, (5, 41))
            for out in MODULES["roadcaster"][1]:
                if cycler in MODULES[out][1]:
                    break

            i = 0
            while True:
                label.add_str(out, (1, 2 + i * 7))
                if cycler not in MODULES[out][1]:
                    label.add_str(" ", (3, 2 + i * 7))
                if out not in MODULES[cycler][1]:
                    label.add_str(" ", (3, 3 + i * 7))
                positions[out] = (label, i)

                out = next(
                    (module for module in MODULES[out][1] if module != cycler), None
                )
                if not out:
                    break

                i += 1

        broadcast_label = Text(
            size=(len(cyclers) * 7, 22), default_color_pair=AOC_PRIMARY
        )
        broadcast_label.add_border()
        broadcast_label.add_str("Cycles:    0", (1, 1))

        self.add_gadgets(broadcast_label, *cycler_labels)

        (rx_in,) = inputs("rx")
        sources = [*inputs(rx_in)]
        cyclers_to_sources = {src: next(inputs(src)) for src in sources}

        npresses = []

        async def on_progress(src, dst, signal):
            if signal and dst == rx_in:
                npresses.append(i)
                broadcast_label.add_str(
                    f"{cyclers_to_sources[src]} cycle: {i:>4}", (len(npresses) + 1, 1)
                )

            broadcast_label.add_str(f"Cycles: {i:>4}", (1, 1))

            if src in cyclers:
                cycler = positions[src]
                cycler.colors[4:, :, :3] = (
                    GREEN if not all(states[src].values()) else RED
                )
                if dst in positions:
                    _, pos = positions[dst]
                    cycler.colors[3, 3 + pos * 7, :3] = GREEN if signal else RED
                    await asyncio.sleep(0)
                    cycler.colors[3, 3 + pos * 7, :3] = AOC_GREY
            elif src in positions:
                cycler, pos = positions[src]
                cycler.colors[0:3, pos * 7 : (pos + 1) * 7 - 1, :3] = (
                    GREEN if states[src] else RED
                )
                if dst in cyclers:
                    cycler.colors[3, 2 + pos * 7, :3] = GREEN if signal else RED
                    await asyncio.sleep(0)
                    cycler.colors[3, 2 + pos * 7, :3] = AOC_GREY
                elif dst in positions:
                    cycler.colors[1, pos * 7 + 6, :3] = GREEN if signal else RED
                    await asyncio.sleep(0)
                    cycler.colors[1, pos * 7 + 6, :3] = AOC_GREY

        for i in count(1):
            await cycle(states, on_progress)
            if len(npresses) == len(states[rx_in]):
                break

        broadcast_label.add_str(f"LCM: {lcm(*npresses)}", (len(npresses) + 2, 1))


if __name__ == "__main__":
    PulseApp(title="Pulse Propagation", background_color_pair=AOC_PRIMARY).run()
