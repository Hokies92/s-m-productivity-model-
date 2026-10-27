# Commercial Model Project Charter

## Instructions, canonical foundation, file rules, and GitHub controls

Owner: Scott Santucci / Growth Enablement LLC  
Date: October 26, 2026  
Status: User-directed working charter; ready for project integration. Controls specified here are requirements, not claims that GitHub settings or code have already been configured.

## 1. Mission and immediate priority

Long-term mission: create a differentiated commercial model supporting the scenario exploration, financial reasoning, assisted collection, decision support, visualization, web interfaces, and eventual intelligence envisioned in this session.

FIRST GATE: faithfully reproduce the existing model's purpose and functionality in a modern, usable Excel implementation. Improve the experience and maintainability without sacrificing the original calculations, scenarios, financial outputs, diagnostics, or explanatory depth.

This is a modernization of a functioning economic model, not permission to replace its logic with conventional revenue-operations practices. Long-term architecture must accommodate evolution; speculative platform features must not displace completion of Gate 1.

Gate sequence:

| Stage | Required outcome |
|---|---|
| Gate 1A: faithful core | Original behavior reproduced; modern data entry, workflow, presentation, scenarios, and explanations verified in Excel |
| Gate 1B: controlled delivery | Versioned export plus bounded web input/custom-output demonstration, using the same approved calculation contract |
| Gate 1 acceptance | Owner accepts both parts with evidence; frozen release becomes the foundation for evolution |
| Gate 2: evolution | Broader operating relationships, intervention economics, and state architecture added as versioned extensions |
| Later gates | Production web delivery, optimization, intelligence, governed benchmarking, and validated differentiation |

Gate 1B is part of Gate 1, not an excuse to defer the user's export/web requirements. It may use a bounded demonstrator rather than a production multitenant service. Gate 1 cannot be called passed on workbook parity alone.

## 2. Canonical foundation

### Purpose

Compare commercial investment choices—especially adding selling resources versus improving existing capacity—by carrying operating assumptions through costs and a pro forma income statement to operating income, then explaining obstacles to achieving improvements.

### Functional chain that must survive modernization

Orientation → Data Entry → Performance Breakdown → Financial Impact → Scenario Diagnostic.

Preserve all original data groups and supporting cost detail. Preserve individual scenarios for quantity, close rate, cycle, and transaction value; preserve combined scenarios and their links to the individual changes. A user must be able to follow each output back to the active values and the rules that used them.

### Economic relationships

The original computes opportunity throughput from concurrent opportunity capacity and cycle length, converts throughput into successful transactions, applies transaction value, and scales by territories. It then applies direct sales costs, overhead, marketing, cost of revenue, R&D, and G&A to reach operating income.

The original's territory quantity is not silently redefined as employed people. The original capacity concept is not silently redefined as labor hours. New definitions belong to explicit extensions.

The model permits historical information, estimates, assumptions, and illustrative defaults. These are legitimate inputs. Distinguish source, verification, active selection, and missingness. Zero and unknown are different states.

### Authority and interpretation

Latest explicit user decisions govern project scope and acceptance. Original artifacts establish historical behavior. Confirmed author intent explains meaning. `docs/MODEL.md` is the single current interpretive statement. Mathematical inference and unconfirmed interpretations must be labeled.

When implementation and source disagree, record the disagreement; do not silently change source to fit implementation. When documents conflict, correct or archive the subordinate document. No second competing canonical model statement is permitted.

At the time of this charter, the inspected `Hokies92/s-m-productivity-model-/docs/MODEL.md` is the relevant canonical statement. A second repository, `Hokies92/sales-marketing-effectiveness-model`, follows a different implementation path. Before a write, resolve the selected repository and branch. Never mix their test evidence, baseline policies, or release statuses.

### Known interpretation constraints

- The $87,750 applied salary versus $116,850 entry-sheet calculation is recorded in the canonical statement as a deliberate author estimate. Preserve the distinction and show the applied value; do not automatically link them and call that faithful reproduction.
- The $75,000 transaction reference and $25M/755 historical derivation may have different bases. Preserve both and make their usage understandable.
- Original ramp and commission treatments must be reproduced for parity. Unresolved intent is recorded, not guessed. Alternative policies require separate model versions and change decisions.
- A result can be computationally correct yet incomplete or economically unsuitable. These are different properties and must not share a single PASS label.

