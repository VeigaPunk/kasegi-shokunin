# ExecCarryChecks — receipt (kasegi round 43, leaf seat)

Seat: ExecCarryChecks (integration owner for the thirteen carried checks).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write target). Fleet root and
`/home/vgpnk/Projects/shokuknow` untouched. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Frozen claims (`claims.json`) read first and not edited. No subagent dispatched, no swarm, no git/jj
mutation outside my own scratch fixture, no write to a PATH directory.

## Deliverables (in this directory)

| file | lines | sha256 |
| --- | --- | --- |
| `ExecCarryChecks.report.md` | 689 | `5882c95ce7e6ffd359d5cfeecb27bcc8215a4be5808e795fb8c7d6f55a2a07d7` |
| `ExecCarryChecks.declared-blocks.txt` | 21 | `4084008047e5a5b2263065a7034ae6061f55346241c8c373e963c64c2f72086c` |
| `ExecCarryChecks.transcript.txt` | 147 | `aee9297f4a4ee4a95a67287cadc80187ca7ffb186e1a1b44ffdb98f1235bf59a` |

`ExecCarryChecks.declared-blocks.txt` lands byte-for-byte as `.ufo/waves/round-43/declared-blocks.txt`
(21 entries, r42 format: `<path> <lines> <sha256>` or `<path> dyn unpinned`).

## What was done

Forked `corpus/instruments/r42-closure.sh` in scratch, applied the stage-A rename and the stage-B semantic
patch (report §2-§3), and ran the result three ways. Six scratch-only `check_k14..k19` stubs were needed to
produce a nineteen-line suite before the real limbs land; they are marked SCRATCH STUB in the patch and must
be deleted at integration.

### 1. the r42 suite over an export of base (baseline)

```
$ bash corpus/instruments/r42-closure.sh --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
      --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work <S>/r42base/work --scratch-root <S>/r42base
all-gates v2
export-ref=ab98fac9dce87130bc4f66de89e30650d63943dc
suite-sha256=fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,...,diff=0,...,payload-match=12/12,forged=6/6 closed=0
closed=12/13 exit=1
```

Reproduces `.ufo/waves/round-43/c1-controls/do-nothing.txt` payload-for-payload.

### 2. the r43 carry over the same export

```
$ bash <S>/r43-carry.sh --export-ref ab98fac9... --lane <lane> --work <S>/c43base/work --scratch-root <S>/c43base
all-gates v3
suite-sha256=none
K8 payload=receipt=(canonical),source=canonical,...,diff=1,...,payload-match=18/18,forged=6/6 closed=1
K14 payload=limb=absent,owner=ExecK14 closed=0
...
closed=13/19 exit=1
```

**`closed=13/19 exit=1` with exactly K14-K19 open** — the frozen C1 base-state, measured on the carried
suite's own bytes.

### 3. cell-for-cell comparison (id substituted)

```
K1 identical  K2 identical  K3 identical
K4  DIFFERS  coverage 11/11 -> 13/13
K5 identical  K6 identical  K7 identical
K8  DIFFERS  receipt committed -> (canonical), source committed -> canonical, diff 0 -> 1,
             payload-match 12/12 -> 18/18, closed 0 -> 1
K9 identical
K10 DIFFERS  cases/isolated/graded-lines 13 -> 19
K11 identical  K12 identical  K13 identical
compared=13/13
```

Ten of thirteen byte-identical; the three that move are in report §5 with exact cell deltas and why each is
an extension, not a relaxation.

### 4. the carry over a scratch round-43 tree

```
$ bash <tree43b>/corpus/instruments/r43-closure.sh --export-ref 029823ad776b6fb223e2f111922e196f84ae4e5b \
      --lane <tree43b> --work <S>/t43run/work --scratch-root <S>/t43run
suite-sha256=4572ac133aa20dc5cebe56bb5c89588101aae51c8603ec00f2b3b2be42425f62
K1..K13 closed=1 (K4: declared=21,valid=21,missing=0,coverage=19/19; K8: payload-match=18/18,forged=6/6)
K14..K19 closed=0   (this seat's stubs)
closed=13/19 exit=1
```

All thirteen carried checks stay closed on a tree that carries the round's own artifacts. The fixture is a
clone of the lane at base plus the round-43 wave files, the carried suite at
`corpus/instruments/r43-closure.sh`, the `SKILL.md` r43 row and two round-43 correction lines; the commit is
made inside `$S/tree43b` only, with a throwaway identity, after asserting `git rev-parse --show-toplevel`
equals the fixture path.

### 5. refusals on the final bytes

