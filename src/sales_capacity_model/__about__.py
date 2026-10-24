"""Package identity and the About / Product Overview text shown by `scm about` and `scm overview`."""

__title__ = "sales-capacity-model"
__version__ = "2.1.0"
__author__ = "Scott Santucci"
__email__ = "scott.santucci@growthenablement.com"
__license__ = "Proprietary"
__copyright__ = "Copyright (c) 2000-2026 Growth Enablement. All rights reserved."
__summary__ = (
    "A cognitive-temporal throughput model of sales capacity, "
    "connected to the income statement."
)
__url__ = "https://github.com/Hokies92/s-m-productivity-model-"

ABOUT = f"""\
SALES CAPACITY MODEL  v{__version__}
{__summary__}

WHAT IT IS
  A model that answers one question: what actually limits sales output, and
  which operational lever improves profit most? It treats a salesperson as a
  processing system with two hard limits, not as a block of labor hours:

    1. Cognitive load  - how many live opportunities one person can hold and
                         advance well at the same time.
    2. Resolution time - how long the customer's decision takes. Elapsed time,
                         mostly on the customer's clock, not the salesperson's.

  Capacity = Cognitive load limit x (12 / sales cycle months)

  From there it traces close rate, deal size and territory count through to
  revenue, fully loaded sales cost, and operating income, and compares four
  levers: add territories, raise close rate, shorten cycle, raise deal size.

WHY IT EXISTS
  Conventional sales planning assumes capacity = headcount = hours, so more
  reps, leads, calls and meetings should mean proportionally more revenue.
  That assumption fails in practice. This model was built to show, with the
  arithmetic, that "more" is usually the wrong answer and that the quality of
  how each opportunity is handled drives margin.

ORIGIN
  Built in 2000 by Scott Santucci, then a VP of Sales, from an earlier model
  he co-created with a CFO at META Group to transform sales and marketing.
  It grew out of his own experience: following the prescribed playbook
  nearly got him fired, so he rebuilt the math himself, drawing on how a
  competitive swimmer thinks about efficiency over effort. Audited for
  accuracy by Ernst & Young (2003). Updated as the Sales and Marketing
  Efficiency Model (2011). Documented, audited and rebuilt in Python (2026).

WHAT MAKES IT DIFFERENT
  - Separates territory, headcount and capacity, which most models treat as one.
  - Treats cognitive load as a hard ceiling and cycle time as a divisor of
    throughput, not just a metric to report.
  - Varies operational drivers, not just financial inputs, and carries them
    to operating income.
  - Leaves leads out of the core equation on purpose: past the processing
    ceiling, more leads are waste, worse close rates, or longer cycles.

STATUS
  The Python engine reproduces all 48 outputs of the original workbook
  exactly (`scm verify`). Three defects found in the workbook and three open
  decisions are documented in AUDIT_FINDINGS.md and exposed as options.

Owner:   Growth Enablement. The model and its logic are proprietary.
Author:  {__author__} <{__email__}>
Source:  {__url__}
"""

OVERVIEW = """\
PRODUCT OVERVIEW - Sales Capacity Model

WHO IT IS FOR
  CFOs, CROs / VPs of Sales, CEOs, boards and private equity operating
  partners deciding where the next commercial dollar should go.

THE DECISION IT SUPPORTS
  "We want X% more revenue. Do we hire, or do we get better?"
  The model puts both answers on the same income statement.

WHAT GOES IN  (defaults are illustrative; replace with your actuals)
  Structure    territories, average deal size
  Cost         base salary, load rate, travel, commission rate,
               sales overhead, marketing
  Mechanics    opportunities manageable at once, sales cycle (months),
               ramp time (months), close rate
  P&L shape    cost of revenue, R&D and G&A as % of revenue
  Optional     leads per territory (shows whether you are lead-constrained
               or capacity-constrained)

WHAT COMES OUT  (for each scenario)
  Throughput   max opportunities / rep / year, deals / rep, revenue / rep
  Cost         cost per rep, rep costs, sales and marketing cost
  Profit       operating income, change vs baseline, % net gain, S&M ROI
  Guidance     the five common obstacles for each quality lever, and their
               root causes

SCENARIOS
  baseline, add territories, raise close rate, shorten cycle, raise deal
  size, combined quality levers, improve all. Each lever's change is
  adjustable (default 10%).

AT THE DEFAULTS (10% per lever, original workbook logic)
  Add territories   revenue flat in year 1, operating income -2.25M
  Close rate        +11.25M revenue, operating income +5.98M (+18.8%)
  Cycle time        +12.50M revenue, operating income +6.65M (+20.9%)
  Deal size         +11.25M revenue, operating income +5.98M (+18.8%)

HOW TO USE IT
  scm about                     this description
  scm overview                  this overview
  scm template > my_inputs.json write default inputs to edit
  scm run --inputs my_inputs.json
  scm run --adjust 0.15 --ramp-rule steady_state --json
  scm diagnose close_rate       obstacles for one lever
  scm verify                    prove the engine matches the workbook

  Python:
    from sales_capacity_model import ModelInputs, run_scenarios
    results = run_scenarios(ModelInputs(territories=40, close_rate=0.3))

OPTIONS FOR THE OPEN DECISIONS (see AUDIT_FINDINGS.md)
  --use-entered-salary   use base salary x (1 + load rate) instead of the
                         workbook's hard-coded 87,750
  --ramp-rule            workbook (default, reproduces original),
                         year_one (new territories earn only post-ramp
                         revenue in every scenario), or steady_state
                         (full-year credit everywhere)

LIMITS
  Measures the outcome of selling quality (close rate, cycle, deal size);
  it does not model how to produce it. Cognitive load is an input, not
  derived. Non-sales operating costs are modeled as % of revenue.
"""
