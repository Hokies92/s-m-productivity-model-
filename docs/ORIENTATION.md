# Orientation (rewritten)

Status: proposed text for the first tab of the rebuilt workbook and the start page of the web application, 2026-10-24. The as-is orientation text is preserved verbatim in `source/workbook_cells.csv` (sheet "Orientation") and quoted in [AS_IS_INDEX.md](AS_IS_INDEX.md).

## What changes from the as-is orientation, and why

| As-is orientation | Rewritten | Why |
|---|---|---|
| Opens with four business scenarios to improve performance | Opens with what the model is: a description of your commercial system, tested against your results | Scenarios come after a tested baseline |
| "Enter historical data and metrics assumptions" | Every entry is a written, falsifiable assumption with a declared basis | The data tab is an assumption ledger |
| Example: "a 10% decrease in your sales force … could increase operating margin by almost 800%" | No claimed outcomes in the orientation | The orientation should not argue a conclusion before the data is tested |
| Territories and headcount implicit | Territory design and hiring stated as two separate decisions | The core design point of the model |
| Four sections listed by worksheet | Four steps listed by what the user does | Written for the people who will collect the data |
| Recommends running per channel and product line | Kept, as scope | Still right |

---

## Commercial Effectiveness Model

### What this model does

This model describes how your commercial system works, tests that description against your actual financial results, and then lets you explore what would happen if you changed it.

It is built on one discipline: **lead with your assumptions.** Every number you enter is a claim about your business. The model asks you to write each claim down, say where it comes from, and say what would prove it wrong. Then it checks. If anyone later disagrees with a result, you can go straight back to the assumption behind it.

### How the model sees sales capacity

Two decisions create sales capacity, and they are separate:

- **Territories are a design choice.** You decide how to divide your market, how many territories to fund, and what you expect each to yield. A territory without a salesperson still carries that expectation, so leaving it open has a cost.
- **Salespeople are a hiring choice.** A salesperson's capacity is not the hours they work. It is how many opportunities they can hold and advance well at the same time, turned over by the length of your sales cycle.

Revenue happens where the two meet: salespeople assigned to territories, converting opportunities at your win rate and deal size, with every cost flowing through to operating income.

### How to use it

1. **State your assumptions (Data entry).** Work through the steps in order. Each step names who usually owns the data (Finance, Sales Operations, HR, Compensation), so you can forward it to them. For every value, record its basis:
   - **Validated actual:** confirmed by your Finance team from your records.
   - **Calculated estimate:** produced by one of the model's estimators from your data.
   - **Reference value:** borrowed from another context; say which.
   - **Judgment:** your best estimate; give a reason and a low–high range.
2. **Test and calibrate.** The model combines your assumptions into what they imply (contracts, revenue, pipeline, compensation expense) and compares that with your actual results. Every gap goes to a reconciliation list. For each one, revise an assumption, explain the gap, or accept it as a known gap. When the list is resolved, Finance signs off the baseline.
3. **Explore what-if scenarios.** Change assumptions one at a time or in combination: territory design, hiring and fill speed, salesperson capacity, win rate, cycle, deal size, costs. Every change flows through to operating income, with nothing unexplained.
4. **Understand what stands in the way.** For each improvement, review the common obstacles and the conditions that would make it achievable.

### How to read the results

- Until Finance signs off, every result is labeled **Working model: not validated by Finance.**
- Every result shows how much of it rests on validated actuals and how much on estimates, reference values and judgment.
- Results are only as real as the assumptions behind them. To challenge a result, challenge an assumption in the ledger.
- Assumptions are revisited each period. The model keeps a record of assumed versus observed, so your assumptions become more accurate over time.

### What this model is not

- **Not a forecast.** It describes what your system can and does produce under stated assumptions.
- **Not an evaluation of individual salespeople.** Salespeople are measured as a system, under anonymous IDs, to find improvements in how the system works.
- **Not a benchmark ranking.** Reference values from other contexts can inform assumptions, but your baseline is built from your own reality.

### A few points

This is a general model. For a sharper analysis, run it separately for each sales channel and product line, and separate new-customer revenue from revenue from existing customers. The model can be tailored to your business.

© 2000–2026 Growth Enablement. All rights reserved.
