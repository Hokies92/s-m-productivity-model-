# Sales Capacity Model: canonical foundation

Status: proposed canonical statement, 2026-10-26. On acceptance it replaces `docs/MODEL.md` as the single statement of what the model is and what Gate 1 must deliver; MODEL.md moves to `docs/archive/` with a status line. The original workbook and its formula export (`source/`) are the evidence; Scott's confirmed statements come next; this document is the interpretation built on both. The intent ledger (`canonical/INTENT_LEDGER.md`) tracks confirmed and open intent item by item.

© 2000–2026 Growth Enablement. All rights reserved. Author: Scott Santucci.

Basis marks: **source** (the workbook shows it), **Scott** (confirmed intent), **math** (follows from the source), **open** (not confirmed).

---

## 1. What the model is

A model for comparing commercial investment choices, chiefly **adding selling resources** versus **improving the productivity of the resources a company already has**. Each choice is carried through a pro forma income statement to operating income, and the obstacles to each improvement are named (source: Orientation B5; the sheet sequence; Scott).

It is an axiomatic model: a small set of definitions and identities, built so that the data it is given can be checked against itself (Scott, 2026-10-26: "there are redundant constraints built in to make sure data is true").

It is not a forecast, not an evaluation of individual salespeople and not a benchmark. Salespeople are measured as agents in a system, to find system interventions (Scott).

## 2. The system

```
1) Data entry           what the company knows or estimates about last year
        ↓
2) Performance          opportunities per year per territory = opportunities manageable at once × (12 ÷ cycle months)   row 21
   breakdown            transactions per territory           = × close rate                                             row 22
                        revenue per territory                = × deal size                                              row 23
                        revenue                              = × territories                                            row 25
                        cost per territory                   = salary + travel + commission (revenue per territory × rate)  rows 11–14
                        salesperson costs                    = cost per territory × territories                         row 26
        ↓
3) Impact Analysis      cost of revenue, R&D, G&A = % of revenue; sales overhead and marketing fixed;
                        operating income, % net gain, sales and marketing ROI                                          rows 8–27
        ↓
4) Scenario Diagnostic  the obstacles that stand between a company and each quality improvement
```

- **Capacity** is cognitive bandwidth constrained by time, not labor hours (Scott; source row 21).
- **A territory** is a design choice carrying an expected yield, not a unit of demand or a person (Scott; source Data entry C9).
- **Leads** are deliberately not a scenario; they are handled in separate drill-downs (source: Orientation B8).
- **Mechanism (math).** Revenue is a product of its drivers, so +10% close rate or deal size gives +10% revenue and −10% cycle gives +11.1%. A quality improvement raises revenue per territory; salary and travel do not move; commission and the revenue-proportional costs do. Adding territories multiplies the whole cost bundle. That asymmetry, settled at operating income, is the comparison the model exists to make.

## 3. The redundant constraints (the model's self-check)

The data entry sheet asks for some quantities twice: once as an input to the mechanics, once as a fact the company already knows. The second is a constraint the first must satisfy.

| Constraint | Model side | Fact side | Sample (illustrative) | Basis |
|---|---|---|---|---|
| Deal size | Entered deal size (Data entry F11) | Revenue ÷ contracts (E13 ÷ E12); C11: "you can get this figure by dividing your revenue by total number of contracts" | $75,000 vs $33,113 | source |
| Transactions | Transactions per territory × territories (Performance breakdown C22 × C9) | Contracts in the period, same channel (E12) | 1,500 vs 755 | math |
| Revenue | Baseline revenue (C25) | Revenue in the period, same channel (E13) | $112.5M vs $25.0M | math |
| Salesperson cost | Salary used by the calculations (C11, typed $87,750) | Base × (1 + load) (F15) | $87,750 vs $116,850 | source; the $87,750 is a deliberate test value (Scott) |
| Sales and marketing total | Overhead + marketing (F39 = F41 + F48) | — (a calculated summary; the original holds no Finance total to compare) | $14.5M | source |

