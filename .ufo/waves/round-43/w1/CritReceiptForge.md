# CritReceiptForge — forged round-43 receipts against the receipt validator

Axes: depth:verifiability (primary), coverage. Receipt-only item: forge the round-43 receipt
(extra payload line, plausible-but-unprinted payload value, second `all-gates` header, summary
contradicting the payload lines, `run-utc` after the commit, receipt for a different ref with
the same suite digest, selftest block copied from another round), run each against the receipt
validator, record accept/reject with the failing token.

Read before writing: `.ufo/waves/round-43/claims.json` (frozen; never edited),
`.ufo/waves/round-42/claims.json`, `corpus/instruments/r42-closure.sh` (read whole: header,
argument parsing, export harness, receipt writer, selftest runner, J8), the committed round-42
receipt `.ufo/waves/round-42/final-gates/all-gates.txt`, `corpus/lessons/round-42*.md`,
`.ufo/waves/round-43/w1/` (landed sibling deliverables: ExecK16Placeholder.sh,
ExecK19Freeze.sh + transcripts).

## 1. What "the receipt validator" is here — and what did not exist

There is no round-43 receipt reader at the freeze commit `4cb6d4a`:
`git cat-file -e 4cb6d4a:corpus/instruments/r43-closure.sh` fails (the file does not exist at
any ref), and the wave-1 suite deliverable (`ExecSuiteSkeleton.r43-closure.sh`) and the receipt
grammar deliverable (`ExecNegCtlReceipt.spec.txt`) had not landed in
`.ufo/waves/round-43/w1/` while this ran (`ls .ufo/waves/round-43/w1/` shows neither).

