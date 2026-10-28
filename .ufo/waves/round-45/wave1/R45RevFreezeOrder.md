VERDICT: BROKEN

Scope: freeze record `.ufo/waves/round-45/freeze.txt` and `claims.json` against QUALITY.md R44 (`corpus/QUALITY.md:370`), freeze commit `8cf62c879e6e6b031e67412f8fac1fba0bd378cf`. Read-only; no commit, no git mutation. Literal R44 sub-conditions 1-4 hold; the R44 corroboration principle fails for the `measured-at` value (2c). Separately, the freeze commit carries C2 wave-1 evidence, so the frozen "before" reading is stale.

## 1. Freeze-record sub-conditions (R44)

Command: `sed -n 's/^frozen-at: //p' .ufo/waves/round-45/freeze.txt`
Printed: `2026-10-28T20:55:34Z`   (freeze.txt:1)

Command: `grep -n 'measured-at' .ufo/waves/round-45/freeze.txt`
Printed: `4:controls: .ufo/waves/round-45/controls/freeze-controls.txt measured-at: 2026-10-28T20:55:13Z`

Commit stamps: `git show -s --format='committer-utc=...'` on 8cf62c8 printed
`committer-utc=2026-10-28T20:55:40Z` and `author-utc=2026-10-28T20:47:59Z`
(epochs 1793220940 / 1793220479). Reflog corroborates the committer stamp:
`8cf62c8 HEAD@{2026-10-28 17:55:40 -0300}: export from jj`.

| R44 sub-condition | Printed values | Result |
|---|---|---|
| 1. `frozen-at` is an ISO-8601 `Z` instant | `2026-10-28T20:55:34Z` | PASS |
| 2. `frozen-at` >= latest cited `measured-at` | `20:55:34Z` vs `20:55:13Z`, margin 21 s | PASS (arithmetic) |
| 2c. cited control artifact carries the `measured-at` | see below | FAIL |
| 3. `frozen-at` <= containing commit (committer stamp `20:55:40Z`) | margin 6 s | PASS |
| 3-alt. same check with author stamp `20:47:59Z` | margin -455 s | FAIL (author stamp is not the commit time; the R44 precedent uses the committer stamp) |
| 4. `claims-sha256` = claims bytes | freeze `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`; `sha256sum` of committed and worktree claims.json both `bbe40503...c6206` | PASS (`cmp` identical) |
| base field | freeze.txt:3 `base: dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`; claims.json `"base"` same; equals parent of 8cf62c8 | PASS |

### 2c (FAIL): `measured-at` is a label, not carried by its cited control
- `grep -rn 'measured-at' .ufo/waves/round-45/controls corpus/instruments/r45-routed-defects.py corpus/instruments/r45-c2-gate.py .ufo/waves/round-45/claims.json .ufo/waves/round-45/freeze.txt` printed only `.ufo/waves/round-45/freeze.txt:4`.
- `cat -n .ufo/waves/round-45/controls/freeze-controls.txt` is six lines (five `control ...` rows plus `controls total=5 red=5 green=0`); none is a `measured-at` line.
- The round-43 precedent carries it in the receipt: `.ufo/waves/round-43/c1-controls/do-nothing.txt:2:measured-at=2026-10-28T16:32:23Z`, and the round-43 K19 spec requires "exactly one `measured-at=<ISO Z>` line" per control receipt (`.ufo/waves/round-43/build-w1-spec.py:62`).
- The only corroboration is local fs mtime: `stat -c '%n %y' .ufo/waves/round-45/controls/freeze-controls.txt` printed `2026-10-28 17:55:13.878386208 -0300` (= 20:55:13.878Z). That is a worktree mtime, not a committed artifact.

### Do-nothing discrimination and mutants (scratch checker, not committed)
I wrote a sub-check script in scratch (`r44_check.py`, sub-conditions 1-4 and 2c). Results:
- Freeze tree, committer epoch: `VERDICT-R44 fails=['2c']`, rc=1 (R44.1/2/3/4 PASS).
- Freeze tree, author epoch: `R44.3 ... FAIL margin=-455s`, `fails=['2c', '3']`.
- Do-nothing (base export, no freeze.txt): `R44 freeze-record=absent -> FAIL`, rc=1.
- Mutant m-early (`frozen-at: 2026-10-28T20:55:12Z`): `R44.2 ... -> FAIL`, `fails=['2','2c']`.
- Mutant m-late (`frozen-at: 2026-10-28T20:56:00Z`): `R44.3 ... FAIL margin=-20s`.
- Mutant m-offset (`2026-10-28T17:55:34-03:00`): `R44.1 ... FAIL`.
- Mutant m-sha (one hex digit changed): `R44.4 ... -> FAIL`.
- Mutant m-nomeas (no measured-at in freeze.txt): `R44.2 ... vs None -> FAIL`.
- Mutant m-ctl-line (scratch copy of controls with `measured-at=2026-10-28T20:55:13Z` prepended): `R44.2c ... -> PASS`, `fails=none`.
So the checker discriminates every sub-condition, and 2c is the only one the real tree fails.

### Machine grading gap
`corpus/instruments/r43-closure.sh` hard-wires `RECEIPT_REL=".ufo/waves/round-43/..."` and K19 reads `frozen-at=`. The round-45 freeze.txt uses `frozen-at:` and an inline `controls:` line, so no committed instrument grades the round-45 freeze record. The R44 result above is a manual check.

