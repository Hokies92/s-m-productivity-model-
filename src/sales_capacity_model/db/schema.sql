-- Sales Capacity Model: register schema (state assumptions only; docs/MODEL.md section 4)
-- What-if hypotheses and method versions live in modeller.sql and never reference this schema by foreign key.
-- © 2000–2026 Growth Enablement. All rights reserved.
--
-- Written for SQLite (V1); portable to PostgreSQL with type changes only.
-- Layers:
--   1. Tenancy, scope and versions      client, engagement, baseline_version, contributor
--   2. Collection                       collection_step, request, source_document
--   3. Meaning                          field, field_definition, causal_link
--   4. System entities                  entity (supertype), territory, salesperson, assignment, segment, rule, event
--   5. Observations (raw facts)         opportunity, pipeline_snapshot, financial_line
--   6. Assumption ledger                assumption, assumption_value, assumption_input, assumption_evidence,
--                                       assumption_validation, assumption_test
--   7. Tests                            test_definition, test_member, engagement_test_config, test_run,
--                                       test_run_input, resolution
--   8. Track record                     accuracy_record
-- Rules enforced here: append-only history, frozen signed baselines, pseudonymous salespeople,
-- declared basis and scope on every value, reference values name their context.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- 1. Tenancy, scope, versions
CREATE TABLE client (
  client_id   TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE engagement (
  engagement_id      TEXT PRIMARY KEY,
  client_id          TEXT NOT NULL REFERENCES client(client_id),
  scope              TEXT NOT NULL,                     -- whole company, channel, product line
  period_start       TEXT NOT NULL,
  period_end         TEXT NOT NULL,
  currency           TEXT NOT NULL,
  revenue_basis      TEXT NOT NULL CHECK (revenue_basis IN ('recognized', 'bookings')),
  benchmark_consent  INTEGER NOT NULL DEFAULT 0 CHECK (benchmark_consent IN (0, 1)),
  min_group_size     INTEGER NOT NULL DEFAULT 5,
  created_at         TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (period_end > period_start)
);

-- People who provide or validate data. Salespeople are never stored here.
CREATE TABLE contributor (
  contributor_id  TEXT PRIMARY KEY,
  engagement_id   TEXT NOT NULL REFERENCES engagement(engagement_id),
  name            TEXT NOT NULL,
  email           TEXT,
  role            TEXT NOT NULL CHECK (role IN ('sponsor', 'sales_leader', 'finance', 'finance_lead',
                    'sales_ops', 'hr', 'compensation', 'growth_enablement'))
);

CREATE TABLE baseline_version (
  baseline_version_id  TEXT PRIMARY KEY,
  engagement_id        TEXT NOT NULL REFERENCES engagement(engagement_id),
  parent_version_id    TEXT REFERENCES baseline_version(baseline_version_id),
  state                TEXT NOT NULL DEFAULT 'draft'
                         CHECK (state IN ('draft', 'working', 'in_review', 'signed')),
  signed_by            TEXT REFERENCES contributor(contributor_id),
  signed_at            TEXT,
  created_at           TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (state <> 'signed' OR (signed_by IS NOT NULL AND signed_at IS NOT NULL))
);

-- ---------------------------------------------------------------- 2. Collection
CREATE TABLE collection_step (
  step_no             INTEGER PRIMARY KEY,
  name                TEXT NOT NULL,
  default_owner_role  TEXT NOT NULL,
  asks_for            TEXT NOT NULL,
  depends_on          TEXT                                -- comma-separated step numbers
);

CREATE TABLE request (
  request_id      TEXT PRIMARY KEY,
  engagement_id   TEXT NOT NULL REFERENCES engagement(engagement_id),
  step_no         INTEGER NOT NULL REFERENCES collection_step(step_no),
  assigned_to     TEXT REFERENCES contributor(contributor_id),
  status          TEXT NOT NULL DEFAULT 'not_started'
                    CHECK (status IN ('not_started', 'sent', 'in_progress', 'returned', 'complete', 'unavailable')),
  sent_at         TEXT,
  completed_at    TEXT
);

CREATE TABLE source_document (
  document_id     TEXT PRIMARY KEY,
  engagement_id   TEXT NOT NULL REFERENCES engagement(engagement_id),
  step_no         INTEGER REFERENCES collection_step(step_no),
  request_id      TEXT REFERENCES request(request_id),
  kind            TEXT NOT NULL CHECK (kind IN ('questionnaire', 'income_statement', 'plan', 'gl_detail',
                    'roster', 'territory_plan', 'crm_closed', 'crm_snapshot', 'comp_plan',
                    'vacancy_log', 'rules', 'other')),
  filename        TEXT NOT NULL,
  content_hash    TEXT NOT NULL,                       -- sha256 of the stored file
  period_start    TEXT,
  period_end      TEXT,
  uploaded_by     TEXT REFERENCES contributor(contributor_id),
  uploaded_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------- 3. Meaning
-- One row per thing the model can know. Definitions are versioned separately.
CREATE TABLE field (
  field_id          TEXT PRIMARY KEY,                   -- e.g. 'win_rate', 'expected_yield'
  name              TEXT NOT NULL,
  unit              TEXT NOT NULL,                      -- 'ratio', 'months', 'currency', 'count', 'text'
  level             TEXT NOT NULL CHECK (level IN ('company', 'territory', 'salesperson', 'assignment',
                      'segment', 'group', 'rule', 'model')),
  element_type      TEXT NOT NULL CHECK (element_type IN ('parameter', 'buffer', 'stock', 'flow', 'delay',
                      'loop', 'information', 'rule', 'structure', 'goal', 'paradigm')),
  leverage_point    INTEGER NOT NULL CHECK (leverage_point BETWEEN 1 AND 12),
  collection_step   INTEGER REFERENCES collection_step(step_no),
  high_sensitivity  INTEGER NOT NULL DEFAULT 0 CHECK (high_sensitivity IN (0, 1))
);

CREATE TABLE field_definition (
  field_id        TEXT NOT NULL REFERENCES field(field_id),
  version         INTEGER NOT NULL,
  definition      TEXT NOT NULL,
  includes        TEXT,
  excludes        TEXT,
  where_to_find   TEXT,                                 -- report recipe shown to the client
  effective_from  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (field_id, version)
);

-- The model's structure as data: how fields drive each other (Meadows: structure, loops, delays).
CREATE TABLE causal_link (
  link_id                  TEXT PRIMARY KEY,
  from_field_id            TEXT NOT NULL REFERENCES field(field_id),
  to_field_id              TEXT NOT NULL REFERENCES field(field_id),
  relation                 TEXT NOT NULL CHECK (relation IN ('multiplies', 'divides', 'adds', 'subtracts',
                             'caps', 'delays', 'feeds_back')),
  polarity                 TEXT NOT NULL CHECK (polarity IN ('+', '-')),
  structural_assumption    TEXT REFERENCES field(field_id),   -- the model-level assumption that asserts it
  description              TEXT
);

-- ---------------------------------------------------------------- 4. System entities
-- Supertype: everything an assumption can be about.
CREATE TABLE entity (
  entity_id      TEXT PRIMARY KEY,
  engagement_id  TEXT NOT NULL REFERENCES engagement(engagement_id),
  entity_type    TEXT NOT NULL CHECK (entity_type IN ('company', 'territory', 'salesperson', 'assignment',
                   'segment', 'group', 'rule', 'model')),
  created_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE segment (
  entity_id  TEXT PRIMARY KEY REFERENCES entity(entity_id),
  name       TEXT NOT NULL,
  basis      TEXT NOT NULL                                -- geography, industry, size, named accounts, buyer problem
);

-- A territory is a design choice. Status is derived from assignments and events.
CREATE TABLE territory (
  entity_id           TEXT PRIMARY KEY REFERENCES entity(entity_id),
  external_ref        TEXT NOT NULL,                      -- the client's territory code
  name                TEXT,
  segment_entity_id   TEXT REFERENCES segment(entity_id),
  source_document_id  TEXT REFERENCES source_document(document_id)
);

-- A salesperson is an agent. Pseudonymous: the HR ID is hashed with a per-engagement salt on import.
CREATE TABLE salesperson (
  entity_id           TEXT PRIMARY KEY REFERENCES entity(entity_id),
  pseudonym           TEXT NOT NULL,
  role                TEXT NOT NULL DEFAULT 'quota_carrying',
  start_date          TEXT,
  end_date            TEXT,
  cost_band           TEXT,
  source_document_id  TEXT REFERENCES source_document(document_id)
);

-- The only link between territory design and staffing.
CREATE TABLE assignment (
  entity_id           TEXT PRIMARY KEY REFERENCES entity(entity_id),
  territory_id        TEXT NOT NULL REFERENCES territory(entity_id),
  salesperson_id      TEXT NOT NULL REFERENCES salesperson(entity_id),
  share_of_time       REAL NOT NULL DEFAULT 1.0 CHECK (share_of_time > 0 AND share_of_time <= 1),
  valid_from          TEXT NOT NULL,
  valid_to            TEXT,
  source_document_id  TEXT REFERENCES source_document(document_id),
  CHECK (valid_to IS NULL OR valid_to >= valid_from)
);

CREATE TABLE rule (
  entity_id           TEXT PRIMARY KEY REFERENCES entity(entity_id),
  rule_type           TEXT NOT NULL CHECK (rule_type IN ('commission', 'accelerator', 'hiring_approval',
                        'qualification', 'territory_assignment', 'discount_authority', 'design_authority')),
  description         TEXT NOT NULL,
  parameters_json     TEXT,
  source_document_id  TEXT REFERENCES source_document(document_id)
);

-- Dated facts about entities: vacancies and their approval stages, hires, departures.
CREATE TABLE event (
  event_id            TEXT PRIMARY KEY,
  entity_id           TEXT NOT NULL REFERENCES entity(entity_id),
  episode_id          TEXT,                               -- groups the stages of one vacancy
  event_type          TEXT NOT NULL CHECK (event_type IN ('territory_created', 'territory_retired',
                        'vacancy_opened', 'requisition_approved', 'offer_accepted', 'salesperson_started',
                        'ramp_complete', 'salesperson_departed')),
  event_date          TEXT NOT NULL,
  source_document_id  TEXT REFERENCES source_document(document_id),
  recorded_by         TEXT REFERENCES contributor(contributor_id),
  recorded_at         TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------- 5. Observations (raw facts)
-- Kept raw so estimators can recompute; assumptions are derived from these, never the reverse.
CREATE TABLE opportunity (
  opportunity_id      TEXT PRIMARY KEY,
  engagement_id       TEXT NOT NULL REFERENCES engagement(engagement_id),
  external_ref        TEXT,
  salesperson_id      TEXT REFERENCES salesperson(entity_id),
  territory_id        TEXT REFERENCES territory(entity_id),
  created_date        TEXT NOT NULL,
  qualified_date      TEXT,
  closed_date         TEXT,
  outcome             TEXT NOT NULL CHECK (outcome IN ('open', 'won', 'lost', 'disqualified')),
  amount              REAL,
  source_document_id  TEXT NOT NULL REFERENCES source_document(document_id),
  CHECK (outcome = 'open' OR closed_date IS NOT NULL)
);

CREATE TABLE pipeline_snapshot (
  snapshot_id         TEXT PRIMARY KEY,
  engagement_id       TEXT NOT NULL REFERENCES engagement(engagement_id),
  snapshot_date       TEXT NOT NULL,
  salesperson_id      TEXT REFERENCES salesperson(entity_id),
  territory_id        TEXT REFERENCES territory(entity_id),
  open_opportunities  INTEGER NOT NULL CHECK (open_opportunities >= 0),
  open_amount         REAL,
  source_document_id  TEXT NOT NULL REFERENCES source_document(document_id)
);

CREATE TABLE financial_line (
  line_id             TEXT PRIMARY KEY,
  engagement_id       TEXT NOT NULL REFERENCES engagement(engagement_id),
  statement           TEXT NOT NULL CHECK (statement IN ('income_statement', 'plan', 'gl_detail')),
  period_start        TEXT NOT NULL,
  period_end          TEXT NOT NULL,
  account_code        TEXT,
  account_name        TEXT NOT NULL,
  category            TEXT NOT NULL CHECK (category IN ('revenue', 'cost_of_revenue', 'rnd', 'gna',
                        'sales_salaries', 'sales_benefits', 'commissions', 'travel', 'sales_overhead',
                        'marketing', 'other')),
  cost_behavior       TEXT CHECK (cost_behavior IN ('fixed', 'variable', 'step_fixed', 'discretionary')),
  amount              REAL NOT NULL,
  source_document_id  TEXT NOT NULL REFERENCES source_document(document_id)
);

-- ---------------------------------------------------------------- 6. Assumption ledger
-- An assumption is a slot: one field, about one entity, in one scope, in one baseline version.
CREATE TABLE assumption (
  assumption_id        TEXT PRIMARY KEY,
  baseline_version_id  TEXT NOT NULL REFERENCES baseline_version(baseline_version_id),
  field_id             TEXT NOT NULL REFERENCES field(field_id),
  entity_id            TEXT NOT NULL REFERENCES entity(entity_id),
  scope                TEXT NOT NULL DEFAULT 'this_client',  -- 'this_client', 'reference_model', or a segment
  period_start         TEXT,
  period_end           TEXT,
  UNIQUE (baseline_version_id, field_id, entity_id, scope)
);

-- Every value ever asserted for a slot. Append-only; the latest seq is current.
CREATE TABLE assumption_value (
  value_id             TEXT PRIMARY KEY,
  assumption_id        TEXT NOT NULL REFERENCES assumption(assumption_id),
  seq                  INTEGER NOT NULL,
  statement            TEXT NOT NULL,                      -- the claim in plain language
  value_num            REAL,
  value_text           TEXT,
  low                  REAL,
  high                 REAL,
  definition_version   INTEGER NOT NULL DEFAULT 1,
  basis                TEXT NOT NULL CHECK (basis IN ('validated_actual', 'calculated_estimate',
                         'reference_value', 'judgment')),
  method               TEXT,                               -- estimator name, or how it was obtained
  reference_context    TEXT,                               -- required for reference values
  rationale            TEXT,
  collection_step      INTEGER REFERENCES collection_step(step_no),
  sealed_belief        INTEGER NOT NULL DEFAULT 0 CHECK (sealed_belief IN (0, 1)),  -- captured before any data
  asserted_by          TEXT REFERENCES contributor(contributor_id),
  asserted_at          TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  supersedes_value_id  TEXT REFERENCES assumption_value(value_id),
  UNIQUE (assumption_id, seq),
  CHECK (value_num IS NOT NULL OR value_text IS NOT NULL),
  CHECK (basis <> 'reference_value' OR reference_context IS NOT NULL),
  CHECK (basis NOT IN ('reference_value', 'judgment') OR value_num IS NULL OR (low IS NOT NULL AND high IS NOT NULL)),
  CHECK (low IS NULL OR high IS NULL OR (low <= value_num AND value_num <= high))
);

-- Lineage: which values a calculated estimate was built from.
CREATE TABLE assumption_input (
  value_id        TEXT NOT NULL REFERENCES assumption_value(value_id),
  input_value_id  TEXT NOT NULL REFERENCES assumption_value(value_id),
  PRIMARY KEY (value_id, input_value_id),
  CHECK (value_id <> input_value_id)
);

CREATE TABLE assumption_evidence (
  value_id     TEXT NOT NULL REFERENCES assumption_value(value_id),
  document_id  TEXT NOT NULL REFERENCES source_document(document_id),
  PRIMARY KEY (value_id, document_id)
);

-- Finance validation is recorded separately so values stay append-only.
CREATE TABLE assumption_validation (
  validation_id  TEXT PRIMARY KEY,
  value_id       TEXT NOT NULL REFERENCES assumption_value(value_id),
  validated_by   TEXT NOT NULL REFERENCES contributor(contributor_id),
  decision       TEXT NOT NULL CHECK (decision IN ('validated', 'attested', 'rejected')),
  note           TEXT,
  validated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- The falsification attached to an assumption: which test can prove it wrong, and when to look again.
CREATE TABLE assumption_test (
  assumption_id  TEXT NOT NULL REFERENCES assumption(assumption_id),
  test_id        TEXT NOT NULL REFERENCES test_definition(test_id),
  observable     TEXT NOT NULL,                            -- what would prove it wrong
  measured_in    TEXT,                                     -- where that is observed
  threshold      REAL,
  review_date    TEXT,
  PRIMARY KEY (assumption_id, test_id)
);

-- ---------------------------------------------------------------- 7. Tests
CREATE TABLE test_definition (
  test_id            TEXT PRIMARY KEY,
  name               TEXT NOT NULL,
  test_type          TEXT NOT NULL CHECK (test_type IN ('observation', 'implication', 'triangulation',
                       'bounds', 'dispersion', 'prediction')),
  expression         TEXT NOT NULL,                        -- engine reference for the computation
  default_tolerance  REAL,
  tolerance_kind     TEXT NOT NULL DEFAULT 'pct' CHECK (tolerance_kind IN ('pct', 'abs', 'none')),
  default_severity   TEXT NOT NULL CHECK (default_severity IN ('block', 'explain', 'warn')),
  description        TEXT NOT NULL
);

-- Which fields take part in a test: the candidate set when it fails.
CREATE TABLE test_member (
  test_id   TEXT NOT NULL REFERENCES test_definition(test_id),
  field_id  TEXT NOT NULL REFERENCES field(field_id),
  role      TEXT NOT NULL CHECK (role IN ('input', 'observed')),
  PRIMARY KEY (test_id, field_id)
);

CREATE TABLE engagement_test_config (
  engagement_id  TEXT NOT NULL REFERENCES engagement(engagement_id),
  test_id        TEXT NOT NULL REFERENCES test_definition(test_id),
  tolerance      REAL,
  severity       TEXT CHECK (severity IN ('block', 'explain', 'warn')),
  PRIMARY KEY (engagement_id, test_id)
);

CREATE TABLE test_run (
  run_id               TEXT PRIMARY KEY,
  baseline_version_id  TEXT NOT NULL REFERENCES baseline_version(baseline_version_id),
  test_id              TEXT NOT NULL REFERENCES test_definition(test_id),
  scope_entity_id      TEXT REFERENCES entity(entity_id),   -- company, a territory, a salesperson group
  implied_value        REAL,
  observed_value       REAL,
  gap                  REAL,
  outcome              TEXT NOT NULL CHECK (outcome IN ('pass', 'fail', 'warn')),
  engine_version       TEXT NOT NULL,
  run_at               TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- The exact values a run used. On failure, this is the candidate set the client works through.
CREATE TABLE test_run_input (
  run_id    TEXT NOT NULL REFERENCES test_run(run_id),
  value_id  TEXT NOT NULL REFERENCES assumption_value(value_id),
  PRIMARY KEY (run_id, value_id)
);

CREATE TABLE resolution (
  resolution_id   TEXT PRIMARY KEY,
  run_id          TEXT NOT NULL REFERENCES test_run(run_id),
  action          TEXT NOT NULL CHECK (action IN ('fixed', 'explained', 'accepted')),
  category        TEXT CHECK (category IN ('definition', 'timing', 'scope', 'data_quality',
                    'reference_value', 'other')),
  note            TEXT NOT NULL,
  fixed_value_id  TEXT REFERENCES assumption_value(value_id),
  resolved_by     TEXT NOT NULL REFERENCES contributor(contributor_id),
  resolved_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (action <> 'fixed' OR fixed_value_id IS NOT NULL)
);

-- ---------------------------------------------------------------- 8. Track record
CREATE TABLE accuracy_record (
  record_id          TEXT PRIMARY KEY,
  assumption_id      TEXT NOT NULL REFERENCES assumption(assumption_id),
  period_start       TEXT NOT NULL,
  period_end         TEXT NOT NULL,
  assumed_value_id   TEXT NOT NULL REFERENCES assumption_value(value_id),
  observed_value_id  TEXT NOT NULL REFERENCES assumption_value(value_id),
  error              REAL NOT NULL,                        -- observed − assumed
  recorded_at        TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------- Indexes
CREATE INDEX ix_assumption_entity  ON assumption(entity_id);
CREATE INDEX ix_assumption_field   ON assumption(field_id);
CREATE INDEX ix_value_assumption   ON assumption_value(assumption_id, seq);
CREATE INDEX ix_assignment_terr    ON assignment(territory_id, valid_from);
CREATE INDEX ix_assignment_sp      ON assignment(salesperson_id, valid_from);
CREATE INDEX ix_opp_sp             ON opportunity(salesperson_id, closed_date);
CREATE INDEX ix_opp_terr           ON opportunity(territory_id, closed_date);
CREATE INDEX ix_event_entity       ON event(entity_id, event_date);
CREATE UNIQUE INDEX ux_salesperson_pseudonym ON salesperson(pseudonym);
CREATE INDEX ix_territory_ref ON territory(external_ref);

-- ---------------------------------------------------------------- Integrity triggers
-- Append-only history.
CREATE TRIGGER no_update_value BEFORE UPDATE ON assumption_value
BEGIN SELECT RAISE(ABORT, 'assumption_value is append-only: insert a new seq instead'); END;
CREATE TRIGGER no_delete_value BEFORE DELETE ON assumption_value
BEGIN SELECT RAISE(ABORT, 'assumption_value is append-only'); END;
CREATE TRIGGER no_update_event BEFORE UPDATE ON event
BEGIN SELECT RAISE(ABORT, 'event is append-only'); END;
CREATE TRIGGER no_update_run BEFORE UPDATE ON test_run
BEGIN SELECT RAISE(ABORT, 'test_run is append-only'); END;
CREATE TRIGGER no_update_resolution BEFORE UPDATE ON resolution
BEGIN SELECT RAISE(ABORT, 'resolution is append-only'); END;
CREATE TRIGGER no_update_accuracy BEFORE UPDATE ON accuracy_record
BEGIN SELECT RAISE(ABORT, 'accuracy_record is append-only'); END;

-- Signed baselines are frozen.
CREATE TRIGGER frozen_baseline BEFORE UPDATE ON baseline_version
WHEN OLD.state = 'signed'
BEGIN SELECT RAISE(ABORT, 'signed baseline is frozen: create a new version'); END;

CREATE TRIGGER frozen_baseline_assumption BEFORE INSERT ON assumption
WHEN (SELECT state FROM baseline_version WHERE baseline_version_id = NEW.baseline_version_id) = 'signed'
BEGIN SELECT RAISE(ABORT, 'signed baseline is frozen: create a new version'); END;

CREATE TRIGGER frozen_baseline_value BEFORE INSERT ON assumption_value
WHEN (SELECT bv.state FROM assumption a JOIN baseline_version bv USING (baseline_version_id)
      WHERE a.assumption_id = NEW.assumption_id) = 'signed'
BEGIN SELECT RAISE(ABORT, 'signed baseline is frozen: create a new version'); END;

-- Sealed beliefs must be judgments, and nothing can be sealed after data has arrived for that slot.
CREATE TRIGGER sealed_belief_is_judgment BEFORE INSERT ON assumption_value
WHEN NEW.sealed_belief = 1 AND (NEW.basis <> 'judgment'
      OR EXISTS (SELECT 1 FROM assumption_value v WHERE v.assumption_id = NEW.assumption_id))
BEGIN SELECT RAISE(ABORT, 'a sealed belief must be the first value for its slot and a judgment'); END;

-- Only finance roles may validate.
CREATE TRIGGER finance_validates BEFORE INSERT ON assumption_validation
WHEN (SELECT role FROM contributor WHERE contributor_id = NEW.validated_by) NOT IN ('finance', 'finance_lead')
BEGIN SELECT RAISE(ABORT, 'only Finance can validate a value'); END;

-- ---------------------------------------------------------------- Views
-- Current value of every assumption.
CREATE VIEW v_current_value AS
SELECT a.assumption_id, a.baseline_version_id, a.field_id, a.entity_id, a.scope,
       v.value_id, v.value_num, v.value_text, v.low, v.high, v.basis, v.statement, v.asserted_at,
       EXISTS (SELECT 1 FROM assumption_validation x
               WHERE x.value_id = v.value_id AND x.decision = 'validated') AS validated
FROM assumption a
JOIN assumption_value v ON v.assumption_id = a.assumption_id
WHERE v.seq = (SELECT MAX(seq) FROM assumption_value w WHERE w.assumption_id = a.assumption_id);

-- Perception gap: the sealed belief against the current evidence-based value.
CREATE VIEW v_perception_gap AS
SELECT a.baseline_version_id, a.field_id, a.entity_id,
       b.value_num AS believed, c.value_num AS current, c.basis AS current_basis,
       c.value_num - b.value_num AS gap
FROM assumption a
JOIN assumption_value b ON b.assumption_id = a.assumption_id AND b.sealed_belief = 1
JOIN v_current_value c ON c.assumption_id = a.assumption_id
WHERE c.basis IN ('validated_actual', 'calculated_estimate');

-- Territory status at any date: filled if an assignment covers the date, otherwise open.
CREATE VIEW v_territory_assignment_share AS
SELECT t.entity_id AS territory_id, t.external_ref, a.salesperson_id, a.share_of_time,
       a.valid_from, a.valid_to
FROM territory t
LEFT JOIN assignment a ON a.territory_id = t.entity_id;

-- Vacancy timeline: days spent in each stage of each vacancy episode.
CREATE VIEW v_vacancy_stages AS
SELECT e.entity_id AS territory_id, e.episode_id,
       MAX(CASE WHEN e.event_type = 'vacancy_opened'       THEN e.event_date END) AS opened,
       MAX(CASE WHEN e.event_type = 'requisition_approved' THEN e.event_date END) AS approved,
       MAX(CASE WHEN e.event_type = 'offer_accepted'       THEN e.event_date END) AS offer_accepted,
       MAX(CASE WHEN e.event_type = 'salesperson_started'  THEN e.event_date END) AS started
FROM event e
WHERE e.episode_id IS NOT NULL
GROUP BY e.entity_id, e.episode_id;

-- Candidate set for every failed test: the values that could be wrong.
CREATE VIEW v_candidate_set AS
SELECT r.run_id, r.test_id, r.baseline_version_id, r.gap, v.value_id, a.field_id, a.entity_id,
       v.basis, v.statement
FROM test_run r
JOIN test_run_input i ON i.run_id = r.run_id
JOIN assumption_value v ON v.value_id = i.value_id
JOIN assumption a ON a.assumption_id = v.assumption_id
WHERE r.outcome = 'fail'
  AND NOT EXISTS (SELECT 1 FROM resolution s WHERE s.run_id = r.run_id);

-- Confidence profile: share of current values by basis, per baseline.
CREATE VIEW v_confidence_profile AS
SELECT baseline_version_id, basis, COUNT(*) AS n,
       ROUND(1.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY baseline_version_id), 3) AS share
FROM v_current_value
GROUP BY baseline_version_id, basis;
