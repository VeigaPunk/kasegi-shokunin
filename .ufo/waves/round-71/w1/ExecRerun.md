# Round 71 · ExecRerun · independent re-run of the C1 controls (clone at 4e33119)

Seat: ExecRerun (executor, leaf). Scope: re-run the three committed C1 controls and pin hashes on a
`git clone --shared` checkout; run the gate selftest, mutbat and real ledger. No production file
written, no git mutation in the lane, no commit or push. Scratch tree
`/fast/scratch/hyaku/kasegi-r71/ExecRerun/` removed before yield.

Tools: none installed or updated (no pacman, uv or npm activity). Host: `sort (GNU coreutils) 9.12`,
`git version 2.56.0`, `Python 3.14.8` (`/usr/bin/python3`). Note: `sort` is also a bash builtin name in
my persistent shell; the counter's subprocesses resolve `/usr/bin/sort` (GNU 9.12, shown in every
HOST line), so the builtin did not affect any result.

## 1. Clone and checkout

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin $S/clone
git -C $S/clone rev-parse --show-toplevel   -> /fast/scratch/hyaku/kasegi-r71/ExecRerun/clone
git -C $S/clone checkout -q --detach 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60
git -C $S/clone rev-parse HEAD              -> 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60
git -C $S/clone status --porcelain | wc -l  -> 0
```

Gate bytes for the do-nothing and base modes were exported from the revisions that carry them, not from
the lane working tree:

```
git show 1bd01ee:corpus/instruments/figure-audit.py        > $S/gates/base/figure-audit.py       (r69)
git show c1051749:corpus/instruments/figure-audit.py       > $S/gates/donothing/figure-audit.py  (r70)
cp  $S/clone/corpus/instruments/figure-audit.py              $S/gates/candidate/figure-audit.py   (4e33119)
```

## 2. Hash table

Pins are `.ufo/waves/round-71/controls/pins-r71.txt` as committed at 0e260a5 (the file is byte-identical
at 4e33119: `git diff --quiet 0e260a5 4e33119 -- <pins>` exit 0). Every computed hash below is from the
clone at 4e33119.

| file (clone @4e33119) | pinned (pins-r71.txt / claims text) | computed | verdict |
|---|---|---|---|
| controls/c1-probe-run-r71.py (counter) | 80020705e1ff8c3cd8b0d2d20485589d8f17b65e9d1aae9eb9af2f748dd61c0b | 80020705e1ff8c3cd8b0d2d20485589d8f17b65e9d1aae9eb9af2f748dd61c0b | MATCH |
| controls/c1-base-r71.txt | f553ddb45b33832dc553e56836f10fb8947f97abefe9e1efeee509e8907025d3 | f553ddb45b33832dc553e56836f10fb8947f97abefe9e1efeee509e8907025d3 | MATCH |
| controls/c1-donothing-r71.txt | eb24dd87bc99c4976f692c6fcf8d63e148e11f5d232215b88234eb5cc7ad1ba6 | eb24dd87bc99c4976f692c6fcf8d63e148e11f5d232215b88234eb5cc7ad1ba6 | MATCH |
| controls/c2-base-counters-r71.txt | 4adae3b6893e6b2332e872f1c0ed4d8c00f93c55018ecb29e91efd42ff0ca79e | 4adae3b6893e6b2332e872f1c0ed4d8c00f93c55018ecb29e91efd42ff0ca79e | MATCH |
| claims.json | c530ec658cff551459a61b1dd3c8052cb089d806497c0e8a9f3ca0243238b3e6 | c530ec658cff551459a61b1dd3c8052cb089d806497c0e8a9f3ca0243238b3e6 | MATCH |
| controls/c1-candidate-trial-r71.txt | NOT PINNED (absent from pins-r71.txt; absent from the 0e260a5 tree; added by 4e33119) | 2231c8c814549ec9ffd4e0a6f35ffb3431f4079d79c6764134b21f12879de4dc | no pin to compare |
| corpus/instruments/figure-audit.py (candidate gate) | 182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 | 182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 | MATCH |
| round-70 gate (do-nothing; export of c1051749, same bytes as 39cde8a and 0e260a5) | 7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 | 7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 | MATCH |
| r69 base gate (export of 1bd01ee) | c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde | c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde | MATCH |
| corpus/source-snapshots/round-71/S106.txt | 291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db (148 lines, 15004 bytes) | 291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db (148 lines, 15004 bytes) | MATCH |
| corpus/instruments/figure-audit-mutbat.py | none pinned | 7a61cf1e5cd22c4f0fa553b2455aab795a26cc3f5ac491466753e4cceffd9992 | informational |
| corpus/instruments/figure-audit-ledger.json | none pinned | 28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b | informational |
| corpus/instruments/frontier-recheck-count.py | none pinned | 010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6 | informational |

Pinned entries: 5 of 5 MATCH. Claims-text gate and S106 hashes: 4 of 4 MATCH. Mismatches: none.
Gate-history cross-check (`git log` of the gate): 4e33119 = 182f4ef7, c1051749 = 7a8d52eb,
1bd01ee = c09b0fb1, 39cde8a = 7a8d52eb.

## 3. Frozen counter, three modes, on the clone

Commands (cwd = clone; `--lane` passed explicitly, because the counter's default lane is the real lane):

```
python3 -B $C/.ufo/waves/round-71/controls/c1-probe-run-r71.py --gate $C/corpus/instruments/figure-audit.py \
  --work $S/work/candidate --lane $C --mode candidate