**What the constraints do (math).** If deal size equals revenue ÷ contracts and transactions equal contracts, revenue equals revenue: the first three rows hold two independent constraints. When the baseline does not reproduce last year's contracts, the throughput assumptions are what to question (territories, opportunities manageable, cycle, close rate). When it reproduces contracts but not revenue, the deal size is what to question. The model points to the assumption to question; it adds no outside rule.

**In the sample nothing agrees**, consistent with values placed to see whether the reader understands the whole (Scott, for $87,750 and $75,000).

**Confirmed (Scott, 2026-10-27).** The baseline rebuilt from the mechanics must reproduce the company's actual contracts and revenue **for whatever period is provided**: one year, or three years if three years of data are supplied. The original's wording ("last year") is one case of this. **The company figures must cover the same scope as the inputs:** when one sales channel is analyzed, contracts and revenue come only from that channel's territories, and contracts from other channels are excluded.

**Consequences (math and implementation).** The mechanics produce annual figures (12 ÷ cycle months), so a multi-year period is compared after putting both sides on the same period (company figures ÷ years, or model figures × years); deal size (revenue ÷ contracts) needs no adjustment. The modern workbook's checks currently assume a one-year period and do not yet record the period or the channel; adding both is Gate 1 component C3. Scope rules for channels, territories and shared costs (nesting and cross-checks in data entry) are expected to grow; how companies define territories and deploy resources is itself a finding the model will surface (Scott, 2026-10-27).

## 4. Scenarios

Six columns, each carried to operating income: **C** baseline; **E** hire more salespeople (territories +size); **F** close rate +size; **G** cycle −size; **H** deal size +size; **J** close rate, cycle and deal size combined; **K** all four. The default size is 10% (Performance breakdown E7:H7).

- E–H each change one input, isolating one lever. J and K combine the changed inputs and trace back to the single-lever columns (source).
- **Two ramp treatments (open).** E25 credits added territories with (12 − ramp) ÷ 12 of a year; K25 computes all territories at full value, then subtracts the same credit. At a 12-month ramp, E adds no first-year revenue for new territories and K adds a full year.
- **Commission on new territories (open).** In E, each added territory carries salary, travel and commission at baseline revenue per territory, while ramp credits it with (12 − ramp) ÷ 12 of a year's revenue.
- **Mathematical bounds (math).** An improved close rate cannot exceed 100%; a reduced cycle must stay above zero. A scenario that breaks a bound has no meaning and must be shown as such, not computed silently.

## 5. Income statement and metrics

Revenue; increase in revenue from base; increase in sales costs; total sales costs (sales overhead + salesperson costs); marketing; cost of revenue, R&D and G&A as fixed shares of revenue (original sample 13.22%, 10.19%, 15.4%); total operating expenses; **operating income**; % net gain = (increase in revenue − increase in sales costs) ÷ baseline revenue; sales and marketing ROI = (revenue − sales and marketing costs) ÷ sales and marketing costs (source: Impact Analysis rows 8–27, 30–32).

## 6. Definitions, as the original states them

| Term | The original's words (Data entry, column C) |
|---|---|
| Sales territories | "the number of open sales territories you had last year. This is not based on individual people, so if someone has left the company, but the territory is still open, count that as a sales territory." (C9) |
| Opportunities manageable | "the number of accounts any given sales person can effectively manage at the same time" (C31) |
| Sales cycle | "from when a qualified opportunity enters the pipeline to when it closes as a sale … for simplicity … from first meeting to the date the agreement is received by accounting" (C33) |
| Ramp time | time "to get a new sales person up to speed to where they are operating at maximum efficiency" (C35) |
| Close rate | "the percentage of all of the pipeline opportunities that your organization has worked that have resulted in an executed agreement" (C37) |
| Deal size | "the average deal size … you can get this figure by dividing your revenue by total number of contracts" (C11) |

## 7. Gate 1: modern replication

**Purpose.** Repeat the purpose and functionality of the current model, exactly, with 20 years of spreadsheet technical debt removed. Gate 1 adds no new economics. It is accepted by Scott after he tests it with his own data; nothing from the evolution starts before then.

**Architecture.** One model, two implementations, one contract:

