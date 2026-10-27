> **Archived 2026-10-26.** Superseded by [canonical/FOUNDATION.md](../../canonical/FOUNDATION.md). Kept for the record; not current.

# System Diagnostic: original, repository, and the logic that produced it

Date: 2026-10-25. Requested by Scott Santucci after two days of rebuild work (16 commits).
Question: is there a failure contagion between the original workbook, the interpretations of it, the repository, the deliberate test values in the original, and the category errors made during the rebuild?

Answer: yes. The mechanism is described below, with evidence from the repository as it stands at commit `d3da7dc`.

© 2000–2026 Growth Enablement. All rights reserved.

---

## 1. The original: what it is and what it was testing

Five sheets, one-way flow: Data entry → Performance breakdown (mechanics per scenario) → Impact Analysis (pro forma income statement) → Scenario Diagnostic (obstacles per scenario). Every input pulled by reference; the same chain in every scenario column; the scenario size an input (row 7). It is already a logic sheet plus a results sheet plus a prescription sheet.

Three values in it were placed deliberately, and each tests one thing about the reader:

| Value | Where | What it tests | What I did |
|---|---|---|---|
| Salary $87,750 typed into the engine while tab 1 computes $116,850 | Performance breakdown C11 | Whether the reader understands that tab 1 cells are *entries* that other tabs reference, and that an entry can be overridden by any input method. Logic, not numbers. | Called it defect F1, built an engine option around it (`use_entered_salary`), wrote it into eight documents and the package's own `about` text. |
| Deal size $75,000 while revenue ÷ contracts = $33,113 | Data entry F11 vs E12:E13 | Whether the reader understands scope: a reference value from another context is valid for a general model and invalid as a claim about this client. | Called it a "genuine data problem" and an "operator error." Then, told it was deliberate, invented a reference story (75,000 × 1.17) instead of asking. |
| 12-month ramp with (12 − ramp)/12 credit | Data entry F35; Performance breakdown E25, K25 | Whether the reader can hold two scenario treatments at once and ask which is the assumption. | Called F2 and F3 defects; built a `ramp_rule` option with three values. |

The pattern in the right-hand column is the diagnosis. Each time, I located a discrepancy between two numbers, labeled it, and proposed to fix it. That is analytical reduction: judge each part against another part. The model asks for the opposite: understand how the parts compose into one calculation first, then ask what each value is *for*. The deliberate values were a test of which method the reader uses. I failed it three times with the same method, and when corrected, I moved the label and kept the method.

## 2. The contagion path

### 2.1 First interpretation written as fact, then frozen

Day 1 produced `AUDIT_FINDINGS.md` ("three defects"), `ABOUT.md`, `PRODUCT_OVERVIEW.md`, `Discovery_and_Architecture_Assessment.md`, the JSON spec, the .docx, and `__about__.py`. The "defect" reading is in all of them. It is also **in code**: `inputs.py` defines `WORKBOOK_HARDCODED_SALARY` and options named for the findings.

When the correction came, the repository rule "as-is documents are never rewritten; superseded readings get a dated note" was applied to these files. That rule exists to protect the 2000 artifact. These files are not the 2000 artifact. They are 2026 interpretations, and the rule froze the wrong interpretation in place with a note on top. Evidence today:

- `ABOUT.md:56`: "the 2026 formula audit found three defects in the workbook" — described in `AS_IS_INDEX.md` as "describes the as-is software accurately."
- `src/sales_capacity_model/__about__.py:62`: same sentence, shipped in `scm about`.
- `spec/...json:422`, `PRODUCT_OVERVIEW.md:107`, `Discovery_and_Architecture_Assessment.md:18,141,200` ("The hard-code is a defect, not a choice").

**Category error 1: the as-is artifact vs my reading of it.** Only `source/` and the parity engine are as-is. Everything else dated 2026 is interpretation and must be corrected, not annotated.

### 2.2 A correct correction turned into a totalizing rule

"The data tab is an assumption ledger" is right. My response was to make *everything* an assumption:

- `DATA_MODEL_REQUIREMENTS.md` DM-08: "No value enters a calculation unless it is an assumption in the ledger."
- `DATABASE_SCHEMA.md:14`: "Everything the model reasons with is an assumption."
- `schema.sql` layer 9: scenarios stored as `scenario_change` rows against assumption fields, in the same database as the register, with scenario-only entities carrying a `scenario_id`.
- Workbook v1 (`tools/archive/build_workbook_ledger_v1.py`): 20 columns per entry, leverage-point tag on every cell, a leadership-belief column, nine scenarios.

The circularity Scott identified on 2026-10-25 (scenario claims in the register validate against nothing and contaminate the baseline) was already built into the schema on 2026-10-24. I proposed it again verbally a day later because the schema had made it feel settled.

