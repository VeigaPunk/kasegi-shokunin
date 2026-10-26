# ExecDensity — round 38 (depth:density baselines)

Axis: depth:density. Item: record the density and anchor no-harm baselines at base
`a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, then the same over a scratch mirror whose
`SKILL.md` gains one appended Gates & probes registry row for `r38-closure.sh`.
Receipt only.

## Baseline tree

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git rev-parse HEAD
700153593eb586c70a6499c8ca225ee4d673bc9b
$ git status --porcelain | head -3
?? .ufo/waves/round-38/wave1.ready
?? .ufo/waves/round-38/wave1.ready.partial
?? .ufo/waves/round-38/wave1/
$ mkdir -p "$S/base"; git archive a173b0c2b98c5ae39599fa9be76027fbbead0b9e | tar -x -C "$S/base"
extracted files: 7290
$ sha256sum "$S/base/SKILL.md"; wc -l "$S/base/SKILL.md"
dc6b94b0582ca0b1421fc614a5cdc5e4c557be7236b9221032b0ab7205d58b30  .../base/SKILL.md
1113 .../base/SKILL.md
$ cmp -s "$S/base/SKILL.md" SKILL.md && echo identical
SKILL.md identical to worktree
$ git diff --stat a173b0c2 7001535 -- SKILL.md corpus/instruments/
(no output: SKILL.md and both instruments are byte-identical from base to lane HEAD 7001535)
$ sha256sum corpus/instruments/density.py corpus/instruments/anchorcheck.py SKILL.md
ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710  corpus/instruments/density.py
d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912  corpus/instruments/anchorcheck.py
dc6b94b0582ca0b1421fc614a5cdc5e4c557be7236b9221032b0ab7205d58b30  SKILL.md
```

Scratch `S=/fast/scratch/hyaku/kasegi-r38/ExecDensity`; `TMPDIR=$S` exported for every run;
all exports/copies/measurements under `$S`. `python3 -V` = 3.14.8, `git --version` = 2.56.0.

## 1. depth:density at base

```
$ cd "$S/base" && python3 corpus/instruments/density.py SKILL.md --label base
# Density census — base (1113 lines, 27 blocks)
...
| | **mean dens** | | | | | | | | **229.1** |

Total path-citation instances: 760 across 27 blocks.
exit=0
```

Recorded: **mean dens 229.1**, **27 blocks**, **760 path-citation instances** (1113 lines,
ev total 1451, exact mean `229.098889`).

Last block (the registry block an EOF row extends):

```
| 27 | Round-36 Gates & probes registry addition (appended 2026-10-26) | 8 | 7 | 18 | 4 | 9 | 0 | 31 | 442.9 |
```

(`lines=8 nb=7 cites=18 tbl=4 num=9 sig=0 ev=31`; `num_tokens=['0','1','14','2','35','36','37','7','9']`.)

## 2. anchor no-harm at base

```
$ cd "$S/base" && python3 corpus/instruments/anchorcheck.py SKILL.md
...
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors;
   LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
```

Recorded: **in-range 16**, **bad 0**, **distinct 16**, **LOST-RECORDED 306** (all
`[lost-tree]`-marked, recorded not failed), **exit 0**. `lane_root` was the base export
(a full 7290-file lane copy), so lane-relative cites resolved inside the export; no cite
resolves into MIRROR/ORIGIN/BOUNTIES roots (ORIGIN=0, BASE-ABSENT=0, BOUNTIES-ABSENT=0).

## 3. Mirror: SKILL.md + one appended registry row for r38-closure.sh

Row shape lifted from the r37 row at `SKILL.md:1112` (8 columns:
name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner),
with the contract values taken only from the frozen claims (`--export-ref <hash>`, plain run
exit 2, `closed=8/8 exit=0`, `selftest cases=8 failures=0`, base and r37-judged-head exports red).
No per-check live-line payload grammar is asserted, because the suite source is not yet in
wave1 and I will not invent it.

```
$ rm -rf "$S/mirror"; cp -a "$S/base/." "$S/mirror/"
$ printf '%s\n' "$row" >> "$S/mirror/SKILL.md"
$ wc -l -c "$S/mirror/SKILL.md"
1114 110771
$ sha256sum "$S/mirror/SKILL.md"
06b7acf7e22f73afba6a1347959f7182c21c7405b96101c1d7b04fed2c07f6cd
$ cd "$S/mirror" && python3 corpus/instruments/density.py SKILL.md --label mirror-r38-row
| 27 | Round-36 Gates & probes registry addition (appended 2026-10-26) | 9 | 8 | 23 | 5 | 11 | 0 | 39 | 487.5 |
| | **mean dens** | | | | | | | | **230.8** |

Total path-citation instances: 765 across 27 blocks.
exit=0
$ python3 corpus/instruments/anchorcheck.py SKILL.md
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors;
   LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
$ diff <(grep -E '^\| [0-9]+ \|' density-base.txt | grep -vE '^\| 27 \|') \
       <(grep -E '^\| [0-9]+ \|' density-mirror.txt | grep -vE '^\| 27 \|')
blocks 1-26 IDENTICAL
$ diff <(grep -E '^\| [0-9]+ \|' density-base.txt) <(grep -E '^\| [0-9]+ \|' density-mirror.txt)
27c27
< | 27 | ... | 8 | 7 | 18 | 4 | 9 | 0 | 31 | 442.9 |
> | 27 | ... | 9 | 8 | 23 | 5 | 11 | 0 | 39 | 487.5 |
```

