import asyncio
from pathlib import Path

from nurses_2.app import App
from nurses_2.colors import AColor, ColorPair, WHITE
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.graphic_widget import GraphicWidget, Anchor
from nurses_2.widgets.image import Image
from nurses_2.widgets.parallax import Parallax

from .commands import COMMANDS
from .stable_fluid import StableFluid

ASSETS = Path("assets")
PARALLAX_IMAGES = sorted((ASSETS / "parallax_frames").iterdir())
VELOCITY_SCALE = .035
WATER_COLOR = AColor.from_hex("0805bf")
LABEL_COLOR = tuple(i//2 for i in WATER_COLOR[:3])


class SubmarineApp(App):
    async def on_start(self):
        background = Parallax(
            layers=[Image(path=path, size_hint=(1.0, 1.0)) for path in PARALLAX_IMAGES],
            size_hint=(1.0, 1.0),
        )

        fluid = StableFluid(alpha=.5, size_hint=(1.0, 1.0))

        submarine = Image(
            path=ASSETS / "submarine.png",
            size_hint=(.2, .2),
            pos_hint=(.5, .5),
            anchor=Anchor.TOP_CENTER,
        )

        water_mask = GraphicWidget(
            default_color=WATER_COLOR,
            alpha=.5,
            size_hint=(1.0, 1.0),
        )

        label = TextWidget(
            size=(1, 18),
            default_color_pair=ColorPair.from_colors(WHITE, LABEL_COLOR),
            pos_hint=(None, .5),
            anchor=Anchor.TOP_CENTER,
        )
        label.add_text("Command:")

        self.add_widgets(background, fluid, submarine, water_mask, label)

        async def background_update():
            while True:
                fluid.poke()

                match command:
                    case "forward":
                        fluid.velocity[1] -= amount * VELOCITY_SCALE
                        background.horizontal_offset += amount
                    case "up":
                        fluid.velocity[0] += amount * VELOCITY_SCALE
                        background.vertical_offset -= amount
                    case "down":
                        fluid.velocity[0] -= amount * VELOCITY_SCALE
                        background.vertical_offset += amount

                try:
                    await asyncio.sleep(0)
                except asyncio.CancelledError:
                    return

        background_task = asyncio.create_task(background_update())

        for command, amount in COMMANDS:
            label.add_text(f'{f"{command} {amount}":<10}', column=9)
            await asyncio.sleep(1)

        background_task.cancel()


SubmarineApp().run()
