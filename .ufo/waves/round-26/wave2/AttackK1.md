# AttackK1 — scoped findings report (round-26 wave-2, falsify)

Seat: `k1` / AttackK1 (reviewer). Axes: depth:verifiability.
Milestone: old receipts untouched. Date: 2026-10-25 UTC. Lane only, read-only
(report files under `.ufo/waves/round-26/wave2/` are my only writes).

## Item

"Confirm no round-25 or earlier file changed: `git diff 1b076fa7 --stat` shows
only the round-26 files; specifically `.ufo/waves/round-25/` untouched and
`corpus/lessons/round-25*.md` untouched."

## Verdict: NO DEFECT FOUND — claim holds

The diff against the claims-freeze commit `1b076fa7`
("round-26: freeze claims.json (C1 gate conformance, C2 F11 assimilation) before
any measurement or dispatch") contains exactly the 7 round-26 file changes, zero
round-25/earlier files, zero deletions, zero `.ufo/` paths.

## Checks performed (all observed, not inferred)

1. `git diff 1b076fa7 --stat` → 7 files changed, 180 insertions(+), 6 deletions(-):
   `LOG.md` (10), `PROVINCE.md` (1), `SCORECARD.md` (27), `SKILL.md` (9),
   `corpus/README.md` (5 +-), `corpus/SOURCES.md` (7), `corpus/instruments/recheck-audit.py` (127 +-).
   Matches the claimed stat exactly.
2. `git diff 1b076fa7 --name-only` → same 7 paths; none under `.ufo/`, none under
   `corpus/lessons/`, none outside the round-26 scope.
3. `git diff 1b076fa7 --name-only -- .ufo/waves/round-25/` → empty
   (`.ufo/waves/round-25/` untouched).
4. `git diff 1b076fa7 --name-only -- 'corpus/lessons/round-25*.md'` → empty
   (both round-25 lessons, `round-25.md` and `round-25-verifier-spotcheck.md`,
   untouched; they are tracked, so this is a meaningful byte comparison).
5. `git diff 1b076fa7 --diff-filter=D --name-only` → empty (no file deleted at all).
6. Baseline integrity: `git ls-files .ufo/waves/round-25/` → 3773 tracked files,
   so the untracked-blind-spot caveat does not apply to the milestone objects.
7. Content inspection of each of the 7 diffs: all changes are round-26 additions
   (Round 26 log entry; F11 line; round-26 SCORECARD rows; SKILL gates registry
   row; README F11 row + 10/10→11/11 count bump; SOURCES S041 row + `## Registry
   changes` note; recheck-audit.py landed `--expect` instrument). The 6 deletions
   are removed lines inside these same round-26 files (README count-line rewrite,
   SOURCES recheck-cell prose moved to the Registry-changes note), i.e. not
   old-round content.

## Incidence on the milestone

- Old receipts untouched: yes. Round-25 wave artifacts (3773 tracked files) and
  round-25 lessons unchanged; wave-1 round-26 receipts (`c1-controls/`,
  `c2-controls/`, `c1-receipt-index.txt`, `c1-instrument-digest.txt`,
  `c1-live.json`) show no tree diff either (they are new/untracked files, so the
  git diff is silent on them — but they cannot have been modified by a tracked
  diff and are not part of the "round-25 or earlier" claim).

## Residual risk / verification gaps

- Git diff covers tracked files. Any *new* file (untracked) is out of scope of
  `git diff <commit>`; the milestone question is about prior-round files, which are
  tracked and therefore fully covered. No gap material to the claim.
- This is a tree-state check, not a content-semantics check of the round-26
  changes (other seats own those checks: h1 live audit, i1 kill rules, i2/m1
  mutation probes).

## Tooling

No installs performed; used git and python3 only (pre-existing). No VCS writes;
all checks read-only.
