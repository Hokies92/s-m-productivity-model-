# Commercial Model: Learnings and Assisted Data Entry Handoff

Date: October 26, 2026

Status: Source-ready design handoff. Captures this conversation's learning and proposals, reconciled with the GitHub documents inspected on this date. It is not a code-change or test-completion report.

Suggested project location: `docs/design/assisted-data-entry-and-state.md`.

## 1. Purpose and authority

The project helps leadership compare commercial investment choices by carrying operating assumptions through resource costs and a pro forma income statement to operating income. The original compares adding resources with improving existing capacity; the evolution supports broader assumption-driven exploration of alternatives.

Start with the original Data Entry sheet and preserve its explanatory detail. Assisted collection should help users understand the commercial system as they describe it, rather than merely collect numbers for a later calculator.

For `Hokies92/s-m-productivity-model-`, `docs/MODEL.md` is the canonical statement. This handoff supports its evolution and does not supersede it. Source evidence and confirmed author intent govern interpretations. Its protected original and as-is oracle remain unchanged. Evolution proposals belong on the evolution path.

For `Hokies92/sales-marketing-effectiveness-model`, the inspected `docs/spec/business_logic_v1.md` describes a separate engine implementation. Do not assume its interfaces, corrections, or test claims apply to the other repository. Select the target repository before integration.

## 2. What we learned about the whole model

The model connects resources and spending, operating mechanics, and financial consequences. Its distinctive design intent is to evaluate changes at operating income, with explanatory obstacles attached to improvement choices.

The operating chain is concurrent opportunity capacity → annual opportunity throughput → successful transactions → transaction value. Resource and operating assumptions determine costs as well as volume. Their combined financial effect is the comparison, not revenue alone.

Under a stated steady-state convention:

`transaction capacity = productive equivalents × concurrent opportunities × (12 / cycle months) × win rate × average transaction value`

The original uses territories in place of productive equivalents. Evolution must separate territory design from staffing, linked through assignment. Capacity means opportunities a salesperson can hold and advance effectively; time constrains it, but capacity is not simply labor hours.

The model can operate with imperfect data. Estimates and explicit assumptions are legitimate. Actuals strengthen calibration but must not silently overwrite a selected assumption. Mathematical sensitivities describe the specified model, not the difficulty or causal effectiveness of an intervention.

Compounding is useful: a 10% relative close-rate increase, a 10% transaction-value increase, and a 10% cycle reduction produce a capacity multiplier of `1.1 × 1.1 / 0.9 = 1.344444`. This does not establish that all three changes can be achieved independently or without investment.

## 3. Corrections to earlier interpretations

The latest inspected canonical model records information that changes some earlier statements in this conversation:

| Earlier characterization | Correct handling for the current project |
|---|---|
| $87,750 engine salary versus $116,850 entry calculation was simply a disconnected defect | Canonical document records confirmed author intent: a deliberate estimate testing understanding. Preserve the original and distinguish entered, calculated, and applied values. An evolved linking policy is explicit, not a retroactive correction of intent. |
| $75,000 transaction value should necessarily reconcile to $25M / 755 | Canonical document records the $75,000 reference came from a different client. Preserve both; compare their basis and scope before proposing reconciliation. |
| Original ramp differences should automatically be corrected | Canonical document marks intent open and requires exact original reproduction as a special case. A consistent alternative policy may be explored separately. |
| The existing model is universally best described as a simulator | Describe original and evolution separately. Canonical original is an investment comparison; the adopted product direction is broader simulation and decision support. |
| A complete-looking result is valid if its formulas add correctly | Input completeness, computational correctness, and economic validity are distinct. Missing required costs cannot silently become zero. |

The prior local `Commercial_Effectiveness_Specification_V1.md` is a dated working proposal. Where its default replacement rules conflict with current canonical interpretation, use the canonical interpretation and this correction table before implementation. Do not insert both as competing current specifications.

## 4. What we contributed, and what GitHub actually shows

### Contributions made in this conversation

