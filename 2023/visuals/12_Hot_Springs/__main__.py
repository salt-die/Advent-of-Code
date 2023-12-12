import asyncio
from itertools import product
from pathlib import Path

import aoc_lube
from aoc_theme import AOC_GREY, AOC_PRIMARY, AOC_THEME
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets.braille_video_player import BrailleVideoPlayer
from batgrl.gadgets.text import Text

GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")
SPRING = Path(__file__).parent / "spring.gif"


def parse_raw():
    data = []
    for line in aoc_lube.fetch(year=2023, day=12).splitlines():
        springs, groups = line.split()
        data.append((springs, tuple(int(i) for i in groups.split(","))))

    spring_length = max(len(springs) for springs, _ in data)
    group_length = 30
    found = f"{{0:>{spring_length}}}"
    comb = f"{found} => {{1:<{group_length}}}"

    return data, found, comb


DATA, FOUND, COMB = list(parse_raw())


class SpringApp(App):
    async def on_start(self):
        total_label = Text(size=(20, 20), default_color_pair=AOC_PRIMARY)
        total_label.canvas[:, 7]["char"] = "┃"
        total_label.add_str("━━━━━━━╋━━━━━━━━━━━━", pos=(-2, 0))
        total_label.add_str(" TOTAL ", pos=(-1, 0))
        total_label.add_str("0", pos=(-1, -2))

        combinations_label = Text(size=(20, 1), default_color_pair=AOC_PRIMARY)
        combinations_label.left = total_label.right
        combinations_label.width = len(COMB.format("", ""))

        found_label = Text(size=(20, 1), default_color_pair=AOC_PRIMARY)
        found_label.left = combinations_label.right
        found_label.width = len(FOUND.format(""))
        found_label.colors[2:, :, :3] = GREEN

        video = BrailleVideoPlayer(
            source=SPRING,
            size=(18, 15),
            pos=(2, found_label.x - 17),
            default_color_pair=AOC_PRIMARY,
            gray_threshold=25,
        )
        video.play()

        animated_text = Text(
            default_color_pair=AOC_PRIMARY, is_enabled=False, is_transparent=True
        )

        self.add_gadgets(
            total_label,
            combinations_label,
            found_label,
            video,
            animated_text,
        )

        total = 0
        for springs, groups in DATA:
            subtotal = 0
            combinations_label.canvas["char"] = " "
            combinations_label.canvas["char"][1] = "━"
            combinations_label.colors[:] = AOC_PRIMARY
            combinations_label.add_str(COMB.format(springs, str(groups)[1:-1]))
            found_label.canvas["char"] = " "
            found_label.canvas["char"][1] = "━"
            found_label.add_str("     0 ", (0, -7))

            for i, n in enumerate(product((0, 1), repeat=springs.count("?")), start=2):
                n = iter(n)
                tests = "".join(".#"[next(n)] if c == "?" else c for c in springs)
                testg = tuple(len(group) for group in tests.replace(".", " ").split())
                equals = groups == testg
                if i < combinations_label.height:
                    y = i
                else:
                    y = combinations_label.height - 1
                    combinations_label.canvas[2:-1] = combinations_label.canvas[3:]
                    combinations_label.colors[2:-1] = combinations_label.colors[3:]
                    combinations_label.colors[-1] = AOC_PRIMARY

                combinations_label.add_str(
                    COMB.format(tests, str(testg)[1:-1], n=str(equals)), (y, 0)
                )

                if equals:
                    combinations_label.colors[y, :, :3] = GREEN
                    subtotal += 1

                    if subtotal + 1 < found_label.height:
                        fy = subtotal + 1
                    else:
                        fy = found_label.height - 1
                        found_label.canvas[2:-1] = found_label.canvas[3:]
                        found_label.canvas[-1]["char"] = " "

                    animated_text.set_text(FOUND.format(tests))
                    animated_text.pos = y, combinations_label.x
                    animated_text.colors[..., :3] = GREEN
                    animated_text.is_enabled = True
                    await animated_text.tween(
                        duration=0.5, easing="out_bounce", pos=(fy, found_label.x)
                    )
                    animated_text.is_enabled = False

                    found_label.add_str(f"{subtotal:>6} ", (0, -7))
                    found_label.add_str(FOUND.format(tests), pos=(fy, 0))
                else:
                    combinations_label.colors[y, :, :3] = RED

                await asyncio.sleep(0)

            total_label.canvas[:-3, 8:] = total_label.canvas[1:-2, 8:]
            total_label.canvas[-3, 8:]["char"] = " "

            animated_text.set_text(str(subtotal).rjust(10))
            animated_text.pos = 0, found_label.right - 11
            animated_text.colors[..., :3] = AOC_GREY
            animated_text.is_enabled = True
            await animated_text.tween(
                duration=1, easing="out_bounce", pos=(total_label.bottom - 3, 9)
            )
            animated_text.is_enabled = False

            total += subtotal
            total_label.add_str(str(subtotal).rjust(10), pos=(-3, 9))
            total_label.add_str(str(total).rjust(10), pos=(-1, 9))


if __name__ == "__main__":
    SpringApp(
        title="Hot Springs", background_color_pair=AOC_PRIMARY, color_theme=AOC_THEME
    ).run()
