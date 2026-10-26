# CritC1Kill — round 39 wave 2 (falsify): C1 depth:verifiability

Seat: `CritC1Kill`. Item: falsify frozen claim **C1** (depth:verifiability, held 4) by
trying to satisfy the r39 suite counters without the real fixes, and to find a state
where `closed=8/8` holds while a routed defect (R1–R5) is still present.

I did not author the deliverable under attack (wave-1 suite by `ExecSuiteBuild`/L1).
Attacked bytes: lane HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37` (= Y,
`round-39: receipt Y (all-gates v3)`), `corpus/instruments/r39-closure.sh`
(sha256 `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`),
`.ufo/waves/round-39/final-gates/all-gates.txt`, `.ufo/waves/round-39/declared-blocks.txt`,
and the frozen predicates in `.ufo/waves/round-39/claims.json` + `claims-erratum-1.md`.

Scratch: `/fast/scratch/hyaku/kasegi-r39/CritC1Kill` (removed before yield). Fixtures:
`git clone --no-hardlinks` of the lane into scratch, toplevel asserted
(`git -C $S/lane rev-parse --show-toplevel` = `$S/lane`), fixture commits made with
`-c user.email=r39-critic@local -c user.name=r39-critic` **inside that clone only**.
The lane and fleet repo were read-only throughout (git read commands only, `--no-optional-locks`
where the suite uses it). No mutating git/jj command was run in the lane.

Tooling: none installed, none upgraded (no pacman, no uv/npx). Network: none used.

**Axis named:** depth:verifiability. Coverage and density are untouched by this seat.

---

## Verdict

C1 **as frozen cannot be held**, on three independent grounds, each measured below:

1. **Its own counting command is unsatisfiable.** `claims.json` C1 lists
   `bash corpus/instruments/r39-closure.sh --export-ref <J> -> closed=8/8 exit=0`.
   At J = `46c66c268502abd1b2c342fc71bf88ccf721845b` the receipt is absent from the export
   by construction (G2 `receipt=0`), so the best achievable J-run is **7/8** (clean lane
   checked out at J, isolated scratch root) and the frozen command on the real lane prints
   **5/8**. Erratum E4 replaces the measured ref with Y after the freeze; `claims.json`
   itself was not amended, so the frozen file contradicts its own erratum.
2. **Over Y the frozen command is red on the lane:** `closed=6/8 exit=1` and
   `selftest cases=8 failures=2`. The 8/8 exists only with two non-default deviations that
   the detecting command does not contain (`--lane <clean clone at Y>`,
   `--scratch-root <isolated>`), and the committed receipt records neither.
   This is exactly the R1 class (a frozen predicate that no commit can satisfy) recurring at
   the measurement level, one layer up from where round 39 closed it.
3. **The G2 "graded receipt" limb still passes shape, not truth.** A receipt whose selftest
   block is eight well-formed case lines with **zero detail lines** — bytes no `--selftest`
   run produces — is accepted at `closed=8/8 exit=0`; the suite's *own* judge
   (`judge_selftest_report`) **rejects the same bytes**, and the **landed receipt is that
   shape** (0 detail, 0 judge lines). R3 ("the committed 8/8 is a receipt whose payloads are
   placeholders; G2 checks shape") is therefore not closed.

What does hold (measured, not conceded): the 34 selftest mutants are real and all rejected in
a clean fixture; base and r38-head are red; the plain run is refused with exit 2; the two
declared front-door tails are exact; the G1/G4/G8 mutant limbs are load-bearing.

---

## 0. Controls (do-nothing)

```
$ bash corpus/instruments/r39-closure.sh            # plain run
exit=2
r39-closure: refusing to run against the live worktree: this suite is export-mode only.

$ bash corpus/instruments/r39-closure.sh --export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a
closed=1/8 exit=1        (G1,G2,G4,G5,G7 closed=0)

