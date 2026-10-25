-- Sales Capacity Model: modeller schema (docs/MODEL.md section 4)
-- © 2000–2026 Growth Enablement. All rights reserved.
--
-- Holds method assumptions and intervention hypotheses. Never state.
-- It refers to the register only by identifiers (field ids, a frozen register version id),
-- never by foreign key: the register must stay valid with the modeller absent, and the
-- register's baseline can never depend on anything here.

PRAGMA foreign_keys = ON;

-- A lever is a register field the modeller may scale, and how revenue responds to it.
CREATE TABLE lever (
  lever_id        TEXT PRIMARY KEY,                     -- 'close_rate', 'cycle', 'deal_size'
  register_field  TEXT NOT NULL,                        -- register field id, e.g. 'win_rate' (by name, not FK)
  direction       TEXT NOT NULL CHECK (direction IN ('up', 'down')),   -- an improvement raises or lowers the field
  revenue_effect  TEXT NOT NULL CHECK (revenue_effect IN ('proportional', 'inverse', 'structural')),
  label           TEXT NOT NULL
);

-- A method version is the set of equations applied to the register: the chain, in words and in code.
CREATE TABLE method_version (
  method_version_id  TEXT PRIMARY KEY,                  -- e.g. 'chain-2026-10-25'
  unit_of_throughput TEXT NOT NULL CHECK (unit_of_throughput IN ('salesperson', 'territory')),
  description        TEXT NOT NULL,                     -- the rules in words, one per line
  created_at         TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- A scenario is a vector of multipliers on levers: a hypothesis, not a belief about the present.
CREATE TABLE scenario (
  scenario_id   TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  question      TEXT,                                   -- the question it answers, in the client's words
  is_default    INTEGER NOT NULL DEFAULT 0,             -- the original's set ships as defaults
  created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scenario_lever (
  scenario_id  TEXT NOT NULL REFERENCES scenario(scenario_id),
  lever_id     TEXT NOT NULL REFERENCES lever(lever_id),
  improvement  REAL NOT NULL,                           -- relative: 0.10 = 10 % better in the lever's direction
  PRIMARY KEY (scenario_id, lever_id)
);

-- A run records which hypothesis was applied, with which method, to which frozen register version.
-- Results are a cache keyed by all three; they are never written back to the register.
CREATE TABLE scenario_run (
  run_id               TEXT PRIMARY KEY,
  scenario_id          TEXT NOT NULL REFERENCES scenario(scenario_id),
  method_version_id    TEXT NOT NULL REFERENCES method_version(method_version_id),
  register_version_id  TEXT NOT NULL,                   -- register baseline_version id, by name
  run_at               TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scenario_run_result (
  run_id   TEXT NOT NULL REFERENCES scenario_run(run_id),
  metric   TEXT NOT NULL,                               -- 'revenue', 'operating_income', 'd_operating_income', ...
  value    REAL,
  PRIMARY KEY (run_id, metric)
);

-- Default levers and scenarios: the original's quality set.
INSERT INTO lever VALUES
  ('close_rate', 'win_rate',      'up',   'proportional', 'Close rate'),
  ('cycle',      'cycle_months',  'down', 'inverse',      'Sales cycle'),
  ('deal_size',  'deal_size',     'up',   'proportional', 'Average revenue per contract');

INSERT INTO method_version (method_version_id, unit_of_throughput, description) VALUES
  ('chain-2026-10-25', 'salesperson',
   'worked = MIN(held, capacity); resolved = worked x 12 / cycle; contracts per salesperson = resolved x close rate; ' ||
   'revenue = contracts per salesperson x deal size x salespeople; income statement per docs/MODEL.md section 3');

INSERT INTO scenario (scenario_id, name, question, is_default) VALUES
  ('close_rate', 'Close rate',  'What if we won a larger share of the opportunities we already work?', 1),
  ('cycle',      'Cycle time',  'What if each opportunity took less time to resolve?', 1),
  ('deal_size',  'Deal size',   'What if each contract were worth more?', 1),
  ('combined',   'Combined',    'What if all three improved together?', 1);

INSERT INTO scenario_lever VALUES
  ('close_rate', 'close_rate', 0.10),
  ('cycle',      'cycle',      0.10),
  ('deal_size',  'deal_size',  0.10),
  ('combined',   'close_rate', 0.10),
  ('combined',   'cycle',      0.10),
  ('combined',   'deal_size',  0.10);
