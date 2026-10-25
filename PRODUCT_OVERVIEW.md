# Product Overview: Sales Capacity Model

> **Describes the as-is software (package 2.1.0), which reproduces the original workbook.** The model is stated in [docs/MODEL.md](docs/MODEL.md); the blank modern workbook is `workbook/Sales_Capacity_Model.xlsx`; the redesign proceeds on branch `evolution`.


## The decision it supports

> "We want more revenue. Do we hire, or do we get better?"

The model puts both answers on the same income statement, so the comparison is margin to margin rather than opinion to opinion.

## Who it is for

| Audience | What they get |
|----------|---------------|
| CFO | Operating-income impact of each lever, side by side, with fully loaded sales cost |
| CRO / VP Sales | Where salespeople hit their ceiling, and why more leads or more salespeople won't move it |
| CEO / Board | Which capability to invest in, and what growth costs each way |
| Private equity operating partners | A fast, auditable read on whether a portfolio company's growth plan is volume-bound or quality-bound |

## How it works

```
Inputs ─► Capacity ─► Throughput ─► Revenue ─► Sales cost ─► Income statement ─► Lever ranking
                                                                               └► Obstacles to each lever
```

1. **Capacity:** opportunities held at once × (12 ÷ cycle months) = opportunities per territory per year.
2. **Throughput:** × close rate = deals; × deal size = revenue per territory; × territories = revenue.
3. **Cost:** salary + travel + commission per territory, plus sales overhead and marketing.
4. **Income statement:** cost of revenue, R&D and G&A as % of revenue, giving operating income.
5. **Scenarios:** each lever changed alone and in combination (default 10%), compared with baseline.
6. **Diagnostics:** the five common obstacles to each quality lever, with root causes.

## Inputs

| Group | Fields |
|-------|--------|
| Structure | territories, average deal size |
| Salesperson cost | base salary, load rate, commission rate, travel components and trips per year |
| Mechanics | opportunities manageable at once, sales cycle (months), ramp (months), close rate |
| Overhead | non-quota managers, sales engineers, sales admin, training, incentives |
| Marketing | personnel, web, events, advertising, direct mail, telemarketing, branding/PR, collateral |
| P&L shape | cost of revenue %, R&D %, G&A % |
| Optional | leads per territory |

Defaults are the original workbook's illustrative values. `scm template` prints them as JSON to edit.

## Outputs, per scenario

- Max opportunities, opportunities worked, deals and revenue per territory
- Cost per territory, salesperson costs, sales and marketing cost
- Revenue, operating income, and change vs baseline (absolute and %)
- **% Net Gain** as the workbook defines it: (Δrevenue − Δsales cost) ÷ baseline revenue
- **S&M ROI**: (revenue − S&M cost) ÷ S&M cost
- Lever ranking; lead utilization and excess leads when leads are supplied

## Results at the defaults (10% per lever, original workbook logic)

| Scenario | ΔRevenue | ΔSales cost | ΔOperating income |
|----------|---------:|------------:|------------------:|
| Add territories | 0 (year-1 ramp) | +2.25M | −2.25M (−7.1%) |
| Raise close rate | +11.25M | +0.90M | +5.98M (+18.8%) |
| Shorten sales cycle | +12.50M | +1.00M | +6.65M (+20.9%) |
| Raise deal size | +11.25M | +0.90M | +5.98M (+18.8%) |
| All three quality levers | +38.75M | +3.10M | +20.61M (+64.8%) |

Even with full-year credit for new territories (`--ramp-rule steady_state`), adding territories ranks last.

## Using it

Install from the repository root:

```
pip install -e .
```

Command line:

```
scm about                                   # what this is and where it came from
scm overview                                # this overview
scm template > my_inputs.json               # default inputs to edit
scm run --inputs my_inputs.json             # all scenarios, text table
scm run --set close_rate=0.3 --adjust 0.15  # quick overrides
scm run --json > results.json               # machine-readable output
scm diagnose close_rate                     # obstacles for one lever
scm verify                                  # prove the engine matches the workbook
```

Python:

```python
from sales_capacity_model import ModelInputs, ModelOptions, Adjustments, run_scenarios

results = run_scenarios(
    ModelInputs(territories=40, deal_size=120_000, close_rate=0.22, cycle_months=9),
    ModelOptions(ramp_rule="year_one", adjustments=Adjustments(close_rate=0.15)),
)
print(results["close_rate"].operating_income_change)
```

## Options: alternatives to the original's deliberate values

| Option | Values | Default |
|--------|--------|---------|
| `use_entered_salary` / `--use-entered-salary` | Use base salary × (1 + load rate) instead of the 87,750 the original types into its engine (a deliberate test value; docs/MODEL.md §6) | off (workbook) |
| `ramp_rule` / `--ramp-rule` | `workbook`: reproduces the original, including its inconsistency · `year_one`: new territories earn only post-ramp revenue everywhere · `steady_state`: full-year credit everywhere | `workbook` |
| `adjustments` / `--adjust`, `--adjust-<lever>` | Size of each lever's change | 10% each |

## Limits

- Measures the results of selling quality, not how to produce them.
- Cognitive load is an input, not derived from anything.
- Non-sales operating costs scale as a fixed % of revenue.
- One-year horizon. No attrition, backfill or multi-year ramp.

## Package contents

| Module | Role |
|--------|------|
| `inputs.py` | Inputs, derived totals, options, validation |
| `engine.py` | Capacity chain, scenarios, income statement, ranking |
| `diagnostics.py` | Obstacles and root causes per lever |
| `verify.py` | Parity check against the original workbook |
| `report.py` | Text and JSON output |
| `cli.py` | The `scm` command |
| `__about__.py` | Version, About and Overview text |
