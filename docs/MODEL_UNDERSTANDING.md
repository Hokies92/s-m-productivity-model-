# Model Understanding (current)

Status: **current understanding, 2026-10-24.** This is the to-be view. The as-is model (the original workbook, its audit, spec v2.1 and package 2.1.0) is unchanged and preserved; see [AS_IS_INDEX.md](AS_IS_INDEX.md) and the `as-is-2026-10-24` branch.

© 2000–2026 Growth Enablement. All rights reserved.

## 1. What the model is

**A falsifiable system model of a company's commercial engine.** It states how a company believes its sales system works, tests those beliefs against the company's own financial reality, and then lets leadership explore what-if changes from a baseline that describes what is actually happening.

The method, in one line:

> State assumptions → compute what they imply → compare with what is observed → the gap shows which assumptions are wrong → revise and record → run what-ifs from a baseline that describes reality.

The arithmetic is simple on purpose. Its job is to make assumptions testable, not to be clever. What is hard, and uncommon, is structuring and calculating it so the whole system and each of its parts stay accurate at the same time.

## 2. The parts, reinterpreted

| Workbook part | Earlier reading | Current understanding |
|---|---|---|
| Data entry | Inputs | **The theory of the present**: the company's beliefs about itself, each written down and falsifiable. An assumption ledger. |
| Performance breakdown | Calculation engine | **The theory of structure**: how the beliefs combine. These relationships are assumptions too. |
| Impact analysis | Financial output | **The test instrument.** Assumptions are forced into a predicted income statement; Finance holds the real one. The true-up is where theory meets reality. |
| Scenario diagnostic | Obstacle list | **Causal hypotheses** about why a lever is stuck, also testable |
| What-if scenarios | The main event | **Deliberate changes to assumptions that survived testing.** A scenario is only as credible as the baseline it changes. |

The right question about the model is not "is the math right?" but "is every assumption, including the structural ones, explicit and testable?" The model is valuable because it can be shown to be wrong.

## 3. Two decisions, linked by assignment

Sales capacity comes from two related but independent decisions:

1. **Territory design is a choice.** The company decides how to divide its market, how many territories to fund, and what yield it expects from each. A territory is not demand. It is a claim of expected yield. An open territory still carries that expectation, so its shortfall is a cost.
2. **Staffing is a choice.** The company hires salespeople. A salesperson's capacity is not hours worked; it is how many opportunities they can hold and advance well at once, turned over by cycle time.

Revenue happens only where the two meet, through the **assignment** of salespeople to territories.

| Territory state | Expected yield | Actual yield | Cost |
|---|---|---|---|
| Filled, fully ramped | Full | Depends on the salesperson as an agent | Full salesperson cost |
| Filled, ramping | Full | Partial | Full salesperson cost |
| Open | Full | Zero, or partial if covered | Salary saved, contribution lost |
| Shared or covered | Full | Partial; the covering salesperson's own territory suffers | Split |

Variables of territory design (quality, number vs market segmentation, coverage model, support model, skills and development strategy) matter, but the model does not need to understand them all. It needs **each territory identified as its own record**, with its status and expected yield.

### The cost of an open territory

Under the as-is workbook's own assumptions (illustrative): expected yield $1.125M per territory per year, $93,750 per month.

| Item | Per month |
|---|---|
| Contribution lost (yield − 38.81% revenue-linked costs − 8% commission) | $49,866 |
| Salesperson cost saved (salary $87,750 + travel $47,500, ÷ 12) | −$11,271 |
| **Net cost of one open territory** | **$38,595** |

The loss continues after the hire because of ramp. Six months open plus the workbook's 12-month zero-yield ramp costs about $830K per vacancy; with a linear ramp, about $530K. Every month spent in HR and Finance approvals has a price. Internal process latency turning into lost contribution is a hidden commercial cost in its purest form.

## 4. Capacity and Little's Law

Little's Law (items in a stable system = arrival rate × time in the system) applies to the **salesperson as an agent**:

```
Opportunities resolved per year (capacity) = opportunities held at once ÷ cycle (years)
```

The territory contributes the **expected yield** (the design claim) and the **record of what actually flowed through it** (observed pipeline, resolved opportunities, revenue). Market demand is a third thing the model does not need to model yet.

