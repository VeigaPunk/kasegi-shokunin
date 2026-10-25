# Terminal classes — how missions end

Source: `[lost-tree] docs/continuation-notes.md` (486-mission freeze
partition), `docs/review-verdicts.jsonl` (verdict counts), `docs/wrap-report.md`
(claim-review gate outcomes). Read 2026-09-28.

## Non-claim-ready partition (495 statuses − 9 claim-ready mission IDs)

| Class | Count | Rule |
|---|---:|---|
| LEARNED honest-zero | 438 | Bounded park/evidence-only completion; includes completed results behind duplicate in-flight statuses |
| FAILED-infra | 26 | 21 `mission_failed` + 5 `SCOPING` with no terminal packet |
| RETIRED auth-walled | 19 | `mission_retired` terminal; reopen needs authenticated scope read or newly public policy |
| RETRY-method | 3 | Non-claim-ready members of the RETRY_METHOD reset cohort |

Precedence: RETRY-method → latest RETIRED → FAILED-infra → LEARNED (disjoint,
exhaustive). Note: dispatcher maps evidence-only DONE-without-deliverable to
`mission_failed` — infra class ≠ work quality.

## Review verdicts (486 items)

`leave` 430 · `continue` 50 · `drop` 6 — from `fleets/review-mission.md`:
drop = dead end, continue = name the one executable next step, leave = don't
touch again. Default is leave; ~88% of the back-catalog is closed.

## Claim-ready review outcomes (7 canonical packages, wrap-report.md)

0 GO · 5 GO-WITH-FIX-NEEDED · 2 NO-GO. Every blocker was a disclosure defect,
not a code defect: portal severity strings, severity hedging/inflation,
provenance-contradicted absolutes, internal artifacts in attachments, stale
`claim-ready/*` tags. NO-GO cases: unproven live precondition (3CX uid=0 VM
capture; WordPress pinned-checkout rerun).

## Anti-overclaim invariants (I8 + custodian)

- Honest-zero is a first-class deliverable — 438/486 non-claim-ready missions
  terminate there; manufacturing a finding is the cardinal violation.
- `coverage.missing` semantics: empty `in_scope_assets` = "not observed in this
  response", not "no scope exists".
- "Best among observed" — never claim exhaustive testing
  (`fleets/mission-template.md` NEVER list).
- `claim-ready/*` git tags are provenance markers only; never authority over
  current bytes (`docs/claim-ready-index.md` excluded-tags table).

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/docs/continuation-notes.md, docs/review-verdicts.jsonl, and docs/wrap-report.md; round-1 freeze partition.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true
