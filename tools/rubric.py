"""Rubric for the recreated as-is workbook, as code.

Every criterion is scored by a measurement, not by reading. Where a criterion cannot be measured
by a program (marked HUMAN), the tool never scores it: it reads the score from a reviewer file
or reports it as unscored. The builder cannot raise a HUMAN score.

Usage
    python tools/rubric.py WORKBOOK.xlsx MANIFEST.json [--reviewer SCORES.json] [--out score_sheet.md]

Inputs
    WORKBOOK.xlsx   the blank, general workbook produced by the builder (no company data).
    MANIFEST.json   produced by the same builder run. It declares facts the rubric checks, so
                    that scoring never depends on guessing layout. Schema (all keys required):
      {
        "sheet_order":  ["Orientation", "1) Data Entry", ...],           # presentation order
        "entry_sheet":  "1) Data Entry",                                 # the one sheet with gridlines
        "inputs": [                                                      # every cell a client may type in
          {"sheet": "...", "cell": "E12", "id": "revenue",
           "label": "...", "unit": "...", "definition": "...", "where": "...", "original_text": "..."}
        ],
        "cell_map": [                                                    # original cell -> new cell
          {"orig_sheet": "1) Data entry", "orig_cell": "F9", "sheet": "...", "cell": "...",
           "role": "input" | "formula"}
        ],
        "scenario_size_cells": [{"sheet": "...", "cell": "..."}],         # the editable improvement sizes
        "chain_rows": [{"sheet": "...", "row": 21, "rule_cell": "B21",   # one calculation per row
                        "columns": ["C","E","F","G","H","J","K"]}],
        "detail_rows": [{"sheet": "...", "rows": [20, 26]}],              # rows that must be grouped
        "diagnostic_sheet": "...",
        "no_gridline_sheets": ["Orientation", ...]
      }
    SCORES.json (optional)  {"A1": {"score": 2, "note": "..."}, ...} for HUMAN criteria only.
                            Scores given here for AUTO criteria are ignored.

Output
    A score sheet (markdown) and the same as JSON next to it. Gate first; if the gate fails,
    dimensions A–F are reported but marked "not counted".

Scoring
    Every AUTO criterion maps a measured quantity to 0 / 1 / 2 with thresholds written in its
    check function. Changing a threshold is a change to this file, visible in the diff.

© 2000–2026 Growth Enablement. All rights reserved.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Callable, Optional

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[1]
ORIGINAL_CSV = ROOT / "source" / "workbook_cells.csv"
RECALC = pathlib.Path("/mnt/skills/public/xlsx/scripts/recalc.py")

AUTO, HUMAN = "AUTO", "HUMAN"
TOL = 0.005  # currency and ratio tolerance, absolute, after recalculation


# ---------------------------------------------------------------- infrastructure
@dataclass
class Result:
    cid: str
    dimension: str
    statement: str
    method: str
    score: Optional[int]            # 0, 1, 2, or None (unscored HUMAN / not run)
    measured: str                   # the quantity measured, as text
    evidence: list = field(default_factory=list)


class Ctx:
    """Everything the checks need, computed once."""

    def __init__(self, wb_path: pathlib.Path, manifest: dict, workdir: pathlib.Path):
        self.path = wb_path
        self.m = manifest
        self.workdir = workdir
        self.wb = openpyxl.load_workbook(wb_path)                 # formulas
        self.orig = self._load_original()
        self.blank_values = self._recalc_values(wb_path)           # blank workbook, recalculated
        self.parity_values = None                                  # filled lazily by the gate

    @staticmethod
    def _load_original() -> dict:
        cells = {}
        with open(ORIGINAL_CSV, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                key = (r["sheet"].strip(), r["cell"])
                raw = r["formula_or_input"]
                val = r["value"]
                num = None
                try:
                    num = float(val)
                except (TypeError, ValueError):
                    pass
                cells[key] = dict(formula=raw if raw.startswith("=") else None, text=None if num is not None else raw,
                                  value=num, is_formula=r["is_formula"].strip().lower() == "true")
        return cells

    def _recalc_values(self, path: pathlib.Path):
        if shutil.which("soffice") is None or not RECALC.exists():
            return None
        tmp = self.workdir / (path.stem + "_recalc.xlsx")
        shutil.copy(path, tmp)
        out = subprocess.run([sys.executable, str(RECALC), str(tmp), "120"], capture_output=True, text=True, timeout=600)
        try:
            info = json.loads(out.stdout[out.stdout.index("{"):])
        except ValueError:
            info = {"total_errors": -1, "raw": out.stdout[-400:]}
        wbv = openpyxl.load_workbook(tmp, data_only=True)
        return dict(info=info, wb=wbv)

    def formula_cells(self, sheet=None):
        for ws in self.wb.worksheets:
            if sheet and ws.title != sheet:
                continue
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.startswith("="):
                        yield ws, c

    def input_cells(self):
        for i in self.m["inputs"]:
            yield i, self.wb[i["sheet"]][i["cell"]]


def band(x: float, two: float, one: float) -> int:
    """Map a measured share (0..1) to a score: >= two -> 2, >= one -> 1, else 0."""
    return 2 if x >= two else 1 if x >= one else 0


CHECKS: list[tuple[str, str, str, str, Callable[[Ctx], tuple[Optional[int], str, list]]]] = []


def criterion(cid, dimension, statement, method=AUTO):
    def deco(fn):
        CHECKS.append((cid, dimension, statement, method, fn))
        return fn
    return deco


def human(cid, dimension, statement):
    CHECKS.append((cid, dimension, statement, HUMAN, lambda ctx: (None, "requires a reviewer score", [])))


# ---------------------------------------------------------------- Gate: fidelity
def _parity(ctx: Ctx):
    """Type the original's inputs into the mapped input cells, recalculate, compare mapped formula cells."""
    if ctx.parity_values is not None:
        return ctx.parity_values
    wb = openpyxl.load_workbook(ctx.path)
    typed = 0
    for m in ctx.m["cell_map"]:
        if m["role"] != "input":
            continue
        o = ctx.orig.get((m["orig_sheet"], m["orig_cell"]))
        if o is None or o["value"] is None:
            continue
        wb[m["sheet"]][m["cell"]].value = o["value"]
        typed += 1
    tmp = ctx.workdir / "parity_input.xlsx"
    wb.save(tmp)
    rec = ctx._recalc_values(tmp)
    ctx.parity_values = dict(rec=rec, typed=typed)
    return ctx.parity_values


