import json
from pathlib import Path

import cv2
import numpy as np

from nurses_2.colors import AColor

_THIS_DIR = Path(__file__).parent
_INPUTS = _THIS_DIR.parent.parent.parent / "aoc_helper" / "inputs.json"
_RAW = json.loads(_INPUTS.read_text())["1"]

DEPTHS = list(map(int, _RAW.splitlines()))
FLOOR_COLOR = AColor.from_hex("050423ff")
SCALE = 10  # Stretch texture horizontally by this scale.

def create_floor_texture():
    """
    Create a texture array from puzzle input using cv2's `fillPoly`.
    """
    min_depth = min(DEPTHS)
    height = max(DEPTHS) - min_depth
    width = len(DEPTHS) * SCALE

    texture = np.zeros((height, width, 4), dtype=np.uint8)
    points = np.array([[SCALE * i, depth - min_depth] for i, depth in enumerate(DEPTHS)] + [[0, height]])
    cv2.fillPoly(texture, [points], FLOOR_COLOR)

    return texture
