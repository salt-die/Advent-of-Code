from pathlib import Path

from nurses_2.app import App
from nurses_2.widgets.braille_video_player import BrailleVideoPlayer

from .tetrish import Tetrish, GREY_ON_BLUE

ASSETS = Path(__file__).parent.parent / "assets"


class TetrishApp(App):
    async def on_start(self):
        background = BrailleVideoPlayer(
            source=ASSETS / "elephants.mp4",
            size_hint=(1.0, 1.0),
            default_color_pair=GREY_ON_BLUE,
            invert_colors=True,
        )
        tetris = Tetrish(size=(22, 7), pos_hint=(.5, .1), anchor="center")

        self.add_widgets(background, tetris)

        background.play()
        tetris.new_game()


TetrishApp(title="Tetrish").run()