- Examined the uploaded original workbook's sheets, values, instructions, mechanics, and scenario outputs.
- Adopted the user's revised framing: assumption-driven commercial and financial scenario exploration, constrained by explicit financial consequences.
- Created `Commercial_Effectiveness_Specification_V1.md` as a working business-logic and scenario specification, starting from the original Data Entry detail.
- Proposed assisted input routes, live economic feedback, reconciliation prompts, sensitivity-guided collection, reusable business profiles, and versioned state.
- Prepared this handoff and corrected interpretations using the current repository documents.

No GitHub write, commit, pull request, or implementation was made by this assistant in this conversation. The earlier specification was saved as a document. Existing repository work must not be attributed to this assistant without commit evidence.

### Repository evidence inspected October 26, 2026

| Repository | Evidence | What can be stated |
|---|---|---|
| `Hokies92/sales-marketing-effectiveness-model` | README; `docs/spec/business_logic_v1.md` | Documents a Python reference engine and engine v2 covering provenance, operating policies, scenarios, financial bridges, comparison, and tests. README lists web application and later analytics/benchmarking as pending. |
| `Hokies92/s-m-productivity-model-` | README; `docs/MODEL.md`; CONTRIBUTING | Documents protected original reproduction, a modern as-is workbook not yet approved, and an evolution branch with register/modeller separation and territory–salesperson separation. Canonical document lists input-completeness and version-linkage requirements still needing work. |

These are repository-reported statuses, not independently rerun tests. Source modules, branch implementations, and CI results were not audited in this handoff. The two repositories' test counts and baseline conventions must not be blended.

## 5. Data entry becomes a register of the business state

Retain the original three groups:

1. Individual sales resource data: territories, staffing, transaction value, compensation, load, travel, commission.
2. Sales mechanics: concurrent opportunity capacity, cycle, ramp, close rate.
3. Overhead, management, and marketing: all original spending categories and supporting detail.

The register records observations and beliefs about the system as it is. The modeller applies methods and evaluates interventions. Distinguish three kinds of assumption:

| Kind | Example | Location |
|---|---|---|
| State | Current close rate is estimated at 25% | Register |
| Method | Throughput calculation or selected ramp policy | Versioned method definition, explained beside calculations |
| Intervention | Explore a 10% relative close-rate increase | Modeller scenario |

A hypothetical business configuration can be a separately labeled exploratory baseline. Never overwrite an observed-state register with the desired outcome of an intervention, or validate a proposal against itself.

## 6. Assisted collection design

Each major value supports four routes: enter a known total; build it from components; use a labeled estimate/default; map it from a file. All routes resolve to the same defined concept and preserve their basis.

| Group | Assistance | Immediate value |
|---|---|---|
| Territories and people | Capture coverage units, filled assignments, vacancies, start dates, and staffing separately | Explain why territory count, payroll, and productive capacity differ |
| Transaction value | Direct entry or revenue divided by corresponding contracts | Surface population and period differences without forcing equality |
| Compensation | Salary-plus-load build or fully loaded total | Explain included costs and possible overlap with support overhead |
| Travel | Annual total or trip-frequency and trip-cost build | Reveal frequency versus unit-cost drivers; distinguish days from nights |
| Mechanics | Define opportunity entry, exit, population, and period | Identify incompatible cycle and close-rate measures |
| Overhead/marketing | Total first, detail progressively allocated | Show assigned and unassigned spending while preserving the total |

Example prompt: “$25 million across 755 contracts implies $33,113 per contract. The selected model value is $75,000. Are these different scopes, a deliberate reference assumption, or values you want to reconcile?” Offer keep-with-note, select-derived-value, or split-scope actions.

Descriptions should explain what is included, what is excluded, why the model needs the value, and what it affects. Replace long static instructions with concise guidance and expandable detail. Preserve original wording separately where required by the as-is contract.

### Collection routes

- Executive: totals and estimates, then consequential detail.
- Finance: reporting periods and expense categories, then mapping to operating drivers.
- Sales operations: assignments, opportunities, conversion, and timing.
- File-assisted: proposed mappings, units, scope, and period, reviewed before application.

Routes populate one register, not separate models. Retain drafts and allow users to switch routes. Imported observations remain staged until accepted; mapping must not fabricate missing values or treat an unrecognized expense as zero.

## 7. Value produced during entry

### A. Live operating and economic view

Display supported resource totals, capacity, cost composition, and per-unit economics as inputs arrive. Every output states whether it is complete, partial, or unavailable. Offer an explicitly labeled illustrative estimate when required inputs are missing; do not display it as complete company operating income.

