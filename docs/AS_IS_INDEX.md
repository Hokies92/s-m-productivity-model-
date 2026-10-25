# As-Is Model: Index

Status: **reference record of the as-is model, preserved unchanged.** Everything listed here describes the original workbook and its faithful reproduction. The current statement of the model is [MODEL.md](MODEL.md); supporting reasoning in [MODEL_UNDERSTANDING.md](MODEL_UNDERSTANDING.md) and [DATA_MODEL_REQUIREMENTS.md](DATA_MODEL_REQUIREMENTS.md).

Snapshot: the branch `as-is-2026-10-24` on GitHub holds the repository exactly as it stood before the redesign documents were added (commit `1e1b03c`).

© 2000–2026 Growth Enablement. All rights reserved.

## What the as-is model is

The Sales and Marketing Efficiency Modeling Tool: five worksheets (Orientation, Data entry, Performance breakdown, Impact Analysis, Scenario Diagnostic). Originated 2000, audited for accuracy by Ernst & Young in 2003, updated in 2011. Reproduced exactly in Python in 2026: all 48 stored outputs on the Impact Analysis sheet match (`scm verify`).

## As-is artifacts

| Artifact | What it holds | Status |
|---|---|---|
| `source/Sales_and_Marketing_Effectiveness_Model_original.xls` | The original workbook | Frozen; never edited |
| `source/workbook_cells.csv` | All 415 non-empty cells: sheet, cell, formula or input, stored value | Ground truth for what the as-is model does |
| `src/sales_capacity_model/` (package 2.1.0) | Python reproduction; defaults reproduce the workbook exactly; options for salary source and ramp rule | Current software |
| `tests/test_model.py` | Workbook parity (48/48) and option tests | Passing |
| `spec/sales_capacity_model_specification.json` (v2.1) | Machine-readable description of the as-is inputs, formulas, cell references and scenario results | Reconciled to the workbook |
| `docs/archive/Sales_Capacity_Model_Technical_Specification_v2.0.docx` | First narrative description | Contains errors listed in `AUDIT_FINDINGS.md` |
| `docs/archive/AUDIT_FINDINGS_2026-10-24.md` | First reading: findings F1–F3 (now understood as deliberate test values), spec errors F4–F8 | Findings stand as the as-is record; see the reframing note at its top |
| `docs/archive/Discovery_and_Architecture_Assessment_2026-10-24.md` | Verdicts, sensitivity, break-even, six gaps, target architecture | As-is assessment; partly superseded |
| `docs/Commercial_Effectiveness_Reassessment.md` | Governing product and architecture direction | Still governing for scenarios and architecture; extended by the new documents |
| `ABOUT.md`, `PRODUCT_OVERVIEW.md` | Project description and the v2.1 software overview | Describe the as-is software accurately |

