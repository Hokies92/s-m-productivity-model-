# The Model: current statement

This is the current canonical interpretation of the Sales Capacity Model (2000; Sales and Marketing Efficiency Model, 2011 edition). The original workbook and its formula export are the evidence; this document is the interpretation built on them, and Scott reviews changes to it. Where another interpretation disagrees, this one governs; where the source or Scott's confirmed statements disagree with it, they govern and this document is corrected. Part A describes the model as it is; Part B describes where the rebuild is taking it; the closing section lists the requirements and how each is enforced. The evolution lives on the `evolution` branch.

© 2000–2026 Growth Enablement. All rights reserved. Author: Scott Santucci.

---

# Part A. The model as it is

Basis is marked where it matters to the conclusion: **source** (the original workbook or its formula export), **Scott** (confirmed intent), **math** (follows from the source), **interpretation** (a conclusion that reasonably follows but is not confirmed). Confirmed and open intent is tracked item by item in the project's intent ledger.

## 1. What it is

**Established.** A model for comparing commercial investment choices, chiefly adding selling resources versus improving the productivity of the resources a company already has, by carrying each choice through a pro forma income statement to operating income, and then naming the challenges to overcome for each. Source: Orientation B5 ("determine the impact of each of these investment decisions on your top line revenue and bottom line performance … identify the challenges you must overcome"); the structure Data entry → Performance breakdown → Impact Analysis → Scenario Diagnostic. Scott has confirmed this purpose.

**Reasonably follows.** It is a comparative economic argument made in arithmetic: the throughput chain is the premise, the income statement is where the comparison is settled, and the fixed scenarios are the cases compared. Its type is closer to an investment comparison than to a forecast, a staffing plan or a simulation.

It is not a forecast, not an evaluation of individual salespeople, and not a benchmark.

## 2. Core purpose

To compare, in a form that can be audited cell by cell, two kinds of commercial investment at operating income: improving how opportunities are handled (close rate, cycle time, deal size) and adding selling resources (territories). The economic argument the model was built to make (Scott) is that improving the productivity of existing selling capacity can return more operating income than proportionally expanding it, because revenue and cost respond differently to the two (§4); with the original's illustrative inputs, each quality lever does. For a particular company, the result follows from that company's entered assumptions, the timing and ramp treatment, and its cost structure: the model shows the comparison for those inputs rather than presuming its outcome. The Scenario Diagnostic then names what stands between a company and each quality improvement (source: three diagnosed scenarios; why "hire more" has no diagnostic section is not documented).

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

**Mechanism (math).** Revenue is a product of the inputs, so a 10% change in close rate or deal size adds 10% to revenue, and a 10% shorter cycle adds 11.1% (1 ÷ 0.9). Salesperson cost is one bundle per territory, salary + travel + commission (row 14), where commission is revenue per territory × the commission rate (row 13), and the bundle is multiplied by the number of territories (row 26).

- A quality improvement raises revenue per territory, so it adds commission on the new revenue and the revenue-proportional costs (cost of revenue, R&D, G&A); salary and travel do not change.
- Adding territories multiplies the whole bundle by the new count (E26 = E14 × E9). In "hire more", revenue per territory is the baseline's (E22 = C22), so each added territory carries salary, travel and commission at baseline revenue per territory, while revenue credits the added territories with (12 − ramp) ÷ 12 of a year (E25). At a 12-month ramp they add no first-year revenue. With the illustrative inputs, the added cost is $2,252,500, of which $900,000 is commission.

