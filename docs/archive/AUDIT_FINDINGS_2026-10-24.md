> **Archived 2026-10-25.** First reading of the original (2026-10-24). Its "workbook defects" F1–F3 are deliberate test values and declared assumptions; see [MODEL.md §6](../MODEL.md). Its spec errors F4–F8 were real and are fixed in the JSON spec v2.1. Kept as a record of the interpretation, not as a description of the model.

# Workbook Reconciliation Findings

> **As-is record, kept unchanged (note added 2026-10-24).** The findings below are the audit as first recorded. Under the current understanding, several are undeclared assumptions rather than defects: F1 (hard-coded salary) and F2 (year-one ramp) are to be confirmed and declared; the contracts and revenue inputs are the actuals that test the assumptions; the $75,000 deal size is a deliberate reference value. F3 (improve-all ramp) remains a defect. See [docs/AS_IS_INDEX.md](docs/AS_IS_INDEX.md) and [docs/MODEL_UNDERSTANDING.md](docs/MODEL_UNDERSTANDING.md).


Date: 2026-10-24
Method: converted the original `.xls` to read its formulas (`source/workbook_cells.csv`, 415 cells), then rebuilt every calculation (now `scm verify` / `src/sales_capacity_model/engine.py`). All 48 stored outputs on the Impact Analysis sheet reproduce exactly.

## Verdict

- **Core capacity logic: valid.** `Max opps = (12 / cycle) × manageable opps`, then × close rate × deal size × territories. Matches the spec.
- **Conclusion holds: valid.** Every quality lever beats adding territories under every measure the workbook reports.
- **Spec v2.0 had five errors**, and the workbook has three internal defects. Details below. Spec errors are fixed in the JSON (v2.1); the `.docx` is kept as drafted and needs the same corrections.

## Workbook defects (in the original model)

| ID | Defect | Where | Effect at defaults |
|----|--------|-------|--------------------|
| F1 | Fully loaded salary is hard-coded at **87,750**. The Data Entry value (**116,850** = 95,000 × 1.23) is never used. | Performance Breakdown row 11 (C, F, G, H, J) | Salesperson costs understated by 29,100 per salesperson, 2.91M total. Baseline operating income would be 28.9M, not 31.8M. Ranking of levers unchanged. |
| F2 | Ramp time applies only to added territories: they earn `(12 − ramp)/12` of a year. At 12-month ramp, new territories produce **0 revenue** in year 1 but carry full cost. | Performance Breakdown E25 | "Hire" shows revenue flat and operating income **down 2.25M**. This is defensible as a year-1 view, but it is a modeling choice that should be stated, not hidden. |
| F3 | "Improve all" subtracts the *ramped* share instead of the *un-ramped* share, so new territories get **full-year** credit. Opposite of F2. | Performance Breakdown K25 | Improve-all revenue overstated by up to 15.1M (10 territories × 1.5125M). With F2's logic it would equal the combined-quality revenue (151.25M) at higher cost. |

## Spec v2.0 errors (in what we wrote)

| ID | v2.0 said | Workbook actually does |
|----|-----------|------------------------|
| F4 | % Net Gain = ΔOperating income ÷ baseline operating income | `(ΔRevenue − ΔSales costs) ÷ baseline revenue`. Ignores revenue-linked COGS, R&D, G&A. Close rate shows **9.2%**, not 18.8%. |
| F5 | S&M ROI = Revenue ÷ S&M cost = 3.04 | `(Revenue − S&M) ÷ S&M` = **2.04** |
| F6 | Ramp time is not integrated | It is, in the territory scenarios only (F2, F3) |
| F7 | Cell references E8, E10, E30… | Off by one row and column. Use `source/workbook_cells.csv`. |
| F8 | JSON scenario results: territories net gain −7.1% shown as "percentage_net_gain" | Mixed two metrics. JSON v2.1 now reports both the workbook metric and true operating-income change, recomputed. |

## Unused inputs

"Number of contracts last year" (755) and "Revenue from those contracts" (25M) are entered but feed nothing. 25M ÷ 755 = 33,113, which conflicts with the 75,000 deal size used.

## Corrected results at defaults (10% per lever)

| Scenario | ΔRevenue | ΔSales cost | ΔOperating income | % Net Gain (workbook) | S&M ROI |
|----------|---------:|------------:|------------------:|----------------------:|--------:|
| Add territories | 0 | +2.25M | −2.25M (−7.1%) | −2.0% | 1.86 |
| Close rate | +11.25M | +0.90M | +5.98M (+18.8%) | +9.2% | 2.26 |
| Cycle time | +12.50M | +1.00M | +6.65M (+20.9%) | +10.2% | 2.29 |
| Deal size | +11.25M | +0.90M | +5.98M (+18.8%) | +9.2% | 2.26 |
| Combined quality | +38.75M | +3.10M | +20.61M (+64.8%) | +31.7% | 2.77 |
| Improve all* | +53.88M | +5.66M | +27.30M (+85.8%) | +42.9% | 2.90 |

\* Inflated by F3.

## Decisions needed before the rebuild

1. Salary: use the entered 116,850 (fix F1)?
2. Territory ramp: one consistent rule across all columns, and show year 1 and steady state separately?
3. Headline metric: keep the workbook's % Net Gain, switch to Δoperating income, or show both?
