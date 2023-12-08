import asyncio
from pathlib import Path

from nurses_2.app import App
from nurses_2.colors import AColor, gradient
from nurses_2.widgets.animation import Animation
from nurses_2.widgets.graphic_widget import GraphicWidget
from nurses_2.widgets.image import Image
from nurses_2.widgets.text_widget import TextWidget

import aoc_lube

GAMES = [(a, b) for a, _, b in aoc_lube.fetch(2022, 2).splitlines()]

ASSETS = Path(__file__).parent.parent / "assets"
LEFT = ASSETS / "left.png"
LEFT_ROCK = ASSETS / "left_rock"
LEFT_PAPER = ASSETS / "left_paper"
LEFT_SCISSORS = ASSETS / "left_scissors"
RIGHT = ASSETS / "right.png"
RIGHT_ROCK = ASSETS / "right_rock"
RIGHT_PAPER = ASSETS / "right_paper"
RIGHT_SCISSORS = ASSETS / "right_scissors"


class RPSApp(App):
    async def on_start(self):
        background = GraphicWidget(size_hint=(1.0, 1.0))
        def _update_texture():
            background.texture[:] = gradient(AColor.from_hex("3ad84a"), AColor.from_hex("d82515"), background.width)

        background.subscribe(background, "size", _update_texture)

        label = TextWidget(size=(7, 26), pos_hint=(.2, .5), anchor="center")
        label.add_border()

        left_kwargs = dict(size_hint=(1.0, .5))
        right_kwargs = dict(size_hint=(1.0, .5), pos_hint=(None, 1.0), anchor="top_right")
        common_kwargs = dict(
            loop = False,
            is_visible = False,
            frame_durations = [.3, .2, .3, .2, .3, .5],
        )

        left = Image(path=LEFT, **left_kwargs)
        right = Image(path=RIGHT, **right_kwargs)

        left_rock = Animation(path=LEFT_ROCK, **left_kwargs, **common_kwargs)
        left_paper = Animation(path=LEFT_PAPER, **left_kwargs, **common_kwargs)
        left_scissors = Animation(path=LEFT_SCISSORS, **left_kwargs, **common_kwargs)

        right_rock = Animation(path=RIGHT_ROCK, **right_kwargs, **common_kwargs)
        right_paper = Animation(path=RIGHT_PAPER, **right_kwargs, **common_kwargs)
        right_scissors = Animation(path=RIGHT_SCISSORS, **right_kwargs, **common_kwargs)

        self.add_widgets(
            background,
            left,
            right,
            left_rock,
            left_paper,
            left_scissors,
            right_rock,
            right_paper,
            right_scissors,
            label,
        )

        total = 0
        outcomes = ["loss", "draw", "win"]
        throws = ["rock", "paper", "scissors"]

        async def shoot(a, b):
            nonlocal total

            a_int = ord(a) - ord("A")
            b_int = ord(b) - ord("X")
            outcome = (b_int - a_int + 1) % 3
            throw_score = b_int + 1
            outcome_score = 3 * outcome
            score = throw_score + outcome_score

            label.add_text(f"{a:^11}  {b:^11}", row=1, column=1, underline=True)
            label.add_text(f"   throw: {throws[b_int]:>8} => {throw_score}", row=2, column=1)
            label.add_text(f" outcome: {outcomes[outcome]:>8} => {outcome_score}", row=3, column=1)
            label.add_text("   score: ", row=4, column=1)
            label.add_text(f"            {score}", row=4, column=11, underline=True)
            label.add_text(f"   total: {total:>13}", row=5, column=1)

            left_anim = [left_rock, left_paper, left_scissors][a_int]
            right_anim = [right_rock, right_paper, right_scissors][b_int]

            left.is_visible = right.is_visible = False
            left_anim.is_visible = right_anim.is_visible = True

            await asyncio.gather(left_anim.play(), right_anim.play())

            left_anim.is_visible = right_anim.is_visible = False
            left.is_visible = right.is_visible = True

            total += score

        for a, b in GAMES:
            await shoot(a, b)


RPSApp(title="Paper, Rock, Scissors").run()
