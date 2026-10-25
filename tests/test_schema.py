"""The data module schema, exercised with the as-is sample data."""
import sqlite3

import pytest

from sales_capacity_model.db import create


@pytest.fixture
def con():
    c = create()
    x = c.execute
    x("INSERT INTO client VALUES ('c1', 'Sample Co', CURRENT_TIMESTAMP)")
    x("""INSERT INTO engagement (engagement_id, client_id, scope, period_start, period_end, currency, revenue_basis)
         VALUES ('e1', 'c1', 'whole company', '2025-01-01', '2025-12-31', 'USD', 'recognized')""")
    x("INSERT INTO contributor VALUES ('p_lead', 'e1', 'Sales Leader', NULL, 'sales_leader')")
    x("INSERT INTO contributor VALUES ('p_fin', 'e1', 'Controller', NULL, 'finance')")
    x("INSERT INTO baseline_version (baseline_version_id, engagement_id, state) VALUES ('b1', 'e1', 'working')")
    x("INSERT INTO entity (entity_id, engagement_id, entity_type) VALUES ('co', 'e1', 'company')")
    x("""INSERT INTO source_document (document_id, engagement_id, step_no, kind, filename, content_hash)
         VALUES ('d_is', 'e1', 3, 'income_statement', 'fy25_is.pdf', 'sha256:x')""")
    return c


def assume(c, aid, field, entity="co"):
    c.execute("INSERT INTO assumption (assumption_id, baseline_version_id, field_id, entity_id) VALUES (?, 'b1', ?, ?)",
              (aid, field, entity))


def value(c, vid, aid, seq, num, basis, statement, **kw):
    cols = ["value_id", "assumption_id", "seq", "value_num", "basis", "statement"] + list(kw)
    c.execute(f"INSERT INTO assumption_value ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
              [vid, aid, seq, num, basis, statement] + list(kw.values()))


def test_schema_and_seed_load():
    c = create()
    assert c.execute("SELECT COUNT(*) FROM collection_step").fetchone()[0] == 11
    assert c.execute("SELECT COUNT(*) FROM field WHERE level = 'model'").fetchone()[0] == 9
    levels = {r[0] for r in c.execute("SELECT DISTINCT leverage_point FROM field")}
    assert {2, 3, 4, 5, 6, 8, 9, 10, 11, 12} <= levels


def test_reference_value_and_perception_gap(con):
    # Step 2: the sales leader's sealed belief, before any data
    assume(con, "a_deal", "deal_size")
    value(con, "v_belief", "a_deal", 1, 75000, "judgment", "Our average deal is about $75,000",
          low=60000, high=90000, sealed_belief=1, asserted_by="p_lead", collection_step=2)
    # Step 3: Finance's actuals
    assume(con, "a_rev", "revenue")
    value(con, "v_rev", "a_rev", 1, 25_000_000, "validated_actual", "Revenue for FY25 was $25.0M", collection_step=3)
    assume(con, "a_con", "contracts")
    value(con, "v_con", "a_con", 1, 755, "validated_actual", "755 contracts closed in FY25", collection_step=3)
    con.execute("INSERT INTO assumption_validation (validation_id, value_id, validated_by, decision) VALUES ('x1', 'v_rev', 'p_fin', 'validated')")
    # Estimator: deal size from revenue ÷ contracts, with lineage
    value(con, "v_deal_est", "a_deal", 2, 25_000_000 / 755, "calculated_estimate",
          "Revenue ÷ contracts gives an average deal of $33,113", method="revenue_div_contracts",
          supersedes_value_id="v_belief")
    con.executemany("INSERT INTO assumption_input VALUES (?, ?)", [("v_deal_est", "v_rev"), ("v_deal_est", "v_con")])

    gap = con.execute("SELECT believed, current FROM v_perception_gap WHERE field_id = 'deal_size'").fetchone()
    assert gap[0] == 75000 and round(gap[1]) == 33113
    validated = con.execute("SELECT validated FROM v_current_value WHERE assumption_id = 'a_rev'").fetchone()[0]
    assert validated == 1


def test_reference_value_requires_context(con):
    assume(con, "a_deal", "deal_size")
    with pytest.raises(sqlite3.IntegrityError):
        value(con, "v1", "a_deal", 1, 75000, "reference_value", "Deal size from another client", low=60000, high=90000)
    value(con, "v2", "a_deal", 1, 75000, "reference_value", "Deal size from another client",
          low=60000, high=90000, reference_context="Enterprise software client, 2000")


def test_append_only_and_sealing(con):
    assume(con, "a_cap", "opportunities_capacity")
    value(con, "v1", "a_cap", 1, 30, "judgment", "A salesperson can hold 30 opportunities", low=25, high=35, sealed_belief=1)
    with pytest.raises(sqlite3.DatabaseError, match="append-only"):
        con.execute("UPDATE assumption_value SET value_num = 40 WHERE value_id = 'v1'")
    with pytest.raises(sqlite3.DatabaseError, match="sealed belief"):
        value(con, "v2", "a_cap", 2, 32, "judgment", "Revised belief", low=25, high=35, sealed_belief=1)


