"""Build the Commercial Effectiveness Model workbook.

Run:  python tools/build_workbook.py  ->  workbook/Commercial_Effectiveness_Model.xlsx

Structure: each tab has two worksheets.
  * A client view: only what the client enters or chooses, and the results.
  * A logic sheet: every calculation, one per row, with the rule written in words
    next to the live formula.

Data flow (one direction only):
  1) Data Entry (client inputs)  ->  1) Data Entry Logic (value used, named v_<id>)
  ->  2) What-If Logic (scenarios and pro forma income statement)  ->  2) What-If (client view)

Previous version (single ledger sheet, nine scenarios): tools/archive/build_workbook_ledger_v1.py

© 2000–2026 Growth Enablement. All rights reserved.
"""
from __future__ import annotations

import csv
import math
import pathlib

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "workbook" / "Commercial_Effectiveness_Model.xlsx"

DE = "1) Data Entry"
DL = "1) Data Entry Logic"
WI = "2) What-If"
WL = "2) What-If Logic"

# ---------------------------------------------------------------- styles
FONT = "Arial"
f_body = Font(name=FONT, size=10)
f_input = Font(name=FONT, size=10, color="0000FF")
f_bold = Font(name=FONT, size=10, bold=True)
f_head = Font(name=FONT, size=10, bold=True, color="FFFFFF")
f_title = Font(name=FONT, size=16, bold=True)
f_h2 = Font(name=FONT, size=12, bold=True)
f_note = Font(name=FONT, size=9, italic=True, color="595959")
f_link = Font(name=FONT, size=10, color="008000")          # green: pulled from another sheet
fill_input = PatternFill("solid", start_color="FFF2CC")    # yellow: enter or choose
fill_calc = PatternFill("solid", start_color="F2F2F2")     # grey: calculated
fill_used = PatternFill("solid", start_color="DDEBF7")     # blue: value the model uses / key result
fill_head = PatternFill("solid", start_color="1F3864")
fill_step = PatternFill("solid", start_color="D9E1F2")
fill_banner = PatternFill("solid", start_color="FCE4D6")
fill_total = PatternFill("solid", start_color="E2EFDA")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
top_line = Border(top=Side(style="thin", color="000000"), left=thin, right=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
center = Alignment(horizontal="center", vertical="top", wrap_text=True)

FMT = {"currency": '$#,##0;($#,##0);"-"', "pct": "0.0%", "count": "#,##0", "count1": "#,##0.0",
       "months": "0.0", "text": "@", "spct": '+0.0%;-0.0%;0.0%', "scur": '+$#,##0;-$#,##0;"-"'}
UNIT_LABEL = {"currency": "$", "pct": "%", "count": "count", "count1": "count", "months": "months"}

SOURCES = ["Validated by Finance", "Your entry", "Use our estimate"]
SAMPLE = "As-is model sample (illustrative)"


def row_height(text: str, chars_per_line: float, base: float = 13.0) -> float:
    lines = sum(max(1, math.ceil(len(p) / chars_per_line)) for p in str(text or "").split("\n"))
    return base * max(1, lines) + 4


# Original "Description" text from the as-is Data Entry sheet, word for word.
WHY_CELLS = {"territory_count": ["C9"], "deal_size": ["C11"], "loaded_salary": ["C15"],
             "travel_per_salesperson": ["C19"], "commission_rate": ["C28"], "opportunities_capacity": ["C31"],
             "cycle_months": ["C33"], "ramp_months": ["C35"], "win_rate": ["C37"],
             "sales_overhead": ["C39", "C41"], "marketing": ["C48"]}


def load_why() -> dict:
    cells = {}
    with open(ROOT / "source" / "workbook_cells.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["sheet"].strip() == "1) Data entry":
                cells[r["cell"]] = " ".join(r["formula_or_input"].split())
    return {k: "\n\n".join(cells[c] for c in v) for k, v in WHY_CELLS.items()}


WHY = load_why()

# ---------------------------------------------------------------- entries
# Collection order: the easiest sequence for a client to assemble, step by step.
STEPS = [
    (1, "Financial results", "Finance", "Income statement for the 12-month period in scope."),
    (2, "Sales and marketing costs", "Finance", "General ledger detail for sales and marketing cost centers; payroll; expense reports."),
    (3, "Territories and salespeople", "Sales Operations and HR", "Territory plan and the roster of quota-carrying salespeople."),
    (4, "Pipeline and sales mechanics", "Sales Operations", "CRM report of opportunities closed in the period, and month-end open opportunities."),
]

E: list[dict] = []


def add(step, id_, name, unit, what, default=None, est=None, est_words="", test="", used_by="", why_id=None):
    """default: a number (sample value), None (optional, no default), or "est" (default is our estimate)."""
    E.append(dict(step=step, id=id_, name=name, unit=unit, what=what, default=default, est=est,
                  est_words=est_words, test=test, used_by=used_by, why=WHY.get(why_id or id_, "")))


# Step 1. Financial results
add(1, "revenue", "Revenue", "currency", "Revenue for the period and scope (income statement).", 25_000_000,
    test="Model baseline revenue differs from it (revenue check)", used_by="Checks: revenue, deal size, commission")
add(1, "contracts", "Contracts closed", "count", "Executed agreements in the period that produced that revenue.", 755,
    test="Won opportunities in the CRM differ; model contracts differ (contracts check)", used_by="Checks: contracts, deal size")
add(1, "cost_of_revenue_amt", "Cost of revenue ($), optional", "currency", "Direct cost of delivering that revenue. Lets us estimate the % below.",
    used_by="Estimate of cost of revenue %")
add(1, "cost_of_revenue_pct", "Cost of revenue, % of revenue", "pct", "Cost of revenue ÷ revenue.", 0.1322,
    est="{cost_of_revenue_amt}/{revenue}", est_words="Cost of revenue ($) ÷ revenue",
    test="Income statement history shows a different ratio or a fixed part", used_by="Income statement: cost of revenue")
add(1, "rnd_amt", "Research and development ($), optional", "currency", "R&D expense for the period.", used_by="Estimate of R&D %")
add(1, "rnd_pct", "R&D, % of revenue", "pct", "R&D ÷ revenue.", 0.1019, est="{rnd_amt}/{revenue}",
    est_words="R&D ($) ÷ revenue", test="R&D does not move with revenue", used_by="Income statement: R&D")
add(1, "gna_amt", "General and administrative ($), optional", "currency", "G&A expense for the period.", used_by="Estimate of G&A %")
add(1, "gna_pct", "G&A, % of revenue", "pct", "G&A ÷ revenue.", 0.154, est="{gna_amt}/{revenue}",
    est_words="G&A ($) ÷ revenue", test="G&A does not move with revenue", used_by="Income statement: G&A")

# Step 2. Sales and marketing costs
add(2, "base_salary", "Average base salary per salesperson", "currency",
    "Quota-carrying salespeople only; excludes managers, sales engineers and executives (payroll).", 95_000,
    used_by="Estimate of fully loaded salary")
add(2, "load_rate", "Benefits and payroll tax load", "pct", "Benefits and payroll taxes ÷ base salary.", 0.23,
    used_by="Estimate of fully loaded salary")
add(2, "loaded_salary", "Fully loaded salary per salesperson", "currency", "Base salary plus benefits and payroll taxes.",
    "est", est="{base_salary}*(1+{load_rate})", est_words="Base salary × (1 + load)",
    test="Payroll for quota-carrying salespeople ÷ salespeople differs", used_by="Income statement: salesperson pay")
for i, (tid, tname, tdef, tval) in enumerate([
        ("trip_fare", "Travel per trip: air, train, mileage", "Round trip, one salesperson.", 750),
        ("trip_ground", "Travel per trip: cabs, tolls, rental", "Per trip.", 200),
        ("trip_meals", "Meals per day", "Breakfast, lunch, dinner.", 100),
        ("trip_lodging", "Lodging per night", "Average room cost.", 250),
        ("trip_days", "Days per trip", "Days away per trip.", 2),
        ("trip_entertainment", "Entertainment per trip", "Client meals and events per trip.", 250),
        ("trips_per_year", "Trips per year", "Sales trips per salesperson per year.", 25)]):
    add(2, tid, tname, "count" if tid in ("trip_days", "trips_per_year") else "currency", tdef, tval,
        used_by="Estimate of travel per salesperson")
add(2, "travel_per_salesperson", "Travel cost per salesperson", "currency",
    "Best: travel and entertainment ledger for quota salespeople ÷ salespeople. Otherwise use the trip build-up above.", "est",
    est="(({trip_fare}+{trip_ground}+{trip_entertainment})+{trip_days}*({trip_meals}+{trip_lodging}))*{trips_per_year}",
    est_words="(fare + ground + entertainment + days × (meals + lodging)) × trips per year",
    test="Travel ledger for quota salespeople differs", used_by="Income statement: salesperson travel")
add(2, "commissions_paid", "Commissions paid ($), optional", "currency", "Commission expense for quota salespeople in the period.",
    used_by="Estimate and check of commission rate")
add(2, "commission_rate", "Commission rate", "pct", "Commission as a share of revenue (compensation plan).", 0.08,
    est="{commissions_paid}/{revenue}", est_words="Commissions paid ÷ revenue",
    test="Commissions paid ÷ revenue differs from the plan rate (commission check)", used_by="Income statement: commissions")
for oid, oname, odef, oval in [
        ("oh_managers", "Non-quota sales manager salaries", "Managers who carry no quota.", 2_750_000),
        ("oh_engineers", "Sales engineers and other non-quota support", "Pre-sales and support roles.", 6_000_000),
        ("oh_admin", "Sales operations and administration", "Sales ops and admin staff.", 800_000),
        ("oh_training", "Training", "Training, travel for training, related headcount.", 500_000),
        ("oh_incentives", "Non-quota incentives", "Contests, recognition trips, non-quota commissions.", 750_000)]:
    add(2, oid, oname, "currency", odef, oval, used_by="Estimate of sales overhead")
add(2, "sales_overhead", "Sales overhead (total)", "currency", "Non-variable cost of running the sales organization.", "est",
    est="{oh_managers}+{oh_engineers}+{oh_admin}+{oh_training}+{oh_incentives}", est_words="Sum of the five lines above",
    test="Ledger total for sales overhead differs", used_by="Income statement: sales overhead")
for mid, mname, mdef, mval in [
        ("mk_people", "Marketing personnel", "All marketing staff.", 1_000_000),
        ("mk_web", "Website", "Website investment and maintenance.", 250_000),
        ("mk_events", "Events", "Online events and roadshows.", 500_000),
        ("mk_ads", "Advertising", "Paid media.", 500_000),
        ("mk_mail", "Direct mail", "Print and online.", 250_000),
        ("mk_leadgen", "Lead generation programs", "Telemarketing and other lead generation.", 250_000),
        ("mk_brand", "Branding and public relations", "Identity, PR, consulting.", 200_000),
        ("mk_collateral", "Collateral", "Sales tools, white papers, brochures, printing.", 750_000)]:
    add(2, mid, mname, "currency", mdef, mval, used_by="Estimate of marketing")
add(2, "marketing", "Marketing (total)", "currency", "Investment the company makes to help drive revenue.", "est",
    est="{mk_people}+{mk_web}+{mk_events}+{mk_ads}+{mk_mail}+{mk_leadgen}+{mk_brand}+{mk_collateral}",
    est_words="Sum of the eight lines above", test="Ledger total for marketing differs", used_by="Income statement: marketing")

# Step 3. Territories and salespeople
add(3, "territory_count", "Funded territories", "count",
    "Territories the company has decided to fund, filled or open. A territory is a design choice, not a person.", 100,
    test="Filled + open territories differ from this count (territory check)", used_by="Estimate of salespeople; territory check")
add(3, "open_territories", "Open territories at period end", "count", "Funded territories with no salesperson assigned.", 0,
    test="Roster and territory plan disagree", used_by="Estimate of salespeople; territory check")
add(3, "filled_seats", "Quota-carrying salespeople", "count",
    "People in quota-carrying roles at period end (roster, no names). If blank, funded − open territories.", "est",
    est="{territory_count}-{open_territories}", est_words="Funded territories − open territories",
    test="Roster count differs from filled territories", used_by="Every scenario: number of salespeople")
add(3, "ramp_months", "Ramp time (months)", "months", "Months until a new salesperson reaches average productivity.", 12,
    test="New-hire productivity by month differs", used_by="Not used by the four scenarios; used by later hiring and territory scenarios")

# Step 4. Pipeline and sales mechanics
add(4, "opps_won", "Qualified opportunities won, optional", "count", "Closed as won in the period (CRM).",
    used_by="Estimate and check of close rate")
add(4, "opps_lost", "Qualified opportunities lost, optional", "count", "Closed as lost in the period (CRM).",
    used_by="Estimate and check of close rate")
add(4, "win_rate", "Close rate", "pct", "Won ÷ (won + lost) qualified opportunities, by count.", 0.25,
    est="{opps_won}/({opps_won}+{opps_lost})", est_words="Won ÷ (won + lost)",
    test="CRM won ÷ (won + lost) differs (close rate check)", used_by="Every scenario: close rate")
add(4, "cycle_months", "Sales cycle (months)", "months",
    "Median months from qualified opportunity to signature, for won deals (CRM).", 6,
    test="CRM median cycle differs; Little's Law check fails", used_by="Every scenario: cycle time")
add(4, "deal_size", "Average revenue per contract", "currency", "Average deal size. Our estimate is revenue ÷ contracts.", 75_000,
    est="{revenue}/{contracts}", est_words="Revenue ÷ contracts",
    test="Revenue ÷ contracts differs (deal size check)", used_by="Every scenario: deal size")
add(4, "open_opps_total", "Open qualified opportunities, optional", "count",
    "Average of month-end open qualified opportunities across all salespeople (CRM).",
    used_by="Opportunities held per salesperson; Little's Law check")
add(4, "opportunities_capacity", "Opportunities a salesperson can manage at once", "count",
    "Most qualified opportunities a salesperson can hold and advance well at the same time.", 30,
    test="Close rate and cycle hold steady at loads above this level", used_by="Every scenario: salesperson capacity")

IDS = [e["id"] for e in E]
EBY = {e["id"]: e for e in E}


def refs(expr: str) -> str:
    for i in sorted(IDS, key=len, reverse=True):
        expr = expr.replace("{" + i + "}", "v_" + i)
    assert "{" not in expr, expr
    return expr


def est_formula(e) -> str | None:
    if not e["est"]:
        return None
    ins = sorted({i for i in IDS if "{" + i + "}" in e["est"]})
    blanks = ",".join(f'v_{i}=""' for i in ins)
    return f'=IFERROR(IF(OR({blanks}),"",{refs(e["est"])}),"")'


def name(wb, nm, sheet, cell):
    col = "".join(ch for ch in cell if ch.isalpha())
    row = "".join(ch for ch in cell if ch.isdigit())
    wb.defined_names[nm] = DefinedName(nm, attr_text=f"'{sheet}'!${col}${row}")


def header(ws, row, labels, widths=None):
    for i, h in enumerate(labels):
        c = ws.cell(row, i + 1, h)
        c.font, c.fill, c.border, c.alignment = f_head, fill_head, box, center
    if widths:
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w


def put(ws, row, col, value, font=f_body, fill=None, fmt=None, align=wrap, border=box):
    c = ws.cell(row, col, value)
    c.font, c.alignment, c.border = font, align, border
    if fill:
        c.fill = fill
    if fmt:
        c.number_format = fmt
    return c


# ---------------------------------------------------------------- Orientation
def build_orientation(ws):
    ws.sheet_view.showGridLines = False
    for col, w in {"A": 3, "B": 24, "C": 40, "D": 40, "E": 40}.items():
        ws.column_dimensions[col].width = w
    r = 2

    def para(text, font=f_body, gap=0):
        nonlocal r
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        c = ws.cell(r, 2, text)
        c.font, c.alignment = font, wrap
        ws.row_dimensions[r].height = row_height(text, 135 if font.size <= 10 else 95)
        r += 1 + gap

    def heading(text):
        nonlocal r
        r += 1
        para(text, f_h2)

    para("Commercial Effectiveness Model", f_title)
    para("© 2000–2026 Growth Enablement. All rights reserved.", f_note, gap=1)

    heading("What this model does")
    para("This model describes how your commercial system works, tests that description against your actual financial "
         "results, and then lets you explore what would happen if you changed it.")
    para("It is built on one discipline: lead with your assumptions. Every number you enter is a claim about your "
         "business. The model asks where each claim comes from, checks it against your other numbers, and shows which "
         "results rest on validated actuals and which on estimates. If anyone disagrees with a result, you can go straight "
         "back to the assumption behind it.")

    heading("How the model sees sales capacity")
    para("•  Territories are a design choice. You decide how to divide your market and how many territories to fund. "
         "A territory without a salesperson still carries an expected yield, so leaving it open has a cost.")
    para("•  Salespeople are a hiring choice. A salesperson's capacity is not the hours they work. It is how many "
         "opportunities they can hold and advance well at the same time, turned over by the length of your sales cycle.")
    para("•  Revenue = salespeople × opportunities worked at once × (12 ÷ cycle months) × close rate × deal size. Every "
         "cost then flows through a pro forma income statement to operating income.")

    heading("How the workbook is organized")
    para("Each tab has two worksheets. The client view holds only what you enter or choose, and the results. The logic "
         "sheet shows every calculation, one per row, with the rule written in words next to the live formula, so anyone "
         "can audit how a result was produced.")
    hdr = ["Worksheet", "Who uses it", "What it holds"]
    for i, h in enumerate(hdr):
        put(ws, r, 2 + i, h, f_head, fill_head)
    ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
    r += 1
    for row in [
        ("1) Data Entry", "Client: Finance, Sales Operations, HR", "Four steps, in the order the data is easiest to collect. For each entry: your value and where it came from. Shows the value the model uses and the cross-checks."),
        ("1) Data Entry Logic", "Growth Enablement and Finance reviewers", "For each entry: the rule that picks the value used, our estimate and how it is calculated, the default, and the basis. The cross-check calculations."),
        ("2) What-If", "Client: leadership", "Choose a scenario and the size of each improvement. Shows the pro forma income statement, the four scenarios side by side, and what it would take to reach a target operating income."),
        ("2) What-If Logic", "Growth Enablement and Finance reviewers", "Baseline and the four scenarios, calculated step by step from salesperson capacity to operating income, with a true-up."),
    ]:
        for i, v in enumerate(row):
            put(ws, r, 2 + i, v, f_bold if i == 0 else f_body)
        ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
        ws.row_dimensions[r].height = row_height(row[2], 75)
        r += 1

    heading("How to use it")
    para("1.  Collect the data (1) Data Entry). Work through the four steps in order; each names who usually owns the data, so "
         "the sheet can be forwarded. For each entry, type your value and choose its source:")
    for nm, desc in [("Validated by Finance", "confirmed by your Finance team from your records."),
                     ("Your entry", "your best number, not yet validated. Accepted, but labeled."),
                     ("Use our estimate", "the model calculates it from your other entries (for example, revenue ÷ contracts)."),
                     ("Left blank", "the model uses a default sample value, labeled “Default (sample)”, so it works from day one.")]:
        para(f"      –  {nm}: {desc}")
    para("2.  Confront the checks. At the bottom of 1) Data Entry, the model compares what your entries imply with what you "
         "reported. Each REVIEW is a place where two of your numbers cannot both be true. Revise an entry or explain the gap.")
    para("3.  Explore scenarios (2) What-If). Four scenarios: close rate, cycle time, deal size, and all three combined. The pro "
         "forma income statement is the constraint every scenario must pass through: an improvement only counts if it reaches "
         "operating income. Enter a target operating income to see what each lever would have to achieve.")
    para("4.  Sign off. Until Finance has validated every entry, every result is labeled “Working model: not validated by Finance.”")

    heading("Color legend")
    for label, fill, font, desc in [("Yellow", fill_input, f_input, "Enter or choose (client view only)"),
                                    ("Grey", fill_calc, f_body, "Calculated"),
                                    ("Blue", fill_used, f_bold, "Value the model uses, or a key result"),
                                    ("Green text", None, f_link, "Pulled from another worksheet")]:
        c = ws.cell(r, 2, label)
        c.font, c.border = font, box
        if fill:
            c.fill = fill
        ws.cell(r, 3, desc).font = f_body
        r += 1

    heading("What this model is not")
    for t in ["•  Not a forecast. It describes what your system can and does produce under stated assumptions.",
              "•  Not an evaluation of individual salespeople. Salespeople are measured as a system, without names, to find improvements in how the system works.",
              "•  Not a benchmark ranking. Reference values can inform assumptions, but your baseline is built from your own reality."]:
        para(t)

    heading("A few points")
    para("This is a general model. For a sharper analysis, run it separately for each sales channel and product line, "
         "and separate new-customer revenue from revenue from existing customers. The model can be tailored to your business.")
    para("“Increase leads” is not listed as a business scenario because we consider lead generation to be a more "
         "leveraged way to conduct sales prospecting. The number of leads, how to acquire them, and how much you can "
         "invest to acquire those leads are all handled in the tactical “drill down” spreadsheets that accompany this model.")
    para("Scenarios for adding territories, filling open territories and hiring will be added later; ramp time and open "
         "territories are collected now so they are ready.", f_note)


# ---------------------------------------------------------------- 1) Data Entry (client view)
DE_HDR = ["#", "Entry", "What to enter and where to find it", "Unit", "Your value", "Source", "Our estimate",
          "Value used", "Basis", "Why it matters (original)"]
DE_W = [6, 34, 46, 8, 15, 20, 15, 15, 24, 70]
DE_FIRST = 12          # first data row on the client sheet
DE_ROW: dict[str, int] = {}


def layout_de():
    """Assign client-sheet rows (step header rows interleaved). Logic sheet uses its own rows."""
    r = DE_FIRST
    for s, *_ in STEPS:
        r += 1  # step header row
        for e in E:
            if e["step"] == s:
                DE_ROW[e["id"]] = r
                r += 1
        r += 0
    return r


DL_FIRST = 8
DL_ROW = {e["id"]: DL_FIRST + i for i, e in enumerate(E)}
CHECK_ROW0 = DL_FIRST + len(E) + 4   # header row of the check block on the logic sheet

CHECKS = [
    # id, name, what it compares, implied (model) formula, reported formula, tolerance, entries involved
    ("deal", "Deal size", "Revenue ÷ contracts, compared with the deal size used",
     'IF(OR(v_revenue="",N(v_contracts)=0),"",v_revenue/v_contracts)', "v_deal_size", 0.10,
     "Revenue, contracts, deal size"),
    ("revenue", "Revenue", "Revenue the model produces at baseline, compared with revenue reported",
     "m_base_revenue", "v_revenue", 0.10, "Salespeople, capacity, opportunities held, cycle, close rate, deal size, revenue"),
    ("contracts", "Contracts", "Contracts the model produces at baseline, compared with contracts reported",
     "m_base_contracts", "v_contracts", 0.10, "Salespeople, capacity, opportunities held, cycle, close rate, contracts"),
    ("win", "Close rate", "CRM won ÷ (won + lost), compared with the close rate used",
     'IF(OR(v_opps_won="",v_opps_lost=""),"",v_opps_won/(v_opps_won+v_opps_lost))', "v_win_rate", 0.10,
     "Opportunities won and lost, close rate"),
    ("commission", "Commission", "Commissions paid ÷ revenue, compared with the commission rate used",
     'IF(OR(v_commissions_paid="",N(v_revenue)=0),"",v_commissions_paid/v_revenue)', "v_commission_rate", 0.10,
     "Commissions paid, revenue, commission rate"),
    ("littles", "Little's Law", "Opportunities each salesperson must hold to close the reported contracts "
     "(contracts ÷ close rate ÷ salespeople × cycle ÷ 12), compared with opportunities held in the CRM",
     'IF(OR(N(v_win_rate)=0,N(v_filled_seats)=0),"",v_contracts/v_win_rate/v_filled_seats*v_cycle_months/12)',
     'IF(N(v_open_opps_total)=0,"",v_open_opps_total/v_filled_seats)', 0.25,
     "Contracts, close rate, salespeople, cycle, open opportunities"),
    ("territory", "Territories", "Salespeople + open territories, compared with funded territories "
     "(runs only when the salesperson count is entered, not estimated)",
     f"IF('{DE}'!$E${{fs}}=\"\",\"\",v_filled_seats+v_open_territories)", "v_territory_count", 0.0,
     "Salespeople, open territories, funded territories"),
]


def build_data_entry(ws, wb):
    ws.sheet_view.showGridLines = False
    end = layout_de()
    header(ws, DE_FIRST - 1, DE_HDR, DE_W)
    ws.freeze_panes = ws.cell(DE_FIRST, 3)

    put(ws, 1, 1, "1) Data Entry", f_title, border=None)
    put(ws, 2, 1, "© 2000–2026 Growth Enablement. All rights reserved.", f_note, border=None)
    ws.merge_cells("A3:J3")
    put(ws, 3, 1, "=v_banner", f_bold, fill_banner)
    lines = [
        "How to fill this in. Work through the four steps in order. Each step names who usually has the data, so you can forward this sheet to them.",
        "For each entry: type the number in “Your value” (yellow) and choose its Source. Validated by Finance = confirmed from your records. "
        "Your entry = your best number, not yet validated. Use our estimate = let the model calculate it from your other entries (shown in “Our estimate”).",
        "Leave an entry blank and the model uses a default sample value, labeled “Default (sample)”, so it works from day one. “Value used” is what the model actually uses.",
        "At the bottom, the checks compare what your numbers imply with what you reported. A REVIEW means two of your numbers cannot both be true: revise one, or explain the gap.",
    ]
    for i, t in enumerate(lines):
        ws.merge_cells(start_row=5 + i, start_column=1, end_row=5 + i, end_column=10)
        put(ws, 5 + i, 1, t, f_body, border=None)
        ws.row_dimensions[5 + i].height = row_height(t, 230)

    dv = DataValidation(type="list", formula1='"' + ",".join(SOURCES) + '"', allow_blank=True)
    ws.add_data_validation(dv)

    for s, sname, owner, ask in STEPS:
        first = min(DE_ROW[e["id"]] for e in E if e["step"] == s)
        hr = first - 1
        ws.merge_cells(start_row=hr, start_column=1, end_row=hr, end_column=10)
        put(ws, hr, 1, f"Step {s}.  {sname}   ·   Ask: {owner}   ·   {ask}", f_bold, fill_step)
        n = 0
        for e in E:
            if e["step"] != s:
                continue
            n += 1
            r = DE_ROW[e["id"]]
            lr = DL_ROW[e["id"]]
            fmt = FMT[e["unit"]]
            put(ws, r, 1, f"{s}.{n}", f_body, align=center)
            put(ws, r, 2, e["name"], f_bold if e["default"] == "est" else f_body)
            put(ws, r, 3, e["what"])
            put(ws, r, 4, UNIT_LABEL[e["unit"]], align=center)
            put(ws, r, 5, None, f_input, fill_input, fmt)
            src = put(ws, r, 6, None, f_input, fill_input)
            dv.add(src)
            if e["est"]:
                put(ws, r, 7, f"='{DL}'!E{lr}", f_link, fill_calc, fmt)
            else:
                put(ws, r, 7, "—", f_note, fill_calc, align=center)
            put(ws, r, 8, f"=v_{e['id']}", f_bold, fill_used, fmt)
            put(ws, r, 9, f"='{DL}'!J{lr}", f_link, fill_calc)
            put(ws, r, 10, e["why"], f_note)
            ws.row_dimensions[r].height = max(row_height(e["what"], 48), row_height(e["why"], 85, 11.5), 17)

    # basis colouring
    rng = f"I{DE_FIRST}:I{end}"
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT(I{DE_FIRST},7)="Default"'], font=Font(color="C00000")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'I{DE_FIRST}="Validated by Finance"'], font=Font(color="008000", bold=True)))

    # checks (client view of the logic sheet's check block)
    r = end + 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
    put(ws, r, 1, "Checks: do your numbers agree with each other?", f_h2, border=None)
    r += 1
    for i, h in enumerate(["", "Check", "What it compares", "", "Model implies", "You reported", "Gap", "Status", "Entries involved", "What to do"]):
        put(ws, r, i + 1, h, f_head, fill_head, align=center)
    first_check_row = r + 1
    for k, chk in enumerate(CHECKS):
        r += 1
        lr = CHECK_ROW0 + 1 + k
        fmt = FMT["currency"] if chk[0] in ("deal", "revenue") else FMT["pct"] if chk[0] in ("win", "commission") else FMT["count1"]
        put(ws, r, 1, k + 1, align=center)
        put(ws, r, 2, chk[1], f_bold)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        put(ws, r, 3, chk[2])
        put(ws, r, 5, f"='{DL}'!D{lr}", f_link, fill_calc, fmt)
        put(ws, r, 6, f"='{DL}'!E{lr}", f_link, fill_calc, fmt)
        put(ws, r, 7, f"='{DL}'!F{lr}", f_link, fill_calc, FMT["spct"])
        put(ws, r, 8, f"='{DL}'!H{lr}", f_bold, fill_calc, align=center)
        put(ws, r, 9, chk[6])
        put(ws, r, 10, f'=IF(H{r}="REVIEW","These entries cannot all be true. Revise one, or write the explanation here.",'
                       f'IF(H{r}="NEEDS DATA","Enter the optional data above to run this check.",""))', f_note)
        ws.row_dimensions[r].height = row_height(chk[2], 50)
    rng = f"H{first_check_row}:H{r}"
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'H{first_check_row}="PASS"'], fill=PatternFill("solid", start_color="C6EFCE")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'H{first_check_row}="REVIEW"'], fill=PatternFill("solid", start_color="FFC7CE")))

    r += 2
    put(ws, r, 2, "Source of the values used", f_h2, border=None)
    for basis in ["Validated by Finance", "Your entry (not validated)", "Our estimate", "Default (sample)", "Not provided (optional)"]:
        r += 1
        put(ws, r, 2, basis)
        put(ws, r, 3, f"=COUNTIF('{DL}'!$J${DL_FIRST}:$J${DL_FIRST + len(E) - 1},\"{basis.split(' (')[0] if basis.startswith('Our') else basis}*\")",
            f_link, fill_calc, FMT["count"], align=center)
    ws.print_title_rows = f"{DE_FIRST - 1}:{DE_FIRST - 1}"