def _compare(ctx: Ctx, sheets: Optional[set] = None):
    p = _parity(ctx)
    if p["rec"] is None:
        return None, "LibreOffice not available", []
    wbv = p["rec"]["wb"]
    ok, bad, n = 0, [], 0
    for m in ctx.m["cell_map"]:
        if m["role"] != "formula":
            continue
        if sheets and m["orig_sheet"] not in sheets:
            continue
        o = ctx.orig.get((m["orig_sheet"], m["orig_cell"]))
        if o is None or o["value"] is None:
            continue
        n += 1
        got = wbv[m["sheet"]][m["cell"]].value
        if isinstance(got, (int, float)) and abs(got - o["value"]) <= max(TOL, abs(o["value"]) * 1e-9):
            ok += 1
        else:
            bad.append(f"{m['orig_sheet']}!{m['orig_cell']} = {o['value']}  ->  {m['sheet']}!{m['cell']} = {got}")
    return ok, n, bad


@criterion("G1", "Gate", "Original inputs typed in -> every numeric formula on Performance breakdown and Impact Analysis matches the original")
def g1(ctx):
    r = _compare(ctx, {"2) Performance breakdown", "3) Impact Analysis"})
    if r[0] is None:
        return None, r[1], []
    ok, n, bad = r
    return (2 if ok == n and n > 0 else 0), f"{ok} of {n} matched", bad[:40]


@criterion("G2", "Gate", "Every original numeric formula cell (all sheets) is mapped and matches")
def g2(ctx):
    orig_formula_numeric = sum(1 for k, o in ctx.orig.items() if o["is_formula"] and o["value"] is not None)
    r = _compare(ctx)
    if r[0] is None:
        return None, r[1], []
    ok, n, bad = r
    unmapped = orig_formula_numeric - n
    score = 2 if ok == orig_formula_numeric else 0
    return score, f"{ok} matched of {orig_formula_numeric} original numeric formula cells ({unmapped} unmapped)", bad[:40]


