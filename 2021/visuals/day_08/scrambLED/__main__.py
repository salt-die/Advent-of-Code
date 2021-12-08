import asyncio
from itertools import permutations

from nurses_2.app import App
from nurses_2.widgets.graphic_widget import Interpolation
from nurses_2.widgets.animation import Animation
from nurses_2.widgets.behaviors import AutoSizeBehavior, AutoPositionBehavior, Anchor

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


class AutoGeometryAnimation(AutoSizeBehavior, AutoPositionBehavior, Animation):
    ...


class Scrambled(App):
    async def on_start(self):
        computer_animation = AutoGeometryAnimation(
            paths=COMPUTER_FRAMES,
            interpolation=Interpolation.NEAREST,
        )

        sonar_animation = AutoGeometryAnimation(
            size_hint=(.39, .28),
            pos_hint=(.48, .67),
            paths=SONAR_FRAMES,
            interpolation=Interpolation.NEAREST,
        )

        digits = DigitFolder(pos_hint=(.24, .5), anchor=Anchor.CENTER)

        self.root.add_widgets(
            computer_animation,
            sonar_animation,
            digits,
        )

        computer_animation.play()
        sonar_animation.play()

        pattern_displays = digits.children[:-4]
        output_displays = digits.children[-4:]

        for data in DATA:
            for trans in TRANSLATIONS:
                patterns, output_digits = data[: -4], data[-4:]

                # Update Display
                for pattern, pattern_display in zip(patterns, pattern_displays):
                    pattern_display.reset()
                    for segment in pattern:
                        setattr(pattern_display, trans[segment], segment)

                for output_digit, output_display in zip(output_digits, output_displays):
                    output_display.reset()
                    for segment in output_digit:
                        setattr(output_display, trans[segment], True)

                if all(
                    frozenset(trans[segment] for segment in pattern) in DIGITS
                    for pattern in patterns
                ):
                    for display in pattern_displays:
                        display.flash()
                        await asyncio.sleep(.05)

                    for display in output_displays:
                        display.flash()
                        await asyncio.sleep(.05)

                    await asyncio.sleep(1)
                    break
                else:
                    await asyncio.sleep(0)


Scrambled().run()
