import asyncio
from itertools import cycle
from math import dist

import aoc_lube
from aoc_lube.utils import int_grid

from nurses_2.app import App
from nurses_2.colors import gradient, AColor, ABLACK, WHITE, RED
from nurses_2.io import MouseEventType
from nurses_2.widgets.shadow_caster.shadow_caster import ShadowCaster
from nurses_2.widgets.shadow_caster.shadow_caster_data_structures import (
    Camera,
    Interval,
    LightIntensity,
    LightSource,
)

MAP = int_grid(aoc_lube.fetch(year=2022, day=8))
TILE_COLORS = gradient(ABLACK, AColor.from_hex("35ce27"), 10)
COLOR_CYCLE = cycle(map(
    LightIntensity.from_color,
    gradient(WHITE, RED, 10) + gradient(RED, WHITE, 10),
))


class CustomCaster(ShadowCaster):
    def on_mouse(self, mouse_event):
        if (
            mouse_event.event_type is MouseEventType.MOUSE_MOVE
            and self.collides_point(mouse_event.position)
        ):
            self.light_sources[0].coords = self.to_map_coords(self.to_local(mouse_event.position))

        return super().on_mouse(mouse_event)

    def _visible_points_quad(self, quad, origin, intensity, intensities, map):
        y, x, vert = quad
        oy, ox = origin
        h, w, _ = intensities.shape

        light_decay = self.light_decay
        smooth_radius = self.radius + self.smoothing

        obstructions = [ ]
        for i in range(self.radius):
            if len(obstructions) == 1 and obstructions[0] == (0.0, 1.0):
                return

            theta = 1.0 / float(i + 1)

            for j in range(i + 1):
                if vert:
                    p = py, px = oy + i * y, ox + j * x
                else:
                    p = py, px = oy + j * y, ox + i * x

                if not (0 <= py < h and 0 <= px < w):
                    continue

                if (d := dist(origin, p)) <= smooth_radius:
                    interval = Interval(j * theta, (j + 1) * theta)

                    if self._point_is_visible(interval, obstructions):
                        intensities[p] = intensity
                        intensities[p] *= light_decay(d)

                        if map[p] > map[origin]:  # Normal caster only checks for non-zero values here.
                            self._add_obstruction(obstructions, interval)

                    elif self.not_visible_blocks:
                        self._add_obstruction(obstructions, interval)


class TreetopApp(App):
    async def on_start(self):
        caster = CustomCaster(
            size_hint=(1.0, 1.0),
            map=MAP,
            camera=Camera((0, 0), (99, 99)),
            tile_colors=TILE_COLORS,
            light_sources=[LightSource()],
            ambient_light=.1,
            radius=50,
            restrictiveness="permissive",
        )
        self.add_widget(caster)

        while True:
            caster.cast_shadows()
            caster.light_sources[0].intensity = next(COLOR_CYCLE)
            await asyncio.sleep(.05)


TreetopApp(title="--- Day 8: Treetop Tree House ---").run()