## 3. Agent instructions — content for AGENTS.md

The following is the operative instruction set for any human or AI contributor:

1. Read `docs/MODEL.md`, this charter, `CONTRIBUTING.md`, applicable nested `AGENTS.md`, and current gate requirements before editing. Inspect repository state and existing work before making changes.
2. State the requirement being served, the intended behavior change, and the evidence needed. Use the existing project vocabulary: salesperson/salespeople; customer; commercial environment. Preserve verbatim historical quotations separately.
3. Prioritize Gate 1. Implement modern workflow and presentation while preserving the parity contract. Do not redesign economic meaning under the label of cleanup.
4. Keep original artifacts and as-is oracle protected. Never overwrite reference evidence. No corrections to expected values solely to make new code pass.
5. Expose entered, calculated, and applied values where they differ. Every editable input and control must either affect a defined result/workflow or be clearly marked informational. Do not display inert controls as active drivers.
6. Keep unknown distinct from zero. Missing required costs block complete-looking operating income; available subtotals may remain visible with their status.
7. Keep baseline state separate from interventions. Scenario edits cannot mutate a saved baseline or another scenario. Explain method changes separately from operating changes.
8. Prefer transparent native Excel formulas and structured inputs for core calculations. Use Python where it improves extraction, generation, parity, export, or testing. Do not create a second undocumented numerical truth.
9. Use macros/scripts only for a defined workflow benefit. Core calculations must work without enabled macros. Never require “enable all macros.” Do not automate external writes without an explicit user action and documented destination.
10. Verify recalculation and user workflows in supported Excel. A Python result, formula string, cached workbook value, screenshot, or LibreOffice result alone is not Excel acceptance.
11. Preserve detailed explanations through progressive disclosure, not deletion. Visual polish and explanatory completeness are both required.
12. Follow protected-branch, PR, evidence, and release rules. Never claim a commit, test, deployed capability, or gate acceptance that did not occur.
13. Record uncertainties without blocking independent authorized work. Reserve owner acceptance for a concrete reviewable candidate, not routine reversible implementation choices.

## 4. Gate 1 capability requirements

| ID | Requirement | Evidence required |
|---|---|---|
| G1-01 | Preserve original purpose, functional chain, scenario set, diagnostic linkage, and output definitions | Source-to-modern function map plus owner review |
| G1-02 | Reproduce original numeric behavior | Full mapped parity results for all reference formula outputs; seeded and nondefault cases |
| G1-03 | Modern, assisted Excel entry | Enter/build/estimate routes where applicable; validation; units; expandable descriptions; active-value trace |
| G1-04 | Complete and partial input handling | Blank, partial, zero, invalid, and complete cases; required missing inputs cannot disappear into profit |
| G1-05 | Modern presentation | Reviewed workbook screenshots/renders and native Excel walkthrough; readable at normal zoom and in export |
| G1-06 | Calculation illumination | Rule in words; input-to-output trace; visible method and source references; explanation for selected scenario |
| G1-07 | Improved scenario workflow | Create/copy/name/reset/compare scenarios; preserve original presets; baseline isolation and saved-state tests |
| G1-08 | Portable visualization export | JSON/CSV contract, schema, units, version IDs, source selections, completeness, and round-trip/consumer tests |
| G1-09 | Bounded web delivery | Demonstrate input submission, versioned calculation, and selected custom output without distributing model implementation |
| G1-10 | Optional workflow automation | Reviewed scripts/macros where beneficial; macro-disabled fallback; platform-specific behavior documented |
| G1-11 | Repeatable builds and verification | Pinned environment, source hashes, build manifest, reproducible numerical results, CI checks |
| G1-12 | Formal acceptance and release | Evidence pack tied to commit and artifact hashes; owner decision; immutable release tag |

Optional macros are not an acceptance requirement in themselves. Useful, verified workflow capability is the requirement. Gate 1 does not require production AI, benchmark infrastructure, new causal relationships, or full opportunity-cohort modeling.

## 5. Modern Excel and presentation standards

Use tables, meaningful names, consistent formats, input validation, conditional formatting, clear navigation, freeze panes, sheet protection against accidental edits, and print/export layouts where they improve use. Consider LET/LAMBDA, dynamic arrays, Power Query, and other features only after specifying supported Excel editions and fallbacks. No feature earns inclusion solely because it is modern.

