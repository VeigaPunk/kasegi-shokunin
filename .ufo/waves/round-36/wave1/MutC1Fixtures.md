# MutC1Fixtures — fixture flip matrix + vacuousness probes, round-36 C1 fixture corpus

Round 36, wave 1, seat `MutC1Fixtures` (mutation-tester, leaf — no subagents). Item: mutation-test
the fixtures from ExecC1Fixtures — flip each red fixture to green (fix the defect) and confirm the
check then passes; flip a green to red and confirm it fails; add a vacuous fixture (asserting
nothing) and confirm it is detected as vacuous. Judged axis: depth:verifiability.

## Verdict

**66/66 matrix rows met — 0 fixture-level survivors; 1 judge-level survivor (vacuous report
accepted).** The fixture corpus discriminates in both directions under both detector drafts:

- **Detector A** (ExecC1Fixtures' own draft, sha256 `4283a9d3…`, 308 lines): 32/32 met — green
  9/9; all 11 red fixtures (E1–E9 + E4b + E9b) read `closed=8/9 exit=1` with **only their own
  check open**; all 11 red→green flips read `closed=9/9 exit=0`; all 9 independent green→red
  injections read `closed=8/9 exit=1` with only the injected check open.
- **Detector B** (ExecC1SuiteBuild's FROZEN draft, sha256 `76273416…`, 817 lines, 34631 bytes,
  `bash -n` clean): 34/34 met — green 9/9; pristine reds 11/11 own-open; flips 11/11 → 9/9;
  independent injections: E1/E2/E3/E7/E9 own-open, **E4/E5/E6/E8 read closed (measured A/B
  strength divergence, §5)**; B-native E8a/E8b both open E8.
- **Vacuous fixture**: green bytes labelled as a red case (no defect) read `own_open=0` under
  both detectors → **detected as vacuous** by the matrix rule (a red case must have
  `own_open=1`). At the suite level, a vacuous 10th case line is rejected by the frozen judge
  (`cases==9` bound) — but a **detail-free all-pass caseline report is ACCEPTED by the frozen
  judge** (survivor, §6).
- The four A/B strength divergences and the judge survivor are **coverage findings, not
  permissions to change the contract**; they are reported for the L1's landing decision.

## 1. Pins

| artifact | sha256 | notes |
|---|---|---|
| suite-A (ExecC1Fixtures' draft) | `4283a9d3eae810e03ddc6181e4c7a11de491e0fdd4f8f554ce7c1fbc947c03e5` | 308 lines; stable across the whole seat; matches their receipt line 19 |
| suite-B frozen (ExecC1SuiteBuild) | `76273416f7a6668a702eadf5a6c03b80ae87ad4793f652880303fcb7f8230323` | 817 lines / 34631 B; `bash -n` exit 0; re-hashed EQUAL at seat end |
| fixture generator v2 | `20de0cb39b2d3036b5f34ce2ca61ab8f8a48d7c4f47f37e013897d05e234801b` | pinned from ExecC1Fixtures before their yield; receipt-embedded there |
| src snapshot | unchanged across my two pins (`diff -r` empty) | pruned `git archive b47f2cd`, normalised |
| fx2/green | HEAD=`0ef3a50a5759243208fa5d818112bb19db4eb5bd` BASE=`d540b7cfd38c6c52b2745854e6b888cc16764c3a` | deterministic regen (fixed GIT_*_DATE) reproduces ExecC1Fixtures' cited shas exactly |

fx2 red HEADs (all BASE=`d540b7cf…`): E1 `6216b2f1` E2 `b3e595a9` E3 `1606d0cc` E4 `4dd0a828`
E5 `44e02390` E6 `5c8af556` E7 `9d0d6936` E8 `4b1d452d` E9 `0ef3a50a` (defect uncommitted —
dirtiness IS the defect) E4b `81a637c7` (index drop) E9b `0ef3a50a` (stray dir lives under the
scratch root, not the repo).

## 2. Method

- **Isolated copies only.** Every fixture repo and both suite drafts were copied into
  `/fast/scratch/hyaku/kasegi-r36/MutC1Fixtures/` (pinned by digest) before any mutation. The
  siblings' scratch trees were never written; ExecC1Fixtures' scratch was removed at their yield
  (their receipt embeds the generator verbatim, so the corpus is reproducible from my pins).
- **Corpus regeneration.** Because the corpus was amended mid-flight (§7), I regenerated the
  full set (`fx2/`) with the pinned generator v2 + pinned src: `green`, `red-E1..E9`, `red-E4b`
  (green + `untrack .ufo/waves/round-35/wave1-results.json`), `red-E9b` (clean green). The
  regeneration reproduced ExecC1Fixtures' cited green shas byte-for-byte (deterministic dates),
  so the matrix ran on exactly the corpus their receipt cites.
- **Detectors.** A: `KASEGI_SCRATCH=<mine> KASEGI_R36_SCRATCH=<empty|stray> bash suite-A.sh
  --root <repo> --gitroot <repo>`. B: `bash suite-B-frozen.sh --export-ref <repo-HEAD> --lane
  <repo> --scratch-root <empty|stray> --work <mktemp under my scratch>` (work dir removed after
  each run; B clears `export/`+`mut/` inside it before use). The suite's own per-check lines +
  `closed=K/9 exit=E` + exit code are the only detector; nothing was re-implemented.
- **Git hygiene.** Every `git add`/`commit` ran only inside a `mktemp -d` copy under my scratch
  after verifying `git rev-parse --show-toplevel` equals the copy's realpath; every mutated tree
  was re-committed so `git status --porcelain` is empty (except the E9 probes, where the
  untracked file IS the defect) — otherwise E9 would open for a reason that is not the injection.
- **Flip edits (red→green)** mirror the generator's own defect inverses: E1 placeholder → the
  repo's own C0 hash; E2 `depth density` → `depth:density`; E3 re-insert the
  `| r35-defect-closure.sh` row before the r36 row; E4 restore the provenance note; E4b drop the
  `.git/info/exclude` line + `git add` the results file; E5 restore the d5 erratum; E6
  `Correction (round 34)` → `Correction (round 35)`; E7 `R22 citation unchanged` →
  `supersedes R22`; E8 restore the lesson; E9 remove the untracked stray; E9b empty scratch root.
- **Independent green→red injections** deliberately use DIFFERENT byte edits than the
  generator's, so the checks are proved to discriminate the defect class and not the generator's
  specific bytes: E1 second `Final lane commit:` line naming a nonexistent 40-hex; E2 corrected
  mean `201.2`→`201.3` (anchor kept; generator broke the anchor instead); E3 r36-row removal
  (generator removed the r35 row); E4 provenance note truncated to EMPTY; E5 d5 file kept, both
  statement clauses stripped; E6 stale dead-seat sentence restored with correction kept; E7 R23
  row removed (generator broke R22); E8 `+10/0` measured-pair token removed from the lesson; E9
  different untracked stray path (`stray2.md` at repo root).

## 3. Matrix A — detector A (suite-A `4283a9d3…`, 308 lines) — 32/32 met

| run | expected | observed | verdict |
|---|---|---|---|
| pristine green | closed=9/9 exit=0 | closed=9/9 exit=0 | met |
| pristine red-E1..E9, E4b, E9b (11) | closed=8/9 exit=1, own check open only | all 11 exactly that | met |
| flip-E1..E9, E4b, E9b (11) | closed=9/9 exit=0 | all 11 exactly that | met |
| gr-E1..E9 (9, independent injections) | closed=8/9 exit=1, own check open only | all 9 exactly that | met |

## 4. Matrix B — detector B (suite-B FROZEN `76273416…`, 817 lines) — 34/34 met

| run | expected | observed | verdict |
|---|---|---|---|
| pristine green | closed=9/9 exit=0 | closed=9/9 exit=0 | met |
| pristine red-E1..E9, E4b, E9b (11) | closed=8/9 exit=1, own check open only | all 11 exactly that | met |
| bflip-E1..E9, E4b, E9b (11) | closed=9/9 exit=0 | all 11 exactly that | met |
| bgr-E1, E2, E3, E7, E9 | closed=8/9 exit=1, own check open only | all 5 exactly that | met |
| bgr-E4, E5, E6, E8 | closed=9/9 (predicted B-weaker divergence) | all 4 closed=9/9 | met (divergence confirmed, §5) |
| bE8-E8a (M36 rows absent, source-recheck still named) | closed=8/9, E8 open | `m36-rows=0,names-corrected-line=1,stale-line=0,round35-lesson=1` → E8 open | met |
| bE8-E8b (M36 present, stale line reintroduced) | closed=8/9, E8 open | `m36-rows=4,names-corrected-line=1,stale-line=1,round35-lesson=1` → E8 open | met |

Green fixture under frozen B, full payload (the corpus amendment reconciled the earlier 7/9):

```
export-ref=0ef3a50a5759243208fa5d818112bb19db4eb5bd mode=export
E1 payload=placeholders=0,lane-hash-markers=0,final-lane-commits=1,bound=1 closed=1
E2 payload=erratum-row=1,erratum-mean=6 closed=1
E3 payload=registry-r35-defect-closure=1,registry-r36-closure=1 closed=1
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=1 closed=1
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=4,names-corrected-line=1,stale-line=0,round35-lesson=1 closed=1
E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
closed=9/9 exit=0
```

## 5. Finding — four A/B check-strength divergences (measured, same trees)

Same injection, different verdicts. Suite-A is stricter; suite-B (frozen) closes all four:

| probe (independent injection) | detector A | detector B | clause difference |
|---|---|---|---|
| gr-E4: provenance note truncated to empty | `provenance_note=0 open=1` | `provenance-note=1 closed=1` | A tests `[ -s ]` (non-empty), B tests `[ -f ]` (exists) |
| gr-E5: d5 file kept, both statements stripped | `discriminating_invocation=0 per_id_occurrences=0 open=1` | `claims-erratum-d5=1 closed=1` | A requires both statement literals, B existence-only |
| gr-E6: stale dead-seat sentence restored, correction kept | `stale_dead_seat=1 open=1` | `correction-round35=1 closed=1` | A requires stale==0, B checks the correction only |
| gr-E8: `+10/0` measured-pair removed from lesson | `measured_pair=0 open=1` | `m36-rows=4,names=1,stale=0,lesson35=1 closed=1` | A requires the measured pair, B does not |

Decision-relevant for the landing: if B lands as-is, these four defect classes pass undetected
on this fixture corpus, and B's own selftest mutants do not cover them either (ExecC1Fixtures'
cross-clause run already flagged E5b/E5c/E6b as beyond the frozen wording and E8b/E8d as a real
residual; B's `names-corrected-line` limb now covers E8b's naming half). Under A they are caught.
Neither draft contradicts the frozen claim's literal wording; the corpus only discriminates the
stricter predicate. Recorded as a coverage finding for the L1, not a check defect.

## 6. Finding — vacuousness: fixture-level DETECTED, judge-level SURVIVOR

- **Fixture-level (the item's ask): DETECTED.** `vac-red-E3` = green bytes labelled as a red
  case, no defect: detector A reads `closed=9/9 exit=0` with `own_open=0` → the matrix rule
  (red case must have `own_open=1`, `others_open=none`) flags the case vacuous; detector B reads
  the same (`closed=9/9`, `own_open=0`). ExecC1Fixtures' own suite-mutant M1 (always-closed E3)
  exercises the same rule from the suite side.
- **Extra case: REJECTED.** A report with 9 valid cases plus one vacuous extra
  (`selftest case=EV positive=pass mutants=0/0 verdict=pass`) is rejected by the frozen judge
  (`cases==9` bound).
- **SURVIVOR — detail-free all-pass caseline report ACCEPTED by the frozen judge
  (`76273416…`).** Sourcing the frozen bytes and calling `judge_selftest_report` on:

  ```
  selftest case=E1 positive=pass mutants=0/0 verdict=pass
  selftest case=E2 positive=pass mutants=0/0 verdict=pass
  … (E3..E9 same shape) …
  selftest cases=9 failures=0
  ```

  → **ACCEPTED (rc=0)**. The report asserts nothing — no `selftest detail=` lines, no fixture
  rejections, no mutant runs, `mutants=0/0` on every case — yet satisfies the judge, which only
  counts case lines / `verdict=pass` lines / the summary line and per-id presence. The r35
  instrument's `report_ok` closed exactly this class (per-id detail-line requirement +
  `mutants=ok/n` == detail-count cross-check); the frozen r36 judge dropped both. The suite's
  own three forgeries (forge-summary, forge-caselines, forge-failed-cases) remain rejected, and
  the runtime selftest path is safe (its cases print verdict=fail into FAILS when vacuous) —
  the hole is the anti-forgery layer only. Reported to ExecC1SuiteBuild with the exact input;
  suggested repair: require ≥1 `selftest detail=<id> mutant=<name> rejected=1 limb=…` line per
  id and cross-check each case line's `mutants=ok/n` against its detail-line counts (r35
  `report_ok` pattern).

