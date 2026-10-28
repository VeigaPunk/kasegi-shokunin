# ExecSuiteSkeleton — r43 C1 `corpus/instruments/r43-closure.sh` (skeleton, K1–K19)

Seat **ExecSuiteSkeleton** (executor, leaf). Lane `kasegi-shokunin`, base
`ab98fac9dce87130bc4f66de89e30650d63943dc`, lane HEAD at wrap `9e6800ea`.

Deliverables sit beside this receipt and were NOT landed by me (the L1 lands
them):

| file | lines | sha256 |
|---|---|---|
| `ExecSuiteSkeleton.r43-closure.sh` (land as `corpus/instruments/r43-closure.sh`) | 2339 | `5a38d32c159c563e369fc18fbd1d80e8da5531686202f4082b2493201b2b1fce` |
| `ExecSuiteSkeleton.usage.txt` (operator + limb-integration note) | 106 | `4ac0e4a5be5e27ee86b596e823cccaede25d76e490074c9497c88125375643d2` |

Self-contained: `bash` + `python3` + coreutils, plus `git`/`tar` for the
export. No network, no write outside `<scratch-root>` / `--receipt-out`, no
mutating git anywhere. Frozen `claims.json` read once, never edited.

## 1. Shape implemented

Forked from `corpus/instruments/r42-closure.sh` (2185 lines) — driver, export
harness, receipt writer, fixed-point selftest runner and K1–K13 bodies carried;
ids renamed `J→K`, sentinel `all-gates v2 → all-gates v3`, `N=19`.

* **Export mode only.** `bash …` prints the two refusal lines and exits 2
  before any mkdir. The tree comes from
  `git -C <lane> archive <resolved> | tar -x -C <work>/export`; `--work` and
  (derived) `--scratch-root` must resolve outside the lane or the run exits 2.
* **Unresolvable ref** → one stdout line `ERROR ref-not-found ref=<tok>
  closed=0 exit=1`, exit 1 (distinct red, never a vacuous tally).
* **Run transcript** (25 lines): `all-gates v3`, `export-ref`, `suite-sha256`
  (the export's copy, `none` when absent), `time-basis=ref-commit`, `run-utc`
  (committer instant of the ref), `K1..K19 payload=… closed=0|1`,
  `closed=<n>/19 exit=0|1`.
* **Receipt** (`--receipt-out`): the 25 printed lines byte-for-byte, then the
  nineteen graded lines and `selftest cases=19 failures=<k>` — 45 lines, one
  unedited tee of one run (measured below).
* **`--selftest`**: nineteen graded lines
  `selftest case=K<n> positive=pass|fail mutants=<ok>/<total> verdict=pass|fail`
  and the summary only. `verdict=pass` requires `positive=pass`, a payload
  identical to the run's line, and a nonempty mutant battery with every mutant
  rejected.
* **`--leaf`** defers K9/K10; **`--only K<n>`** grades one leaf check
  (K1–K7, K11–K19); K8/K9/K10 are aggregates and `--only` refuses them with
  exit 2.

## 2. Measured evidence (all commands run from
`/fast/scratch/hyaku/kasegi-r43/ExecSuiteSkeleton`, removed before yield)

### 2.1 Plain run (export mode only)

```
$ bash r43-closure.sh ; echo exit=$?
r43-closure: a plain run is refused (export mode only)
r43-closure: usage: r43-closure.sh --export-ref <hash> [options]
exit=2
```

### 2.2 Unresolvable ref

```
$ bash r43-closure.sh --export-ref deadbeefdeadbeefdeadbeefdeadbeefdeadbeef ; echo exit=$?
ERROR ref-not-found ref=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef closed=0 exit=1
exit=1
```

### 2.3 Base export `ab98fac9…` — the required after-state (exactly K14–K19 open)

