"""Build the rebuilt workbook: Orientation and 1) Data Entry (the assumption ledger).

Run:  python tools/build_workbook.py  ->  workbook/Commercial_Effectiveness_Model.xlsx

Design (tab 1):
  * Each row is one entry. Its "Value used" cell is the only cell other tabs reference,
    through a workbook name (v_<entry id>).
  * Each entry offers input options: Validated actual, Calculated, Reference value,
    Judgment (the leadership belief). "Input method" chooses which one is used.
  * Calculators reference other entries' Value used cells, never raw cells.
  * Defaults reproduce the as-is model's tab 1 values (illustrative), so the
    workbook works on first open and its cross-checks show what they test.

© 2000–2026 Growth Enablement. All rights reserved.
"""
from __future__ import annotations

import math
import pathlib

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "workbook" / "Commercial_Effectiveness_Model.xlsx"
DE = "1) Data Entry"

# ---------------------------------------------------------------- styles
FONT = "Arial"
f_body = Font(name=FONT, size=10)
f_input = Font(name=FONT, size=10, color="0000FF")
f_bold = Font(name=FONT, size=10, bold=True)
f_used = Font(name=FONT, size=10, bold=True)
f_head = Font(name=FONT, size=10, bold=True, color="FFFFFF")
f_title = Font(name=FONT, size=16, bold=True)
f_h2 = Font(name=FONT, size=12, bold=True)
f_note = Font(name=FONT, size=9, italic=True, color="595959")
fill_input = PatternFill("solid", start_color="FFF2CC")   # yellow: enter data (as-is convention)
fill_calc = PatternFill("solid", start_color="F2F2F2")    # grey: calculated
fill_used = PatternFill("solid", start_color="DDEBF7")    # blue: the value the model uses
fill_head = PatternFill("solid", start_color="1F3864")
fill_step = PatternFill("solid", start_color="D9E1F2")
fill_banner = PatternFill("solid", start_color="FCE4D6")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
used_border = Border(left=Side(style="medium", color="1F3864"), right=Side(style="medium", color="1F3864"),
                     top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
center = Alignment(horizontal="center", vertical="top")

FMT = {
    "currency": '$#,##0;($#,##0);"-"',
    "ratio": "0.0%",
    "count": "#,##0",
    "count1": "#,##0.0",
    "months": "0.0",
    "days": "#,##0",
    "text": "@",
    "date": "yyyy-mm-dd",
}
METHODS = ["Validated actual", "Calculated", "Reference value", "Judgment"]
AS_IS = "As-is model sample (illustrative)"

# ---------------------------------------------------------------- tab 1 entries
# step, id, entry, unit, definition, owner, where to find, default method,
# actual, calc (uses {ids}), reference, context, what would prove it wrong, leverage point, kind
STEPS = {
    1: ("Scope", "Sponsor"),
    2: ("Leadership beliefs", "Sales leader"),
    3: ("Financial results", "Finance"),
    4: ("Sales and marketing cost detail", "Finance"),
    5: ("Salesperson roster", "HR"),
    6: ("Territory plan", "Sales Operations"),
    7: ("CRM exports", "Sales Operations"),
    8: ("Compensation plan", "Compensation"),
    9: ("Vacancy and hiring timeline", "HR and Finance"),
    10: ("Rules and definitions", "Sales Operations and Finance"),
}

E = []


def add(step, id_, name, unit, definition, where="", method="Validated actual", actual=None, calc=None,
        ref=None, context="", test="", lev=None, kind="num", owner=None):
    E.append(dict(step=step, id=id_, name=name, unit=unit, definition=definition, owner=owner or STEPS[step][1],
                  where=where, method=method, actual=actual, calc=calc, ref=ref, context=context, test=test,
                  lev=lev, kind=kind))


# Step 1. Scope: direct entries that every other value inherits
add(1, "scope_business", "Business in scope", "text", "Whole company, or one channel, product line or sales motion",
    "Sponsor decision", kind="scope", actual="Whole company")
add(1, "period_start", "Period start", "date", "First day of the 12-month period every value describes", "Sponsor decision", kind="scope")
add(1, "period_end", "Period end", "date", "Last day of the period", "Sponsor decision", kind="scope")
add(1, "currency", "Currency", "text", "Reporting currency for every money value", "Sponsor decision", kind="scope", actual="USD")
add(1, "revenue_basis", "Revenue basis", "text", "Recognized revenue or bookings; every revenue value follows it",
    "Sponsor decision", kind="scope", actual="Recognized revenue")

# Step 2. Leadership beliefs: the market definition and goals; numeric beliefs go in the belief column of every entry below
add(2, "segmentation_basis", "How the market is divided into territories", "text",
    "Geography, industry, company size, named accounts, buyer problem, or a mix", "Sales leader", method="Judgment",
    test="Territory results differ more within a segment than between segments", lev=2, kind="text")
add(2, "theory_of_buying", "How our customers buy", "text", "The stated theory of who decides, how, and why",
    "Sales leader", method="Judgment", test="Won and lost deals do not follow the stated pattern", lev=2, kind="text")
add(2, "system_goal", "What the sales system is run to maximize", "text", "Bookings, margin, new logos, retention, or another goal",
    "Sponsor and sales leader", method="Judgment", test="Compensation and reviews reward something else", lev=3, kind="text")

# Step 3. Financial results
add(3, "revenue", "Revenue in scope", "currency", "Revenue for the period and scope, on the chosen basis",
    "Income statement or segment report", actual=25_000_000, context=AS_IS,
    test="Contracts × deal size, and the capacity chain, should reproduce it", lev=12)
add(3, "contracts", "Contracts closed", "count", "Executed agreements in the period that produced that revenue",
    "Billing or contract system", actual=755, context=AS_IS, test="Won opportunities in the CRM should match", lev=12)
add(3, "plan_target", "Revenue plan", "currency", "Revenue the plan expected for the period", "Annual plan",
    test="Territories × expected yield per territory should match", lev=3)
add(3, "cost_of_revenue_amt", "Cost of revenue", "currency", "Direct cost of delivering that revenue", "Income statement", kind="component")
add(3, "rnd_amt", "Research and development", "currency", "R&D expense for the period", "Income statement", kind="component")
add(3, "gna_amt", "General and administrative", "currency", "G&A expense for the period", "Income statement", kind="component")
add(3, "cost_of_revenue_pct", "Cost of revenue, % of revenue", "ratio", "Cost of revenue ÷ revenue", "Income statement",
    method="Reference value", calc="{cost_of_revenue_amt}/{revenue}", ref=0.1322, context="Industry average used in the as-is model",
    test="Income statement history shows a different ratio or a fixed component", lev=12)
add(3, "rnd_pct", "R&D, % of revenue", "ratio", "R&D ÷ revenue", "Income statement", method="Reference value",
    calc="{rnd_amt}/{revenue}", ref=0.1019, context="Industry average used in the as-is model",
    test="R&D does not move with revenue", lev=12)
add(3, "gna_pct", "G&A, % of revenue", "ratio", "G&A ÷ revenue", "Income statement", method="Reference value",
    calc="{gna_amt}/{revenue}", ref=0.154, context="Industry average used in the as-is model",
    test="G&A does not move with revenue", lev=12)

# Step 4. Sales and marketing cost detail
add(4, "base_salary", "Average base salary per salesperson", "currency",
    "Base pay of quota-carrying salespeople only; excludes managers, sales engineers and executives", "Payroll register",
    method="Reference value", ref=95_000, context=AS_IS, test="Payroll for quota-carrying roles differs", lev=12, kind="component")
add(4, "load_rate", "Benefits and payroll tax load", "ratio", "Benefits and payroll taxes ÷ base salary (no overhead allocation)",
    "Payroll and benefits ledger", method="Reference value", ref=0.23, context=AS_IS,
    test="Benefits ledger ÷ base payroll differs", lev=12, kind="component")
add(4, "loaded_salary", "Fully loaded salary per salesperson", "currency", "Base salary × (1 + load)", "Calculated from the two lines above",
    method="Calculated", calc="{base_salary}*(1+{load_rate})", test="Compensation cross-check against the ledger", lev=12)
add(4, "trip_fare", "Travel per trip: air, train, mileage", "currency", "Round trip, one salesperson", "Expense reports",
    method="Reference value", ref=750, context=AS_IS, kind="component")
add(4, "trip_ground", "Travel per trip: cabs, tolls, rental", "currency", "Per trip", "Expense reports",
    method="Reference value", ref=200, context=AS_IS, kind="component")
add(4, "trip_meals", "Meals per day", "currency", "Breakfast, lunch, dinner", "Expense reports",
    method="Reference value", ref=100, context=AS_IS, kind="component")
add(4, "trip_lodging", "Lodging per night", "currency", "Average room cost", "Expense reports",
    method="Reference value", ref=250, context=AS_IS, kind="component")
add(4, "trip_days", "Days per trip", "count", "Days away per trip", "Expense reports",
    method="Reference value", ref=2, context=AS_IS, kind="component")
add(4, "trip_entertainment", "Entertainment per trip", "currency", "Client meals and events per trip", "Expense reports",
    method="Reference value", ref=250, context=AS_IS, kind="component")
add(4, "trips_per_year", "Trips per year", "count", "Sales trips per salesperson per year", "Expense reports or calendars",
    method="Reference value", ref=25, context=AS_IS, kind="component")
add(4, "travel_per_salesperson", "Travel cost per salesperson", "currency",
    "Actual: quota salespeople's T&E ÷ salespeople. Calculated: trip build-up", "Expense ledger",
    method="Calculated", calc="(({trip_fare}+{trip_ground}+{trip_entertainment})+{trip_days}*({trip_meals}+{trip_lodging}))*{trips_per_year}",
    test="T&E ledger for quota salespeople differs", lev=12)
add(4, "oh_managers", "Non-quota sales manager salaries", "currency", "Managers who carry no quota", "General ledger",
    method="Reference value", ref=2_750_000, context=AS_IS, kind="component")
add(4, "oh_engineers", "Sales engineers and other non-quota support", "currency", "Pre-sales and support roles", "General ledger",
    method="Reference value", ref=6_000_000, context=AS_IS, kind="component")
add(4, "oh_admin", "Sales operations and administration", "currency", "Sales ops and admin staff", "General ledger",
    method="Reference value", ref=800_000, context=AS_IS, kind="component")
add(4, "oh_training", "Training", "currency", "Training costs, travel for training, related headcount", "General ledger",
    method="Reference value", ref=500_000, context=AS_IS, kind="component")
add(4, "oh_incentives", "Non-quota incentives", "currency", "Contests, recognition trips, non-quota commissions", "General ledger",
    method="Reference value", ref=750_000, context=AS_IS, kind="component")
add(4, "sales_overhead", "Sales overhead", "currency", "Non-variable cost of running the sales organization",
    "Sum of the lines above", method="Calculated",
    calc="{oh_managers}+{oh_engineers}+{oh_admin}+{oh_training}+{oh_incentives}", test="Ledger total differs", lev=12)
add(4, "mk_people", "Marketing personnel", "currency", "All marketing staff", "General ledger",
    method="Reference value", ref=1_000_000, context=AS_IS, kind="component")
add(4, "mk_web", "Website", "currency", "Website investment and maintenance", "General ledger",
    method="Reference value", ref=250_000, context=AS_IS, kind="component")
add(4, "mk_events", "Events", "currency", "Online events and roadshows", "General ledger",
    method="Reference value", ref=500_000, context=AS_IS, kind="component")
add(4, "mk_ads", "Advertising", "currency", "Paid media", "General ledger",
    method="Reference value", ref=500_000, context=AS_IS, kind="component")
add(4, "mk_mail", "Direct mail", "currency", "Print and online", "General ledger",
    method="Reference value", ref=250_000, context=AS_IS, kind="component")
add(4, "mk_leadgen", "Lead generation programs", "currency", "Telemarketing, SDR and BDR programs", "General ledger",
    method="Reference value", ref=250_000, context=AS_IS, kind="component")
add(4, "mk_brand", "Branding and public relations", "currency", "Identity, PR, consulting", "General ledger",
    method="Reference value", ref=200_000, context=AS_IS, kind="component")
add(4, "mk_collateral", "Collateral", "currency", "Sales tools, white papers, brochures, printing", "General ledger",
    method="Reference value", ref=750_000, context=AS_IS, kind="component")
add(4, "marketing", "Marketing", "currency", "Investment the company makes to help drive revenue", "Sum of the lines above",
    method="Calculated", calc="{mk_people}+{mk_web}+{mk_events}+{mk_ads}+{mk_mail}+{mk_leadgen}+{mk_brand}+{mk_collateral}",
    test="Ledger total differs", lev=12)
add(4, "commissions_paid", "Commissions paid to quota salespeople", "currency", "Commission expense for the period", "General ledger",
    kind="component")
add(4, "sales_comp_expense", "Quota salesperson compensation in the ledger", "currency",
    "Salaries, benefits and commissions of quota-carrying salespeople", "General ledger", test="Used by the compensation cross-check", lev=12)

# Step 5. Salesperson roster (pseudonymous; names never entered)
add(5, "filled_seats", "Quota-carrying salespeople at period end", "count", "People employed in quota-carrying roles",
    "HR roster export", test="Territory plan shows a different number of filled territories", lev=10)
add(5, "hires", "Salespeople hired in the period", "count", "Quota-carrying hires", "HR roster export", lev=10, kind="component")
add(5, "departures", "Salespeople who left in the period", "count", "Quota-carrying departures", "HR roster export", lev=10, kind="component")
add(5, "productive_salespeople", "Productive (ramped) salespeople", "count1",
    "Salespeople working at full productivity on average. Calculated: filled seats − hires × share of year spent ramping",
    "Roster with start dates", method="Calculated", calc="MAX(0,{filled_seats}-{hires}*MIN(1,{ramp_months}/12))",
    test="Productivity by tenure shows a different ramp", lev=10)

# Step 6. Territory plan (a design choice)
add(6, "territory_count", "Funded territories", "count",
    "Territories the company has decided to fund, filled or open. A territory is a design choice, not a person",
    "Territory plan", method="Reference value", ref=100, context=AS_IS,
    test="Filled + open territories differ from this count", lev=10)
add(6, "open_territories", "Open territories at period end", "count", "Funded territories with no salesperson assigned",
    "Territory plan", test="Roster and plan disagree", lev=10)
add(6, "expected_yield", "Expected yield per territory (average)", "currency",
    "Revenue a filled, ramped territory is expected to produce in a year", "Territory plan or quota letters",
    calc="{plan_target}/{territory_count}", test="Territories × expected yield differs from the plan", lev=3)

# Step 7. CRM exports
add(7, "opps_won", "Qualified opportunities won", "count", "Closed as won in the period", "CRM closed-opportunity report",
    kind="component")
add(7, "opps_lost", "Qualified opportunities lost", "count", "Closed as lost in the period", "CRM closed-opportunity report",
    kind="component")
add(7, "win_rate", "Close rate", "ratio", "Won ÷ (won + lost) qualified opportunities, by count", "CRM closed-opportunity report",
    method="Reference value", calc="{opps_won}/({opps_won}+{opps_lost})", ref=0.25, context=AS_IS,
    test="CRM won ÷ (won + lost) differs", lev=12)
add(7, "cycle_months", "Sales cycle (months)", "months",
    "Median time from qualified opportunity to signature for won deals", "CRM closed-opportunity report",
    method="Reference value", ref=6, context=AS_IS, test="CRM median cycle differs; Little's Law check fails", lev=9)
add(7, "deal_size", "Average revenue per contract", "currency", "Revenue ÷ contracts", "Calculated from step 3",
    method="Reference value", calc="{revenue}/{contracts}", ref=75_000,
    context="Reference value from another client, chosen so the model fits companies of any size (as-is model)",
    test="Revenue ÷ contracts differs (deal size cross-check)", lev=12)
add(7, "open_opps_total", "Open qualified opportunities", "count", "Average of month-end open qualified opportunities",
    "CRM month-end snapshots", kind="component")
add(7, "opportunities_load", "Opportunities each salesperson holds", "count1", "Open qualified opportunities ÷ salespeople",
    "Calculated from CRM snapshots and roster", method="Calculated", calc="{open_opps_total}/{filled_seats}",
    test="Little's Law check fails", lev=11)
add(7, "opportunities_capacity", "Opportunities a salesperson can manage at once", "count",
    "Most qualified opportunities a salesperson can hold and advance well at the same time", "Sales leader judgment",
    method="Reference value", ref=30, context=AS_IS,
    test="Win rate and cycle hold steady at loads above this level", lev=12)

# Step 8. Compensation plan
add(8, "commission_rate", "Commission rate", "ratio",
    "Actual: the plan rate. Calculated: commissions paid ÷ revenue", "Compensation plan",
    method="Reference value", calc="{commissions_paid}/{revenue}", ref=0.08, context=AS_IS,
    test="Commissions paid ÷ revenue differs from the plan rate", lev=5)

# Step 9. Vacancy and hiring timeline
add(9, "ramp_months", "Ramp time (months)", "months", "Months until a new salesperson reaches average productivity",
    "Sales manager, or productivity by tenure", method="Reference value", ref=12, context=AS_IS,
    test="New-hire productivity by month differs", lev=9)
add(9, "time_to_fill_days", "Days to fill an open territory (average)", "days", "From vacancy to the new salesperson's start date",
    "HR requisition records", test="Vacancy records differ", lev=9)
add(9, "approval_days", "Days to approve a requisition (average)", "days", "From vacancy to approved requisition",
    "HR and Finance approval records", test="Approval records differ", lev=9)

# Step 10. Rules and definitions
add(10, "qualification_definition", "When an opportunity counts as qualified", "text", "The rule the CRM stage uses",
    "Sales Operations", test="Qualified opportunities do not meet the stated rule", lev=5, kind="text")
add(10, "hiring_approval_rule", "Steps and approvers to fill a territory", "text", "Who approves a requisition, in what order",
    "HR and Finance", test="Approval records follow a different path", lev=5, kind="text")
add(10, "design_authority", "Who can change territory design or roles", "text", "Who decides territories, coverage and roles",
    "Sponsor", test="Changes were made by someone else", lev=4, kind="text")

IDS = {e["id"] for e in E}

CHECKS = [
    ("deal_size_triangulation", "Deal size", "Revenue ÷ contracts vs the deal size used", 0.10,
     "IFERROR(v_revenue/v_contracts,\"\")", "v_deal_size", "Revenue, contracts, deal size"),
    ("contracts_implication", "Contracts implied", "Territories × capacity × 12 ÷ cycle × close rate vs contracts", 0.10,
     "IFERROR(v_territory_count*v_opportunities_capacity*12/v_cycle_months*v_win_rate,\"\")", "v_contracts",
     "Territories, capacity, cycle, close rate"),
    ("revenue_implication", "Revenue implied", "Implied contracts × deal size vs revenue", 0.10,
     "IFERROR(v_territory_count*v_opportunities_capacity*12/v_cycle_months*v_win_rate*v_deal_size,\"\")", "v_revenue",
     "Territories, capacity, cycle, close rate, deal size"),
    ("littles_law", "Little's Law", "Contracts ÷ close rate ÷ productive salespeople × cycle ÷ 12 vs opportunities held", 0.25,
     "IFERROR(v_contracts/v_win_rate/v_productive_salespeople*v_cycle_months/12,\"\")", "v_opportunities_load",
     "Contracts, close rate, productive salespeople, cycle, opportunities held"),
    ("territory_counts", "Territory count", "Filled seats + open territories vs funded territories", 0.0,
     "IFERROR(v_filled_seats+v_open_territories,\"\")", "v_territory_count", "Filled seats, open territories, funded territories"),
    ("expected_yield_plan", "Expected yield vs plan", "Territories × expected yield vs revenue plan", 0.05,
     "IFERROR(v_territory_count*v_expected_yield,\"\")", "v_plan_target", "Territories, expected yield, plan"),
    ("comp_ledger", "Compensation vs ledger", "Salespeople × loaded salary + commission × revenue vs ledger compensation", 0.10,
     "IFERROR(v_filled_seats*v_loaded_salary+v_commission_rate*v_revenue,\"\")", "v_sales_comp_expense",
     "Salespeople, loaded salary, commission rate, revenue"),
]


def calc_formula(expr: str) -> str:
    for i in sorted(IDS, key=len, reverse=True):
        expr = expr.replace("{" + i + "}", "v_" + i)
    assert "{" not in expr, expr
    return f'=IFERROR({expr},"")'


def row_height(text: str, chars_per_line: float, base: float = 13.5) -> float:
    lines = max(1, math.ceil(len(text) / chars_per_line))
    return base * lines + 4


# ---------------------------------------------------------------- Orientation
def build_orientation(ws):
    ws.sheet_view.showGridLines = False
    widths = {"A": 3, "B": 8, "C": 26, "D": 62, "E": 48}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    total_chars = 140
    r = 2

    def para(text, font=f_body, gap=0):
        nonlocal r
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        c = ws.cell(r, 2, text)
        c.font, c.alignment = font, wrap
        ws.row_dimensions[r].height = row_height(text, total_chars if font.size <= 10 else 100)
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
         "business. The model asks you to write each claim down, say where it comes from, and say what would prove it "
         "wrong. Then it checks. If anyone later disagrees with a result, you can go straight back to the assumption behind it.")

    heading("How the model sees sales capacity")
    para("Two decisions create sales capacity, and they are separate:")
    para("•  Territories are a design choice. You decide how to divide your market, how many territories to fund, and "
         "what you expect each to yield. A territory without a salesperson still carries that expectation, so leaving it "
         "open has a cost.")
    para("•  Salespeople are a hiring choice. A salesperson's capacity is not the hours they work. It is how many "
         "opportunities they can hold and advance well at the same time, turned over by the length of your sales cycle.")
    para("Revenue happens where the two meet: salespeople assigned to territories, converting opportunities at your win "
         "rate and deal size, with every cost flowing through to operating income.")

    heading("How to use it")
    para("1.  State your assumptions (1) Data Entry). Work through the steps in order. Each step names who usually owns "
         "the data, so you can forward it to them. For every value, choose its input method:")
    for name, desc in [
        ("Validated actual", "confirmed by your Finance team from your records."),
        ("Calculated", "produced by the model's calculator from other entries (for example, revenue ÷ contracts)."),
        ("Reference value", "borrowed from another context; say which in the source column."),
        ("Judgment", "your best estimate; give a reason and a low–high range. The sales leader's beliefs go here first, before any data is collected."),
    ]:
        para(f"      –  {name}: {desc}")
    para("2.  Test and calibrate. The model combines your assumptions into what they imply (contracts, revenue, pipeline, "
         "compensation expense) and compares that with your actual results in the cross-checks at the end of tab 1. For "
         "each one that needs review, revise an assumption, explain the gap, or accept it as a known gap. When the list is "
         "resolved, Finance signs off the baseline.")
    para("3.  Explore what-if scenarios (later tabs). Change assumptions one at a time or in combination: territory design, "
         "hiring and fill speed, salesperson capacity, win rate, cycle, deal size, costs. Every change flows through to "
         "operating income, with nothing unexplained.")
    para("4.  Understand what stands in the way (later tabs). For each improvement, review the common obstacles and the "
         "conditions that would make it achievable.")

    heading("How to read the results")
    for t in ["•  Until Finance signs off, every result is labeled “Working model: not validated by Finance.”",
              "•  Every result shows how much of it rests on validated actuals and how much on calculations, reference values and judgment.",
              "•  Results are only as real as the assumptions behind them. To challenge a result, challenge an assumption on tab 1.",
              "•  Assumptions are revisited each period, so they become more accurate over time."]:
        para(t)

    heading("What this model is not")
    for t in ["•  Not a forecast. It describes what your system can and does produce under stated assumptions.",
              "•  Not an evaluation of individual salespeople. Salespeople are measured as a system, without names, to find improvements in how the system works.",
              "•  Not a benchmark ranking. Reference values from other contexts can inform assumptions, but your baseline is built from your own reality."]:
        para(t)

    heading("How tab 1 works")
    para("Each row on tab 1 is one entry. Its “Value used” cell (blue, outlined) is the only cell the rest of the model "
         "reads, by name. The yellow cells to its right are the ways to fill it; “Input method” chooses which one is used. "
         "Grey cells are calculated from other entries. Changing how an entry is filled never changes the model's logic.")
    legend = [("Yellow", fill_input, "Enter or choose a value"), ("Grey", fill_calc, "Calculated from other entries"),
              ("Blue, outlined", fill_used, "Value used: the cell other tabs reference")]
    for label, fill, desc in legend:
        ws.cell(r, 2).fill = fill
        ws.cell(r, 2).border = box
        ws.cell(r, 3, label).font = f_bold
        ws.cell(r, 4, desc).font = f_body
        r += 1

    heading("Collection sequence: who to ask, in what order")
    para("Steps 3 to 8 can go to their owners at the same time once steps 1 and 2 are done. Steps 9 and 10 need the territory plan.", f_note)
    hdr = ["Step", "Owner", "What we ask for", "What it unlocks"]
    for i, h in enumerate(hdr):
        c = ws.cell(r, 2 + i, h)
        c.font, c.fill, c.border = f_head, fill_head, box
    r += 1
    seq = [
        (1, "Sponsor", "Four answers: period, business in scope, currency, revenue basis", "Every request pre-filled with the same scope"),
        (2, "Sales leader", "Short questionnaire, no data: how the market is divided, expected yield, win rate, cycle, deal size, opportunities a salesperson can handle, ramp, time to fill", "Sealed beliefs; a working model on day one"),
        (3, "Finance", "Income statement for the period, and the plan", "Validated revenue, contracts and P&L; the first test of the beliefs"),
        (4, "Finance", "General ledger detail for sales and marketing cost centers", "Cost per salesperson, commission, overhead, marketing; compensation check"),
        (5, "HR", "Roster export of quota-carrying salespeople: start and end dates, role, salary band (no names)", "Filled seats, hires, departures, ramp state"),
        (6, "Sales Operations", "Territory list: assigned salesperson or open, expected yield, segment", "Open territories and expected yield vs plan"),
        (7, "Sales Operations", "CRM: closed opportunities in the period; month-end open opportunities", "Close rate, cycle, deal size, opportunities held; the belief gap"),
        (8, "Compensation", "Current compensation plan", "Commission rules checked against commissions paid"),
        (9, "HR and Finance", "For each open territory: opened, requisition approved, offer accepted, start", "Cost of open territories and approval time"),
        (10, "Sales Ops and Finance", "Qualification rule, hiring approval steps, who can change territory design", "Rules declared, so scenarios can change them"),
        (11, "Finance lead", "Review the cross-checks and sign off", "The signed baseline"),
    ]
    for row in seq:
        for i, v in enumerate(row):
            c = ws.cell(r, 2 + i, v)
            c.font, c.alignment, c.border = f_body, (center if i == 0 else wrap), box
        ws.row_dimensions[r].height = row_height(row[2], 60)
        r += 1

    heading("Workbook map")
    for t in ["•  Orientation: this page.",
              "•  1) Data Entry: the assumption ledger, in collection order, with cross-checks and sign-off.",
              "•  Later tabs (to be rebuilt): performance breakdown, impact on the income statement, scenario diagnostics. They read only the Value used cells on tab 1."]:
        para(t)
    para("For a sharper analysis, run the model separately for each sales channel and product line, and separate "
         "new-customer revenue from revenue from existing customers.", f_note)