## 7. Concurrent-revision disclosure (moving targets, pinned per run)

- **Fixture generator**: `a8b4ce9b…` (first read) → `f037684e…` (first pin) → `20de0cb3…`
  (final pin). The last revision added deterministic commit dates, `M36-1..M36-4` rows in the
  fixture lesson, the round-35 stale-line correction, and `bind_blocks()` (re-binds every 40-hex
  token in a `Final lane commit` window to the fixture's own base).
- **Suite-B**: `d395aa52…` (719 ln) → `ff616adc…` (737 ln) → `9fbdee69…` (their cross-run) →
  `76273416…` (817 ln, FROZEN). All B numbers above are at the frozen digest.
- **Historical measurement, superseded**: at `ff616adc…` + the pre-amendment corpus, the green
  fixture read `closed=7/9 exit=1` (E1 `final-lane-commits=4,bound=1` — three historical
  Final-lane-commit hashes unresolvable in a fixture repo; E8 `m36-rows=0` — lesson without M36
  rows). Both were fixture-predicate mismatches, not check defects; the corpus amendment
  (bind_blocks + M36 lesson) and B's E8 revisions reconciled them — frozen-B green now reads
  9/9 (§4). Recorded because the earlier 7/9 was quoted in my peer messages.
- **Suite-A**: `4283a9d3…` (308 lines) stable across the whole seat; their receipt cites the
  same digest (their "340 lines" IRC figure was a slip, retracted by them).

## 8. Write scope, isolation, restoration evidence

- Allowed writes only: this receipt + scratch under
  `/fast/scratch/hyaku/kasegi-r36/MutC1Fixtures/` (removed before yield; the pins above preserve
  reproducibility). No sibling scratch, lane file, fleet file, or source tree was written.
- ExecC1SuiteBuild's bytes re-hashed EQUAL at seat end: `76273416…` at the frozen check and
  `4db1ae70…` at the final check (the suite owner's own revision between those two, not mine).
  ExecC1Fixtures' scratch was removed at their yield before my final check; my matrix ran on my
  deterministic regeneration, which reproduces their receipt's cited shas (green
  `0ef3a50a…`/`d540b7cf…`).
- Lane repo `git status --porcelain` showed the same 9 orchestration entries before and after
  all probes; my only lane write is this receipt.
- Every git mutation ran inside a `mktemp -d` copy under my scratch after
  `rev-parse --show-toplevel` verification; no lane-repo git state was touched.
## 10. Addendum — re-run at the FINAL suite digest `4db1ae70…` (supersedes §4/§6/§8 digits)

ExecC1SuiteBuild revised the suite after my judge finding: **FINAL bytes
`4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`** (894 lines,
39022 bytes, `bash -n` clean; `76273416…` superseded). The corpus was regenerated
(`fx3/`) from the receipt-embedded final generator (sha `474a27e…`, extracted verbatim
from `.ufo/waves/round-36/wave1/ExecC1Fixtures.md` Appendix and digest-verified) and the
rebuilt `src` (`git archive b47f2cd -- <their reproduce recipe>`): every fx3 sha equals
the fx2 sha (green HEAD=`0ef3a50a…`, BASE=`d540b7cf…`; all red HEADs identical), so the
corpus is the same; only the detector moved.

### 10.1 B-final matrix (suite `4db1ae70…`) — 34/34 met after one probe fix

| run | result |
|---|---|
| pristine green | closed=9/9 exit=0 (E1 `round36-section=1,round36-final-lane-commits=1,bound=1`; E2 `erratum-marker=1,erratum-row=1,erratum-mean=6`; E9 `lane-root=1,scratch-root=present`) |
| pristine red-E1, E3..E9, E4b | all closed=8/9 exit=1, own check open only (10/10) |
| **pristine red-E2** | **closed=9/9 exit=0 — VACUOUS w.r.t. B-final** (new finding, §10.2) |
| pristine red-E9b | closed=8/9 exit=1, E9 open, `scratch-seat-dirs=1` (after my probe fix, §10.3) |
| b2flip-E1..E9, E4b, E9b (11) | all closed=9/9 exit=0 |
| b2gr-E1, E2, E3, E7, E9 | all closed=8/9 exit=1, own check open only |
| b2gr-E4 | closed=8/9, E4 open — **divergence CLOSED**: B-final now requires non-empty provenance (`[ -s ]`) |
| b2gr-E5, E6, E8 | closed=9/9 — **divergence STANDS** (A stricter; §5 unchanged) |
| b2E8-E8a / E8b | both closed=8/9, E8 open (payloads as §4) |
| b2vac-red-E3 | 9/9, own_open=0 → vacuous DETECTED |

### 10.2 Finding — red-E2 vacuous w.r.t. B-final (new E2 predicate)
The final E2 requires `Erratum (round 35)` >=1 AND the row shape
`^\|\s*depth:density\s*\|\s*9\s*\|\s*mean **201.2**` >=1 AND `201.2` >=1. The
generator's E2 defect breaks only the OLD anchor prose (`round-34 depth:density row` →
`round-34 depth density row`), which B-final no longer reads → pristine red-E2 reads
`closed=9/9 exit=0` under B-final, indistinguishable from green. The E2 red fixture must
be regenerated against the new predicate (break the marker or the row) for the corpus to
discriminate E2 under B-final. Evidence: my independent gr-E2 (`201.2`→`201.3`) does
open B-final's E2 (`erratum-mean=0`) — the check itself discriminates; the fixture
byte edit is stale.

