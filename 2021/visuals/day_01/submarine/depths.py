import json
from pathlib import Path

THIS_DIR = Path(__file__).parent
INPUTS = THIS_DIR.parent.parent.parent / "aoc_helper" / "inputs.json"

RAW = json.loads(INPUTS.read_text())["1"]

DEPTHS = list(map(int, RAW.splitlines()))