**Category error 2: three kinds of "assumption" merged under one word.** (a) State assumptions: beliefs about the system as it is, tested against actuals; these are the register. (b) Method assumptions: the equations and reasoning the modeller applies (revenue linear in close rate, cycle enters as 12 ÷ cycle, commission on revenue produced); these live with the logic, in words beside formulas. (c) Intervention hypotheses: "we can raise close rate 10%"; these are scenarios, conditional on the register, tested by nothing until the next period's register shows the result. Only (a) belongs in the ledger.

### 2.3 Three artifacts, three units of throughput

- Python engine (`engine.py:3`): "The throughput chain (per territory)"; `sales_costs = territories × cost_per_rep`.
- `MODEL_UNDERSTANDING.md` §4: Little's Law at the salesperson level; territory is a design choice.
- Current workbook `2) What-If Logic`: per salesperson, `v_filled_seats`.

No test connects them. The engine is faithful to the as-is and is the parity oracle; the docs state the corrected unit; the workbook implements the corrected unit. All three are in `main` with nothing saying which is the model.

**Category error 3: territory vs salesperson as the unit**, resolved in prose, unresolved in code.

### 2.4 Tests cover the artifacts that are not the product

20 tests: 11 on the as-is Python engine, 8 on the schema, 1 terminology regex. The workbook, which is the actual deliverable, has none. Every verification of it was a scratch script Scott never saw, reported back as numbers. That is why the review burden fell on him: the only check on the product was his reading of my summary.

### 2.5 Instance fixes, not class fixes

- The salesperson terminology rule was implemented as a regex for one banned word. The abbreviation of "representative" survived in 33 places including `__about__.py`, `ABOUT.md`, `PRODUCT_OVERVIEW.md`. The principle (salespeople are agents measured as a system; use the word that says so) was not implemented; one token was.
- `MIN` ignoring blanks was fixed in the one cell that showed it, not by a rule for how blank inputs are read.
- Each correction from Scott produced a local patch plus a new rule (DM-08, the terminology test, the as-is note), and the rules then accumulated as more things to monitor.

### 2.6 Documentation as sediment

22,500 words across 12 Markdown files, versus a 945-line builder and a 400-line engine. Each iteration added a document rather than correcting one. The early documents are the longest and the most wrong. To check any claim, a reviewer has to know which document is current, and the repository does not say in one place.

## 3. The logic I was following

Stated plainly: reactive local repair. For each correction, find the nearest artifact, patch it, annotate the rest, add a rule, report results. There was no written statement of the model's invariants to check a build against, so each build was checked against my latest understanding, which changed with every correction. Preservation ("don't lose the as-is") and correction ("my reading was wrong") were handled with the same tool, the dated note, so wrong readings were preserved as carefully as the original.

## 4. Category errors, enumerated

1. As-is artifact vs 2026 interpretation of it (froze both).
2. State assumptions vs method assumptions vs intervention hypotheses (all called "assumption"; scenarios in the register).
3. Territory vs salesperson as the unit of throughput (three artifacts disagree).
4. Deliberate test value vs defect vs data error (all three deliberate values labeled wrong, then re-labeled, never understood as tests of method).
5. Preservation vs correction (one tool for both).
6. Results vs logic (numbers reported as the deliverable; the chain was the deliverable).
7. Instance vs class (token fixes for principle-level rules).

## 5. Remedy: structural, not another document

1. **One current statement of the model.** `docs/MODEL.md`: definitions, the unit of each quantity, the chain in order, the three kinds of assumption and where each lives, the deliberate test values and what each tests, the invariants. Under 1,500 words. Every other 2026 document is either corrected to match it or moved to `docs/archive/` with one status line. Only `source/`, the parity engine, and the verbatim original text keep "never rewrite" protection.
2. **Invariants as tests, on the product.** (a) New workbook reproduces the original's four quality scenarios (contracts, revenue, ΔOI) from the same inputs. (b) Structure: one-way sheet flow; every `v_` name referenced exists; every logic row has its rule in words; no scenario field in the register. (c) Language: the salesperson rule applied to the whole class of banned words (the s-word and the abbreviation of "representative"), outside `source/` and quoted original text.
3. **Resolve the unit in code.** The Python engine is either renamed as the as-is oracle (`asis/`) and nothing else, or regenerated from the same specification as the workbook. It cannot stay in `main` as a third model.
4. **Separate the modeller's data from the register's data.** Scenario definitions (id, levers, multipliers, method version, register version run against) live in the modeller, in their own table or sheet, never in the assumption schema. Schema layer 9 is moved out.
5. **Change protocol, to lower the monitoring cost.** Each commit states: which invariant it serves; which artifacts it changed; which it deliberately left. If a change cannot name an invariant, it does not go in.

## 6. What stands

- `source/` frozen; 415-cell export; as-is parity 48/48; branch `as-is-2026-10-24`.
- The corrected understanding in `MODEL_UNDERSTANDING.md` §§3–5, 9–10 (territory as design choice, Little's Law per salesperson, scope of reference values, lineage).
- The current workbook's architecture (client view + logic sheet per stage, pro forma income statement, one-way flow), which is the original's architecture restored.
- The 4-step collection order and the three input methods.
