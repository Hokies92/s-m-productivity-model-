"""Frame check: catch the reduction-before-synthesis pattern in text about the model.

The pattern (docs/SYSTEM_DIAGNOSTIC.md): compare one part of the original to another, label the
gap (defect, error, discrepancy, hard-coded, quirk, gap to reconcile), and propose a fix, before
stating what the part is for. It recurred five times in the 2026 rebuild. This tool finds it in
text so it is caught mechanically, not by Scott reading.

Usage
    python tools/frame_check.py FILE [FILE ...]          # any text: a doc, a draft, a pasted description
    python tools/frame_check.py --repo                    # every current document in the repository
Exit code 1 if any FAULT finding; WARN findings never fail.

Findings
    FAULT  fault-label  a fault word in the same sentence as something from the original
                        (a deliberate value, the workbook, the sample), with no "deliberate"/"on purpose"/
                        "not a" framing. Fix: say what the thing is for, or ask Scott.
    FAULT  sample-as-company  the illustrative sample treated as a company to reconcile or calibrate.
    WARN   results-heavy  more than one currency figure per three sentences: results leading the mechanism.
    WARN   frame-missing  (only with --review) a description of the model that omits the purpose
                        (operating income), the mechanism (cost asymmetry), or the paired values as a check.

Thresholds and word lists are literals in this file; changing them is a visible diff.

© 2000–2026 Growth Enablement. All rights reserved.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

FAULT_WORDS = re.compile(
    r"\b(defects?|errors?|bugs?|flaws?|mistakes?|wrong|inconsisten(?:t|cy|cies)|contradict(?:s|ed|ion|ions|ory)?|"
    r"discrepanc(?:y|ies)|hard[- ]?coded|dead inputs?|operator error|data problem|quirks?|hidden mechanic|"
    r"broken|incorrect|invalid)\b", re.I)
QUOTED_FAULT = re.compile(r"[\"“](?:defects?|errors?|flaws?|bugs?)[.,]?[\"”]", re.I)  # the word quoted in order to reject it
ANCHORS = re.compile(
    r"(87,?750|\$?75,?000|116,?850|33,?113|\bramp\b|\boriginal\b|\bas-is\b|\bworkbook\b|\bsample\b|"
    r"\b2000\b|engine value|\bI9\b|deal size|loaded salary|commission)", re.I)
REFRAMED = re.compile(r"\b(deliberate(?:ly)?|on purpose|test(?:s)? of method|not an? |not defects|rather than an? |"
                      r"never call|instead of calling|first reading|recorded as|was read as|misread|placed to test|when wrong\b)", re.I)
SAMPLE_AS_COMPANY = re.compile(
    r"(\b4\.5\s*(?:times|x|×)|calibrat\w* (?:the )?(?:sample|baseline)|reconcil\w*.{0,60}\bsample\b|"
    r"\bsample\b.{0,60}reconcil\w*|not a calibrated company|operating reality of the sample|"
    r"modeled revenue is \S+ (?:times|x) reported)", re.I)
CURRENCY = re.compile(r"\$\s?\d[\d,.]*\s?(?:[MBK]\b|million|billion)?", re.I)
RESULTS_PER_SENTENCE = 1 / 3

FRAME_ELEMENTS = {
    "purpose: settled at operating income": re.compile(r"operating income|operating profit", re.I),
    "mechanism: cost asymmetry between adding and improving": re.compile(r"asymmetr|salary.{0,80}(before|without)|cost.{0,40}(before|ramp)", re.I),
    "paired values as the model's own check": re.compile(r"(beside|alongside|side by side).{0,120}(agree|check|compar)|validation layer|checks itself", re.I),
}

EXEMPT = {  # records of past readings, the rule text itself, history
    "CLAUDE.md", "CHANGELOG.md", "docs/SYSTEM_DIAGNOSTIC.md", "docs/AS_IS_INDEX.md", "tools/frame_check.py",
}
EXEMPT_DIRS = {"archive", "source", ".git", "__pycache__", ".venv", "evolution"}
EXEMPT_SUFFIXES = (".score.md",)  # rubric output quotes the rubric's own criterion text


def sentences(text: str):
    """Yield (line_no, sentence). Tables and bullets count each cell/line as its own sentence."""
    for n, line in enumerate(text.splitlines(), 1):
        if "frame-check: allow" in line:
            continue
        parts = re.split(r"(?<=[.!?])\s+|\s*\|\s*", line)
        for p in parts:
            if p.strip():
                yield n, p.strip()


def check_text(text: str, name: str, review: bool = False) -> list[tuple[str, str, int, str]]:
    out = []
    n_sent = 0
    n_cur = 0
    for n, s in sentences(text):
        n_sent += 1
        n_cur += len(CURRENCY.findall(s))
        if FAULT_WORDS.search(QUOTED_FAULT.sub("", s)) and ANCHORS.search(s) and not REFRAMED.search(s):
            out.append(("FAULT", "fault-label", n, s[:160]))
        if SAMPLE_AS_COMPANY.search(s) and not re.search(r"\b(never|not|no)\b", s, re.I):
            out.append(("FAULT", "sample-as-company", n, s[:160]))
    if n_sent and n_cur / n_sent > RESULTS_PER_SENTENCE:
        out.append(("WARN", "results-heavy", 0, f"{n_cur} currency figures in {n_sent} sentences"))
    if review:
        for label, rx in FRAME_ELEMENTS.items():
            if not rx.search(text):
                out.append(("WARN", "frame-missing", 0, label))
    return out


def repo_files():
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if any(part in EXEMPT_DIRS for part in rel.parts) or str(rel) in EXEMPT or p.name.endswith(EXEMPT_SUFFIXES):
            continue
        yield p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*", type=pathlib.Path)
    ap.add_argument("--repo", action="store_true", help="check every current document in the repository")
    ap.add_argument("--review", action="store_true", help="also check that a description of the model carries the frame")
    a = ap.parse_args(argv)
    files = list(repo_files()) if a.repo else a.files
    faults = 0
    for f in files:
        findings = check_text(f.read_text(errors="ignore"), str(f), a.review)
        for level, kind, line, text in findings:
            print(f"{level:5} {kind:18} {f}:{line}  {text}")
            faults += level == "FAULT"
    print(f"\n{faults} FAULT finding(s) in {len(files)} file(s).")
    if faults:
        print("Fix: for each, state what the thing is for (docs/MODEL.md §6), or ask Scott. Do not relabel the fault.")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