# ---------------------------------------------------------------- 1) Data Entry Logic
DL_HDR = ["ID", "Entry", "Your value", "Source chosen", "Our estimate", "How our estimate is calculated", "Default",
          "Default context", "Value used", "Basis", "What would prove it wrong", "Used by"]
DL_W = [22, 34, 14, 20, 14, 36, 14, 26, 15, 26, 40, 36]


def build_data_logic(ws, wb):
    ws.sheet_view.showGridLines = False
    put(ws, 1, 1, "1) Data Entry Logic", f_title, border=None)
    put(ws, 2, 1, "Programming logic for the data entry. Nothing here is typed by the client; every cell is a formula or a fixed default.",
        f_note, border=None)
    rules = [
        "Rule for Value used:  if Source = “Use our estimate” and an estimate exists → Our estimate;  otherwise, if Your value is entered → Your value;  otherwise → Default.",
        "Rule for Basis:  Validated by Finance (value entered and source = Validated by Finance) · Your entry (not validated) · Our estimate · Default (sample) · Not provided (optional entry left blank).",
        "Every Value used cell is a workbook name, v_<ID>. It is the only way any other worksheet reads an entry.",
    ]
    for i, t in enumerate(rules):
        ws.merge_cells(start_row=3 + i, start_column=1, end_row=3 + i, end_column=12)
        put(ws, 3 + i, 1, t, f_body, border=None)
    header(ws, DL_FIRST - 1, DL_HDR, DL_W)
    ws.freeze_panes = ws.cell(DL_FIRST, 3)

    for e in E:
        r = DL_ROW[e["id"]]
        cr = DE_ROW[e["id"]]
        fmt = FMT[e["unit"]]
        put(ws, r, 1, e["id"], f_note)
        put(ws, r, 2, e["name"])
        put(ws, r, 3, f"=IF('{DE}'!E{cr}=\"\",\"\",'{DE}'!E{cr})", f_link, fill_calc, fmt)
        put(ws, r, 4, f"=IF('{DE}'!F{cr}=\"\",\"\",'{DE}'!F{cr})", f_link, fill_calc)
        ef = est_formula(e)
        put(ws, r, 5, ef if ef else "", f_body, fill_calc, fmt)
        put(ws, r, 6, e["est_words"] or "No estimate: enter a value or use the default", f_note if not e["est_words"] else f_body)
        if e["default"] == "est":
            put(ws, r, 7, f"=E{r}", f_body, fill_calc, fmt)
            put(ws, r, 8, "Our estimate", f_note)
        elif e["default"] is None:
            put(ws, r, 7, '=""', f_body, fill_calc)
            put(ws, r, 8, "Optional; no default", f_note)
        else:
            put(ws, r, 7, e["default"], f_body, fill_calc, fmt)
            put(ws, r, 8, SAMPLE if e["id"] != "deal_size" else
                "Reference value from another client, chosen so the model fits companies of any size (as-is model)", f_note)
        put(ws, r, 9, f'=IF(AND(D{r}="Use our estimate",E{r}<>""),E{r},IF(C{r}<>"",C{r},G{r}))', f_bold, fill_used, fmt)
        default_label = '"Our estimate"' if e["default"] == "est" else '"Default (sample)"'
        put(ws, r, 10, f'=IF(I{r}="","Not provided (optional)",IF(AND(D{r}="Use our estimate",E{r}<>""),"Our estimate",'
                       f'IF(C{r}<>"",IF(D{r}="Validated by Finance","Validated by Finance","Your entry (not validated)"),{default_label})))',
            f_body, fill_calc)
        put(ws, r, 11, e["test"], f_note)
        put(ws, r, 12, e["used_by"], f_note)
        name(wb, "v_" + e["id"], DL, f"I{r}")

    # checks
    r = CHECK_ROW0 - 1
    put(ws, r, 1, "Cross-checks: what the entries imply vs what was reported", f_h2, border=None)
    for i, h in enumerate(["ID", "Check", "What it compares", "Model implies", "Reported / used", "Gap",
                           "Tolerance", "Status", "Rule"]):
        put(ws, CHECK_ROW0, i + 1, h, f_head, fill_head, align=center)
    fs_row = DE_ROW["filled_seats"]
    for k, (cid, cname, words, implied, reported, tol, involved) in enumerate(CHECKS):
        r = CHECK_ROW0 + 1 + k
        fmt = FMT["currency"] if cid in ("deal", "revenue") else FMT["pct"] if cid in ("win", "commission") else FMT["count1"]
        put(ws, r, 1, cid, f_note)
        put(ws, r, 2, cname, f_bold)
        put(ws, r, 3, words)
        put(ws, r, 4, "=IFERROR(" + implied.replace("{fs}", str(fs_row)) + ',"")', f_body, fill_calc, fmt)
        put(ws, r, 5, f'=IFERROR({reported},"")', f_body, fill_calc, fmt)
        put(ws, r, 6, f'=IF(OR(D{r}="",E{r}="",N(E{r})=0),"",D{r}/E{r}-1)', f_body, fill_calc, FMT["spct"])
        put(ws, r, 7, tol, f_body, fill_calc, "0%")
        put(ws, r, 8, f'=IF(F{r}="","NEEDS DATA",IF(ABS(F{r})<=G{r}+1E-9,"PASS","REVIEW"))', f_bold, fill_used, align=center)
        put(ws, r, 9, "Gap = implied ÷ reported − 1.  PASS if |gap| ≤ tolerance.", f_note)
        ws.row_dimensions[r].height = row_height(words, 34)

    # status summary and banner
    r = CHECK_ROW0 + len(CHECKS) + 3
    put(ws, r, 1, "Status", f_h2, border=None)
    rng_basis = f"$J${DL_FIRST}:$J${DL_FIRST + len(E) - 1}"
    rng_check = f"$H${CHECK_ROW0 + 1}:$H${CHECK_ROW0 + len(CHECKS)}"
    items = [
        ("st_required", "Entries the model uses (not optional blanks)", f'=COUNTA({rng_basis})-COUNTIF({rng_basis},"Not provided*")'),
        ("st_validated", "Of those, validated by Finance", f'=COUNTIF({rng_basis},"Validated by Finance")'),
        ("st_review", "Checks needing review", f'=COUNTIF({rng_check},"REVIEW")'),
        ("v_banner", "Banner shown on every client sheet",
         '=IF(AND(st_validated=st_required,st_review=0),"Baseline validated by Finance",'
         '"Working model: not validated by Finance  ·  "&st_validated&" of "&st_required&" entries validated  ·  "'
         '&st_review&" checks need review")'),
    ]
    for nm, label, f in items:
        r += 1
        put(ws, r, 1, nm, f_note)
        put(ws, r, 2, label)
        put(ws, r, 3, f, f_bold, fill_used, FMT["count"] if nm != "v_banner" else None)
        if nm == "v_banner":
            ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=9)
        name(wb, nm, DL, f"C{r}")


