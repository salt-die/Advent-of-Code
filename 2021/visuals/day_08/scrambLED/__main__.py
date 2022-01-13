import asyncio
from itertools import permutations

from nurses_2.app import App
from nurses_2.widgets.graphic_widget import Interpolation, Anchor
from nurses_2.widgets.animation import Animation

from . import DATA, COMPUTER_FRAMES, SONAR_FRAMES
from .digit_display import DigitFolder

SEGMENTS = "abcdefg"
TRANSLATIONS = tuple(dict(zip(p, SEGMENTS)) for p in permutations(SEGMENTS))
DIGITS = frozenset((
    frozenset("abcefg"),
    frozenset("cf"),
    frozenset("acdeg"),
    frozenset("acdfg"),
    frozenset("bcdf"),
    frozenset("abdfg"),
    frozenset("abdefg"),
    frozenset("acf"),
    frozenset("abcdefg"),
    frozenset("abcdfg"),
))


class Scrambled(App):
    async def on_start(self):
        computer_animation = Animation(
            path=COMPUTER_FRAMES,
            interpolation=Interpolation.NEAREST,
            size_hint=(1.0, 1.0),
        )

        sonar_animation = Animation(
            size_hint=(.39, .28),
            pos_hint=(.48, .67),
            path=SONAR_FRAMES,
            interpolation=Interpolation.NEAREST,
        )

        digits = DigitFolder(pos_hint=(.24, .5), anchor=Anchor.CENTER)

        self.add_widgets(
            computer_animation,
            sonar_animation,
            digits,
        )

        computer_animation.play()
        sonar_animation.play()

        displays = digits.children

        for data in DATA:
            for trans in TRANSLATIONS:
                for datum, display in zip(data, displays):
                    display.reset()
                    for segment in datum:
                        setattr(display, trans[segment], segment)

                if all(
                    frozenset(trans[segment] for segment in pattern) in DIGITS
                    for pattern in data[:-4]
                ):
                    for display in displays:
                        display.flash()
                        await asyncio.sleep(.05)

                    await asyncio.sleep(1)
                    break
                else:
                    await asyncio.sleep(0)


Scrambled().run()
