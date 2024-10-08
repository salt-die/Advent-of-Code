import asyncio
from pathlib import Path

from nurses_2.app import App
from nurses_2.colors import Color, ColorPair
from nurses_2.widgets.animation import Animation
from nurses_2.widgets.image import Image
from nurses_2.widgets.parallax import Parallax
from nurses_2.widgets.text_widget import TextWidget

import aoc_lube
from aoc_lube.utils import extract_ints

TABLE_COLORPAIR = ColorPair.from_colors(Color.from_hex("8cffff"), Color.from_hex("053d1a"))
CALORIES = [list(extract_ints(elf)) for elf in aoc_lube.fetch(year=2022, day=1).split("\n\n")]
ASSETS = Path(__file__).parent.parent / "assets"
ELF = ASSETS / "elf"
JUNGLE = ASSETS / "jungle"
SKY = ASSETS / "sky.png"
CANDY_CANE = ASSETS / "candy_cane.png"


class CalorieApp(App):
    async def on_start(self):
        sky = Image(path=SKY, size_hint=(1.0, 1.0))
        jungle = Parallax(path=JUNGLE, size_hint=(1.0, 1.0))

        elf = Animation(path=ELF, size=(13, 26), interpolation="nearest")
        elf.subscribe(jungle, "size", lambda: setattr(elf, "bottom", jungle.bottom - 1))

        table = TextWidget(size=(17, 12), default_color_pair=TABLE_COLORPAIR)
        right_border = Image(path=CANDY_CANE, size=(17, 6))
        right_border.texture = right_border.texture[::-1, ::-1]
        right_border.subscribe(table, "pos", lambda: setattr(right_border, "pos", (table.y, table.right)))
        bottom_border = Image(path=CANDY_CANE)
        bottom_border._otexture = bottom_border._otexture.swapaxes(0, 1)[::-1, ::-1]  # Rotate original image and then resize.
        bottom_border.size = (3, 15)
        bottom_border.subscribe(table, "pos", lambda: setattr(bottom_border, "pos", (table.bottom, table.x)))

        self.add_widgets(sky, jungle, elf, table, right_border, bottom_border)

        async def scroll_forever():
            while True:
                jungle.horizontal_offset += 1
                await asyncio.sleep(.01)

        asyncio.create_task(scroll_forever())
        elf.play()

        max_calorie = 0
        for calories in CALORIES:
            elf.x = jungle.width

            total = sum(calories)
            if total > max_calorie:
                max_calorie = total

            table.canvas[:] = " "
            table.add_text(f"  MAX: {max_calorie}", row=-1, italic=True)
            table.add_text(f"TOTAL: {total}", row=-2, italic=True)
            for i, calorie in enumerate(calories):
                table.add_text(str(calorie).rjust(table.width), row=-3 - i, underline=i == 0)

            await asyncio.gather(
                elf.tween(duration=3.0, x=-elf.width),
                table.tween(duration=.5, bottom=i + 3),
            )


CalorieApp(title="Counting Calories").run()