That asymmetry is what separates the levers at operating income. Why commission is charged on territories that are credited no revenue is not documented (§6); the formulas are preserved exactly.

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
| Engine salary $87,750 (Performance breakdown C11, F11, G11, H11, J11; E11 and K11 reference them) beside the entry sheet's $116,850 (F15) | The calculations use $87,750; F15 is referenced by nothing in the calculations | **Confirmed (Scott):** a deliberate estimate placed to test whether a reader understands how the model works |
| Deal size $75,000 (F11) beside contracts and revenue (E12, E13) | C11 says deal size can be obtained as revenue ÷ contracts; with the sample, that gives $33,113 | **Confirmed (Scott):** $75,000 is a reference value from a different client, so the model works for many companies. Whether contracts and revenue are also meant as a comparison is open |
| Ramp credited in "hire more" (E25) and in "improve all" (K25) | E25 adds (12 − ramp) ÷ 12 of a year for new territories; K25 computes all territories at full value then subtracts the same credit | **Open.** Mechanics preserved exactly |
| Commission on new territories in "hire more" (E13, E26) | Cost per territory, including commission at baseline revenue per territory, × 110 territories | **Open.** Mechanics preserved exactly |
| Total sales overhead and marketing (F39) | `=F41+F48`; referenced by nothing | A calculated summary in the original. A reconciliation control would be a proposed enhancement |

The sample values are illustrative. They show and test the mechanics and are not a description of one company.

## 7. What it demonstrably does, and how it compares

**Demonstrated by the source.** It carries every scenario through an income statement to operating income; it compares quantity and quality levers with one arithmetic in one frame; every result traces, cell by cell, to formulas and the values they use (entered inputs, and values typed into the calculations such as the $87,750 salary). The four individual-lever scenarios (E–H) each change one input, isolating that lever's effect; the two combined scenarios (J, K) combine those changed inputs, so each traces back to the individual columns it draws from. Fixed scenarios built this way and a one-period horizon keep the comparison focused and traceable. They support that purpose; they are not required by it, and a model with more scenarios or periods could also be auditable.

**Comparative claims (not established here).** Whether other sales capacity tools, velocity calculators, quota planners or forecasting products do the same is a claim about those products and needs evidence about them. The project's October 2026 market notes (archived) are a starting point for that comparison, not a verification of it.

## 8. The blank modern workbook (`workbook/Sales_Capacity_Model.xlsx`)

**Verified:** with the original's inputs, it reproduces all 200 numeric formula cells of the original (`tools/rubric.py` G1–G4); labels and descriptions word for word; no typed constants in the calculations; a fully blank workbook shows no errors.

**Known implementation problems (not problems with the original):** with partial inputs, missing costs can drop out of operating income (a blank marketing section removes all sales and marketing expense); the E39 entry cell and its "value used" display a figure that drives nothing. These are separate implementation work; the original arithmetic is not changed to solve them. The workbook is not approved.

**Three different properties, not to be confused:**
- **Input completeness:** every input that a result's calculation requires is present, and each carries its status: an actual zero, unknown (blank), a confirmed actual, an estimate or assumption, or an illustrative default. A result whose required costs are unknown must not be presented as a complete operating income. Completeness is defined relative to the inputs and calculations the model specifies.
- **Computational correctness:** the calculations reproduce the original's formulas (parity).
- **Economic validity:** whether the model's specified categories capture every cost and constraint that matters for a particular company. A fully populated, correctly computed workbook does not establish this; it is a judgment about the company, outside what the workbook can verify.

---

# Part B. Where the rebuild is taking it (branch `evolution`)

## 9. The direction

Make the company's assumptions, their sources, and their relationship to the company's actual results explicit and testable, while preserving the original. Preserving the original means its calculations are kept and its results are reproduced as a defined special case of the evolved architecture: given the original's inputs and scenario sizes, the evolved model returns the original's results exactly, including both of its ramp treatments. The evolution may add structures and relationships around it; it does not change the preserved original. The original contains material for this (historical inputs, assumptions, and calculated values that can be compared) but does not implement such checks; of its paired values, two have confirmed intent and the others are open (§6), so the evolution does not assume they were designed as validation tests. The entry sheet becomes a **register** of state assumptions (each with a basis: validated by Finance, the client's entry, the model's estimate, or a labeled default), and cross-checks compare what the assumptions imply with what the company reports. Scenarios and the equations applied to the register live in a separate **modeller**. Territory and salesperson become separate counts linked by assignment, so open territories and ramp carry their cost. The income statement stays the constraint every scenario passes through.

