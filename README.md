# Sales Capacity Model

A cognitive-temporal throughput model of sales capacity, connected to the income statement.

**Core premise:** sales capacity is not labor hours. It is cognitive bandwidth constrained by time.

```
Max opportunities / year = Manageable opportunities × (12 ÷ Sales cycle months)
Revenue = Max opps × Close rate × Deal size × Territories
```

Originated 2000. Audited by Ernst & Young, 2003. Published as the Forrester Sales and Marketing Efficiency Model, 2011. Documentation and rebuild, 2026.

## Repository layout

| Path | What it is | Status |
|------|-----------|--------|
| `source/Sales_and_Marketing_Effectiveness_Model_original.xls` | Original workbook | Never edit. Reference copy. |
| `source/workbook_cells.csv` | Every cell, formula, and stored value from the workbook (415 cells) | Ground truth for what the workbook does |
| `model/recompute.py` | Rebuilds every calculation in Python and checks it against the workbook | 48/48 match |
| `spec/sales_capacity_model_specification.json` | Machine-readable spec for analysis | v2.1, reconciled to workbook |
| `docs/Sales_Capacity_Model_Technical_Specification_v2.0.docx` | Narrative white paper | v2.0, needs the corrections in `AUDIT_FINDINGS.md` |
| `AUDIT_FINDINGS.md` | Defects in the workbook and errors in v2.0 spec | Read before rebuilding |
| `CHANGELOG.md` | Version history | |

## Verify the model

```
python3 model/recompute.py
```

Exit code 0 means the Python logic reproduces the workbook exactly. Run this after any change to the logic.

## Working rules

1. `source/` is read-only history.
2. Change logic in `model/`, then rerun `recompute.py`. Intentional departures from the workbook (fixing F1 to F3) go in a new function, not by editing the reproduction.
3. Every change to spec or logic gets a `CHANGELOG.md` entry.
