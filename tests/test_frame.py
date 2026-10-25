"""No current document labels the original's deliberate values as faults or treats the sample as a company.

Enforces CLAUDE.md rules 1-3 on everything in the repository outside source/, archives and history.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import frame_check  # noqa: E402


def test_no_fault_framing_in_current_documents():
    faults = []
    for f in frame_check.repo_files():
        for level, kind, line, text in frame_check.check_text(f.read_text(errors="ignore"), str(f)):
            if level == "FAULT":
                faults.append(f"{f.relative_to(ROOT)}:{line} [{kind}] {text[:100]}")
    assert not faults, "State what it is for (docs/MODEL.md section 6) or ask Scott:\n" + "\n".join(faults)


def test_checker_catches_the_known_pattern():
    """The checker must keep catching the sentences that slipped through on 2026-10-25."""
    known = [
        "Using the calculated salary instead of the hard-coded engine value reduces baseline operating income.",
        "And modeled revenue is 4.5 times reported revenue.",
        "The workbook has three defects: the salary at 87,750 is hard-coded.",
        "The $75,000 deal size is an operator error in the original.",
    ]
    for s in known:
        assert any(f[0] == "FAULT" for f in frame_check.check_text(s, "known")), s
    allowed = [
        "The salary of 87,750 is a deliberate value placed to test the reader's method.",
        "A reader who compares parts to parts finds \"defects.\"",
        "The sample is never a company: it is not reconciled.",
    ]
    for s in allowed:
        assert not any(f[0] == "FAULT" for f in frame_check.check_text(s, "allowed")), s
