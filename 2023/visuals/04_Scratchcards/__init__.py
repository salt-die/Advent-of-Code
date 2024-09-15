import site
from pathlib import Path

site.addsitedir(Path(__file__).parent.parent / "aoc_theme.py")
