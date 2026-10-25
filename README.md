# Sales Capacity Model

A comparative economic argument, made in arithmetic, about where a company's next commercial dollar should go: improve how each opportunity is handled (close rate, cycle time, deal size), or add more of what the company already does (territories, salespeople). Built 2000, audited by Ernst & Young 2003. The argument is settled at operating income, after every cost, in a form a CFO can audit by hand.

**Sales capacity is not labor hours.** A salesperson's capacity is the opportunities they can hold and advance well at once, turned over by the sales cycle. Territories are a coverage design, not people.

**Branches.** `main` is the as-is: the frozen source, the Python oracle, and the blank modern workbook proven against the original. `evolution` is where the rebuild (register, modeller, territory–salesperson separation) proceeds until an as-is version is accepted.

```
Salesperson capacity (opportunities per year) = opportunities held at once × (12 ÷ cycle months)
As-is model:  Revenue = capacity × close rate × deal size × territories
```

## Documents

**Start here**

- [MODEL.md](docs/MODEL.md): the one current statement: what the model is, its purpose, the decisions it drives, how it works, the deliberate paired values, how it is unique, the evolution, the invariants. Where any other document disagrees, this one wins.
- [Blank workbook](workbook/Sales_Capacity_Model.xlsx): the as-is, general and modern, no company data. Built by `tools/build_asis_modern.py`; scored by `tools/rubric.py` ([score sheet](workbook/Sales_Capacity_Model.score.md)); gated by `tests/test_asis_workbook.py`
- [FOUNDATION.md](docs/FOUNDATION.md): what stands from the original and the rebuild, and why it makes a different model
- [CONTRIBUTING.md](CONTRIBUTING.md): what is protected, branches, the commit protocol, the pre-push hook, terminology

**Supporting (current, aligned to MODEL.md)**

- [Model Understanding](docs/MODEL_UNDERSTANDING.md): the longer reasoning: territory design vs staffing, how assumptions are tested, Meadows leverage points, market comparison, language and lineage
- [Reassessment](docs/archive/Commercial_Effectiveness_Reassessment_2026-10-24.md): product and architecture direction for the evolution (see its status note)
- On the `evolution` branch: the register/modeller workbook, its builder and tests, the register and modeller schemas, the data model requirements
- [System Diagnostic](docs/SYSTEM_DIAGNOSTIC.md): what went wrong in the first two days of the rebuild, and the remedy

**As-is model (preserved unchanged)**

- [As-Is Index](docs/AS_IS_INDEX.md): every as-is artifact, the original orientation text, logic, sample results, and findings as recorded vs as now understood
- [About](ABOUT.md) · [Product Overview](PRODUCT_OVERVIEW.md) (the as-is oracle, package v2.1)
- Archived readings: `docs/archive/` (first audit findings, discovery assessment, orientation draft, white paper v2.0)
- Snapshot branch: `as-is-2026-10-24`

## Quick start (as-is software)

```
pip install -e .
scm about
scm run
scm verify        # 48/48 workbook outputs reproduced
```

```python
from sales_capacity_model import ModelInputs, run_scenarios
results = run_scenarios(ModelInputs(close_rate=0.3))
```

## Repository layout

| Path | What it is |
|------|-----------|
| `src/sales_capacity_model/` | The as-is oracle: Python package (`scm` command) reproducing the original workbook per territory |
| `tests/` | As-is parity (48/48), blank-workbook gate and no-regression, terminology rule |
| `source/` | Original workbook and its full formula export. Read-only history. |
| `spec/` | Machine-readable JSON specification of the as-is model (v2.1) |
| `tools/` | `build_asis_modern.py` (workbook + manifest), `rubric.py` (measured criteria), `recalc.py` (LibreOffice recalculation) |
| `workbook/` | The blank workbook, its manifest and its score sheet |
| `docs/` | MODEL.md and supporting documents; `archive/` for superseded readings |

## Working rules

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: `source/` and the as-is oracle are never rewritten; every other document is corrected or archived when wrong; `docs/MODEL.md` is the single current statement; tests pass before every commit; each commit names the invariant it serves; the terminology rule is enforced by test.

Originated 2000 · E&Y audit 2003 · updated edition 2011 · Python rebuild 2026.

© 2000–2026 Growth Enablement. All rights reserved. The model and its logic are owned by Growth Enablement. Author: Scott Santucci.