The only committed receipt validator is J8 of `corpus/instruments/r42-closure.sh`, and the frozen
C1 predicate carries it into K8 ("K1-K13 keep the r42 J1-J13 payload grammar and their replay
limbs"). It was therefore graded against, in two forms:

- **Instrument A — the reader, retargeted.** The python engine is extracted byte-exactly with
  `sed -n '107,2184p' corpus/instruments/r42-closure.sh > r42_engine.py`
  (sha256 `2ef5441937c35b32265a4b70f5745ace6402994cf43be903a07770b6e82e51ff`, 2078 lines,
  `ast.parse` ok) and imported unchanged. Only the id namespace moves: `CHECK_IDS`
  `J1..J13 -> K1..K19`, `RECEIPT_LINE_RX`/`SELFTEST_RX` `J`->`K`, and the two id literals inside
  `forgery_verdicts` (`"J1 payload="`->`"K1 payload="`, `"J5 payload="`->`"K5 payload="`). The
  fact ledger is `check_j8`'s `add()` sequence, in order, with N=19 and
  `DETERMINISTIC = every K id except K8` (r42 excludes J8, `r42-closure.sh:127-130`).
- **Instrument B — the committed code, unmodified.** `insitu_j8.py` sets
  `E.EXPORT` to an export of `b2c49ea` (the commit that carries the committed r42 receipt),
  `E.REF = b2c49ea`, lane = the real lane, and calls `E.check_j8(...)` — J ids, real
  `ref_utc`/`merge-base`/`diff`, real suite bytes for the digest, no retargeting at all.

**Calibration** (A on the real committed receipt, ref `4c40ef2`):

```
$ ./validate_receipt.py .ufo/waves/round-42/final-gates/all-gates.txt --prefix J --count 13 \
    --grade-ref 4c40ef21cced6ebed592e5622996ab41996e2da9 --expect cases/expected-r42.json
all-gates.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=12/12 forged=6/6 verdict=ACCEPT failing=none
```

and B on the same receipt/export:

```
### committed check_j8 (r42-closure.sh:1531-1645, unmodified) on an export of b2c49ea
control: real committed receipt    all-gates.txt  ok=True receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
```

A full end-to-end run of the committed suite at `b2c49ea` agrees (3m45s):

```
$ bash corpus/instruments/r42-closure.sh --export-ref b2c49ea5e7bc214e91c2b0bede5d4eaed4968572 \
    --work $S/run-ctrl/w --scratch-root $S/run-ctrl
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6 closed=1
closed=13/13 exit=0
```

So A reproduces B on the accept path, and B reproduces the suite's own J8 on the real receipt.
The forged receipts are round-43 shaped: 19 `K<n> payload=... closed=0|1` lines, `closed=19/19
exit=0`, nineteen selftest lines, `selftest cases=19 failures=0`, 45 lines. `K1..K13` payloads
and `K1..K13` selftest lines are the committed round-42 values with the id mapped J->K;
`K16`/`K19` payload grammar is copied from the landed r43 limbs
(`sections=...,promises=...,fenced=...,unresolved=...`; `freeze=...,order=...,sha=...`);
`K14/K15/K17/K18` carry shape fixtures in their declared grammar and assert nothing about the
round's state.

## 2. The genuine fixture and its control

```
$ python3 build_cases.py
00-control-genuine.txt             lines=45
01-extra-payload-line.txt          lines=46
01b-extra-payload-K20.txt          lines=46
01c-swapped-payload-id.txt         lines=45
02-payload-unprinted-value.txt     lines=45
02b-payload-unprinted-value-K8.txt lines=45
03-second-header.txt               lines=46
04-summary-contradicts.txt         lines=45
04b-summary-vs-closed-payload.txt  lines=45
05-run-utc-after-commit.txt        lines=45
06-different-ref-same-digest.txt   lines=45
07-selftest-from-r42.txt           lines=39
07b-selftest-relabelled-padded.txt lines=45
```

Base: `export-ref=4cb6d4ae768481e1a14afbedc2d865a060ebacfd`,
`suite-sha256=fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b` (the real digest
of `corpus/instruments/r42-closure.sh` at the ref — byte-identical at `ab98fac9`, `4c40ef2` and
`4cb6d4a`, which is what makes attack 6 live), `run-utc=2026-10-28T16:37:11Z` (`ref_utc(4cb6d4a)`).
Control under the carried ledger: **ACCEPT**, `payload-match=18/18`, `forged=6/6`, every fact 1.

## 3. The seven forgeries, graded by the carried ledger (A)

Grading ref `4cb6d4a`; expected payload map = the control's own values. Command per case:

```
$ ./validate_receipt.py <case> --prefix K --count 19 \
    --grade-ref 4cb6d4ae768481e1a14afbedc2d865a060ebacfd --expect cases/expected.json
```

| # | attack | bytes changed | verdict | failing token(s) |
|---|---|---|---|---|
| 1 | extra payload line | duplicate `K5 payload=... closed=1` after `K5` (46 lines) | REJECT | `lines` |
| 1b | extra payload line, foreign id | `K20 payload=extra=1 closed=1` after `K19` | REJECT | `lines`, `run-lines` |
| 1c | extra payload line, id swapped | `K1` line overwrites `K7` (19 ids -> 18) | REJECT | `run-lines`, `payload-match` |
| 2 | plausible but unprinted value | `K11 ... corrections=34` -> `corrections=33` (the exact stale literal RD42-1 mines) | REJECT | `payload-match` (17/18) |
| 2b | plausible but unprinted value, K8 | `K8 payload=... forged=6/6` -> `forged=7/7` | **ACCEPT** | none — **defect D1** |
| 3 | second `all-gates` header | `all-gates v2` inserted after line 0 | REJECT | `lines`, `no-stray` |
| 4 | summary contradicts the payload lines | `selftest cases=19 failures=0` -> `cases=18` | REJECT | `summary` |
| 4b | summary clean, a payload line contradicts it | `K7 ... closed=1` -> `closed=0`, summary untouched | REJECT | `payload-match` (17/18) |
| 5 | `run-utc` after the commit | `run-utc=2026-10-28T16:47:11Z` (+10 min over `ref_utc(4cb6d4a)`) | REJECT | `utc` |
| 6 | receipt for a different ref, same suite digest | `export-ref=ab98fac9...`, `run-utc=2026-10-28T16:27:52Z`, payloads unchanged | REJECT | `diff` (9 files `ab98fac9..4cb6d4a`); **ACCEPT when the grader adopts the claim's own ref** (see §5) |
| 7 | selftest block copied from another round | the committed round-42 `J1..J13` selftest lines verbatim (39 lines) | REJECT | `lines`, `selftest-lines`, `verdicts`, `no-stray`, `forged` (5/6) |
| 7b | same, relabelled J->K and padded to 19 | thirteen r42 lines relabelled + six `mutants=1/1` pads | **ACCEPT** | none — **defect D2** |

Raw output of the whole ledger-A matrix (`matrixA.txt`):

```
00-control-genuine.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=ACCEPT failing=none
rc=0
01-extra-payload-line.txt facts=sentinel=1,lines=0,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=REJECT failing=lines
rc=1
01b-extra-payload-K20.txt facts=sentinel=1,lines=0,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=0,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=REJECT failing=lines,run-lines
rc=1
01c-swapped-payload-id.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=0,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=0,forged=1 payload-match=17/18 forged=6/6 verdict=REJECT failing=run-lines,payload-match
rc=1
02-payload-unprinted-value.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=0,forged=1 payload-match=17/18 forged=6/6 verdict=REJECT failing=payload-match
rc=1
02b-payload-unprinted-value-K8.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=ACCEPT failing=none
rc=0
03-second-header.txt facts=sentinel=1,lines=0,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=0,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=REJECT failing=lines,no-stray
rc=1
04-summary-contradicts.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=0,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=REJECT failing=summary
rc=1
04b-summary-vs-closed-payload.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=0,forged=1 payload-match=17/18 forged=6/6 verdict=REJECT failing=payload-match
rc=1
05-run-utc-after-commit.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=0,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=REJECT failing=utc
rc=1
06-different-ref-same-digest.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=0,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=REJECT failing=diff
rc=1
07-selftest-from-r42.txt facts=sentinel=1,lines=0,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=0,verdicts=0,summary=1,closed-line=1,no-stray=0,payload-match=1,forged=0 payload-match=18/18 forged=5/6 verdict=REJECT failing=lines,selftest-lines,verdicts,no-stray,forged
rc=1
07b-selftest-relabelled-padded.txt facts=sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1 payload-match=18/18 forged=6/6 verdict=ACCEPT failing=none
rc=0
```

## 4. The same attacks against the committed code, unmodified (B)

Export of `b2c49ea` (tree = the r42 final tree + the committed receipt); payload truth held at
the pristine receipt's re-derived values (the tree under test is unchanged by an edit to the
receipt file; no check but J8 reads it). Command: `./insitu_run.sh`.

