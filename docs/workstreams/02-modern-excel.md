# Workstream 2 — Modernize the model in Excel

## Purpose and boundary

Deliver a modern, usable Excel model that preserves the original model's purposes, original scenarios, diagnostic content and financial outputs. Make improvements to workflow, design and maintainability visible and traceable. An unapproved change to economic behavior is a proposed future model, not a faithful reproduction.

## Accountable roles

Workbook lead: implementation and evidence. Scott: business and usability acceptance. Model analyst: reference interpretation. Technical lead: shared contracts and automated verification. Roles besides Scott are unassigned.

## Inputs

Original workbook and protected source, current workbook/build tools and repository tests, stream 1 reference cases, stream 3 design, stream 4 contract, charter Gate 1 requirements.

## Work plan

1. Inventory what the current candidate already implements against original functions and G1-01–G1-12. Distinguish repository-reported checks from tests executed on the candidate.
2. Map original input groups, calculation rows, scenario columns, output rows and diagnostics into stable modern locations. Preserve the original numerical rules and stated/applied values.
3. Address known modern-candidate problems: required missing expenses must not disappear into complete-looking operating income, and a displayed active value must actually drive the result it claims to drive.
4. Implement guided entry, useful validation, normal-zoom readability, explanations and scenario controls using appropriate native Excel features. Keep core calculation functional without macros; document support for optional automation.
5. Test original and nondefault reference cases, missing versus zero, calculations, scenario isolation, and reporting. Review print and screen presentation with stream 3.
6. Have a named supported Excel installation recalculate, save, reopen and exercise the workflows. Record version, screenshots, results and unresolved issues; automated Python or another spreadsheet engine is supplemental evidence.
7. Deliver a candidate workbook, manifest, mapping, test results, known limitations and demonstration for Scott's acceptance.

## Deliverables and handoffs

- Modern Excel candidate and reproducible build instructions, with visible source/active-value mapping.
- Scenario comparison and interpretation outputs for stream 3; versioned input and result payloads for stream 4.
- Parity, completeness and native Excel evidence for the shared Gate 1 record; corrections/questions to stream 1.

## Milestones and completion

First: reference-to-candidate inventory and a priority list. Next: usable workbook with mapped calculations. Gate 1 workbook evidence: source-defined scenarios and financial outputs reproduced, nondefault and partial-input cases checked, native Excel workflow tested, and Scott's visual and usability review recorded. Export/web evidence is coordinated with stream 4 and does not follow automatically from workbook parity.

## Dependencies and controls

Stream 1 supplies the reference; stream 3 supplies approved entry and explanation designs; stream 4 supplies shared format and independent checks. Do not overwrite protected source or use an unreviewed correction to make parity pass.

## First actions

Inspect the existing workbook, builder, manifest and rubric; reproduce the known partial-input and inactive-value issues; propose the smallest reviewable fix. No calendar dates or responsible individual have yet been assigned.
