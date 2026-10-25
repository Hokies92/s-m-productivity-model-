# Data Model and Requirements: the Assumption Ledger

Status: **draft for review, 2026-10-24; aligned to [MODEL.md](MODEL.md) 2026-10-25.** Scope: the register (state assumptions) only. Method assumptions and scenarios belong to the modeller (MODEL.md §4) and are out of scope here. Defines what the data entry module collects, why, in what structure, and with what metadata, so scenario modules can later build on it. Background: [MODEL_UNDERSTANDING.md](MODEL_UNDERSTANDING.md). The as-is data entry sheet is preserved verbatim in `source/` and mapped field by field in section 10.

© 2000–2026 Growth Enablement. All rights reserved.

## 1. Purpose

**To produce a tested, calibrated, signed description of the client's commercial system as it really is, and to keep it accurate over time.**

1. **Make beliefs explicit.** Each one is a plain-language claim with value, range, scope, owner and reason.
2. **Declare the basis:** validated actual, calculated estimate, reference value (and from what context), or judgment.
3. **Attach a test:** what observation would prove the claim wrong, where it is measured, the threshold.
4. **Run the tests:** individually, jointly through their implications, against bounds, over time.
5. **Locate and record every gap.** Each failed test is resolved by revising, explaining, or accepting it as a known gap.
6. **Calibrate and sign.** The baseline reproduces actual results or carries its known gaps openly. Finance signs it.
7. **Set guardrails.** Tested assumptions become tolerances; drift and scenarios that leave tested ground are flagged.
8. **Build the track record.** Assumed vs observed every period, so accuracy improves and confidence is earned.
9. **Declare structure at every leverage point**, from parameters to paradigm, so scenarios can reach all of them.

What the module delivers before any scenario runs: the assumption register with statuses, test results, the yield bridge (designed → actual), the perception gap (believed → observed), the confidence profile, and open questions.

## 2. Design principles

| # | Principle |
|---|---|
| P1 | Lead with assumptions. Every value is a claim that can be disputed and traced. |
| P2 | Every claim is falsifiable: it names the observation that would prove it wrong. |
| P3 | Basis and scope are always declared. A reference value is legitimate; an undeclared one is not. |
| P4 | Territory design and staffing are separate entities, linked by assignment. |
| P5 | Salespeople are agents measured as a system: pseudonymous, never ranked. |
| P6 | Structure is data too: rules, delays, goals and the market definition are declared, not hard-coded. |
| P7 | Nothing is overwritten. History is the record that makes assumptions more accurate. |
| P8 | Derived values are recomputed from their inputs, never stored as truth. |
| P9 | Results flow immediately (working model), but are labeled until Finance signs off. |
| P10 | Hypothetical values are never mixed with observed values, in the baseline or in any benchmark. |

## 3. Entities and relationships

```
Client ── Engagement (scope, period, currency, revenue basis)
              │
              └── Baseline version (draft → working → in review → signed)
                     │
                     ├── Market definition (segmentation basis, theory of how customers buy)
                     │
                     ├── Territory ──────┐            (design choice: status, expected yield)
                     │                   ├── Assignment (share of time, effective dates)
                     ├── Salesperson ────┘            (agent: pseudonymous ID, start date, role, cost band)
                     │
                     ├── Event (vacated, requisition approved, offer accepted, started, ramp complete, departed)
                     ├── Rule (comp plan, approval chain, qualification definition, assignment rule)
                     ├── Financial line (P&L line, cost behavior: fixed, variable, step-fixed, discretionary)
                     ├── Information source (system or report, definition, owner, refresh lag)
                     │
                     ├── Assumption ─── Evidence (files, reports)
                     │       └── Test ─── Test result ─── Resolution
                     │
                     └── Scenario (changes to assumptions; never writes back into the baseline)
```

Every measured or asserted value in the model is an **Assumption** attached to an entity (the company, a territory, a salesperson, a group, or the model itself).