### B. Reconciliation and coverage

Compare a stated total with its allocated detail. If marketing is $3.7M and identified lines total $3.2M, retain $0.5M as unallocated within the total. Do not add it again or silently replace the stated total. Allocation coverage measures classification progress, not economic validity.

### C. Sensitivity-guided collection

Ask for the uncertain inputs most consequential to the active comparison. Use user-supplied plausible ranges or clearly labeled illustrative ranges. Recompute the comparison across those ranges, respecting constraints. Flag when the ranking changes. Do not turn a percentage sensitivity into a confidence probability.

### D. Reusable learning

Attach a source note, definition, period, and basis to each value. Reuse a profile in later periods or scopes through explicit copy/version operations. Ask users to reconfirm stale values instead of silently labeling copied assumptions as current actuals.

## 8. Proposed state and persistence contract

This section specifies intended behavior; a database and production storage service have not been selected here.

| Object | Required content |
|---|---|
| Business scope | Organization/profile ID, channel/offering/customer population, currency, period, owner |
| Source observation | Source ID, value, unit, scope, period, supporting reference, capture time, verification status |
| Register draft | Stable input keys, candidate values, active selections, notes, unresolved questions, revision |
| Register version | Immutable snapshot of selected state values and their basis |
| Method version | Formula/rule definitions, policies, dependencies, units, model version |
| Scenario revision | Register version reference, method version, explicit intervention changes, horizon, costs, timing, constraints |
| Calculation run | Exact input/version references, outputs, completeness flags, checks, run timestamp |
| Recommendation record | Supporting run, rule/evidence basis, missing prerequisites, suggested action |

For a numerical input, store candidates and selection separately: a historical derived value can remain available beside a selected estimate. Source type (actual, derived, assumption, default), verification status (for example Finance-validated or unverified), and completeness (known/missing/not applicable) are separate dimensions.

Store missing as null, never numeric zero. A known zero is a valid supplied value. Preserve raw source units and explicit normalization. Keep currency, period, population, and cost-category coverage with the value. Do not assign an artificial confidence percentage because an input has a source label.

Drafts autosave with an expected revision to detect concurrent changes. A stale edit must produce a conflict or a reviewed merge, not silently overwrite newer input. Baseline/register publication creates a frozen version. Editing a published version creates a new draft/version; existing scenarios stay pinned unless explicitly rebased. Rebase shows a before/after change list and creates a new scenario revision.

Cache results by resolved inputs, method version, policies, and horizon. Editing a dependency invalidates affected cached outputs and recommendations. Preserve old calculation runs for reproducibility; never display them as results of a newly edited draft.

Proposed physical mapping: structured tables in Excel for the first workbook implementation; structured durable database records for the web application. Browser state may support interaction or recovery but must not be the sole durable store of saved web profiles. GitHub holds specifications, schemas, code, tests, and synthetic examples—not live customer entries. Production access control must isolate each organization's profiles and supporting files.

## 9. Implications for scenario planning

The register supplies the starting state; scenario interventions are explicit deltas or replacements. Each intervention identifies the field, unit, relative/absolute/percentage-point operation, timing, and cost. Changes do not mutate the register.

Direct totals and component builds require one active control path. If a travel total override is active, a change in trip frequency must request switching to the component method or disclose that it cannot affect the active cost. Never count total and component savings twice.

Separate method experiments from operating interventions. An alternative ramp calculation is a policy/method comparison; a program reducing ramp duration is an intervention. Display that distinction in comparisons.

Compare on a consistent scope and horizon. Include implementation costs when supplied, and clearly identify their absence when not supplied. Equal-percentage exploration is useful; investment and feasibility comparisons require additional evidence. Do not rank options by an invented difficulty score.

## 10. Outputs and recommendations

Each comparison should explain what changed, the active values and their basis, transmission through operating and cost relationships, financial bridge, constraints, required missing inputs, and assumptions capable of changing the conclusion.

Separate three levels of output:

1. Arithmetic implication: what the specified rules calculate.
2. Conditional decision insight: which alternative performs better under selected costs, timing, and constraints.
3. Intervention recommendation: requires evidence connecting an action to achievable change, effort, timing, and dependencies.

