# ExecH10NoHarmBase — H10 no-harm baseline at the round-40 claims freeze

Seat: `ExecH10NoHarmBase` (leaf executor, round 40, wave 1).
Item: record the base no-harm measurements the C1 `H10` guard compares against, on the
claims-freeze commit `5e985b74075dd3813a63d7750966bf8abf693465`.

- Deliverable: `.ufo/waves/round-40/wave1/ExecH10NoHarmBase.txt`
- Lines: **55** — Bytes: **2713**
- sha256: `087cd15c2e77adb7844bf1d2d8d357b28e5868f9e8dd71d6d5152f854efae8b4`
- Shape: 55 lines, every line `^h10\.[a-z0-9][a-z0-9.-]*=<non-empty>`, zero comment lines,
  zero blank lines, zero duplicate keys (verified, §3).
- Run UTC: `2026-10-26T21:17:40Z` (all reads done after this seat's spawn; nothing back-dated).
- Lane mutations: **none**. `git diff --stat 5e985b74` over the lane is empty; `git status`
  shows only pre-existing untracked sibling wave files plus this seat's `wave1/` dir (§6).
- Tooling: no installs, no upgrades (nothing was needed; `python3`, `git`, `awk` sufficed).

## 1. Axes and the move

Axes owned by this seat's host claim: `depth:verifiability` (C1), `coverage` (C2). This item
serves C1 `H10` — the no-harm limb, which is the one check that can *red* a round that
otherwise closes 10/10, so its baseline has to be exact rather than approximate. One move:
take four measurements at the freeze commit and emit them as machine-comparable `key=value`
lines, with the freeze readings distinguished from the at-Y invariants so the suite builder
cannot wire a drifting value as a hard equality.

## 2. Runs (verbatim commands, actual output)

All runs executed with `cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin` (working tree is
byte-identical to the freeze commit for every file measured — checked in §2.5) and, to prove
export-mode parity, against a `git archive` export of `5e985b74` under this seat's scratch.

### 2.1 Density census (freeze commit)

```
$ python3 corpus/instruments/density.py SKILL.md --label SKILL
# Density census — SKILL (1115 lines, 27 blocks)
...
| | **mean dens** | | | | | | | | **232.9** |

Total path-citation instances: 771 across 27 blocks.
```

`mean dens = 232.9`, `27` blocks, `1115` file lines, `771` path-citation instances.

### 2.2 Anchor check (freeze commit)

```
$ python3 corpus/instruments/anchorcheck.py SKILL.md
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

(The 306 `LOST-RECORDED` detail lines are pre-existing lost-tree/lost-base citations recorded
in the file itself; the guard-relevant fields are `0 bad`, `PIN-BROKEN=0`, `ORIGIN=0`,
`OUTSIDE-BASE=0`, `BASE-ABSENT=0`.)

### 2.3 Append-only limb — SKILL.md and PROVINCE.md, base → freeze

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --numstat \
    a7af2ce63bce153757d39bf66b366a96caf30c13 5e985b74075dd3813a63d7750966bf8abf693465 \
    -- SKILL.md PROVINCE.md
<no output>
rc=0
```

Empty: neither front door moved one byte across the round's pre-freeze commits, so the
append-only requirement is trivially satisfied at the freeze by construction. Both files are
byte-identical at base and at freeze:

| path | lines | sha256 (identical at base and freeze) |
|---|---:|---|
| `SKILL.md` | 1115 | `ce6689c554f2e33b6d7b79a53fde387b7f7e7140ace1ade6e9f4670548b242f4` |
| `PROVINCE.md` | 158 | `4d42eed1afa00ff0dafcfea235e2f48c3b607fd67cdbe1d489504f1a098a155c` |
| `corpus/instruments/density.py` | 208 | `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710` |

### 2.4 Whole-tail numstat — base → freeze

```
$ git diff --numstat a7af2ce63bce153757d39bf66b366a96caf30c13 5e985b74075dd3813a63d7750966bf8abf693465
11	0	.ufo/waves/round-40/c1-controls/before.txt
10	0	.ufo/waves/round-40/c2-controls/before.txt
20	0	.ufo/waves/round-40/c2-controls/junk-decisions.md
5	0	.ufo/waves/round-40/census-before.txt
71	0	.ufo/waves/round-40/claims.json
rc=0

$ git diff --name-status a7af2ce6... 5e985b74...
A	.ufo/waves/round-40/c1-controls/before.txt
A	.ufo/waves/round-40/c2-controls/before.txt
A	.ufo/waves/round-40/c2-controls/junk-decisions.md
A	.ufo/waves/round-40/census-before.txt
A	.ufo/waves/round-40/claims.json
```

5 files added, 117 added lines (`11+10+20+5+71`), **0 deleted lines**, **0 deleted paths**,
`A` only (no `M`/`D`). Only the freeze files were added, exactly as the item requires.

Both views are emitted as keys so the paired reviewer (wave-1 `items[45]`, which reproduces
`--name-status` and lists changed paths) can compare machine-to-machine without parsing prose:
`h10.freeze.numstat.{1..5}=<added>:<deleted>:<path>` and
`h10.freeze.name-status.{1..5}=<status>:<path>`.

```
$ git diff --diff-filter=D --name-only a7af2ce6... 5e985b74... | wc -l
0
$ git diff --name-only a7af2ce6... 5e985b74... -- corpus/instruments | wc -l
0
```

The instruments subtree is untouched base → freeze: the density instrument's bytes at the
freeze are its bytes at base, so the `expect-density-sha256` pin is not merely a snapshot of
a round-40 edit.

### 2.5 Freeze-lineage and export parity

```
$ git rev-parse 5e985b74^
a7af2ce63bce153757d39bf66b366a96caf30c13          # freeze is a DIRECT child of base
$ git show -s --format='%H%n%ci%n%s' 5e985b74
5e985b74075dd3813a63d7750966bf8abf693465
2026-10-26 18:10:32 -0300
round-40: freeze claims C1/C2 + control receipts
```

Export parity — the suite runs over `git archive`, not the working tree, so the baseline was
re-taken on an archive of the freeze under scratch:

```
$ git -C <lane> archive --format=tar 5e985b74 | tar -xf - -C $S/exp     # 7755 files
$ cd $S/exp && sha256sum SKILL.md PROVINCE.md corpus/instruments/density.py
ce6689c5…b242f4  SKILL.md
4d42eed1…a155c   PROVINCE.md
ee803726…f54710  corpus/instruments/density.py
$ python3 corpus/instruments/density.py SKILL.md --label SKILL | grep -E 'mean dens|Total|^# Density'
# Density census — SKILL (1115 lines, 27 blocks)
| | **mean dens** | | | | | | | | **232.9** |
Total path-citation instances: 771 across 27 blocks.
$ python3 corpus/instruments/anchorcheck.py SKILL.md | grep '^== '
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

Identical digests and identical instrument output in export mode: the baseline is
reproducible from `git archive` alone, no working-tree dependence.

## 3. Deliverable validation

Every one of the 55 emitted keys was recomputed independently from `git show`, `git diff
--numstat`, and fresh instrument runs over the archive export, then compared against the file:

```
expected keys: 55 | file keys: 55
missing: []   extra: []   MISMATCHES: 0
ALL-OK
```

Shape:

```
$ awk '$0 !~ /^h10\.[a-z0-9][a-z0-9.-]*=./ {bad++} END{print ...}'  -> lines=55 bad=0
$ cut -d= -f1 <file> | sort | uniq -d | wc -l                       -> 0
$ wc -lc <file>                                                     -> 55 2713
$ sha256sum <file>  -> 087cd15c2e77adb7844bf1d2d8d357b28e5868f9e8dd71d6d5152f854efae8b4
```

### 3.1 Negative control — the comparison can fail

A copy of the deliverable was mutated three ways (guard pin so the last hex digit `6`→`7`;
`deleted-lines` `0`→`1`; an invented sixth numstat row) and re-validated with the same
recomputation:

```
negative control on mutated copy:
  mismatches = 2
   MISMATCH h10.freeze.deleted-lines        got = 1                        want= 0
   MISMATCH h10.guard.expect-density-sha256 got = ee803727…f54710           want= ee803726…f54710
  extra-keys = [... 'h10.freeze.numstat.6' ...]
  VERDICT: caught
```

The invented row is caught as an unexpected key, the flipped digest and the false deletion
count as value mismatches. The validator is therefore able to red a tampered baseline, which
is the property that makes it usable as guard evidence rather than decoration.

## 4. How H10 should consume these keys (handoff to the suite builder)

Two classes, deliberately distinguished — wiring the second class as an at-Y equality would
be a false red the moment round 40 appends a SKILL.md block.

**(a) Hard invariants, safe to assert at the verification ref Y** (they are properties of the
append-only/no-delete regime, not snapshots of a transient reading):

| key | assert |
|---|---|
| `h10.guard.expect-skill-deleted` | `git diff --numstat <base> <ref> -- SKILL.md` deleted column `== 0` |
| `h10.guard.expect-province-deleted` | same for `PROVINCE.md` deleted column `== 0` |
| `h10.guard.expect-density-sha256` | `sha256(<ref>:corpus/instruments/density.py) == ee803726…f54710` |
| `h10.guard.expect-deleted-paths` | `git diff --diff-filter=D --name-only <base> <ref> \| wc -l == 0` |
| `h10.guard.expect-instruments-changed-paths` | `git diff --name-only <base> <ref> -- corpus/instruments` adds no change to `density.py` (round 40 legitimately ADDS `r40-closure.sh`, so assert membership of `density.py` in the change set is false, not that the subtree delta is empty — see §5 risk R2) |

**(b) Freeze readings — provenance, not at-Y equalities.** `h10.skill.*`, `h10.province.*`,
`h10.density-instrument.*`, `h10.freeze.census.*`, `h10.freeze.anchorcheck.*`. These pin
*which commit and which bytes* the baseline was taken on (`5e985b74`, digests above). They
must be reproduced by re-running the instruments at the freeze commit; they must NOT be
compared against the Y export, because round 40 will append to `SKILL.md` (the r29–r36
precedent: one "Gates & probes registry addition" block per round), which moves
`file-lines`, `blocks`, `mean-dens`, `path-cite-instances` and the anchorcheck counts.

The append-only limb is a `deleted == 0` assertion, not an `added == 0` assertion: a round
that adds zero lines to both front doors also satisfies no-harm, and an `added >= 1` floor
would red a legitimately quiet round. `added` is deliberately absent from the guard keys.

## 5. Risks / notes for the integrator

- **R1 — census keys drift by design.** If `r40-closure.sh`'s H10 compares
  `h10.freeze.census.mean-dens` at Y, it will red spuriously after the round's own SKILL.md
  append. §4(b) is the instruction that prevents this; the keys are named `h10.freeze.*`
  precisely to signal "reading at the freeze", and the guard keys are named
  `h10.guard.expect-*` precisely to signal "assert at Y".
- **R2 — instruments subtree is not frozen whole.** Round 40 MUST add
  `corpus/instruments/r40-closure.sh`. `expect-instruments-changed-paths=0` is a *base→freeze*
  observation only; at Y the correct guard is "`density.py` itself is unchanged"
  (`expect-density-sha256`), which is a subset assertion and survives the new file.
- **R3 — anchorcheck denominators.** `16 in-range / 306 LOST-RECORDED` are freeze readings.
  Any round-40 SKILL.md cite addition changes both. Do not pin them at Y.
- **R4 — no-harm does not cover `corpus/SOURCES.md` / `corpus/knowledge/`.** Those are the C2
  deliverables and are expected to grow. `H10`'s deleted-paths limb is whole-tree and still
  applies to them (`--diff-filter=D` must stay empty), which is the only correct reading:
  growth is allowed, deletion anywhere is not.
- **R5 — `git status` at filing** carries untracked sibling wave files
  (`wave1-plan.out`, `wave2-dispatch.json`, `kasegi-r40-build.ready*`, …) written by the L1
  and other seats, plus this seat's `wave1/` dir. None are tracked; none are mine to remove.
  The H6-style scratch check is a distinct claim limb, not mine — but for the record this
  seat's scratch dir is removed before yield (§7) and I created no `kasegi-r39*`/`r40`-suffixed
  sibling directory anywhere.

## 6. Blast radius

Writes made: exactly two paths, both inside this seat's allowance.

1. `.ufo/waves/round-40/wave1/ExecH10NoHarmBase.txt` (deliverable, 55 lines / 2713 B / sha256 above)
2. `.ufo/waves/round-40/wave1/ExecH10NoHarmBase.md` (this receipt)

Plus scratch under `/fast/scratch/hyaku/kasegi-r40/ExecH10NoHarmBase/`. No tracked lane file
was created, modified or deleted (`git diff --stat 5e985b74` → empty). No file in the fleet
root, `shokuknow`, `~/Projects/*`, `MANIFEST.json`, `templates/`, `scripts/`, `.ufo/state/`,
or `~/.local/bin` was touched. No mutating git/jj command was run: every git invocation was
`rev-parse`, `show`, `diff`, `archive` or `status`.

## 7. Scratch

`S=/fast/scratch/hyaku/kasegi-r40/ExecH10NoHarmBase` held the archive export (`exp/`) and the
mutation copy. Both removed with the scratch dir at the end of this seat (`rm -rf -- "$S"`),
after the deliverable and receipt were copied into the wave dir; the H6 live scratch check
will find no `ExecH10NoHarmBase` directory.
