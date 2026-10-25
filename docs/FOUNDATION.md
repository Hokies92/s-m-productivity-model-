# Foundation: what stands, what was learned, and why it makes a different model

Date: 2026-10-25. Companion to [SYSTEM_DIAGNOSTIC.md](SYSTEM_DIAGNOSTIC.md), which records what went wrong, and to [MODEL.md](MODEL.md), which states what the model is. This records what held, and why those four things are enough to build on. Of the four, the first is the as-is itself; the second, third and fourth are the evolution's foundations, and they are stated here as such.

© 2000–2026 Growth Enablement. All rights reserved.

---

## 1. The four things that stand

### 1.1 The frozen source and the parity engine

**What it is.** `source/` holds the 2000 workbook (2011 edition) untouched, and a 415-cell export of every formula and value. The Python package, with default options, reproduces all 48 of its outputs, and a test proves it on every change.

**Why it matters.** It is the oracle. Every claim about what the original does can be checked against a formula, not a memory. Without it, the rebuild would be a new model that resembles the original; with it, the rebuild can be proven to *be* the original, made workable. It also fixes the boundary of "as-is": whatever is not in `source/` or reproduced by the oracle is interpretation.

**Lesson learned.** The boundary was drawn correctly on day one and then ignored: 2026 documents were given the same protection as the source. The lesson is that preservation applies to the artifact and the oracle, and to nothing else. Interpretations get corrected.

### 1.2 Territory as a design choice; Little's Law at the salesperson

**What it is.** A territory is a funded decision about how to divide a market, carrying an expected yield whether or not anyone sits in it. A salesperson is a hiring decision. Capacity belongs to the salesperson and is cognitive, not temporal: the number of opportunities one person can hold and advance well, turned over by the cycle. Revenue happens at the assignment of one to the other.

```
resolved per salesperson per year = opportunities worked at once × (12 ÷ cycle months)
contracts  = resolved × close rate
revenue    = contracts × deal size × salespeople
```

**Why it matters.** It is the model's point of view, and it is what no other sales calculator has. Quota math treats territory, headcount and capacity as one number. Separating them produces questions the others cannot ask: what does an open territory cost; what is the yield of a territory versus the throughput of the person in it; where does the constraint bind, in the design, in the staffing, in the pipeline, or in the person's bandwidth. The original encoded this in 2000 by scaling a per-person throughput by a territory count and treating ramp as time before a territory yields. The rebuild makes the two decisions explicit entries.

**Lesson learned.** Three artifacts in the repository currently use different units for the same chain (engine per territory, documents per salesperson, workbook per salesperson). A point of view that lives only in prose is not yet in the model. The unit is an invariant and belongs in a test.

### 1.3 The workbook architecture: client view and logic sheet, one-way flow

**What it is.** Four stages, each reading only the stage before it: inputs → value used (named) → scenario chain and pro forma income statement → client view. Each stage has a sheet a client uses and a sheet a reviewer audits, where every calculation is one row with its rule in words beside the formula.

**Why it matters.** This is the original's architecture (data entry → performance breakdown → impact analysis), restored after a detour into a single 20-column ledger. It is what let E&Y audit the model in 2003 and what lets a client's Finance team audit it now. The income statement is the enabling constraint: a lever only counts if its effect survives the trip through cost of revenue, commission and operating expense to operating income. The one-way flow is what makes the model falsifiable: a result can always be traced back to the entry that produced it, and nothing downstream can reach back and change an entry.

**Lesson learned.** Complexity that tracks the steps without doing the calculation is the wrong complexity. The test of a logic sheet is that someone can read it top to bottom and recompute the result by hand.

### 1.4 Four-step collection and three input methods

**What it is.** Data is collected in the order a client can most easily assemble it: financial results (Finance), sales and marketing costs (Finance), territories and salespeople (Sales Operations and HR), pipeline and mechanics (Sales Operations). Every entry can be filled three ways: validated by Finance, the client's own entry, or the model's estimate from other entries; blank falls to a labeled sample default so the model runs from day one.

**Why it matters.** It is the register in practice. Each entry carries its basis, so every result can say how much of it rests on validated actuals. The estimates are the cross-checks: revenue ÷ contracts beside the deal size entered; commissions paid ÷ revenue beside the plan rate; the model's own baseline revenue beside the revenue reported. Where two of a client's numbers cannot both be true, the sheet says so. That is the discipline the original asked for in its directions ("enter your historical data or assumptions") made mechanical.

**Lesson learned.** The register holds beliefs about the system as it is. It does not hold scenario hypotheses, and it does not hold the modeller's equations. Mixing them makes the baseline validate against itself.

## 2. Why these four make a different model

Other sales capacity tools (quota calculators, territory planners, CRM forecasting) share one structure: capacity = people × hours × activity rate, and the question is how many people. They cannot distinguish a design problem from a staffing problem from a bandwidth problem, because they have one variable where this model has three. They have no register, so an input is never tested against the client's own actuals. They have no income statement in the loop, so an improvement is measured in bookings, not in operating income. And they are not falsifiable: nothing in them can be shown wrong by the next quarter's numbers.

The four things that stand are each one half of a distinction the others collapse:

| Distinction | Collapsed elsewhere into | Held here by |
|---|---|---|
| Territory vs salesperson vs capacity | headcount | §1.2, as separate entries and a stated unit |
| Belief vs actual | "input" | §1.4, basis per entry and cross-checks |
| State vs method vs intervention | "assumption" | the register / logic sheet / modeller split |
| Bookings vs operating income | revenue | §1.3, the income statement as constraint |
| The model vs a reading of it | documentation | §1.1, the frozen source and oracle |

A model that holds all five distinctions can do what the others cannot: say where the constraint binds, say how much of its answer is validated, say what an improvement is worth after costs, and be proven wrong. That is the product. Everything in the remedy (one statement of the model, invariants as tests, one unit in code, the modeller separated from the register) exists to keep those five distinctions from collapsing again, in the repository or in the next person's reading of it.

## 3. What the deliberate test values taught

The original contains values placed to test the reader's method: a salary typed into the engine that differs from the one computed on the entry sheet; a deal size that contradicts revenue ÷ contracts; a ramp handled two ways. A reader who compares parts to parts finds "defects." A reader who first asks how the whole composes finds that entries can be overridden, that reference values have a scope, and that ramp is an assumption to declare. The values are a filter for synthesis over reduction, and they are kept in the source for that reason. The rebuild's register is the mechanism that makes the same test explicit for every entry: declare the basis, declare the scope, let the cross-checks say where two claims collide.