```
$ bash <S>/r43-carry.sh
r43-closure: a plain run is refused (export mode only)
exit=2
$ bash <S>/r43-carry.sh --export-ref deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
ERROR ref-not-found ref=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef closed=0 exit=1
exit=1
```

### 6. the carried bytes are reproducible from the report

```
$ cp r42-mech.sh repro.sh            # r42-closure.sh with stage A applied
$ patch -s -p0 repro.sh < semantic.diff
$ cmp repro.sh r43-carry.sh && echo REPRODUCED
REPRODUCED: stage A + the report patch == the runnable carry bytes
$ sha256sum r43-carry.sh
4572ac133aa20dc5cebe56bb5c89588101aae51c8603ec00f2b3b2be42425f62
```

`4572ac13…` is also the `suite-sha256=` line of run 4, i.e. that run graded the bytes the report reproduces.

## Findings the L1 must act on (report §6)

1. **Vacuity trap, measured.** `run_lines_from` prints `payloads.get(i, ("pending", True))`, so an id in
   `CHECK_IDS` that is missing from `CHEAP`/`run_one` reports `payload=pending closed=1`. My first dry run
   printed `K14…K19 payload=pending` and a forged `closed=19/19 exit=0` at base.
2. **K2's replay limb had an ungraded substrate**, measured on the round-43 tree: it mutated a round-42
   correction and the mutant was accepted (`replay=RevC1Counters.defeats.txt=accepted`). Fixed by grading
   only `graded_lines(text)` plus an F-TOKEN injection when no graded line quotes a prior tally yet.
3. **K1's evidence reader ignores dot-prefixed paths** (`PATH_RX` starts `[A-Za-z0-9_]`): a round-43
   correction citing only `.ufo/waves/...` scores `evidence=0` (measured `records=2,blocks=2,evidence=0`
   in the dry run). Cite `corpus/...` or a 40-hex commit.
4. **K3 needs the integrator's `| r43-closure.sh | … |` row** in `SKILL.md` (exactly one, table-shaped).
5. **Declaration digests are a mid-wave snapshot** (sibling seats were writing `SCORECARD.md`,
   `corpus/README.md`, `corpus/SOURCES.md` during the run). Regenerate at J with the loop in report §6.4;
   K4 reads existence, never the digest.
6. **Unresolved composition conflict with the landed skeleton** (report §6.6). While this seat ran,
   `corpus/instruments/r43-closure.sh` landed as a 474-line wrapper whose header says K1-K7/K9-K13
   re-emit the committed r42 suite's `J<n>` lines and that "the round-42 J8 is NOT carried"
   (`CARRIED_REL="corpus/instruments/r42-closure.sh"`), with a `check_k8` that prints
   `source=absent, …,closed-line=0 closed=0` when no receipt exists. Consequences read off that file:
   (a) base becomes **12/19**, not the frozen 13/19, because K8 has no canonical branch; (b) K4 grades
   `.ufo/waves/round-42/declared-blocks.txt`, so this seat's round-43 declaration would never be read and
   the brief's K4-coverage requirement is unmet; (c) K1 keeps `ROUND=42`, so round-43 corrections are
   graded by K14 alone and K2/K3 stay on round-41/round-42 artifacts. The two routes are mutually
   exclusive; the L1 must choose (keep the wrapper and erratum the C1 base state + K4 sentence, or apply
   this report's fork and delete the wrapper's K8/delegation).

## Out of scope, forwarded

`W1ScribeLessonGate` reported a `corpus/SOURCES.md` defect (the `S242` row's quoted `O_NONBLOCK | O_WRONLY`
pipe is unescaped ⇒ `sources-census.sh validate --root /home/vgpnk/Projects/shokunin souji` reports
`E01 S242 fields=12`). `corpus/SOURCES.md` is outside this seat's write set; forwarded to the L1, recorded
in report §8.

## Tooling / environment

`bash 5.3.20(1)-release`, `Python 3.14.8`, `git 2.56.0`. No tool installed, upgraded or removed (no pacman,
no `uv tool install`). Disk guard run before the heavy passes (`bash scripts/hyaku/disk-guard.sh status`:
`/fast` 198G used / 606G free, scratch files idle). Scratch `S=/fast/scratch/hyaku/kasegi-r43/ExecCarryChecks`
removed before yielding.

## Residual risk

* The carry is proven against a **synthetic** round-43 tree. Real Y still depends on the scribe's round-43
  corrections (evidence token class), the integrator's SKILL row, the K14-K19 limbs, and the composition
  decision in finding 6.
* K8's `payload-match` now spans K14-K19: if any of those limbs emits a payload that is not a pure function
  of the tree, the receipt re-derivation breaks at Y.
