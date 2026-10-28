# ScribeQualityRows — round 43 receipt

Seat `ScribeQualityRows` (leaf scribe, kasegi-shokunin round 43, L1 `KasegiR43`). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Read first, not edited: `.ufo/waves/round-43/claims.json` (sha256
`a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630`, per
`.ufo/waves/round-43/freeze.txt`). No subagent dispatch, no mutating git, no writes outside this wave
file, the deliverable below, and `$S`.

## Deliverable

| path (relative to `kasegi-shokunin/`) | lines | bytes | sha256 |
|---|---:|---:|---|
| `.ufo/waves/round-43/w1/ScribeQualityRows.append.md` | 17 | 6982 | `4f91038519632a2b766d374865275b6fb78a5b05ce3d77925b91c3061a0c14d1` |

Byte-exact append block for `corpus/QUALITY.md`: heading line, the R6 preamble (fresh bytes/lines/sha
plus the not-edited row list), a three-column table, and four rows `R43`–`R46`. It is the only
landable content; all validation lives in this receipt.

## Candidate → landed id

Row ids continue the file (`R42` is the last row at line 354), so the dispatch's four candidates
`R43-1`…`R43-4` land as `R43`…`R46` 1:1. The `### Round-43 move-log rows` LOG draft
(`w1/ScribeLogEntry.log-entry.md:116`) names the same four criteria in this order.

| candidate | landed id | title | grounded in (committed evidence) | machine check |
|---|---|---|---|---|
| R43-1 narrative-vs-evidence binding | R43 | a record asserting a run/tally/wave is graded by a committed counter over its own bytes | RD42-1 `SCORECARD.md:1634` vs `final-gates/all-gates.txt:16`; RD42-2 `LOG.md:1804`; RD42-3 `corpus/lessons/round-42.md:11,16`; RD42-4 `corpus/lessons/round-42.md:52`; RD42-5 `round-42-verifier-spotcheck.md:65` vs `all-gates.pre-repair.txt:19,33`; RD42-8 round-42 C1 `before` vs `c1-controls/do-nothing.txt:16`; M43-1 withdrawn pre-declared base figure (`INTEGRATION-PLAN.md` §Mined mistake) | K14–K18 of `corpus/instruments/r43-closure.sh` |
| R43-2 freeze-record ordering | R44 | declared freeze instant corroborated by its containing commit and cited controls | RD42-6 `round-42-verifier-spotcheck.md:38,178`; round-42 `wave1/ConnCrossClaims.md:54`; round-42 `claims.json` `frozen_at_utc` vs commit `0566bd66` | K19 (`w1/ExecK19Freeze.transcript.txt`) |
| R43-3 capability rows require a run | R45 | a capability row enters only with its demonstration command and printed output; `<pending: demo>` until then | round-42 `wave1/RevC2Shape.md:152` ("No measure (45/45 = 1.000) command was exercised…"), quoted at `w1/ScribeReportSkeleton.report.md:420`; round-43 row ships `<pending: demo>` (`w1/ScribeScorecardRound43.append.md` §Round-43 capabilities) | C2 after-state carries commands, not the measure literal |
| R43-4 `claimable` is operator-owned | R46 | a gate never requires, infers or writes `claimable`; it only checks boolean consistency with its own gates | `w1/ScoutClaimContract.md:149` ("That single import makes the exemplar DEFECT and fails the frozen claim", against `claim-gates.md:68`), `:183` (`#/claimable === true` forbidden for the exemplar); `w1/ExecGateChain.md:108-109,130-131` | R-STATUS mutations/probes: `claimable-true-failing-gate` → `verdict=pass`, `claimable-false-no-blocker` → `verdict=pass`, probe `claimable=false with named blocker accepted ok=yes` |

