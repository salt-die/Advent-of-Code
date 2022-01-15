from nurses_2.app import App
from nurses_2.colors import ColorPair, WHITE, BLACK
from nurses_2.widgets.slider import Slider
from nurses_2.widgets.text_widget import TextWidget, Anchor

from .automata import Automata, BLUISH

WHITE_ON_BLUISH = ColorPair.from_colors(WHITE, BLUISH)
BLACK_ON_BLUISH = ColorPair.from_colors(BLACK, BLUISH)


class Dumbo(App):
    async def on_start(self):
        automata = Automata(size_hint=(1.0, 1.0))

        container = TextWidget(
            size=(4, 63),
            pos_hint=(1.0, .5),
            default_color_pair=WHITE_ON_BLUISH,
            anchor=Anchor.BOTTOM_CENTER,
        )
        container.add_border()

        label = TextWidget(size=(2, 11), pos=(1, 1), default_color_pair=WHITE_ON_BLUISH)
        label.add_text("STATES:")
        label.add_text("ENERGY:", row=1)

        nstates = Slider(
            width=50,
            pos=(1, 12),
            min=5,
            max=100,
            proportion=.06,
            fill_color=WHITE,
            default_color_pair=BLACK_ON_BLUISH,
            handle_color=WHITE,
            callback=lambda n: (
                setattr(automata, "nstates", int(n)),
                label.add_text(f"{int(n):>3}", 0, 8)
            ),
        )

        energy = Slider(
            width=50,
            pos=(2, 12),
            min=-24,
            max=25,
            proportion=.52,
            fill_color=WHITE,
            default_color_pair=BLACK_ON_BLUISH,
            handle_color=WHITE,
            callback=lambda n: (
                setattr(automata, "energy", int(n)),
                label.add_text(f"{int(n):>3}", 1, 8),
            ),
        )

        container.add_widgets(label, nstates, energy)

        self.add_widgets(automata, container)


Dumbo().run()
