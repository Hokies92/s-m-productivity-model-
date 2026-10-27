"""Calculation engine.

The throughput chain (per territory):

    max_opportunities = manageable_opportunities x (12 / cycle_months)
    deals             = opportunities_worked x close_rate
    revenue_per_salesperson   = deals x deal_size
    cost_per_salesperson      = salary + travel + revenue_per_salesperson x commission_rate

Scaled by territories, then carried to the income statement:

    sales_costs       = territories x cost_per_salesperson + sales_overhead
    sm_costs          = sales_costs + marketing
    opex              = revenue x (cogs% + rnd% + gna%) + sm_costs
    operating_income  = revenue - opex

Workbook metrics (kept exactly as the original computes them):

    pct_net_gain = (Δrevenue - Δsales_costs) / baseline_revenue
    sm_roi       = (revenue - sm_costs) / sm_costs
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Optional

from .inputs import WORKBOOK_ENGINE_SALARY, ModelInputs, ModelOptions

SCENARIOS = ("baseline", "territories", "close_rate", "cycle_time",
             "deal_size", "combined_quality", "all")

SCENARIO_LABELS = {
    "baseline": "Baseline",
    "territories": "Add territories",
    "close_rate": "Raise close rate",
    "cycle_time": "Shorten sales cycle",
    "deal_size": "Raise deal size",
    "combined_quality": "Close + cycle + deal size",
    "all": "Improve all",
}


@dataclass
class ScenarioResult:
    scenario: str
    label: str
    # levers as applied
    territories: float
    deal_size: float
    cycle_months: float
    close_rate: float
    # throughput (per territory)
    max_opportunities: float
    opportunities_worked: float
    deals_per_salesperson: float
    revenue_per_salesperson: float
    # cost (per territory)
    salary: float
    travel: float
    commission_per_salesperson: float
    cost_per_salesperson: float
    # totals
    revenue: float
    salesperson_costs: float
    sales_overhead: float
    sales_costs: float
    marketing: float
    sm_costs: float
    cost_of_revenue: float
    rnd: float
    gna: float
    opex: float
    operating_income: float
    sm_roi: float
    # vs baseline (filled by run_scenarios)
    revenue_change: float = 0.0
    sales_cost_change: float = 0.0
    operating_income_change: float = 0.0
    operating_income_change_pct: float = 0.0
    pct_net_gain: Optional[float] = None
    # optional lead diagnostic
    leads_per_territory: Optional[float] = None
    capacity_utilization: Optional[float] = None
    excess_leads_per_territory: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)


def max_opportunities(manageable: float, cycle_months: float) -> float:
    """Capacity = cognitive load limit x inventory turns per year."""
    return manageable * (12.0 / cycle_months)


def _revenue(scenario: str, T: float, T0: float, rev_salesperson: float,
             base_rev_salesperson: float, ramp_factor: float, rule: str) -> float:
    """Total revenue, including how added territories are credited.

    ramp_factor = share of the year a new territory produces = (12 - ramp) / 12.
    """
    new_T = T - T0
    if new_T == 0 or rule == "steady_state":
        return T * rev_salesperson
    if rule == "year_one":
        return T0 * rev_salesperson + ramp_factor * new_T * rev_salesperson
    # rule == "workbook": reproduce the original, including its inconsistency
    if scenario == "territories":                       # workbook E25 ((12 - ramp)/12 credit)
        return ramp_factor * new_T * rev_salesperson + T0 * rev_salesperson
    if scenario == "all":                               # workbook K25 (ramp credited a second way; canonical/FOUNDATION.md section 4)
        return T * rev_salesperson - ramp_factor * new_T * base_rev_salesperson
    return T * rev_salesperson


def compute_scenario(scenario: str, inputs: ModelInputs, options: ModelOptions,
                     T: float, D: float, Y: float, R: float) -> ScenarioResult:
    i = inputs
    salary = i.fully_loaded_salary if options.use_entered_salary else WORKBOOK_ENGINE_SALARY
    travel = i.travel

    max_opps = max_opportunities(i.manageable_opportunities, Y)
    worked = max_opps
    util = excess = None
    if i.leads_per_territory is not None:
        worked = min(max_opps, i.leads_per_territory)
        util = worked / max_opps if max_opps else 0.0
        excess = max(0.0, i.leads_per_territory - max_opps)

    deals = worked * R
    rev_salesperson = deals * D
    comm = rev_salesperson * i.commission_rate
    cost_salesperson = salary + travel + comm

    base_worked = max_opportunities(i.manageable_opportunities, i.cycle_months)
    if i.leads_per_territory is not None:
        base_worked = min(base_worked, i.leads_per_territory)
    base_rev_salesperson = base_worked * i.close_rate * i.deal_size
    ramp_factor = (12.0 - i.ramp_months) / 12.0

    revenue = _revenue(scenario, T, i.territories, rev_salesperson, base_rev_salesperson,
                       ramp_factor, options.ramp_rule)
    salesperson_costs = T * cost_salesperson
    sales_costs = salesperson_costs + i.sales_overhead
    sm = sales_costs + i.marketing
    cogs, rnd, gna = revenue * i.cogs_pct, revenue * i.rnd_pct, revenue * i.gna_pct
    opex = cogs + rnd + gna + sm
    oi = revenue - opex

    return ScenarioResult(
        scenario=scenario, label=SCENARIO_LABELS[scenario],
        territories=T, deal_size=D, cycle_months=Y, close_rate=R,
        max_opportunities=max_opps, opportunities_worked=worked,
        deals_per_salesperson=deals, revenue_per_salesperson=rev_salesperson,
        salary=salary, travel=travel, commission_per_salesperson=comm, cost_per_salesperson=cost_salesperson,
        revenue=revenue, salesperson_costs=salesperson_costs, sales_overhead=i.sales_overhead,
        sales_costs=sales_costs, marketing=i.marketing, sm_costs=sm,
        cost_of_revenue=cogs, rnd=rnd, gna=gna, opex=opex, operating_income=oi,
        sm_roi=(revenue - sm) / sm if sm else float("nan"),
        leads_per_territory=i.leads_per_territory,
        capacity_utilization=util, excess_leads_per_territory=excess,
    )


def run_scenarios(inputs: Optional[ModelInputs] = None,
                  options: Optional[ModelOptions] = None) -> Dict[str, ScenarioResult]:
    """Run baseline plus every lever scenario. Returns results keyed by scenario name."""
    inputs = inputs or ModelInputs()
    options = options or ModelOptions()
    inputs.validate()
    a = options.adjustments
    T, D, Y, R = inputs.territories, inputs.deal_size, inputs.cycle_months, inputs.close_rate
    T1, D1 = T * (1 + a.territories), D * (1 + a.deal_size)
    Y1, R1 = Y * (1 - a.cycle_time), R * (1 + a.close_rate)
    if Y1 <= 0:
        raise ValueError("cycle_time adjustment must be < 1.0")

    plan = {
        "baseline": (T, D, Y, R),
        "territories": (T1, D, Y, R),
        "close_rate": (T, D, Y, R1),
        "cycle_time": (T, D, Y1, R),
        "deal_size": (T, D1, Y, R),
        "combined_quality": (T, D1, Y1, R1),
        "all": (T1, D1, Y1, R1),
    }
    results = {name: compute_scenario(name, inputs, options, *levers)
               for name, levers in plan.items()}

    b = results["baseline"]
    for r in results.values():
        r.revenue_change = r.revenue - b.revenue
        r.sales_cost_change = r.sales_costs - b.sales_costs
        r.operating_income_change = r.operating_income - b.operating_income
        r.operating_income_change_pct = (r.operating_income_change / b.operating_income
                                         if b.operating_income else float("nan"))
        if r.scenario != "baseline":
            r.pct_net_gain = ((r.revenue_change - r.sales_cost_change) / b.revenue
                              if b.revenue else float("nan"))
    return results


def rank_levers(results: Dict[str, ScenarioResult], by: str = "operating_income_change"):
    """Single-lever scenarios ordered best to worst on the chosen metric."""
    singles = ["territories", "close_rate", "cycle_time", "deal_size"]
    return sorted((results[s] for s in singles), key=lambda r: getattr(r, by), reverse=True)
