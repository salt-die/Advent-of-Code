import pathlib

YEAR = 2021
URL = f"https://adventofcode.com/{YEAR}/day/{{day}}"

THIS_DIR = pathlib.Path(__file__).parent
SOLUTION_DIR = THIS_DIR.parent
TEMPLATE_FILE = THIS_DIR / "code_template.txt"
INPUTS_FILE = THIS_DIR / "inputs.yaml"
SUBMISSIONS_FILE = THIS_DIR / "submissions.yaml"

TOKEN_FILE = THIS_DIR / ".token"