# ---------------------------------------------------------------- 2) What-If Logic
SCEN = [("Baseline", "C"), ("Close rate", "D"), ("Cycle time", "E"), ("Deal size", "F"), ("Combined", "G")]
SC = [c for _, c in SCEN]
WL_HDR_ROW = 6

# key, label, how it is calculated (words), format, formula template, or dict per column
# {k} = same column, {$k} = baseline column C
WL_ROWS = [
    ("§", "Scenario changes (set on 2) What-If)"),
    ("ch_win", "Close rate improvement", "Set on 2) What-If; applies to Close rate and Combined", "spct",
     {"C": "0", "D": "wi_win", "E": "0", "F": "0", "G": "wi_win"}),
    ("ch_cycle", "Cycle time reduction", "Set on 2) What-If; applies to Cycle time and Combined", "spct",
     {"C": "0", "D": "0", "E": "wi_cycle", "F": "0", "G": "wi_cycle"}),
    ("ch_deal", "Deal size increase", "Set on 2) What-If; applies to Deal size and Combined", "spct",
     {"C": "0", "D": "0", "E": "0", "F": "wi_deal", "G": "wi_deal"}),
    ("§", "Salesperson throughput"),
    ("salespeople", "Salespeople", "Value used: quota-carrying salespeople", "count", "v_filled_seats"),
    ("capacity", "Opportunities a salesperson can manage at once", "Value used: capacity", "count1", "v_opportunities_capacity"),
    ("held", "Opportunities each salesperson holds", "Open opportunities ÷ salespeople; blank if not entered", "count1",
     'IF(N(v_open_opps_total)=0,"",v_open_opps_total/{salespeople})'),
    ("worked", "Opportunities worked at once", "Lesser of held and capacity; capacity if held is not entered", "count1",
     'IF({held}="",{capacity},MIN({held},{capacity}))'),
    ("utilization", "Utilization of capacity", "Worked ÷ capacity; blank if held is not entered", "pct",
     'IF({held}="","",{worked}/{capacity})'),
    ("cycle", "Sales cycle (months)", "Cycle used × (1 − cycle time reduction)", "months", "v_cycle_months*(1-{ch_cycle})"),
    ("resolved", "Opportunities resolved per salesperson per year", "Worked × 12 ÷ cycle (Little's Law)", "count1",
     "{worked}*12/{cycle}"),
    ("win", "Close rate", "Close rate used × (1 + close rate improvement)", "pct", "v_win_rate*(1+{ch_win})"),
    ("deals_per", "Contracts per salesperson per year", "Resolved × close rate", "count1", "{resolved}*{win}"),
    ("deal", "Average revenue per contract", "Deal size used × (1 + deal size increase)", "currency", "v_deal_size*(1+{ch_deal})"),
    ("rev_per", "Revenue per salesperson", "Contracts per salesperson × deal size", "currency", "{deals_per}*{deal}"),
    ("contracts", "Contracts", "Contracts per salesperson × salespeople", "count", "{deals_per}*{salespeople}"),
    ("§", "Pro forma income statement"),
    ("revenue", "Revenue", "Revenue per salesperson × salespeople", "currency", "{rev_per}*{salespeople}"),
    ("cor", "Cost of revenue", "Revenue × cost of revenue %", "currency", "{revenue}*v_cost_of_revenue_pct"),
    ("gross", "Gross profit", "Revenue − cost of revenue", "currency", "{revenue}-{cor}"),
    ("rnd", "Research and development", "Revenue × R&D %", "currency", "{revenue}*v_rnd_pct"),
    ("sp_pay", "Salesperson pay (salary and benefits)", "Fully loaded salary × salespeople", "currency", "v_loaded_salary*{salespeople}"),
    ("sp_travel", "Salesperson travel", "Travel per salesperson × salespeople", "currency", "v_travel_per_salesperson*{salespeople}"),
    ("sp_comm", "Commissions", "Commission rate × revenue", "currency", "v_commission_rate*{revenue}"),
    ("overhead", "Sales overhead", "Value used: sales overhead (fixed)", "currency", "v_sales_overhead"),
    ("sales_total", "Total sales costs", "Pay + travel + commissions + overhead", "currency",
     "{sp_pay}+{sp_travel}+{sp_comm}+{overhead}"),
    ("marketing", "Marketing", "Value used: marketing (fixed)", "currency", "v_marketing"),
    ("sm_total", "Total sales and marketing", "Total sales costs + marketing", "currency", "{sales_total}+{marketing}"),
    ("gna", "General and administrative", "Revenue × G&A %", "currency", "{revenue}*v_gna_pct"),
    ("opex", "Total operating expenses", "R&D + sales and marketing + G&A", "currency", "{rnd}+{sm_total}+{gna}"),
    ("oi", "Operating income", "Gross profit − operating expenses", "currency", "{gross}-{opex}"),
    ("margin", "Operating margin", "Operating income ÷ revenue", "pct", 'IF({revenue}=0,"",{oi}/{revenue})'),
    ("§", "Compared with baseline"),
    ("total_costs", "Total costs", "Cost of revenue + operating expenses", "currency", "{cor}+{opex}"),
    ("d_rev", "Change in revenue", "Revenue − baseline revenue", "scur", "{revenue}-{$revenue}"),
    ("d_costs", "Change in total costs", "Total costs − baseline total costs", "scur", "{total_costs}-{$total_costs}"),
    ("d_oi", "Change in operating income", "Operating income − baseline operating income", "scur", "{oi}-{$oi}"),
    ("d_oi_pct", "Change in operating income, %", "Change ÷ baseline operating income", "spct",
     'IF({$oi}=0,"",{d_oi}/ABS({$oi}))'),
    ("trueup", "True-up", "Change in revenue − change in costs − change in operating income = 0", "text",
     'IF(ABS({d_rev}-{d_costs}-{d_oi})<1,"Balanced","Check")'),
    ("net_gain", "Percentage net gain (as-is definition)", "(Change in revenue − change in sales costs) ÷ baseline revenue", "spct",
     "({d_rev}-({sales_total}-{$sales_total}))/{$revenue}"),
    ("sm_roi", "Sales and marketing ROI", "(Revenue − sales and marketing) ÷ sales and marketing", "pct",
     'IF({sm_total}=0,"",({revenue}-{sm_total})/{sm_total})'),
    ("§", "Guardrails"),
    ("flag", "Guardrail", "Close rate above 100%, cycle at or below zero, or pipeline (not capacity) limiting revenue", "text",
     'IF({win}>1,"Close rate above 100%: reduce the improvement",IF({cycle}<=0,"Cycle must stay above zero",'
     'IF(AND({held}<>"",N({held})<{capacity}),"Salespeople hold fewer opportunities than they can manage: the pipeline limits revenue","OK")))'),
]

