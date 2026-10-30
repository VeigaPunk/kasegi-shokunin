# Round-3 lessons

Round: 3 (2026-09-28). Evidence: `LOG.md` round-3 entry, commit `round-3`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-3/kasegi.md`.

## What I closed

- **Gate-list gap → `corpus/knowledge/claim-gates.md`.** Read `ops/claim-check.mjs`
  in full (233 lines) plus `claim-index.mjs` and `prepare-claims.mjs`. Facts
  worth keeping: the duplicate-submission guard is GLOBAL (scans all
  `claims/*/*/status.json` for same slug or same ≥16-char title with a prior
  submission record); `claim_review.reviewer.role` must be the literal string
  `kx-reviewer`; `prepare-claims.mjs` restores original payload bytes if the
  post-write recheck fails — manifest-bound payloads are immutable without
  re-review.
- **`vdp-disclosures/` walked → `corpus/knowledge/vdp-disclosure-packages.md`.** It is
  a distinct four-file package shape (ROUTE/cover-note/report/SUBMITTED), not
  the six-file claim contract; free + fully attributed per operator decree;
  sent via the vendor's security.txt Contact route (H1 embedded_submissions).
- **Cantina fee-gate generalization tested.** Sampled 5 sibling ingestions:
  only dydx repeats `positive-blocked-live-precondition`; morpho/euler/
  uniswap/reserve are honest-zero parks. $100 fee is Pendle-specific so far —
  recorded as such rather than generalized.

## Friction

- Hashline `PUT >N` inserts inside a table mid-edit broke the triage table
  once — fix by inserting section-level blocks at section boundaries, or
  re-reading after each structural edit before the next PUT.

## Open gaps (carried)

- `vgn-bounty-lab/` still unwalked.
- `fleets/registry.json` lane→model routing — possibly cross-domain.
- `evidence/` dir conventions vs `claims/*/evidence/` (per-program vs
  per-package) unexamined.
