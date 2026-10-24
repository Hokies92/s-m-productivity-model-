# Sales Capacity Model

A cognitive-temporal throughput model of sales capacity, connected to the income statement.

**Sales capacity is not labor hours. It is cognitive bandwidth constrained by time.**

```
Max opportunities / year = Manageable opportunities × (12 ÷ Sales cycle months)
Revenue = Max opportunities × Close rate × Deal size × Territories
```

- [About](ABOUT.md): what the project is, why it exists, where it came from
- [Product Overview](PRODUCT_OVERVIEW.md): who it's for, inputs, outputs, how to use it
- [Audit Findings](AUDIT_FINDINGS.md): workbook defects and open decisions
- [Discovery and Architecture Assessment](docs/Discovery_and_Architecture_Assessment.md): verdicts, sensitivity, gaps, target architecture, roadmap

## Quick start

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
| `src/sales_capacity_model/` | The Python package (`scm` command) |
| `tests/` | Tests, including workbook parity (`pytest`) |
| `source/` | Original workbook and its full formula export. Read-only history. |
| `spec/` | Machine-readable JSON specification (v2.1) |
| `docs/` | White paper (v2.0; needs the corrections in `AUDIT_FINDINGS.md`) |

## Working rules

1. `source/` is never edited.
2. Defaults reproduce the original workbook. Changes to logic go behind an option, and `scm verify` must still pass with defaults.
3. Every change gets a `CHANGELOG.md` entry.

Originated 2000 · E&Y audit 2003 · Forrester edition 2011 · Python rebuild 2026. Author: Scott Santucci.