# ---------------------------------------------------------------- Data Entry
COLS = ["Step", "ID", "Entry", "What it means", "Unit", "Input method", "Value used", "Validated actual", "Calculated",
        "Reference value", "Leadership belief (judgment)", "Low", "High", "Source or reference context", "Owner",
        "Where to find it", "What would prove it wrong", "Belief vs value used", "Leverage point"]
WIDTH = [6, 22, 36, 44, 9, 17, 15, 15, 15, 15, 16, 12, 12, 34, 18, 28, 36, 12, 9]
C = {name: i + 1 for i, name in enumerate(COLS)}


def build_data_entry(ws, wb):
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(WIDTH, 1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    ws["A1"] = "1) Data Entry: the assumption ledger"
    ws["A1"].font = f_title
    ws["A2"] = ("Each row is one entry. The rest of the model reads only the Value used column. Fill an entry any of the "
                "ways offered and choose the one to use in Input method. Work through the steps in order; each names its owner.")
    ws["A2"].font = f_note
    ws.merge_cells("A2:Q2")

    # summary panel (formulas filled after rows are known)
    ws["A4"], ws["C4"] = "", "Baseline status"
    ws["C4"].font = f_bold
    ws["D4"] = "Working model"
    ws["D4"].fill, ws["D4"].font, ws["D4"].border = fill_input, f_input, box
    dv_state = DataValidation(type="list", formula1='"Draft,Working model,In Finance review,Signed by Finance"', allow_blank=False)
    ws.add_data_validation(dv_state)
    dv_state.add("D4")
    ws["F4"] = '=IF(D4="Signed by Finance","Signed baseline: validated by Finance","Working model: not validated by Finance")'
    ws["F4"].font, ws["F4"].fill = f_bold, fill_banner
    ws.merge_cells("F4:J4")

    header_row = 9
    for name, col in C.items():
        c = ws.cell(header_row, col, name)
        c.font, c.fill, c.border, c.alignment = f_head, fill_head, box, Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[header_row].height = 30
    ws.freeze_panes = ws.cell(header_row + 1, C["Value used"] + 1)

    dv_method = DataValidation(type="list", formula1='"' + ",".join(METHODS) + '"', allow_blank=True)
    ws.add_data_validation(dv_method)
    dv_basis = DataValidation(type="list", formula1='"Recognized revenue,Bookings"', allow_blank=False)
    ws.add_data_validation(dv_basis)

    r = header_row + 1
    current_step = None
    entry_rows = []
    for e in E:
        if e["step"] != current_step:
            current_step = e["step"]
            name, owner = STEPS[current_step]
            label = f"Step {current_step}. {name}  ·  Owner: {owner}"
            if current_step == 2:
                label += "  ·  Fill the Leadership belief column for every number below before any data arrives"
            ws.cell(r, 1, label).font = f_bold
            for col in range(1, len(COLS) + 1):
                ws.cell(r, col).fill = fill_step
            r += 1
        row = r
        ws.cell(row, C["Step"], e["step"]).alignment = center
        ws.cell(row, C["ID"], e["id"])
        ws.cell(row, C["Entry"], ("    " if e["kind"] == "component" else "") + e["name"])
        ws.cell(row, C["What it means"], e["definition"])
        ws.cell(row, C["Unit"], e["unit"])
        ws.cell(row, C["Owner"], e["owner"])
        ws.cell(row, C["Where to find it"], e["where"])
        ws.cell(row, C["What would prove it wrong"], e["test"])
        ws.cell(row, C["Leverage point"], e["lev"]).alignment = center
        ws.cell(row, C["Source or reference context"], e["context"])
        for col in range(1, len(COLS) + 1):
            cell = ws.cell(row, col)
            cell.font = cell.font if cell.font.bold else f_body
            cell.border = box
            if cell.alignment.horizontal != "center":
                cell.alignment = wrap
        if e["kind"] == "component":
            ws.cell(row, C["Entry"]).font = Font(name=FONT, size=10, color="404040")
        else:
            ws.cell(row, C["Entry"]).font = f_bold
        fmt = FMT[e["unit"]]
        used = ws.cell(row, C["Value used"])
        L = {k: ws.cell(row, C[k]).coordinate for k in COLS}

        if e["kind"] == "scope":
            ws.cell(row, C["Input method"], "Direct entry").font = f_note
            used.value = e["actual"]
            used.fill, used.font = fill_input, Font(name=FONT, size=10, bold=True, color="0000FF")
            if e["id"] == "revenue_basis":
                dv_basis.add(used.coordinate)
        else:
            m = ws.cell(row, C["Input method"], e["method"])
            m.fill, m.font = fill_input, f_input
            dv_method.add(m.coordinate)
            used.value = (f'=IF({L["Input method"]}="Validated actual",IF({L["Validated actual"]}="","",{L["Validated actual"]}),'
                          f'IF({L["Input method"]}="Calculated",IF({L["Calculated"]}="","",{L["Calculated"]}),'
                          f'IF({L["Input method"]}="Reference value",IF({L["Reference value"]}="","",{L["Reference value"]}),'
                          f'IF({L["Input method"]}="Judgment",IF({L["Leadership belief (judgment)"]}="","",{L["Leadership belief (judgment)"]}),""))))')
            used.fill, used.font = fill_used, f_used
            for k, v in (("Validated actual", e["actual"]), ("Reference value", e["ref"]), ("Leadership belief (judgment)", None),
                         ("Low", None), ("High", None)):
                c = ws.cell(row, C[k], v)
                c.fill, c.font = fill_input, f_input
                c.number_format = fmt if e["unit"] != "text" else "@"
            for k in ("Source or reference context",):
                c = ws.cell(row, C[k])
                c.fill, c.font = fill_input, f_input
            calc = ws.cell(row, C["Calculated"])
            calc.fill = fill_calc
            if e["calc"]:
                calc.value = calc_formula(e["calc"])
                calc.number_format = fmt
            if e["unit"] != "text":
                gap = ws.cell(row, C["Belief vs value used"])
                gap.value = (f'=IF(OR({L["Leadership belief (judgment)"]}="",{L["Value used"]}="",'
                             f'{L["Input method"]}="Judgment"),"",IFERROR({L["Leadership belief (judgment)"]}/{L["Value used"]}-1,""))')
                gap.number_format = '+0%;-0%;0%'
                gap.fill = fill_calc
        used.number_format = fmt
        used.border = used_border
        wb.defined_names["v_" + e["id"]] = DefinedName("v_" + e["id"], attr_text=f"'{DE}'!${used.column_letter}${row}")
        ws.row_dimensions[row].height = max(row_height(e["definition"], 42), row_height(e["test"], 34), row_height(e["context"], 32))
        if e["kind"] != "scope":
            entry_rows.append(row)
        r += 1

    # Step 11: cross-checks
    r += 1
    ws.cell(r, 1, "Step 11. Reconcile and sign  ·  Owner: Finance lead  ·  For each check that needs review: fix an entry, explain the gap, or accept it as a known gap").font = f_bold
    for col in range(1, len(COLS) + 1):
        ws.cell(r, col).fill = fill_step
    r += 1
    chk_cols = ["", "Check ID", "Check", "What it compares", "", "Tolerance", "Status", "Implied by entries", "Observed",
                "Gap", "Entries that could be wrong", "Resolution", "Category", "Note"]
    for i, h in enumerate(chk_cols, 1):
        if h:
            c = ws.cell(r, i, h)
            c.font, c.fill, c.border, c.alignment = f_head, fill_head, box, Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[r].height = 30
    r += 1
    dv_res = DataValidation(type="list", formula1='"Fixed,Explained,Accepted as known gap"', allow_blank=True)
    dv_cat = DataValidation(type="list", formula1='"Definition,Timing,Scope,Data quality,Reference value,Other"', allow_blank=True)
    ws.add_data_validation(dv_res)
    ws.add_data_validation(dv_cat)
    first_chk = r
    for cid, name, compares, tol, implied, observed, cands in CHECKS:
        vals = {2: cid, 3: name, 4: compares, 6: tol, 8: "=" + implied, 9: f'=IF({observed}="","",{observed})', 11: cands}
        for col, v in vals.items():
            c = ws.cell(r, col, v)
            c.font, c.border, c.alignment = f_body, box, wrap
        ws.cell(r, 3).font = f_bold
        ws.cell(r, 6).number_format = "0%"
        ws.cell(r, 6).fill, ws.cell(r, 6).font = fill_input, f_input
        unit_fmt = "#,##0.00" if cid in ("littles_law",) else '$#,##0;($#,##0);"-"' if cid in (
            "deal_size_triangulation", "revenue_implication", "expected_yield_plan", "comp_ledger") else "#,##0"
        for col in (8, 9):
            ws.cell(r, col).number_format = unit_fmt
            ws.cell(r, col).fill = fill_calc
        ws.cell(r, 10, f'=IF(OR(H{r}="",I{r}=""),"",IFERROR(I{r}/H{r}-1,""))').number_format = "+0%;-0%;0%"
        ws.cell(r, 10).fill, ws.cell(r, 10).border = fill_calc, box
        st = ws.cell(r, 7, f'=IF(OR(H{r}="",I{r}=""),"NEEDS DATA",IF(ABS(J{r})<=F{r},"PASS","REVIEW"))')
        st.font, st.border, st.alignment = f_bold, box, center
        for col in (12, 13, 14):
            c = ws.cell(r, col)
            c.fill, c.font, c.border = fill_input, f_input, box
        dv_res.add(ws.cell(r, 12).coordinate)
        dv_cat.add(ws.cell(r, 13).coordinate)
        ws.row_dimensions[r].height = max(row_height(compares, 42), row_height(cands, 32))
        r += 1
    last_chk = r - 1

    # utilization is a bound, not a match: add it as its own row
    vals = {2: "utilization", 3: "Utilization", 4: "Opportunities held ÷ opportunities a salesperson can manage; cannot exceed 100%",
            6: 1.0, 8: '=IFERROR(v_opportunities_load/v_opportunities_capacity,"")', 11: "Opportunities held, capacity"}
    for col, v in vals.items():
        c = ws.cell(r, col, v)
        c.font, c.border, c.alignment = f_body, box, wrap
    ws.cell(r, 3).font = f_bold
    ws.cell(r, 6).number_format = "0%"
    ws.cell(r, 6).fill, ws.cell(r, 6).font = fill_input, f_input
    ws.cell(r, 8).number_format = "0%"
    ws.cell(r, 8).fill = fill_calc
    ws.cell(r, 9).fill = fill_calc
    ws.cell(r, 10).fill = fill_calc
    st = ws.cell(r, 7, f'=IF(H{r}="","NEEDS DATA",IF(H{r}<=F{r},"PASS","REVIEW"))')
    st.font, st.border, st.alignment = f_bold, box, center
    for col in (12, 13, 14):
        c = ws.cell(r, col)
        c.fill, c.font, c.border = fill_input, f_input, box
    dv_res.add(ws.cell(r, 12).coordinate)
    dv_cat.add(ws.cell(r, 13).coordinate)
    ws.row_dimensions[r].height = 30
    last_chk = r

    green = PatternFill("solid", start_color="C6EFCE")
    amber = PatternFill("solid", start_color="FFEB9C")
    grey = PatternFill("solid", start_color="E7E6E6")
    rng = f"G{first_chk}:G{last_chk}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"PASS"'], fill=green))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"REVIEW"'], fill=amber))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"NEEDS DATA"'], fill=grey))

    # summary panel formulas
    f_rng = ",".join(f"F{x}" for x in entry_rows)
    ws["C5"], ws["C6"] = "Values in use, by input method", "Cross-checks"
    ws["C5"].font = ws["C6"].font = f_bold
    method_col = "F"
    used_col = "G"
    rows_min, rows_max = min(entry_rows), max(entry_rows)
    for i, mname in enumerate(METHODS):
        col = 4 + i
        ws.cell(7, col, mname).font = f_note
        ws.cell(5, col, f'=SUMPRODUCT(({method_col}{rows_min}:{method_col}{rows_max}="{mname}")*(LEN({used_col}{rows_min}:{used_col}{rows_max})>0))')
        ws.cell(5, col).font, ws.cell(5, col).alignment = f_bold, center
        ws.cell(7, col).alignment = center
    ws.cell(5, 8 + 0)
    ws["H5"] = f'=SUMPRODUCT((LEN({method_col}{rows_min}:{method_col}{rows_max})>0)*(LEN({used_col}{rows_min}:{used_col}{rows_max})=0)*(LEFT({method_col}{rows_min}:{method_col}{rows_max},6)<>"Direct"))'
    ws["H5"].font, ws["H5"].alignment = f_bold, center
    ws["H7"] = "Waiting for data"
    ws["H7"].font, ws["H7"].alignment = f_note, center
    for i, s in enumerate(["PASS", "REVIEW", "NEEDS DATA"]):
        ws.cell(6, 4 + i, f'=COUNTIF(G{first_chk}:G{last_chk},"{s}")&" {s.lower()}"').font = f_bold
        ws.cell(6, 4 + i).alignment = center
    ws.row_dimensions[7].height = 14
    return entry_rows


def main():
    wb = Workbook()
    ws_o = wb.active
    ws_o.title = "Orientation"
    build_orientation(ws_o)
    ws_d = wb.create_sheet(DE)
    build_data_entry(ws_d, wb)
    for ws, landscape in ((ws_o, False), (ws_d, True)):
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws_d.print_title_rows = "9:9"
    wb.properties.creator = "Growth Enablement"
    wb.properties.title = "Commercial Effectiveness Model"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