```
### committed check_j8 (r42-closure.sh:1531-1645, unmodified) on an export of b2c49ea
### payload truth = the pristine receipt's re-derived payloads (held fixed)
control: real committed receipt    all-gates.txt                ok=True receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=0
forged J8 own payload (7/7)        all-gates.txt                ok=True receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=0
forged J11 payload (corrections=33) all-gates.txt                ok=False receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=0,forged=1,payload-match=11/12,forged=6/6
rc=1
duplicate J5 payload line          all-gates.txt                ok=False receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=0,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=1
second all-gates header            all-gates.txt                ok=False receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=0,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=0,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=1
summary cases=12                   all-gates.txt                ok=False receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=0,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=1
run-utc +10min                     all-gates.txt                ok=False receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=0,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=1
ref ab98fac9, same suite digest    all-gates.txt                ok=False receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=0,diff=0,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=1
selftest block relabelled 1/1      all-gates.txt                ok=True receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=0
control after restore              all-gates.txt                ok=True receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6
rc=0
```

Verbatim `insitu.txt`; the restored control brackets the sweep, so the mutation is the only
variable. Verdicts agree with A on every class: six of the seven attack classes are rejected on
every variant; **the `J8`-payload forgery and the relabelled selftest block are accepted by the
committed code**.

## 5. Attack 6 in detail — what it does and does not prove

`suite-sha256` is byte-identical at `ab98fac9`, `4c40ef2`, `4cb6d4a`, `b2c49ea` (all
`fca5ae62...`), so a receipt can be re-aimed at another ref without touching its digest. What
catches it is `diff`: the claimed ref must be an ancestor of the grading ref and the trees may
differ in at most the receipt file. Graded at `4cb6d4a`, `ab98fac9` is 9 files away -> REJECT.
In situ, `ab98fac9` is a *descendant* of `b2c49ea`, so `ancestor=0` and `diff=0` -> REJECT.

