# Sales Capacity Model: Discovery and Architecture Assessment

Oct 24, 2026 · Scott Santucci

> Repository copy. The live version with its chart and two diagrams: https://claude.ai/artifact/U4pvy1F8aYHdJuVzPGE1Lh

## Bottom line

The model is valid and worth rebuilding, but its headline conclusion is stronger in the workbook than the math alone supports. Quality levers beat hiring by $1.35M per 10% at steady state, not by the $8.24M the workbook shows.

| Area | Verdict | Basis |
| --- | --- | --- |
| Core premise (capacity = cognitive load × time) | Valid | Same form as Little's Law: throughput = work in progress ÷ cycle time |
| Arithmetic | Valid | Python engine reproduces all 48 workbook outputs exactly |
| Workbook implementation | Invalid in 3 places | Hard-coded salary; two contradictory treatments of new-rep ramp |
| Conclusion: quality beats hiring | Valid, conditional | Holds under every option, but the size of the win depends on two assumptions |
| Ontology: territory ≠ headcount ≠ capacity | Stated, not implemented | The math still costs one rep per territory |
| Python package | Sound foundation | Pure functions, tested, workbook-faithful by default |
| Fitness for rebuild | Ready, after 4 decisions | See Roadmap and decisions |

Three findings matter most:

1. **The win is mostly an assumption.** Revenue is a pure product of territories, opportunities, close rate and deal size, so a 10% change in any lever adds about the same revenue. Quality wins only because the model charges hiring for salary, travel and ramp, and charges quality improvement nothing.
2. **Ramp drives the dramatic year-1 result.** With a 12-month ramp, new territories add cost and zero revenue. With full-year credit, hiring adds $4.63M of operating income against $5.98M for close rate.
3. **The right output is a break-even budget.** The model can say exactly how much a company can spend to lift close rate 10% and still beat hiring: $8.24M in year 1, $1.35M at steady state. That is a sharper, more defensible claim than "quality always wins."

## Scope and method

The assessment covers the original workbook, the v2.0 specification, and the v2.1 Python package, as of commit `08ff311`.

- **Formula discovery:** the `.xls` was converted and all 415 non-empty cells exported with formulas and stored values.
- **Independent rebuild:** every calculation reimplemented in Python and checked cell by cell against stored outputs (48/48 match).
- **Option testing:** all 6 combinations of salary source and ramp rule run, to see which conclusions survive.
- **Sensitivity:** each lever moved 1% and 10%; break-even investment computed against hiring.
- **Conceptual review:** each formula traced back to the premise it encodes, and each premise checked for whether the code actually expresses it.

Not in scope: validating the default input values against real company data, and the Hidden Commercial Costs framework beyond its link points.

## Model inventory

Seven artifacts make up the model today; only the workbook and the package compute anything, and the package is now the source of truth.

| Artifact | Role | Computes? | Status |
| --- | --- | --- | --- |
| Original workbook (`.xls`), 5 sheets | Origin; reference copy | Yes | Frozen. 3 defects documented |
| Formula export (`workbook_cells.csv`), 415 cells | Ground truth for what the workbook does | No | Complete |
| Python package `sales_capacity_model` v2.1.0 | Engine, scenarios, diagnostics, CLI | Yes | 11 tests passing; workbook-faithful by default |
| JSON specification v2.1 | Machine-readable description for analysis | No | Reconciled to workbook |
| White paper (`.docx`) v2.0 | Narrative explanation | No | Out of date: 5 errors listed in Audit Findings |
| Audit Findings | Defects and open decisions | No | Current |
| About, Product Overview | Positioning and usage | No | Current |

| Sheet | Layer | Cells | Holds |
| --- | --- | --- | --- |
| Orientation | Narrative | text | Purpose and instructions |
| 1) Data entry | Inputs | 31 entry cells (2 unused) | Territories, deal size, cost components, mechanics, overhead, marketing |
| 2) Performance breakdown | Engine | 7 scenario columns | Capacity chain and per-rep economics |
| 3) Impact Analysis | Financial bridge | 7 scenario columns | Income statement, % net gain, S&M ROI |
| 4) Scenario Diagnostic | Interpretation | 15 obstacles | Obstacles and root causes for 3 quality levers |

