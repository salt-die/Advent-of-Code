import asyncio

import aoc_lube
from aoc_theme import AOC_GREEN_ON_BLUE, AOC_PRIMARY, AOC_THEME, WHITE, AocToggle
from batgrl.app import App
from batgrl.colors import Color, rainbow_gradient
from batgrl.gadgets.behaviors.movable import Movable
from batgrl.gadgets.progress_bar import ProgressBar
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text, add_text

INIT_SEQUENCE = aoc_lube.fetch(year=2023, day=15).split(",")
RAINBOW = rainbow_gradient(9)

# Note that the max number of lenses a box contains at any point for my input is 6, so the
# size of our boxes is just big enough to fit 6 lenses. Not guaranteed to work on your input!
LENS_BOX = """\
 Box {:>3}
+-+------+
--)------)--
+-+------+"""
BH, BW = 4, 12
LR = 2  # Light row
LO = 3  # Lens offset


def box_pos(n):
    row, column = divmod(n, 16)
    return row * BH, column * BW


def hash(string):
    total = 0
    for char in string:
        total += ord(char)
        total *= 17
    return total % 256


def color_blend(a: Color, b: Color):
    # So lenses don't color blend I don't think (but I'm no physicist).
    # I think they subtract color, but if my lenses did that then the light would just
    # turn black and won't look as cool. So my ascii lenses break the laws of physics and
    # blend.
    return Color(
        a.red // 2 + b.red // 2, a.green // 2 + b.green // 2, a.blue // 2 + b.blue // 2
    )


class MovableText(Movable, Text):
    ...


class LensApp(App):
    async def on_start(self):
        box_border = Text(default_color_pair=AOC_GREEN_ON_BLUE, is_transparent=True)
        box_border.set_text(">       <")

        boxes_label = Text(size=(16 * BH, 16 * BW), default_color_pair=AOC_PRIMARY)
        for i in range(256):
            row, column = box_pos(i)
            add_text(boxes_label.canvas[row:, column:], LENS_BOX.format(i))
            boxes_label.colors[row + 2, column + BW - 2 : column + BW, :3] = WHITE

        boxes_label.add_gadget(box_border)

        sv = ScrollView(
            size_hint={"height_hint": 1.0, "width_hint": 1.0},
            disable_ptf=True,
            show_horizontal_bar=False,
            show_vertical_bar=False,
        )
        sv.view = boxes_label

        pause_event = asyncio.Event()
        pause_event.set()

        def pause(state):
            if state == "on":
                pause_event.clear()
            else:
                pause_event.set()

        pause_button = AocToggle("PAUSE", pause, pos=(3, 8))
        auto_move_button = AocToggle("AUTO-MOVE", lambda _: None, pos=(4, 8))

        delay = 0.5

        def go_fast(state):
            nonlocal delay
            if state == "on":
                delay = 0
            else:
                delay = 0.5

        fast_button = AocToggle("TURBO", go_fast, pos=(5, 8))
        progress = ProgressBar(size=(1, 28), pos=(2, 1))
        info_label = MovableText(
            size=(7, 30),
            pos=(1, 0),
            default_color_pair=AOC_PRIMARY,
            disable_oob=True,
        )
        info_label.add_border()
        info_label.add_gadgets(progress, pause_button, auto_move_button, fast_button)

        self.add_gadgets(sv, info_label)

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

            row, col = box_border.pos = box_pos(box_id)

            if not sv.is_grabbed and auto_move_button.toggle_state == "on":
                ly, lx = boxes_label.pos
                absy, absx = row + ly, col + lx

                if absy < 0:
                    sv._scroll_up(-absy + 1)
                elif absy + BH >= sv.port_height:
                    sv._scroll_down(absy - sv.port_height + BH + 1)
                if absx < 0:
                    sv._scroll_left(-absx + 1)
                elif absx + BW >= sv.port_width:
                    sv._scroll_right(absx - sv.port_width + BW + 1)

            boxes_label.add_str(
                ")" * len(box) + "-" * (6 - len(box)), (row + LR, col + LO)
            )
            for i, focal in enumerate(box.values(), start=col + 3):
                boxes_label.colors[row + LR, i, :3] = RAINBOW[focal - 1]

            current_color = WHITE
            for i, box in enumerate(boxes):
                row, col = box_pos(i)
                row += LR
                boxes_label.colors[row, col : col + 2, :3] = current_color
                col += 3
                # Uncomment below for an extra color blend on entering a box:
                # current_color = color_blend(current_color, WHITE)
                for focal in box.values():
                    current_color = color_blend(current_color, RAINBOW[focal - 1])
                boxes_label.colors[
                    row, col + len(box.values()) : col + 6, :3
                ] = current_color
                col += 7
                boxes_label.colors[row, col : col + 2, :3] = current_color

            await asyncio.sleep(delay)


if __name__ == "__main__":
    LensApp(
        title="Lens Library", background_color_pair=AOC_PRIMARY, color_theme=AOC_THEME
    ).run()
