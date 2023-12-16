from pathlib import Path

from sitecustomize import site

site.addsitedir(Path(__file__).parent.parent / "aoc_theme.py")
