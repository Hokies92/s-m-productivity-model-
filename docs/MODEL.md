# The Model: current statement

This is the current canonical interpretation of the Sales Capacity Model (2000; Sales and Marketing Efficiency Model, 2011 edition). The original workbook and its formula export are the evidence; this document is the interpretation built on them, and Scott reviews changes to it. Where another document disagrees, this one governs until the evidence says otherwise. Part A describes the model as it is; Part B describes where the rebuild is taking it. The as-is is what `main` holds and what the tests enforce. The evolution lives on the `evolution` branch until an as-is version is accepted.

© 2000–2026 Growth Enablement. All rights reserved. Author: Scott Santucci.

---

# Part A. The model as it is

Basis is marked where it matters to the conclusion: **source** (the original workbook or its formula export), **Scott** (confirmed intent), **math** (follows from the source), **interpretation** (a conclusion that reasonably follows but is not confirmed). Confirmed and open intent is tracked item by item in the project's intent ledger.

## 1. What it is

**Established.** A model for comparing commercial investment choices, chiefly adding selling resources versus improving the productivity of the resources a company already has, by carrying each choice through a pro forma income statement to operating income, and then naming the challenges to overcome for each. Source: Orientation B5 ("determine the impact of each of these investment decisions on your top line revenue and bottom line performance … identify the challenges you must overcome"); the structure Data entry → Performance breakdown → Impact Analysis → Scenario Diagnostic. Scott has confirmed this purpose.

**Reasonably follows.** It is a comparative economic argument made in arithmetic: the throughput chain is the premise, the income statement is where the comparison is settled, and the fixed scenarios are the cases compared. Its type is closer to an investment comparison than to a forecast, a staffing plan or a simulation.

It is not a forecast, not an evaluation of individual salespeople, and not a benchmark.

## 2. Core purpose

To show, in a form that can be audited cell by cell, how improving how opportunities are handled (close rate, cycle time, deal size) compares with adding selling resources (territories), measured at operating income. Scott's stated finding is that the quality levers consistently outperform the quantity levers on margin; the model is the arithmetic that shows it for the inputs entered. The Scenario Diagnostic then names what stands between a company and each quality improvement (source: three diagnosed scenarios; why "hire more" has no diagnostic section is not documented).

## 3. Decisions it informs

Primary: add selling resources, or improve how the current team sells. Subordinate: which quality lever to pursue first for the inputs entered; what an improvement is worth in operating income, and therefore what could be spent to achieve it (interpretation: the original reports the value, not a spending limit); which obstacles the chosen lever meets.

## 4. How it works

```
Data entry           figures a company has or estimates (historical and assumptive data, Orientation B5)
      ↓
Performance          opportunities per year   = opportunities manageable at once × (12 ÷ cycle months)   (row 21)
breakdown            transactions per year    = × close rate                                              (row 22)
                     revenue per territory    = × deal size                                               (row 23)
                     revenue                  = × territories                                             (row 25)
                     scenario columns E–H each change one input by the size in row 7 (default 10%);
                     J takes the changed close rate, cycle and deal size from F–H; K adds E's territories to J
      ↓
Impact Analysis      cost of revenue, R&D and G&A as % of revenue; salesperson costs (salary, travel, commission)
                     × territories; sales overhead and marketing fixed → operating income, % net gain, S&M ROI
      ↓
Scenario Diagnostic  five common obstacles for each of close rate, cycle time and deal size
```

**Mechanism (math).** Revenue is a product of the inputs, so a 10% change in close rate or deal size adds 10% to revenue, and a 10% shorter cycle adds 11.1% (1 ÷ 0.9). On the cost side, a quality improvement adds commission and the revenue-proportional costs; adding territories adds salary and travel per territory and, at a 12-month ramp, no first-year revenue for the new territories (E25). That asymmetry is what separates the levers at operating income.

## 5. Definitions, as the original states them

