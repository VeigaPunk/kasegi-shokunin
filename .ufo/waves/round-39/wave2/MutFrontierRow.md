# MutFrontierRow — receipt (kasegi round 39, wave 2, falsify)

Seat: MutFrontierRow (attack seat, leaf; no subagents spawned). Judged axis: coverage — C2 attack
surface. Date: 2026-10-26. Dispatch: L1 KasegiR39, hyaku run 9, wave 2.
Item: mutate the F22 frontier row and the S057 entry's `recheck:` line on a scratch mirror of the
lane at HEAD; run `corpus/instruments/frontier-recheck-count.py` per mutation; record which
mutations make it red.

## What was attacked

- Frozen predicate: claims.json C2 counting command
  `python3 corpus/instruments/frontier-recheck-count.py -> entries=25 pass=25 exit=0`
  (read with E1/E5 erratum semantics; E5.9 content binding for the row).
- Landed bytes, read at lane HEAD 5006097a84305267c9a3e8c1e1d560e60fe41d37 via `git archive` into
  the scratch mirror, live working tree verified byte-identical (sha256 equal on all three):
  - corpus/README.md F22 row (line 506) — f6d97c2975945a32d13b259bbc0862372ac0d7e774dd6099f9ef029819a83ee1
  - corpus/knowledge/cisa-when-to-issue-vex.md `recheck:` line (line 6) — 5010a107cc7ef34bcd7e8d1a74eb2a2bb2a71c3ea666577506d7c2f93dc25d29
  - corpus/source-snapshots/round-39/S057.txt — 11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f
    (equals the digest declared in the entry header and the manifest).

## Method

1. Scratch S=/fast/scratch/hyaku/kasegi-r39/MutFrontierRow (mkdir -p; TMPDIR bound to S/tmp;
   HYAKU_SCRATCH unset for harness runs; /tmp never used).
2. Mirror = `git -C <lane> archive HEAD | tar -x` (read-only git; plain tree, no .git).
3. Driver (scratch/driver.py, removed with the scratch) applied each mutation with a
   uniqueness-asserted string replace, ran the harness with `--root <mirror> --json <out>/<tag>.json`,
   restored the pristine bytes, and verified sha256 equality after every mutation.
4. Mutations: row cell 4 emptied (M1), row sources cell S057→S055 (M2), row status→queued (M3),
   row broken to 7 cells in three shapes (M4a mid-topic pipe / M4b trailing cell / M4c entry-path
   split), recheck cd prefix dropped (M5), recheck manifest → missing path (M6), plus M5b
   (cd dropped + corrupted capture) and controls C-ESC / C-DIGEST / live-lane / C0 / C9.

## Results

Full detail with actual outputs: .ufo/waves/round-39/wave2/MutFrontierRow.mutations.txt

- Killed (harness red): M4c (`FAIL F22 knowledge/cisa-when-to-issue-vex ids=- exit=- problems=missing-entry`,
  entries=25 pass=24 exit=1), M6 (`problems=manifest-unreadable`, fail-closed before execution,
  exit=1), M5b (`problems=recheck-exit-1`, exit=1).
- Survived (harness green): M1 (entry path emptied; entries 25→24), M2 (sources cell S057→S055;
  count unchanged 25/25 — uninstrumented), M3 (status queued; 25→24), M4a (7 cells, cells shift;
  25→24), M4b (7 cells, trailing; 25/25 — fully invisible), C-ESC (corrupted mirror capture with
  the cd prefix intact → PASS 25/25).

## Findings

- F-A: the Frontier row's `sources` cell is parsed by no committed instrument — the harness regex
  stops at cell 4 and no other instrument reads the table (grepped corpus/instruments and scripts).
  M2 is a full survivor against every frozen C2 counter; the only pin is the E5.9 prose sentence.
- F-B: row width is never validated and a regex-non-matching admitted row is silently dropped
  (M1/M3/M4a survive with exit 0; M1/M3 also keep the frozen frontier grep count at 22).
- F-C: rule D's "executed, from the lane root" is defeated by the recheck line's own absolute
  `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix — the exit-code limb binds to the
  hardcoded lane root, not --root (C-ESC PASS on a corrupted mirror vs M5b RED with the cd dropped;
  C-DIGEST shows the corruption is detectable under root-bound execution). At the live lane the cd
  target equals root, so the frozen counting command is unaffected; the root-bound (cd-less) form
  also passes (M5).
- F-D: the fail-closed limbs that do bind work as documented (missing-entry, manifest-unreadable,
  recheck-exit-1 — all red with named-row problems); pristine baseline and post-restoration runs
  both print the frozen `entries=25 pass=25 exit=0`.

Claim impact: C2's harness limb is real but narrower than its receipt line — row-level binding
(sources cell, row shape, row presence) is enforced only by the frozen entries=25 count (M1/M3/M4a
drift it) and the E5.9 prose predicate (M2); M4b flips nothing at all; the executed recheck is bound
to a hardcoded path rather than to the harness root. No mutation made a frozen counter report a
false green count — survivors survive by leaving the counters untouched.

## Controls run (do-nothing)

- Live-lane frozen command exactly as written (no --root): `entries=25 pass=25 exit=0`, exit 0.
- Pristine mirror baseline (C0) and post-restoration re-run (C9): both `entries=25 pass=25 exit=0`.
- C-DIGEST: corrupted capture under root-bound execution →
  `S057:sha256 MISMATCH expected=11c8d6d6… actual=b8f1bdb3…`, exit 1.

## Tooling

No tools installed or upgraded (operator tooling authorization 2026-10-19 acknowledged; nothing
needed beyond the lane's own python3 instruments; pacman untouched; no service touched).

## Write scope / cleanup

Writes: this receipt, MutFrontierRow.mutations.txt (beside it), and scratch
/fast/scratch/hyaku/kasegi-r39/MutFrontierRow (removed before yield, after the deliverables were
landed). Lane tree, fleet root, shokuknow, sibling repos: read-only. No mutating git/jj command
anywhere (git archive and rev-parse only). Restoration verified by sha256 equality for every
mutated mirror file (ledger in the deliverable).

Report: .ufo/waves/round-39/wave2/MutFrontierRow.md