Working documents in Claude Docs (not copied into the repo): [Discovery and Architecture Assessment](https://claude.ai/artifact/U4pvy1F8aYHdJuVzPGE1Lh), [Consolidated Review of Five Assessments](https://claude.ai/artifact/WEPdCoP1jGQPCNRYFNJDwn), [Data Entry Model: Deep Dive](https://claude.ai/artifact/9EgvTQicadD59WZ8Qcx4Ez).

## As-is orientation text (verbatim)

From the Orientation sheet, cells B1–B8. The historical attribution line in B10 is retained in the source file only.

> **Sales and Marketing Efficiency Modeling Tool**
>
> Overview: This worksheet is intended to provide you with visibility into your sales and marketing activities. This model helps you examine four business scenarios that can help you improve your business performance: increase the size of your sales force, increase your sales organization’s close rate, decrease your sales cycle time, or increase your average order size. By entering historical and assumptive data, you will be able to determine the impact of each of these investment decisions on your top line revenue and bottom line performance. For example, a 10% decrease in your sales force, coupled with a 10% improvement in your average order size could increase your top line revenue by 7%, but increase your operating margin by almost 800%. Finally, this tool will help you identify the challenges you must overcome to achieve success in each of the business scenarios and provide you with a better framework to assess current and future sales and marketing investments.
>
> It is broken down into the following sections: 1) Data entry - enter historical data and metrics assumptions about your sales and marketing performance. 2) Performance breakdown - a what-if tool that allows you to determine the impact of incremental improvements in your sales and marketing activities. 3) Impact Analysis - highlights the potential impact on your Income Statement by making incremental improvements. 4) Scenario Diagnostic - Lists common are obstacles that stand in the way of achieving your intended results for each scenario.
>
> A Few Points: This is a generic tool intended to give you insight into your sales and marketing mechanics. For a more complete analysis, we recommend that you perform this assessment for each of your sales channels and product lines. Also, there are attributes about your business that are different from others. This model can be tailored to your company. Finally, "increase leads" is not listed as a business scenario because we consider lead generation to be a more leveraged way to conduct sales prospecting. The number of leads, how to acquire them, and how much you can invest to acquire those leads are all handled in the tactical "drill down" spreadsheets that accompany this model.

## As-is logic in brief

```
Max opportunities per territory per year = opportunities manageable at once × (12 ÷ cycle months)
Deals = max opportunities × close rate
Revenue per territory = deals × deal size
Revenue = revenue per territory × territories
Cost per territory = $87,750 (typed into the engine; a deliberate test value) + travel + revenue per territory × commission
Operating income = revenue − revenue × (13.22% + 10.19% + 15.40%) − (territories × cost per territory + sales overhead + marketing)
```

Seven scenario columns: baseline, add territories, close rate, cycle time, deal size, combined quality levers, improve all; each lever changed 10%. Added territories earn (12 − ramp) ÷ 12 of a year of revenue in the add-territories column; the improve-all column credits them with a full year.

## As-is sample results

| Scenario | Revenue | Operating income | % net gain (workbook) | S&M ROI (workbook) |
|---|---|---|---|---|
| Baseline | $112.50M | $31.81M | — | 2.04 |
| Add territories | $112.50M | $29.56M | −2.0% | 1.86 |
| Close rate +10% | $123.75M | $37.80M | +9.2% | 2.26 |
| Cycle −10% | $125.00M | $38.46M | +10.2% | 2.29 |
| Deal size +10% | $123.75M | $37.80M | +9.2% | 2.26 |
| Combined quality | $151.25M | $52.42M | +31.7% | 2.77 |
| Improve all | $166.38M | $59.12M | +42.9% | 2.90 |

Workbook definitions: % net gain = (Δrevenue − Δsales cost) ÷ baseline revenue; S&M ROI = (revenue − S&M cost) ÷ S&M cost.

## As-is findings, as recorded and as now understood

| Finding (archived AUDIT_FINDINGS) | Recorded as | Now understood as |
|---|---|---|
| F1 salary hard-coded at $87,750; entered $116,850 unused | Defect | **Confirmed by Scott (2026-10-24):** an estimate placed in the engine deliberately, to test whether a reviewer understood how the model works. It shows why no value may enter a calculation outside the ledger (DM-08) |
| F2 added territories earn zero in year one at 12-month ramp | Undisclosed modeling choice | A declared assumption (structural S2, S5) |
| F3 improve-all credits added territories with a full year | Defect | With F2, the third deliberate value: ramp credited two ways, testing whether the reader declares one ramp rule (MODEL.md §6). The rebuild holds ramp as one register entry with one rule. |
| Contracts and revenue entered but unused | Dead inputs | The actuals that test the assumptions |
| $75,000 deal size vs $33,113 implied | Data problem | A deliberate reference value from another client; declare its scope |
| New hires charged commission with no revenue (from the governing reassessment) | Causal inconsistency | Still an inconsistency to resolve with a declared rule |
