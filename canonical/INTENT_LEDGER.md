# Sales Capacity Model: intent ledger

Status: current, 2026-10-26. What is confirmed about the original model's design intent, what is established by the source, and what is open. Companion to `canonical/FOUNDATION.md`; maintained alongside the formula export (`source/workbook_cells.csv`; in Project Knowledge, `source/original_workbook_formula_export.csv`). Cell references are to the original workbook. Open items stay open until Scott confirms them; their mechanics are preserved exactly in every implementation of the original.

© 2000–2026 Growth Enablement. All rights reserved.

## Basis

- **Source**: what the original workbook or its formula export demonstrably contains.
- **Scott**: what Scott Santucci has confirmed about intent (date in brackets).
- **Math**: what follows mathematically from the source.
- **Open**: an interpretation not yet confirmed.

## Confirmed or established

| Topic | What is known | Basis |
|---|---|---|
| Purpose | The model compares commercial investment choices, chiefly adding selling resources versus improving the productivity of existing ones, by carrying each through a pro forma income statement to operating income, and then names the challenges to overcome for each. | Source (Orientation B5; Performance breakdown → Impact Analysis → Scenario Diagnostic) and Scott |
| Redundant constraints | The model is axiomatic: it has redundant constraints built in to make sure the data is true. Its checks are self-evident from its structure, not added validation rules. | Scott (2026-10-26) |
| Client data versus the model | Inaccurate or loosely defined client data (for example headcount given instead of territories) is a property of the client's data, not a defect of the model. | Scott (2026-10-26) |
| Capacity | Sales capacity is cognitive bandwidth constrained by time, not labor hours: opportunities a salesperson can manage at once × (12 ÷ cycle months). | Source (Performance breakdown row 21) and Scott |
| Leads | "Increase leads" is deliberately not a scenario; leads are handled in separate drill-down spreadsheets. | Source (Orientation B8) |
| Entries | Each cell on the data entry tab is an entry that other tabs reference; an entry can be filled in different ways, and some are calculated. | Scott (2026-10-24) |
| Engine salary $87,750 (Performance breakdown C11, F11:J11) | A deliberate estimate typed into the calculations, placed to test whether a reader understands how the model works. The data entry tab separately computes $116,850 (F15). | Scott (2026-10-24) |
| Deal size $75,000 (Data entry F11) | A reference value from a different client, chosen so the model works for many companies. Revenue ÷ contracts on the same tab gives $33,113. | Scott (2026-10-24) |
| Territory | A territory is a design choice carrying an expected yield, not a unit of demand; it is separate from hiring. Open territories carry an expected yield and an opportunity cost. | Scott (2026-10-24) |
| Salespeople | Measured as agents in a system, to find system interventions, never to inspect individuals. | Scott (2026-10-24) |
| Sample data | Illustrative, used to show and test the mechanics; at least one value ($75,000) comes from a different client. Whether every sample value comes from a different source is not confirmed. | Scott |
| Mathematical bounds | A close rate cannot exceed 100% and a cycle must be longer than zero; a scenario that breaks a bound has no meaning. | Math |

## Open: mechanics preserved exactly, intent unconfirmed

| # | Element | What the source does | What follows mathematically | Status |
|---|---|---|---|---|
| Q1 | Contracts and revenue (Data entry E12, E13) as constraints | Entered beneath deal size (F11), labeled "Number of contracts last year" and "Revenue from those contract"; no formula references them. C11: "you can get this figure by dividing your revenue by total number of contracts." | Three identities: deal size = revenue ÷ contracts ($75,000 vs $33,113); baseline transactions = contracts (C22 × C9 = 1,500 vs 755); baseline revenue = revenue (C25 = $112.5M vs $25.0M). Two are independent. | Redundant constraints are confirmed in general (above). That these three identities are the intended check, so the baseline rebuilt from the mechanics must reproduce last year's contracts and revenue, is the reading that follows; Scott has not confirmed it specifically. |
| Q2 | Ramp time, 12 months (Data entry F35) | Entered value used by the hiring and improve-all scenarios. | At 12 months, added territories earn (12 − 12) ÷ 12 = 0 of a year in "Hire more"; above 12 months the credit turns negative. | Open. Hypotheses: a real planning assumption; a value placed to test the reader; something else. |
| Q3 | Two ramp treatments (Performance breakdown E25, K25) | E25 credits added territories with (12 − ramp) ÷ 12 of a year. K25 computes revenue on all territories, then subtracts the same ramp credit. | At 12 months, E25 adds no revenue for new territories; K25 adds a full year for them. | Open. Hypotheses: two intended views (first year vs steady state); a value placed to test; a construction artifact; something else. |
| Q4 | Commission on new territories in "Hire more" (E13, E26) | Commission per territory = revenue per territory × rate, using baseline revenue per territory; salesperson costs = cost per territory × 110. | Commission is charged on 110 territories ($9.9M) while revenue is credited for 100 ($112.5M); $0.90M of the $2.25M year-one change. | Open. Hypotheses: a funded territory budgeted at expected yield; a guaranteed draw during ramp; a by-product of scaling one cost bundle by the territory count; something else. |
| Q5 | Total sales overhead and marketing (Data entry F39) | `=F41+F48`; referenced by no other cell. | A calculated summary total. | A calculated summary in the original. Adding a Finance total to compare it with would be an extension, proposed only with Scott's authorization. |
| Q6 | Impact Analysis I9 | `=I8-'2) Performance breakdown'!$C$25` in the spacer column; no label; nothing references it. | Has no effect on any result. | Open. Hypotheses: a fill artifact; something else. |

## Modern implementation (not the original)

| Item | Status |
|---|---|
| Missing inputs | In `main` (merged by Scott 2026-10-27, PR #4): a missing input shows Incomplete through operating income, unrelated lines stay calculated, an entered zero is a value; 200/200 parity and 48/48 oracle outputs preserved. Verified in LibreOffice; not yet in Excel. Gate 1 not accepted. |
| E39 entry cell and "Value used" for F39 | Removed (in `main`); F39 is the calculated total. |
| Constraints shown (FOUNDATION §7, 1.2) | In `main` (PR #3): Performance breakdown rows 30–35 show deal size, transactions, revenue and salary beside the company's figures with the difference; they change no result. Open: travel, sales overhead and marketing still use a direct entry over its components without showing both. |
| Mathematical bounds (1.4) | In `main` (PR #3): close rate above 100% or cycle of zero or less shows Invalid through operating income. |
| Scenario comparison (1.8) | In `main` (PR #4): sheet Compare (drivers per scenario, operating income bridge that balances, saved run by paste-values); Impact Analysis row 24. A one-click save needs a macro companion (not built). |
| Independent ChatGPT candidate (reviewed 2026-10-26) | 200/200 parity; withholds whole sheets when any input is missing or invalid; checks mathematical bounds; worksheet protection off and inputs locked. Not approved. |