Token accounting for the appended row (measured with `density.py`'s own `is_pathlike`;
598-byte single line, 9 backticked spans):

```
pathlike=True   'bash corpus/instruments/r38-closure.sh --export-ref <hash>'
pathlike=True   'closed=K/8 exit=0\\|1'
pathlike=True   'bash corpus/instruments/r38-closure.sh --selftest --export-ref <hash>'
pathlike=False  'selftest cases=8 failures=0'
pathlike=False  'selftest case=G<n>'
pathlike=False  'a173b0c2'
pathlike=True   'closed<8/8 exit=1'
pathlike=False  '2387dcf6'
pathlike=True   'closed<8/8 exit=1'
single-row block census: {'nb': 2, 'cites': 5, 'tbl': 1, 'num': 5, 'sig': 0, 'ev': 11}
num_tokens: ['0', '1', '2', '38', '8']
```

So the row contributes `cites +5`, `tbl +1`, `num +2` (only `38` and `8` are new to the
block) and `nb +1` to block 27: `31 -> 39 ev`, `442.9 -> 487.5 dens`.

## 4. Expected after-values (depth:density)

| quantity | base | after one EOF registry append | delta |
|---|---|---|---|
| mean dens | **229.1** (229.098889) | **230.8** (230.752328) | **+1.7** |
| blocks | 27 | 27 | 0 |
| path-citation instances | 760 | 765 | +5 |
| block 27 (`nb`) | 7 | 8 | +1 |
| block 27 `ev / dens` | 31 / 442.9 | 39 / 487.5 | +8 / +44.6 |
| anchorcheck in-range / bad / distinct / LOST-RECORDED / exit | 16 / 0 / 16 / 306 / 0 | 16 / 0 / 16 / 306 / 0 | none |

**EOF registry append does not move existing blocks.** The census segments on `^#{2,3}`; a
row appended after the last line (file ends with `\n`, so no join hazard) lands inside the
already-open block 27 ("Round-36 Gates & probes registry addition"), and blocks 1–26 come out
byte-identical in the per-block table (diff above). Only the extended block changes; the mean
moves only through that one block's `dens`.

Sensitivity, measured, so the number is not mistaken for a constant of the round: if the
landed row is terser (`corpus/instruments/r38-closure.sh` as its only path-like span, no new
numeric), block 27 is `nb=8 cites=19 tbl=5 num=10 ev=34 dens=425.0` and the mean falls to
**228.4**; if instead the row is landed under its own
`## Round-38 Gates & probes registry addition` heading, a 28th block is created
(`5 lines nb=4 cites=5 tbl=1 num=5 ev=11 dens=275.0`) and the mean is **230.7** across
**28 blocks** (cites still 765). The invariant is the same in all three: blocks before the
append never move, and no variant registers an anchor cite.

## 5. No-harm verdict

- depth:density: 229.1 -> 230.8 for the measured row (registry block 442.9 -> 487.5); no block
  outside the appended one changes; the doc stays at 27 blocks, so no dilution of the mean by
  a sparse stub section (that is exactly what the heading variant would add: a 275.0 block).
- anchors: in-range 16, bad 0, distinct 16, LOST-RECORDED 306, exit 0 before and after —
  the row adds no `path:NN` anchor and no lost-tree marker, so no verdict class moves.
- Nothing else was written: this receipt plus `$S` scratch; `$S` removed below.

## 6. Tooling

No installs or upgrades; existing `python3` 3.14.8 and `git` 2.56.0 sufficed, so no channel
record is due. No pacman, no network fetch, no host service touched.

## 7. Scratch

`/fast/scratch/hyaku/kasegi-r38/ExecDensity` removed after the measurements below were copied
into this receipt (`rm -rf -- "$S"`, then `test ! -e "$S"` verified).

## DELIVERABLE

The exact row measured above (1 line, 598 bytes, sha256
`ded051bf7fa684c03cfc7432cab0f7d98317d57efa4368e86a63d392d15c0897`):

```
| r38-closure.sh | gate | `bash corpus/instruments/r38-closure.sh --export-ref <hash>` (export-mode only; a plain run refuses with exit 2) | then `closed=K/8 exit=0\|1`; exit 0 only for K=8; exit 2 on harness error or plain run; 0 closed \| 1 open \| 2 could-not-evaluate | `bash corpus/instruments/r38-closure.sh --selftest --export-ref <hash>` -> `selftest cases=8 failures=0` exit 0, one `selftest case=G<n>` line per check | base `a173b0c2` export -> `closed<8/8 exit=1`; r37 judged head `2387dcf6` export -> `closed<8/8 exit=1` | read-only (export to a scratch work dir) | kasegi (round 38) |
```
