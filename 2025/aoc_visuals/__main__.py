from batgrl.app import App
from batgrl.colors import Color

from .aoc_theme import AOC_THEME, AocButton
from .day_01 import SecretApp

BG_COLOR = Color.from_hex(AOC_THEME["primary_bg"])
PROBLEMS = [
    ("Secret Entrance", SecretApp),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
    ("Not available", None),
]


class AocVisuals(App):
    async def on_start(self):
        for i in range(12):
            title, app = PROBLEMS[i]
            button = AocButton(
                label=title, pos_hint={"x_hint": 0.5}, callback=None, pos=(i, 0)
            )
            if app is None:
                button.button_state = "disallowed"
            else:
                button.callback = lambda i=i: self.exit(i)
            self.add_gadget(button)


visuals = AocVisuals(
    color_theme=AOC_THEME,
    bg_color=BG_COLOR,
    title="AoC Visuals 2025",
    inline=True,
    inline_height=12,
)

while True:
    day = visuals.run()
    if day is None:
        break
    title, app = PROBLEMS[day]
    app(color_theme=AOC_THEME, bg_color=BG_COLOR, title=title).run()
