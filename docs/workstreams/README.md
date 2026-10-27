# Workstream map and coordination plan

Owner: Scott Santucci. Working plan, October 27, 2026. The project charter and `docs/MODEL.md` govern; this map does not alter original formulas or certify the first gate.

**Goal:** make the original commercial model understandable and usable in a modern form; then evolve its capabilities with Scott's accumulated experience. First show the original can be faithfully modernized in Excel, with its scenarios and economic results intact. The proposed Gate 1 also includes a bounded visualization export and web input/custom-output demonstration, under the charter. Gate 1 remains open.

## Five focused workstreams

| Plan | Purpose | Near-term output | Owns the first draft of |
|---|---|---|---|
| [01 Understand the original](01-original-model.md) | Explain source behavior and author intent | Source-to-function map and intent ledger | Definitions, original behavior and reference examples |
| [02 Modernize the model](02-modern-excel.md) | Deliver a modern Excel reproduction | Reviewable workbook and parity evidence | Excel workbook, build and native-Excel workflow evidence |
| [03 Make it understandable](03-user-experience.md) | Help people enter data, compare and interpret scenarios | Guided entry and explanation designs tested with examples | Interface copy, usability and visual review |
| [04 Build the technical foundation](04-technical-foundation.md) | Keep calculations, saved state and exports consistent | Versioned contracts, checks and bounded delivery demonstration | Data contracts, Python verification and integration tests |
| [05 Capture and develop lessons](05-lessons-and-evolution.md) | Make Scott's lessons explicit and ready to evaluate | Evidence-linked lesson and idea register | Lesson capture and proposals for future capabilities |

The names identify areas of responsibility, not separate companies or separate models. No people are assigned to these roles yet. Scott owns business meaning and approves the milestone; the project coordinator manages handoffs and keeps this map current. Technical, workbook, experience and research leads are roles to be assigned, not implied hires.

## Order of work

| Sequence | Coordinated activity | Exit evidence |
|---|---|---|
| 1. Establish the reference | Stream 1 maps original behaviors; stream 4 identifies existing tests; stream 5 captures questions for Scott | Functional map, reference cases, known unknowns and existing evidence with sources |
| 2. Design the modern experience | Streams 2 and 3 design entry, scenarios and presentation against the reference; stream 4 defines shared input/output IDs | A reviewed workflow and traceable definitions; no unapproved formula changes |
| 3. Build and reconcile | Streams 2 and 4 implement and verify; stream 3 reviews understanding and visual quality | Candidate workbook and comparison evidence; incomplete inputs clearly identified |
| 4. Demonstrate connected outputs | Streams 3 and 4 show selected export and bounded web input/output using the approved logic | Same example produces consistent labeled results in Excel, export and demonstration |
| 5. Decide Gate 1 | Coordinator assembles evidence; Scott reviews the working candidate | Owner records pass or open issues; do not infer acceptance from code or tests |
| 6. Evolve | Stream 5 proposes the next additions; all affected streams assess them | Selected proposals with impact and acceptance criteria, implemented as versioned changes |

There are no assumed calendar dates. The coordinator adds estimates and owners only after the reference and current state are inventoried. Stream 5 can collect lessons throughout without making them unapproved Gate 1 behavior.

## Shared foundation and handoffs

The current source and `docs/MODEL.md` establish the reference interpretation. Each input/output in the shared mapping needs an ID, plain-language definition, unit, scope, original location, active value or source, and downstream outputs. An example case includes baseline values, scenario changes, expected operating and financial results, and source references. Stream 4 proposes versioned contracts from stream 1's definitions; streams 2 and 3 review them before use. Unresolved questions remain visible.

| Producer → consumer | Required handoff | Integration check |
|---|---|---|
| 1 → 2, 3, 4 | Source map, definitions, author-intent status and reference cases | Each original scenario and key output has an identified modern location and test |
| 3 → 2, 4 | Input labels, collection routes, explanation and scenario interaction design | Every editable control maps to one active input/rule; missing and zero remain distinct |
| 4 → 2, 3 | Versioned definitions, result/export formats, validation and status semantics | Excel, output view and export agree on units, source, model version and completeness |
| 2 → 1, 3, 4 | Workbook candidate, build ID, source mapping and outputs | Independent reference cases and end-to-end workflow reproduce expected results |
| 5 → 1–4 | Lesson/proposal record with evidence, impact and affected interfaces | Accepted changes are versioned; original compatibility remains reproducible |

## How we coordinate

1. Each stream maintains its own plan and names an accountable lead when assigned. Work items state purpose, inputs, output, dependency and acceptance evidence.
2. A shared decision log records the question, source evidence, Scott's decision where needed, affected workstreams, date and model version. Separate confirmed author intent from interpretation.
3. Before modifying a shared definition, scenario rule or export format, record the proposed change and its impact; owners of affected streams review it. Do not silently change the original reference.
4. At each integration checkpoint, run the same approved example from data entry through scenario calculation, income statement, explanation and export. Record exact versions and any failed or unavailable checks.
5. Publish a short status for each stream: next result, evidence, dependency/blocker, and decision needed. Status is updated at checkpoints, not inferred from a plan.
6. GitHub stores project files, decisions and reviewed changes. A workstream may have a separate conversation, but decisions and artifacts must be added to the shared project record. Follow CONTRIBUTING and the accepted branch/PR rules. The current charter and these plans are in a draft pull request until merged.

## First milestone checklist

- [ ] Original purpose, input groups, scenarios, financial outputs and diagnostics mapped with evidence.
- [ ] Existing workbook and reference tests inventoried; unresolved intent identified for Scott.
- [ ] Candidate supports guided entry and clear, complete or explicitly incomplete results.
- [ ] Original examples and representative changed inputs reconcile to the reference, with documented tolerances.
- [ ] Native Excel recalculation, save/reopen and scenario workflow verified on a named supported build.
- [ ] Presentation and explanatory detail reviewed by Scott against a working candidate.
- [ ] Export and a bounded web input/custom-output example use the same versioned calculation rules.
- [ ] Evidence pack identifies artifacts, versions, results, missing checks and limitations; Scott records acceptance.

See the [charter](../PROJECT_CHARTER.md) for detailed requirements G1-01 through G1-12. These are targets, not proof they are implemented. Verified capabilities and outstanding issues are tracked separately in the canonical model and evidence pack.
