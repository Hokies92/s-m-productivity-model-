# The Model: current statement

This is the one current statement of what the Commercial Effectiveness Model (Sales Capacity Model, 2000) is. Any document in this repository that disagrees with it is wrong and is corrected or archived. Tests in `tests/test_workbook.py` enforce the invariants in §7.

© 2000–2026 Growth Enablement. All rights reserved. Author: Scott Santucci.

## 1. What it is

A falsifiable model of a company's commercial system. It records what the company believes about that system, tests the beliefs against the company's own financial results, and then asks what would happen to operating income if named parts of the system changed. It is not a forecast, not an evaluation of individuals, and not a benchmark.

## 2. Definitions and units

| Term | Means | Unit |
|---|---|---|
| Territory | A funded decision about how to divide the market. Carries an expected yield whether filled or open. | count |
| Salesperson | A person in a quota-carrying role. Measured as an agent in a system, never by name. | count |
| Capacity | The most qualified opportunities one salesperson can hold and advance well at the same time. Cognitive, not hours. | opportunities per salesperson |
| Opportunities held | Open qualified opportunities ÷ salespeople, from the CRM. | opportunities per salesperson |
| Opportunities worked | The lesser of held and capacity. | opportunities per salesperson |
| Cycle | Median months from qualified opportunity to signature, won deals. | months |
| Close rate | Won ÷ (won + lost) qualified opportunities, by count. | ratio |
| Deal size | Revenue ÷ contracts. | currency per contract |
| Ramp | Months until a new salesperson reaches average productivity. | months |
| Operating income | Revenue − cost of revenue − operating expenses, on the pro forma income statement. | currency |

**The unit of throughput is the salesperson.** Territories scale design (how many yields are expected); salespeople scale production. The original scaled a per-person throughput by the territory count, which is the special case where every territory is filled by one ramped salesperson.

## 3. The chain

Every line depends only on lines above it. Same chain in every scenario column.

```
worked      = MIN(held, capacity)                 (capacity if held not entered)
resolved    = worked × 12 ÷ cycle                  (Little's Law)
contracts/s = resolved × close rate
revenue/s   = contracts/s × deal size
revenue     = revenue/s × salespeople
contracts   = contracts/s × salespeople

cost of revenue   = revenue × cost of revenue %
R&D               = revenue × R&D %
salesperson pay   = loaded salary × salespeople
salesperson travel= travel per salesperson × salespeople
commissions       = commission rate × revenue
sales overhead    = fixed
marketing         = fixed
G&A               = revenue × G&A %
operating income  = revenue − cost of revenue − (R&D + sales + marketing + G&A)
```

Self-tests on every column: Δrevenue − Δcosts − Δoperating income = 0; model baseline revenue within tolerance of reported revenue; close rate ≤ 1; cycle > 0.

**Inverse.** Operating income is linear in revenue (variable costs are ratios of revenue; the rest is fixed), so for a target operating income: required revenue = (target + fixed) ÷ (1 − variable %). Revenue is proportional to close rate and deal size and inversely proportional to cycle, so the required revenue converts directly to the value each lever would need. This holds only while levers are multiplicative on revenue; territory and hiring levers are not, and are deferred.

## 4. Three kinds of assumption, and where each lives

| Kind | What | Lives in | Tested by |
|---|---|---|---|
| State | A belief about the system as it is: a value, a definition, a rule the company runs by | The register: `1) Data Entry`; `register` schema | The company's actuals, via cross-checks, this period |
| Method | An equation or reasoning rule applied to the register | Beside each formula, in words: logic sheets; `modeller` schema | Parity with the original; the true-up; hand recomputation |
| Intervention | A hypothesis: "close rate +10%" | The modeller's scenario table only | Nothing now; next period's register shows what happened |

Intervention hypotheses never enter the register. If they did, the baseline would validate against its own proposals.

## 5. Input methods and basis

Every register entry has one value used, chosen by rule: the model's estimate if the client selects it and it can be computed; otherwise the client's value; otherwise a labeled sample default. Its basis is recorded as one of: Validated by Finance, Your entry (not validated), Our estimate, Default (sample), Not provided (optional). Until every used entry is validated and every check passes, every result carries "Working model: not validated by Finance."

Collection order, chosen for ease of assembly: 1 financial results (Finance); 2 sales and marketing costs (Finance); 3 territories and salespeople (Sales Operations, HR); 4 pipeline and mechanics (Sales Operations).

## 6. Deliberate values in the original, and what each tests

| Value | Tests whether the reader sees | Correct reading |
|---|---|---|
| Salary $87,750 typed in the engine; $116,850 computed on the entry sheet | That entries are referenced by other sheets and can be overridden by any input method | An entry with an alternative basis, not a defect |
| Deal size $75,000; revenue ÷ contracts = $33,113 | That a value has a scope | A reference value from another context, valid for a general model, contradicted for this client |
| Ramp 12 months, credited (12 − ramp)/12 in one column and a full year in another | That ramp is an assumption to declare, with one rule | Declare the rule; the register holds ramp as an entry |

These are kept in `source/` as they are. They are tests of method: synthesis (how does the whole compose) before reduction (which part disagrees with which).

## 7. Invariants

1. **Oracle.** `source/` is never edited. The Python engine with default options reproduces all 48 original outputs.
2. **Parity.** For the original's inputs, the rebuilt workbook reproduces the original's contracts, revenue and change in operating income for close rate, cycle, deal size and combined scenarios.
3. **Unit.** Throughput is per salesperson. Every artifact that computes the chain uses that unit or is labeled as the as-is oracle.
4. **One-way flow.** `1) Data Entry` → `1) Data Entry Logic` → `2) What-If Logic` → `2) What-If`. No sheet reads a sheet downstream of it, except the client's scenario choices read by the logic sheet.
5. **Named interface.** Downstream sheets read the register only through `v_<id>` names, and every name referenced exists.
6. **Rule in words.** Every logic row carries its rule in words beside its formula.
7. **Register purity.** No scenario or intervention field in the register, in the workbook or the schema.
8. **Separation of schemas.** State assumptions in `register`; scenarios and method versions in `modeller`.
9. **Terminology.** Salesperson / salespeople. Not the s-word and not the three-letter abbreviation of "representative". Outside `source/` and archived documents.
10. **Income statement in the loop.** Every scenario result is an operating income, after all costs, with a balanced true-up.
11. **Labeled until validated.** Results carry the validation banner until Finance has validated every used entry and all checks pass.

## 8. What is deferred, and why

Territory and hiring scenarios (add territories, fill open territories, fill speed, ramp). They break the multiplicative inverse in §3 and need the territory–salesperson assignment made explicit. Ramp and open territories are collected now so the register is ready. The original's "hire more salespeople" column is the quantity lever shown beside the quality levers, and returns with them.

Scenario Diagnostic (obstacles per scenario), the original's fourth sheet. Returns keyed to scenario ids once the modeller's scenario table exists.
