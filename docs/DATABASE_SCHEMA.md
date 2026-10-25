# Database Schema: Register and Modeller

Status: **V1, 2026-10-24; split into two schemas 2026-10-25** per [MODEL.md §4](MODEL.md). The **register** (`schema.sql`, `seed.sql`) holds state assumptions: the client's beliefs about the system as it is. The **modeller** (`modeller.sql`) holds method versions and intervention hypotheses (scenarios). The two never share a foreign key: the modeller refers to the register by identifiers only, so the register stays valid with the modeller absent and the baseline can never depend on a hypothesis. Tested in `tests/test_schema.py`.

```python
from sales_capacity_model.db import create, create_modeller
reg = create("register.db")          # register: schema + reference data
mod = create_modeller("modeller.db") # modeller: levers, method versions, default scenarios
```

© 2000–2026 Growth Enablement. All rights reserved.

## Design in one paragraph

Raw facts (CRM opportunities, pipeline snapshots, ledger lines, roster, territory plan, events) are stored as **observations**. Every **state** value the model reasons with is an **assumption** in the register: one field, about one entity, in one scope, in one baseline version. Each assumption keeps every **value** ever asserted for it, append-only, with its basis, owner, range, lineage and evidence. **Tests** record which values they used, so a failure points to its candidate set. **Scenarios** live in the modeller, as multipliers on levers applied to a frozen register version; they never write back. The model's own structure is data too: the **field catalog** tags every field with its element type and Meadows leverage point, and **causal links** record how fields drive each other.

## Entity relationships

```mermaid
erDiagram
    CLIENT ||--o{ ENGAGEMENT : has
    ENGAGEMENT ||--o{ BASELINE_VERSION : versions
    ENGAGEMENT ||--o{ CONTRIBUTOR : "data owners"
    ENGAGEMENT ||--o{ REQUEST : "collection steps"
    REQUEST ||--o{ SOURCE_DOCUMENT : returns
    ENGAGEMENT ||--o{ ENTITY : contains
    ENTITY ||--o| TERRITORY : "is a"
    ENTITY ||--o| SALESPERSON : "is a"
    ENTITY ||--o| ASSIGNMENT : "is a"
    ENTITY ||--o| SEGMENT : "is a"
    ENTITY ||--o| RULE : "is a"
    TERRITORY ||--o{ ASSIGNMENT : "covered by"
    SALESPERSON ||--o{ ASSIGNMENT : covers
    SEGMENT ||--o{ TERRITORY : groups
    ENTITY ||--o{ EVENT : "dated facts"
    TERRITORY ||--o{ OPPORTUNITY : "flows through"
    SALESPERSON ||--o{ OPPORTUNITY : works
    SALESPERSON ||--o{ PIPELINE_SNAPSHOT : holds
    SOURCE_DOCUMENT ||--o{ OPPORTUNITY : "imported from"
    SOURCE_DOCUMENT ||--o{ FINANCIAL_LINE : "imported from"
    BASELINE_VERSION ||--o{ ASSUMPTION : holds
    FIELD ||--o{ ASSUMPTION : "defines"
    ENTITY ||--o{ ASSUMPTION : "is about"
    FIELD ||--o{ FIELD_DEFINITION : "versioned meaning"
    FIELD ||--o{ CAUSAL_LINK : drives
    ASSUMPTION ||--o{ ASSUMPTION_VALUE : "history (append-only)"
    ASSUMPTION_VALUE ||--o{ ASSUMPTION_INPUT : "built from"
    ASSUMPTION_VALUE ||--o{ ASSUMPTION_EVIDENCE : "supported by"
    ASSUMPTION_VALUE ||--o{ ASSUMPTION_VALIDATION : "Finance validates"
    ASSUMPTION ||--o{ ASSUMPTION_TEST : "falsified by"
    TEST_DEFINITION ||--o{ TEST_MEMBER : "involves fields"
    TEST_DEFINITION ||--o{ TEST_RUN : runs
    TEST_RUN ||--o{ TEST_RUN_INPUT : "candidate set"
    TEST_RUN ||--o{ RESOLUTION : "fixed, explained, accepted"
    ASSUMPTION ||--o{ ACCURACY_RECORD : "assumed vs observed"
```

## Tables by layer