Proposed primary target: current Microsoft 365 desktop Excel on Windows. Record the exact tested version/build. Mac and browser Excel have explicit supported/limited/not-tested statuses; do not imply parity without verification. Do not impose a Python-in-Excel subscription or optional add-in on core arithmetic.

Core workbook calculations remain inspectable native Excel formulas with a documented mapping to the reference logic. Python may generate the workbook and serve as an independent parity oracle. Generated artifacts must not become an undocumented source of business rules.

Presentation: conclusion-led titles, restrained palette, clear grid, exact alignment, generous whitespace, direct labels, legible financial detail, consistent hierarchy. Use the agreed McKinsey exhibit discipline, Tufte information density, and Apple finish as review criteria, not as substitute evidence. Do not shrink text or remove needed explanations to make a page look simple.

Potential automations: duplicate scenario; restore defaults; show change list; trace calculation; generate comparison report; export selected results. Provide confirmation/undo where a workflow replaces user work. Workbook sheet protection is not a confidentiality boundary.

## 6. Data, scenarios, and output contracts

Keep original entry groups and all cost categories. Retain supporting observations alongside selected assumptions. Direct totals and detail builds have one active control path so changes are never counted twice.

Separate state assumptions in the register, method definitions in the calculation specification, and interventions in the modeller. A saved scenario references an immutable register version and method version. Draft changes create new versions and invalidate affected cached results. No automatic rebase of previously saved comparisons.

Required identifiers: business scope, period, currency, model version, schema version, register version, scenario revision, run ID, and artifact build/commit reference. Every exported metric has a definition and unit. Unknown values remain null with status; exports must not convert them to zero.

Custom output presents the selected scenarios, active assumptions, financial bridge, completeness, and relevant diagnostics. Do not present unsupported recommended actions as causal findings. Proposals remain distinct from observations and must never enter benchmarks as actual results.

## 7. Web and external visualization boundary

Design explicit interfaces: input schema → validation → approved calculation service → output schema → selected visualization/report. Use the same versioned rules and test cases as Excel; no separately invented browser arithmetic.

For controlled delivery, retain proprietary rules server-side. Browser clients receive only approved inputs, results, and necessary explanatory information. Inspect browser bundles, API responses, exports, and error messages for accidental distribution of source formulas or unrestricted internal state. A downloadable workbook cannot reliably conceal its logic; public workbook distribution and private server calculation are separate delivery choices.

Gate 1B demonstration must show rejection of invalid inputs, parity for agreed cases, selectable output, and no calculation implementation shipped to the browser. If data is saved, demonstrate access control and isolation; otherwise label the demonstrator as synthetic-data/no-persistence. Production hosting, retention, authorization, and capacity testing belong to the production delivery gate.

## 8. Project files and ownership

Adapt to existing paths rather than creating duplicate competing structures. Each requirement must map to a file and a verification mechanism.

| File or directory | Role and rule |
|---|---|
| `AGENTS.md` | Contributor instructions from §3; nested rules may specialize, never weaken protected-source and gate requirements |
| `CONTRIBUTING.md` | Branch, PR, review, check, and release process |
| `docs/MODEL.md` | Single canonical model interpretation; original versus evolution clearly separated |
| `docs/PROJECT_CHARTER.md` | This charter and gate priority |
| `docs/GATE1_ACCEPTANCE.md` | Requirement checklist, evidence links, unresolved items, owner acceptance record |
| `docs/INTENT_LEDGER.md` | Source/confirmed intent/open interpretation, decision date, supporting evidence |
| `docs/decisions/ADR-*.md` | Append-only material architectural/model decisions; superseding records reference prior decision |
| `docs/COMPATIBILITY.md` | Supported Excel platforms, tested builds, fallbacks, macro/script behavior |
| `source/` | Original workbook/formula evidence, preserved bytes; changes rejected by CI |
| `reference/manifest.json` | Artifact hashes, source identity, extraction tool versions, mapping coverage |
| `spec/` or `schemas/` | Versioned input/output/state contracts and metric definitions |
| `src/` | Maintained implementations; preserved as-is oracle isolated from extensions |
| `tools/` | Repeatable builders, extraction, export, recalculation, and verification tools |
| `tests/` | Source protection, parity, input completeness, scenario isolation, export and workflow tests |
| `tests/fixtures/` | Immutable expected reference cases; synthetic data; independent derivation documented |
| `workbook/` | Release/candidate workbook plus manifest; generated status explicit |
| `automation/` | Reviewable VBA/Office Script sources and instructions; no untracked embedded-only logic |
| `exports/examples/` | Synthetic sample payloads and consumer examples, never real client records |
| `docs/archive/` | Superseded interpretations with clear status and current replacement link |
| `.github/workflows/` | Protected required CI; CI modifications reviewed as engineering controls |
| `.github/CODEOWNERS` | Review owners for model, source, engine, schemas, automation, and releases |
| `.github/pull_request_template.md` | Required evidence and change declarations |
| `.gitignore`, `.gitattributes` | Exclude credentials, private datasets, temporary/cache files; document binary storage policy |
| dependency lock/config files | Pinned reproducible toolchain and declared runtime support |
| `CHANGELOG.md` | User-visible capability and model-behavior changes per release |

