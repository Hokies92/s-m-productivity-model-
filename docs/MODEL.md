# The Model: current statement

This is the one current statement of what the Sales Capacity Model (2000; Sales and Marketing Efficiency Model, 2011 edition) is. Any document in this repository that disagrees with it is wrong and is corrected or archived. Part A describes the model as it is; Part B describes where the rebuild is taking it. The as-is is what `main` holds and what the tests enforce. The evolution lives on the `evolution` branch until an as-is version is accepted.

© 2000–2026 Growth Enablement. All rights reserved. Author: Scott Santucci.

---

# Part A. The model as it is

## 1. What it is

A **comparative economic argument, made in arithmetic**, about where a company's next commercial dollar should go. Its type is closer to an investment comparison than to a capacity model, a forecast or a simulation. The throughput chain is the premise; the income statement is the conclusion; four fixed scenarios are the cases compared. It was built to settle one recurring decision, not to explore many.

It is not a forecast, not a staffing plan, not an evaluation of individual salespeople, and not a benchmark.

## 2. Core purpose

To show, in a form a CFO can audit by hand, that improving how each opportunity is handled (close rate, cycle time, deal size) returns more operating income than adding more of what the company already does (territories and salespeople, and by extension leads). The Orientation sheet says this in its first paragraph. The Scenario Diagnostic sheet then names what stands between the company and each improvement: the handoff from the argument to the work.

## 3. Decisions it drives

One primary: hire more, or improve how the current team sells. Three subordinate: which quality lever to pursue first (the columns rank them for that company); how much an improvement is worth in operating income, and therefore what could be spent to get it; and which obstacles the chosen lever meets (Scenario Diagnostic).

## 4. How it works

```
Entry sheet      ~40 figures a company already has, in Finance's language
      ↓
Chain            opportunities per salesperson per year = opportunities managed at once × (12 ÷ cycle months)
                 transactions per salesperson = × close rate
                 revenue per salesperson      = × deal size
                 revenue                      = × territories          (one filled, ramped salesperson per territory)
      ↓
Scenarios        four columns, each moves ONE input by ONE chosen share (default 10%); two combined
                 columns borrow the moved inputs from the single-lever columns; nothing else differs
      ↓
Income statement cost of revenue, R&D, salesperson pay, travel, commission, sales overhead, marketing, G&A
                 → operating income, percentage net gain, sales and marketing ROI, for every column
      ↓
Diagnostic       five common obstacles per scenario
```

The conclusion comes from the income statement, not the chain. The chain is linear in every lever, so each 10% change adds about the same revenue. A quality improvement costs commission on the new revenue; a new territory costs salary and travel before it earns, and earns (12 − ramp) ÷ 12 of a year. That asymmetry is the argument, and it is what the compared tools leave out.

## 5. Definitions and units

| Term | Means | Unit |
|---|---|---|
| Territory | A funded slot in the coverage design, filled or open; not a person | count |
| Salesperson | A person in a quota-carrying role, measured as part of a system, never by name | count |
| Opportunities manageable at once | The most qualified opportunities one salesperson can hold and advance well at the same time: cognitive capacity, not hours | per salesperson |
| Cycle | Months from qualified opportunity to signature, won deals | months |
| Close rate | Won ÷ (won + lost) qualified opportunities, by count | ratio |
| Deal size | Average revenue per contract (revenue ÷ contracts when calculated) | currency per contract |
| Ramp | Months until a new salesperson reaches average productivity | months |
| Operating income | Revenue − cost of revenue − operating expenses, on the pro forma income statement | currency |

In the as-is, throughput is computed per salesperson and scaled by territories, which is the special case where every territory holds one filled, ramped salesperson.

## 6. Values the original holds beside each other on purpose

The sample values are illustrative and come from different sources, so they deliberately do not agree. The sample is never a company: it is not reconciled, calibrated or explained. Only a company's own figures are.

Several inputs sit beside a second figure that should agree with them. Where they disagree, the reader learns something about the company. This is the model's validation layer, left implicit, and the only part the original did not complete.

