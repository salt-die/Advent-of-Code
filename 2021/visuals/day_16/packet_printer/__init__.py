from pathlib import Path

import yaml

def _parse_raw():
    this_dir = Path(__file__).parent
    inputs = this_dir.parent.parent.parent / "aoc_helper" / "inputs.yaml"
    raw = yaml.full_load(inputs.read_text())["16"]

    bits = bin(int(raw, 16))[2:]

    return bits

BITS = _parse_raw()
