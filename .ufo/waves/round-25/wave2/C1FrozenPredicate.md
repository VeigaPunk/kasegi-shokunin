# C1FrozenPredicate — wave-2 falsification of the C1 before / frozen-after / final-after counters

Seat: `L1Kasegi25.C1FrozenPredicate` (reviewer, wave 2, round 25). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`
(`git rev-parse HEAD` — HEAD still equals base; all round-25 work is uncommitted worktree state).
Scope: claim C1 only (`claims.json` id `C1`). Read-only; no VCS mutation, no production edits,
no spawns. Tool install/update record: none — `python3`, `git`, `bash`, `diff`, `cp` already
present; pacman untouched.

## Verdict

**SUSTAINED — all three receipts reproduce exactly.** Instrument digest, counts, exits,
per-entry limbs, per-entry exit codes, and all per-entry output digests are identical to the
frozen receipts. No actionable defect in the C1 measurement. Two reporting-grade notes (F1, F2)
below; neither moves a number.

| Surface | Wave-1 receipt | Independent re-run | Match |
|---|---|---|---|
| before (base bytes) | `lines=35 pass=6 strict=6/35 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` | identical | yes |
| frozen-after-35 | `lines=35 total=35 pass=35 strict=35/35 fail-closed=23 gated=23 exit=0` | identical | yes |
| final-after-37 | `lines=37 total=37 pass=37 strict=37/37 fail-closed=23 gated=23 exit=0` | identical | yes |

The claim's `do_nothing_control` ("same counter on the unchanged committed bytes -> pass=6
exit=1; a control that meets the target voids the claim") holds: unchanged bytes score 6, not 35.
The `kill_rule` fails closed limbs are retained as `gated` (23 lines still exit non-zero on the
absent `~/Projects/bounties` base), not deleted.

## Instrument digest

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/recheck-audit.py
c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  corpus/instruments/recheck-audit.py
$ python3 corpus/instruments/recheck-audit.py --selftest ; echo exit=$?
selftest cases=14 failures=0 exit=0
exit=0
```

Matches `c1-instrument-digest.txt:1` and the `instrument_sha256` field inside
`c1-before-strict.json`, `c1-after-35.json`, `c1-after.json` — one instrument, three surfaces,
as the index claims (`c1-receipt-index.txt:3`).

## Commands, outputs, exits (verbatim)

### 1. before — independent base bytes, not the wave-1 snapshot

```
$ git -C <lane> archive b49948f1164ef65106b2c4cbee3f53e8a44b8c41 | tar -x -C /tmp/w2-c1base
$ diff -r /tmp/w2-c1base/corpus/knowledge <lane>/.ufo/waves/round-25/c1-controls/base/corpus/knowledge
(no output — KNOWLEDGE_IDENTICAL)
$ diff -r /tmp/w2-c1base/corpus/instruments <lane>/.ufo/waves/round-25/c1-controls/base/corpus/instruments
Only in .../c1-controls/base/corpus/instruments: recheck-audit.py   # wave-1 staged the instrument there; irrelevant to measured bytes
$ python3 corpus/instruments/recheck-audit.py --root /tmp/w2-c1base \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/w2-c1base.json --quiet
strict pass=6/35 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=12 gated=0 broken=23  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1
exit status: 1
```

Matches `c1-before-strict.json` (root differs: theirs was the `c1-controls/base` copy, mine the
`git archive` export — corpus contents proven byte-identical first). Per-entry diff of my JSON vs
receipt JSON: **0 field differences, 0 digest differences** across `pass`, `pass_strict`,
`class`, `limbs`, `strict`, `lane_exit`, `foreign_exit`, `command`, `cd_target`,
`lane_output_sha256`, `foreign_output_sha256` on all 35 entries. The earlier `c1-before.json`
(frozen-limb receipt, lane-root run) also reconciles: same `pass=6`, `fail_closed=23`,
`parse=23, cwd=6, paths=0` (`c1-before.txt` tail confirms `exit=1`).

### 2. frozen-after-35 — two runs, receipt snapshot and independent copy