_NUM = re.compile(r"(?<![A-Za-z_$])\d+(?:\.\d+)?(?![A-Za-z_\d])")
_ALLOWED_LITERALS = {"0", "1", "12", "100", "1E-9", "0.5"}


def _literals(formula: str) -> list:
    f = re.sub(r'"[^"]*"', "", formula)                 # strings
    f = re.sub(r"'[^']*'!", "", f)                     # sheet names
    f = re.sub(r"\$?[A-Z]{1,3}\$?\d+", "", f)          # cell refs
    f = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", "", f)   # names and functions
    return [x for x in _NUM.findall(f) if x not in _ALLOWED_LITERALS]


@criterion("G3", "Gate", "No typed constant in any formula on engine or analysis sheets (literals other than 0, 1, 12, 100)")
def g3(ctx):
    entry = ctx.m["entry_sheet"]
    bad = []
    for ws, c in ctx.formula_cells():
        if ws.title == entry or ws.title == ctx.m["sheet_order"][0]:
            continue
        lits = _literals(c.value)
        if lits:
            bad.append(f"{ws.title}!{c.coordinate}: {lits} in {c.value[:60]}")
    return (2 if not bad else 0), f"{len(bad)} formulas with typed constants", bad[:40]


@criterion("G4", "Gate", "Both original ramp treatments reproduced (Performance breakdown E25 and K25 match)")
def g4(ctx):
    p = _parity(ctx)
    if p["rec"] is None:
        return None, "LibreOffice not available", []
    hits, bad = 0, []
    for cell in ("E25", "K25"):
        m = next((x for x in ctx.m["cell_map"] if x["orig_sheet"] == "2) Performance breakdown" and x["orig_cell"] == cell), None)
        if not m:
            bad.append(f"{cell} not mapped")
            continue
        got = p["rec"]["wb"][m["sheet"]][m["cell"]].value
        want = ctx.orig[("2) Performance breakdown", cell)]["value"]
        if isinstance(got, (int, float)) and abs(got - want) <= TOL:
            hits += 1
        else:
            bad.append(f"{cell}: want {want}, got {got}")
    return (2 if hits == 2 else 0), f"{hits} of 2", bad


# ---------------------------------------------------------------- A. Logical layout
human("A1", "A. Layout", "Sheet order follows the work: orient -> enter -> scenarios -> income statement -> obstacles")


@criterion("A2", "A. Layout", "Each sheet reads only sheets before it in presentation order")
def a2(ctx):
    order = {s: i for i, s in enumerate(ctx.m["sheet_order"])}
    bad = []
    for ws, c in ctx.formula_cells():
        for ref in re.findall(r"'([^']+)'!", c.value):
            if order.get(ref, -1) > order.get(ws.title, -1):
                bad.append(f"{ws.title}!{c.coordinate} reads {ref}")
    return (2 if not bad else 0), f"{len(bad)} backward references", bad[:20]


human("A3", "A. Layout", "One titled section per sheet; nothing needed is below the fold without a visible pointer (1366x768)")
human("A4", "A. Layout", "Ten sampled output cells each trace to an input in two clicks")


# ---------------------------------------------------------------- B. Data collection
@criterion("B1", "B. Collection", "Every input unlocked and filled; every formula locked; sheet protection on without password")
def b1(ctx):
    bad = []
    for i, c in ctx.input_cells():
        if c.protection.locked:
            bad.append(f"input locked: {i['sheet']}!{i['cell']}")
        if c.fill is None or c.fill.fgColor is None or c.fill.fgColor.rgb in (None, "00000000"):
            bad.append(f"input not filled: {i['sheet']}!{i['cell']}")
    for ws, c in ctx.formula_cells():
        if not c.protection.locked:
            bad.append(f"formula unlocked: {ws.title}!{c.coordinate}")
    for ws in ctx.wb.worksheets:
        if not ws.protection.sheet:
            bad.append(f"protection off: {ws.title}")
        if ws.protection.password:
            bad.append(f"password set: {ws.title}")
    return (2 if not bad else 1 if len(bad) <= 3 else 0), f"{len(bad)} violations", bad[:30]