| Term | The original's description | Cell |
|---|---|---|
| Sales territories | "the number of open sales territories you had last year. This is not based on individual people, so if someone has left the company, but the territory is still open, count that as a sales territory." Scott: a territory is a design choice carrying an expected yield. | Data entry C9 |
| Opportunities manageable at one time | "the number of accounts any given sales person can effectively manage at the same time"; introduced through the share of non-selling time. Scott: capacity is cognitive bandwidth constrained by time, not labor hours. | C31 |
| Sales cycle | "from when a qualified opportunity enters the pipeline to when it closes as a sale … for simplicity … from first meeting to the date the agreement is received by accounting"; estimate if not tracked. | C33 |
| Ramp time | Time "to get a new sales person up to speed to where they are operating at maximum efficiency"; from a sales manager. | C35 |
| Close rate | "the percentage of all of the pipeline opportunities that your organization has worked that have resulted in an executed agreement." | C37 |
| Deal size | "the average deal size … you can get this figure by dividing your revenue by total number of contracts." | C11 |

The evolution uses tighter, testable definitions for some of these (for example close rate as won ÷ won + lost); those belong to Part B, not to the original.

## 6. Values held side by side in the original

| Element | Source | Intent |
|---|---|---|
| Engine salary $87,750 (Performance breakdown C11, F11:J11) beside the entry sheet's $116,850 (F15) | The calculations use $87,750; F15 is referenced by nothing in the calculations | **Confirmed (Scott):** a deliberate estimate placed to test whether a reader understands how the model works |
| Deal size $75,000 (F11) beside contracts and revenue (E12, E13) | C11 says deal size can be obtained as revenue ÷ contracts; with the sample, that gives $33,113 | **Confirmed (Scott):** $75,000 is a reference value from a different client, so the model works for many companies. Whether contracts and revenue are also meant as a comparison is open |
| Ramp credited in "hire more" (E25) and in "improve all" (K25) | E25 adds (12 − ramp) ÷ 12 of a year for new territories; K25 computes all territories at full value then subtracts the same credit | **Open.** Mechanics preserved exactly |
| Commission on new territories in "hire more" (E13, E26) | Cost per territory, including commission at baseline revenue per territory, × 110 territories | **Open.** Mechanics preserved exactly |
| Total sales overhead and marketing (F39) | `=F41+F48`; referenced by nothing | A calculated summary in the original. A reconciliation control would be a proposed enhancement |

The sample values are illustrative. They show and test the mechanics and are not a description of one company.

## 7. How it compares (interpretation)

Against sales capacity calculators, velocity simulators, quota planners and CRM forecasting as reviewed in October 2026, it is distinctive in (a) carrying a sales change to operating income rather than to revenue or headcount, (b) comparing quantity and quality levers in one frame with one arithmetic, and (c) being auditable cell by cell by someone who did not build it. Fixed scenarios and a one-period horizon follow from (c) and from the single decision it informs.

## 8. The blank modern workbook (`workbook/Sales_Capacity_Model.xlsx`)

**Verified:** with the original's inputs, it reproduces all 200 numeric formula cells of the original (`tools/rubric.py` G1–G4); labels and descriptions word for word; no typed constants in the calculations; a fully blank workbook shows no errors.

**Known implementation problems (not problems with the original):** with partial inputs, missing costs can drop out of operating income (a blank marketing section removes all sales and marketing expense); the E39 entry cell and its "value used" display a figure that drives nothing. Formula protection on export and incomplete-input handling are not yet verified. The workbook is not approved.

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
4a. **Incomplete inputs are not reported as complete** (not yet met). A result whose required inputs are missing shows that it is incomplete instead of a number; an entered zero is distinguished from a blank.
5. **Rule in words** beside every calculation row (C3).
6. **Terminology.** Salesperson / salespeople; not the s-word, not the abbreviation of "representative". Outside `source/`, archived documents and manifests quoting the original.
7. **Income statement in the loop.** Every scenario result is an operating income after all costs.
8. **No regression.** No automatic rubric criterion scores lower than at the last accepted version (`workbook/Sales_Capacity_Model.score.json`).
9. **Unit.** On the `evolution` branch, throughput is per salesperson; the as-is oracle is labeled as per territory.
10. **Register purity** (evolution). No scenario or intervention field in the register; register and modeller never share a key.
