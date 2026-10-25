"""Project terminology rule (docs/MODEL.md, invariant 9).

Salespeople are agents measured as a system, so the project says "salesperson" / "salespeople".
Banned, as a class: the word "seller(s)" and the abbreviation "rep(s)".

Scans every text file in the repo except source/ (the frozen original), tools/archive/ and docs/archive/.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "source", "__pycache__", "build", "dist", "archive", ".venv"}
TEXT_SUFFIXES = {".py", ".md", ".json", ".toml", ".txt", ".csv", ".sql"}
BANNED = re.compile(r"\b(sellers?|reps?)\b", re.IGNORECASE)
# The rule may be stated by quoting the banned word.
RULE_STATEMENT = re.compile(r"(never\s+[\"']sellers?[\"']|word\s+\"sellers?\(s\)\"|\"seller\(s\)\"|\"rep\(s\)\")", re.IGNORECASE)


def test_terminology_class():
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS or part.endswith(".egg-info") for part in path.relative_to(ROOT).parts):
            continue
        if path.name in ("test_terminology.py", "workbook_cells.csv") or path.name.endswith(".manifest.json"):
            continue  # copies of the original's own text are exempt
        for n, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if BANNED.search(RULE_STATEMENT.sub("", line)):
                offenders.append(f"{path.relative_to(ROOT)}:{n}: {line.strip()[:80]}")
    assert not offenders, "Use 'salesperson' / 'salespeople':\n" + "\n".join(offenders)
