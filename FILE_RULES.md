# File rules

Where every file lives, what may change it, and what must never be in it. Applies to the repository (github.com/Hokies92/s-m-productivity-model-) and to the Claude Project's Knowledge.

© 2000–2026 Growth Enablement. All rights reserved.

## 1. Repository layout

Folders marked † do not exist yet; they are created by the first change that needs them.

```
source/                     EVIDENCE. Immutable; nothing is ever added, changed or removed here.
  Sales_and_Marketing_Effectiveness_Model_original.xls
  workbook_cells.csv        formula export of the original (415 cells)
canonical/                  THE ONE STATEMENT. Changed only with Scott's approval.
  FOUNDATION.md             what the model is; Gate 1 scope and acceptance
  INTENT_LEDGER.md          confirmed and open intent, item by item
schemas/ †                  CONTRACTS between workbook, engine, export and web
  inputs.schema.json
  outputs.schema.json       stable id, unit and definition for every result
src/sales_capacity_model/   PYTHON. Engine (oracle), exports, web adapters
tools/                      BUILD. Workbook builder, recalculation, formula dump, rubric
tests/                      Every acceptance test in FOUNDATION §7, plus parity
  source.sha256             checksums of source/; a test fails if any source file changes
workbook/                   GENERATED. Never edited by hand
  Sales_Capacity_Model.xlsx
  Sales_Capacity_Model.formulas.csv †   text dump of every cell, for review and diff
  Sales_Capacity_Model.manifest.json
web/ †                      Data entry and output pages (schemas only; no model formulas)
docs/                       Guides for users and builders. Not canonical
docs/archive/               Superseded documents, each with a one-line status at the top
examples/ †                 Synthetic input sets only (the original sample; invented test companies)
.github/                    CI workflow, pull request template, CODEOWNERS
CHANGELOG.md  README.md  FILE_RULES.md  CONTRIBUTING.md (the version-control rules)  NOTICE  pyproject.toml
```

## 2. Rules by kind of file

| Kind | Rule |
|---|---|
| `source/` | Never modified, renamed or re-exported. A checksum test (`tests/source.sha256`) enforces it. |
| `canonical/` | One statement only. A change needs Scott's explicit approval in the pull request. Any other document that disagrees with it is corrected or archived in the same pull request. |
| Generated files (`workbook/`) | Produced only by `tools/`. A pull request that changes a generated file must include the source change that produced it, and CI rebuilds and compares. Reviewers read `.formulas.csv`, not the binary. |
| Workbook format | Core model: `.xlsx`, no macros. Optional companion (`.xlsm` or Office Scripts) only for illumination or workflow; no result may depend on it. |
| Schemas | Every input and output has a stable id, unit and definition. Ids never change meaning; a renamed or removed id is a major version change. |
| Python | Package code in `src/`; build and test tooling in `tools/`. Type-hinted, tested, formatted with `ruff`. No network calls in the engine. |
| Tests | Each acceptance requirement has a named test. A test is never weakened to make a change pass; changing a test needs the reason in the pull request. |
| Documents | Write a document only when someone will use it. No documents whose purpose is to govern Claude's behavior. Superseded documents go to `docs/archive/` with a status line, never left beside the current one. |
| Names | Files: `Title_Case_With_Underscores` for deliverables, `snake_case` for code. No dates or "final", "v2" or "new" in file names; versions live in git tags. |

## 3. Never in the repository

- Client data, client names or anything that identifies a client. Client input sets live outside the repository (a private store Scott controls). `.gitignore` excludes `clients/`, `*.client.*` and `private/`.
- Credentials, tokens or keys.
- Hand-edited copies of generated files.
- Large binaries other than the original and the released workbook. Releases attach their files to the GitHub Release.

## 4. Claude Project Knowledge

| Path | Holds | Changed by |
|---|---|---|
| `source/original_workbook_formula_export.csv` | The formula export (evidence) | Never |
| `Sales_and_Marketing_Effectiveness_Model_original.xls` | The original (evidence) | Never |
| `canonical/FOUNDATION.md` | Copy of the repository's canonical statement | Scott, when a canonical change merges |
| `canonical/INTENT_LEDGER.md` | Copy of the repository's intent ledger | Scott, when it changes |

Nothing else. Historical and superseded documents live only in the repository's `docs/archive/`, so they are never read as current.

Knowledge mirrors the repository's `canonical/` after each accepted change. If the two differ, the repository's merged version governs, and Knowledge is updated.

## 5. Deliverables to Scott

A workbook, document or export goes to Scott as a file with a one-line description. A version for acceptance is a pull request with its CI results and the built files attached to it, never a description of the work.
