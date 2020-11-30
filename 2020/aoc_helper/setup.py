"""This sets up our AoC directory."""
import pathlib

FILE_DIR = pathlib.Path(__file__).parent.parent
TEMPLATE_FILE = "code_template.txt"

with open(TEMPLATE_FILE) as f:
    template = f.read()

for i in range(1, 26):
    file = FILE_DIR / f"day_{i:02}.py"
    if file.exists():  # We don't overwrite what could be possible solutions.
        continue
    with open(file, "w") as f:
        f.write(template.format(day=i))
