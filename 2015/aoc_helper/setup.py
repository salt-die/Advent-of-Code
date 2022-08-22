"""
Run once to set up AoC directory.
"""
from constants import *

if not INPUTS_FILE.exists():
    INPUTS_FILE.write_text("{}\n")

if not SUBMISSIONS_FILE.exists():
    SUBMISSIONS_FILE.write_text("{}\n")

template = TEMPLATE_FILE.read_text()

for i in range(1, 26):
    file = SOLUTION_DIR / f"day_{i:02}.py"

    if not file.exists():
        file.write_text(template.format(day=i))
