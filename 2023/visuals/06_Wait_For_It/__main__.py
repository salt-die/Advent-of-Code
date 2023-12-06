import asyncio
from pathlib import Path
from time import monotonic

from aoc_theme import AOC_PRIMARY, AOC_THEME, AocButton
from batgrl.app import App
from batgrl.gadgets.image import Image
from batgrl.gadgets.parallax import Parallax
from batgrl.gadgets.text import Text
from batgrl.gadgets.textbox import Textbox

WATER = Path(__file__).parent / "water"
BOAT = Path(__file__).parent / "boat.png"


class BoatApp(App):
    async def on_start(self):
        parallax = Parallax(
            path=WATER, size_hint={"height_hint": 1.0, "width_hint": 1.0}
        )
        self.add_gadget(parallax)

        boats = [
            Image(
                path=BOAT,
                pos=(i * 3 + 11, i),
                size=(3, 24 + i),
                interpolation="nearest",
            )
            for i in range(5)
        ]
        self.add_gadgets(boats)

        input_labels = Text(
            pos_hint={"y_hint": 1.0, "x_hint": 1.0, "anchor": "bottom-right"},
            default_color_pair=AOC_PRIMARY,
        )
        input_labels.set_text(
            "\n Time allowed:      \n\n"
            "    Charge Times \n"
            "    ──────────── \n"
            "     Boat 1: \n"
            "     Boat 2: \n"
            "     Boat 3: \n"
            "     Boat 4: \n"
            "     Boat 5: \n\n\n"
        )
        input_labels.add_border("thick")

        allowed_time = 15
        boat_charge_times = [0, 0, 0, 0, 0]

        def allowed_time_input_callback(tb: Textbox):
            nonlocal allowed_time
            try:
                allowed_time = int(tb.text)
                tb.focus_next()
            except ValueError:
                tb.text = str(allowed_time)

        allowed_time_input = Textbox(
            pos=(1, 15), size=(1, 3), enter_callback=allowed_time_input_callback
        )
        allowed_time_input.text = str(allowed_time)

        def make_boat_callback(i):
            def callback(tb: Textbox):
                try:
                    boat_charge_times[i] = int(tb.text)
                    tb.focus_next()
                except ValueError:
                    tb.text = str(boat_charge_times[i])

            return callback

        boat_inputs = [
            Textbox(
                pos=(i + 5, 13),
                size=(1, 3),
                enter_callback=make_boat_callback(i),
            )
            for i in range(5)
        ]

        for charge_time, boat_input in zip(boat_charge_times, boat_inputs):
            boat_input.text = str(charge_time)

        ok_event = asyncio.Event()
        ok_button = AocButton(label="OK", pos=(11, 8), callback=ok_event.set)

        input_labels.add_gadgets(reversed(boat_inputs))
        input_labels.add_gadgets(allowed_time_input, ok_button)
        self.add_gadget(input_labels)

        finish_line = Text(
            size=(1, 1),
            size_hint={"height_hint": 1.0},
            default_char="┃",
            default_color_pair=AOC_PRIMARY,
            is_enabled=False,
        )
        finished_label = Text(is_enabled=False, default_color_pair=AOC_PRIMARY)
        self.add_gadgets(finish_line, finished_label)

        async def move_boat(boat, charge, time):
            await asyncio.sleep(charge)
            await boat.tween(
                duration=time - charge, x=boat.x + (time - charge) * charge
            )

        async def move_parallax(time):
            start = monotonic()
            while monotonic() < start + time:
                parallax.horizontal_offset += 1
                await asyncio.sleep(0)

        while True:
            ok_event.clear()
            await ok_event.wait()

            finish_line.is_enabled = False
            finished_label.is_enabled = False
            for i, boat in enumerate(boats):
                boat.x = i

            tasks = [move_parallax(allowed_time)]
            for i in range(5):
                tasks.append(move_boat(boats[i], boat_charge_times[i], allowed_time))

            await asyncio.gather(*tasks)

            distance, i = max(
                ((allowed_time - charge_time) * charge_time, i)
                for i, charge_time in enumerate(boat_charge_times)
            )

            finish_line.x = boats[i].right
            finish_line.is_enabled = True
            finished_label.set_text(
                f"\n Boat {i + 1} wins! Distance traveled: {distance} \n"
            )
            finished_label.add_border("thick")
            finished_label.pos = self.root.height // 2 - 2, finish_line.right + 2
            finished_label.is_enabled = True


if __name__ == "__main__":
    BoatApp(title="Wait For It", color_theme=AOC_THEME).run()
