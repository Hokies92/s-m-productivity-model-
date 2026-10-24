"""Plain-text and JSON output."""
from __future__ import annotations

import json
from typing import Dict

from .engine import ScenarioResult, rank_levers
from .inputs import ModelInputs, ModelOptions


def _m(x: float) -> str:
    return f"{x / 1e6:,.2f}M"


def _signed_m(x: float) -> str:
    return f"{x / 1e6:+,.2f}M"


def text_report(results: Dict[str, ScenarioResult], inputs: ModelInputs,
                options: ModelOptions) -> str:
    b = results["baseline"]
    out = []
    mode = "original workbook logic" if options.is_workbook_faithful else "modified logic"
    out.append(f"SALES CAPACITY MODEL  ({mode}; salary={'entered' if options.use_entered_salary else 'workbook 87,750'}, "
               f"ramp rule={options.ramp_rule})")
    out.append("")
    out.append("CAPACITY (per territory)")
    out.append(f"  {inputs.manageable_opportunities:g} opportunities held x (12 / {inputs.cycle_months:g} months) "
               f"= {b.max_opportunities:,.1f} opportunities / year")
    out.append(f"  x {inputs.close_rate:.1%} close rate = {b.deals_per_rep:,.1f} deals "
               f"x {inputs.deal_size:,.0f} = {b.revenue_per_rep:,.0f} revenue / rep")
    if b.capacity_utilization is not None:
        out.append(f"  Leads {inputs.leads_per_territory:g} vs capacity {b.max_opportunities:,.1f}: "
                   f"utilization {b.capacity_utilization:.0%}, excess leads {b.excess_leads_per_territory:,.1f}")
    out.append("")
    hdr = f"  {'Scenario':28}{'Revenue':>11}{'ΔRevenue':>11}{'ΔSales cost':>12}{'Op. income':>12}{'ΔOI':>11}{'ΔOI %':>8}{'Net gain':>10}{'S&M ROI':>9}"
    out.append("RESULTS")
    out.append(hdr)
    out.append("  " + "-" * (len(hdr) - 2))
    for r in results.values():
        ng = "" if r.pct_net_gain is None else f"{r.pct_net_gain:+.1%}"
        out.append(f"  {r.label:28}{_m(r.revenue):>11}{_signed_m(r.revenue_change):>11}"
                   f"{_signed_m(r.sales_cost_change):>12}{_m(r.operating_income):>12}"
                   f"{_signed_m(r.operating_income_change):>11}{r.operating_income_change_pct:>+8.1%}"
                   f"{ng:>10}{r.sm_roi:>9.2f}")
    out.append("")
    out.append("LEVER RANKING (by change in operating income)")
    for n, r in enumerate(rank_levers(results), 1):
        out.append(f"  {n}. {r.label:24}{_signed_m(r.operating_income_change):>10}")
    out.append("")
    out.append("Net gain = (ΔRevenue - ΔSales cost) / baseline revenue, as the workbook defines it.")
    if options.ramp_rule == "workbook" and inputs.ramp_months > 0:
        out.append("Note: 'Improve all' gives new territories full-year revenue while 'Add territories' "
                   "applies ramp (AUDIT_FINDINGS F3).")
    return "\n".join(out)


def json_report(results: Dict[str, ScenarioResult], inputs: ModelInputs,
                options: ModelOptions) -> str:
    from dataclasses import asdict
    payload = {
        "inputs": inputs.to_dict(),
        "derived_inputs": {"fully_loaded_salary": inputs.fully_loaded_salary,
                           "travel": inputs.travel, "sales_overhead": inputs.sales_overhead,
                           "marketing": inputs.marketing},
        "options": asdict(options),
        "results": {k: v.to_dict() for k, v in results.items()},
        "lever_ranking": [r.scenario for r in rank_levers(results)],
    }
    return json.dumps(payload, indent=2)
