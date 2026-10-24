import json
import math

import pytest

from sales_capacity_model import (Adjustments, ModelInputs, ModelOptions, max_opportunities,
                                  obstacles, rank_levers, run_scenarios, verify)
from sales_capacity_model.cli import main


def test_engine_reproduces_every_workbook_output():
    checks = verify()
    assert len(checks) == 48
    bad = [c for c in checks if not c.ok]
    assert not bad, bad


def test_capacity_equation():
    assert max_opportunities(30, 6) == 60
    assert math.isclose(max_opportunities(30, 5.4), 66.6667, rel_tol=1e-4)


def test_derived_inputs_match_workbook_data_entry():
    i = ModelInputs()
    assert i.fully_loaded_salary == pytest.approx(116_850)
    assert i.travel == 47_500
    assert i.sales_overhead == 10_800_000
    assert i.marketing == 3_700_000


def test_quality_levers_beat_territories_under_every_ramp_rule():
    for rule in ("workbook", "year_one", "steady_state"):
        for salary in (False, True):
            r = run_scenarios(options=ModelOptions(use_entered_salary=salary, ramp_rule=rule))
            ranking = [x.scenario for x in rank_levers(r)]
            assert ranking[-1] == "territories", (rule, salary, ranking)


def test_ramp_rules():
    wb = run_scenarios(options=ModelOptions(ramp_rule="workbook"))
    y1 = run_scenarios(options=ModelOptions(ramp_rule="year_one"))
    ss = run_scenarios(options=ModelOptions(ramp_rule="steady_state"))
    assert wb["territories"].revenue_change == 0                 # F2: 12-month ramp, no year-1 revenue
    assert ss["territories"].revenue_change == pytest.approx(11_250_000)
    assert y1["all"].revenue == pytest.approx(y1["combined_quality"].revenue)  # consistent rule
    assert wb["all"].revenue == pytest.approx(ss["all"].revenue)   # F3: workbook gives full credit


def test_entered_salary_option():
    r = run_scenarios(options=ModelOptions(use_entered_salary=True))
    assert r["baseline"].salary == pytest.approx(116_850)
    assert r["baseline"].rep_costs == pytest.approx(22_525_000 + 2_910_000)


def test_lead_constraint_extension():
    under = run_scenarios(ModelInputs(leads_per_territory=40))["baseline"]
    assert under.opportunities_worked == 40 and under.capacity_utilization == pytest.approx(40 / 60)
    over = run_scenarios(ModelInputs(leads_per_territory=100))["baseline"]
    assert over.revenue == run_scenarios()["baseline"].revenue    # extra leads add nothing
    assert over.excess_leads_per_territory == 40


def test_custom_adjustments():
    r = run_scenarios(options=ModelOptions(adjustments=Adjustments(close_rate=0.2)))
    assert r["close_rate"].close_rate == pytest.approx(0.30)
    assert r["deal_size"].deal_size == pytest.approx(82_500)


def test_input_validation():
    with pytest.raises(ValueError):
        ModelInputs.from_dict({"close_rat": 0.3})
    with pytest.raises(ValueError):
        ModelInputs.from_dict({"cycle_months": 0})
    with pytest.raises(ValueError):
        ModelOptions(ramp_rule="sometimes")


def test_diagnostics():
    assert len(obstacles("close_rate")) == 5
    with pytest.raises(ValueError):
        obstacles("territories")


def test_cli(capsys, tmp_path):
    assert main(["about"]) == 0 and "SALES CAPACITY MODEL" in capsys.readouterr().out
    assert main(["overview"]) == 0 and "PRODUCT OVERVIEW" in capsys.readouterr().out
    assert main(["verify"]) == 0 and "48/48" in capsys.readouterr().out
    f = tmp_path / "in.json"
    f.write_text(json.dumps({"territories": 40}))
    assert main(["run", "--inputs", str(f), "--set", "close_rate=0.3", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["inputs"]["territories"] == 40 and out["inputs"]["close_rate"] == 0.3
    assert main(["run", "--set", "nope=1"]) == 2