@criterion("B2", "B. Collection", "Every input has label, unit, definition, where-to-find and the original's explanation")
def b2(ctx):
    fields = ("label", "unit", "definition", "where", "original_text")
    n, ok, bad = 0, 0, []
    for i in ctx.m["inputs"]:
        n += 1
        missing = [f for f in fields if not str(i.get(f, "")).strip()]
        if missing:
            bad.append(f"{i['id']}: missing {missing}")
        else:
            ok += 1
    share = ok / n if n else 0
    return band(share, 1.0, 0.9), f"{ok} of {n} inputs complete", bad[:30]


@criterion("B3", "B. Collection", "Every input cell has data validation")
def b3(ctx):
    n, ok, bad = 0, 0, []
    for i, c in ctx.input_cells():
        n += 1
        ws = ctx.wb[i["sheet"]]
        covered = any(c.coordinate in dv.sqref for dv in ws.data_validations.dataValidation)
        if covered:
            ok += 1
        else:
            bad.append(f"{i['sheet']}!{i['cell']}")
    return band(ok / n if n else 0, 1.0, 0.9), f"{ok} of {n} validated", bad[:30]


@criterion("B4", "B. Collection", "Blank workbook recalculates with zero error values")
def b4(ctx):
    if ctx.blank_values is None:
        return None, "LibreOffice not available", []
    errs = ctx.blank_values["info"].get("total_errors", -1)
    return (2 if errs == 0 else 0), f"{errs} error cells", [json.dumps(ctx.blank_values["info"].get("error_summary", {}))[:200]]


human("B5", "B. Collection", "Inputs that can be entered or calculated show both, say which is in use, never silently prefer one")


@criterion("B6", "B. Collection", "Detail rows are grouped under their totals (outline level set)")
def b6(ctx):
    n, ok, bad = 0, 0, []
    for d in ctx.m["detail_rows"]:
        ws = ctx.wb[d["sheet"]]
        for r in d["rows"]:
            n += 1
            if ws.row_dimensions[r].outlineLevel and ws.row_dimensions[r].outlineLevel > 0:
                ok += 1
            else:
                bad.append(f"{d['sheet']} row {r}")
    return band(ok / n if n else 0, 1.0, 0.8), f"{ok} of {n} detail rows grouped", bad[:20]


human("B7", "B. Collection", "A Finance person can fill the entry sheet alone, forwarded without the rest of the workbook")


# ---------------------------------------------------------------- C. Scenario calculations
@criterion("C1", "C. Scenarios", "Scenario sizes are unlocked, labeled, validated input cells")
def c1(ctx):
    n, ok, bad = 0, 0, []
    for s in ctx.m["scenario_size_cells"]:
        n += 1
        ws = ctx.wb[s["sheet"]]
        c = ws[s["cell"]]
        label = ws.cell(c.row, 2).value or ws.cell(c.row - 1, c.column).value
        validated = any(c.coordinate in dv.sqref for dv in ws.data_validations.dataValidation)
        if not c.protection.locked and label and validated:
            ok += 1
        else:
            bad.append(f"{s['sheet']}!{s['cell']}: locked={c.protection.locked} label={bool(label)} validated={validated}")
    return band(ok / n if n else 0, 1.0, 0.75), f"{ok} of {n}", bad


def _skeleton(formula: str) -> str:
    """Formula with column letters removed, so the same chain in different columns compares equal."""
    f = re.sub(r"'[^']*'!", "S!", formula)
    f = re.sub(r"\$?[A-Z]{1,3}(\$?\d+)", r"#\1", f)
    return f