## 4. The assumption record

| Group | Field | Required | Why it exists |
|---|---|---|---|
| Identity | `assumption_id`, `field_id`, `entity_type`, `entity_id` | Yes | Join to territories, salespeople, assignments, model |
| Meaning | `definition_id` + version, `unit`, `period`, `scope`, `level` (company, territory, salesperson, group, model) | Yes | Same word, same meaning, across clients and time |
| Claim | `statement` (plain language), `value`, `low`, `high` | Statement and value yes; range required for estimate, reference and judgment | Lead with the assumption in words anyone can dispute |
| Basis | `basis_type`, `source` (document or system), `method`, `inputs` (assumption IDs), `reference_context` | Yes; reference context required for reference values | Shows why the number was chosen, including deliberate overrides |
| Owner | `asserted_by`, `asserted_at`, `rationale` | Yes | The person to go back to when someone disagrees |
| Falsification | `test_ids`, `observable`, `measured_in`, `threshold`, `review_date` | Yes for high-sensitivity fields; recommended for all | Makes the claim testable |
| Validation | `validated_by`, `validated_at`, `status` | When validated | Finance sign-off and the reconciliation trail |
| Track record | prior values, observed vs assumed per period, error, drift | Kept automatically | Accuracy improves; guardrails are earned |
| System role | `element_type` (parameter, stock, flow, delay, loop, information, rule, structure, goal, paradigm), `leverage_point` (1–12) | Yes | Lets scenarios work at every level |
| Handling | `pseudonymized`, `min_group_size`, `benchmark_consent` | Yes for salesperson data | Agents measured as a system; data rights respected |

**Basis types** (ranked for confidence, highest first):

| Basis | Meaning | Who may assign it |
|---|---|---|
| Validated actual | Confirmed by the client's Finance team from records | Finance only |
| Calculated estimate | Produced by a model estimator from client data; inherits the lowest basis of its inputs | The estimator |
| Reference value | Deliberately borrowed from another context (client, segment, published source), which is named | Anyone; context required |
| Judgment | A person's best estimate | Anyone; reason and range required |

## 5. Structural assumptions (model level)

| ID | Assumption | Test |
|---|---|---|
| S1 | A salesperson's throughput = opportunities held ÷ cycle (steady state) | Little's Law on CRM: open pipeline ≈ resolved per year × cycle |
| S2 | A territory yields only when filled and ramped | Revenue by territory status and tenure of the assigned salesperson |
| S3 | Win rate and deal size are independent | Do segments with larger deals win less often? |
| S4 | Load does not affect win rate or cycle | Win rate and cycle by load level across salespeople |
| S5 | Ramp shape (step, linear or curve) | Productivity by tenure month across hiring groups |
| S6 | Non-sales costs scale with revenue at fixed % | P&L history: do R&D and G&A move with revenue? |
| S7 | Commission is a flat rate on revenue | Comp ledger ÷ revenue, by period |
| S8 | One salesperson per territory | Assignment register |
| S9 | Every filled territory runs at full capacity | Utilization: measured load ÷ stated capacity |

## 6. Test library and standard cross-checks

| Test type | Logic |
|---|---|
| Direct observation | Compare with a measured value |
| Joint implication | Several assumptions together predict an observable |
| Triangulation | Same quantity derived two independent ways |
| Bounds | Impossible outcomes |
| Dispersion | Is one average enough? |
| Prediction | Last period's assumptions vs this period's observations |

A failed joint test shows at least one assumption in the set is false, not which one. The module shows the candidate set and asks the client to locate the error with targeted evidence.

**Standard cross-checks** (tolerance and severity are configurable per engagement):

