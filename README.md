# Sales Capacity Model

A falsifiable system model of a company's commercial engine: it states how the sales system is believed to work, tests those beliefs against the company's own financial results, and then explores what-if changes from a baseline that describes reality.

**The data tab is an assumption ledger.** Every entry is a written, falsifiable claim with a declared basis, scope and owner, and a way to test it.

**Sales capacity is not labor hours.** Territories are a design choice carrying an expected yield; salespeople are a hiring choice whose capacity is cognitive bandwidth constrained by time. Revenue happens where the two meet.

```
Salesperson capacity (opportunities per year) = opportunities held at once × (12 ÷ cycle months)
As-is model:  Revenue = capacity × close rate × deal size × territories
```

## Documents

**Current understanding and target design**

- [Model Understanding](docs/MODEL_UNDERSTANDING.md): what the model is, territory design vs staffing, how assumptions are tested, Meadows leverage points, market comparison
- [Data Model and Requirements](docs/DATA_MODEL_REQUIREMENTS.md): the assumption ledger, entities, record schema, tests, lifecycle, collection workflow, numbered requirements, map from the as-is sheet
- [Orientation (rewritten)](docs/ORIENTATION.md): proposed first tab of the rebuilt workbook
- [Governing Reassessment](docs/Commercial_Effectiveness_Reassessment.md): product and architecture direction for scenarios

**As-is model (preserved unchanged)**

- [As-Is Index](docs/AS_IS_INDEX.md): every as-is artifact, the original orientation text, logic, sample results, and findings as recorded vs as now understood
- [About](ABOUT.md) · [Product Overview](PRODUCT_OVERVIEW.md) (v2.1 software) · [Audit Findings](AUDIT_FINDINGS.md) · [Discovery and Architecture Assessment](docs/Discovery_and_Architecture_Assessment.md)
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
| `src/sales_capacity_model/` | The Python package (`scm` command), reproducing the as-is workbook |
| `tests/` | Workbook parity (48/48), option tests, terminology rule |
| `source/` | Original workbook and its full formula export. Read-only history. |
| `spec/` | Machine-readable JSON specification of the as-is model (v2.1) |
| `docs/` | Current understanding, data model requirements, orientation, as-is index, assessments, white paper v2.0 |

## Working rules

1. `source/` is never edited.
2. The as-is model stays reproducible: `scm verify` must pass with defaults.
3. As-is documents are never rewritten; superseded readings get a dated note and a pointer to the current document.
4. Every change gets a `CHANGELOG.md` entry.
5. **Terminology: never "seller".** Always "salesperson" / "salespeople", in code, docs and output. Enforced by `tests/test_terminology.py`.

Originated 2000 · E&Y audit 2003 · updated edition 2011 · Python rebuild 2026.

© 2000–2026 Growth Enablement. All rights reserved. The model and its logic are owned by Growth Enablement. Author: Scott Santucci.