```
inputs (schema: inputs.schema.json)
   ├─► Excel workbook  (generated by code; the analyst's working model)
   └─► Python engine   (the oracle; serves exports and the web)
outputs (schema: outputs.schema.json; stable ids for every result)
```

The workbook and the Python engine must return identical outputs for every test case. The web and the export read and write only the two schemas; neither ever contains the workbook's formulas.

| # | Requirement | Accepted when |
|---|---|---|
| 1.1 | **Fidelity.** Same arithmetic, scenarios, ramp treatments, labels and original text | 200/200 original numeric formula results and 48/48 oracle outputs, with the original inputs, on every build; source checksums unchanged |
| 1.2 | **Constraints shown, never resolved silently.** Each pair in §3 displayed side by side with its difference and which assumption it points to; the calculations use what the original uses, so parity holds | Test: every §3 pair present with both sides and the difference; no cell that picks one side without showing the other |
| 1.3 | **Completeness.** A missing input is never zero; whatever depends on it shows Incomplete through operating income; unrelated lines stay calculated; an entered zero is a value | Behavior tests after recalculation (removal, partial, zero cases) |
| 1.4 | **Bounds.** Scenarios that break §4's bounds show Invalid | Behavior tests |
| 1.5 | **Modern Excel.** Named inputs, structured tables, data validation, conditional formatting, grouping, protection with unlocked inputs; functions chosen for readability only if the test engine can recalculate them | No output changes (1.1 re-run); protection and unlocked inputs verified after recalculation |
| 1.6 | **Look and feel.** One design system; a client view and a logic view per stage; the rule in words beside every calculation; prints and exports to PDF cleanly | Reviewer score (Scott) on layout, traceability, usability |
| 1.7 | **Illumination.** Show how any result is calculated (rule in words, precedents, a trace from result to inputs) | Ten sampled results trace to inputs; core workbook works with macros off; any macro or script lives in an optional companion and is not needed for any result |
| 1.8 | **Scenario work.** Sizes editable per lever; named scenario sets saved and compared side by side; a size sweep per lever; defaults reproduce the six original columns exactly; a scenario never alters the baseline inputs | Tests: defaults equal the original; baseline unchanged by any scenario |
| 1.9 | **Export.** Every input and output exported with stable ids, units, model version and input-set id, as CSV and JSON, for any visualization tool | Schema validation; round trip (export → import → same outputs) |
| 1.10 | **Web.** A data entry page that produces a valid input set; output pages that show selected results only, computed by the Python engine; the model itself is never exposed | Input page output validates against the schema; output pages show only declared outputs; engine–workbook agreement test passes for the input sets used |
| 1.11 | **Python.** The oracle, the workbook builder, the tests, exports and web adapters; Python inside Excel only where it adds something formulas cannot | All tests pass in CI |

**Platform facts to verify before relying on them.** VBA does not run in Excel for the web. Office Scripts and Python in Excel depend on the Microsoft 365 plan. The test engine is LibreOffice; a function it cannot recalculate needs another verification route or is not used.

## 8. Confirmed and open

Confirmed (Scott): the purpose (§1); the baseline must reproduce the company's actual contracts and revenue for the period provided, within the same channel (§3, 2026-10-27); capacity as cognitive bandwidth; territory as a design choice; salespeople measured as agents; leads not a scenario; $87,750 a deliberate test value; $75,000 a reference value from a different client; sample data illustrative; redundant constraints exist to make sure data is true.

Open, mechanics preserved exactly: the two ramp treatments; commission on new territories in "hire more"; whether to add a Finance total to compare with F39 (an extension, not in the original); Impact Analysis I9 (a stray formula that affects nothing).

## 9. After Gate 1 (the evolution, not built yet)

Recorded so it is not lost, not as features of the original: a register of state assumptions with their basis (Finance-validated, client entry, estimate, default); a separate modeller for method and intervention assumptions, so interventions never enter the baseline; territory and salesperson as separate counts linked by assignment, so open territories and ramp carry their cost; a two-stage data intake (fast input by the client, then an auditable final data set). The income statement stays the constraint every scenario passes through.