Store business customer data in the approved data store, not the Git repository. Preserve source originals in their designated protected location; do not sanitize the historical source by overwriting it. Exports intended for examples use synthetic data.

Generated Excel binaries require the generator source and a manifest linking inputs, model version, commit, checks, and workbook SHA-256. Never hand-edit a generated workbook and silently overwrite its generator output. If a native-Excel finishing step is required, record it and retain a reproducible or explicitly documented process. Use LFS or release assets when binary size warrants it; avoid committing repetitive intermediates.

## 9. STRICT GitHub change controls

### Repository and branch controls

1. Resolve one target repository before any write. No automatic cross-repository copying, branch switching, or merging of competing engines.
2. Protect `main`, release branches/tags, and any accepted as-is baseline with repository rulesets. Require pull requests; prohibit force pushes and deletion of protected refs. Apply controls to administrators; no routine bypass.
3. Use short-lived `modernize/<issue>-<description>`, `fix/<issue>-<description>`, or `docs/<issue>-<description>` branches. Existing `evolution` remains an integration line, not a substitute for PR review. Branches targeting evolution receive equivalent required checks.
4. Never commit directly to a protected integration branch. Never move an accepted tag. Use a new candidate/release for every revision.

### Change and review controls

5. Every change links to a requirement/issue, explains user-visible behavior, and names the invariant it serves. Separate presentation/workflow modernization from economic-method changes.
6. Model meaning, original behavior, accounting/financial policy, or fixture changes require explicit owner review and a decision record. Proposed extensions do not replace as-is defaults.
7. Require at least one independent human approval on every PR and appropriate CODEOWNER approval. The author or AI agent cannot approve its own work. Owner approval is additionally required for model-semantic changes and gate acceptance.
8. Dismiss approvals when new commits are pushed; require review of the latest changes, resolved discussions, and passing checks on the exact merge candidate. Re-run checks after conflict resolution.
9. Do not weaken a test, tolerance, reference value, or rubric to turn a failure green. Expected-value changes require independent evidence, a stated rationale, and model-owner approval.
10. Use signed commits/tags where the organization can enforce them. Verify attribution; an assistant must not impersonate the owner. Squash reviewed changes or use the repository's documented merge strategy; retain the PR audit trail.

### Required checks

11. CI runs from a clean environment on PRs and protected integration branches: source checksums, reference parity, missing/zero behavior, scenario isolation, relevant workbook formulas/features, export schema compatibility, language checks, lint/types, and affected unit/integration tests.
12. Pin dependencies and CI action versions; scan dependencies and credentials; grant workflow tokens minimal permissions. Untrusted PR content receives no production secrets or write token.
13. Excel-native verification produces an evidence artifact tied to the exact candidate. When native Excel is unavailable, leave its check pending/blocked; never substitute a cached-value or alternate-engine pass. Human workflow and visual checks are separately recorded and linked.
14. Unit-test coverage percentages and rubric scores cannot substitute for required business cases. No unexecuted test is reported as passed. Distinguish CI-automated, native-Excel-verified, manually reviewed, proposed, failed, and blocked.

### Release and rollback

