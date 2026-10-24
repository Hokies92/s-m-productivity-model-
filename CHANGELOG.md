# Changelog

## Unreleased
- Terminology rule: "salesperson", never "seller"; enforced by tests/test_terminology.py.

## Package 2.1.0 — 2026-10-24
- Installable Python package `sales-capacity-model` (src layout, no runtime dependencies, Python 3.9+).
- `scm` command: `about`, `overview`, `template`, `run`, `diagnose`, `verify`.
- Engine reproduces all 48 workbook outputs by default. Open decisions exposed as options: `use_entered_salary` (F1) and `ramp_rule` = workbook / year_one / steady_state (F2, F3). Per-lever adjustment sizes.
- Optional `leads_per_territory` extension: opportunities worked = min(capacity, leads); reports utilization and excess leads.
- Worksheet 4 diagnostics packaged as data.
- Added `ABOUT.md` and `PRODUCT_OVERVIEW.md`. README rewritten.
- `model/recompute.py` retired; its check now lives in `scm verify` and `tests/`.

## v2.1 — 2026-10-24
- Exported all 415 workbook cells with formulas to `source/workbook_cells.csv`.
- Added `model/recompute.py`: reproduces all 48 Impact Analysis outputs exactly.
- JSON spec reconciled to the workbook: % Net Gain and S&M ROI formulas, ramp-time usage, hard-coded salary, unused inputs, recomputed scenario results.
- Added `AUDIT_FINDINGS.md` (3 workbook defects, 5 spec errors, 3 open decisions).
- `.docx` white paper left at v2.0 pending corrections.

## v2.0 — 2026-10 (initial documentation)
- Technical specification (`.docx`) and JSON spec drafted from the workbook's values and structure.

## v1 — 2000 / 2003 / 2011
- Model created (2000), E&Y accuracy audit (2003), updated edition (2011).