**What the as-is formula assumes without saying so:** revenue = territories × one salesperson's capacity × win rate × deal size. That holds only if every territory has exactly one full-time, fully ramped salesperson working at full capacity. The redesign treats each of those as an assumption to declare and test.

**Overload, through Little's Law:** if a salesperson holds more opportunities than they can advance well, open opportunities rise at the same throughput, so time per opportunity rises. Extra load becomes longer cycles and lower win rates, not more deals.

**Each lever has a territory part and a salesperson part:**

| Lever | Territory part | Salesperson part |
|---|---|---|
| Cycle | The buyers' decision process in that segment | How well the salesperson helps buyers decide |
| Win rate | Fit and competition in the segment | Quality of engagement |
| Deal size | Account size and potential | Value and scope the salesperson builds |

## 5. Assumptions and how they are tested

**Two kinds of assumption:**

1. **Parameter assumptions:** values about this company (win rate is 25%; salespeople can hold 30 opportunities).
2. **Structural assumptions:** relationships the model asserts (throughput = held ÷ cycle; non-sales costs scale with revenue). They can be wrong for a given client, so they live in the same ledger at model level.

**Test types:**

| Test | Logic | Example |
|---|---|---|
| Direct observation | Compare with a measured value | Stated win rate vs CRM won ÷ (won + lost) |
| Joint implication | Several assumptions together predict something observable | Territories × capacity × 12 ÷ cycle × win rate × deal size vs actual revenue |
| Triangulation | Same quantity, two independent derivations | Deal size from revenue ÷ contracts vs CRM average |
| Bounds | Some outcomes are impossible | Utilization ≤ 100%; filled seats ≤ territories |
| Dispersion | An average misleads if the spread is wide | Win rate by territory or salesperson group |
| Prediction | Last period's assumptions predict this period | Assumed vs observed every period: the running accuracy record |

A failed joint test shows that **at least one** assumption in the set is false, not which one. Locating it is the client's work: confronting ambiguity with targeted evidence. The module therefore presents the candidate set, not a verdict.

**Scope matters.** The same value can be valid in one scope and contradicted in another. The as-is workbook's $75,000 deal size is a deliberate **reference value from another client**, chosen so the model works for companies of any size. As a reference for a general model it is sound; as a claim about a specific client whose actuals imply $33,113, it is contradicted. Every assumption declares its scope.

**Worked on the as-is sample data.** The data tab's assumptions jointly imply 1,500 contracts and $112.5M; the actuals are 755 contracts and $25.0M. Targeted evidence locates the gap:

- If cycle and win rate hold, Little's Law says salespeople hold about 15 opportunities, not 30: 50% utilization. That explains 1,500 → 755 contracts.
- The $75,000 reference value, applied to this client, is contradicted by $25M ÷ 755 = $33,113. That explains the rest of the revenue gap.
- Residual: $0, provided cycle and win rate are confirmed.

The result is a sharper question: is idle capacity a territory design problem or a salesperson problem?

## 6. Whole system and its parts: Meadows' leverage points

The model aims to be a synthetic, whole-system calculator that is also accurate when reduced to its parts. To support scenarios at as many of Donella Meadows' leverage points as possible, the data module captures at least a declaration at each level.

| # | Leverage point | What is captured | Scenario it enables |
|---|---|---|---|
| 12 | Parameters | Win rate, cycle, deal size, capacity, costs, counts | Improve a lever by x% |
| 11 | Buffers | Open pipeline per salesperson vs throughput; candidate bench | Is the pipeline buffer too thin to absorb a vacancy? |
| 10 | Stocks and flows | Territories, salespeople, pipeline; hires, departures, opportunity flow | Change the structure |
| 9 | Delays | Cycle, ramp, vacancy-to-fill by approval stage, revenue recognition lag | Cut approval time by 30 days |
| 8 | Balancing loops | Capacity ceiling and overload; budget limits on hiring | Where does the system push back on growth? |
| 7 | Reinforcing loops | Wins → references → opportunities; vacancy → stretch → attrition | Break a vicious cycle, feed a virtuous one |
| 6 | Information flows | Where each number comes from, who sees it, with what lag | Sales and Finance on the same definitions |
| 5 | Rules | Comp plan, hiring approval rules, qualification definition, assignment rules | Change the commission rule or the approval chain |
| 4 | Self-organization | Who can redesign territories or create roles | Let regions redesign coverage |
| 3 | Goals | Plan target, expected yield per territory, what the system optimizes | Optimize margin instead of bookings |
| 2 | Paradigm | How the market is defined; the stated theory of how customers buy | Are we carving the market the right way? |
| 1 | Transcending paradigms | The ledger itself: every belief held as falsifiable | Which assumption, if wrong, changes everything? |

