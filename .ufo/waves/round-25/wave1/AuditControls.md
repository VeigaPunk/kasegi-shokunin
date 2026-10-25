# C1 isolating controls — `recheck-audit.py` limb liveness (round 25, wave 1)

Seat `L1Kasegi25.AuditControls`. Lane base revision `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.
Instrument under test: `corpus/instruments/recheck-audit.py`, sha256
`d07af435009a0395662b3062c33bd5e5242afd8b6902d30f34b155cd11b564d6` (untracked lane file; copied
into every scratch tree so each tree is self-contained).

All work is on scratch copies under `.ufo/waves/round-25/c1-controls/`. No production file was
edited; no VCS write was issued.

## Verdict

**Every limb is load-bearing. No mutant passes.** Each of M1–M4 flips exactly one limb of one
previously-passing line, and the tree's `pass` count drops 6 → 5 with exactly one failing-limb
counter rising by exactly one. The do-nothing control stays at `pass=6`, i.e. it does **not**
reach the frozen target `pass=35`, so the claim's target is not met by the base bytes.

## Base tree construction and fidelity

```
git -C …/kasegi-shokunin archive b49948f corpus | tar -x -C .ufo/waves/round-25/c1-controls/base
cp corpus/instruments/recheck-audit.py .ufo/waves/round-25/c1-controls/base/corpus/instruments/
```

`git archive` yields base-revision bytes for `corpus/knowledge` (35 files), `corpus/instruments`
(minus the untracked instrument, copied in) and `corpus/source-snapshots` — the last is required so
the six non-prefixed recheck commands can actually execute from the scratch root and be compared
against the foreign cwd; without it both runs would fail identically and limb (b) would pass
spuriously.

Fidelity check, per file:

```
for f in $(git ls-tree --name-only b49948f corpus/knowledge/); do
  git show b49948f:$f | sha256sum ; sha256sum .ufo/…/base/$f ; done
base-vs-b49948f mismatches=0 files=35
```

Mutant isolation: `diff -rq base <tree>` reports exactly one differing file
(`corpus/knowledge/authorised-testing-rules-of-engagement.md`) for each of M1–M4, and no
difference at all for `do-nothing` (`diff -r base do-nothing` → exit 0, no output).

Per-tree recheck-manifest digest (sha256 over the sorted 35 `entry<TAB>recheck-line` pairs):

| tree | manifest sha256 | lines |
|---|---|---|
| base | `1f90e35f3f9469f693eedcac5fb20d689e216ffc7bbe70cbaca9407a9482b405` | 35 |
| do-nothing | `1f90e35f3f9469f693eedcac5fb20d689e216ffc7bbe70cbaca9407a9482b405` | 35 |
| M1-parse | `ecb1fa735e35631f6147600a3bc76b45021f73245c3e154bfd2189af4def7c95` | 35 |
| M2-cwd | `3888a30d98d733b10d5402cacaf6de01477992ecd2ec1ad5060a2bf8df38c12d` | 35 |
| M3-paths | `4f58a3c2862abce45856e2a6f5385c1d4f3fbf00658528f0d6cb7b319449cbfe` | 35 |
| M4-degenerate | `92d2157b9f46380d82947d450e3fdc154dd5ca23341559782afdcde7001ebe0b` | 35 |

## Scoring command (identical for every tree)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-controls/<tree> \
        --json .ufo/waves/round-25/c1-controls/<tree>.json
```

Receipts: `base.txt`, `do-nothing.txt`, `M1-parse.txt`, `M2-cwd.txt`, `M3-paths.txt`,
`M4-degenerate.txt` (command line + full per-entry output + `EXIT=`), matching `.json`, and
`mutants-diff.txt` (unified diffs + the digest table above).

## Receipts

| tree | lines | pass | fail-closed | parse_fail | cwd_fail | paths_fail | exit | target-line triple (parse,cwd,paths) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| base | 35 | **6** | 23 | 23 | 6 | 0 | 1 | `111` |
| do-nothing | 35 | **6** | 23 | 23 | 6 | 0 | 1 | `111` |
| M1-parse | 35 | 5 | 24 | **24** | 6 | 0 | 1 | **`011`** |
| M2-cwd | 35 | 5 | 23 | 23 | **7** | 0 | 1 | **`101`** |
| M3-paths | 35 | 5 | 24 | 23 | 6 | **1** | 1 | **`110`** |
| M4-degenerate | 35 | 5 | 23 | 23 | 6 | **1** | 1 | **`110`** |