TARGET_ROWS = [
    ("t_target", "Target operating income", "Entered on 2) What-If (optional)", "currency", 'IF(wi_target="","",wi_target)'),
    ("t_var", "Costs that move with revenue, % of revenue", "Cost of revenue % + R&D % + G&A % + commission rate", "pct",
     "v_cost_of_revenue_pct+v_rnd_pct+v_gna_pct+v_commission_rate"),
    ("t_fixed", "Costs that do not move with revenue", "Baseline pay + travel + sales overhead + marketing", "currency",
     "{$sp_pay}+{$sp_travel}+{$overhead}+{$marketing}"),
    ("t_check", "Check: baseline operating income from this split", "Baseline revenue × (1 − variable %) − fixed; must equal baseline operating income",
     "currency", "{$revenue}*(1-{t_var})-{t_fixed}"),
    ("t_req_rev", "Revenue required", "(Target + fixed costs) ÷ (1 − variable %)", "currency",
     'IF({t_target}="","",IF({t_var}>=1,"",({t_target}+{t_fixed})/(1-{t_var})))'),
    ("t_lift", "Revenue increase required", "Revenue required ÷ baseline revenue − 1", "spct",
     'IF({t_req_rev}="","",{t_req_rev}/{$revenue}-1)'),
    ("t_win", "Close rate needed (close rate alone)", "Close rate × (1 + increase); revenue moves one for one with close rate", "pct",
     'IF({t_lift}="","",v_win_rate*(1+{t_lift}))'),
    ("t_cycle", "Cycle needed, months (cycle alone)", "Cycle ÷ (1 + increase); revenue moves inversely with cycle", "months",
     'IF({t_lift}="","",v_cycle_months/(1+{t_lift}))'),
    ("t_deal", "Deal size needed (deal size alone)", "Deal size × (1 + increase)", "currency",
     'IF({t_lift}="","",v_deal_size*(1+{t_lift}))'),
    ("t_each", "Combined: improvement needed in each of the three", "(1 + increase)^(1/3) − 1, if close rate, cycle and deal size each improve by the same share",
     "spct", 'IF({t_lift}="","",IF(1+{t_lift}<=0,"",(1+{t_lift})^(1/3)-1))'),
    ("t_flag", "Feasibility", "Flags a close rate above 100% or a target below baseline", "text",
     'IF({t_lift}="","Enter a target operating income on 2) What-If",IF({t_lift}<=0,"Target is at or below baseline operating income",'
     'IF({t_win}>1,"Close rate alone cannot reach the target (would exceed 100%)","Reachable in the model; test whether it is achievable")))'),
]