$ bash corpus/instruments/r39-closure.sh --export-ref 66703acaaff50529a35be49aa8759d04140720ad
closed=1/8 exit=1        (G1,G2,G4,G5,G7 closed=0)
```

The base/r38-head reds are genuine, not vacuous (G1 `diff-read=missing`, G2 `receipt=0`,
G4 `read=fail`, G5/G7 `section=0`).

---

## 1. Reproducibility matrix of the frozen counter

All rows are the frozen command shape `bash corpus/instruments/r39-closure.sh --export-ref <ref>`
(`TMPDIR=$S` only; extra flags shown where used). "real lane" = `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
at HEAD = Y; "clean clone" = scratch clone checked out at `<ref>` with an empty `git status --porcelain`.

| ref | lane | scratch root | observed |
|---|---|---|---|
| J `46c66c2` | real lane (HEAD=Y) | default `/fast/scratch/hyaku` | **closed=5/8 exit=1** (G2,G6,G8 red) |
| J `46c66c2` | clean clone @J | isolated | **closed=7/8 exit=1** (G2 red only) |
| Y `5006097` | real lane (HEAD=Y) | default | **closed=6/8 exit=1** (G6,G8 red) |
| Y `5006097` | real lane | isolated | **closed=7/8 exit=1** (G8 red) |
| Y `5006097` | clean clone @Y | default | **closed=7/8 exit=1** (G6 red) |
| Y `5006097` | clean clone @Y | isolated | **closed=8/8 exit=0** ← the only green state |

Row 3, verbatim:

```
G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=none,read=ok closed=0
G8 payload=pin-ref=2387dcf6ccfefcfb703783387b9aade8fc82abfa,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=0,r37-exit=1 closed=0
closed=6/8 exit=1
```

Causes, attributed:

- **G6** is live by design and the wave-2 protocol itself reds it: `kasegi-r39` holds the
  seats' own scratch dirs (11 entries when measured — 10 seat dirs + `gates-work`; 25 by the
  time this receipt was written). The seat spec *mandates*
  `S=/fast/scratch/hyaku/kasegi-r39/<SEATNAME>`; the suite audits that same root. A verifier
  cannot be quiescent while verifying.
- **G8** runs the pinned r37 suite against `--lane`, and r37's E9 limb reads the live
  worktree. On the real lane, `git status --porcelain` = 5 untracked wave-2 entries, so:

```
E9 payload=status-read=ok,status-dirty=5,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=absent closed=0
closed=13/14 exit=1
```

  i.e. G8 is red because the round's own dispatch files exist. The suite header documents
  "at the real judged head the lane must be checked out at Y with a clean tree"; the frozen
  counting command does not say `--lane <clean clone>`, so the command is red for the whole
  duration of wave 2.

Row 6 was reached with `--lane <clean clone @Y> --scratch-root <isolated> --work ...`, and
the suite itself flags both deviations:

```
deviation=non-default --lane
deviation=non-default --scratch-root
closed=8/8 exit=0
```

The committed receipt at Y has **no** `deviation=` line and its G6 payload names the real
root, so its 8/8 is a point-in-time measurement, not a re-runnable counter.

Selftest:

```
$ bash corpus/instruments/r39-closure.sh --selftest --export-ref 5006097...   # real lane
selftest case=G6 positive=fail mutants=4/4 verdict=fail
selftest case=G8 positive=fail mutants=3/3 verdict=fail
selftest cases=8 failures=2        exit=1

$ bash corpus/instruments/r39-closure.sh --selftest --export-ref 5006097... \
    --lane $S/lane --scratch-root $S/sroot --work $S/wst                  # clean clone
selftest case=G1 positive=pass mutants=4/4 verdict=pass
selftest case=G2 positive=pass mutants=8/8 verdict=pass
selftest case=G3 positive=pass mutants=2/2 verdict=pass
selftest case=G4 positive=pass mutants=6/6 verdict=pass
selftest case=G5 positive=pass mutants=4/4 verdict=pass
selftest case=G6 positive=pass mutants=4/4 verdict=pass
selftest case=G7 positive=pass mutants=3/3 verdict=pass
selftest case=G8 positive=pass mutants=3/3 verdict=pass
selftest cases=8 failures=0        exit=0
selftest judge=own-report accepted=1
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-7-cases rejected=1
selftest judge=forged-no-verdict rejected=1
```