### 10.3 Probe bug, disclosed
My first red-E9b re-run read 9/9 only because the recreated scratch lacked the stray
dir (`scratch-root=absent`); with `e9root-stray/stray-seat` present the probe reads
`scratch-seat-dirs=1` → E9 open → closed=8/9. Not a suite regression.

### 10.4 Judge fix verified — F2 KILLED
`judge_selftest_report` at `4db1ae70…` now requires, per id, `n>=1` and exactly `n`
`selftest detail=<id> mutant=` lines of which `ok` say `rejected=1` (ok==n). Probes:

| report | verdict |
|---|---|
| vacuous-caselines (9 pass cases, mutants=0/0, no details) — the F2 input | **REJECTED** |
| valid-shaped (details present, counts agree) | ACCEPTED |
| 10-case (9 valid + 1 vacuous extra) | REJECTED |
| count-mismatch (E3 case says 1/1, 2 detail lines) | REJECTED |
| ok<n (E5 mutant detail rejected=0) | REJECTED |

Suite `--selftest` on the fixture green at the final digest: `selftest cases=9
failures=0` exit 0, `judge=own-report accepted=1`, and all four permanent forgery
cases rejected (`forged-summary`, `forged-caselines`, `forged-failed-cases`,
`forged-detail-free` all =1).

### 10.5 Final verdict at `4db1ae70…`
**66/66 matrix rows met (with the §10.3 probe fix), 0 fixture-level survivors; the
single judge-level survivor (F2, §6) is KILLED.** Remaining open items are coverage
findings only: the stale E2 fixture bytes (§10.2) and the standing E5/E6/E8 strength
divergences (A stricter than B-final; B-final's own selftest mutants do not cover
them — recorded in ExecC1SuiteBuild's receipt as the documented "what was corrected"
dimension limit).

## 9. Tooling record

No tools installed or upgraded (bash, git, python3 sufficed). Tooling-authorization record:
empty.


Report: .ufo/waves/round-36/wave1/MutC1Fixtures.md

