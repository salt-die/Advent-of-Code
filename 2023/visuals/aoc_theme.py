from batgrl.colors import AColor, Color, ColorPair, ColorTheme
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.text import Text

AOC_BLUE = Color.from_hex("0f0f23")
AOC_BRIGHT_GREEN = Color.from_hex("99ff99")
AOC_GREEN = Color.from_hex("009900")
AOC_GREY = AColor.from_hex("cccccc")
# Note: This isn't a full theme, colors will be added as needed.
AOC_THEME = ColorTheme(
    primary=ColorPair.from_colors(AOC_GREY, AOC_BLUE),
    text_pad_line_highlight=ColorPair.from_colors(AOC_GREY, Color.from_hex("161633")),
    text_pad_selection_highlight=ColorPair.from_hex("EFF8FE0078D7"),
    textbox_primary=ColorPair.from_hex("9D9DA010101A"),
    textbox_selection_highlight=ColorPair.from_hex("EFF8FE0078D7"),
    textbox_placeholder=ColorPair.from_hex("3B3B3B10101A"),
    button_normal=ColorPair.from_colors(AOC_GREEN, AOC_BLUE),
    button_hover=ColorPair.from_colors(AOC_BRIGHT_GREEN, AOC_BLUE),
    button_press=ColorPair.from_colors(AOC_BRIGHT_GREEN, AOC_BLUE),
    scroll_view_scrollbar=Color.from_hex("111121"),
    scroll_view_indicator_normal=Color.from_hex("6F6F78"),
    scroll_view_indicator_hover=Color.from_hex("5C5C65"),
    scroll_view_indicator_press=Color.from_hex("3A3A44"),
)


class AocButton(ButtonBehavior, Text):
    def __init__(self, label: str):
        super().__init__(default_color_pair=AOC_THEME.button_normal)
        self.set_text(f"[{label}]")

    def update_normal(self):
        self.colors[:] = AOC_THEME.button_normal

    def update_hover(self):
        self.colors[:] = AOC_THEME.button_hover

    def update_down(self):
        self.colors[:] = AOC_THEME.button_press