So the mutant machinery is real (34/34 rejected). The weakness is downstream, in G2.

---

## 2. Assigned attempts (every named attempt must fail to go green)

Fixture shape for each attack: C0 = Y's tree plus the one mutation; C1 = C0 + receipt whose
`export-ref=C0` (so `git diff --name-only C0 C1` = receipt only, the G2 ancestry/diff limb is
clean and the observed red is the attacked limb, not collateral). Control run first.

### Control — well-formed receipt on the unmodified Y tree

```
### ctrl (ref 58e6819420297c0160da6f4c299d3d2b1e25ff53)
G2 payload=receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,diff-read=ok,digest-match=1,export-suite=1,run-lines=8,closed-lines=0,distinct-ids=8,closed-line=1,graded-cases=8,ungraded-cases=0,selftest-summary=1,scorecard-ref=1,shonen-ref=1,final-lane-commit=0 closed=1
closed=8/8 exit=0
```

Control green ⇒ every red below is the attacked limb.

### (a1) receipt with nine `G<n> ... closed=1` lines

```
G2 payload=...,run-lines=9,closed-lines=0,distinct-ids=8,... closed=0
closed=7/8 exit=1
```

**Rejected** (`run-lines=9`).

### (a2) receipt with a summary-only selftest line

```
G2 payload=...,graded-cases=0,ungraded-cases=0,selftest-summary=1,... closed=0
closed=7/8 exit=1
```

**Rejected** (`graded-cases=0`).

### (a3) eight case lines without the `verdict=` field

```
G2 payload=...,graded-cases=0,ungraded-cases=8,... closed=0
closed=7/8 exit=1
```

**Rejected.**

### (a4) eight well-formed case lines, **no detail lines** — the kill

```
### detailfree (ref 8445d08c657e73b9f8d9f175814b393bb2b3fbbb)
G2 payload=receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,diff-read=ok,digest-match=1,export-suite=1,run-lines=8,closed-lines=0,distinct-ids=8,closed-line=1,graded-cases=8,ungraded-cases=0,selftest-summary=1,scorecard-ref=1,shonen-ref=1,final-lane-commit=0 closed=1
closed=8/8 exit=0
exit=0
```

The same bytes under the suite's own judge:

```
$ source corpus/instruments/r39-closure.sh; judge_selftest_report $S/a4-receipt.txt
detail lines: 0
judge=REJECT
```

**Accepted by G2, rejected by the suite's judge.** The suite's forged-detail-free fixture only
covers `mutants=0/0`; `mutants=2/2` with no details behind it is not in the forgery set.

### (b) partial `declared-blocks.txt` (undersized tail)

`PROVINCE.md 2 <sha(tail -2)>` replaced by `PROVINCE.md 1 <sha(tail -1)>` (the real append is
2 lines; `git diff --numstat 480b1a50 5006097 -- PROVINCE.md` = `2  0`).

```
G1 payload=declared=2,valid=1,front-doors=0,tail-match=1,pure-append=1,paths=1,province-fence=closed,readme-fence=closed,corrections-outside=0,corrections-inside=0,corrections-declared=1,diff-read=ok closed=0
closed=7/8 exit=1
```

**Rejected** (`valid=1`, `front-doors=0`).

### (c) zero-task dispatch added

`.ufo/waves/round-39/zz-dispatch.json` = `{"wave":"fixture-wave","taskCall":{"tasks":[]}}`
plus `zz-results.json` = `{"wave":"fixture-wave","results":[]}`.

```
G4 payload=dispatches=2,pairs=2,seats-ok=1,zero-task=1,read=ok closed=0
closed=7/8 exit=1
```

**Rejected** (`zero-task=1`).

### (d) pinned r37 bytes changed

1. one appended comment in the export's `corpus/instruments/r37-closure.sh`:

```
G8 payload=pin-ref=2387dcf6...,pinned-sha=1,export-copy=0,r37-copy=1,r37-closed=0,r37-exit=1 closed=0
closed=7/8 exit=1
```

