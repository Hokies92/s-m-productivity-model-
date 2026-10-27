# Workstream 1 — Understand the original

## Purpose and boundary

Explain what Scott's model was designed to do, what each part actually calculates, and what its author intended. Provide the reference that all other workstreams use. Preserve the original workbook, formula export and as-is oracle. This stream records proposed improvements separately from original behavior.

## Accountable roles

Scott: author, source of intent and business-meaning decisions. Model analyst: prepares evidence and questions. Project coordinator: records decisions and distributes updates. Roles other than Scott are unassigned.

## Inputs

Original workbook and formula export; `docs/MODEL.md`; existing source maps, tests and examples; Scott's explanations. Separate direct source, confirmed author intent, mathematical consequence and unconfirmed interpretation.

## Work plan

1. Inventory orientation, data entry, performance breakdown, impact analysis and scenario diagnostics. Map every purpose, entry, scenario and output to its source location.
2. Describe operating and financial rules in plain language and show how each result traces to inputs and applied assumptions.
3. Record original versus applied values, including the author-confirmed distinctions for salary and transaction value. Preserve both original ramp treatments and flag unresolved intent instead of guessing.
4. Document reference cases: original example, changed individual levers, combined scenarios and chosen boundary cases. Hand expected results to stream 4 for independent verification.
5. Prepare concise, evidence-backed questions for Scott where meaning cannot be inferred. Record answers, sources, date, impact and open issues in the intent ledger.
6. Map original definitions and diagnostics to the proposed modern workbook; review scope changes with streams 2–4.

## Deliverables and handoffs

- Source-to-function map, input/output definitions, scenario inventory and a source-linked intent ledger.
- Reference-case pack with exact inputs, expected outputs and original-source locations.
- Plain-language model explanation for stream 3; test cases for streams 2 and 4; research questions for stream 5.
- Canonical changes to `docs/MODEL.md` follow CONTRIBUTING and Scott's decisions; this plan itself is not a replacement canonical statement.

## Milestones and completion

Reference inventory complete when each original input group, scenario and named output is mapped. Gate 1 evidence complete when the reference cases support reproduction and Scott can trace the comparison from inputs to operating income. Unresolved intent is visible; it need not be invented to proceed with faithful reproduction.

## Dependencies and controls

Stream 2 needs the map before declaring parity; stream 4 helps check cases independently. A modern feature must not rewrite original evidence. Distinguish tests of original output from assessment of whether a company's model is economically complete.

## First actions

Review existing mappings and `docs/MODEL.md` before creating duplicates; inventory gaps; bring Scott a short list of questions and concrete examples. Dates and assignee are to be agreed after the inventory.