```
$ python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-after-35 \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/w2-c1-after35-snap.json --quiet
lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0   (strict pass=35/35)
exit status: 0

# independent surface: live corpus minus the two C2 entries
$ cp -a corpus /tmp/w2-after35-check/ && rm /tmp/w2-after35-check/corpus/knowledge/vendor-disclosure-*.md
$ diff -r <lane>/.ufo/waves/round-25/c1-after-35/corpus/knowledge /tmp/w2-after35-check/corpus/knowledge
(no output — the 35 measured files are byte-identical; see F1 for the unmeasured diffs)
$ python3 corpus/instruments/recheck-audit.py --root /tmp/w2-after35-check \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/w2-after35-indep.json --quiet
lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0   (strict pass=35/35)
exit status: 0
```

Both runs agree with `c1-after-35.json` on every entry field and both output digests (0 diffs).
The 35/35 is therefore a property of the 35 entry files, not of anything else in the snapshot
tree.

### 3. final-after-37 — live lane

```
$ cd <lane> && python3 corpus/instruments/recheck-audit.py --json /tmp/w2-c1-after37.json --quiet
strict pass=37/37 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=14 gated=23 broken=0
lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
exit status: 0
```

0 per-entry field differences and 0 digest differences vs `c1-after.json` on all 37 entries.
`ls corpus/knowledge/*.md | wc -l` = 37; the two added files are
`vendor-disclosure-policies-as-corpus-objects.md` and
`vendor-disclosure-policy-commitments-crosswalk.md` (both `??` untracked), each carrying a
conforming `recheck:` line.

## Attack surface checked

- **Stale snapshot cheat**: ruled out for the measured surface — `c1-after-35/corpus/knowledge`
  is byte-identical to the live 35, and my independent live-minus-2 copy reproduces 35/35.
- **Instrument drift**: ruled out — sha256 of the live instrument equals the digest embedded in
  all three receipts; selftest 14/14.
- **Base-tree ambiguity**: ruled out — `c1-controls/base` knowledge+instruments equal
  `git archive b49948f` output except wave-1's own staged `recheck-audit.py` copy.
- **Per-entry cheating**: ruled out — 0 diffs on `pass`, all six limb bits, exit codes, command
  text, and both `sha256(stdout\0stderr)` digests, on all three surfaces.
- **`cd` semantics of `--root`**: verified, not a defect — `--root` selects which files are
  audited and which root checks `corpus/` path existence; the 29 `cd`-prefixed commands still
  execute inside the live lane (their `cd` target is the lane root, which is why `--cdroot
  <lane>` yields `cdroot_fail=0`). This is inherent to the fix shape (`cd <lane> && <CMD>`); the
  frozen `cwd` limb remains an equality test between lane-root and `/` runs, so a `cd` prefix is
  exactly what makes it pass. Frozen-limb meaning preserved; strict limbs guard the degenerate
  seats.

## Findings

- **F1 (low, reporting).** `c1-after-35/` is called a "frozen-after" snapshot but only its
  `corpus/knowledge/` (the measured surface) equals the final tree's corresponding 35 files. Its
  `corpus/instruments/recheck-audit.py` is an earlier 7-limb revision (stale copy), and its
  `README.md`/`SOURCES.md`/`QUALITY.md`/`manifest.json` predate C2's landing. Harmless because
  the audit reads only `corpus/knowledge/*.md` and `corpus/` path tokens, and my independent
  reconstruction reproduces the same 35/35 — but the snapshot is not a faithful "tree minus two
  files" outside `knowledge/`.
- **F2 (low, inherent).** The `cdroot`/`instrument`/`own` strict limbs and the `paths` limb are
  evaluated against `--root`, while the `cd`-prefixed commands execute in the live lane; the
  receipt's `executes`/`gated` counts therefore reflect live-lane execution of fixed commands.
  Verdict-stable on all three surfaces (proven by identical digests and exits), but worth one
  line of context when reading `executes=12` on the 35-file snapshot.

## Residual risk / verification gaps

- `~/Projects/bounties` et al. remain absent on this host (verified implicitly: 23 lines still
  exit 1 both cwds). On a host where those paths exist, `gated` lines would execute and counts
  could differ — same host-bound caveat wave-1 recorded.
- I did not re-run the four mutant controls (M1–M4); that is outside this ticket's named item.
- Receipts are uncommitted (`.ufo/waves/round-25/` is `??` in `git status`); "committed" in the
  dispatch means landed in the worktree.

## Verdict

Wave-1's C1 numbers are correct as claimed: instrument `c3c19adc…`, before `pass=6 exit=1`,
frozen-after `35/35 exit=0`, final-after `37/37 exit=0`, all per-entry data byte-identical.
No correction required.