2. the pin **constant** changed (`PIN_R37_SHA=0da98e37…` → `0000…`) in a copy of the suite,
   the mutated suite committed at `corpus/instruments/r39-closure.sh` and the receipt's
   `suite-sha256=` matched to it (so G2's digest limb is green and only the pin is attacked):

```
G2 payload=...,digest-match=1,export-suite=1,... closed=1
G8 payload=pin-ref=2387dcf6...,pinned-sha=0,export-copy=0,r37-copy=1,r37-closed=0,r37-exit=1 closed=0
closed=7/8 exit=1
```

**Rejected** in both forms; the pin constant is load-bearing.

### (e) undeclared appended tail (E5.2 clause)

40 invented lines appended to `corpus/lessons/round-39.md`, `declared-blocks.txt` untouched:

```
G1 payload=declared=2,valid=2,front-doors=2,tail-match=2,pure-append=1,paths=1,province-fence=closed,readme-fence=closed,corrections-outside=0,corrections-inside=0,corrections-declared=1,diff-read=ok closed=1
...
closed=8/8 exit=0
```

**Not rejected.** See K2.

### (f) duplicate earlier `## Round 39` section carrying `Final lane commit:`

`## Round 39 (draft)` with `Final lane commit: deadbeefcafe0000` inserted **before** the real
`## Round 39 result` section:

```
G2 payload=...,final-lane-commit=0 closed=1
G5 payload=round39-section=1,final-lane-commit=0,correction=2,correction-labeled=1 closed=1
closed=8/8 exit=0
```

**Not rejected.** See K6.

---

## 3. Kill findings (8/8 while a defect is still present)

### K1 — G2 accepts a receipt with no execution evidence; the landed receipt is that shape (R3 not closed)

Counterexample: the (a4) fixture above. Landed evidence:

```
$ grep -c '^selftest detail=' .ufo/waves/round-39/final-gates/all-gates.txt      -> 0
$ grep -c '^selftest judge='  .ufo/waves/round-39/final-gates/all-gates.txt      -> 0
$ grep -c '^selftest case='   .ufo/waves/round-39/final-gates/all-gates.txt      -> 8
$ my clean-clone --selftest report: detail=46 judge=7 case=8
$ source r39-closure.sh; judge_selftest_report .ufo/.../all-gates.txt            -> REJECT
```

The suite never prints `run-utc=`, `== run ==` or `== selftest ==` (those strings exist only in
the fixture writer `g2_content`, lines 1150–1154), so the committed receipt is a composed
artifact, not a capture. Its case counts do match a real run exactly
(G1 4/4, G2 8/8, G3 2/2, G4 6/6, G5 4/4, G6 4/4, G7 3/3, G8 3/3) — so the author most likely
did run it and transcribed the case lines — but **G2 cannot tell that apart from a hand-written
block**, which is precisely the R3 defect ("G2 checks shape, not payload truth"). The suite's
own justification for not comparing payload values — "the receipt is the run's own transcript"
(line ~169) — is false for these bytes.

**Impacted axis:** depth:verifiability (G2 limb, R3 closure).
**Smallest safe correction:** apply `judge_selftest_report` to the receipt's selftest block
inside G2 (require per-case `selftest detail=G<i> mutant=…` lines matching the declared
`mutants=n/n`), or commit the raw `--selftest` report beside the receipt and make G2 require
it. This turns the receipt from a summary into execution-backed evidence and rejects (a4) and
the landed receipt as they stand.

### K1b — the receipt defines the judged head and certifies it (circular identity)

In (a4) the receipt's `export-ref=a35cdfee6e0d3fb370e1df48497435243f853a67`, an **empty commit**
on top of Y with the same tree — neither J nor Y — and `git diff --name-only a35cdfe 8445d08`
lists only the receipt, so G2 is green. `claims.json` `judged_head_rule` defines J as "the
`export-ref=` value in all-gates.txt", so the receipt is the sole definer of the head it then
certifies, and G2 accepts any ancestor whose tree differs by at most the receipt. Nothing binds
`export-ref=` to an independently recorded head.

**Impacted axis:** depth:verifiability; duplicate authority (receipt defines and certifies J).
**Smallest safe correction:** require the receipt's `export-ref=` to equal a head named
outside the receipt (e.g. the wave-1 integration commit recorded by hash in the dispatch
results or the SCORECARD judged-head line), or require `export-ref=` to be the **parent** of
the export ref, not an arbitrary tree-equal ancestor.

### K2 — E5.2 "every added tail" is unimplemented; 271 added files are undeclared

E5.2 (frozen erratum, adopted from the freeze audit): "`declared-blocks.txt` must declare BOTH
front doors **and every added tail** (if a file gained lines since base, its declaration must be
present and exact)". G1 as landed requires only the two front doors (`declared>=2`,
`valid==declared`, `doors==2`).

