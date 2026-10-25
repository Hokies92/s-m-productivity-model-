-- Reference data: collection steps, field catalog, structural assumptions, tests, causal links.
-- © 2000–2026 Growth Enablement. All rights reserved.

-- ---------------------------------------------------------------- Collection sequence (easiest for the client)
INSERT INTO collection_step (step_no, name, default_owner_role, asks_for, depends_on) VALUES
 (1,  'Scope',                       'sponsor',      'Period, business in scope, currency, revenue basis', NULL),
 (2,  'Leadership beliefs',          'sales_leader', 'Short questionnaire, no data: territories and market division, expected yield, win rate, cycle, deal size, opportunities a salesperson can hold, ramp, time to fill', '1'),
 (3,  'Financial results',           'finance',      'Income statement for the period and the plan', '1'),
 (4,  'Sales and marketing cost detail', 'finance',  'General ledger detail for sales and marketing cost centers', '1'),
 (5,  'Salesperson roster',          'hr',           'Roster export: start date, end date, role, salary band (names stripped on import)', '1'),
 (6,  'Territory plan',              'sales_ops',    'Territory list with assigned salesperson or open, quota or expected yield, segment', '1'),
 (7,  'CRM exports',                 'sales_ops',    'Closed opportunities in the period; month-end open opportunity snapshots', '1'),
 (8,  'Compensation plan',           'compensation', 'Current compensation plan document', '1'),
 (9,  'Vacancy and hiring timeline', 'hr',           'Per open territory: opened, requisition approved, offer accepted, started', '6'),
 (10, 'Rules and definitions',       'sales_ops',    'Qualification definition, hiring approval, territory assignment, design authority', '6'),
 (11, 'Reconcile and sign',          'finance_lead', 'Reconciliation list, yield bridge, sign-off checklist', '3,4,5,6,7,8,9,10');

-- ---------------------------------------------------------------- Field catalog
-- (field_id, name, unit, level, element_type, leverage_point, collection_step, high_sensitivity)
INSERT INTO field VALUES
 -- Paradigm, goals, self-organization, information (declared)
 ('segmentation_basis',     'How the market is divided into territories', 'text', 'company', 'paradigm', 2, 2, 0),
 ('theory_of_buying',       'Stated theory of how customers buy',         'text', 'company', 'paradigm', 2, 2, 0),
 ('system_goal',            'What the commercial system optimizes',       'text', 'company', 'goal',     3, 2, 0),
 ('plan_target',            'Revenue plan for the period',                'currency', 'company', 'goal', 3, 3, 0),
 ('expected_yield',         'Expected annual yield of a territory',       'currency', 'territory', 'goal', 3, 6, 1),
 ('design_authority',       'Who can change territory design or roles',   'text', 'company', 'structure', 4, 10, 0),
 ('shared_definitions',     'Whether Sales and Finance share definitions','text', 'company', 'information', 6, 10, 0),
 ('qualification_definition','When an opportunity counts as qualified',   'text', 'rule', 'rule', 5, 10, 0),
 ('hiring_approval_rule',   'Steps and approvers to fill a territory',    'text', 'rule', 'rule', 5, 10, 0),
 ('commission_rate',        'Effective commission rate',                  'ratio', 'rule', 'rule', 5, 8, 0),
 -- Stocks and flows
 ('territory_count',        'Funded territories',                         'count', 'company', 'stock', 10, 6, 1),
 ('productive_salespeople', 'Average fully ramped salespeople',           'count', 'company', 'stock', 10, 5, 1),
 ('revenue',                'Revenue in scope for the period',            'currency', 'company', 'flow', 12, 3, 1),
 ('contracts',              'Contracts closed in the period',             'count', 'company', 'flow', 12, 3, 1),
 ('sales_comp_expense',     'Sales compensation expense in the ledger',   'currency', 'company', 'flow', 12, 4, 0),
 -- Buffers and delays
 ('opportunities_load',     'Open qualified opportunities held',          'count', 'salesperson', 'buffer', 11, 7, 1),
 ('cycle_months',           'Qualified opportunity to signature',         'months', 'salesperson', 'delay', 9, 7, 1),
 ('ramp_months',            'Months until a new salesperson is productive','months', 'salesperson', 'delay', 9, 2, 0),
 ('time_to_fill_days',      'Days a territory stays open',                'days', 'territory', 'delay', 9, 9, 0),
 ('approval_days',          'Days from vacancy to approved requisition',  'days', 'territory', 'delay', 9, 9, 0),
 -- Parameters
 ('opportunities_capacity', 'Opportunities a salesperson can hold and advance well', 'count', 'salesperson', 'parameter', 12, 2, 1),
 ('win_rate',               'Won ÷ (won + lost), by count',               'ratio', 'salesperson', 'parameter', 12, 7, 1),
 ('deal_size',              'Revenue per contract',                       'currency', 'salesperson', 'parameter', 12, 7, 1),
 ('base_salary',            'Average base salary of quota-carrying salespeople', 'currency', 'salesperson', 'parameter', 12, 4, 1),
 ('load_rate',              'Benefits and payroll taxes ÷ base salary',   'ratio', 'company', 'parameter', 12, 4, 0),
 ('travel_per_salesperson', 'Travel and entertainment per salesperson',   'currency', 'salesperson', 'parameter', 12, 4, 0),
 ('sales_overhead',         'Non-quota sales costs',                      'currency', 'company', 'parameter', 12, 4, 0),
 ('marketing',              'Marketing costs',                            'currency', 'company', 'parameter', 12, 4, 0),
 ('cost_of_revenue_pct',    'Cost of revenue ÷ revenue',                  'ratio', 'company', 'parameter', 12, 3, 0),
 ('rnd_pct',                'R&D ÷ revenue',                              'ratio', 'company', 'parameter', 12, 3, 0),
 ('gna_pct',                'G&A ÷ revenue',                              'ratio', 'company', 'parameter', 12, 3, 0),
 -- Structural assumptions (model level)
 ('s1_throughput',          'S1 Throughput = opportunities held ÷ cycle', 'text', 'model', 'structure', 10, NULL, 1),
 ('s2_yield_when_staffed',  'S2 A territory yields only when filled and ramped', 'text', 'model', 'structure', 10, NULL, 1),
 ('s3_rate_size_independent','S3 Win rate and deal size are independent', 'text', 'model', 'structure', 10, NULL, 0),
 ('s4_load_quality',        'S4 Load does not affect win rate or cycle',  'text', 'model', 'loop', 8, NULL, 1),
 ('s5_ramp_shape',          'S5 Ramp shape',                              'text', 'model', 'delay', 9, NULL, 0),
 ('s6_cost_scaling',        'S6 Non-sales costs scale with revenue',      'text', 'model', 'structure', 10, NULL, 0),
 ('s7_commission_flat',     'S7 Commission is flat on revenue',           'text', 'model', 'rule', 5, NULL, 0),
 ('s8_one_per_territory',   'S8 One salesperson per territory',           'text', 'model', 'structure', 10, NULL, 0),
 ('s9_full_capacity',       'S9 Every filled territory runs at full capacity', 'text', 'model', 'structure', 10, NULL, 1);

