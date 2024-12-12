import aoc_lube
from aoc_lube.utils import UnionFind, Vec2
from aoc_theme import AOC_THEME, AocText
from batgrl.app import App
from batgrl.colors import BLACK, WHITE, lerp_colors, rainbow_gradient
from batgrl.gadgets.scroll_view import ScrollView

GARDEN = aoc_lube.fetch(year=2024, day=12)


def lerp_to(rgb):
    r, g, b = rgb
    if r * 0.2126 + g * 0.7152 + b * 0.0722 > 255 / 2:
        return BLACK
    return WHITE


def regions():
    grid = {}

    for y, line in enumerate(GARDEN.splitlines()):
        for x, char in enumerate(line):
            grid[Vec2(y, x)] = char

    uf = UnionFind(grid)
    for pos, char in grid.items():
        for adj in pos.adj():
            if grid.get(adj) == char:
                uf.merge(pos, adj)
    return uf


REGIONS = regions()
GRADIENT = dict(zip(REGIONS, rainbow_gradient(len(REGIONS))))


def perimeter(region):
    return 4 * len(region) - sum(adj in region for pos in region for adj in pos.adj())


def nsides(region):
    total = 0
    for dir in Vec2(0, 0).adj():
        edge_uf = UnionFind(pos for pos in region if pos + dir not in region)
        for pos in edge_uf.elements():
            if (adj := pos + dir.rotate(True)) in edge_uf:
                edge_uf.merge(pos, adj)
            if (adj := pos + dir.rotate(False)) in edge_uf:
                edge_uf.merge(pos, adj)
        total += len(edge_uf)
    return total


class HighlightGarden(AocText):
    def _highlight_region(self, pos):
        if pos not in REGIONS:
            return

        region = REGIONS[pos]
        area = len(region)
        peri = perimeter(region)
        sides = nsides(region)

        self.header.clear()
        self.header.add_str(f"Area: {area} Perimeter: {peri} Number of Sides: {sides}")

        for pos in region:
            self.canvas["fg_color"][pos] = lerp_colors(
                self.canvas["fg_color"][pos], WHITE, 0.5
            )

    def _color_region(self, pos):
        if pos not in REGIONS:
            return

        region = REGIONS[pos]
        root = REGIONS.find(pos)

        color = GRADIENT[root]
        for pos in region:
            self.canvas["fg_color"][pos] = color

        edge_color = lerp_colors(color, lerp_to(color), 0.5)

        for pos in region:
            for dir in Vec2(0, 0).adj():
                if pos + dir not in region:
                    self.canvas["fg_color"][pos] = edge_color

    def on_mouse(self, mouse_event):
        pos = self.to_local(mouse_event.pos)
        self._color_region(pos - (mouse_event.dy, mouse_event.dx))

        if not self.collides_point(mouse_event.pos):
            return

        self._color_region(pos)
        self._highlight_region(pos)


class GardenGroupsApp(App):
    async def on_start(self):
        header = AocText(size=(1, 1), size_hint={"width_hint": 1.0})
        gardens = HighlightGarden()
        gardens.set_text(GARDEN)
        gardens.header = header
        sv = ScrollView(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "width_hint": 1.0, "height_offset": -1},
            dynamic_bars=True,
        )
        sv.view = gardens
        self.add_gadgets(header, sv)


GardenGroupsApp(title="Garden Groups", color_theme=AOC_THEME).run()
