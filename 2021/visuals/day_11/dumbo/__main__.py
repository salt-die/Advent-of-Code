from nurses_2.app import App
from nurses_2.colors import color_pair, WHITE, BLACK
from nurses_2.widgets.behaviors import Anchor
from nurses_2.widgets.slider import Slider
from nurses_2.widgets import Widget

from .automata import Automata, BLUISH

WHITE_ON_BLUISH = color_pair(WHITE, BLUISH)


class Dumbo(App):
    async def on_start(self):
        automata = Automata(pos_hint=(.5, .5), anchor=Anchor.CENTER)

        label = Widget((2, 11), default_color_pair=WHITE_ON_BLUISH)
        label.add_text("STATES:")
        label.add_text("ENERGY:", row=1)

        nstates = Slider(
            width=50,
            pos=(0, 11),
            min=5,
            max=100,
            proportion=.06,
            fill_color=BLACK,
            default_color_pair=WHITE_ON_BLUISH,
            callback=lambda n: (
                setattr(automata, "nstates", int(n)),
                label.add_text(f"{int(n):>3}", 0, 8)
            ),
        )

        energy = Slider(
            width=50,
            pos=(1, 11),
            min=-24,
            max=25,
            proportion=.52,
            fill_color=BLACK,
            default_color_pair=WHITE_ON_BLUISH,
            callback=lambda n: (
                setattr(automata, "energy", int(n)),
                label.add_text(f"{int(n):>3}", 1, 8),
            ),
        )

        self.root.add_widgets(
            automata,
            label,
            nstates,
            energy,
        )


Dumbo().run()