| Layer | Tables | Holds |
|---|---|---|
| 1. Tenancy, scope, versions | `client`, `engagement`, `contributor`, `baseline_version` | Scope, period, currency, revenue basis; data owners by role; draft → working → in review → signed |
| 2. Collection | `collection_step`, `request`, `source_document` | The 11-step sequence, requests sent to owners, uploaded files with content hashes |
| 3. Meaning | `field`, `field_definition`, `causal_link` | What can be known, its unit, level, element type, leverage point; versioned definitions with report recipes; how fields drive each other |
| 4. System entities | `entity` (supertype), `territory`, `salesperson`, `assignment`, `segment`, `rule`, `event` | Territory design and staffing as separate entities joined only by assignment; dated vacancy stages, hires, departures |
| 5. Observations | `opportunity`, `pipeline_snapshot`, `financial_line` | Raw imports kept so estimators can recompute |
| 6. Assumption ledger | `assumption`, `assumption_value`, `assumption_input`, `assumption_evidence`, `assumption_validation`, `assumption_test` | Every claim, its history, lineage, evidence, Finance validation and falsification test |
| 7. Tests | `test_definition`, `test_member`, `engagement_test_config`, `test_run`, `test_run_input`, `resolution` | Test library, which fields each test involves, per-engagement tolerances, every run with the exact values used, and how failures were resolved |
| 8. Track record | `accuracy_record` | Assumed vs observed per period |

## Rules enforced by the database

| Rule | How |
|---|---|
| History is never overwritten | Triggers block UPDATE and DELETE on values, events, test runs, resolutions, accuracy records |
| Signed baselines are frozen | Triggers block changes to a signed baseline and new assumptions or values in it |
| Every value declares its basis | `basis` is required: validated actual, calculated estimate, reference value, judgment |
| Reference values name their context | CHECK: `reference_context` required for reference values |
| Estimates and judgments carry a range | CHECK: low and high required for reference values and judgments; value must sit inside the range |
| Leadership beliefs are captured before data | Trigger: a sealed belief must be a judgment and the first value for its slot |
| Only Finance validates | Trigger on `assumption_validation` checks the contributor's role |
| Salespeople are pseudonymous | `salesperson` has a pseudonym (hashed HR ID with a per-engagement salt) and no name column; contributors and salespeople are separate tables |
| Open territories are visible | A territory with no current assignment is open; `v_territory_assignment_share` |

## Views for the data module's outputs

| View | Answers |
|---|---|
| `v_current_value` | The current value of every assumption, with basis and whether Finance validated it |
| `v_perception_gap` | Sealed leadership belief vs current evidence-based value, per field and entity |
| `v_territory_assignment_share` | Which salesperson covers which territory, with share of time; open territories |
| `v_vacancy_stages` | Dates of each stage of each vacancy, for approval-latency cost |
| `v_candidate_set` | For every unresolved failed test, the values that could be wrong |
| `v_confidence_profile` | Share of current values by basis, per baseline |

## Notes

- **V1 is SQLite**; the SQL is standard enough to move to PostgreSQL with type changes (`TEXT` dates to `DATE`, `REAL` to `NUMERIC`), adding row-level security per client.
- **Evidence files** live outside the database (file storage), referenced by `source_document.content_hash`.
- **Derived values are not stored as truth:** calculated estimates are stored as assumption values with their inputs, so they can always be recomputed and audited; scenario results are a modeller cache keyed by scenario, method version and register version.
- **Structural what-ifs** (adding territories or roles) are deferred with the territory and hiring scenarios; when they return they are modeller objects, not register entities.

## The modeller schema (`modeller.sql`)

| Table | Holds | Note |
|---|---|---|
| `lever` | A register field the modeller may scale, its direction, and how revenue responds (proportional, inverse, structural) | Refers to the register field by id, not by key |
| `method_version` | The chain as applied: unit of throughput and the rules in words | A method assumption, versioned |
| `scenario` | A named hypothesis and the question it answers | The original's four quality scenarios ship as defaults |
| `scenario_lever` | The multipliers: one row per lever per scenario | Adding a scenario is adding rows |
| `scenario_run` | Which scenario, with which method version, against which frozen register version | The three keys of any result |
| `scenario_run_result` | Cached metrics for a run | Never written to the register |

```mermaid
erDiagram
    LEVER ||--o{ SCENARIO_LEVER : scaled_by
    SCENARIO ||--o{ SCENARIO_LEVER : has
    SCENARIO ||--o{ SCENARIO_RUN : run_as
    METHOD_VERSION ||--o{ SCENARIO_RUN : applies
    SCENARIO_RUN ||--o{ SCENARIO_RUN_RESULT : produces
```
