"""Sales Capacity Model: sales capacity as cognitive bandwidth constrained by time.

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