Levels 12–8 are computed; 7–5 partly computed; 4–1 captured as structured declarations that frame scenarios. More possibilities widen the set of decisions leadership can consider. Goals and prescriptions come later.

## 7. Salespeople measured as agents

Salespeople are measured as agents in a complex system, to find interventions that improve system performance, not to inspect individuals.

- Pseudonymous IDs; names are never collected.
- Outputs show distributions and groups (tenure, ramp state, territory type, support model), never rankings.
- Groups smaller than about five are never displayed.
- Findings map to system interventions: enablement, support model, territory design, hiring speed, approval chain.
- People game data less when they are not judged individually, so data quality improves.

## 8. How it compares

Competitor details come only from the vendors' own pages (checked 2026-10-24). "Not described" means the page does not mention it.

| | This model | Fullcast | HubSpot ROI calculator | Pigment simulator | Anaplan, Xactly, Varicent | Sales velocity calculators | APQC diagnostic |
|---|---|---|---|---|---|---|---|
| What inputs are | Falsifiable claims with basis, owner, test | Plan inputs, typed or from history | Current metrics as entered | Slider settings | Plan inputs and CRM/HR history | Numbers as entered | Metrics vs peers |
| Tests inputs against reality | Yes: individually, jointly, over time | Not described | No | No | Not described | No | Compares with peers, not own data |
| Model structure open to testing | Yes | No | No | No | No | No | n/a |
| Territory separate from salesperson | Yes, linked by assignment | Ramped vs total headcount | No | No | Territory and capacity planned; method not described | No | No |
| Capacity basis | Opportunities held × 12 ÷ cycle | Quota × attainment | n/a | Quota × attainment | Not described | Opportunities as input, no ceiling | n/a |
| Open territory priced as lost contribution | Yes, including approval delays | Ramp profiles only | No | Ramp only | Coverage gaps (Anaplan) | No | No |
| Reaches the income statement | Yes, as the test instrument | Yes, pro forma P&L | License cost vs return | No | Not stated | No | No |
| Finance sign-off on the baseline | Yes | No | No | No | No | No | No |
| Running accuracy record | Yes | No | No | No | No | No | No |
| Scenarios beyond parameters | Delays, rules, goals, market definition | Parameters, headcount | Parameters | Parameters | Parameters, territories | Parameters | No |

The others take inputs and calculate outcomes. This model questions its inputs, tests them against the client's own financial reality, and keeps score on them over time.

Sources: [Fullcast](https://support.fullcast.com/docs/get-started-with-scenario-and-capacity-planning) · [HubSpot](https://www.hubspot.com/roi-calculator/sales) · [Pigment](https://www.pigment.com/hall-of-frames/sales-capacity-simulator) · [Anaplan](https://anaplan.com/solutions/go-to-market-capacity-planning) · [Varicent](https://www.varicent.com/products/territory-planning-software) · [Xactly](https://assets.xactlycorp.com/m/45651c4f8f4a3ac4/original/Plan-Product-Overview.pdf) · [APQC](https://www.apqc.org/resource-library/resource-listing/interactive-sales-tune-diagnostic) · [Pipedrive (velocity)](https://pipedrive.com/en/blog/sales-velocity)

## 9. Corrections to earlier analyses

Earlier documents in this repo are preserved as written. These readings in them are superseded:

| Earlier reading | Current understanding |
|---|---|
| A territory is a unit of demand | A territory is a design choice carrying an expected yield |
| $75,000 vs $33,113 is a data error | $75,000 is a deliberate reference value; the ledger must declare it and its scope |
| $112.5M vs $25M means the data contradicts itself | It is the gap between designed and actual yield, which the model exists to explain |
| Hard-coded salary and 12-month ramp are defects | Probably undeclared assumptions; declare, then test. Only the improve-all ramp contradiction is clearly a defect |
| Contracts and revenue inputs are dead | They are the actuals that test the assumptions |
| Judge the model on whether the math is right | Judge it on whether every assumption is explicit and testable |
| Per-salesperson output tables | Distributions and groups only; salespeople measured as agents |
