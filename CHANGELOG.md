# Changelog

## Unreleased
- As-is salary $87,750 confirmed as a deliberate test estimate placed in the engine; recorded in the As-Is Index. New requirement DM-08: no value enters a calculation outside the ledger.
- Terminology rule: "salesperson", never "seller"; enforced by tests/test_terminology.py.
- Snapshot of the as-is state preserved as branch `as-is-2026-10-24` (commit 1e1b03c).
- Added current understanding and target design: `docs/MODEL_UNDERSTANDING.md` (language and lineage: what common sales words mean in this model, the analysis traditions it combines, the tab-to-tab logic; falsifiable system model, assumption ledger, territory design vs staffing, Little's Law at the salesperson level, Meadows leverage points, market comparison, corrections to earlier readings), `docs/DATA_MODEL_REQUIREMENTS.md` (entities, assumption record, structural assumptions S1–S9, test library, cross-checks, lifecycles, collection workflow, as-is field map, requirements DM-01 to DM-61), `docs/ORIENTATION.md` (rewritten orientation).
- Added `docs/AS_IS_INDEX.md`: every as-is artifact, the original orientation verbatim, as-is logic and sample results, findings as recorded vs as now understood.
- Dated status notes added to the top of as-is documents (About, Product Overview, Audit Findings, Discovery Assessment, Reassessment, JSON spec); their content is unchanged.
- README rewritten as a map of current vs as-is documents.
- Data module database schema (SQLite V1): `src/sales_capacity_model/db/schema.sql` (9 layers, append-only and frozen-baseline triggers, Finance-only validation, sealed leadership beliefs, perception gap, candidate set and confidence views), `seed.sql` (11 collection steps, field catalog with leverage points, structural assumptions S1–S9, 12 tests, 15 causal links), `docs/DATABASE_SCHEMA.md`; 8 schema tests on the as-is sample data.

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
