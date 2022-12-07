import asyncio
from random import random

import aoc_lube

from nurses_2.app import App
from nurses_2.colors import ColorPair, BLACK, GREEN, WHITE_ON_BLACK
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.split_layout import HSplitLayout
from nurses_2.widgets.file_chooser import FileChooser

RAW = aoc_lube.fetch(2022, 7).splitlines()
GREEN_ON_BLACK = ColorPair.from_colors(GREEN, BLACK)
CURSOR = "█"


class Path:
    """
    This is modeled after pathlib.Path to trick FileChooser.
    """
    def __init__(self, name):
        self.name = name
        self._is_file = False
        self.children = []

    def is_file(self):
        return self._is_file

    def is_dir(self):
        return not self._is_file

    def iterdir(self):
        yield from self.children

    def add_path(self, name, is_file=False):
        for child in self.children:
            if child.name == name:
                return child

        node = Path(name)
        self.children.append(node)
        if is_file:
            node._is_file = True
        else:
            node.parent = self
        return node


class NoSpaceApp(App):
    async def on_start(self):
        terminal = TextWidget(
            size=(1, 1),
            pos_hint=(1.0, None),
            anchor="bottom_left",
            default_color_pair=GREEN_ON_BLACK
        )
        terminal.subscribe(terminal, "size", terminal.update_geometry)

        cwd = system = Path("..")
        system.children.append(Path("/"))
        file_view = FileChooser(root_dir=system, size_hint=(1.0, 1.0))

        split = HSplitLayout(size_hint=(1.0, 1.0))
        split.left_pane.add_widget(terminal)
        split.right_pane.add_widget(file_view)

        self.add_widget(split)
        split.split_col = 40

        for line in RAW:
            match line.split():
                case ["$", "cd", ".."]:
                    cwd = cwd.parent
                case ["$", "cd", dir_]:
                    cwd = cwd.add_path(dir_)
                case ["$", "ls"]:
                    pass
                case ["dir", dir_]:
                    cwd.add_path(dir_)
                case [size, file]:
                    name = f"{file} {size}"
                    cwd.add_path(name, True)

            if line.startswith("$"):
                file_view._view.update_tree_layout()

                absolute = []
                current = cwd
                while current.name != "/":
                    if len(absolute) == 3:
                        absolute.append("..")
                        break
                    absolute.append(current.name)
                    current = current.parent

                prompt = "/".join(reversed(absolute)) + ">"
                start= len(prompt)
                terminal.add_text(prompt, row=-1, bold=True)

                if len(prompt) + len(line) > terminal.width:
                    terminal.width = len(prompt) + len(line) + 1

                for i, char in enumerate(line[1:]):
                    terminal.canvas[-1, start + i] = char
                    terminal.canvas[-1, start + i + 1] = CURSOR
                    await asyncio.sleep(.2 * random())

                terminal.canvas[-1, start + i + 1] = " " # Hide cursor
                terminal.height += 1
            else:
                if len(line) > terminal.width:
                    terminal.width = len(line)
                terminal.add_text(line, row=-1)
                terminal.colors[-1, :] = WHITE_ON_BLACK
                terminal.height += 1


NoSpaceApp(title="--- Day 7: No Space Left On Device ---").run()
