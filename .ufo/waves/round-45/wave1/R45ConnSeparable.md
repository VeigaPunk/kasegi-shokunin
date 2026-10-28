VERDICT: HOLDS

# R45ConnSeparable — are C1 and C2 causally separable?

Seat: R45ConnSeparable (connector, leaf). Lane: kasegi round 45. Frozen claims sha256 bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206 (freeze 8cf62c8, base dc5bb8c).

Answer in one line: yes for the stated criterion (each claim reaches its `expect_after` with the other claim absent, and both reach it together with no interference), with four documented couplings. The strong reading ("C2 is unaffected by C1's content") does NOT hold: C2 gate G7 validates the whole shared `corpus/SOURCES.md`, so a malformed C1 row fails C2.

## Method

No lane file was edited. Everything was built in scratch and removed on exit.

- Base: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd | tar -x -C $S/base`
- Freeze: the same, with `8cf62c879e6e6b031e67412f8fac1fba0bd378cf` (adds claims, counters, controls, S071/S072 captures, manifest).
- Recipes (`build.py`, scratch-only) applied to copies of the freeze tree:
  - C2 = F27: new `corpus/knowledge/linux-kernel-security-bugs-process.md` (source header, 5 curly quotes each cited `` (`S071.txt:N-M`) ``); README row `| F27 | ... | admitted | knowledge/linux-kernel-security-bugs-process.md | S071 | ... |` inserted after `| F26 |`; SOURCES row S071 (tier A, mined, 2026-10-28, on-release, used-by the entry, anchor sha 0918dcfa...) inserted after `| S070 |`.
  - C1 = R1..R5:
    - R1: SOURCES row S072 (tier B, rejected, teaches `supersedes S070 — ... 10029-character body ... flip: ...`, anchor sha 364166c4..., recheck 180d, used-by —) after `| S070 |`; appended `Correction (round 45, appended 2026-10-28): ... S072 ... 10029 characters ...` to round-44.md.
    - R2: append `## Round-45 additions` with R47/R48/R49 rows (3 cells each; needles "do-nothing"/"before data", "presence-only", "capture method"/"reject"; enforced-by paths that exist: freeze-check.py, r45-c2-gate.py, source-recheck.py).
    - R3: `r44-frontier-count.py` gains `--selftest` (10 cases, `selftest cases=10 failures=0`), `--root` no longer required only in that mode; SKILL.md appended section with three 8-cell rows; `corpus/instruments/README.md` row `| \`r44-frontier-count.py\` | ...`.
    - R4: new `corpus/instruments/freeze-check.py` (`--selftest` 8 cases; `--claims ... --tool-root ... --base ...` replays each `counter_cmd` on base and compares the last line with `expect_before`).
    - R5: copy of the lane working-tree receipt `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` (untracked in the lane).
- Trees: `frozen` (freeze only), `C2only`, `C1only`, `both`, `C1bad` (S072 row with an extra cell, 12 cells), `bothbad` (C1bad + C2).
- Counters run, each as `python3 $LANE/corpus/instruments/<counter>.py --root $S/trees/<t> [--baseline $S/base]`, where `LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Findings

### F1 — do-nothing control (base export), matches the frozen `before`

Command: `python3 .../r45-routed-defects.py --root $S/base --baseline $S/base` and `python3 .../r45-c2-gate.py --root $S/base`

Output:
- `routed-defects total=5 fixed=0 unresolved=5 exit=1`
- `c2-gate fixed=1/7 exit=1` (only G7 passes: `gate G7 pass=1 read=census-rc=0`)

This equals the claims' `expect_before` for both claims.

### F2 — the freeze commit alone already moves C2 off its `before` value

Command: counters on `trees/frozen`.

Output:
- C1: `routed-defects total=5 fixed=0 unresolved=5 exit=1`
- C2: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`, `gate G7 pass=1 read=census-rc=0`, `c2-gate fixed=2/7 exit=1`

G4 passes from the frozen capture and manifest, and G7 passes because the SOURCES file is unchanged. So the C2 `before` string `c2-gate fixed=1/7` is true at base only, not at the freeze commit. The frozen replay (`freeze-check`) only replays at base, so it does not catch this.

### F3 — C2 is verifiable with C1 absent (C2only tree)

Output:
- C2: `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-process.md`; `gate G3 pass=1 read=row-S071=ok`; `gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4`; `gate G6 pass=1 read=knowledge=64`; `gate G7 pass=1 read=census-rc=0`; `c2-gate fixed=7/7 exit=0`
- C1: `routed-defects total=5 fixed=0 unresolved=5 exit=1` (R1 `row-S072=absent`, R4 `freeze-check-absent`, R5 `refiled-absent`)

### F4 — C1 is verifiable with C2 absent (C1only tree)