## Conceptual soundness

The premise is valid; the conclusion follows from it only once the cost of improving quality is added, which the model does not yet do.

The capacity equation is Little's Law applied to a salesperson:

    Opportunities resolved per year = Opportunities held at once ÷ Cycle time (years) = M × 12 ÷ Y

Revenue is then a pure product of the levers:

    Revenue = T × M × (12 ÷ Y) × R × D

Because every lever enters as a multiplier, a 10% change in territories, close rate or deal size adds exactly the same revenue ($11.25M), and a 10% shorter cycle adds 11.1% ($12.50M). The levers differ only in what they cost. That is the real engine of the conclusion.

| Assumption the math depends on | Valid? | What follows if it fails |
| --- | --- | --- |
| Each rep runs at full capacity (always holding M opportunities) | Valid for planning; optimistic in practice | Revenue overstated wherever pipeline is thin. The optional lead input now tests this |
| Close rate applies to every resolved opportunity, won or lost | Valid | None; it is the right base for Little's Law |
| Cognitive load, cycle and close rate are independent | Invalid by the model's own theory | The theory says overload lowers close rate and lengthens cycle. The math has no such link, so it cannot show the cost of piling on leads |
| Improving close rate, cycle or deal size costs nothing | Invalid as stated | Quality's advantage is overstated by whatever the improvement costs. This is the largest open assumption |
| New territories need a full 12-month ramp | Plausible for year 1 only | Year-1 view makes hiring look loss-making; steady state narrows the gap to $1.35M |
| One rep per territory | Contradicts the ontology | Territory ≠ headcount is asserted but not modeled |
| COGS, R&D and G&A grow in proportion to revenue (38.81%) | Conservative | Penalizes every growth lever equally; real G&A is partly fixed, so all scenarios understate profit |
| Commission is a flat 8% of revenue | Simplification | Accelerators or caps would change cost per rep at higher output |

The defensible form of the claim is: *quality levers produce the same revenue as hiring with no added fixed cost, so they win whenever the improvement costs less than the hire.* The model can quantify that threshold exactly.

## Calculation architecture

The model is a single forward chain of six layers with no feedback; the scenario layer injects each lever at exactly one point.

*[Diagram in live doc]* Inputs → Capacity (M × 12 ÷ Y) → Throughput (× R, × D) → Scale and cost (× T; S&M) → Income statement → Metrics → (Diagnostics, static). Scenario layer injects Y into capacity, R and D into throughput, T into scale.

The chain runs strictly downward, which makes it easy to audit and also explains gap G2: nothing below capacity can push back on it, so overload cannot lower close rate or stretch the cycle. Diagnostics hang off the end as text and do not feed any number.

## Sensitivity and break-even

The ramp assumption, not the capacity math, decides how large the quality advantage is: $8.24M in year one, $1.35M at steady state.

*[Chart in live doc]* Change in operating income from a 10% move, $M:

| Lever | Year one (12-month ramp) | Steady state (full credit) |
| --- | --- | --- |
| Add territories | −2.25 | +4.63 |
| Raise close rate | +5.98 | +5.98 |
| Shorten cycle | +6.65 | +6.65 |
| Raise deal size | +5.98 | +5.98 |

All three quality levers return the same amount in both views because they add no people. Hiring swings by $6.88M depending on whether new reps earn anything in their first year.

| Measure (steady state) | Add territories | Close rate, cycle or deal size |
| --- | --- | --- |
| Operating income kept from each new revenue dollar | 41.2% | 53.2% |
| Operating income per 1% lever move | $0.43M | $0.60M |
| Close-rate lift that equals a 10% territory increase | — | 7.7% |