| Check | Compares | Default tolerance | Default severity |
|---|---|---|---|
| Field bounds | Win rate 0–100%, cycle > 0, counts ≥ 0 | none | Block |
| Territory counts | Filled + open + shared = total | none | Block |
| Staffing | Assigned salespeople cover filled territories | none | Block |
| Components to totals | Overhead and marketing lines sum to totals | ±1% | Block until fixed or explained |
| Yield bridge | Designed yield − vacancy − ramp − coverage − agent gap = actual revenue | residual = 0 | Explain or accept |
| Revenue implication | All mechanics combined vs actual revenue | ±10% | Explain |
| Contracts implication | Implied contracts vs actual contracts | ±10% | Explain |
| Deal size triangulation | Revenue ÷ contracts vs entered deal size | ±10% | Explain; declare reference values |
| Little's Law | Open pipeline vs resolved per year × cycle | ±25% | Explain |
| Utilization | Measured load ÷ stated capacity | > 100% | Block (impossible) |
| Compensation | Salaries × load + commission × revenue vs ledger comp expense | ±10% | Explain |
| Expected yield | Sum of territory expected yields vs Finance plan | ±5% | Explain |
| Period alignment | All fields share period and scope | none | Block |
| Plausibility | Typical ranges (cycle 1–24 months, load rate 15–40%) | — | Warn |

## 7. Lifecycles and controls

**Assumption lifecycle:** proposed → declared (basis, scope, owner) → tested → supported or contradicted → resolved (revised, explained, or accepted as known gap) → monitored each period → superseded (history kept).

**Baseline lifecycle:** draft → working model (results visible, watermarked) → Finance review → signed (frozen). Editing a signed baseline reopens it.

**Controls against gaming the outcome:**

1. High-sensitivity fields (territories, filled seats, revenue, contracts, win rate, cycle, opportunities held, salary) must be validated actual or calculated estimate before sign-off.
2. Finance reviews the high-sensitivity fields, every explained or accepted gap, and a random sample of other fields (default 20%).
3. Key totals must tie to Finance's own reports.
4. Scenarios change assumptions in a copy; they never write into the baseline.
5. Every output shows how far results moved since first complete entry, and which edits moved them.
6. Every output shows its confidence profile: the share of the result resting on each basis type.

## 8. Collection workflow

| Step | Owner | Collects | Typical sources |
|---|---|---|---|
| 0. Scope | Sponsor | Period, currency, revenue basis, scope (company, channel, product line) | Sponsor's decision |
| 1. Financial actuals | Finance | Revenue, contracts, cost of revenue, R&D, G&A, total S&M, plan target | Income statement, plan |
| 2. Market and territory design | Sales Ops + Finance | Segmentation basis; territory register: ID, status, expected annual yield, segment tag, coverage and support model; for open territories: date opened, approval stage, expected fill | Territory plan |
| 3. Salesperson register | HR + Sales Ops | Pseudonymous ID, start date, role, assigned territory and share, cost band | HR system |
| 4. Agent measures | Sales Ops / CRM | Per salesperson ID: opportunities held, resolved, win rate, cycle, deal size; stated capacity | CRM exports |
| 5. Vacancy and hiring timeline | HR + Finance | Per vacancy: vacated, requisition approved, offer accepted, started, ramp complete | HR, approvals |
| 6. Costs and rules | Finance + Comp | Salary, load rate, commission plan, travel, overhead and marketing lines; approval rules; qualification definition | Payroll, comp, ledger |
| 7. Reconcile and sign | Finance lead | Cross-check queue, yield bridge, sign-off | — |

**Assistance in every step:** forwardable packets in the client's language (web form and an Excel packet that round-trips by field ID); report recipes naming the exact export; raw-file upload with our estimators doing the arithmetic; live implied values as data arrives; a results preview with confidence score. **Aggregate fallback:** a client without per-territory or per-salesperson data may enter averages, tagged as aggregate; territory and agent outputs stay locked until detail arrives.

## 9. Storage rules