@criterion("C2", "C. Scenarios", "Within each chain row, scenario columns share one formula skeleton (combined columns may reference single-lever columns)")
def c2(ctx):
    n, ok, bad = 0, 0, []
    for cr in ctx.m["chain_rows"]:
        ws = ctx.wb[cr["sheet"]]
        skels = {}
        for col in cr["columns"]:
            v = ws[f"{col}{cr['row']}"].value
            if isinstance(v, str) and v.startswith("="):
                skels[col] = _skeleton(v)
        if not skels:
            continue
        n += 1
        distinct = set(skels.values())
        if len(distinct) <= 2:          # one chain skeleton, plus at most one "= other column" pass-through form
            ok += 1
        else:
            bad.append(f"{cr['sheet']} row {cr['row']}: {len(distinct)} skeletons")
    return band(ok / n if n else 0, 1.0, 0.8), f"{ok} of {n} rows consistent", bad[:20]


@criterion("C3", "C. Scenarios", "Every chain row carries its rule in words")
def c3(ctx):
    n, ok, bad = 0, 0, []
    for cr in ctx.m["chain_rows"]:
        n += 1
        v = ctx.wb[cr["sheet"]][cr["rule_cell"]].value
        if v and str(v).strip():
            ok += 1
        else:
            bad.append(f"{cr['sheet']}!{cr['rule_cell']}")
    return band(ok / n if n else 0, 1.0, 0.9), f"{ok} of {n}", bad[:20]


@criterion("C4", "C. Scenarios", "Perturbing each input (after original inputs are typed) changes at least one output and introduces no error")
def c4(ctx):
    p = _parity(ctx)
    if p["rec"] is None:
        return None, "LibreOffice not available", []
    base_wb = openpyxl.load_workbook(ctx.workdir / "parity_input.xlsx")
    base_vals = p["rec"]["wb"]
    outputs = [m for m in ctx.m["cell_map"] if m["role"] == "formula" and m["orig_sheet"] == "3) Impact Analysis"]
    n, ok, bad = 0, 0, []
    for i in ctx.m["inputs"]:
        c = base_wb[i["sheet"]][i["cell"]]
        if not isinstance(c.value, (int, float)):
            continue                     # inputs the original left blank are not perturbed
        n += 1
        wb2 = openpyxl.load_workbook(ctx.workdir / "parity_input.xlsx")
        wb2[i["sheet"]][i["cell"]].value = c.value * 1.07 + (1 if c.value == 0 else 0)
        tmp = ctx.workdir / f"perturb_{i['id']}.xlsx"
        wb2.save(tmp)
        rec = ctx._recalc_values(tmp)
        if rec["info"].get("total_errors", 1) != 0:
            bad.append(f"{i['id']}: errors after perturbation")
            continue
        changed = any(rec["wb"][m["sheet"]][m["cell"]].value != base_vals[m["sheet"]][m["cell"]].value for m in outputs)
        if changed:
            ok += 1
        else:
            bad.append(f"{i['id']}: no output changed")
    return band(ok / n if n else 0, 1.0, 0.9), f"{ok} of {n} inputs move an output cleanly", bad[:30]


# ---------------------------------------------------------------- D. Analysis calculations
@criterion("D1", "D. Analysis", "Impact Analysis lines, including % net gain and S&M ROI, match the original")
def d1(ctx):
    r = _compare(ctx, {"3) Impact Analysis"})
    if r[0] is None:
        return None, r[1], []
    ok, n, bad = r
    return (2 if ok == n and n > 0 else 0), f"{ok} of {n}", bad[:20]


@criterion("D2", "D. Analysis", "Cost ratios (cost of revenue, R&D, G&A) are inputs on the entry sheet")
def d2(ctx):
    entry = ctx.m["entry_sheet"]
    hits, bad = 0, []
    for cell in ("C30", "C31", "C32"):
        m = next((x for x in ctx.m["cell_map"] if x["orig_sheet"] == "3) Impact Analysis" and x["orig_cell"] == cell), None)
        if m and m["role"] == "input" and m["sheet"] == entry:
            hits += 1
        else:
            bad.append(f"Impact Analysis {cell} not an entry-sheet input")
    return (2 if hits == 3 else 0), f"{hits} of 3", bad


human("D3", "D. Analysis", "Each scenario column shows change vs baseline for revenue, costs and operating income")


# ---------------------------------------------------------------- E. Scenario Diagnostic
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