## 10. Three kinds of assumption, and where each lives

| Kind | What | Lives in | Tested by |
|---|---|---|---|
| State | A belief about the system as it is | The register | The company's actuals, via cross-checks |
| Method | An equation or rule applied to the register | Beside each formula, in words; the modeller | Parity with the original; the true-up |
| Intervention | A hypothesis: "close rate +10%" | The modeller's scenario table only | Next period's register |

The separation is semantic. The register holds beliefs and observations describing the system as it is. The modeller applies mathematical methods to them and evaluates proposed interventions. The modeller reads and references register values; an intervention never overwrites or alters the baseline, and every scenario result identifies the register version it was computed from. If interventions entered the register, the baseline would validate against its own proposals. How the separation is implemented (tables, keys, versions) is a design choice that must serve this requirement, not replace it.

## 11. Deferred, and why

Territory and hiring scenarios need the territory–salesperson assignment explicit and break the simple inverse (target operating income → required lever). The original's "hire more" column is the quantity lever shown beside the quality levers; it is in the as-is workbook and returns to the evolution with them. The Scenario Diagnostic returns keyed to scenario ids.

---

# Requirements and how each is enforced

Status: **tested** (an automated test fails if it breaks; CI runs the tests on every push to `main` and has passed), **measured** (scored by the rubric but not verified in Excel), **convention** (kept by working rules, not by a test), **proposed** (not yet met or not yet tested).

## A. The original model, its established reproduction, and project-wide rules

| Requirement | Status |
|---|---|
| The original workbook and its formula export are never modified | Convention (CONTRIBUTING; no checksum test) |
| The Python reproduction, with default options, reproduces all 48 original outputs | Tested (`tests/test_model.py`) |
| Every scenario is carried to operating income after the model's cost categories | Property of the original's structure (Impact Analysis); not a separate test |
| Terminology: salesperson / salespeople, outside quoted original text | Tested (`tests/test_terminology.py`) |

## B. Acceptance criteria for the modern as-is workbook (not yet approved)

| Requirement | Status |
|---|---|
| With the original's inputs, reproduces every original numeric formula cell (200 of 200) | Tested (rubric G1, G2, G4 via `tests/test_asis_workbook.py`) |
| No typed constants in the calculations | Tested (rubric G3) |
| Fully blank: no error values | Tested (rubric B4) |
| A rule in words beside every calculation row | Tested through the no-regression check (rubric C3) |
| No automatic rubric criterion scores lower than the submitted candidate's score (`workbook/Sales_Capacity_Model.score.json`; no version has been accepted yet) | Tested |
| Input completeness as defined in §8: unknown required costs never produce a complete-looking operating income; actual zero, unknown, confirmed actual, estimate and illustrative default are distinguished | Proposed; not met |
| A displayed "value used" drives the calculation it appears to drive (E39) | Proposed; not met |
| Formulas locked, inputs unlocked, protection without password | Measured in the file (rubric B1); not verified in Excel |
| Layout, traceability and usability criteria scored by a reviewer (rubric A1, A3, A4, B5, B7, D3) | Proposed; not yet scored |

## C. Architecture of the evolution (branch `evolution`)

| Requirement | Status |
|---|---|
| Throughput per salesperson, with territory and salesperson as separate quantities | Implemented on `evolution`; tested there by `tests/test_workbook.py` (run locally; CI is not configured on that branch) |
| Three kinds of assumption kept separate: state in the register, method beside formulas, intervention in the modeller (§10) | Implemented on `evolution`; the register's exclusion of scenario fields is tested there |
| Interventions never overwrite the baseline; the modeller may reference register values; every result identifies its register version (§10) | Proposed as stated. The current `evolution` schema enforces a stricter rule (no keys shared between register and modeller), tested in `tests/test_schema.py`; to be revisited against this requirement |