- Append-only history; nothing is overwritten.
- Signed baseline versions are frozen; scenarios reference a specific version.
- Derived values are recomputed, never stored as truth; cached scenario results carry the engine version.
- Client data is isolated; benchmark consent is a separate opt-in; hypothetical values are tagged apart from observed values.
- Salesperson data is pseudonymous; groups below the minimum size are not displayed.
- V1: SQLite plus an evidence folder; schema in [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) and `src/sales_capacity_model/db/`. Production: PostgreSQL plus file storage. Excel import and export use stable field IDs.

## 10. Map from the as-is data entry sheet

Every as-is field is kept. Cell references are the original's (see `source/workbook_cells.csv`).

| As-is field (cell) | As-is value | New home | Basis in the as-is sample | Note |
|---|---|---|---|---|
| Number of sales territories (F9) | 100 | Territory register: count and status | Judgment / illustrative | Now one record per territory, with status and expected yield |
| Average revenue per transaction (F11) | $75,000 | Agent measure: deal size; company-level derived | **Reference value** from another client | Must declare reference context and scope |
| Number of contracts last year (E12) | 755 | Financial actuals: contracts | Illustrative actual | Now feeds the implication tests |
| Revenue from those contracts (E13) | $25,000,000 | Financial actuals: revenue | Illustrative actual | Now feeds the implication tests and the yield bridge |
| Average fully loaded salary (F15) | $116,850 | Derived: salary × (1 + load) | Calculated | As-is engine uses a hard-coded $87,750 (to declare and test) |
| Average salary per sales salesperson (E16) | $95,000 | Costs: base salary, per salesperson or band | Judgment | |
| Corporate load rate (E17) | 23% | Costs: load rate | Judgment | As-is definition includes overhead allocation; proposed: benefits and taxes only |
| Average travel costs per salesperson (F19) | $47,500 | Costs: travel per salesperson | Calculated from trip components | |
| Travel components (E20–E26) | $750, $200, $100, $250, 2 days, $250, 25 trips | Estimator: trip calculator | Judgment | Kept as the travel estimator |
| Commission (F28) | 8% | Rules: comp plan; Costs: effective commission | Judgment | Flat rate is structural assumption S7 |
| Opportunities manageable at one time (F31) | 30 | Agent measure: stated capacity (plus measured load, new) | Judgment | Capacity and load now separate |
| Length of sales cycle (F33) | 6 months | Agent measure: cycle; territory: segment cycle | Judgment | Definition: qualified-opportunity creation to signature |
| Sales ramp up time (F35) | 12 months | Delays: ramp; structural assumption S5 | Judgment | As-is applies a step ramp to added territories only |
| Close rate (F37) | 25% | Agent measure: win rate | Judgment | Definition: won ÷ (won + lost), by count |
| Total sales overhead and marketing (F39) | $14,500,000 | Derived | Calculated | |
| Sales overhead costs (F41) and five lines (E42–E46) | $10.8M | Financial lines, cost behavior tagged | Judgment | Lines kept |
| Marketing costs (F48) and eight lines (E49–E56) | $3.7M | Financial lines, cost behavior tagged | Judgment | Lines kept |
| *Cost of revenue, R&D, G&A % (Impact sheet C30–C32)* | 13.22%, 10.19%, 15.40% | Financial actuals, step 1 | **Reference value** (industry averages) | Now asked; reference used only as fallback |

**New in the redesign (not in the as-is sheet):** market segmentation basis; territory status, expected yield, coverage and support model; salesperson register and assignment; measured load; vacancy and approval timeline; hires and departures; rules beyond the commission rate; plan target; information sources; cost behavior tags; falsification tests and assumption history.

## 11. Requirements

