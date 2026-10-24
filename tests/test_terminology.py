"""Project terminology rule: the word "seller" is never used. Use "salesperson" / "salespeople".

Scans every text file in the repo except source/ (the frozen historical workbook export).
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "source", "__pycache__", "build", "dist"}
TEXT_SUFFIXES = {".py", ".md", ".json", ".toml", ".txt", ".csv"}
BANNED = re.compile(r"\bsellers?\b", re.IGNORECASE)
RULE_STATEMENT = re.compile(r"never\s+[\"']sellers?[\"']", re.IGNORECASE)  # the rule itself may quote the word


def test_no_seller_terminology():
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS or part.endswith(".egg-info") for part in path.relative_to(ROOT).parts):
            continue
        if path.name == "test_terminology.py":
            continue
        for n, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if BANNED.search(RULE_STATEMENT.sub("", line)):
                offenders.append(f"{path.relative_to(ROOT)}:{n}: {line.strip()[:80]}")
    assert not offenders, "Use 'salesperson', never 'seller':\n" + "\n".join(offenders)