def test_only_finance_validates(con):
    assume(con, "a_rev", "revenue")
    value(con, "v_rev", "a_rev", 1, 25_000_000, "validated_actual", "Revenue was $25.0M")
    with pytest.raises(sqlite3.DatabaseError, match="Finance"):
        con.execute("INSERT INTO assumption_validation (validation_id, value_id, validated_by, decision) VALUES ('x', 'v_rev', 'p_lead', 'validated')")


def test_signed_baseline_is_frozen(con):
    assume(con, "a_rev", "revenue")
    value(con, "v_rev", "a_rev", 1, 25_000_000, "validated_actual", "Revenue was $25.0M")
    con.execute("UPDATE baseline_version SET state = 'signed', signed_by = 'p_fin', signed_at = '2026-01-15' WHERE baseline_version_id = 'b1'")
    with pytest.raises(sqlite3.DatabaseError, match="frozen"):
        value(con, "v_rev2", "a_rev", 2, 26_000_000, "validated_actual", "Revenue restated")
    with pytest.raises(sqlite3.DatabaseError, match="frozen"):
        con.execute("UPDATE baseline_version SET state = 'working' WHERE baseline_version_id = 'b1'")


def test_territory_salesperson_assignment_and_vacancy(con):
    x = con.execute
    for eid, typ in [("t1", "territory"), ("t2", "territory"), ("sp1", "salesperson"), ("as1", "assignment")]:
        x("INSERT INTO entity (entity_id, engagement_id, entity_type) VALUES (?, 'e1', ?)", (eid, typ))
    x("INSERT INTO territory (entity_id, external_ref) VALUES ('t1', 'NE-01'), ('t2', 'NE-02')")
    x("INSERT INTO salesperson (entity_id, pseudonym, start_date) VALUES ('sp1', 'h:9f2c', '2023-04-01')")
    x("INSERT INTO assignment (entity_id, territory_id, salesperson_id, valid_from) VALUES ('as1', 't1', 'sp1', '2023-04-01')")
    for i, (etype, d) in enumerate([("vacancy_opened", "2025-02-01"), ("requisition_approved", "2025-04-15"),
                                    ("offer_accepted", "2025-06-01"), ("salesperson_started", "2025-07-01")]):
        x("INSERT INTO event (event_id, entity_id, episode_id, event_type, event_date) VALUES (?, 't2', 'vac1', ?, ?)",
          (f"ev{i}", etype, d))
    open_terr = x("SELECT external_ref FROM v_territory_assignment_share WHERE salesperson_id IS NULL").fetchall()
    assert open_terr == [("NE-02",)]
    stage = x("SELECT opened, approved, started FROM v_vacancy_stages WHERE episode_id = 'vac1'").fetchone()
    assert stage == ("2025-02-01", "2025-04-15", "2025-07-01")


def test_failed_test_exposes_candidate_set(con):
    for aid, field, num in [("a_t", "territory_count", 100), ("a_cap", "opportunities_capacity", 30),
                            ("a_cyc", "cycle_months", 6), ("a_wr", "win_rate", 0.25), ("a_rev", "revenue", 25e6)]:
        assume(con, aid, field)
        value(con, "v_" + aid, aid, 1, num, "judgment" if field != "revenue" else "validated_actual",
              f"{field} = {num}", **({"low": num * 0.8, "high": num * 1.2} if field != "revenue" else {}))
    con.execute("""INSERT INTO test_run (run_id, baseline_version_id, test_id, implied_value, observed_value, gap, outcome, engine_version)
                   VALUES ('r1', 'b1', 'contracts_implication', 1500, 755, -745, 'fail', '2.1.0')""")
    con.executemany("INSERT INTO test_run_input VALUES ('r1', ?)",
                    [("v_a_t",), ("v_a_cap",), ("v_a_cyc",), ("v_a_wr",)])
    candidates = {r[0] for r in con.execute("SELECT field_id FROM v_candidate_set WHERE run_id = 'r1'")}
    assert candidates == {"territory_count", "opportunities_capacity", "cycle_months", "win_rate"}
    con.execute("""INSERT INTO resolution (resolution_id, run_id, action, category, note, resolved_by)
                   VALUES ('s1', 'r1', 'explained', 'data_quality', 'Salespeople hold ~15 opportunities, not 30', 'p_fin')""")
    assert con.execute("SELECT COUNT(*) FROM v_candidate_set WHERE run_id = 'r1'").fetchone()[0] == 0
    profile = dict(con.execute("SELECT basis, n FROM v_confidence_profile").fetchall())
    assert profile == {"judgment": 4, "validated_actual": 1}