### Assumption ledger
- **DM-01** Every value is stored as an assumption record with the required fields in section 4.
- **DM-02** Every assumption declares one basis type; reference values name their source context.
- **DM-03** Judgment and reference values carry a low–high range.
- **DM-04** Every assumption declares its scope; the same field may hold different values in different scopes.
- **DM-05** Calculated estimates record their inputs and inherit the lowest basis among them.
- **DM-06** Structural assumptions S1–S9 are stored in the same ledger at model level.
- **DM-07** Only a Finance user may assign the validated-actual basis (until named Finance users exist, an attestation is recorded and the baseline stays a working model).
- **DM-08** Every *state* value a calculation uses is a register entry with a basis; the modeller holds no state of its own. Method assumptions (equations, rules) live with the modeller, in words beside the formula, and are not register entries. (As-is case: the $87,750 salary typed into the engine is a state value with an alternative basis; in the rebuild it is the loaded-salary entry with its input method.)

### Entities
- **DM-10** Territories and salespeople are separate entities; revenue attribution requires an assignment.
- **DM-11** Each territory record carries status and expected yield; open territories carry vacancy dates and approval stage.
- **DM-12** Salesperson records use pseudonymous IDs; names are never required.
- **DM-13** The engagement declares one period, currency, revenue basis and scope; every field inherits them unless an exception is recorded.
- **DM-14** Every financial line carries a cost behavior tag.

### Testing and reconciliation
- **DM-20** Every high-sensitivity assumption has at least one falsification test.
- **DM-21** The standard cross-checks in section 6 run on every change, with configurable tolerance and severity.
- **DM-22** A failed check enters the reconciliation queue and must be fixed, explained (with category and note) or accepted as a known gap.
- **DM-23** The yield bridge reconciles designed yield to actual revenue with an unexplained residual of zero or a recorded explanation.
- **DM-24** A failed joint test presents the candidate assumption set, not a single verdict.

### Lifecycle, history and controls
- **DM-30** History is append-only; prior values and their bases are retained.
- **DM-31** Observed vs assumed is recorded each period, with error and drift.
- **DM-32** Baselines move through draft, working, review and signed; signed baselines are frozen.
- **DM-33** Until signed, every output is labeled "Working model: not validated by Finance."
- **DM-34** The anti-gaming controls in section 7 are enforced before sign-off.

### Collection
- **DM-40** Collection is organized in owner-routed steps (section 8), each forwardable.
- **DM-41** Web form and Excel packet use the same field IDs; Excel import runs every validation and never silently overwrites.
- **DM-42** Raw exports (P&L, CRM, roster, ledgers) can be uploaded; estimators compute values from them.
- **DM-43** Aggregate entry is allowed and tagged; territory- and agent-level outputs require detail.

### Outputs of the module
- **DM-50** Assumption register with status per assumption.
- **DM-51** Test results and reconciliation log.
- **DM-52** Yield bridge and perception gap.
- **DM-53** Confidence profile per result.
- **DM-54** Agent results as distributions and groups only; groups below the minimum size are hidden.

### Compatibility
- **DM-60** The as-is workbook remains reproducible (48/48 parity) as a declared set of assumptions.
- **DM-61** Every as-is field maps to the new model (section 10); nothing from the as-is sheet is dropped.

## 12. Open decisions

| # | Decision | Proposed |
|---|---|---|
| E1 | Which opportunity count drives the model | Both: measured load is the observation, stated capacity the ceiling |
| E2 | Revenue basis | Chosen in step 0; recognized revenue by default |
| E3 | New vs existing-customer revenue | One pool in V1, with a share flag |
| E4 | Load rate content | Benefits and taxes only |
| E5 | Deal size entry | Derived by default; typed value allowed as a declared reference value or judgment |
| D1 | Basis ranking | Reference value above judgment |
| D2 | Tolerances and severities | Accept section 6 as a starting set |
| D3 | Mandatory Finance review | Fixed list in section 7 for V1 |
| D4 | Spot-check sample | 20% |
| D5 | As-is 12-month step ramp | Confirm intent; record as a declared assumption. (Salary resolved: $87,750 was a deliberate test estimate; see DM-08) |