Output:
- C1: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`; `limb R2 fixed=1 read=criteria=3`; `limb R3 fixed=1 read=selftest-cases=10`; `limb R4 fixed=1 read=selftest-cases=8 replay=base_ok=2`; `limb R5 fixed=1 read=refiled=ok original=unchanged`; `routed-defects total=5 fixed=5 unresolved=0 exit=0`
- C2: `c2-gate fixed=2/7 exit=1` (G4, G7 pass without C2 landing; same as F2)

### F5 — both landed: no interference

Output:
- C1: `routed-defects total=5 fixed=5 unresolved=0 exit=0`
- C2: `gate G7 pass=1 read=census-rc=0`; `c2-gate fixed=7/7 exit=0`
- SOURCES rows in order: `| S070 |` line 76, `| S071 |` line 77, `| S072 |` line 78.

### F6 — one-way coupling, C2 ← C1 content (malformed C1 row)

Command: counters on `trees/C1bad` (S072 row with 12 cells) and `trees/bothbad`.

Output:
- C1bad: `limb R1 fixed=0 read=row-S072=absent`; `routed-defects total=5 fixed=4 unresolved=1 exit=1`
- C1bad, C2: `gate G7 pass=0 read=census-rc=1`; `c2-gate fixed=1/7 exit=1`
- bothbad: C1 `fixed=4 unresolved=1`; C2 `gate G7 pass=0 read=census-rc=1`; `c2-gate fixed=6/7 exit=1`

C2 G7 runs the census `validate --file` over the whole SOURCES file, so a broken C1 row fails C2 even with no C2 landing. The reverse does not happen: C1 never reads C2's rows. C2's gate is therefore not independent of C1's content.

### F7 — merge-level coupling: both claims insert at the same SOURCES anchor

Fixture: `D=$(mktemp -d -p $S)`, `git -C "$D" init -q`, rev-parse printed `$D`; base SOURCES committed on `main`; branch `c1` = C1only SOURCES; branch `c2` = C2only SOURCES; both commits made in the fixture.

Command: `git -C "$D" merge --no-edit c2` after merging c1 into main.

Output:
- `Auto-merging corpus/SOURCES.md`
- `CONFLICT (content): Merge conflict in corpus/SOURCES.md`
- `Automatic merge failed; fix conflicts and then commit the result.`
- conflict markers at lines 77/79/81 of the merged file.

Semantically the rows are independent, but textually they collide at the S070 line because S070 is the last registry row (line 76). This is a git-level coupling, not a counter one.

### F8 — C1 R4 depends on the C2 counter file (intrinsic)

The freeze-check replay runs every claim's counter, including C2's `r45-c2-gate.py`, on base. Removing that file from the C1only tree (sabotage A):

Output:
- `limb R2 fixed=0 read=R48-enforced-by-missing-corpus/instruments/r45-c2-gate.py`
- `limb R4 fixed=0 read=replay-rc=1`
- `routed-defects total=5 fixed=3 unresolved=2 exit=1`

R2 fails only because my recipe pointed R48's `enforced-by` at the C2 counter. Repointing it at `corpus/instruments/r45-routed-defects.py` (C1-owned) clears R2, giving `routed-defects total=5 fixed=4 unresolved=1 exit=1` with `limb R4 fixed=0 read=replay-rc=1`. So R2's coupling is avoidable recipe-level, and R4's coupling is structural: any executor must keep `r45-c2-gate.py` present and its base output unchanged, or C1 R4 breaks.

### F9 — C1 R5 depends on an untracked receipt

`.ufo/waves/round-44/controls/final-attempt3-refiled.txt` is `??` in `git status` of the lane (not committed). Removing it from the C1only copy (sabotage B):

Output: `limb R5 fixed=0 read=refiled-absent`; `routed-defects total=5 fixed=4 unresolved=1 exit=1`.

So C1 can only reach `fixed=5` on a working tree that includes this file. A commit archive of the lane HEAD does not carry it. The receipt's content (`selftest cases=20 failures=0`) is also text-checked only; the counter does not re-run the cited selftest.

### F10 — C2 G7 depends on a fleet-root script outside the lane

`CENSUS` defaults to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. Setting `SOURCES_CENSUS=/nonexistent/sources-census.sh` on the both tree:

Output: `gate G7 pass=0 read=census-rc=127`; `c2-gate fixed=6/7 exit=1`.

The C1 counter declares `CENSUS` (line 55) but never uses it, so that line is dead.

### F11 — the shared instrument r44-frontier-count.py (C2 secondary)

Command: `python3 .../r44-frontier-count.py --root $T --expect 27` over each tree.

Output:
- base, frozen, C1only: `frontier rows=26 admitted=26` then `frontier expected=27 admitted=26 verdict=SHORT exit=1`
- C2only, both, bothbad: `frontier rows=27 admitted=27` (rc 0)

This C2 secondary is not in the C2 counter. It is claim-level text in claims.json, but C1 R3 edits the same file. The edit left the count unchanged (rows counted identically in all trees), and the new selftest is `r44-frontier-count.py --selftest` → `selftest cases=10 failures=0` (rc 0).

### F12 — claims.json is shared and hash-frozen

C1 R4 replays both claims from claims.json, so C2 must not edit it. The file's sha256 matches the freeze record (`bbe40503...`, confirmed with `sha256sum` and `grep claims-sha256`).

### F13 — frozen controls reproduce

Command: `python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export $S/base --lane $LANE --work $S/controls`

Output: five control lines identical to `controls/freeze-controls.txt`, ending `controls total=5 red=5 green=0`, rc 0.

Neither control set includes a one-claim-landed tree, so none of them tests the couplings above.

### F14 — the C1 R1 size token is derivable, not just asserted

`S072.txt` is 10032 bytes (one U+2019 is three bytes), 10030 characters with a final newline. Counted without the final newline, `len = 10029`, which is the token R1 checks by regex. This is a derivable measurement; the counter itself does not compute it.

### F15 — frozen replays and selftests pass on the both tree

Output:
- `selftest cases=10 failures=0` (r44-frontier-count.py), rc 0
- `selftest cases=8 failures=0` (freeze-check.py), rc 0
- `freeze-check claim=C1 base_ok=1 ... expect='routed-defects total=5 fixed=0 unresolved=5 exit=1'`
- `freeze-check claim=C2 base_ok=1 ... expect='c2-gate fixed=1/7 exit=1'`
- `freeze-check claims=2 base_ok=2`, rc 0

## Separability matrix

| Question | Result | Evidence |
|---|---|---|
| C1 verifiable with C2 absent | yes, 5/5 | F4 |
| C2 verifiable with C1 absent | yes, 7/7 | F3 |
| Both landed, no interference | yes, 5/5 and 7/7 | F5 |
| C2 gate independent of C1 content | no (G7 over whole SOURCES) | F6, F10 |
| Textual merge independence | no (same S070 anchor) | F7 |
| C1 R4 independent of C2 counter file | no (intrinsic replay) | F8 |
| C1 R5 independent of working-tree state | no (untracked receipt) | F9 |
| C2 `before` at freeze commit | 2/7, not 1/7 (base only) | F2 |

## Shared-surface map (C1 / C2 / both)

- `corpus/SOURCES.md`: C1 adds S072 (R1); C2 adds S071 (G3) and gates the whole file (G7). Both insert after `| S070 |`.
- `corpus/source-snapshots/round-45/manifest.json`: S072 entry (C1 R1) and S071 entry (C2 G4), each read through `source-recheck.py --source` (distinct entries, prepaid by the freeze commit).
- `corpus/source-snapshots/round-45/S071.txt`: C2 only. `S072.txt`: C1 only.
- `corpus/lessons/round-44.md`: C1 R1 appends the correction; C1 R2 grounds cite it. C2: none.
- `corpus/QUALITY.md`, `SKILL.md`, `corpus/instruments/README.md`: C1 only.
- `corpus/README.md` (frontier table): C2 only (G1, F27 row). Not the same file as `corpus/instruments/README.md`. Root `README.md` is not touched by either.
- `corpus/knowledge/`: C2 only (G6 counts 64).
- `corpus/instruments/r44-frontier-count.py`: C1 R3 edits it; C2's secondary check (claims.json) uses it.
- `corpus/instruments/r45-c2-gate.py`: C2 counter; C1 R4 replays it (F8).
- `corpus/instruments/freeze-check.py`: new, C1 only.
- `.ufo/waves/round-45/claims.json`: shared, hash-frozen, read by C1 R4.
- `scripts/sources-census.sh` (fleet root): C2 G7 only (F10).
- `corpus/lessons/round-45.md`: named in claims.json `frontier_step`; the file does not exist, and no counter reads it.
- `AXES.md`: not present in the lane tree; the axis strings are in claims.json.

## Limitations

- The recipes are my minimal reconstruction in scratch, not the lane's drafts. Nothing was judged for content quality: the F27 prose, teaches wording, R2 criterion grounding, and freeze-check design are not evaluated beyond the counters.
- The counters are textual. R1 checks the token `10029` by regex only (F14 is my check, not theirs). R5 checks receipt text, not a re-run. R2 checks needles and path existence, not that criteria are grounded.
- Only the orders present in the built trees were tested. The trees are sets of applied recipes, not a sequence of commits, except for the F7 merge fixture.
- G7 runs the fleet-root census with the system date (no `--today`). Nothing was re-run on the lane HEAD working tree beyond the reads above.
- I did not test a control that lands only one claim's artifacts in a tree containing the other's counter changes; the frozen controls do not cover this (F13).
- The lane's `corpus/lessons/round-45.md` obligation is outside every counter, so its presence is unverified.

## Host and install record

- No tools installed or upgraded. No pacman, no git or jj mutation in the lane. The only fixture git calls were `init`, `add`, `commit`, `checkout`, `merge` in the scratch fixture (F7).
- Lane writes: this Report only. Scratch removed on exit.
