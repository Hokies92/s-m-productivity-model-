# Workstream 4 — Build the technical foundation

## Purpose and boundary

Make inputs, calculations, saved state, exports and bounded web outputs agree across the project. Use Python where useful for analysis, repeatable builds and verification; the business rules must remain documented, inspectable and tied to original evidence.

## Accountable roles

Technical lead: contracts, integration and automated evidence. Workbook lead: Excel implementation and platform verification. Model analyst: reference cases. Scott: meaning and final gate decisions. Roles besides Scott are unassigned.

## Inputs

Protected source and existing oracle/tests, stream 1 mappings and cases, stream 2 workbook, stream 3 experience needs, charter and repository rules.

## Work plan

1. Inventory the current engine, workbook generator, schemas and tests; report what exists, what was executed and what remains unverified. Preserve original reference and behavior.
2. Define shared input/output IDs, units, scope, source, active selection, completeness and version. Distinguish observations from model rules and scenario interventions.
3. Specify how baseline and named scenario state is saved and versioned; a scenario references a baseline and cannot silently change it. Document actual storage used versus planned storage.
4. Use independent reference cases to compare calculation outputs and investigate discrepancies. Validate numerical tolerances, blank/zero behavior, isolated and combined scenarios, and financial bridges.
5. Define a versioned visualization export and test it with a consumer; include metric definitions, currency, period, model version and completeness.
6. Build a bounded web demonstration of entry and selected output using the same approved calculation rules. Where calculation logic must remain private, keep it server-side; document if the demonstrator uses synthetic data and does not persist.
7. Assemble reproducible build and test evidence for the exact candidate. Distinguish Python tests, workbook recalculation in a named Excel build, visual review and web demonstration.

## Deliverables and handoffs

- Versioned calculation and data contracts, reference cases, automated checks, build manifest and a documented storage design.
- Integration evidence linking Excel, export and web demo on the same inputs, including unsuccessful or unavailable checks.
- Release-ready evidence inputs for stream 2, control mappings for stream 3 and scope questions for stream 1.

## Milestones and completion

First: existing implementation inventory and shared definitions. Next: repeatable calculations and an export contract tested end to end. Gate 1 technical evidence: original cases reconcile under the specified behavior, scenarios remain isolated, export and bounded web output match approved cases, and native Excel verification is recorded separately. Production hosting and a full multi-user platform are not implied by a demonstration.

## Dependencies and controls

Use stream 1 as reference and stream 2 as the workbook source; stream 3 specifies interactions. No second undocumented calculation engine; no live customer data in repository fixtures; do not assume a database or production hosting exists.

## First actions

Inventory existing code, test results and compatibility; propose the smallest shared example and data contract needed for the first entry-to-output integration check. Assign owner and timing after inventory.