@criterion("E1", "E. Diagnostic", "All original Scenario Diagnostic text present word for word")
def e1(ctx):
    ws = ctx.wb[ctx.m["diagnostic_sheet"]]
    present = {_norm(c.value) for row in ws.iter_rows() for c in row if isinstance(c.value, str)}
    want = [o["text"] for k, o in ctx.orig.items() if k[0] == "4) Scenario Diagnostic" and o["text"]
            and "Forrester" not in o["text"]]
    missing = [t[:60] for t in want if _norm(t) not in present]
    share = 1 - len(missing) / len(want) if want else 0
    return band(share, 1.0, 0.95), f"{len(want) - len(missing)} of {len(want)} texts present", missing[:20]


@criterion("E2", "E. Diagnostic", "Diagnostic text cells wrap and their rows are taller than default")
def e2(ctx):
    ws = ctx.wb[ctx.m["diagnostic_sheet"]]
    n, ok, bad = 0, 0, []
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and len(c.value) > 120:
                n += 1
                h = ws.row_dimensions[c.row].height
                if c.alignment.wrap_text and h and h > 20:
                    ok += 1
                else:
                    bad.append(c.coordinate)
    return band(ok / n if n else 0, 1.0, 0.9), f"{ok} of {n} long texts wrapped", bad[:20]


# ---------------------------------------------------------------- F. Look and feel
@criterion("F1", "F. Presentation", "One typeface; at most four font sizes across the workbook")
def f1(ctx):
    names, sizes = set(), set()
    for ws in ctx.wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                names.add(c.font.name)
                sizes.add(c.font.sz)
    score = 2 if len(names) == 1 and len(sizes) <= 4 else 1 if len(names) <= 2 and len(sizes) <= 6 else 0
    return score, f"{len(names)} typefaces {sorted(names)}, {len(sizes)} sizes {sorted(s for s in sizes if s)}", []


@criterion("F2", "F. Presentation", "Freeze panes on every sheet with a table; numeric formula cells carry a number format")
def f2(ctx):
    bad = []
    for ws in ctx.wb.worksheets:
        if ws.title != ctx.m["sheet_order"][0] and not ws.freeze_panes:
            bad.append(f"no freeze panes: {ws.title}")
    general = 0
    total = 0
    for ws, c in ctx.formula_cells():
        total += 1
        if c.number_format in (None, "General"):
            general += 1
    share = 1 - general / total if total else 1
    score = min(2 if not bad else 1, band(share, 0.98, 0.9))
    return score, f"{len(bad)} sheets without freeze panes; {general} of {total} formulas in General format", bad


@criterion("F3", "F. Presentation", "Every sheet set to fit one page wide")
def f3(ctx):
    bad = [ws.title for ws in ctx.wb.worksheets
           if not (ws.sheet_properties.pageSetUpPr and ws.sheet_properties.pageSetUpPr.fitToPage and ws.page_setup.fitToWidth == 1)]
    return (2 if not bad else 0), f"{len(bad)} sheets not fit to width", bad


@criterion("F4", "F. Presentation", "Gridlines off on presentation sheets, on for the entry sheet")
def f4(ctx):
    bad = []
    for ws in ctx.wb.worksheets:
        want = ws.title == ctx.m["entry_sheet"]
        if bool(ws.sheet_view.showGridLines) != want:
            bad.append(ws.title)
    return (2 if not bad else 0), f"{len(bad)} sheets wrong", bad


@criterion("F5", "F. Presentation", "No external links, no macros, blank file recalculates without error")
def f5(ctx):
    bad = []
    if ctx.wb._external_links:
        bad.append("external links present")
    if ctx.path.suffix.lower() != ".xlsx":
        bad.append("not .xlsx (macros possible)")
    if ctx.blank_values and ctx.blank_values["info"].get("total_errors") != 0:
        bad.append("errors on recalculation")
    return (2 if not bad else 0), f"{len(bad)} problems", bad


@criterion("F6", "F. Presentation", "Attribution: Growth Enablement with the original year; no historical attribution outside source/")
def f6(ctx):
    texts = " ".join(str(c.value) for ws in ctx.wb.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str))
    ok = "Growth Enablement" in texts and "2000" in texts and "Forrester" not in texts
    return (2 if ok else 0), f"GE={'Growth Enablement' in texts} year={'2000' in texts} historical={'Forrester' in texts}", []