```
$ bash r43-closure.sh --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
      --work $S/w3 --scratch-root $S --receipt-out $S/receipt-base.txt
all-gates v3
export-ref=ab98fac9dce87130bc4f66de89e30650d63943dc
suite-sha256=none
time-basis=ref-commit
run-utc=2026-10-28T16:27:52Z
K1 payload=records=1,blocks=3,graded=1,evidence=3,missing=0,wrong-grade=0,per-record=SCORECARD.md=3/3;LOG.md=0;SHONEN.md=0,union=0,replay=RevC1Counters.md=rejected closed=1
K2 payload=boundary=10/10,truth-tokens=3,stated=4,mangled=0,truth-stated=1,token=whole,replay=RevC1Counters.defeats.txt=rejected closed=1
K3 payload=tables=18,rows=73,r42-rows=1,r40-rows=1,r40-split=0,bare=0,lead=0,replay=MutSkillTablePipes.md=3/3 closed=1
K4 payload=declared=469,valid=469,missing=0,escape=0,coverage=11/11,file=present,replay=CritDeclarationCoverage.md=2/2 closed=1
K5 payload=family=kasegi-r4[0-9]*,strays=8,scanned=8,read=ok,outside=2,outside-scanned=10,scope=materialized,replay=MutScratchTiming.md=outside=detected,inside=detected closed=1
K6 payload=instrument=present,base=1,missing-path=1,url-mutated=1,digest-mutated=1,rule=reject,replay=MutBindingExistence.md=rejected closed=1
K7 payload=instrument=present,base=1,status-flip=1,no-pass=1,rows=25,admitted=25,replay=MutFrontierParser.md=rejected closed=1
K8 payload=receipt=(canonical),source=canonical,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=18/18,forged=6/6 closed=1
K9 payload=depth=1,base=1,r41=1,accept=tree-red,cap=nested closed=1
K10 payload=cases=19,isolated=19,canary=0,graded-lines=19,fixture=synthetic closed=1
K11 payload=corrections=34,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1
K12 payload=deleted=0,density=1,density-sha=ee803726a322,diff-read=ok,base=5053a7f4 closed=1
K13 payload=faithful=1,extra=0,missing=0,scratch-strays=0,scratch-read=ok,markers=0,named=1 closed=1
K14 payload=stub closed=0
K15 payload=stub closed=0
K16 payload=stub closed=0
K17 payload=stub closed=0
K18 payload=stub closed=0
K19 payload=stub closed=0
closed=13/19 exit=1
```

