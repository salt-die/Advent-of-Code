import asyncio

try:
    from aoc_theme import AOC_BLUE, AOC_GREY, AOC_PRIMARY
except ImportError:
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from aoc_theme import AOC_BLUE, AOC_GREY, AOC_PRIMARY
from aoc_lube.utils import chunk, extract_ints
from aoc_theme import AOC_BLUE, AOC_GREY, AOC_PRIMARY
from batgrl.app import App
from batgrl.colors import GREEN, YELLOW, ColorPair, rainbow_gradient
from batgrl.gadgets.text import Text
from mind_the_gaps import Endpoint, Gaps, x

GREEN_ON_BLUE = ColorPair.from_colors(GREEN, AOC_BLUE)
YELLOW_ON_BLUE = ColorPair.from_colors(YELLOW, AOC_BLUE)
RAINBOW = rainbow_gradient(31)
MIN, MAX = 0, 4_294_967_296
W = 100
RANGE_RATIO = (MAX - MIN) / W
BAR = "#"


def parse_raw():
    seeds, *groups = aoc_lube.fetch(year=2023, day=5).split("\n\n")

    srcs = Gaps()
    for a, b in chunk(extract_ints(seeds), 2):
        srcs |= Gaps([a <= x, x < a + b])

    yield srcs
    yield [group.split("\n", 1)[0] for group in groups]

    for group in groups:
        gaps = (
            (Gaps([src <= x, x < src + length]), dst - src)
            for dst, src, length in chunk(extract_ints(group), 3)
        )
        yield sorted(gaps, key=lambda tup: tup[0].endpoints[0])


def scale_gaps(gaps):
    for a, b in chunk(gaps.endpoints, 2):
        yield int(a.value / RANGE_RATIO), int(b.value / RANGE_RATIO)


def offset_gaps(gaps, offset):
    return Gaps([Endpoint(e.value + offset, e.boundary) for e in gaps.endpoints])


class SeedApp(App):
    async def on_start(self):
        GROUP_LENGTH = 20
        GROUP_SPACING = 3
        GROUP_TOTAL = GROUP_LENGTH + GROUP_SPACING
        TOTAL_LENGTH = GROUP_TOTAL * 7 + 4
        LINE_DURATION = 0.1  # Determines scroll speed

        group_labels = Text(pos=(9, 0), default_color_pair=AOC_PRIMARY)
        groups_brackets = Text(
            size=(TOTAL_LENGTH, W + 4), pos=(10, 29), default_color_pair=AOC_PRIMARY
        )
        groups_text = Text(
            size=(TOTAL_LENGTH, W), pos=(10, 31), default_color_pair=AOC_PRIMARY
        )
        self.add_gadgets(group_labels, groups_brackets, groups_text)

        # Draw brackets and beginning and end of maps
        srcs, names, *groups = parse_raw()
        for i, group in enumerate(groups):
            y1 = i * GROUP_TOTAL + GROUP_SPACING
            y2 = (i + 1) * GROUP_TOTAL

            groups_brackets.canvas["char"][y1, [0, -1]] = "┏", "┓"
            groups_brackets.canvas["char"][y1 + 1 : y2, [0, -1]] = "┃"
            groups_brackets.canvas["char"][y2, [0, -1]] = "┗", "┛"

            for j, (gap, offset) in enumerate(group):
                for x1, x2 in scale_gaps(gap):
                    groups_text.canvas["char"][y1, x1:x2] = BAR
                    groups_text.colors[y1, x1:x2, :3] = RAINBOW[j]
                for x1, x2 in scale_gaps(offset_gaps(gap, offset)):
                    groups_text.canvas["char"][y2, x1:x2] = BAR
                    groups_text.colors[y2, x1:x2, :3] = RAINBOW[j]

        def create_gap_label(a, b, offset, color, duration):
            start_x1 = int(a.value / RANGE_RATIO) + groups_text.x
            start_x2 = int((a.value + offset) / RANGE_RATIO) + groups_text.x
            end_x1 = int(b.value / RANGE_RATIO)
            gap_label = Text(
                size=(1, end_x1 - start_x1),
                pos=(10, start_x1),
                default_char=BAR,
                default_color_pair=ColorPair.from_colors(color, AOC_BLUE),
            )
            self.add_gadget(gap_label)
            last_y = {}

            def draw_trail():
                gy, gx = groups_text.pos
                ly, lx = gap_label.pos
                y = ly - gy
                x = lx - gx
                if y in last_y:
                    last_x = last_y[y]
                    groups_text.canvas[y, last_x : last_x + gap_label.width][
                        "char"
                    ] = " "
                last_y[y] = x
                groups_text.canvas[y, x : x + gap_label.width] = gap_label.canvas[0]
                groups_text.colors[y, x : x + gap_label.width] = gap_label.colors[0]

            return gap_label.tween(
                duration=duration,
                on_complete=gap_label.destroy,
                on_progress=draw_trail,
                x=start_x2,
            )

        for group, name in zip(groups, names):
            duration = LINE_DURATION * GROUP_SPACING
            new_y = groups_text.y - GROUP_SPACING
            tweens = []
            for a, b in chunk(srcs.endpoints, 2):
                tweens.append(create_gap_label(a, b, 0, AOC_GREY, duration))
            tweens.append(groups_brackets.tween(duration=duration, y=new_y))
            tweens.append(groups_text.tween(duration=duration, y=new_y))
            await asyncio.gather(*tweens)

            name = name[:-4].replace("-", " ").title()
            group_labels.set_text(f"\n  {name} \n")
            group_labels.add_border()

            duration = LINE_DURATION * GROUP_LENGTH
            new_y = groups_text.y - GROUP_LENGTH
            tweens = []
            tweens.append(groups_brackets.tween(duration=duration, y=new_y))
            tweens.append(groups_text.tween(duration=duration, y=new_y))

            dsts = Gaps()
            for i, (gap, offset) in enumerate(group):
                intersection = srcs & gap
                mapped = offset_gaps(intersection, offset)
                srcs -= gap
                dsts |= mapped

                for a, b in chunk(intersection.endpoints, 2):
                    tweens.append(create_gap_label(a, b, offset, RAINBOW[i], duration))

            for a, b in chunk(srcs.endpoints, 2):
                tweens.append(create_gap_label(a, b, 0, AOC_GREY, duration))

            srcs |= dsts
            await asyncio.gather(*tweens)

        tweens = []
        duration = LINE_DURATION * 3
        new_y = groups_text.y - 3
        for a, b in chunk(srcs.endpoints, 2):
            tweens.append(create_gap_label(a, b, 0, AOC_GREY, duration))
        tweens.append(groups_text.tween(y=new_y, duration=duration))
        tweens.append(groups_brackets.tween(y=new_y, duration=duration))

        await asyncio.gather(*tweens)

        group_labels.set_text(f"\n  Least location: {srcs.endpoints[0].value}  \n")
        group_labels.add_border()


if __name__ == "__main__":
    SeedApp(
        title="If You Give A Seed A Fertilizer", background_color_pair=AOC_PRIMARY
    ).run()
