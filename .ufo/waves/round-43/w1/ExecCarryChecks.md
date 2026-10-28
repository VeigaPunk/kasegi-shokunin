# ExecCarryChecks — receipt (kasegi round 43, leaf seat)

Seat: ExecCarryChecks (integration owner for the thirteen carried checks).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write target). Fleet root and
`/home/vgpnk/Projects/shokuknow` untouched. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Frozen claims read first; `claims.json` not edited. No subagent dispatched, no swarm, no git/jj mutation
outside my own scratch fixture.

## Deliverables (in this directory)

| file | lines | sha256 |
| --- | --- | --- |
| `ExecCarryChecks.report.md` | 649 | `abdc6fcca330abb1f97c05d1649337762f51bb271d7ece316172560306587211` |
| `ExecCarryChecks.declared-blocks.txt` | 21 | `4084008047e5a5b2263065a7034ae6061f55346241c8c373e963c64c2f72086c` |
| `ExecCarryChecks.transcript.txt` | 147 | `aee9297f4a4ee4a95a67287cadc80187ca7ffb186e1a1b44ffdb98f1235bf59a` |

`ExecCarryChecks.declared-blocks.txt` lands byte-for-byte as `.ufo/waves/round-43/declared-blocks.txt`
(21 entries, r42 format). The report carries the K1-K13 carry recipe, the semantic patch, the measured
base behaviour, the disturbed checks and the integration requirements.

## What was done

Forked `corpus/instruments/r42-closure.sh` in scratch, applied the stage-A rename and the stage-B semantic
patch (report §2-§3), and ran the result three ways. Six scratch-only `check_k14..k19` stubs were needed to
produce a nineteen-line suite before the real limbs land; they are marked in the patch as SCRATCH STUB and
must be deleted at integration.

### 1. the r42 suite over an export of base (baseline)

```
$ bash corpus/instruments/r42-closure.sh --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
      --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work <S>/r42base/work --scratch-root <S>/r42base
all-gates v2
export-ref=ab98fac9dce87130bc4f66de89e30650d63943dc
suite-sha256=fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b
...
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,...,diff=0,...,payload-match=12/12,forged=6/6 closed=0
...
closed=12/13 exit=1
```