Wall time 4m19s (K9's two nested exports dominate). K1–K7 replay limbs all
reported `rejected` against their digest-pinned committed defeats; K8 graded a
canonical transcript because no round-43 receipt exists at base.

### 2.4 Selftest at base — nineteen graded lines, six honest stub failures

```
$ bash r43-closure.sh --selftest --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
      --work $S/w2 --scratch-root $S ; echo exit=$?
selftest case=K1 positive=pass mutants=1/1 verdict=pass
selftest case=K2 positive=pass mutants=1/1 verdict=pass
selftest case=K3 positive=pass mutants=3/3 verdict=pass
selftest case=K4 positive=pass mutants=2/2 verdict=pass
selftest case=K5 positive=pass mutants=2/2 verdict=pass
selftest case=K6 positive=pass mutants=2/2 verdict=pass
selftest case=K7 positive=pass mutants=2/2 verdict=pass
selftest case=K8 positive=pass mutants=6/6 verdict=pass
selftest case=K9 positive=pass mutants=3/3 verdict=pass
selftest case=K10 positive=pass mutants=2/2 verdict=pass
selftest case=K11 positive=pass mutants=1/1 verdict=pass
selftest case=K12 positive=pass mutants=2/2 verdict=pass
selftest case=K13 positive=pass mutants=2/2 verdict=pass
selftest case=K14 positive=fail mutants=0/0 verdict=fail
selftest case=K15 positive=fail mutants=0/0 verdict=fail
selftest case=K16 positive=fail mutants=0/0 verdict=fail
selftest case=K17 positive=fail mutants=0/0 verdict=fail
selftest case=K18 positive=fail mutants=0/0 verdict=fail
selftest case=K19 positive=fail mutants=0/0 verdict=fail
selftest cases=19 failures=6
exit=1
```

The six `verdict=fail` lines are the **stubs** (`positive=fail`, `mutants=0/0`):
they are honest reports that K14–K19 do not exist yet, NOT evidence that the
new checks can see their defects. The suite therefore cannot print
`closed=19/19` or `selftest cases=19 failures=0` until the six limb bodies
land — no green claim is made here.

### 2.5 Receipt is one unedited tee

```
$ wc -l receipt-base.txt            -> 45
$ head -25 receipt-base.txt | diff - tee-stdout.txt   -> (no output) IDENTICAL
$ tail -20 receipt-base.txt | diff - selftest-base.txt -> (no output) IDENTICAL
```

45 = 5 header + 19 payload + `closed` + 19 graded + summary, and the first 25
lines are the bytes the run printed.

### 2.6 Round-41 judged head `1f74646…` — red, as required

```
$ bash r43-closure.sh --export-ref 1f7464612ac4c44e39886b82e812610d3c039b13 \
      --work $S/w4 --scratch-root $S ; echo exit=$?
closed=5/19 exit=1
```
Closed there: K5, K8, K9, K10, K13. Open: K1–K4, K6, K7, K11, K12, K14–K19.

### 2.7 `--only`, aggregate refusal, lane guard

```
$ bash r43-closure.sh --export-ref ab98fac9… --only K8
r43-closure: --only cannot isolate aggregate check K8            exit=2
$ bash r43-closure.sh --export-ref ab98fac9… --work $S/w5 --scratch-root $S --only K14
… (5 header lines) …
K14 payload=stub closed=0
only=K14 closed=0/1 exit=1
$ … --only K5
K5 payload=family=kasegi-r4[0-9]*,strays=8,…,replay=MutScratchTiming.md=outside=detected,inside=detected closed=1
only=K5 closed=1/1 exit=0
$ … --selftest … --only K14
selftest case=K14 positive=fail mutants=0/0 verdict=fail
selftest cases=1 failures=1                                       exit=1
$ bash r43-closure.sh --export-ref ab98fac9… --work /…/kasegi-shokunin/x --scratch-root $S
r43-closure: the export work tree must lie outside the lane (…)   exit=2
```

## 3. K1–K13: what is carried and the four deliberate deltas

Bodies are the r42 bodies with ids renamed; payload cell names, replay
polarity, digest-pinned defeat artifacts and thresholds are unchanged
(K1 `RevC1Counters.md`, K2 `RevC1Counters.defeats.txt`, K3
`MutSkillTablePipes.md`, K4 `CritDeclarationCoverage.md`,
K5 `MutScratchTiming.md`, K6 `MutBindingExistence.md`,
K7 `MutFrontierParser.md`). Deltas, each forced and each stated in the file:

1. **K8's subject moves to `.ufo/waves/round-43/final-gates/all-gates.txt`.**
   Keeping the round-42 receipt path makes K8 unclosable at any later ref
   (`diff` = every round-43 path) and would make the claim's 19/19 unattainable.
2. **K8 `digest` accepts `none`** when the suite is absent from the graded tree
   (base predates it); a committed receipt must still name the export's bytes.
3. **K8 `closed-line`** is strict `(19,19,0)` for a committed receipt and
   "the summary equals what its own payload lines imply" for the canonical
   probe (no receipt committed). The probe cannot claim 19/19 at base.
4. **K9's dependent-red set** gains K14–K19: at base the only tree-dependent
   reds ARE K14–K19, so the carried set `(K1,K2,K3,K4,K8,K11)` would see zero
   dependent reds and reject the control. `neg_accept` still requires exit≠0,
   tally<19 and ≥2 dependent reds.

`ROUND` stays 42, `DECLARED_REL` stays round-42, `BASE_REF`/`DENSITY_SHA` stay
pinned: K1–K13 grade the round-42 closure the r42 suite certified. A round-43
`corrections=` block, a round-43 declared-blocks file and an r43 registry row
are **not** part of frozen C1; pointing K4 at a round-43 declaration would make
C1 unsatisfiable.

## 4. K14–K19: the limb seam

Each slot is `def check_k<n>(_tree) -> (payload, ok)` returning `("stub", False)`
today, with `LIMB_CHECKS`, `LIMB_SLOTS`, `SELFTEST_SPECS` and `DETERMINISTIC`
already wired; a limb replaces the body and `limb_mutants(_check_id, _root) ->
(rejected, built)` and nothing else. Payloads must be ref-invariant (no ref,
host path or clock) because K8 re-derives all 18 deterministic payloads at the
receipt's ref and requires exact equality (`payload-match=18/18`). Labels
reserved: K14 correction-literal, K15 wave-dispatch-narrative, K16
placeholder-promise, K17 claims-before-literal, K18 quoted-closed-values, K19
freeze-record-order.

## 5. Defect found and fixed during the wave

Peer reviewer **RevSuiteContract-2** measured that the K8 selftest case still
built the r42 synthetic line (`… mutants=1/1 positive=pass payload-match=1 …`)
while `SELFTEST_RX` was already the new grammar, so its canonical parse failed,
`forged=5/6`, and K8 could never pass. Fixed by making one producer
`canonical_selftest_lines()` used by both `check_k8` and the K8 case (the two
copies are what drifted). Re-measured: `selftest case=K8 … mutants=6/6
verdict=pass` in §2.4.

## 6. Decisions where the peer contract and the seat contract disagree

* **Selftest field order.** `ScoutInstrumentInventory.md` asks for r42's
  `mutants=… positive=… payload-match=… verdict=…`; this seat's dispatch
  specifies `selftest case=K<n> positive=… mutants=<a>/<b> verdict=…`. Frozen
  C1 uses an ellipsis (`selftest case=K<n> … positive=pass … verdict=pass`), so
  both comply. The seat contract was followed; payload-match is enforced inside
  the verdict instead of printed.
* **No literal `/tmp` fallback.** r42's `SCRATCH_ROOT="${TMPDIR:-/tmp}"` is
  gone: the scratch root is the parent of `--work`, else `$TMPDIR`, else exit 2.
* **`--only`** is an addition (not in r42 or the scout contract); it changes no
  counting command and refuses the aggregate checks.
* **Round-42 subject matter** for K1–K13, with the reasons in §3.

## 7. Risks / what the L1 must do to reach 19/19

1. **The skeleton is red at Y too** until the six limb bodies land: K14–K19
   stub-open and K8 red (the committed receipt cannot say 19/19 / 19 passes).
   Landing order: merge limbs → commit as J → `--export-ref J --receipt-out
   .ufo/waves/round-43/final-gates/all-gates.txt` (must print 19/19) → commit
   the receipt as Y.
2. **K3 is registry-strict**: exactly one `r42-closure.sh` row and one
   `r40-closure.sh` row in `SKILL.md`, all rows pipe-leading and cell-complete.
   A new `r43-closure.sh` row must sit inside a table, not split out by a blank
   line, or K3 goes red.
3. **K12 fails on any tracked deletion under `corpus/`** between `5053a7f4` and
   Y, and on any change to `density.py`.
4. **K4 reads the round-42 declared-blocks file**; every path it declares must
   still exist at Y.
5. **K9 costs two nested exports** (~4 min total run). `--only` is the cheap
   loop for limb development.
6. **A limb that returns `ok` without building a mutant now fails** its case
   (nonempty battery required), by design.

## 8. Hygiene

No tool installed or upgraded, no network fetch, no pacman, no mutating
git/jj anywhere; only read-only git (`rev-parse`, `cat-file`, `archive`,
`merge-base`, `diff`, `ls-tree`, `log`, `status`) and one throwaway fixture
repo inside the suite's own scratch. Lane writes: the two untracked files above
under `.ufo/waves/round-43/w1/` plus this receipt. Scratch
`/fast/scratch/hyaku/kasegi-r43/ExecSuiteSkeleton` removed before yield.