WL_ROW: dict[str, int] = {}


def build_whatif_logic(ws, wb):
    ws.sheet_view.showGridLines = False
    put(ws, 1, 1, "2) What-If Logic", f_title, border=None)
    put(ws, 2, 1, "Programming logic for the scenarios. Reads tab 1 only through the v_ names; reads 2) What-If only for the "
                  "scenario choice, improvement sizes and target.", f_note, border=None)
    ws.merge_cells("A3:I3")
    put(ws, 3, 1, "Each row is one calculation. Column B states the rule in words; columns C–G apply it to the baseline and the four "
                  "scenarios; column H shows the scenario chosen on 2) What-If.", f_body, border=None)
    hdr = ["Line", "How it is calculated"] + [s for s, _ in SCEN] + ["Selected scenario"]
    header(ws, WL_HDR_ROW, hdr, [40, 62, 16, 16, 16, 16, 16, 18])
    ws.freeze_panes = ws.cell(WL_HDR_ROW + 1, 3)

    r = WL_HDR_ROW
    for row in WL_ROWS:
        r += 1
        if row[0] == "§":
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
            put(ws, r, 1, row[1], f_bold, fill_step)
            continue
        WL_ROW[row[0]] = r
    keys = list(WL_ROW)

    def expand(tmpl, col):
        for k in sorted(keys, key=len, reverse=True):
            tmpl = tmpl.replace("{$" + k + "}", f"$C${WL_ROW[k]}").replace("{" + k + "}", f"{col}{WL_ROW[k]}")
        assert "{" not in tmpl, tmpl
        return "=" + tmpl

    bold_keys = {"revenue", "gross", "sales_total", "sm_total", "opex", "oi", "d_oi", "trueup"}
    for row in WL_ROWS:
        if row[0] == "§":
            continue
        k, label, words, fmt, tmpl = row
        r = WL_ROW[k]
        put(ws, r, 1, label, f_bold if k in bold_keys else f_body)
        put(ws, r, 2, words, f_note)
        for col in SC:
            t = tmpl[col] if isinstance(tmpl, dict) else tmpl
            fill = fill_used if k in ("oi", "d_oi") else fill_calc
            c = put(ws, r, ord(col) - 64, expand(t, col), f_bold if k in bold_keys else f_body, fill, FMT[fmt],
                    align=Alignment(horizontal="right", vertical="top", wrap_text=fmt == "text"))
            if k in ("revenue", "oi"):
                c.border = top_line
        put(ws, r, 8, f"=INDEX(C{r}:G{r},MATCH(wi_select,$C${WL_HDR_ROW}:$G${WL_HDR_ROW},0))",
            f_bold if k in bold_keys else f_body, fill_used, FMT[fmt],
            align=Alignment(horizontal="right", vertical="top", wrap_text=fmt == "text"))
        if k.startswith("d_") or k in ("trueup", "net_gain"):
            ws.cell(r, 3).value = "" if k != "trueup" else "—"
            ws.cell(r, 3).alignment = Alignment(horizontal="right")
        if k == "flag":
            ws.row_dimensions[r].height = 40

    # enabling constraint: what it takes to reach a target operating income (baseline only)
    r += 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    put(ws, r, 1, "Enabling constraint: what each lever would have to achieve to reach a target operating income", f_bold, fill_step)
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    put(ws, r, 1, "Operating income = revenue × (1 − costs that move with revenue) − costs that do not. Revenue moves one for one "
                  "with close rate and deal size, and inversely with cycle, so the revenue required converts directly into what "
                  "each lever would need.", f_note, border=None)
    ws.row_dimensions[r].height = 28
    for k, *_ in TARGET_ROWS:
        r += 1
        WL_ROW[k] = r
    keys = list(WL_ROW)
    for k, label, words, fmt, tmpl in TARGET_ROWS:
        rr = WL_ROW[k]
        put(ws, rr, 1, label, f_bold if k in ("t_req_rev", "t_lift") else f_body)
        put(ws, rr, 2, words, f_note)
        put(ws, rr, 3, expand(tmpl, "C"), f_bold if k in ("t_req_rev", "t_lift") else f_body,
            fill_used if k in ("t_req_rev", "t_lift") else fill_calc, FMT[fmt],
            align=Alignment(horizontal="right" if fmt != "text" else "left", vertical="top", wrap_text=True))
        if fmt == "text":
            ws.merge_cells(start_row=rr, start_column=3, end_row=rr, end_column=8)
            ws.row_dimensions[rr].height = 28

    name(wb, "m_base_revenue", WL, f"C{WL_ROW['revenue']}")
    name(wb, "m_base_contracts", WL, f"C{WL_ROW['contracts']}")