```
$ git diff --numstat 480b1a50 5006097a | awk '$1>0 && $3!="PROVINCE.md" && $3!="corpus/README.md" {n++} END{print n+0}'
271
```

and fixture (e) puts 40 invented lines into `corpus/lessons/round-39.md` and still prints
`closed=8/8 exit=0`. So the suite prints 8/8 while the freeze-audit's own non-vacuity clause is
violated — both at the judged head and under a fresh mutation.

**Impacted axis:** depth:verifiability (G1 scope vs frozen semantics).
**Smallest safe correction:** either implement E5.2 (enumerate `git diff --numstat <base> <ref>`
paths with added>0, minus `declared-blocks.txt` itself and a declared exclusion list, and require
each to be declared exactly), or amend E5.2 to say "both front doors" and drop "every added tail".

### K3 — E5.7's own counting command is red at the judged head (LOG.md = 0)

```
$ cd kasegi-shokunin && grep -c '^Correction (round 39)' corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
corpus/lessons/round-38.md:1
LOG.md:0
SCORECARD.md:2
SHONEN.md:1
```

The LOG.md correction exists as a bullet — `LOG.md:1704: - **Correction (round 39):** …` — but
E5.7 counts line-start matches, so the frozen counter is 0/4 for LOG.md, and none of G1–G8
covers it. `LOG.md:1711` even asserts "`Correction (round 39)` blocks in round-38 lesson, LOG,
SCORECARD, SHONEN", which the frozen counter contradicts.

**Impacted axis:** depth:verifiability (frozen measurement semantics vs records).
**Smallest safe correction:** make the LOG.md correction a line-start paragraph (append-only) so
E5.7's counter reads 1, or change E5.7's pattern to `^[-* ]*Correction \(round 39\)`.

### K4 — E5.1's payload clause is unsatisfiable as worded

E5.1: "every `selftest case=G<n>` line carries `mutants=n/n` (n>=1) **and non-empty `payload=`
fields**". Measured: case lines with `payload=` = **0** in the landed receipt and **0** in a real
`--selftest` run (the suite puts payloads on `selftest detail=` lines). So under E5.1 every case
line, real or forged, is non-compliant, while the suite prints 8/8. The erratum text and the
instrument disagree about where the payload lives.

**Impacted axis:** depth:verifiability (frozen semantics vs instrument).
**Smallest safe correction:** reword E5.1 to "each case line carries `mutants=n/n` with n>=1, and
each of its n mutant detail lines carries a non-empty `payload=`/`limb=` field" (which is what the
instrument and `judge_selftest_report` actually enforce).

### K5 — false provenance: the receipt's `run-utc` post-dates the commit that contains it

```
Y committed:            2026-10-26T17:12:12-03:00  (= 2026-10-26T20:12:12Z)
receipt run-utc:        2026-10-26T21:35:00Z       (+82m48s after the commit)
receipt file mtime:     2026-10-26 17:12:08 -0300
```

A run at 21:35Z cannot have produced bytes committed at 20:12Z. G2 does not parse `run-utc` at
all, so the receipt's only timestamp claim is unchecked and false.

