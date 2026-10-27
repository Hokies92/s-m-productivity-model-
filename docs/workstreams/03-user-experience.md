# Workstream 3 — Make the model understandable

## Purpose and boundary

Help a person who does not think in systems enter information, explore choices and understand the economic consequences. Preserve useful detail through clear language and progressive disclosure. The experience must explain the model as implemented; it must not invent causal findings or hide missing data.

## Accountable roles

Experience lead: design, language and usability evidence. Scott: business clarity and presentation review. Workbook and technical leads: implementation and data mapping. Roles besides Scott are unassigned.

## Inputs

Original Data Entry sheet and diagnostic content; stream 1 definitions; stream 2 workbook candidate; stream 4 data and result contracts; `docs/design/assisted-data-entry-and-state.md`.

## Work plan

1. Map who provides each input and how they obtain it: executive estimate, finance totals, sales operations detail or reviewed imported data.
2. Design enter-a-total, build-from-detail and estimate options where useful. Show what's included, unit, time period and active value. Make source comparison available without forcing different populations to match.
3. Design real-time feedback: cost composition, available performance metrics and clear complete/partial/unavailable states. Explain unallocated expense without adding it twice.
4. Design individual and combined scenario selection, baseline comparison and a plain-language bridge from input changes to revenue and operating income.
5. Create context-sensitive explanations and diagnostic prompts. Label source-based observations, conditional implications and recommendations distinctly.
6. Review workbook screens and exports for clarity, detail, accessibility, and the agreed clean exhibit style. Test representative tasks with Scott or intended users and record what they can and cannot understand.
7. Work with stream 4 on selected web inputs and custom output views that use the same definitions; verify that visible controls do what they claim.

## Deliverables and handoffs

- Entry and output flows, input descriptions, explanatory copy, visual examples and a task-based usability checklist.
- A mapping of each control and explanation to stream 4's contract and stream 2's workbook cells.
- Evidence of comprehension and visual review, plus a list of issues, for the Gate 1 pack.

## Milestones and completion

Initial milestone: a walkthrough using original illustrative values, including an unknown required expense. Gate 1 experience evidence: a user can enter or select assumptions, identify the active values, compare scenarios, trace their financial consequences and identify missing information without needing to understand code. Scott reviews the actual candidate.

## Dependencies and controls

Use stream 1 to establish meaning, stream 2 for real workbook behavior and stream 4 for format/status. Design aids must not quietly substitute assumptions or imply that a conditional scenario proves an intervention's cause.

## First actions

Map the current Data Entry sheet, draft one guided entry flow for salary or travel, and demonstrate how its active value reaches the financial result. Agree a reviewer and timeline after inventory.