# ---------------------------------------------------------------- 2) What-If (client view)
SCEN_CHOICES = [s for s, _ in SCEN[1:]]


def build_whatif(ws, wb):
    ws.sheet_view.showGridLines = False
    for col, w in {"A": 3, "B": 42, "C": 18, "D": 18, "E": 18, "F": 18, "G": 44}.items():
        ws.column_dimensions[col].width = w
    L = lambda k, col="H": f"='{WL}'!{col}{WL_ROW[k]}"   # noqa: E731

    put(ws, 1, 2, "2) What-If Scenarios", f_title, border=None)
    put(ws, 2, 2, "© 2000–2026 Growth Enablement. All rights reserved.", f_note, border=None)
    ws.merge_cells("B3:G3")
    put(ws, 3, 2, "=v_banner", f_bold, fill_banner)
    ws.merge_cells("B4:G4")
    put(ws, 4, 2, '=IF(m_base_revenue="","",IF(ABS(m_base_revenue/v_revenue-1)<=0.1,'
                  '"Calibration: the model baseline reproduces reported revenue within 10%.",'
                  '"Calibration: the model baseline produces "&TEXT(m_base_revenue,"$#,##0")&" of revenue; you reported "'
                  '&TEXT(v_revenue,"$#,##0")&". Resolve the checks on 1) Data Entry before relying on these results."))',
        f_note, border=None)
    ws.row_dimensions[4].height = 28

    # inputs
    put(ws, 6, 2, "Choose", f_h2, border=None)
    inputs = [("wi_select", "Scenario to show", "Combined", None, "Close rate, Cycle time, Deal size, or Combined (all three)"),
              ("wi_win", "Close rate improvement", 0.10, "0.0%", "Relative: 10% turns a 25% close rate into 27.5%"),
              ("wi_cycle", "Cycle time reduction", 0.10, "0.0%", "Relative: 10% turns 6 months into 5.4"),
              ("wi_deal", "Deal size increase", 0.10, "0.0%", "Relative: 10% turns $75,000 into $82,500"),
              ("wi_target", "Target operating income (optional)", None, FMT["currency"],
               "Shows what each lever would have to achieve, at the bottom of this sheet")]
    dv = DataValidation(type="list", formula1='"' + ",".join(SCEN_CHOICES) + '"', allow_blank=False)
    ws.add_data_validation(dv)
    for i, (nm, label, val, fmt, note) in enumerate(inputs):
        r = 7 + i
        put(ws, r, 2, label, f_bold)
        c = put(ws, r, 3, val, f_input, fill_input, fmt, align=Alignment(horizontal="right"))
        if nm == "wi_select":
            dv.add(c)
        ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=7)
        put(ws, r, 4, note, f_note, border=None)
        name(wb, nm, WI, f"C{r}")

    # four scenarios at a glance
    r = 13
    put(ws, r, 2, "The four scenarios at a glance", f_h2, border=None)
    r += 1
    for i, h in enumerate(["Scenario", "Revenue", "Operating income", "Change in operating income", "Operating margin", "Guardrail"]):
        put(ws, r, 2 + i, h, f_head, fill_head, align=center)
    for s, col in SCEN:
        r += 1
        put(ws, r, 2, s, f_bold)
        put(ws, r, 3, L("revenue", col), f_link, fill_calc, FMT["currency"])
        put(ws, r, 4, L("oi", col), f_link, fill_calc, FMT["currency"])
        put(ws, r, 5, "" if col == "C" else L("d_oi", col), f_link, fill_used if col != "C" else fill_calc, FMT["scur"])
        put(ws, r, 6, L("margin", col), f_link, fill_calc, FMT["pct"])
        put(ws, r, 7, L("flag", col), f_note)
        ws.row_dimensions[r].height = 26
    glance_end = r

    # pro forma income statement
    r += 2
    put(ws, r, 2, '="Pro forma income statement: "&wi_select', f_h2, border=None)
    r += 1
    for i, h in enumerate(["", "Baseline", "=wi_select", "Change", "Change %"]):
        put(ws, r, 2 + i, h, f_head, fill_head, align=center)
    pl = [("revenue", "Revenue", True), ("cor", "Cost of revenue", False), ("gross", "Gross profit", True),
          ("rnd", "Research and development", False), ("sp_pay", "Salesperson pay (salary and benefits)", False),
          ("sp_travel", "Salesperson travel", False), ("sp_comm", "Commissions", False), ("overhead", "Sales overhead", False),
          ("sales_total", "Total sales costs", True), ("marketing", "Marketing", False),
          ("sm_total", "Total sales and marketing", True), ("gna", "General and administrative", False),
          ("opex", "Total operating expenses", True), ("oi", "Operating income", True), ("margin", "Operating margin", True)]
    for k, label, bold in pl:
        r += 1
        fmt = FMT["pct"] if k == "margin" else FMT["currency"]
        indent = Alignment(indent=0 if bold else 2, vertical="top")
        put(ws, r, 2, label, f_bold if bold else f_body, fill_total if k == "oi" else None, align=indent)
        put(ws, r, 3, L(k, "C"), f_bold if bold else f_link, fill_total if k == "oi" else fill_calc, fmt)
        put(ws, r, 4, L(k), f_bold if bold else f_link, fill_total if k == "oi" else fill_used, fmt)
        if k == "margin":
            put(ws, r, 5, f"=D{r}-C{r}", f_body, fill_calc, '+0.0" pts";-0.0" pts"', )
            ws.cell(r, 5).value = f"=(D{r}-C{r})*100"
            put(ws, r, 6, "", f_body, fill_calc)
        else:
            put(ws, r, 5, f"=D{r}-C{r}", f_bold if bold else f_body, fill_calc, FMT["scur"])
            put(ws, r, 6, f'=IF(C{r}=0,"",(D{r}-C{r})/ABS(C{r}))', f_body, fill_calc, FMT["spct"])
        if k in ("revenue", "gross", "opex", "oi"):
            for cc in range(2, 7):
                ws.cell(r, cc).border = top_line
    r += 1
    put(ws, r, 2, "True-up (change in revenue − change in costs − change in operating income)", f_note)
    put(ws, r, 4, L("trueup"), f_bold, fill_calc, align=Alignment(horizontal="right"))

    # drivers
    r += 2
    put(ws, r, 2, "What drives it", f_h2, border=None)
    r += 1
    for i, h in enumerate(["", "Baseline", "=wi_select", "Change"]):
        put(ws, r, 2 + i, h, f_head, fill_head, align=center)
    for k, label, fmt in [("salespeople", "Salespeople", "count"), ("worked", "Opportunities worked at once, per salesperson", "count1"),
                          ("utilization", "Utilization of capacity (blank if pipeline not entered)", "pct"),
                          ("cycle", "Sales cycle (months)", "months"), ("resolved", "Opportunities resolved per salesperson per year", "count1"),
                          ("win", "Close rate", "pct"), ("deals_per", "Contracts per salesperson per year", "count1"),
                          ("deal", "Average revenue per contract", "currency"), ("rev_per", "Revenue per salesperson", "currency"),
                          ("contracts", "Contracts", "count")]:
        r += 1
        put(ws, r, 2, label)
        put(ws, r, 3, L(k, "C"), f_link, fill_calc, FMT[fmt])
        put(ws, r, 4, L(k), f_link, fill_used, FMT[fmt])
        put(ws, r, 5, f'=IF(OR(C{r}="",D{r}=""),"",D{r}-C{r})', f_body, fill_calc,
            {"currency": FMT["scur"], "pct": '+0.0%;-0.0%;0.0%', "months": '+0.0;-0.0;0.0', "count": '+#,##0;-#,##0;0',
             "count1": '+#,##0.0;-#,##0.0;0.0'}[fmt])
    r += 1
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    put(ws, r, 2, L("flag"), f_note, border=None)

    # enabling constraint
    r += 2
    put(ws, r, 2, "What it would take to reach your target operating income", f_h2, border=None)
    r += 1
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    put(ws, r, 2, "The income statement is the constraint: an improvement only counts if it reaches operating income. "
                  "Enter a target above, and the model works back to the revenue required and what each lever would have to achieve.",
        f_note, border=None)
    ws.row_dimensions[r].height = 26
    for k, label, fmt, base in [("t_target", "Target operating income", "currency", "oi"),
                                ("t_req_rev", "Revenue required", "currency", "revenue"),
                                ("t_lift", "Revenue increase required", "spct", None),
                                ("t_win", "Close rate needed, if close rate alone", "pct", "win"),
                                ("t_cycle", "Cycle needed (months), if cycle alone", "months", "cycle"),
                                ("t_deal", "Deal size needed, if deal size alone", "currency", "deal"),
                                ("t_each", "Or: improve close rate, cycle and deal size each by", "spct", None)]:
        r += 1
        put(ws, r, 2, label, f_bold if k in ("t_req_rev", "t_lift") else f_body)
        put(ws, r, 3, f"='{WL}'!C{WL_ROW[k]}", f_link, fill_used, FMT[fmt])
        if base:
            put(ws, r, 4, f"='{WL}'!C{WL_ROW[base]}", f_link, fill_calc, FMT[fmt])
            put(ws, r, 5, "baseline", f_note, border=None)
    r += 1
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    put(ws, r, 2, f"='{WL}'!C{WL_ROW['t_flag']}", f_bold, border=None)

    ws.conditional_formatting.add(f"G15:G{glance_end}", FormulaRule(formula=['AND(G15<>"OK",G15<>"")'], font=Font(color="C00000")))


# ---------------------------------------------------------------- main
def main():
    wb = Workbook()
    ws_o = wb.active
    ws_o.title = "Orientation"
    build_orientation(ws_o)
    ws_de = wb.create_sheet(DE)
    ws_dl = wb.create_sheet(DL)
    ws_wi = wb.create_sheet(WI)
    ws_wl = wb.create_sheet(WL)
    layout_de()
    build_data_logic(ws_dl, wb)
    build_whatif_logic(ws_wl, wb)
    build_data_entry(ws_de, wb)
    build_whatif(ws_wi, wb)
    for ws, tab in ((ws_de, "FFC000"), (ws_wi, "FFC000"), (ws_dl, "808080"), (ws_wl, "808080")):
        ws.sheet_properties.tabColor = tab
    for ws, landscape in ((ws_o, False), (ws_de, True), (ws_dl, True), (ws_wi, False), (ws_wl, True)):
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.page_setup.orientation = "landscape" if landscape else "portrait"
    wb.properties.creator = "Growth Enablement"
    wb.properties.title = "Commercial Effectiveness Model"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