## 2. Freeze commit contents vs "no seat has run at freeze"
- No `wave1`, draft, or report path is in the freeze commit: `git show --name-only --format= 8cf62c8 | grep -i 'wave1\|draft\|report'` returned nothing (rc=1).
- C2 wave-deliverable evidence IS committed before wave 1: `corpus/source-snapshots/round-45/S071.txt`, `S072.txt`, `manifest.json` (S071 with five manifest quotes Q1-Q5), `.ufo/waves/round-45/source-recon/S071.headers.txt`, `S072.json`. The claims' after-state lists "one new tier-A mined row S071 with a sha-pinned snapshot and five located manifest quotes" as wave output.
- Effect on the counter. Export of 8cf62c8 (`/fast/scratch/hyaku/kasegi-r45/R45RevFreezeOrder/freeze`), run `python3 corpus/instruments/r45-c2-gate.py --root <freeze export>`:
  - `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
  - `c2-gate fixed=2/7 exit=1`
  - Same counter on base: `gate G4 pass=0 read=manifest-absent` and `c2-gate fixed=1/7 exit=1`.
  - The claims' `expect_before` is `c2-gate fixed=1/7`. The tree that wave 1 starts from reads 2/7, so G4 is credited to L1-authored pre-freeze evidence, not to wave work.
- G7 (`census-rc=0`) passes on base, so the do-nothing C2 reading is already 1/7 from a non-discriminating limb.
- C1 at freeze tree: `limb R1 ... read=row-S072=absent` ... `routed-defects total=5 fixed=0 unresolved=5 exit=1`. Consistent with expect_before.
- Quote location (`grep -n` on S071.txt): lines 39, 42, 310-311 contain the manifest quotes; Q1 anchor 310 and Q4 anchor 41 match. S071.txt is 20152 bytes and S072.txt 10032 bytes, both equal to manifest `bytes`; `sha256sum` matches manifest `sha256` for both (`0918dcfa...346f40`, `364166c4...a025`).

## 3. Controls reproduction (falsification of the freeze controls)
Command: `python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export <base dc5bb8c export> --lane <freeze 8cf62c8 export> --work <scratch>/controls`
Printed (exit 0), then `diff` against committed `freeze-controls.txt`:
```
control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED
control c1-marker-only counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control c2-junk-row counter=C2 c2-gate fixed=4/7 exit=1 expect=RED got=RED
control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 expect=RED got=RED
controls total=5 red=5 green=0
```
`diff` printed nothing and the test printed `CONTROLS-IDENTICAL`. All five controls are RED. Tool mtimes precede the control run: `r45-routed-defects.py` 20:54:15Z, `r45-c2-gate.py` 20:54:39Z, `freeze-controls.py` 20:55:08Z, controls 20:55:13Z, claims and freeze.txt 20:55:34Z, commit 20:55:40Z.

## 4. Post-freeze drift
- `git diff --stat 8cf62c8 HEAD -- corpus/instruments/r45-routed-defects.py corpus/instruments/r45-c2-gate.py .ufo/waves/round-45/claims.json .ufo/waves/round-45/freeze.txt .ufo/waves/round-45/controls corpus/source-snapshots/round-45 .ufo/waves/round-45/source-recon` printed nothing (rc=0). No frozen file changed.
- `git log --oneline 8cf62c8..HEAD -- .ufo/waves/round-45 corpus` printed only `5242db6 round-45: wave 1 spec (64 seats, policy v2) and dispatch` (17:59:05 -0300). That commit adds only `build-wave1-spec.py`, `wave1-dispatch.json`, `wave1-spec.json`, `wave1-dispatch.stderr.txt`.
- Wave 1 is already dispatched at HEAD. Any fix to the findings above is an errata or a logged counter note, not a re-freeze, under the kill-rule convention in claims.json C1.

## 5. Findings to route
1. (2c, medium) The cited controls file has no `measured-at` line. Its timestamp rests on the freeze record's own label plus a local mtime. Route: L1 errata recording the control-time evidence, or a re-measure and a new freeze before any seat scores.
2. (C2 pre-credit, medium) `c2-gate` reads 2/7 at the frozen tree, not the stated 1/7. G4 is pre-satisfied by L1-authored snapshot/manifest committed in the freeze. Route: record the 2/7 freeze-tree reading in the round lesson so the wave delta is not overstated; do not credit G4 to wave 1.
3. (instrument, low) G7 `census-rc=0` passes on base; one of seven C2 limbs does not discriminate.
4. (grading gap, low) No committed instrument checks the round-45 freeze record; K19 is hard-wired to round 43 and reads `frozen-at=`.

Not findings: the freeze commit contains no wave-1 draft or report; the claims.json and freeze.txt bytes match the committed bytes; C1 reads 0/5 at freeze and base; the author-stamp difference is consistent with jj preserving change author time [INFERENCE from the jj reflog; not verified against jj metadata].

## Limitations
- Mtime corroboration is the local worktree clock; it is not a committed or signed record.
- I did not fetch docs.kernel.org live. S071 is verified against its own manifest sha and quote locations only, not against the live page.
- The R44 check is a scratch script; it is not committed and not a replacement for a round-45 instrument.
- Counters and controls were run only on the base export (dc5bb8c) and the freeze export (8cf62c8), both via `git archive`. I did not run F27 or the C1 repairs (out of this seat's scope).
- Checked the committed bytes of the freeze commit and HEAD using read-only git; did not inspect the untracked wave-1 files in the worktree.

## Scratch
Scratch root `/fast/scratch/hyaku/kasegi-r45/R45RevFreezeOrder/` (base, freeze, work, mut, tmp), removed on exit.
