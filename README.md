# Sales Capacity Model

A model for comparing commercial investment choices, chiefly adding selling resources versus improving the productivity of the resources a company already has, by carrying each choice through a pro forma income statement to operating income. Created 2000, audited by Ernst & Young 2003, updated 2011. Growth Enablement owns the model and its logic.

**Sales capacity is not labor hours.** A salesperson's capacity is the opportunities they can hold and advance well at once, turned over by the sales cycle. A territory is a design choice, not a person. The model is axiomatic: it asks for some quantities twice, so the data it is given can be checked against itself.

```
Opportunities per year per territory = opportunities manageable at once × (12 ÷ cycle months)
Revenue = opportunities per year × close rate × deal size × territories
```

## Where things are

| Read | For |
|---|---|
| [canonical/FOUNDATION.md](canonical/FOUNDATION.md) | The one statement of what the model is, its built-in constraints, and Gate 1 (modern replication) with its acceptance tests |
| [canonical/INTENT_LEDGER.md](canonical/INTENT_LEDGER.md) | What is confirmed and what is open about the original's intent |
| [FILE_RULES.md](FILE_RULES.md) | Where every file lives, what is immutable, what is generated, what never enters the repository |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Version control: branches, commits, pull requests, required checks, versions and releases |
| [docs/AS_IS_INDEX.md](docs/AS_IS_INDEX.md) | Reference record of the original, with its text quoted word for word |
| `docs/archive/` | Superseded documents, kept for the record |

## Repository layout

| Path | What it is |
|---|---|
| `source/` | The original workbook and its formula export. Evidence; never modified (checked by `tests/test_source_integrity.py`) |
| `canonical/` | The canonical statement and the intent ledger |
| `src/sales_capacity_model/` | Python engine reproducing the original (the oracle; `scm` command) |
| `tools/` | Workbook builder, LibreOffice recalculation, rubric |
| `tests/` | Parity, workbook gate, source integrity, terminology |
| `workbook/` | The generated blank modern workbook, its manifest and score. Never edited by hand |

## Quick start

```
pip install -e .
scm verify        # 48/48 original outputs reproduced
python -m pytest -q
```

Branches: `main` is the accepted product; work arrives by pull request (see CONTRIBUTING.md). `evolution` holds the redesign and is parked until Gate 1 is accepted.

© 2000–2026 Growth Enablement. All rights reserved. Author: Scott Santucci.