During collection, prefer helpful next actions: clarify population; allocate remaining expense; inspect a source; compare a range; investigate an influential constraint. A low close rate alone does not identify its cause. Do not recommend training merely because the close-rate field is low.

User-entered hypothetical scenarios cannot become observed benchmark data. Benchmarking is optional context and feasibility evidence, not a prerequisite to exploration.

## 11. Differentiation to pursue

The intended distinction is understanding created during collection: users assemble an explainable economic representation, not just receive a velocity number. Proposed differentiators are build-or-enter inputs, consistent state/method/intervention separation, live financial consequences, reconciliation assistance, decision-sensitive collection, and reusable versioned profiles.

These are product-design aims, not claims that no competitor offers them. Earlier comparisons identified meaningful overlap with enterprise planning products. Avoid unsupported exclusivity or historical-descent claims.

## 12. Implementation sequence and acceptance examples

First implement build-or-enter selection, provenance, missing/zero treatment, and totals/detail reconciliation. Then draft persistence and immutable register versions, followed by scenario linkage, dependency invalidation, and explanation. Add sensitivity-guided collection after deterministic results and comparisons are reliable.

| Acceptance example | Expected result |
|---|---|
| Historical average differs from selected reference | Retain both; explain scope/basis; never silently overwrite |
| Required marketing input unknown | Operating income marked incomplete/unavailable, not complete at lower expense |
| Marketing explicitly zero | Zero accepted with status preserved |
| Stated total exceeds detail | Difference shown as unallocated, total counted once |
| Direct travel override active | Component changes do not silently affect it; switching method is explicit |
| Vacant territory entered | No automatic employed person or payroll created |
| Intervention entered | Appears in modeller; register snapshot unchanged |
| Register edited after scenario saved | Saved scenario remains on old version until explicit rebase |
| Two edits race | Revision conflict surfaced instead of lost update |
| Dependency changes | Derived values update and old results/recommendations marked stale |
| Assumption range reverses ranking | Show conditional ranking and request better information |
| Scenario result shared or exported | Includes register/method/scenario versions, scope, period, and completeness |

These are requirements to implement and test, not assertions of existing coverage.

## 13. Integration notes and unresolved choices

Choose the target repository and branch before adding this document. In the register/modeller project, link this as supporting evolution design beneath `docs/MODEL.md`; keep protected source and original arithmetic untouched. In the SMEM engine project, map the proposed state records to actual APIs after inspecting code. Do not claim schema parity based on similar names alone.

Open implementation choices: physical database and identity service; collaboration model; exact import formats; which range questions to ask first; initial operating policies; handling of incomplete draft financial outputs; and relationship between the two repositories. These choices do not prevent preserving the semantic contracts above.

Suggested documentation commit scope: this handoff plus a link from the chosen project's documentation index. No calculation changes are implied. Follow that repository's required checks and commit format before making a commit.

## Sources and verification boundary

- Original workbook and user-supplied Data Entry table examined in this conversation.
- User-adopted October 24 reassessment and subsequent assisted-entry discussion.
- Local working specification: `Commercial_Effectiveness_Specification_V1.md`, created October 24.
- https://github.com/Hokies92/s-m-productivity-model-/blob/main/docs/MODEL.md — inspected blob `a0e45fae48df458c32e4e3c483df80f6eb055ba2`.
- https://github.com/Hokies92/s-m-productivity-model-/blob/main/CONTRIBUTING.md — inspected blob `d0b5d08f8ff35430288ea03aad90307f6cd3be96`.
- https://github.com/Hokies92/s-m-productivity-model-/blob/main/README.md — inspected blob `749d73540718c90faec5bdfac0d84157a5eff467`.
- https://github.com/Hokies92/sales-marketing-effectiveness-model/blob/main/README.md — inspected blob `fab096596bbfb1a456bc59e64da7621de991916b`.
- https://github.com/Hokies92/sales-marketing-effectiveness-model/blob/main/docs/spec/business_logic_v1.md — inspected blob `70c3165b850f23851e3910d3cadfd5cf747012b6`.

No code tests or workbook recalculation were performed for this documentation-only handoff. Repository status is attributed to inspected documentation; authorship of existing commits is not inferred.
