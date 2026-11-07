# ExecC1Indep — independent re-derivation of C1 (round 91, attempt 1, wave 1)

Seat: independent C1 verification without reimplementing the lane counter's meter; all three
assigned legs executed. No routed defects found. C1's frozen predicates hold at the landing.

## 1. Frozen C1 command (verbatim)

Executed with cwd = lane, TMPDIR/`--work` = scratch. Full output receipt:
`ExecC1Indep-receipts/ExecC1Indep-frozen-command.txt`.

```
KNOWLEDGE-METER base=890/1883 after=891/1880 base_target=890/1883 target=891/1880 sites=6 labels=6 mirror_absent=True pinned=archive
HOST base abs_tokens=127 abs_nongone=23
HOST after abs_tokens=127 abs_nongone=23
LIMB M0 pass base=890/1883
LIMB M1 pass after=891/1880
LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0
LIMB M4 pass bad=none
LIMB M5 pass out_of_range=none
LIMB M9 pass rows=6 unbound=none
LIMB M10 pass labelled=6 mapped=6 unapplied=none unlabelled=none
LIMB M6 pass sha256=55d50b661bcf79ad5a435c7d7bc86e3954e9910f7dabc480236224170c8c0a7a
KNOWLEDGE-METER-RESULT pass rc=0
```

Pin checks done outside the counter: `sha256sum` of the frozen counter = `be7a100bdf8cd71f75e7bc62b9eb3d548634a46446dec4149d1f5ef48a38b1c1`
and of repair-map.tsv = `55d50b661bcf79ad5a435c7d7bc86e3954e9910f7dabc480236224170c8c0a7a` — both equal the claims.json pins. P3 holds:
`git diff-tree --no-commit-id --name-only -r 8a1a00c…` prints exactly 1 path, `corpus/knowledge/triage-thresholds.md`.

## 2. Own checker, `git show` bytes only (`ExecC1Indep-receipts/ExecC1Indep-check_c1_indep.py`, output `ExecC1Indep-indep-check.txt`)

Base/landing file bytes and the label TSV come only from `git show <rev>:<path>`; the map comes
from the frozen bytes on disk (sha256-checked inside the checker). Label rule reimplemented from
the counter docstring (range label → `` `key` ``→`` `label` ``; fix-replaces-tie-with-— →
`MATCHES: `key``→`—`; fix-names-range → `` `key` ``→`` `corpus/knowledge/<name>.md:N[-M]` ``).
Label TSV cited at blob `9d38d1bc70a4c3ad3e87c4a505ca4143440c25bb` (`e993fd18:…round91-labels.tsv`).

- C1.a base vs landing differ on exactly lines [141, 142, 226, 368, 454, 457] (same line count) — **AGREE**
- C1.b all 6 landed lines equal base with the map's old→new applied once; each old occurs exactly once — **AGREE**
- C1.c all 6 map rows bound to their label row under the docstring rule — **AGREE**
- C1.d labelled=6 mapped=6, unapplied=none, unlabelled=none — **AGREE**

`INDEP-C1-RESULT pass rc=0`.

## 3. Meter in measure mode, live lane vs `git clone --shared` copy in scratch

Outputs `ExecC1Indep-measure-{live,clone}-{base,after}.txt`; clone toplevel asserted equal to the
clone dir before any git call. `diff` byte-identical pairs: **BASE-IDENTICAL**, **AFTER-IDENTICAL**.

| Reading | Value | Live lane | Shared clone | Verdict |
|---|---|---|---|---|
| base rate | 890/1883 (pct 47.27) | yes | byte-identical | AGREE (also = frozen M0) |
| after rate | 891/1880 (pct 47.39) | yes | byte-identical | AGREE (also = frozen M1) |
| HOST lines | abs_tokens=127 abs_nongone=23 both revs | yes | byte-identical | AGREE |
| mirror_absent | True (all runs) | yes | byte-identical | AGREE |

## Verdict per number

- base 890/1883 — AGREE (frozen command, measure live, measure clone)
- after 891/1880 — AGREE (same three sources)
- mapped/labelled sites 6/6, differ-set = {141,142,226,368,454,457}, M9 6/6 bound, M10 complete — AGREE
- map sha `55d50b66…`, counter sha `be7a100b…`, landing changes exactly `corpus/knowledge/triage-thresholds.md` — AGREE
- No DISAGREE. No routed defects from this seat. Qualifier (informational only): absolute-path
  citations (HOST 127/23) are present and unchanged base→after; the claim never asserts they move.

## Housekeeping

- Files written: `ExecC1Indep.md` (this file) and `ExecC1Indep-receipts/`{`ExecC1Indep-frozen-command.txt`,
  `ExecC1Indep-indep-check.txt`, `ExecC1Indep-check_c1_indep.py`, `ExecC1Indep-measure-live-base.txt`,
  `ExecC1Indep-measure-live-after.txt`, `ExecC1Indep-measure-clone-base.txt`, `ExecC1Indep-measure-clone-after.txt`}.
- Receipts carry rates, limb lines, HOST counts and digests only — no fixture bytes, no credential-shaped values.
- No tools installed or upgraded (none needed). No pacman transactions. No git writes in the lane
  (read-only show/rev-parse/diff-tree/ls only; clone was `--shared` into scratch with asserted toplevel).
- Scratch dir `/fast/scratch/hyaku/kasegi-r91/ExecC1Indep/` deleted before yielding.