**Impacted axis:** depth:verifiability; false provenance.
**Smallest safe correction:** correct the field to the actual run time (before Y's commit time)
and add a G2 limb `run-utc <= commit time of REF` (cheap, structural), so the field is no longer
decorative.

### K6 — G5/G2 scan only the LAST `## Round 39` section

`md_section` returns the *last* matching level-2 section, so an earlier `## Round 39 (draft)`
section containing `Final lane commit: deadbeefcafe0000` is invisible; fixture (f) prints
`final-lane-commit=0` and `closed=8/8 exit=0`. The label-drift defect is present while its gate
is green.

**Impacted axis:** depth:verifiability (G5 scope).
**Smallest safe correction:** in `md_section`'s two callers, concatenate **all** `^## Round 39`
sections (or fail when more than one exists), so no Round-39 block escapes the scan.

---

## 4. What genuinely holds (so the verdict is not a blanket rejection)

- **G1 exactness for the two declared tails** — non-vacuous:
  `git diff --numstat 480b1a50 5006097 -- PROVINCE.md` = `2  0`, `tail -n 2 PROVINCE.md` sha =
  `fa2dd99f…` (declared); README = `28  0`, `tail -n 28` sha = `a59d42cc…` (declared).
- **Selftest discrimination is real**: 34 mutants across 8 cases, all rejected in a clean
  fixture, with the rejection payload naming the reopened limb; 6 forged reports rejected by
  the judge.
- **Plain-run refusal** exit 2; **base** and **r38-head** reds at 1/8.
- **The named attacks (a1–a3, b, c, d) all fail to go green** — the suite is robust to exactly
  the forgeries the item listed.
- The G2 digest limb genuinely binds the receipt to the executing bytes and to the export copy
  (`git show Y:corpus/instruments/r39-closure.sh | sha256sum` = `2856a210…`).

**R5 scope note.** R5's named sub-defects: "G8 executing the export's own `r37-closure.sh`" is
closed — G8 extracts the bytes from the pin commit, checks the pin digest constant, checks the
export copy digest, *then* runs the pinned file (attempt d2 shows the constant is load-bearing);
"G4 counting seats not identities" is closed (g4_pair reads a distinct identity field and rejects
duplicates, attempts c and the selftest's `duplicate-identity` mutant). The "25 surviving r38
source mutants" list is **not** re-run here: the r39 suite ships 34 of its own mutants, and
whether those cover the specific 25 survivors is a mutation-analysis item (`M2Tool`/
`MutDetailAssert`), outside this seat's counter attack. I do not claim R5 coverage.

The kill is confined to the **receipt/provenance layer** (G2, and the claim's counting
commands), not to the mutant machinery.

---

## 5. Recommendation to the canonical judge

- If `claims.json` alone is authoritative: **reject C1** on its frozen counting command
  (`--export-ref J -> closed=8/8` is 7/8 in the best fixture, 5/8 on the lane; the kill rule
  reads "the judged-head export prints closed != 8/8").
- If E4 governs the ref: **do not hold C1 without the two run conditions** in the claim text
  (`--lane <clean clone at Y>`, `--scratch-root <isolated>`) and without fixing K1 (G2 must
  require detail-backed case lines). As landed, the 8/8 is point-in-time and the receipt it
  certifies is unreproducible-by-judge and detail-free.
- K2/K3/K4 are text-vs-bytes defects in the frozen erratum semantics; each is cheap to fix or
  to reword, but as frozen they are red on the landed bytes.
- K5/K6 are small, local instrument defects (provenance field unchecked; section scoping).

---

## 6. Limits of this measurement

- G6 reds on the real lane **because the seat protocol puts every seat's scratch under the root
  G6 audits**; this is the finding (a verifier cannot be quiescent), not a suite bug.
- G8 reds on the real lane **because wave-2 dispatch files are untracked in the lane**; with a
  clean clone at Y it is green. I did not modify the lane to make it green, and I did not run a
  mutating git command there.
- Fixture commits live only in `$S/lane` (scratch clone), removed before yield.
- No network fetch was made, so no HTTP status/bytes/UTC to report.

**Report:** `.ufo/waves/round-39/wave2/CritC1Kill.md`