The 12-point flow-through gap is the fixed cost of a territory: $135,250 of salary and travel against $1.125M of revenue per rep. When revenue per rep is high relative to fixed rep cost, hiring closes the gap; when it is low, quality wins by more.

**Break-even quality budget**, the most a company can spend on a 10% improvement and still beat a 10% hire:

| View | Salary basis | Close rate or deal size | Cycle time |
| --- | --- | --- | --- |
| Year one | Workbook $87,750 | $8.24M | $8.90M |
| Year one | Entered $116,850 | $8.53M | $9.19M |
| Steady state | Workbook $87,750 | $1.35M | $2.02M |
| Steady state | Entered $116,850 | $1.64M | $2.31M |

This is the number a CFO can act on. It turns "quality beats quantity" into a budget ceiling for enablement, process or pricing work.

## Implementation assessment

The workbook is a clear, auditable layout with three defects and no controls; the package fixes the controls and preserves the defects on purpose until they are decided.

### Original workbook

| Finding | Type | Effect at defaults |
| --- | --- | --- |
| Fully loaded salary hard-coded at $87,750; entered $116,850 never used (F1) | Defect | Rep costs understated $2.91M; baseline operating income $31.81M instead of $28.90M |
| "Add territories" credits new reps with (12 − ramp) ÷ 12 of a year: zero at 12 months (F2) | Undisclosed modeling choice | Hiring shows −$2.25M operating income |
| "Improve all" subtracts the ramped share, not the unramped share (F3) | Defect | New reps get full-year credit; column overstated by up to $15.13M |
| % Net Gain = (Δrevenue − Δsales cost) ÷ baseline revenue | Undocumented definition | Ignores COGS, R&D, G&A growth; reads 9.2% where operating income rises 18.8% |
| S&M ROI = (revenue − S&M) ÷ S&M | Undocumented definition | 2.04, easily misread as revenue ÷ cost (3.04) |
| Contracts (755) and contract revenue ($25M) entered, never used | Dead inputs | Implied deal size $33,113 conflicts with the $75,000 used |
| Ramp applied only to new territories | Partial | No attrition, backfill or vacancy in the base |
| No input validation, version history or test | Missing controls | Errors like F1 and F3 survived from 2000 to 2026 |

Strengths worth keeping: one sheet per layer, inputs separated from logic, every scenario side by side with baseline, and an income-statement bridge most sales models never build.

### Python package v2.1.0

| Aspect | Assessment |
| --- | --- |
| Structure | Clean layers: `inputs` → `engine` → `report` / `cli`; `diagnostics` and `verify` separate |
| Correctness | Workbook parity is a test; any change that breaks it fails the build |
| Calculation style | Pure functions, no global state, no dependencies; easy to call from a spreadsheet generator, an API or an app |
| Open decisions | Exposed as options (`use_entered_salary`, `ramp_rule`), not settled silently |
| Inputs | Typed, validated, with derived totals computed from components as the workbook does |
| Gaps | Single period; one rep per territory; scenario logic hard-wired to 7 named cases; no investment cost per lever; P&L mapping fixed as % of revenue |
| Risk | `_revenue()` branches on scenario names to reproduce F2/F3. Correct today, but the first thing to replace once the ramp rule is decided |

## Architectural gaps

Six places where the theory says more than the code computes; closing the first two would turn an argument into a decision tool.

| # | The theory says | The code does | What closing it adds | Priority |
| --- | --- | --- | --- | --- |
| G1 | Quality improvement takes effort and money | Treats every quality lever as free | An investment cost per lever, giving ROI and break-even budget per lever | Critical |
| G2 | Overload degrades close rate and lengthens cycle | Load, close rate and cycle are independent | A load-to-quality curve: past capacity, extra leads lower R and raise Y. This is the mechanism behind "more is wrong" | Critical |
| G3 | Territory ≠ headcount ≠ capacity | Cost = reps × territories, 1:1 | Separate counts for territories, people and coverage ratio; shared or split territories | High |
| G4 | Capacity is set by cognition and time | Cognitive load M is a fixed input | Drivers of M: deal complexity, stakeholders per deal, admin and non-selling time. This is where the timely / relevant / in-context framework would enter | High |
| G5 | Ramp, attrition and vacancy shape real capacity | One year; ramp only for added territories | Multi-period view: monthly capacity with ramp curves, attrition, backfill lag | Medium |
| G6 | The income statement is the canonical measure | Non-sales costs fixed at 38.81% of revenue | Configurable P&L mapping: fixed vs variable lines, actual figures, multiple charts of accounts. This is the link to Hidden Commercial Costs | Medium |