Honesty note on grounding: the round-43 lesson draft's §Mistakes table
(`w1/ScribeLessonDraft.round-43-lesson.md`, read this run) lists exactly seven rows — RD42-1, -2, -3,
-4, -5, -6, -8 — and no M43 row; `M43-1` appears in `INTEGRATION-PLAN.md` §"Mined mistake so far".
`R45`/`R46` are therefore grounded in **wave receipts** (`RevC2Shape.md:152`,
`ScoutClaimContract.md:149/183`, `ExecGateChain.md` probes), which the seat spec allows ("cite the
round-43 lesson section or the wave receipt per row"), not in that table. If the canonical judge
finds no mined mistake behind either, striking `R45`/`R46` leaves `R43`/`R44` self-contained: no
other row cites them. `RD42-8`/`M43-1` were folded into `R43` as its frozen-`before`-cell limb (K17)
rather than minted as a fifth row, because both are one defect shape: a stated result that its own
cited artifact contradicts.

## R6 preamble — measurement (commands and real output)

Measured on the live `corpus/QUALITY.md` immediately before writing the deliverable, 2026-10-28T16:47:40Z:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ wc -c corpus/QUALITY.md ; wc -l corpus/QUALITY.md
71668 corpus/QUALITY.md
354 corpus/QUALITY.md
$ head -c 71668 corpus/QUALITY.md | sha256sum
c4468c9587e09f55eabf3efaee4ed47dd652496fb8b36d386908c121c31cb1be  -
$ sha256sum corpus/QUALITY.md          # the whole file is exactly the 71668-byte prefix
c4468c9587e09f55eabf3efaee4ed47dd652496fb8b36d386908c121c31cb1be  corpus/QUALITY.md
$ stat -c '%s %y' corpus/QUALITY.md
71668 2026-10-28 09:14:05.854698900 -0300   # 12:14:05Z
```

Repeated twice, byte-identical (deterministic). Row line numbers in the preamble were read, not
assumed:

```
$ grep -n '^| R[0-9]* |' corpus/QUALITY.md | sed -E 's/^([0-9]+):\| (R[0-9]+) .*/\2=\1/' | \
    awk -F= '$1~/^R(2[2-9]|3[0-9]|4[0-2])$/'
R22=226 R23=227 R24=228 R25=229 R26=249 R27=250 R28=263 R29=264 R30=277 R31=278 R32=291 R33=292
R34=307 R35=308 R36=309 R37=323 R38=337 R39=351 R40=352 R41=353 R42=354
```

### Landing simulation (copy in `$S`, lane file not touched)

```
$ S=/fast/scratch/hyaku/kasegi-r43/ScribeQualityRows
$ cp corpus/QUALITY.md "$S/QUALITY.md"
$ cat .ufo/waves/round-43/w1/ScribeQualityRows.append.md >> "$S/QUALITY.md"
$ wc -l "$S/QUALITY.md" ; wc -c "$S/QUALITY.md"
371 /fast/scratch/hyaku/kasegi-r43/ScribeQualityRows/QUALITY.md
78650 /fast/scratch/hyaku/kasegi-r43/ScribeQualityRows/QUALITY.md
$ head -n 354 "$S/QUALITY.md" | sha256sum
c4468c9587e09f55eabf3efaee4ed47dd652496fb8b36d386908c121c31cb1be  -
$ grep -c '^| R' "$S/QUALITY.md"
46
$ grep -n '^| R4[0-6] ' "$S/QUALITY.md" | cut -c1-40
352:| R40 | Evidence that a correction l
353:| R41 | A counted or compared value
354:| R42 | A check counts as repaired o
368:| R43 | A committed record that repo
369:| R44 | A claimed freeze instant is
370:| R45 | A capability row enters `SCO
371:| R46 | An exemplar's `claimable` st
$ cmp <(head -c 71668 corpus/QUALITY.md) <(head -c 71668 "$S/QUALITY.md") && echo prefix-identical
prefix-identical
```

So the append shifts no existing line (R6), lands `R43`–`R46` at lines 368–371, and every line of the
block that is a table row has exactly three cells:

```
$ awk -F'|' '{printf "%d NF=%d\n", NR, NF}' ScribeQualityRows.append.md
1 NF=1   2 NF=0   3 NF=1   4 NF=2   5 NF=1 … 11 NF=0
12 NF=5  13 NF=5  14 NF=5  15 NF=5  16 NF=5  17 NF=5
```

(`NF=5` = leading pipe + two separators + trailing pipe; the `NF=2` line is preamble prose carrying
`head -c 71668 corpus/QUALITY.md | sha256sum`, exactly as the round-42 preamble does.)

## Evidence checks run for the rows (read-only, real output)

Each defect the rows ground was re-read from committed bytes this run; none is quoted from memory.

```
$ sed -n '1634p' SCORECARD.md | cut -c1-120
Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite at Y prints `J11 payload=corrections=33
$ sed -n '16p' .ufo/waves/round-42/final-gates/all-gates.txt
J11 payload=corrections=34,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1
$ sed -n '1804p' LOG.md | cut -c1-160
  (`.ufo/waves/round-42/wave1-dispatch.json`); wave 2 `kasegi-r42-falsify` 36 seats dispatched against the repaired head; dead seats counted from `wave2-results
$ sed -n '11p;16p;52p' corpus/lessons/round-42.md | cut -c1-120
never estimated: wave 2 dispatched 36 seats; the round total is 100. Every wave carries connector seats this round (the 
from the wave-2 dispatch when it lands: 36 seats, 32 attack roles.
## Wave-2 falsification
$ ls .ufo/waves/round-42/wave2-results.json
ls: cannot access '.ufo/waves/round-42/wave2-results.json': No such file or directory
$ sed -n '65p' corpus/lessons/round-42-verifier-spotcheck.md | cut -c1-200
instrument at `de09313` prints `closed=10/13 exit=1` and `selftest cases=13 failures=3` (re-run from that ref's own
$ sed -n '19p;33p' .ufo/waves/round-42/final-gates/all-gates.pre-repair.txt
closed=9/13 exit=1
selftest cases=13 failures=4
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-42/claims.json'));print(d['claims'][0]['before'][0][:200])"
see .ufo/waves/round-42/c1-controls/do-nothing.txt — the frozen counter run against the base tree: r42 suite absent (exit 127, cannot print closed=13/13); the r41 suite at base prints closed=10/12 exi
$ sed -n '16p' .ufo/waves/round-42/c1-controls/do-nothing.txt
closed=8/12 exit=1
$ git show -s --format='%H%nauthor=%ai%ncommit=%ci' 0566bd66e93d429b2df8b6751cf10cbdc391e79b
0566bd66e93d429b2df8b6751cf10cbdc391e79b
author=2026-10-27 10:06:29 -0300
commit=2026-10-28 08:00:01 -0300
$ python3 -c "import json;print(json.load(open('.ufo/waves/round-42/claims.json'))['frozen_at_utc'])"
2026-10-28T12:05:00Z
$ grep -n "K14 payload" .ufo/waves/round-43/w1/ExecK14Corrections.transcript.txt | head -3
38:K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
48:K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
63:K14 payload=literals=3,stale=0,superseded=2,live=corrections=35,groups=4 closed=1
$ grep -nE 'mutation claimable|probe claimable' .ufo/waves/round-43/w1/ExecGateChain.md
108:mutation claimable-true-failing-gate expected=R-STATUS observed=R-STATUS count=gates-fail=1 other-rule=pass:yes verdict=pass
109:mutation claimable-false-no-blocker expected=R-STATUS observed=R-STATUS count=blocker=no other-rule=pass:yes verdict=pass
130:probe claimable=true finding_count=0 rejected ok=yes
131:probe claimable=false with named blocker accepted ok=yes
$ sed -n '149p;183p' .ufo/waves/round-43/w1/ScoutClaimContract.md | cut -c1-190
C2 also says the exemplar keeps `claimable` false. So this rule **must not** require `claimable === true`. The lost checker does (`claim-gates.md:68`). That single import makes the exemplar 
- `#/claimable` === `true`. Forbidden for the exemplar. CONTRACT line 42 defines the queue bit; anatomy: absent 241/280, true only 12/280.
$ sed -n '152p' .ufo/waves/round-42/wave1/RevC2Shape.md
- No measure (45/45 = 1.000) command was exercised: it is not in the nine counting commands and its tool is not named in the C2 claim.
$ sed -n '54p' .ufo/waves/round-42/wave1/ConnCrossClaims.md | cut -c1-200
H12 — Freeze timing (`claims.json`). The frozen claims predate every repair, against SCORECARD `:1628`. Its own `frozen_at_utc` value is `2026-10-28T12:05:00Z`. The freeze commit `0566bd6` is `2026-
$ sed -n '43p;49p;61p;73p' .ufo/waves/round-43/w1/ExecK19Freeze.transcript.txt
K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
K19 payload=freeze=present,order=ok,sha=match closed=1
K19 payload=freeze=present,order=bad,sha=match closed=0
K19 payload=freeze=present,order=bad,sha=match closed=0
```

Those four lines are, in order, the `§C` scenarios whose headers read: "--- base ab98fac9 with its own
commit time: no .ufo/waves/round-43/freeze.txt -> red", "--- live round-43 commit, one argument (suite
convention) -> green", "--- m-early: label 16:30:00Z earlier than the control max 16:34:15Z -> red" and
"--- m-dupe-measured: c1 carries two measured-at lines -> red", each read against the current transcript
bytes (309 lines, sha256 `571019c812fce9e1ae53d3af968e49b145e26b931ecd4c042148c44289d349f9`, mtime
2026-10-28 13:48:06 -0300). The transcript was 133 lines when this seat first read it at 16:40Z and
309 lines at 16:52Z; the quoted lines were re-read at the later bytes, and the file also carries the
`m-late-baddigest`, `m-missing-line`, `m-label-drift` and `m-max-drift` runs.

## Decisions

1. **Four rows, ids `R43`–`R46`.** The file's last row is `R42`; a round-43 addition continuing at
   `R43` is the same convention round 42 used (`R39`–`R42` after `R38`).
2. **`RD42-8` + `M43-1` folded into `R43`.** Both are the shape "a record states a result its own
   cited artifact contradicts"; K17 is the check that grades it. One row, one criterion, one check
   family.
3. **No other criteria minted.** `RD42-7` (undispatched wave) is a conformance finding with a
   status-neutral required action, not a record that contradicts a run; `RD42-9` (`SHONEN.md` form) is
   a form defect already covered by R37/R39-style receipt discipline. Minting rows for them would be
   padding without a distinct failure shape.
4. **No claimability or capability state asserted beyond cited receipt lines.** The block never says
   the `claim-package-gate` row entered, never says the demo ran, and never says the exemplar is
   claimable; `R45`/`R46` only state the gates.

## Known limits

1. **Wave mid-flight at write.** `w1/` held 59 entries when the evidence above was read; the lesson,
   `final-gates/`, `corpus/instruments/r43-closure.sh` and `claim-package-check.py` are not on the
   tree yet, so no after-state value appears in the block and none is claimed here.
2. **Preamble is a point-in-time measurement.** `corpus/QUALITY.md` was 71668 bytes / 354 lines with
   sha256 `c4468c95…` at 16:47:40Z (file mtime 12:14:05Z). The landing commit MUST re-run both
   commands (R19): any earlier append in the same round moves them.
3. **`corpus/lessons/round-43.md` is cited but not yet on the tree.** The block cites it as the
   landing path (draft: `w1/ScribeLessonDraft.round-43-lesson.md`). If the L1 lands the lesson with a
   different §Mistakes membership, `R43`/`R44` grounding still resolves through the committed
   round-42 spot-check and the `c1-controls` receipt.
4. **The block carries no validation table and no headings of its own beyond the convention heading**
   (deliverable discipline); the checks are here.

## Observed, out of this seat's write scope

A sibling seat (`W1ScribeLessonGate`) reported by IRC, verbatim and **not verified by me**: registry
defect in the uncommitted r38 SOURCES rows — `corpus/SOURCES.md:189` (S242, `open(2)` ENXIO) has
`NF=14` under `awk -F'|'` because its quoted `"O_NONBLOCK | O_WRONLY"` pipe is unescaped; their
validator run `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin souji`
returned rc=1 with `souji E01 S242 fields=12`. Fix proposed by them: escape the pipe as
`O_NONBLOCK \| O_WRONLY`. Not edited: `corpus/SOURCES.md` is outside this seat's write scope. This is
a second-hand report; I ran no census.

## Tooling

No tool installed or upgraded; no network fetch by this seat (the only fetch in this lane is the
sibling `ExecSourceCapture` curl of `curl.se`, cited in the block through its receipts). Scratch
`S=/fast/scratch/hyaku/kasegi-r43/ScribeQualityRows` is removed before yield; the disk guard was read
before the pass (`/fast/scratch/hyaku` 25% used, 603.8G free).