INSERT INTO field_definition (field_id, version, definition, includes, excludes, where_to_find) VALUES
 ('win_rate', 1, 'Share of qualified opportunities closed as won, out of all that reached won or lost in the period',
  'Opportunities past the qualification stage', 'Open opportunities; opportunities disqualified before qualification',
  'CRM: opportunities closed in the period, grouped by outcome'),
 ('cycle_months', 1, 'Median days from qualified-opportunity creation to signature for won deals, divided by 30.4',
  'Won deals closed in the period', 'Lost deals', 'CRM closed opportunities: qualified date and close date'),
 ('expected_yield', 1, 'Revenue the company expects a territory to produce in a year when filled and ramped',
  'Quota or plan allocation for the territory', 'Stretch targets above plan', 'Territory plan or quota letter'),
 ('opportunities_capacity', 1, 'Most qualified opportunities a salesperson can hold and advance well at the same time',
  NULL, NULL, 'Sales leader judgment; tested against measured load and win rate by load level');

-- ---------------------------------------------------------------- Tests
INSERT INTO test_definition (test_id, name, test_type, expression, default_tolerance, tolerance_kind, default_severity, description) VALUES
 ('bounds_fields',        'Field bounds',              'bounds',        'engine.bounds',            NULL, 'none', 'block',   'Win rate 0–1, cycle > 0, counts ≥ 0'),
 ('territory_counts',     'Territory counts',          'bounds',        'engine.territory_counts',  NULL, 'none', 'block',   'Filled + open + shared = total territories'),
 ('revenue_implication',  'Revenue implication',       'implication',   'engine.implied_revenue',   0.10, 'pct',  'explain', 'Territories × capacity × 12 ÷ cycle × win rate × deal size vs actual revenue'),
 ('contracts_implication','Contracts implication',     'implication',   'engine.implied_contracts', 0.10, 'pct',  'explain', 'Territories × capacity × 12 ÷ cycle × win rate vs actual contracts'),
 ('deal_size_triangulation','Deal size triangulation', 'triangulation', 'engine.deal_size_check',   0.10, 'pct',  'explain', 'Revenue ÷ contracts vs entered deal size; reference values declared'),
 ('littles_law',          'Little''s Law',             'implication',   'engine.littles_law',       0.25, 'pct',  'explain', 'Open pipeline vs opportunities resolved per year × cycle ÷ 12'),
 ('utilization',          'Utilization',               'bounds',        'engine.utilization',       1.00, 'abs',  'block',   'Measured load ÷ stated capacity cannot exceed 1'),
 ('comp_ledger',          'Compensation vs ledger',    'triangulation', 'engine.comp_check',        0.10, 'pct',  'explain', 'Salaries × (1 + load) + commission × revenue vs ledger compensation'),
 ('expected_yield_plan',  'Expected yield vs plan',    'triangulation', 'engine.yield_vs_plan',     0.05, 'pct',  'explain', 'Sum of territory expected yields vs Finance plan'),
 ('yield_bridge',         'Yield bridge',              'implication',   'engine.yield_bridge',      0.00, 'abs',  'explain', 'Designed yield − vacancy − ramp − coverage − agent gap = actual revenue'),
 ('win_rate_dispersion',  'Win rate dispersion',       'dispersion',    'engine.dispersion',        NULL, 'none', 'warn',    'Is one company win rate representative across territories and groups?'),
 ('period_prediction',    'Period prediction',         'prediction',    'engine.prediction',        0.15, 'pct',  'warn',    'Last period''s assumptions vs this period''s observations');