| Pair | What a disagreement means | How the blank workbook holds it |
|---|---|---|
| Deal size typed ($75,000) beside revenue ÷ contracts ($33,113) | The typed figure is a reference value with a scope; where a company's own revenue ÷ contracts differs, the reference is outside its scope for that company | Deal size is an entry with two ways to fill it; the value used is shown |
| Salary typed into the engine ($87,750) beside the entry sheet's calculation ($116,850) | An entry can be overridden; the engine reads the entry, not the calculation | Fully loaded salary is an entry with a direct figure or the calculation; the value used is shown |
| Ramp credited (12 − ramp) ÷ 12 in "hire more" and deducted again in "improve all" | Ramp is an assumption to declare with one rule | Both formulas reproduced exactly; the rule stated in words beside them |

They are tests of method: compose the whole before judging a part. A reader who compares parts to parts finds defects; a reader who composes first finds entries with options, values with scope, and a rule to declare.

## 7. How it is unique, as is

Against sales capacity calculators, velocity simulators, quota planners and CRM forecasting, it is the only one that (a) carries a sales change to operating income rather than to revenue or headcount; (b) compares quantity and quality levers in one frame with one arithmetic; (c) can be audited cell by cell by someone who did not build it; (d) holds places where the company's own numbers can contradict each other. It has the first three fully and the fourth in embryo. What the early assessments read as gaps (fixed scenarios, one period, no demand constraint) are consequences of (c) or outside the decision it drives.

## 8. The blank workbook (`workbook/Sales_Capacity_Model.xlsx`)

The as-is, made general and modern without a change of logic: five sheets, every label and description word for word, every formula reproduced (200 of 200 numeric formula cells, `tools/rubric.py` gate), no company data, no typed constants in the engine, blank-safe, named inputs, validation, locked formulas, grouped detail, a rule in words beside every calculation. The three income statement ratios are entries. Impact Analysis `I9`, a stray fill-right formula in a spacer column, is excluded with the reason in the rubric code.

---

# Part B. Where the rebuild is taking it (branch `evolution`)

## 9. The direction

Make the implicit validation layer explicit and keep everything else. The entry sheet becomes a **register** of state assumptions (each with a basis: validated by Finance, the client's entry, the model's estimate, or a labeled default) whose implications are compared with the client's actuals in cross-checks. Scenarios and the equations applied to the register live in a separate **modeller**. Territory and salesperson become separate counts linked by assignment, so open territories and ramp carry their cost. The income statement stays the constraint every scenario passes through.

## 10. Three kinds of assumption, and where each lives

| Kind | What | Lives in | Tested by |
|---|---|---|---|
| State | A belief about the system as it is | The register | The company's actuals, via cross-checks |
| Method | An equation or rule applied to the register | Beside each formula, in words; the modeller | Parity with the original; the true-up |
| Intervention | A hypothesis: "close rate +10%" | The modeller's scenario table only | Next period's register |

Intervention hypotheses never enter the register; if they did, the baseline would validate against its own proposals.

## 11. Deferred, and why

Territory and hiring scenarios need the territory–salesperson assignment explicit and break the simple inverse (target operating income → required lever). The original's "hire more" column is the quantity lever shown beside the quality levers; it is in the as-is workbook and returns to the evolution with them. The Scenario Diagnostic returns keyed to scenario ids.

---

# Invariants (enforced on `main`)

1. **Oracle.** `source/` is never edited. The Python package with default options reproduces all 48 original outputs (`tests/test_model.py`).
2. **Parity.** With the original's inputs, the blank workbook reproduces every original numeric formula cell (`tools/rubric.py` G1–G4; `tests/test_asis_workbook.py`).
3. **No typed constants** in any engine or analysis formula (G3).
4. **Blank-safe.** With no data entered, no cell shows an error and no engine or analysis cell shows a number (B4).
5. **Rule in words** beside every calculation row (C3).
6. **Terminology.** Salesperson / salespeople; not the s-word, not the abbreviation of "representative". Outside `source/`, archived documents and manifests quoting the original.
7. **Income statement in the loop.** Every scenario result is an operating income after all costs.
8. **No regression.** No automatic rubric criterion scores lower than at the last accepted version (`workbook/Sales_Capacity_Model.score.json`).
9. **Unit.** On the `evolution` branch, throughput is per salesperson; the as-is oracle is labeled as per territory.
10. **Register purity** (evolution). No scenario or intervention field in the register; register and modeller never share a key.