Exit 1 (12/13, J8 open because the r42 receipt's ref no longer matches the graded tree). This reproduces
`.ufo/waves/round-43/c1-controls/do-nothing.txt` payload-for-payload.

### 2. the r43 carry over the same export

```
$ bash <S>/r43-carry.sh --export-ref ab98fac9... --lane <lane> --work <S>/c43base/work --scratch-root <S>/c43base
all-gates v3
suite-sha256=none
K8 payload=receipt=(canonical),source=canonical,...,payload-match=18/18,forged=6/6 closed=1
K14 payload=limb=absent,owner=ExecK14 closed=0
...
closed=13/19 exit=1
```

**`closed=13/19 exit=1` with exactly K14-K19 open** — the frozen C1 base-state, measured on the carried
suite's own bytes.

### 3. cell-for-cell comparison (id substituted)

```
K1  identical   K2 identical   K3 identical
K4  DIFFERS  coverage 11/11 -> 13/13
K5  identical   K6 identical   K7 identical
K8  DIFFERS  receipt committed -> (canonical), source committed -> canonical, diff 0 -> 1,
             payload-match 12/12 -> 18/18, closed 0 -> 1
K9  identical
K10 DIFFERS  cases/isolated/graded-lines 13 -> 19
K11 identical   K12 identical   K13 identical
compared=13/13
```

Ten of thirteen are byte-identical; the three that move are documented in report §5 with the exact cell
deltas and the reason each is an extension rather than a relaxation.

### 4. the carry over a scratch round-43 tree

```
$ bash <tree43b>/corpus/instruments/r43-closure.sh --export-ref 029823ad776b6fb223e2f111922e196f84ae4e5b \
      --lane <tree43b> --work <S>/t43run/work --scratch-root <S>/t43run
export-ref=029823ad776b6fb223e2f111922e196f84ae4e5b
suite-sha256=4572ac133aa20dc5cebe56bb5c89588101aae51c8603ec00f2b3b2be42425f62
K1 ... closed=1   K2 ... closed=1   K3 ... closed=1   K4 ... declared=21,valid=21,coverage=19/19 closed=1
K5 ... closed=1   K6 ... closed=1   K7 ... closed=1   K8 ... payload-match=18/18 closed=1
K9 ... closed=1   K10 ... closed=1  K11 ... closed=1  K12 ... closed=1  K13 ... closed=1
closed=13/19 exit=1
```

All thirteen carried checks stay closed on a tree that carries the round's own artifacts (K14-K19 red
there only because they are this seat's stubs). The fixture is a clone of the lane at base plus the
round-43 wave files, the carried suite, the SKILL.md r43 row and two round-43 correction lines; the commit
is made inside `$S/tree43b` only, with a throwaway identity, and `git rev-parse --show-toplevel` was
asserted equal to the fixture path before the commit.

### 5. refusals on the final bytes

```
$ bash <S>/r43-carry.sh
r43-closure: a plain run is refused (export mode only)
exit=2
$ bash <S>/r43-carry.sh --export-ref deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
ERROR ref-not-found ref=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef closed=0 exit=1
exit=1
```

## Findings the L1 must act on (also in report §6)

1. **Vacuity trap, measured.** `run_lines_from` prints `payloads.get(i, ("pending", True))`, so an id in
   `CHECK_IDS` that is missing from `CHEAP`/`run_one` reports `payload=pending closed=1`. My first dry run
   printed `K14…K19 payload=pending` and `closed=19/19 exit=0` at base. Any transcript containing
   `payload=pending` has a forged tally above it.
2. **K2's replay limb had an ungraded substrate.** On a round-43 tree it mutated a round-42 correction and
   the mutant was accepted (`replay=RevC1Counters.defeats.txt=accepted`, measured in the tree43 dry run).
   Fixed by grading only `graded_lines(text)` and injecting the F-TOKEN defeat when no graded line quotes a
   prior tally yet.
3. **K1's evidence reader ignores dot-prefixed paths.** `PATH_RX` starts with `[A-Za-z0-9_]`, so a round-43
   correction citing only `.ufo/waves/...` scores `evidence=0` (measured: `records=2,blocks=2,evidence=0`
   in the dry run). Round-43 corrections must cite `corpus/...` or a 40-hex commit.
4. **K3 needs the integrator's `| r43-closure.sh | … |` row** in `SKILL.md` (exactly one, table-shaped).
5. **Declaration digests are a mid-wave snapshot** (sibling seats were writing `SCORECARD.md`,
   `corpus/README.md`, `corpus/SOURCES.md` while this seat ran). Regenerate at J with the loop printed in
   report §6.4; K4 reads only existence, never the digest.

## Reproducibility of the carried bytes

The report's stage A plus its semantic patch regenerate the exact suite that was run:

```
$ cp r42-mech.sh repro.sh            # r42-closure.sh with stage A applied
$ patch -s -p0 repro.sh < semantic.diff
$ cmp repro.sh r43-carry.sh && echo REPRODUCED
REPRODUCED: stage A + the report patch == the runnable carry bytes
$ sha256sum r43-carry.sh
4572ac133aa20dc5cebe56bb5c89588101aae51c8603ec00f2b3b2be42425f62
```

That digest is also the `suite-sha256=` line of the round-43-tree run (§4 above), i.e. the run graded the
bytes the report reproduces, not a variant.

## Out of scope, forwarded

`W1ScribeLessonGate` reported a `corpus/SOURCES.md` defect (line for `S242`, unescaped `O_NONBLOCK | O_WRONLY`
pipe ⇒ `sources-census.sh validate --root /home/vgpnk/Projects/shokunin souji` reports `E01 S242 fields=12`).
`corpus/SOURCES.md` is not in this seat's write set; forwarded to the L1, and noted in report §8.

## Tooling / environment

`bash 5.3.20(1)-release`, `Python 3.14.8`, `git 2.56.0`. No tool installed, upgraded or removed (no pacman,
no `uv tool install`). Disk guard run before the heavy passes (`bash scripts/hyaku/disk-guard.sh status`:
`/fast` 198G used / 606G free, scratch files idle). Scratch root `/fast/scratch/hyaku/kasegi-r43/ExecCarryChecks`
removed before yielding.

## Residual risk

* The carry is proven against a **synthetic** round-43 tree; the real Y depends on the scribe's round-43
  corrections (evidence token class §6.3), the integrator's SKILL row, and the K14-K19 limbs.
* K8's `payload-match` now spans K14-K19; if any of those limbs emits a payload that is not a pure function
  of the tree, the receipt re-derivation breaks at Y. K14-K19 must keep payloads tree-derived only.
