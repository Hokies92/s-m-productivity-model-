# Score sheet

**Gate: PASS**

| ID | Criterion | Method | Score | Measured |
|---|---|---|---|---|
| G1 | Original inputs typed in -> every numeric formula on Performance breakdown and Impact Analysis matches the original | AUTO | 2 | 199 of 199 matched |
| G2 | Every original numeric formula cell (all sheets) is mapped and matches | AUTO | 2 | 200 matched of 200 original numeric formula cells (0 unmapped; 1 excluded as stray) |
| G3 | No typed constant in any formula on engine or analysis sheets (literals other than 0, 1, 12, 100) | AUTO | 2 | 0 formulas with typed constants |
| G4 | Both original ramp treatments reproduced (Performance breakdown E25 and K25 match) | AUTO | 2 | 2 of 2 |

## Dimensions (counted)

| ID | Dimension | Criterion | Method | Score | Measured |
|---|---|---|---|---|---|
| A1 | A. Layout | Sheet order follows the work: orient -> enter -> scenarios -> income statement -> obstacles | HUMAN | — | UNSCORED (human) |
| A2 | A. Layout | Each sheet reads only sheets before it in presentation order | AUTO | 2 | 0 backward references |
| A3 | A. Layout | One titled section per sheet; nothing needed is below the fold without a visible pointer (1366x768) | HUMAN | — | UNSCORED (human) |
| A4 | A. Layout | Ten sampled output cells each trace to an input in two clicks | HUMAN | — | UNSCORED (human) |
| B1 | B. Collection | Every input unlocked and filled; every formula locked; sheet protection on without password | AUTO | 2 | 0 violations |
| B2 | B. Collection | Every input has label, unit, definition, where-to-find and the original's explanation | AUTO | 2 | 38 of 38 inputs complete |
| B3 | B. Collection | Every input cell has data validation | AUTO | 2 | 38 of 38 validated |
| B4 | B. Collection | Blank workbook recalculates with zero error values | AUTO | 2 | 0 error cells |
| B5 | B. Collection | Inputs that can be entered or calculated show both, say which is in use, never silently prefer one | HUMAN | — | UNSCORED (human) |
| B6 | B. Collection | Detail rows are grouped under their totals (outline level set) | AUTO | 2 | 24 of 24 detail rows grouped |
| B7 | B. Collection | A Finance person can fill the entry sheet alone, forwarded without the rest of the workbook | HUMAN | — | UNSCORED (human) |
| C1 | C. Scenarios | Scenario sizes are unlocked, labeled, validated input cells | AUTO | 2 | 4 of 4 |
| C2 | C. Scenarios | Within each chain row, the scenario columns (baseline excluded) share one skeleton plus at most one pass-through form; the revenue row mapped from the original's row 25 may have three, as the original does | AUTO | 2 | 29 of 29 rows consistent |
| C3 | C. Scenarios | Every chain row carries its rule in words | AUTO | 2 | 29 of 29 |
| C4 | C. Scenarios | Perturbing each input (after original inputs are typed) changes at least one output and introduces no error | AUTO | 0 | 31 of 35 inputs move an output cleanly |
| D1 | D. Analysis | Impact Analysis lines, including % net gain and S&M ROI, match the original | AUTO | 2 | 95 of 95 |
| D2 | D. Analysis | Cost ratios (cost of revenue, R&D, G&A) are inputs on the entry sheet | AUTO | 2 | 3 of 3 |
| D3 | D. Analysis | Each scenario column shows change vs baseline for revenue, costs and operating income | HUMAN | — | UNSCORED (human) |
| E1 | E. Diagnostic | All original Scenario Diagnostic text present word for word | AUTO | 2 | 41 of 41 texts present |
| E2 | E. Diagnostic | Diagnostic text cells wrap and their rows are taller than default | AUTO | 2 | 17 of 17 long texts wrapped |
| F1 | F. Presentation | One typeface; at most four font sizes across the workbook | AUTO | 2 | 1 typefaces ['Arial'], 4 sizes [9.0, 10.0, 12.0, 16.0] |
| F2 | F. Presentation | Freeze panes on every sheet with a table; numeric formula cells carry a number format | AUTO | 2 | 0 sheets without freeze panes; 0 of 113 formulas in General format |
| F3 | F. Presentation | Every sheet set to fit one page wide | AUTO | 2 | 0 sheets not fit to width |
| F4 | F. Presentation | Gridlines off on presentation sheets, on for the entry sheet | AUTO | 2 | 0 sheets wrong |
| F5 | F. Presentation | No external links, no macros, blank file recalculates without error | AUTO | 2 | 0 problems |
| F6 | F. Presentation | Attribution: Growth Enablement with the original year; no historical attribution outside source/ | AUTO | 2 | GE=True year=True historical=False |

## Totals

| Dimension | Scored | Of | Unscored (human) |
|---|---|---|---|
| A. Layout | 2 | 2 | 3 |
| B. Collection | 10 | 10 | 2 |
| C. Scenarios | 6 | 8 | 0 |
| D. Analysis | 4 | 4 | 1 |
| E. Diagnostic | 4 | 4 | 0 |
| F. Presentation | 12 | 12 | 0 |

Automatic criteria: **38 / 40**. Human criteria are scored only from a reviewer file.

## Evidence

**B4** 0 error cells
- {}

**C4** 31 of 35 inputs move an output cleanly
- entry_12: no output changed
- entry_13: no output changed
- entry_16: no output changed
- entry_17: no output changed
