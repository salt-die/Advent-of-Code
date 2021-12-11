from nurses_2.app import App
from nurses_2.widgets.behaviors import Anchor

from .automata import Automata

class Dumbo(App):
    async def on_start(self):
        self.root.add_widget(
            Automata(pos_hint=(.5, .5), anchor=Anchor.CENTER)
        )


Dumbo().run()
