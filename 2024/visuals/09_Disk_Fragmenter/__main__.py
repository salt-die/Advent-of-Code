import asyncio

from aoc_theme import AOC_THEME, AocButton, AocText
from batgrl.app import App
from batgrl.colors import BLACK, RED, WHITE, lerp_colors
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.color_picker import ColorPicker
from batgrl.gadgets.grid_layout import GridLayout
from batgrl.gadgets.pane import Pane
from batgrl.gadgets.text import Text, new_cell
from batgrl.gadgets.textbox import Textbox


class Memory(AocText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_cell = new_cell(char=".")
        self.clear()
        self._preview = Text(
            is_transparent=True,
            alpha=0,
            is_enabled=False,
            size_hint={"height_hint": 1.0, "width_hint": 1.0},
        )
        self.add_gadgets(self._preview)

    def on_mouse(self, mouse_event):
        self._preview.is_enabled = (
            self.collides_point(mouse_event.pos)
            and not self.bg.is_enabled
            and not self.file_id.default_bg_color == self.default_fg_color
            and not self.defrag.is_set()
        )
        if not self._preview.is_enabled:
            return

        y, x = self.to_local(mouse_event.pos)
        if mouse_event.event_type == "mouse_up":
            self.place_memory(y, x)
        else:
            self.preview_memory(y, x)

    def preview_memory(self, y, x):
        self._preview.clear()
        self._preview.canvas["fg_color"] = self.file_id.default_bg_color

        size = int(self.file_size.text or "1")
        i = y * self.width + x
        chars = self._preview.canvas["char"].reshape(-1)
        ids = self._preview.canvas["fg_color"].reshape(-1, 3)
        if len(chars) - i >= size:
            chars[i : i + size] = "█"
            ids[i : i + size] = self.file_id.default_bg_color

    def place_memory(self, y, x):
        where_mem = self._preview.canvas["char"] == "█"
        self.canvas["char"][where_mem] = self._preview.canvas["char"][where_mem]
        self.canvas["fg_color"][where_mem] = self._preview.canvas["fg_color"][where_mem]


class OnlyInts(Textbox):
    def on_key(self, key_event):
        if len(key_event.key) == 1 and not key_event.key.isdigit():
            return
        return super().on_key(key_event)


class ColorPickerButton(ButtonBehavior, Pane):
    def update_normal(self):
        self.bg_color = self.default_bg_color

    def update_hover(self):
        self.bg_color = lerp_colors(self.default_bg_color, WHITE, 0.5)

    def on_release(self):
        self.modal.is_enabled = True


class DiskFragmenterApp(App):
    async def on_start(self):
        defrag = asyncio.Event()
        defrag_kind = 1
        start = 0

        bg = Pane(
            bg_color=BLACK,
            alpha=0.5,
            size_hint={"height_hint": 1.0, "width_hint": 1.0},
            is_enabled=False,
        )

        color_button = ColorPickerButton(pos=(0, 10), size=(1, 2), is_transparent=False)
        color_button.default_bg_color = RED
        color_button.update_normal()
        color_button.modal = bg

        def ok_callback(color):
            color_button.default_bg_color = color
            color_button.update_normal()
            bg.is_enabled = False

        color_picker = ColorPicker(
            ok_callback=ok_callback,
            size_hint={"height_hint": 0.5, "width_hint": 0.5},
            pos_hint={"x_hint": 0.5, "y_hint": 0.5},
        )
        color_picker.label.children[-1].label = "[ OK ]"  # HACK!
        bg.add_gadget(color_picker)

        file_size = OnlyInts(placeholder="1", size=(1, 10), pos=(0, 25))

        memory = Memory(
            size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
            pos=(1, 0),
        )
        memory.bg = bg
        memory.defrag = defrag
        memory.file_size = file_size
        memory.file_id = color_button

        def do_part_1():
            nonlocal defrag_kind
            defrag_kind = 1
            defrag.set()

        def do_part_2():
            nonlocal defrag_kind
            defrag_kind = 2
            defrag.set()

        def pause():
            nonlocal start
            start = memory.height * memory.width
            defrag.clear()

        defrag_1_button = AocButton("Defrag Any", do_part_1)
        defrag_2_button = AocButton("Defrag All", do_part_2)
        pause_button = AocButton("Pause", pause)
        clear_button = AocButton("Format", memory.clear)
        button_container = GridLayout(
            grid_columns=4, pos_hint={"x_hint": 1.0, "anchor": "right"}
        )
        button_container.add_gadgets(
            defrag_1_button, defrag_2_button, pause_button, clear_button
        )
        button_container.size = button_container.min_grid_size

        header = AocText(size=(1, 25), size_hint={"width_hint": 1.0, "min_width": 25})
        header.add_str("File ID:")
        header.add_str("File Size:", pos=(0, 14))
        header.add_gadgets(color_button, file_size, button_container)

        self.add_gadgets(header, memory, bg)

        def get_last_file_segment(pos):
            chars = memory.canvas["char"].reshape(-1)
            ids = memory.canvas["fg_color"].reshape(-1, 3)
            end = None
            file_id = None
            while pos >= 0:
                if end is None and chars[pos] != ".":
                    file_id = ids[pos]
                    end = pos + 1
                elif end is not None and (
                    chars[pos] == "." or (ids[pos] != file_id).all()
                ):
                    return pos + 1, end
                pos -= 1
            return 0, end

        def get_next_free(size):
            pos = 0
            chars = memory.canvas["char"].reshape(-1)
            start = None
            while pos < len(chars):
                if start is None and chars[pos] == ".":
                    start = pos
                elif start is not None and pos - start >= size:
                    return start, pos
                elif chars[pos] != ".":
                    start = None
                pos += 1
            return start, pos

        async def move(start, size=1):
            free_start, free_end = get_next_free(size)
            if free_end > start:
                return
            chars = memory.canvas["char"].reshape(-1)
            ids = memory.canvas["fg_color"].reshape(-1, 3)
            bg = memory.canvas["bg_color"].reshape(-1, 3)

            if size > 1:  # Animate move
                for i in range(free_start, start)[::-1]:
                    bg[:] = memory.default_bg_color
                    bg[i : i + size] = lerp_colors(
                        ids[start], memory.default_bg_color, 0.5
                    )
                    await asyncio.sleep(0.01)
                bg[:] = memory.default_bg_color

            end = start + size
            chars[free_start:free_end] = chars[start:end]
            ids[free_start:free_end] = ids[start:end]

            chars[start:end] = "."
            ids[start:end] = memory.default_fg_color

        start = memory.height * memory.width
        while True:
            await defrag.wait()
            start, end = get_last_file_segment(start - 1)
            if start == 0:
                defrag.clear()
                start = memory.height * memory.width - 1
                continue

            if defrag_kind == 1:
                await move(end - 1)
                start = end
            else:
                await move(start, end - start)

            await asyncio.sleep(0.1)


DiskFragmenterApp(title="Disk Fragmenter", color_theme=AOC_THEME).run()