The hole is narrower but real: if the grader adopts the ref the receipt names (no external Y),
the same bytes are **ACCEPTED** (`--grade-ref ab98fac9...` -> all 16 facts 1). The r42 design
accepts this on purpose — a receipt minted at J is graded at Y with `Y\J = {receipt}` — but the
consequence must not be over-claimed: **the validator proves the receipt is *consistent with* a
ref, not that a run happened at it.** Two edits (`export-ref`, `run-utc`) re-aim a receipt at
any ancestor whose bytes are the same minus the receipt, and nothing in the receipt can tell.
That is a wording constraint on C1's "one unedited tee of one run", not (by itself) a check
defect: the suite always grades at its own REF.

## 6. Two defects in the carried K8, with the smallest safe correction

**D1 — K8's own payload is unbound.** `DETERMINISTIC` excludes the receipt check itself
(`r42-closure.sh:127-130` excludes J8), so `payload-match` iterates 18 of 19 ids: a plausible,
never-printed value inside the `K8 payload=` line is accepted by both A and the committed B.
Real-world form: edit `forged=6/6` (or any fact token) in the receipt's K8 line and the receipt
still greens, including in situ. The recomputation used for comparison is the *re-derived*
payload string, which does not read the recorded K8 line — there is no true circularity; only
the self-count token needs masking.
Smallest safe correction: include K8 in the payload comparison with its own
`payload-match=<n>/<m>` token masked (or compared against the fixed 19/19).

**D2 — the selftest block is shape-checked, not content-bound.** `check_j8` checks the count,
that every verdict is `pass`, and the summary; it never compares a case's `mutants=<n>/<m>` to
the case list the selftest runner actually executed. A block relabelled from another round and
padded to nineteen lines is accepted by A and by the committed B (`selftest block relabelled
1/1` -> ok=True), even though the real per-case counts are `1/1,1/1,3/3,2/2,...,6/6,3/3,2/2` and
the round-43 spec requires at least `2/2` for each of K14-K19.
Smallest safe correction: one `selftest-mutants` fact — compare each parsed
`mutants=<n>/<m>` to the declared case list (`ExecSelftest19.cases.txt`).

**Proof both corrections close the holes without trapping the honest receipt** (ledger B: same
reader, `--det-all` + `cases/declared-mutants.json`):

```
00-control-genuine.txt facts=...payload-match=1,selftest-mutants=1,forged=1 payload-match=19/19 forged=6/6 verdict=ACCEPT failing=none
02b-payload-unprinted-value-K8.txt facts=...payload-match=0,selftest-mutants=1,forged=1 payload-match=18/19 forged=6/6 verdict=REJECT failing=payload-match
07b-selftest-relabelled-padded.txt facts=...payload-match=1,selftest-mutants=0,forged=1 payload-match=19/19 forged=6/6 verdict=REJECT failing=selftest-mutants
```

Control stays green; both survivors go red with exactly their own fact. `declared-mutants.json`
uses the committed round-42 counts for K1-K13 and `2/2` for K14-K19 from the ExecSelftest19
spec ("a positive case ... and a mutant built from the COMMITTED r42 defeat bytes").

Two corollaries for whoever lands the r43 suite:
1. **Do not let the exclusion set grow.** Every id outside `DETERMINISTIC` is a forgeable
   payload. K9 (negative controls) must stay in the set, or its payload must be bound to a
   committed transcript, or the same D1 hole opens on K9.
2. **`closed=19/19 exit=0` is a text check.** `closed-line` compares the line's three numbers,
   not the count of `closed=1` payload lines. Today the payload comparison catches a flipped
   flag (04b), but only for ids inside `DETERMINISTIC`; once an id leaves the set, a
   `closed=0` line under a `closed=19/19` header is accepted. A one-line `closed-count` fact
   (`sum(payload closed)==19`) closes it for all nineteen.

## 7. Verdict on the seven named attacks

