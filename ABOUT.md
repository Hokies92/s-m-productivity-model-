# About the Sales Capacity Model

> **Current understanding (2026-10-24):** the model is a falsifiable system model of a company's commercial engine. Its data tab is an assumption ledger: every entry is a written, testable claim with a declared basis, tested against the company's own financial results before any what-if runs. Territory design and hiring are separate decisions, linked by assignment. Full description: [docs/MODEL_UNDERSTANDING.md](docs/MODEL_UNDERSTANDING.md). The text below describes the project's origin and the as-is model, and is kept as written.


## The claim

**Sales capacity is not labor hours. It is cognitive bandwidth constrained by time.**

A salesperson does not "spend hours" on deals. They hold deals in working memory while each deal moves through the customer's decision process on the customer's clock. That gives every salesperson two hard ceilings:

1. **Cognitive load:** how many live opportunities one person can hold and advance well at the same time. Effort does not raise it.
2. **Resolution time:** how long the customer takes to decide. Pushing harder shortens it only by degrading conversion.

```
Capacity (opportunities per year) = Cognitive load limit × (12 ÷ sales cycle months)
```

Thirty opportunities held on a six-month cycle turn over twice a year: sixty opportunities, no matter how many leads arrive or how many hours are worked.

## Why it exists

Most sales planning assumes capacity equals headcount equals hours. If that were true, adding salespeople, leads, calls, meetings, content or training would raise revenue in proportion. Companies do all of these routinely and the revenue doesn't follow.

The model was built to show, with arithmetic anyone can audit, where the real limits are and which levers actually move profit. Its consistent answer: improving how well each opportunity is handled (close rate, cycle time, deal size) beats adding volume (territories, leads), because quality levers raise output without raising cost in proportion.

## Where it came from

Scott Santucci built the model in 2000 as a VP of Sales. It extended an earlier model he co-created with the CFO at META Group, where he was the company's top salesperson, to make the case for transforming sales and marketing.

The origin was personal. Following the prescribed sales methodology to the letter nearly got him fired. He had to prove his problem was not more leads, more training, more content, more objection handling, more calls or more meetings. "More" was exactly the wrong thing. So he rebuilt the math himself, drawing on how a competitive swimmer thinks: more strokes don't make you faster; efficiency through the water does. His compensation rewarded growth in contract value over the average, and he used that to turn $15,000 transactions into structured programs worth $90,000, $300,000 and $1 million.

Underneath the model sits a view of buying decisions: a decision moves when it is **timely** (the customer's situation and personal readiness), **relevant** (impact relative to cost), and **in context** (the person's role, motivation and environment). The model measures what that produces: close rate, cycle time and deal size.

| Year | Milestone |
|------|-----------|
| 2000 | Model created |
| 2003 | Audited for accuracy by Ernst & Young |
| 2011 | Updated as the Sales and Marketing Efficiency Model |
| 2026 | Documented, formula-audited, and rebuilt as this Python package |

## What makes it different

- **Territory ≠ headcount ≠ capacity.** A territory is a workload container. Headcount is people. Capacity is throughput, set by cognition and time. Conventional models treat all three as one number.
- **Cycle time is a divisor of throughput**, not just a metric on a dashboard.
- **Operational drivers carried to operating income.** Most models vary price or cost. This one varies the physics of how revenue is produced and follows it through the P&L.
- **Leads are deliberately left out of the core equation.** Past the processing ceiling, extra leads are ignored, worked badly (lower close rate) or create overload (longer cycles). The package adds an optional lead input that shows whether a team is lead-constrained or capacity-constrained.

## Relationship to Hidden Commercial Costs

The model is the first proof of a broader idea: conventional management conflates things that should be separate (territory, headcount and capacity in sales; activity and results in commercial spend), and that conflation misallocates capital. The Hidden Commercial Costs work applies the same constraint-based thinking to what an organization actually purchases with its commercial spending.

## Status and honesty about the numbers

- The engine reproduces every output of the original workbook exactly (`scm verify`, 48/48).
- The original contains deliberate test values (an engine salary that differs from the entry sheet; a reference deal size; ramp credited two ways). They test whether a reader composes the whole before judging a part. See [docs/MODEL.md §6](docs/MODEL.md). The engine reproduces them as the as-is oracle; options expose the alternatives.
- Under every combination of those options, the conclusion holds: each quality lever beats adding territories.
- The model measures the outcome of selling quality. It does not yet model how to produce it.

© 2000–2026 Growth Enablement. All rights reserved. The model and its logic are owned by Growth Enablement.

Author: Scott Santucci · scott.santucci@growthenablement.com
