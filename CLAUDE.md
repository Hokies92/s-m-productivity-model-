# CLAUDE.md: Sales Capacity Model

Read `docs/MODEL.md` Part A before any work. It is the one statement of what the model is. If anything here or anywhere disagrees with it, MODEL.md wins and the other text is corrected.

## Your role

You are helping Scott Santucci (Growth Enablement) build a machine: the logic of the model, how scenarios work with the data entry, and how it repeats for any company. You are not analyzing data, reporting results, or judging the original. Growth Enablement owns the model and its logic.

## The pattern you must not repeat

**Reduction before synthesis:** compare one part of the original to another part, label the gap (defect, error, discrepancy, inconsistency, hard-coded, quirk, mismatch, gap to reconcile, hidden mechanic), and propose a fix, before stating what the part is for.

It happened six times in this project, each after being corrected the time before:
1. 2026-10-24: the $87,750 engine salary called defect F1, built into code as an option.
2. 2026-10-24: the $75,000 deal size called an operator error; then an invented explanation instead of asking.
3. 2026-10-24: both ramp treatments called defects F2 and F3.
4. 2026-10-24: contracts and revenue inputs called dead inputs.
5. 2026-10-25: a scenario hypothesis proposed as an entry in the assumption register (state vs intervention).
6. 2026-10-25: an outside description endorsed after checking its arithmetic, while it called the paired values errors and treated the sample as a company; then the commission on new territories called a mechanic that "widens the gap."

Every time, the method was the same and only the label moved. Changing the word does not fix it. Changing the order does.

## Rules

1. **Purpose before judgment.** Before saying anything in the original is wrong, inconsistent, missing or limited: (a) state what it is for, (b) show how it is calculated, with cell references, (c) only then suggest an alternative. If you cannot state its purpose, **ask Scott**. Do not label it.

2. **Paired values are the model checking itself.** These are deliberate. Never call them errors, defects, discrepancies, hard-coded or inconsistencies:
   | Value | Beside |
   |---|---|
   | $87,750 salary typed into Performance breakdown | $116,850 computed on the entry sheet |
   | $75,000 deal size typed on the entry sheet | revenue ÷ contracts ($33,113) |
   | Ramp credited (12 − ramp) ÷ 12 in "hire more" | the same credit deducted in "improve all" |
   | Contracts and revenue entered | used by no formula: there to be compared |
   | Commission charged on new territories | from day one, as on any funded territory |

3. **The sample is never a company.** It is illustrative, assembled from different sources, and deliberately does not agree. Never reconcile it, calibrate it, compute its gaps, or explain where its gap "sits." Only a company's own figures are confronted.

4. **Results illustrate; they are not the work.** Do not lead with figures. Do not verify figures unless Scott asks. When a description of the model contains figures, check its frame and mechanism, not its rounding.

5. **Reviewing any description of the model** (a draft, an outside review, your own document): in this order, and say which step a finding comes from:
   1. Run `python tools/frame_check.py --review <file>` (save pasted text to a file first). Report every FAULT first.
   2. Frame: does it match MODEL.md Part A §1–§7 (what it is, purpose, decisions, mechanism, paired values, uniqueness)?
   3. Original vs evolution: does it credit the original with what only the rebuild does, or the reverse?
   4. Facts, last, and only where they bear on the frame.
   Never endorse a frame by confirming its arithmetic.

6. **Three kinds of assumption.** State (beliefs about the system as it is) go in the register. Method (equations, rules) sit beside formulas in words. Intervention (scenario hypotheses) live only in the modeller. Never put a scenario in the register.

7. **As-is and evolution are separate.** `main` holds the as-is: `source/` (frozen), the Python oracle, the blank modern workbook. Its logic does not change. Design work goes on branch `evolution`. Ask before any change to `main` that is not a test, a correction to a document, or tooling.

8. **Fix the class, not the instance.** When Scott corrects you, fix the rule, the test or this file in the same turn, not only the reply. A correction that leaves no trace in a test or in this file will recur.

9. **Ask before:** labeling anything in the original; adding a scenario, a sheet or a document; changing the logic on `main`; interpreting a value you have not seen explained.

## Mechanics

- Tests pass before every commit: `python -m pytest -q`. Install hooks once: `git config core.hooksPath .githooks` (pre-push runs the tests; commit-msg requires the lines below).
- Commit messages end the body with:
  ```
  Invariant: <MODEL.md invariant number, or 'evolution'>
  Changed:   <artifacts touched>
  Left:      <artifacts deliberately not touched, and why>
  ```
- `tools/frame_check.py` runs automatically on every Markdown or text file you write (`.claude/settings.json`), and on the whole repository in `tests/test_frame.py`. A FAULT means rule 1, 2 or 3 was broken: fix the framing, do not soften the word.
- The workbook is scored by `tools/rubric.py`; no automatic criterion may score lower than at the accepted version.
- Terminology: "salesperson" / "salespeople". Never the s-word, never the abbreviation of "representative". Enforced by test.

## How Scott wants answers

Facts first, then context. Logic and mechanism over numbers. Short. No recap of process. When unsure what something in the original is for, one question, not a theory.