15. Release from an approved exact commit. Attach workbook/export schemas, manifests, checksums, compatibility statement, test evidence, known limitations, changelog, and owner gate decision.
16. Use semantic versioning. Breaking input/output or model-behavior changes require a major version. Compatible capabilities use a minor version; backward-compatible implementation fixes use a patch. Original-compatibility mode remains explicitly identified and testable.
17. Never overwrite published binaries; ship a new version. A rollback redeploys a known approved artifact or creates a reviewed revert commit. Never rewrite published history to hide a regression.
18. Schema migrations are versioned and tested with backups/rollback or documented forward recovery. Users' saved baseline/scenario records must not silently change meaning after an engine upgrade.
19. Record who accepted a candidate, what was accepted, artifact/commit hashes, date, and any explicit limitations. CI may recommend readiness; only the owner can accept Gate 1.

If branch-protection/reviewer capabilities are unavailable for the repository's plan or ownership model, report the exact unenforced control. Do not claim commercial-grade enforcement from a Markdown policy or local hook alone.

### Required PR body

```text
Requirement / issue:
Purpose and before/after behavior:
Invariant served:
Changed files and generated artifacts:
Model semantics changed? If yes, decision record and owner review:
Original parity evidence:
Partial-input and zero-input evidence:
Excel platform/build and native workflow evidence:
Visual review:
Export/web impact:
Tests executed, results, and blocked checks:
Compatibility / migration / rollback:
Known limitations:
Deliberately untouched:
```

### Commit format

```text
<type>(<scope>): <concrete change>

Requirement: <gate/issue ID>
Invariant: <canonical requirement; or evolution>
Changed: <artifacts>
Left: <protected/unchanged artifacts and reason>
Evidence: <test/run or PR reference>
```

Keep meaningful commits independently understandable. Tests appropriate to the change pass before commit; required full checks pass before merge. Do not create misleading “verified” commits when native verification is still blocked.

## 10. Gate 1 evidence and acceptance procedure

1. Freeze the source manifest and exact reference oracle/fixtures. Map every functional element and numeric output. Resolve coverage counts from the artifacts; do not substitute 48 selected outputs for full formula-cell coverage.
2. Produce a modern candidate without changing original semantics. Record mapping from source cells to stable input/output IDs and modern locations.
3. Run parity over the original example plus representative nondefault combinations, preserving original distinctions in input versus applied values. Integer/count/status equality is exact; numeric tolerances are explicitly defined per unit and magnitude before testing. No universal loose percentage tolerance.
4. Change inputs in Excel, force recalculation, save, reopen, and inspect results. Include blank/partial/zero entries; resets; copy/compare scenarios; intended protection and navigation; macro-disabled behavior.
5. Review readability, detailed explanations, print/PDF/report layouts, and scenario comparison workflows. Export versioned results and demonstrate the controlled web boundary on the same reference cases.
6. Present the evidence pack and candidate to the owner. Gate status stays OPEN until acceptance is recorded. Once accepted, tag the exact commit and retain its artifacts as the evolution baseline.

Known blocking issues in the inspected canonical statement—partial inputs suppressing required expense and an inert displayed value—must be resolved in the modern implementation without rewriting the original arithmetic. Any output limitation must be explicit; preserve exploratory usefulness without implying complete financial results.

## 11. Long-term differentiation, held behind the gate

Preserve the integrated economic comparison, operational detail, and diagnostic explanation. Future differentiation can come from assisted collection, explicit state, feasible intervention comparison, financial bridges, controlled custom output, and evidence-informed scenarios. Competitor capability claims require current evidence; no blanket “nobody else does this” claims.

Do not add production AI, a benchmark database, new ramp defaults, generalized demand models, full revenue recognition, or advanced optimization to the Gate 1 critical path unless required to preserve current functionality. Keep interfaces extensible while proving the existing model first.

## 12. Implementation status and source basis

This charter was created as documentation. It does not modify a workbook, repository, GitHub ruleset, CI workflow, or release. No gate is certified by its creation.

Basis: the user's October 26 gate instruction; original workbook and Data Entry discussion; adopted reassessment; local specification and assisted-entry handoff; `Hokies92/s-m-productivity-model-/docs/MODEL.md` inspected October 26, blob `a0e45fae48df458c32e4e3c483df80f6eb055ba2`; previously inspected CONTRIBUTING and the second repository's business-logic specification. Earlier local proposals are subordinate wherever the user's gate priority or canonical interpretation supersedes them.

Next implementation action: resolve the target repository, integrate these instructions into its canonical documents without duplication, inventory existing tests/artifacts against G1-01 through G1-12, and implement the missing Gate 1 capabilities on a review branch.
