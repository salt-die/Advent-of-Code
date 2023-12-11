from pathlib import Path

from aoc_theme import AOC_PRIMARY, AOC_THEME, AocButton
from batgrl.app import App
from batgrl.colors import WHITE, Color, ColorPair
from batgrl.gadgets.behaviors.movable import Movable
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text
from batgrl.gadgets.textbox import Textbox
from batgrl.gadgets.video_player import VideoPlayer
from batgrl.io import MouseEvent, MouseEventType

LIGHT_BLUE = Color.from_hex("1C1C42")
WHITE_ON_BLUE = ColorPair.from_colors(WHITE, LIGHT_BLUE)
SPACE = Path(__file__).parent / "space.gif"


class Space(Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.highlight = Gadget(
            size=(1, 1),
            background_color_pair=WHITE_ON_BLUE,
            is_enabled=False,
            is_transparent=True,
        )
        self.add_gadget(self.highlight)

    def on_mouse(self, mouse_event: MouseEvent) -> bool | None:
        if not self.collides_point(mouse_event.position):
            self.highlight.is_enabled = False
            return

        pos = self.to_local(mouse_event.position)
        self.highlight.is_enabled = True
        self.highlight.pos = pos

        if mouse_event.event_type is MouseEventType.MOUSE_UP:
            if self.canvas["char"][pos] == "#":
                self.canvas[pos] = self.default_char
            else:
                self.canvas["char"][pos] = "#"


class Options(Movable, Text):
    ...


class CosmicApp(App):
    async def on_start(self):
        space = Space(size=(3, 3), default_color_pair=AOC_PRIMARY, default_char=".")

        sv = ScrollView(is_grabbable=False, is_transparent=True)
        sv.view = space

        def update_sv_geom():
            if space.height <= self.root.height:
                sv.height = space.height
                sv.show_vertical_bar = False
                sv.y = self.root.height // 2 - space.height // 2
            else:
                sv.height = self.root.height
                sv.show_vertical_bar = True
                sv.y = 0

            if space.width <= self.root.width:
                sv.width = space.width
                sv.show_horizontal_bar = False
                sv.x = self.root.width // 2 - space.width // 2
            else:
                sv.width = self.root.width
                sv.show_horizontal_bar = True
                sv.x = 0

            sv._corner.is_visible = sv.show_horizontal_bar or sv.show_vertical_bar

        sv.subscribe(space, "size", update_sv_geom)
        sv.subscribe(self.root, "size", update_sv_geom)

        def remove_row():
            space.rows -= 1

        def add_row():
            space.rows += 1

        def remove_column():
            space.columns -= 1

        def add_column():
            space.columns += 1

        expansion = 1

        def update_expansion(box):
            nonlocal expansion
            try:
                expansion = int(box.text)
            except ValueError:
                box.text = str(expansion)

        def expand():
            i = 0
            while i < space.width:
                if (space.canvas[:, i]["char"] == ".").all():
                    space.width += expansion
                    space.canvas[:, i + expansion :] = space.canvas[:, i:-expansion]
                    space.canvas[:, i : i + expansion] = space.default_char
                    i += expansion
                i += 1

            i = 0
            while i < space.height:
                if (space.canvas[i]["char"] == ".").all():
                    space.height += expansion
                    space.canvas[i + expansion :] = space.canvas[i:-expansion]
                    space.canvas[i : i + expansion] = space.default_char
                    i += expansion
                i += 1

        def restart():
            space.size = 3, 3
            space.canvas[:] = space.default_char

        remove_row_button = AocButton("-", remove_row, pos=(1, 7))
        add_row_button = AocButton("+", add_row, pos=(1, 11))
        remove_column_button = AocButton("-", remove_column, pos=(2, 10))
        add_column_button = AocButton("+", add_column, pos=(2, 14))
        expansion_box = Textbox(
            size=(1, 3), pos=(3, 12), enter_callback=update_expansion, max_chars=2
        )
        expansion_box.text = str(expansion)
        expand_button = AocButton("Expand", expand, pos=(4, 5))
        restart_button = AocButton("Restart", restart, pos=(5, 5))

        options = Options(default_color_pair=AOC_PRIMARY, disable_oob=True)
        options.set_text("\n Rows:\n Columns:         \n Expansion:\n\n\n")
        options.add_border("thick")
        options.right = self.root.right - 3
        options.add_gadgets(
            add_row_button,
            remove_row_button,
            add_column_button,
            remove_column_button,
            expansion_box,
            expand_button,
            restart_button,
        )

        background = VideoPlayer(
            source=SPACE,
            size_hint={"height_hint": 1.0, "width_hint": 1.0},
            interpolation="nearest",
        )
        background.play()
        self.add_gadgets(background, sv, options)


if __name__ == "__main__":
    CosmicApp(
        title="Cosmic Expansion",
        background_color_pair=AOC_PRIMARY,
        color_theme=AOC_THEME,
    ).run()
