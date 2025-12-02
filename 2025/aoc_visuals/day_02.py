from batgrl.app import App
from batgrl.colors import Color, rainbow_gradient
from batgrl.gadgets.grid_layout import GridLayout
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text
from batgrl.gadgets.textbox import Textbox
from batgrl.terminal.events import KeyEvent

from .aoc_theme import AocText

ERROR_RED = Color.from_hex("891b16")


class OnKeyTextbox(Textbox):
    def on_key(self, key_event: KeyEvent) -> bool | None:
        if key_event.key not in {
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "enter",
            "left",
            "right",
            "delete",
            "backspace",
        }:
            return

        result = super().on_key(key_event)

        if result and self.enter_callback:
            self.enter_callback(self)
            return True


class RangeGenerator(ScrollView):
    def __init__(self, minimum: int, maximum: int, **kwargs):
        super().__init__(**kwargs)

        generated = []
        seen = set()
        s = str(minimum)
        for i in range(1, len(s) // 2 + 1):
            if len(s) % i:
                continue

            initial = int(s[:i])
            while True:
                possible = int(str(initial) * (len(s) // i))
                if possible > maximum:
                    break
                if possible >= minimum and possible not in seen:
                    seen.add(possible)
                    generated.append((possible, i))
                initial += 1

        text_width = self.width
        if len(generated) > self.height:
            text_width -= 2

        if len(generated) == 0:
            return

        text = Text(is_transparent=True, size=(len(generated), text_width))
        for i, (possible, r) in enumerate(generated):
            text.add_str(f"{possible:^{text_width}}", pos=(i, 0))
            o = (text.width - len(str(possible))) // 2
            for j in range(len(s) // r):
                text.canvas["fg_color"][i, o + j * r : o + (j + 1) * r] = (
                    rainbow_gradient(r)
                )

        self.view = text


class Visual(App):
    async def on_start(self):
        range_grid = GridLayout(grid_columns=4, horizontal_spacing=1)
        slider_sv = ScrollView(
            pos=(1, 0), size=(23, 1), size_hint={"width_hint": 1.0}, dynamic_bars=True
        )
        slider_grid = GridLayout(horizontal_spacing=1, grid_rows=2, orientation="tb-lr")

        enter_range = AocText()
        enter_range.set_text("Enter Range:")

        minimum = OnKeyTextbox(size=(1, 20))
        maximum = OnKeyTextbox(size=(1, 20))

        hint = Text(size=(1, 34), is_transparent=True)
        hint.default_fg_color = ERROR_RED
        hint.clear()

        range_grid.add_gadgets(enter_range, minimum, maximum, hint)
        range_grid.size = range_grid.min_grid_size
        slider_sv.view = slider_grid
        self.add_gadgets(range_grid, slider_sv)

        def generate_sliders():
            mint = minimum.text
            mini = int(mint)
            maxt = maximum.text
            maxi = int(maxt)

            children = []

            while True:
                if len(mint) < len(maxt):
                    next_mini = int("9" * len(mint))
                else:
                    next_mini = maxi

                label = AocText()
                label.set_text(f"{mini}-{next_mini}")
                children.append(label)
                children.append(
                    RangeGenerator(
                        mini, next_mini, size=(20, label.width), dynamic_bars=True
                    )
                )
                if next_mini == maxi:
                    break

                mini = next_mini + 1
                mint = str(mini)

            slider_grid.grid_columns = len(children)
            slider_grid.add_gadgets(children)
            slider_grid.size = slider_grid.min_grid_size

        def on_key(*_):
            slider_grid.prolicide()

            if not minimum.text and not maximum.text:
                hint.set_text("No range.")
            elif not minimum.text:
                hint.set_text("No minimum.")
            elif not maximum.text:
                hint.set_text("No maximum.")
            elif int(minimum.text) > int(maximum.text):
                hint.set_text("Minimum must be less than maximum.")
            else:
                hint.clear()
                generate_sliders()
                return

        minimum.enter_callback = maximum.enter_callback = on_key
        on_key()