INSERT INTO test_member (test_id, field_id, role) VALUES
 ('revenue_implication', 'territory_count', 'input'), ('revenue_implication', 'opportunities_capacity', 'input'),
 ('revenue_implication', 'cycle_months', 'input'),    ('revenue_implication', 'win_rate', 'input'),
 ('revenue_implication', 'deal_size', 'input'),       ('revenue_implication', 'revenue', 'observed'),
 ('contracts_implication', 'territory_count', 'input'), ('contracts_implication', 'opportunities_capacity', 'input'),
 ('contracts_implication', 'cycle_months', 'input'),    ('contracts_implication', 'win_rate', 'input'),
 ('contracts_implication', 'contracts', 'observed'),
 ('deal_size_triangulation', 'revenue', 'input'), ('deal_size_triangulation', 'contracts', 'input'),
 ('deal_size_triangulation', 'deal_size', 'observed'),
 ('littles_law', 'contracts', 'input'), ('littles_law', 'win_rate', 'input'), ('littles_law', 'cycle_months', 'input'),
 ('littles_law', 'productive_salespeople', 'input'), ('littles_law', 'opportunities_load', 'observed'),
 ('utilization', 'opportunities_load', 'input'), ('utilization', 'opportunities_capacity', 'input'),
 ('comp_ledger', 'base_salary', 'input'), ('comp_ledger', 'load_rate', 'input'), ('comp_ledger', 'commission_rate', 'input'),
 ('comp_ledger', 'revenue', 'input'), ('comp_ledger', 'productive_salespeople', 'input'),
 ('comp_ledger', 'sales_comp_expense', 'observed'),
 ('expected_yield_plan', 'expected_yield', 'input'), ('expected_yield_plan', 'plan_target', 'observed'),
 ('yield_bridge', 'expected_yield', 'input'), ('yield_bridge', 'time_to_fill_days', 'input'),
 ('yield_bridge', 'ramp_months', 'input'), ('yield_bridge', 'revenue', 'observed');

-- ---------------------------------------------------------------- Causal structure
INSERT INTO causal_link (link_id, from_field_id, to_field_id, relation, polarity, structural_assumption, description) VALUES
 ('L01', 'territory_count',        'revenue',            'multiplies', '+', 's9_full_capacity',     'Each funded, filled territory adds a salesperson''s throughput'),
 ('L02', 'opportunities_capacity', 'revenue',            'multiplies', '+', 's1_throughput',        'Capacity sets opportunities resolved per year'),
 ('L03', 'cycle_months',           'revenue',            'divides',    '-', 's1_throughput',        'Longer cycles turn capacity over fewer times a year'),
 ('L04', 'win_rate',               'revenue',            'multiplies', '+', NULL,                   'Share of resolved opportunities that become contracts'),
 ('L05', 'deal_size',              'revenue',            'multiplies', '+', NULL,                   'Revenue per contract'),
 ('L06', 'opportunities_load',     'cycle_months',       'feeds_back', '+', 's4_load_quality',      'Overload lengthens cycles (Little''s Law at fixed throughput)'),
 ('L07', 'opportunities_load',     'win_rate',           'feeds_back', '-', 's4_load_quality',      'Overload lowers win rate'),
 ('L08', 'opportunities_capacity', 'opportunities_load', 'caps',       '+', 's9_full_capacity',     'Load cannot exceed capacity without quality loss'),
 ('L09', 'time_to_fill_days',      'revenue',            'delays',     '-', 's2_yield_when_staffed','Open territories yield nothing until filled'),
 ('L10', 'approval_days',          'time_to_fill_days',  'adds',       '+', NULL,                   'Approval time is part of time to fill'),
 ('L11', 'ramp_months',            'revenue',            'delays',     '-', 's5_ramp_shape',        'New salespeople produce partially while ramping'),
 ('L12', 'deal_size',              'win_rate',           'feeds_back', '-', 's3_rate_size_independent','Larger deals may close less often'),
 ('L13', 'revenue',                'sales_comp_expense', 'adds',       '+', 's7_commission_flat',   'Commission rises with revenue'),
 ('L14', 'base_salary',            'sales_comp_expense', 'adds',       '+', NULL,                   'Fixed compensation per salesperson'),
 ('L15', 'expected_yield',         'plan_target',        'adds',       '+', NULL,                   'Territory yields sum to the plan');
