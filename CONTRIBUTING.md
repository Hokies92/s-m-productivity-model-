# Version control

Strict rules for every change to github.com/Hokies92/s-m-productivity-model-. They apply to Claude, to Scott and to any other contributor. A rule here is not waived for a small change.

© 2000–2026 Growth Enablement. All rights reserved.

## 1. Branches

| Branch | Purpose | Rules |
|---|---|---|
| `main` | The released, accepted product. Always releasable. | Protected. No direct pushes, no force pushes, no deletion. Changes arrive only by pull request. |
| `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `test/<slug>`, `build/<slug>`, `chore/<slug>` | One change each, short-lived (days, not weeks) | Branched from current `main`; rebased on `main` before review; deleted after merge. |
| `release/vX.Y.Z` | Preparing a release (version number, CHANGELOG, built files) | Only release changes; merged by pull request. |
| `evolution` | The redesign. Parked until Gate 1 is accepted. | No work until Scott reopens it; then it is rebased on the accepted release. |

No other long-lived branches. Snapshots are tags, not branches.

## 2. Settings Scott enables on GitHub (one time)

Settings → Rules → Rulesets, for `main`:
- Require a pull request before merging; 1 approval; dismiss stale approvals on new commits; require review from Code Owners (`CODEOWNERS`: `* @Hokies92`).
- Require status checks to pass, up to date with `main`. Today CI has one job, `test` (all tests, including parity and source integrity): require it now. Add each further check in §5 to the required list when its CI job exists.
- Require linear history (squash merge only).
- Block force pushes and deletion.
- Restrict who can create tags matching `v*` to Scott.

## 3. Commits

Format (Conventional Commits):

```
<type>(<scope>): <summary in the imperative, under 72 characters>

Changed:  what this commit changes, by file or artifact
Left:     what it deliberately does not touch, and why
Verified: the tests and checks run, and their results
Refs:     #<issue>

Co-Authored-By: ...        (when Claude contributes)
```

- Types: `feat` (new capability), `fix` (wrong behavior corrected), `docs`, `test`, `build`, `refactor` (no behavior change), `chore`.
- One logical change per commit. Tests pass before the commit, not after.
- A change to a generated file is committed together with the source change that produced it, never alone.
- No commits of client data, credentials or hand-edited generated files (FILE_RULES §3).

## 4. Pull requests

Every pull request:
1. References an issue that states the problem and the acceptance test.
2. States which of the three it touches (original, modern implementation, evolution) and whether it is a correction, an extension or an alternative.
3. Lists what changed, what was deliberately left alone, and how it was verified. CI results are the evidence; a claim of "tested" without a CI run is not accepted.
4. Attaches the built workbook and its formula dump when the workbook changes.
5. Is reviewed and approved by Scott. Claude never approves or merges.

Pull request template (`.github/pull_request_template.md`):

```
## What and why
Issue: #
Touches: original / modern implementation / evolution — correction / extension / alternative

## Changed

## Deliberately left alone

## Verification
- [ ] Parity: 200/200 original formula results, 48/48 oracle outputs
- [ ] Source checksums unchanged
- [ ] Workbook rebuilt from source; formula dump matches
- [ ] Behavior tests (completeness, zeros, bounds, constraints, protection)
- [ ] CHANGELOG updated under Unreleased

## Files for review
```

## 5. Required checks (CI on every pull request and on `main`)

| Check | Fails when | In CI today |
|---|---|---|
| source integrity | Any file in `source/` differs from `tests/source.sha256` | Yes, inside `test` |
| parity | Any of the 200 original formula results or 48 oracle outputs differ | Yes, inside `test` |
| behavior and terminology | Any test fails (completeness, zeros, bounds, constraints, protection, schema, engine–workbook agreement, terminology) | Yes, inside `test` (the tests that exist) |
| `build-reproducible` | Rebuilding the workbook from `tools/` gives a formula dump different from the committed one | No: first Gate 1 build task |
| `lint` | `ruff` reports an error | No: added with a one-time formatting pass |

A failing check blocks the merge. A check is never disabled or weakened to let a change through.

## 6. Versions and releases

Semantic versioning, one version for the product (workbook, engine, schemas): `vMAJOR.MINOR.PATCH`.

| Part | Increments when | Example |
|---|---|---|
| MAJOR | Any output changes for the same inputs, or a schema id is removed or changes meaning | A changed formula; a renamed output id |
| MINOR | A capability is added and every existing output is unchanged | Scenario comparison; an export format |
| PATCH | A fix or presentation change with every output unchanged | Formatting; a label; a validation message |

Gate 1 releases are `v1.x.y`. Any output difference from the original is not a Gate 1 release.

Release procedure:
1. `release/vX.Y.Z` branch: set the version, move CHANGELOG "Unreleased" to the version, rebuild the workbook.
2. Pull request; all checks green; Scott approves; squash merge.
3. Scott tags the merge commit: `git tag -a vX.Y.Z -m "<summary>"` and pushes the tag.
4. GitHub Release for the tag with the workbook, its formula dump, the manifest and the score sheet attached.

The version and the input-set id are written into the workbook (Orientation and file properties) and into every export.

## 7. Fixes to a release

A defect in a released version: `fix/<slug>` from `main`, the same pull request rules, a PATCH release. If a later release has introduced a MAJOR change, the fix branches from the release tag and is released as a PATCH of that line.

## 8. What Claude may and may not do

| May | May not |
|---|---|
| Create `feat/`, `fix/`, `docs/`, `test/`, `build/`, `chore/` and `release/` branches | Push to `main`, merge, approve, tag or delete remote branches |
| Push commits that pass the tests locally | Push with failing tests or skip the pre-push hook |
| Open pull requests (or, if the session cannot, push the branch and give Scott the compare link) | Change `source/`, `canonical/` or a test's acceptance threshold without Scott's approval in the pull request |
| Propose a cleanup | Rewrite published history |

## 9. One-time cleanup (Scott executes; Claude cannot delete branches)

Current remote branches and the proposed disposition:

| Branch | Disposition |
|---|---|
| `main` | Keep |
| `evolution` | Keep, parked |
| `candidate/asis-v1.1`, `docs/foundation`, `feat/model-checks`, `feat/compare` | Merged into `main` (PRs #2–#4); delete |
| `as-is-2026-10-24` | Contained in `main`. Keep it as a tag (a tag of the same name exists in Claude's local copy; confirm it is on GitHub), then delete the branch |
| `candidate/asis-v1.0`, `asis-modern` | Contained in `main`; delete |
| `candidate/model-provenance` | Its MODEL.md is identical to `main`'s; delete |
| `candidate/guardrails`, `candidate/behavior-test` | Governed Claude's behavior, not the model; tag as `archive/guardrails` and `archive/behavior-test`, then delete |
