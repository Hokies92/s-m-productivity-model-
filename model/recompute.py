"""
Recompute the Sales Capacity Model exactly as the original workbook does,
then check every result against the values stored in the workbook.

Run:  python3 model/recompute.py
Exit code 0 = every output matches the workbook.

Logic reproduced from source/workbook_cells.csv (the formula export).
Known workbook quirks are reproduced on purpose, not fixed; see AUDIT_FINDINGS.md.
"""
import csv, os, sys

INPUTS = {
    "territories": 100,
    "deal_size": 75000,
    "loaded_salary_used": 87750,   # hard-coded in Performance Breakdown (finding F1)
    "loaded_salary_entered": 116850,  # Data Entry value; never used downstream
    "travel": 47500,
    "commission_rate": 0.08,
    "manageable_opps": 30,
    "cycle_months": 6,
    "ramp_months": 12,
    "close_rate": 0.25,
    "sales_overhead": 10_800_000,
    "marketing": 3_700_000,
    "cogs_pct": 0.1322, "rnd_pct": 0.1019, "gna_pct": 0.154,
}
ADJ = 0.10

def scenario(name, T, D, Y, R, I=INPUTS):
    """One column of Performance Breakdown + Impact Analysis."""
    T0 = I["territories"]
    max_opps = (12 / Y) * I["manageable_opps"]
    deals = max_opps * R
    rev_rep = deals * D
    comm = rev_rep * I["commission_rate"]
    cost_rep = I["loaded_salary_used"] + I["travel"] + comm
    ramp_factor = (12 - I["ramp_months"]) / 12          # 0 when ramp = 12 months
    new_T = T - T0
    if name == "hire":
        # Hire column: new territories earn only the post-ramp share of a year (finding F2)
        revenue = ramp_factor * rev_rep * new_T + T0 * rev_rep
    elif name == "all":
        # 'Improve all' column subtracts the ramped share instead of the un-ramped share,
        # so new territories get full-year credit (finding F3)
        base_rev_rep = (12 / I["cycle_months"]) * I["manageable_opps"] * I["close_rate"] * I["deal_size"]
        revenue = T * rev_rep - ramp_factor * base_rev_rep * new_T
    else:
        revenue = T * rev_rep
    rep_costs = T * cost_rep
    sales_costs = rep_costs + I["sales_overhead"]
    sm = sales_costs + I["marketing"]
    opex = revenue * (I["cogs_pct"] + I["rnd_pct"] + I["gna_pct"]) + sm
    oi = revenue - opex
    return dict(max_opps=max_opps, deals=deals, rev_rep=rev_rep, commission=comm,
                cost_rep=cost_rep, revenue=revenue, rep_costs=rep_costs,
                sales_costs=sales_costs, sm_costs=sm, opex=opex, operating_income=oi,
                sm_roi=(revenue - sm) / sm)

def run(I=INPUTS, adj=ADJ):
    T, D, Y, R = I["territories"], I["deal_size"], I["cycle_months"], I["close_rate"]
    cols = {
        "baseline": scenario("baseline", T, D, Y, R, I),
        "hire":     scenario("hire", T * (1 + adj), D, Y, R, I),
        "close":    scenario("close", T, D, Y, R * (1 + adj), I),
        "cycle":    scenario("cycle", T, D, Y * (1 - adj), R, I),
        "deal":     scenario("deal", T, D * (1 + adj), Y, R, I),
        "combined": scenario("combined", T, D * (1 + adj), Y * (1 - adj), R * (1 + adj), I),
        "all":      scenario("all", T * (1 + adj), D * (1 + adj), Y * (1 - adj), R * (1 + adj), I),
    }
    b = cols["baseline"]
    for c in cols.values():
        # Workbook '% net gain' = (Δrevenue − Δsales costs) / baseline revenue (finding F4)
        c["pct_net_gain"] = ((c["revenue"] - b["revenue"]) - (c["sales_costs"] - b["sales_costs"])) / b["revenue"]
    return cols

# Workbook Impact Analysis columns: C baseline, E hire, F close, G cycle, H deal, J combined, K all
COLMAP = {"C": "baseline", "E": "hire", "F": "close", "G": "cycle", "H": "deal", "J": "combined", "K": "all"}
ROWMAP = {"8": "revenue", "13": "sales_costs", "15": "sm_costs", "22": "opex",
          "23": "operating_income", "26": "pct_net_gain", "27": "sm_roi"}

def check():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "source", "workbook_cells.csv")
    stored = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            if row["sheet"] == "3) Impact Analysis":
                col, r = row["cell"][0], row["cell"][1:]
                if col in COLMAP and r in ROWMAP and row["value"] not in ("", "None"):
                    stored[(COLMAP[col], ROWMAP[r])] = float(row["value"])
    cols, bad = run(), 0
    for (scen, metric), v in sorted(stored.items()):
        mine = cols[scen][metric]
        ok = abs(mine - v) <= max(1e-6, abs(v) * 1e-9)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {scen:9} {metric:17} workbook={v:>16,.4f} recomputed={mine:>16,.4f}")
    print(f"\n{len(stored) - bad}/{len(stored)} match")
    return bad == 0

if __name__ == "__main__":
    sys.exit(0 if check() else 1)