(a) **Base receipt reproduces the frozen before exactly**:
`lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` — identical to
`claims.json` `before` and to `.ufo/waves/round-25/c1-before.json`. The 6 passing lines are the 5
`cd … && python3 corpus/instruments/source-recheck.py …` entries plus
`root-loss-2026-10-12.md` (absolute `~/Projects/...` tests only).

(b) **Each mutant fails exactly the intended limb** (target line = the entry's
`recheck:` line, mutated in place; every other line byte-identical):

| mutant | mutation (exact new `recheck:` value) | triple | only counter that moved | target-line run |
|---|---|---|---|---|
| M1 parse | `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S032 (note)` | `011` | parse_fail 23 → 24 | lane=2 foreign=2 |
| M2 cwd | same command with the `cd … && ` prefix removed | `101` | cwd_fail 6 → 7 | lane=0 foreign=2 |
| M3 paths | `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/anchorcheck.py corpus/knowledge/ghost.md` | `110` | paths_fail 0 → 1 | lane=1 foreign=1, `missing_paths=['corpus/knowledge/ghost.md']` |
| M4 degenerate | `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true` | `110` | paths_fail 0 → 1 | lane=0 foreign=0, `missing_paths=[]` (names no `corpus/` path and no `~/Projects/` base) |

No other entry changed verdict in any mutant; `pass` fell by exactly one each time, so each limb is
individually necessary to the conjunction and none is redundant with another.

(c) **No mutant passes.** No limb is inert; no instrument weakening to report. The four controls
together cover all three limbs: parse (M1), cwd (M2), paths-existence (M3) and paths-naming (M4 —
the degenerate `cd <lane> && true`, which is otherwise a perfectly cwd-independent, parseable
no-op, so only limb (c) can reject it).

(d) **Do-nothing control: `pass=6`, `exit=1`.** It does not reach `pass=35`; the frozen target is
not satisfied by the unchanged base bytes, which is the condition the claim requires.

## Instrument limits observed while building the controls (recorded, not repaired)

1. **Limb (b) is evaluated even when limb (a) fails, and passes trivially then.** M1's target line
   reports `cwd=True` because `bash -c` refuses the same syntax in both cwds and the identical
   stderr digests match. The same triple `011` appears on all 23 prose lines in the base receipt.
   The conjunction is still sound (the line fails on parse), but `cwd_fail` under-reports cwd
   dependence among unparseable lines — it counts only lines whose command actually runs.
2. **Limb (b) is satisfied by an absolute `cd`, not by success.** M3's command fails (exit 1) in
   both cwds and is therefore cwd-independent; limb (c) is the sole discriminator there, which is
   what makes M3 a clean paths control.
3. **`paths_fail` conflates "names nothing" with "names something missing".** M3 and M4 both score
   `110`; the JSON's `missing_paths` (ghost.md vs empty) is the only field separating them.

## Concurrency note (why the controls score git bytes, not the worktree)

`corpus/knowledge` in the working tree is being edited by sibling wave-1 seats while this seat ran:
`git status --porcelain corpus/knowledge | wc -l` → **29 modified files**, and the live worktree
currently scores `lines=35 pass=32 fail-closed=23 parse_fail=0 cwd_fail=3 exit=1`
(`c1-controls/live-lane.json`). That receipt is **not** the frozen before and is not used by this
report for any verdict; the base tree is `git archive b49948f`, which is byte-pinned (0/35
mismatches). Recording it so no later reader mistakes the moving worktree for the frozen state. The same
window also carries a peer's `corpus/instruments/README.md` edit (10+/4−, D24-2/D24-3 wording);
this seat did not write it — every file this seat touched is listed below.

## Files written (all inside `.ufo/waves/round-25/c1-controls/`)

- `base/`, `do-nothing/`, `M1-parse/`, `M2-cwd/`, `M3-paths/`, `M4-degenerate/` — scratch trees
  (`corpus/{knowledge,instruments,source-snapshots,lessons}`).
- `base.txt` / `base.json`, `do-nothing.txt` / `do-nothing.json`, `M1-parse.txt` / `M1-parse.json`,
  `M2-cwd.txt` / `M2-cwd.json`, `M3-paths.txt` / `M3-paths.json`, `M4-degenerate.txt` /
  `M4-degenerate.json`, `mutants-diff.txt`, `live-lane.json`.
- This report: `.ufo/waves/round-25/wave1/AuditControls.md`.

No tool was installed or upgraded for this item.

## Checks the main agent should run

- `diff -r .ufo/waves/round-25/c1-controls/base .ufo/waves/round-25/c1-controls/do-nothing` → no
  output (do-nothing is the unchanged base).
- `python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-controls/base` →
  `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`.
- Spot-check any mutant tree's single differing file against the mutation table above
  (`mutants-diff.txt` carries the unified diffs).
