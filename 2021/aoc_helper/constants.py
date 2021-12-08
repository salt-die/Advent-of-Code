import pathlib
from datetime import timezone, timedelta

__all__ = (
    "YEAR",
    "URL",
    "SOLUTION_DIR",
    "TEMPLATE_FILE",
    "INPUTS_FILE",
    "SUBMISSIONS_FILE",
    "TOKEN_FILE",
    "UNLOCK_TIME_INFO",
)

YEAR = 2021
URL = f"https://adventofcode.com/{YEAR}/day/{{day}}"

THIS_DIR = pathlib.Path(__file__).parent
SOLUTION_DIR = THIS_DIR.parent
TEMPLATE_FILE = THIS_DIR / "code_template.txt"
INPUTS_FILE = THIS_DIR / "inputs.yaml"
SUBMISSIONS_FILE = THIS_DIR / "submissions.yaml"

TOKEN_FILE = THIS_DIR / ".token"

# AoC puzzle inputs unlock at midnight -5 UTC
# during month of December.
UNLOCK_TIME_INFO = {
    "month": 12,
    "hour": 0,
    "minute": 0,
    "second": 0,
    "microsecond": 0,
    "tzinfo": timezone(timedelta(hours=-5), 'Eastern US'),
}
