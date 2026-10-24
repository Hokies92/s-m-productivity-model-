"""Prove the engine reproduces the original workbook.

Compares every stored output on the workbook's Impact Analysis sheet
(exported to data/workbook_cells.csv) against the engine at default inputs
and workbook-faithful options.
"""
from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from importlib import resources
from typing import List

from .engine import run_scenarios
from .inputs import ModelInputs, ModelOptions

# Workbook column -> scenario; workbook row -> result attribute
COLUMNS = {"C": "baseline", "E": "territories", "F": "close_rate", "G": "cycle_time",
           "H": "deal_size", "J": "combined_quality", "K": "all"}
ROWS = {"8": "revenue", "13": "sales_costs", "15": "sm_costs", "22": "opex",
        "23": "operating_income", "26": "pct_net_gain", "27": "sm_roi"}


@dataclass
class Check:
    scenario: str
    metric: str
    workbook: float
    engine: float

    @property
    def ok(self) -> bool:
        return abs(self.engine - self.workbook) <= max(1e-6, abs(self.workbook) * 1e-9)


def load_workbook_cells() -> List[dict]:
    text = resources.files("sales_capacity_model.data").joinpath("workbook_cells.csv").read_text()
    return list(csv.DictReader(io.StringIO(text)))


def verify() -> List[Check]:
    results = run_scenarios(ModelInputs(), ModelOptions())
    checks = []
    for row in load_workbook_cells():
        if row["sheet"] != "3) Impact Analysis":
            continue
        col, r = row["cell"][0], row["cell"][1:]
        if col in COLUMNS and r in ROWS and row["value"] not in ("", "None"):
            scen, metric = COLUMNS[col], ROWS[r]
            checks.append(Check(scen, metric, float(row["value"]),
                                float(getattr(results[scen], metric))))
    return sorted(checks, key=lambda c: (c.scenario, c.metric))
