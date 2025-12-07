import importlib
import sys

from batgrl.app import App
from batgrl.colors import Color

from .aoc_theme import AOC_THEME, AocButton

BG_COLOR = Color.from_hex(AOC_THEME["primary_bg"])
NOT_AVAILABLE = "Not available"
PROBLEMS = [
    "Secret Entrance",
    "Gift Shop",
    "Lobby",
    "Printing Department",
    NOT_AVAILABLE,
    "Trash Compactor",
    "Laboratories",
    NOT_AVAILABLE,
    NOT_AVAILABLE,
    NOT_AVAILABLE,
    NOT_AVAILABLE,
    NOT_AVAILABLE,
]


class AocVisuals(App):
    async def on_start(self):
        for i in range(12):
            title = PROBLEMS[i]
            button = AocButton(
                label=title, pos_hint={"x_hint": 0.5}, callback=None, pos=(i, 0)
            )
            if title == NOT_AVAILABLE:
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
    day: int | None = visuals.run()
    if day is None:
        break

    # Hot reload of visualizations:
    module_name = f"aoc_visuals.day_{day + 1:02}"
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)

    app: type[App] = getattr(module, "Visual")
    app(color_theme=AOC_THEME, bg_color=BG_COLOR, title=PROBLEMS[day]).run()