# ---------------------------------------------------------------- run
def run(wb_path: pathlib.Path, manifest_path: pathlib.Path, reviewer: Optional[pathlib.Path]) -> list[Result]:
    manifest = json.loads(manifest_path.read_text())
    scores = json.loads(reviewer.read_text()) if reviewer and reviewer.exists() else {}
    results = []
    with tempfile.TemporaryDirectory() as td:
        ctx = Ctx(wb_path, manifest, pathlib.Path(td))
        for cid, dim, stmt, method, fn in CHECKS:
            if method == HUMAN:
                s = scores.get(cid, {})
                sc = s.get("score")
                results.append(Result(cid, dim, stmt, method, sc if sc in (0, 1, 2) else None,
                                      "reviewer score" if sc in (0, 1, 2) else "UNSCORED (human)", [s.get("note", "")] if s else []))
                continue
            try:
                sc, measured, ev = fn(ctx)
            except Exception as e:  # a crashed check scores 0 and says why
                sc, measured, ev = 0, f"check failed: {type(e).__name__}: {e}", []
            results.append(Result(cid, dim, stmt, method, sc, measured, ev))
    return results


def render(results: list[Result]) -> str:
    gate = [r for r in results if r.dimension == "Gate"]
    gate_pass = all(r.score == 2 for r in gate)
    lines = ["# Score sheet", "", f"**Gate: {'PASS' if gate_pass else 'FAIL'}**", ""]
    lines += ["| ID | Criterion | Method | Score | Measured |", "|---|---|---|---|---|"]
    for r in gate:
        lines.append(f"| {r.cid} | {r.statement} | {r.method} | {'' if r.score is None else r.score} | {r.measured} |")
    lines += ["", f"## Dimensions {'(counted)' if gate_pass else '(not counted: gate failed)'}", ""]
    lines += ["| ID | Dimension | Criterion | Method | Score | Measured |", "|---|---|---|---|---|---|"]
    totals: dict[str, list] = {}
    for r in results:
        if r.dimension == "Gate":
            continue
        lines.append(f"| {r.cid} | {r.dimension} | {r.statement} | {r.method} | {'—' if r.score is None else r.score} | {r.measured} |")
        totals.setdefault(r.dimension, [0, 0, 0])
        if r.score is not None:
            totals[r.dimension][0] += r.score
            totals[r.dimension][1] += 2
        else:
            totals[r.dimension][2] += 1
    lines += ["", "## Totals", "", "| Dimension | Scored | Of | Unscored (human) |", "|---|---|---|---|"]
    for d, (s, of, un) in totals.items():
        lines.append(f"| {d} | {s} | {of} | {un} |")
    auto_s = sum(r.score for r in results if r.method == AUTO and r.dimension != "Gate" and r.score is not None)
    auto_of = 2 * sum(1 for r in results if r.method == AUTO and r.dimension != "Gate")
    lines += ["", f"Automatic criteria: **{auto_s} / {auto_of}**. Human criteria are scored only from a reviewer file.", ""]
    lines += ["## Evidence", ""]
    for r in results:
        if r.evidence and any(str(e).strip() for e in r.evidence):
            lines.append(f"**{r.cid}** {r.measured}")
            lines += [f"- {e}" for e in r.evidence if str(e).strip()]
            lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("workbook", type=pathlib.Path)
    ap.add_argument("manifest", type=pathlib.Path)
    ap.add_argument("--reviewer", type=pathlib.Path, default=None)
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("score_sheet.md"))
    a = ap.parse_args(argv)
    results = run(a.workbook, a.manifest, a.reviewer)
    md = render(results)
    a.out.write_text(md)
    a.out.with_suffix(".json").write_text(json.dumps([r.__dict__ for r in results], indent=2))
    print(md)
    gate_pass = all(r.score == 2 for r in results if r.dimension == "Gate")
    return 0 if gate_pass else 1


if __name__ == "__main__":
    sys.exit(main())