| attack | verdict on every variant | token |
|---|---|---|
| extra payload line | REJECT (3/3 variants) | `lines` / `run-lines` / `payload-match` |
| plausible but unprinted value | REJECT for every deterministic id; **ACCEPT for K8** | `payload-match` / *none* |
| second `all-gates` header | REJECT | `lines`, `no-stray` |
| summary contradicts payloads | REJECT (both directions) | `summary` / `payload-match` |
| `run-utc` after the commit | REJECT | `utc` |
| different ref, same digest | REJECT at an anchored grader; ACCEPT when self-anchored | `diff` / *none* |
| selftest block from another round | REJECT when copied verbatim; **ACCEPT when relabelled** | `selftest-lines`,... / *none* |

No attack in this set defeated the reader's structural grammar: the sentinel, line count,
payload count, selftest count, verdict, summary, closed line, stray line, ref, digest,
time-basis, commit time, ancestry and diff facts all held. The two survivors are both
*content-binding* holes (D1, D2), which is exactly the class round 43 exists to close: a record
that names a value the counter never re-derives is still invisible to the counter.

## 8. Evidence inventory

```
$ sha256sum r42_engine.py
2ef5441937c35b32265a4b70f5745ace6402994cf43be903a07770b6e82e51ff  r42_engine.py   (2078 lines, sed 107,2184p)
$ sha256sum validate_receipt.py build_cases.py
138bf4c017ab6053f3252fff33354d4c6d5834c879cde4c1344c2fb74aeb661c  validate_receipt.py
e47a7a642d4bc3f5e02383ebf9eee484a26c71341792889eab70fb14e2f4eb30  build_cases.py
$ sha256sum cases/*.txt   (line counts from build_cases.py)
5b28ddd1e2f20e99…  45  00-control-genuine.txt
6be83a2c880e2bc8…  46  01-extra-payload-line.txt
4e690afdfd6f7470…  46  01b-extra-payload-K20.txt
6bcb9302632a8d35…  45  01c-swapped-payload-id.txt
38a24104fc381048…  45  02-payload-unprinted-value.txt
8c012fcc91cdf075…  45  02b-payload-unprinted-value-K8.txt
a25b7c4e46e2ee9a…  46  03-second-header.txt
4cc34d4532841d51…  45  04-summary-contradicts.txt
1b812ca123a2db43…  45  04b-summary-vs-closed-payload.txt
c895351da2fb5e58…  45  05-run-utc-after-commit.txt
adf65ac9f1197356…  45  06-different-ref-same-digest.txt
91a2161362a1e166…  39  07-selftest-from-r42.txt
7e47beb1794d1d26…  45  07b-selftest-relabelled-padded.txt
```

Commands actually run (all in `$S=/fast/scratch/hyaku/kasegi-r43/CritReceiptForge`):

1. `sed -n '107,2184p' <lane>/corpus/instruments/r42-closure.sh > r42_engine.py` -> 2078 lines,
   sha256 above; `python3 -c "import ast;ast.parse(...)"` -> `parse-ok`.
2. Calibration (J/13) -> `ACCEPT failing=none`, `payload-match=12/12 forged=6/6`.
3. `python3 build_cases.py` -> 13 receipts, 39-46 lines each.
4. `for f in cases/0*.txt; do ./validate_receipt.py "$f" --prefix K --count 19
   --grade-ref 4cb6d4a... --expect cases/expected.json; done` -> matrix in §3.
5. Same three cases with `--det-all --cases cases/declared-mutants.json` -> matrix in §6.
6. `git -C <lane> archive b2c49ea | tar -x -C insitu/export`; `./insitu_run.sh` -> §4.
7. `bash <lane>/corpus/instruments/r42-closure.sh --export-ref b2c49ea --work … --scratch-root …`
   -> `closed=13/13 exit=0`, `J8 … source=committed … closed=1` (3m45s).
8. Fixture git repo used for an early in-situ attempt (a scratch `git init` with
   `rev-parse --show-toplevel` verified equal to the fixture dir; no lane or fleet mutation);
   superseded by §4's export-based driver and removed with the scratch tree.

**Tooling:** none installed or upgraded (no `pacman`, no `uv`, no `npx`; `~/.omp/agent/*`
untouched). **Scratch:** `$S` created with `mkdir -p` under `/fast/scratch/hyaku/kasegi-r43/`
and removed after this receipt was written; `/tmp` unused. **Network:** none used (no HTTP
fetch this seat).