Two smaller gaps: leads now enter only as a cap on opportunities worked (G2 would make them matter), and diagnostics are static text with no tie from an obstacle to the lever value it suppresses.

## Target architecture

Rebuild around one tested Python engine and generate every surface from it, so the spreadsheet, the app and the documents can never disagree.

*[Diagram in live doc]* Layers, bottom to top: Ontology and data contracts → Financial bridge (P&L mapping G6, quality investment cost G1) → Engine (capacity, load-to-quality G2, cognitive-load drivers G4, territory ≠ headcount G3, monthly ramp/attrition G5) → Scenarios and decisions (scenarios as data, break-even budget) → Surfaces (generated spreadsheet, app, CLI/API, generated documents). Assurance alongside: workbook parity, tests, validation, provenance, versioning.

Data flows upward: definitions and inputs at the base, the engine in the middle, decisions and surfaces on top. Each gap from the previous section lands in exactly one layer.

Four design rules carry the architecture:

1. **The engine is the only place a number is computed.** The spreadsheet is generated with live formulas for transparency, not maintained by hand. This removes the class of error that let F1 and F3 survive 26 years.
2. **Scenarios are data, not code.** A scenario is a named set of lever changes. Today's seven columns become seven rows of a default list, and clients add their own.
3. **Workbook mode stays forever.** The original logic remains a selectable mode with its parity test, so the E&Y-audited lineage is always reproducible.
4. **The ontology is the contract.** Territory, headcount, capacity and opportunity are defined once in the input schema, so every surface uses the same meaning. This is the same meaning-consistency problem Hidden Commercial Costs addresses, solved here first.

## Roadmap and decisions

Four decisions gate the rebuild; each has a recommended answer, and none changes which lever wins.

| # | Decision | Options | Recommendation | Why |
| --- | --- | --- | --- | --- |
| D1 | Salary source | Workbook $87,750 · entered base × (1 + load) | Entered | The hard-code is a defect, not a choice |
| D2 | Ramp rule | Workbook (inconsistent) · year one · steady state | Report year one and steady state side by side | Year one alone makes hiring look loss-making; steady state alone hides ramp cost. Both are true |
| D3 | Headline metric | Workbook % net gain · Δ operating income · break-even quality budget | Δ operating income, with break-even budget as the decision number | % net gain ignores most of the P&L; break-even budget answers "how much can we spend on getting better?" |
| D4 | Quality investment | Free (today) · cost per lever entered by the user | Cost per lever, default zero | Makes the conclusion testable instead of assumed (G1) |

The phased plan, each phase gated on the last:

1. **Settle and correct (v2.2).** Apply D1–D4, replace the scenario-name branches in `_revenue()` with one ramp rule, add the break-even output, update the white paper. Gate: `scm verify` still passes in workbook mode.
2. **Separate territory from headcount (v3.0).** Territories, people and coverage as distinct inputs; quality investment cost per lever. Gate: the ontology in the white paper is now computed, not just stated.
3. **Model the mechanism (v3.1).** Load-to-quality curve (G2) and drivers of cognitive load (G4). Gate: the model can show that more leads lower profit past capacity.
4. **Time and the P&L (v4.0).** Monthly multi-period view with ramp, attrition and backfill (G5); configurable P&L mapping (G6). Gate: a real client's actuals run through it.
5. **Surfaces.** A generated spreadsheet with live formulas for transparency, and an app with guided entry. Both read the same engine.
