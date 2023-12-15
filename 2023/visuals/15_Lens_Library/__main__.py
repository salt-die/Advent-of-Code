import asyncio

import aoc_lube
from aoc_theme import AOC_PRIMARY, AOC_THEME, WHITE, AocToggle
from batgrl.app import App
from batgrl.colors import Color, rainbow_gradient
from batgrl.gadgets.progress_bar import ProgressBar
from batgrl.gadgets.text import Text

INIT_SEQUENCE = aoc_lube.fetch(year=2023, day=15).split(",")
RAINBOW = rainbow_gradient(9)

# Note that the max number of lenses a box contains at any point for my input is 6, so the
# size of our boxes is just big enough to fit 6 lenses. Not guaranteed to work on your input!
NLENS = 6
LENS_BOX = "┄)┄┄┄┄┄┄)┄"
BH, BW = 1, 10
LO = 2  # Lens offset
NROWS = 32
NCOLS = 8


def box_pos(n):
    row, column = divmod(n, 8)
    return row * BH, column * BW


def hash(string):
    total = 0
    for char in string:
        total += ord(char)
        total *= 17
    return total % 256


def color_blend(a: Color, b: Color):
    return Color((a.red + b.red) // 2, (a.green + b.green) // 2, (a.blue + b.blue) // 2)


class LensApp(App):
    async def on_start(self):
        boxes_label = Text(
            size=(NROWS * BH, NCOLS * BW), default_color_pair=AOC_PRIMARY
        )
        for i in range(256):
            y, x = box_pos(i)
            boxes_label.add_str(LENS_BOX, (y, x))
            boxes_label.canvas[["overline", "underline"]][y, x + 1 : x + BW - 2] = True

        pause_event = asyncio.Event()
        pause_event.set()

        def pause(state):
            if state == "on":
                pause_event.clear()
            else:
                pause_event.set()

        pause_button = AocToggle("PAUSE", pause, pos=(3, 8))

        delay = 0.2

        def go_fast(state):
            nonlocal delay
            if state == "on":
                delay = 0
            else:
                delay = 0.5

        fast_button = AocToggle("TURBO", go_fast, pos=(4, 8))
        progress = ProgressBar(size=(1, 28), pos=(2, 1))
        info_label = Text(
            size=(6, 30),
            pos=(NROWS * BH // 2 - 3, NCOLS * BW + 1),
            default_color_pair=AOC_PRIMARY,
        )
        info_label.add_border()
        info_label.add_gadgets(progress, pause_button, fast_button)

        self.add_gadgets(boxes_label, info_label)

        init_sequence = aoc_lube.fetch(year=2023, day=15).split(",")
        boxes = [{} for _ in range(256)]

        for i, s in enumerate(init_sequence):
            progress.progress = i / (len(init_sequence) - 1)
            await pause_event.wait()

            if s.endswith("-"):
                label = s[:-1]
                box_id = hash(label)
                box = boxes[box_id]
                box.pop(label, None)

                info_label.add_str(
                    f"Removing {label} from {box_id}.".center(28), (1, 1)
                )
            else:
                label, n = s.split("=")
                box_id = hash(label)
                box = boxes[box_id]
                box[label] = int(n)
                info_label.add_str(f"Adding {label} to {box_id}.".center(28), (1, 1))

            row, col = box_pos(box_id)
            col += LO

            boxes_label.add_str(")" * len(box) + "┄" * (NLENS - len(box)), (row, col))
            boxes_label.canvas[row, col + len(box) : col + BW - 4][
                ["overline", "underline"]
            ] = True
            for x, focal in enumerate(box.values(), start=col):
                boxes_label.colors[row, x, :3] = RAINBOW[focal - 1]
            boxes_label.colors[row, col + len(box) : col + NLENS] = AOC_PRIMARY

            current_color = WHITE
            for i, box in enumerate(boxes):
                row, col = box_pos(i)
                boxes_label.colors[row, col, :3] = current_color
                for focal in box.values():
                    current_color = color_blend(current_color, RAINBOW[focal - 1])

                boxes_label.colors[
                    row, col + LO + len(box) : col + BW - 2, :3
                ] = current_color
                boxes_label.colors[row, col + BW - 1, :3] = current_color

            await asyncio.sleep(delay)


if __name__ == "__main__":
    LensApp(
        title="Lens Library", background_color_pair=AOC_PRIMARY, color_theme=AOC_THEME
    ).run()
