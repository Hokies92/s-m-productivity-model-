"""Sales Capacity Model: the as-is oracle.

This package reproduces the original 2000 workbook exactly, per territory, and is the
reference every rebuild is tested against (tests/test_model.py, tests/test_asis_workbook.py).
The model is stated in docs/MODEL.md; the blank modern workbook is built by tools/build_asis_modern.py.

    from sales_capacity_model import ModelInputs, ModelOptions, run_scenarios
    results = run_scenarios(ModelInputs(close_rate=0.3))
    results["close_rate"].operating_income_change
"""
from .__about__ import ABOUT, OVERVIEW, __author__, __summary__, __version__
from .diagnostics import DIAGNOSTICS, obstacles
from .engine import (SCENARIOS, ScenarioResult, compute_scenario, max_opportunities,
                     rank_levers, run_scenarios)
from .inputs import Adjustments, ModelInputs, ModelOptions
from .verify import verify

__all__ = [
    "ABOUT", "OVERVIEW", "__version__", "__author__", "__summary__",
    "ModelInputs", "ModelOptions", "Adjustments",
    "run_scenarios", "compute_scenario", "max_opportunities", "rank_levers",
    "ScenarioResult", "SCENARIOS", "DIAGNOSTICS", "obstacles", "verify",
]
