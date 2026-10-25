# Working rules

## What is protected

Only these are "never rewrite":

- `source/` — the original workbook and its 415-cell export.
- The as-is oracle: `src/sales_capacity_model/` with default options, and `tests/test_model.py` (48/48 parity).
- Verbatim original text quoted in `docs/AS_IS_INDEX.md`.

Everything else dated 2026 is interpretation. When an interpretation is found wrong, it is corrected in place or moved to `docs/archive/` with a one-line status at the top. A dated note on top of a wrong reading is not a correction.

## One current statement

`docs/MODEL.md` is the single statement of what the model is: definitions, units, the chain, the kinds of assumption and where each lives, the deliberate test values, the invariants. Any document that disagrees with it is wrong, and is corrected or archived.

## Every commit

Tests pass before the commit, not after. Then the message states three things:

```
<summary line>

Invariant: <which invariant in docs/MODEL.md this serves, by number>
Changed:   <artifacts touched>
Left:      <artifacts deliberately not touched, and why>
```

A change that cannot name an invariant does not go in.

## Terminology

Salespeople are agents measured as a system. Use "salesperson" / "salespeople". Not the s-word and not the three-letter abbreviation of "representative". Enforced by `tests/test_terminology.py` on every text file outside `source/`, `tools/archive/` and `docs/archive/`.

## Three kinds of assumption

| Kind | What it is | Where it lives |
|---|---|---|
| State | A belief about the commercial system as it is, testable against actuals | The register (tab 1, `register` schema) |
| Method | An equation or reasoning rule the modeller applies to the register | Beside the formula, in words (logic sheets; `modeller` schema) |
| Intervention | A hypothesis about a change ("close rate +10%") | The modeller's scenario table; never the register |