python3 -B $C/.ufo/waves/round-71/controls/c1-probe-run-r71.py --gate $S/gates/base/figure-audit.py \
  --work $S/work/base --lane $C --mode base
python3 -B $C/.ufo/waves/round-71/controls/c1-probe-run-r71.py --gate $S/gates/donothing/figure-audit.py \
  --work $S/work/donothing --lane $C --mode donothing
```

Each mode was run twice (run 1 `out/<mode>.txt`, run 2 `out/<mode>2.txt`); the two runs were byte-identical
(`diff` 0 lines for all three modes). Exit codes captured per run:

```
candidate exit=0    (run 1 and run 2)
base      exit=1    (run 1 and run 2)
donothing exit=1    (run 1 and run 2)
```

VERIFY lines, as printed by the reruns:

```
VERIFY measurements=25 failures=0 gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing
```

Receipt-vs-rerun comparison (`diff <committed receipt> <rerun>`, whole file, not only MEASURE lines):

| receipt | rerun | differing lines | differing MEASURE lines |
|---|---|---|---|
| controls/c1-candidate-trial-r71.txt | out/candidate.txt | 2 (lines 15 and 22) | 2 of 25 |
| controls/c1-base-r71.txt | out/base.txt | 2 (lines 15 and 22) | 2 of 25 |
| controls/c1-donothing-r71.txt | out/donothing.txt | 2 (lines 15 and 22) | 2 of 25 |

Total: 6 of 75 MEASURE lines differ; the HOST, GATE and VERIFY lines are byte-identical in all three modes.
The same two rows differ in each mode; only the `direct_rc` field changes (0 -> 1):

```
< MEASURE R1-capture-binding-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1      (candidate, base)
> MEASURE R1-capture-binding-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
< MEASURE R8-capture-binding-pipeline ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1  (candidate, base)
> MEASURE R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
< MEASURE R1-capture-binding-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0     (donothing)
> MEASURE R1-capture-binding-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
< MEASURE R8-capture-binding-pipeline FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0 (donothing)
> MEASURE R8-capture-binding-pipeline FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
```

Cause, measured. The two rows run `capture-binding-check.py --root .` (R8 pipes it to
`grep -c records=84`). Run directly on the clone and on the lane (`cmp` of the two outputs: identical):

```
MANIFEST round-71 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=85 with_url=85 with_fetched_utc=47 with_archival=38 snapshot_dirs=44 manifest_dirs=44 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S106 dir=round-71
records=85 bound=84 unbound=1
```

exit 1 on both trees. Supporting facts:
- `corpus/SOURCES.md` at 4e33119: 105 rows matching `^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|`; `grep -c S106` = 0.
  The same at 0e260a5 (`grep -c S106` = 0).
- `git show --stat 4e33119` touches 4 files: `controls/c1-candidate-trial-r71.txt`, `corpus/instruments/figure-audit.py`,
  `corpus/source-snapshots/round-71/S106.txt`, `corpus/source-snapshots/round-71/manifest.json`. `corpus/SOURCES.md` is not among them.
- The lane working tree has `corpus/SOURCES.md` unmodified (`git status --porcelain -- corpus/SOURCES.md` empty), so the lane has no S106 row either.
- `capture-binding-check.py` reads the registry as column 2 of `| S0xx |` rows (its header line 173; `load_registry` line 231).

Consequence (measured): the committed receipts' `direct_rc=0` for R1 and R8 is NOT reproduced at 4e33119.
The rerun is internally consistent (gate_rc equals direct_rc, value_ok=1), so the C1 kill rule (any FAIL
MEASURE on the candidate; nonzero candidate exit) is not triggered by this difference.
[INFERENCE] The receipts were taken on a tree state that differed from the committed 4e33119 registry, which
lacks the S106 row the round-71 manifest needs; this seat did not verify that history.
The C2 counting predicate `records=85 bound=85 unbound=0` and `registry=106` in claims.json does NOT reproduce
on the committed tree (measured: bound=84 unbound=1, 105 registry rows). I did not run the rest of the C2
predicate (frontier census, entries, knowledge sort, census validate): that is the C2 seat's measurement.

## 4. Kill rules and predicate, applied to the reruns

- candidate: failures=0, exit 0, gate sha256 = frozen 182f4ef7 -> predicate holds.
- candidate: no FAIL MEASURE line (`grep -c FAIL out/candidate.txt` = 0) -> kill rule not triggered.
- do-nothing: failures=13 (>= 10), exit 1, marker_runs=1 on N8 (`N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0`),
  and R1..R8 all `gate_rc=2 admitted=0` -> holds.
- base (r69): failures=14, exit 1; N1..N12 all FAIL with refused=0 (all twelve negatives admitted) -> holds.
- forgery control: not run by this seat (the counter's `forgery` mode choice exists but was not run); not verified here.

## 5. Gate selftest, mutbat, real ledger

```
cd $C; TMPDIR=$S/tmp-selftest python3 corpus/instruments/figure-audit.py --selftest      -> rc=0, 107 lines
selftest case=final-exit1-stale exit=1 want=1 verdict=pass reasons=derive-exit-1
selftest case=final-error-precedes-upstream-error exit=1 want=1 verdict=pass reasons=derive-exit-7
selftest case=python-census-covers-instruments exit=0 want=0 verdict=pass
selftest cases=106 failures=0
```

Selftest pin lines (`grep -c "selftest pin"`): 0. Selftest `^selftest` lines: 107.

```
cd $C; TMPDIR=$S/tmp-mutbat python3 corpus/instruments/figure-audit-mutbat.py --instrument corpus/instruments/figure-audit.py -> rc=0
MUT m4-drop-stale-literal-case sites=1 compile=0 selftest_exit=1 killed=1 invalid=0 last='selftest cases=105 failures=1'
MUT m6-readonly-gate-off sites=1 compile=0 selftest_exit=1 killed=1 invalid=0 last='selftest cases=106 failures=4'
MUT m7-python-confinement-off sites=1 compile=0 selftest_exit=1 killed=1 invalid=0 last='selftest cases=106 failures=2'
MUT m8-python-prefix-off sites=1 compile=0 selftest_exit=1 killed=1 invalid=0 last='selftest cases=106 failures=1'
MUT m9-python-boundary-separator-off sites=1 compile=0 selftest_exit=1 killed=1 invalid=0 last='selftest cases=106 failures=1'
mutbat killed=5/5 survivors=0 invalid=0 controls=pass
```

```
cd $C; TMPDIR=$S/tmp-ledger python3 corpus/instruments/figure-audit.py --ledger corpus/instruments/figure-audit-ledger.json --root . -> rc=0
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
```

## 6. Summary for the L1

- C1 controls reproduce: candidate VERIFY failures=0 exit 0; do-nothing failures=13 exit 1 with N8 marker_runs=1; r69 base failures=14 exit 1 with N1-N12 all admitted. Selftest 106/0, mutbat 5/5, ledger 35/35.
- All five pinned hashes and the four claims-text hashes match. No mismatch.
- Receipt-vs-rerun: 2 MEASURE rows differ per receipt (R1 and R8, `direct_rc` 0 -> 1). Measured cause: `capture-binding-check.py --root .` exits 1 at 4e33119 because the committed registry lacks the S106 row (`FAIL rule=no-row record=S106`). NOT VERIFIED: the receipts' R1/R8 `direct_rc=0` at this revision.
- C2 counting predicate (`bound=85 unbound=0`, `registry=106`) does not reproduce on the committed 4e33119 tree (measured bound=84 unbound=1, 105 registry rows). Reported as observed; not judged here.
- Not run by this seat: the forgery mode, the C2 census/entries/knowledge commands, and any lane-tree command other than the read-only derives above.
