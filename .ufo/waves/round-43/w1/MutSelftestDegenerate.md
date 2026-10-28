# MutSelftestDegenerate — degenerate-selftest battery for BOTH round-43 instruments

Seat `MutSelftestDegenerate` (leaf, mutation-tester). Lane `kasegi-shokunin`, round 43,
base `ab98fac9dce87130bc4f66de89e30650d63943dc`, claims freeze `4cb6d4ae` (read first,
never edited). Receipt-only item: no deliverable file is landed by this seat.

Axes touched: `depth:verifiability` (the C1 selftest's own degeneracy) and `coverage`
(the C2 gate's selftest controls). One plausible defect per control, smallest
behaviour-bearing point, isolated scratch copies, bounded behavioural detector,
pristine/mutant/restored bytes.

## Target bytes (exact artifacts the verdicts pin to)

Both instruments are still **w1 deliverables, not committed** at the time of this run
(`corpus/instruments/r43-closure.sh` and `corpus/instruments/claim-package-check.py`
do not exist in the lane tree). The battery therefore runs on the published wave
artifacts, and the L1 must re-run it after landing.

| role | path | sha256 |
|---|---|---|
| C1 selftest runner (to be embedded as `r43-closure.sh --selftest`) | `.ufo/waves/round-43/w1/ExecSelftest19.sh` | `d2c947b4a5004d49f9677479f6142a10b1d796f638da3fd3481863ffb5a11848` |
| C2 gate | `.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py` | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` |
| C2 selftest body | `.ufo/waves/round-43/w1/ExecGateSelftest.selftest.py` | `04951ca0e72050725fc01a16ba1e42d7a52bd29bb0ae653b164a39ed39b57b17` |
| nine defect fixtures | `.ufo/waves/round-43/w1/ExecGateFixtures.defect-{1..9}-*` | (dirs; `sha256sum` per fixture not pinning bytes here) |
| exemplar parts | `.ufo/waves/round-43/w1/ExecExemplarPackage.*` | composed to `report.md`, `claim_checklist.md`, `evidence/manifest.json`, `evidence/{source-capture,source-excerpt,solution-fixed-in,disclosure-timeline}.txt`, `custodian-receipts.json`, `provenance.json`, `status.json` |
| C2 instrument as composed per the selftest's own splice note | scratch `c2/claim-package-check.py` | `efdd4d6c95498267b587d3e4ca564a51f8ef4f5d0ba6131bf730e8eb3de4a2ca` |

C2 composition is exactly what the selftest's docstring prescribes: the gate bytes,
with the selftest body pasted above the gate's
`# <!-- selftest-body-paste-anchor: ... -->` line, fixtures at
`<gate dir>/fixtures/claim-package/`. No byte of the composition is invented.

## Battery

Driver: scratch `battery.py` (removed with the scratch dir at the end; the log below
is its verbatim stdout). C1 engine extracted from the runner's `ES19_PY` heredoc and
imported; C2 gate composed as above. Every mutant is a copy under
`$S/battery-tmp` or `$S/work`; the published artifacts are never written.

```
cd /fast/scratch/hyaku/kasegi-r43/MutSelftestDegenerate
TMPDIR="$S/battery-tmp" python3 battery.py all | tee logs/battery.log
EXIT=0
```

```
== C1 runner ==                    ExecSelftest19.sh sha256=d2c947b4a5004d49
C1 accept summary-only             got=reject want=reject REJECTED-OK (lines=0 summaries=1)
C1 accept skipped-case-K19         got=reject want=reject REJECTED-OK (lines=18 summaries=1)
C1 accept wellformed-19            got=accept want=accept REJECTED-OK 
C1 accept duplicate-ids            got=reject want=reject REJECTED-OK (duplicate-ids)
C1 accept failed-case              got=reject want=reject REJECTED-OK (failed-case:K19)
C1 accept summary-count-lie        got=reject want=reject REJECTED-OK (summary:selftest cases=18 failures=0)
C1 shape-limb good                 verdict=True mutants=2/2
C1 shape-limb first-only           verdict=False mutants=1/2 reasons=['shape:accepted'] -> REJECTED-OK
C1 forced-verdict mutant           D-STUB/D-DUPLICATE would accept: stub=True dup=True
C1 isolation cross-case-alias      isolated=True verdict=True SURVIVED(undetected)
C1 isolation leak-outside-work     isolated=False verdict=False REJECTED-OK
C1 isolation sibling-read          isolated=False verdict=False -> REJECTED-OK
C1 --probe-controls pristine       rc=0 control=D-STUB expected=reject observed=reject | control=D-SUMMARY expected=reject observed=reject | control=D-DUPLICATE expected=reject observed=reject | control=ACCEPT expected=accept observed=accept
C1 --probe-controls verdict:=True  rc=3 control=D-STUB expected=reject observed=accept | control=D-SUMMARY expected=reject observed=reject | control=D-DUPLICATE expected=reject observed=accept | control=ACCEPT expected=accept observed=accept
== C2 gate ==                      gate=8b6f849349157a91 selftest=04951ca0e7205072 composed=efdd4d6c95498267
C2 exemplar                        rc=0 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
C2 selftest baseline               rc=0 case_lines=10 fails=0 summary=selftest cases=10 failures=0
C2 B1 summary-only                 rc=0 case_lines=0 stdout='selftest cases=10 failures=0' external_counter=REJECT
C2 B2 skipped-case                 rc=1 case_lines=10 fails=10 summary=selftest cases=10 failures=10 -> REJECTED-OK
C2 B3 always-pass gate             rc=1 fails=9 summary=selftest cases=10 failures=9 -> REJECTED-OK
C2 B4 dup                          occurrences=2 rc=1 fails=['R-NOSECRET'] verdict=DEFECT exit=1
C2 B4 dup-fix1                     occurrences=1 rc=1 fails=['R-NOSECRET'] verdict=DEFECT exit=1
C2 B4 dup-fixall                   occurrences=0 rc=0 fails=[] verdict=WELL-FORMED exit=0
C2 B5 sibling-read                 rc=1 fails=9 detail=sibling-read -> REJECTED-OK
C2 B5 source-fixture-read          rc=1 fails=9 detail=source-fixture-read -> REJECTED-OK
C2 B6 tmpdir-honored(no-clean)     rc=0 summary=selftest cases=10 failures=0 under_TMPDIR=1 /tmp_leak=0 -> honored(TMPDIR used)
C2 B6 tmpdir-pinned-/tmp           rc=0 summary=selftest cases=10 failures=0 under_TMPDIR=0 /tmp_leak=1 -> ACCEPTED(no containment assertion; selftest still green)
```

Write-side isolation probes on the same composed gate (only the audit-hook path is
exercised — the gate writes one file, then runs normally):

```
write-outside-/tmp     rc=1 fails=9 detail=external-write summary=selftest cases=10 failures=9
write-sibling          rc=1 fails=9 detail=sibling-write  summary=selftest cases=10 failures=9
```

The C1 end-to-end `--probe-controls` on the pristine runner printed all four controls
as expected and exited 0; the same runner with the single behaviour-bearing mutation
`verdict = (positive_ok and mutants_ok and payload_match == 1 and isolated)` →
`verdict = True` printed `D-STUB observed=accept`, `D-DUPLICATE observed=accept` and
exited **3** (a degenerate runner refuses to print a transcript).

## Control matrix — which degenerate control each selftest rejects / accepts

| control (seat brief) | C1 runner `--selftest` | C2 gate `--selftest` |
|---|---|---|
| summary-only line (`cases=19/10 failures=0`, no case lines) | **REJECTED** by `accept_selftest` (`lines=0 summaries=1`); D-SUMMARY | **ACCEPTED by the instrument**: `_selftest_emit` suppression prints `selftest cases=10 failures=0`, exit 0, zero case lines; only an external counter (`^selftest case=` count == 10) rejects it |
| a skipped case | **REJECTED**: 18 lines + `cases=19` → `lines=18`; well-formed-19 accepted | **REJECTED**: one defect fixture removed → `fixtures=8` → 10/10 rows fail, `failures=10`, exit 1 |
| an always-pass instrument | **REJECTED**: D-STUB; forced-verdict mutant makes D-STUB/D-DUPLICATE accept and the control run exit 3 | **REJECTED**: every rule forced pass → 9 defect cases fail, `failures=9`, exit 1 |
| mutant rewriting one occurrence of a **duplicated** block (R42) | **REJECTED**: D-DUPLICATE; the shape limb is load-bearing (`shape:accepted` → `mutants=1/2`); ignoring the limb accepts | **REJECTED**: exemplar + secret twice, first rewritten → `occurrences=1`, `DEFECT`/`R-NOSECRET`; both rewritten → `WELL-FORMED` (discriminating positive) |
| a case that reads another case's fixture dir | **REJECTED** for a concurrently-existing sibling (structural `len(live)==1`) and for the canonical fixtures root; **SURVIVES** when `case_root()` is aliased so only the other case's dir exists (`isolated=True`, `verdict=pass`) | **REJECTED**: `sibling-read` (work-root sibling) and `source-fixture-read` (canonical fixture root), and write-side `sibling-write` |
| a case whose fixture dir leaks outside TMPDIR | **REJECTED**: `case_root` → `<work>/../leaked/...` gives `isolated=False`, `verdict=fail` | **ACCEPTED**: pinning `tempfile.mkdtemp(dir="/tmp")` leaves `under_TMPDIR=0`, one `/tmp/claim-pkg-selftest-*`, and `selftest cases=10 failures=0` exit 0 |

## Findings

- **F1 (C2, accepted degenerate — coverage gap).** The gate's `--selftest` has **no
  transcript acceptor**. Suppressing `_selftest_emit` yields a summary-only
  `selftest cases=10 failures=0` at exit 0; the summary count is a literal `10`, not
  `len(emitted lines)`, so nothing inside the instrument binds the green summary to
  ten graded lines. C1's `accept_selftest` is the exact missing piece. Cheapest fix:
  derive the summary count from the emitted rows (or add an acceptor mirroring C1's)
  so "a summary-only line satisfies a case" is impossible, not merely externally
  spot-checked.
- **F2 (C1, survived mutant).** `probe()` asserts `len(live)==1`, that the live dir is
  the case root, and that the tree is inside it — but never that
  `os.path.basename(case_root(work, cid)) == "case-<cid>"`. Aliasing `case_root` for
  every case onto `case-K14` produced `isolated=True verdict=pass` with a battery hook
  and a constant dispatch; the shared dir is removed by the `finally`, so nothing
  surfaces. One added assertion closes it. (The literal degenerate — a check that
  reads a concurrently-existing sibling — *is* caught structurally, silent or not.)
- **F3 (C2, accepted degenerate).** The new write-side audit hook covers the **gate
  child process**, not the selftest's own scratch root: `work_root` can be pinned
  outside `TMPDIR` and the selftest still reports `failures=0`. An assertion that
  `work_root` is under `TMPDIR` (or under a `--work` the caller names, as C1 does)
  would make the leak detectable.
- **F4 (C1, fixed by the owner before this run).** An earlier composition of the C2
  instrument (`.../ExecGateSelftest/integ/spliced/claim-package-check.py`,
  sha256 `2c5da6be0c6aac28086f7fbb02ede4fd22d34dadc6b2bfabe3b15fea9d8ba6b1`) carried
  **two** `RULES` bindings — the gate's dict (line 697) and the pasted selftest's rule-id
  tuple (line 852). The tuple shadowed the dict, `run_rules` evaluated `RULES['R-FILES']`
  on a tuple, every rule returned `error:TypeError`, and `--selftest` printed
  `selftest cases=10 failures=9` with nine `wrong-rule`. Renaming only the pasted tuple
  to `RULE_IDS` (no other change) made the same composition print nine `verdict=pass`
  and `selftest cases=10 failures=0`. The published selftest now uses
  `_SELFTEST_RULES` and its docstring records this exact measured break; the battery
  above confirms the current pair is green. Reported to the L1 at discovery time.
- **F5 (scope note).** C2's selftest has no duplicated-shape control of its own (unlike
  C1's D-DUPLICATE); the gate *rules* nevertheless pass the duplicated-defect probe
  (B4), so the gap is in the selftest's control set, not in gate behaviour.

## Restoration evidence

- No sibling source and no lane file was written. Only copies under
  `$S/pristine`, `$S/runner`, `$S/pub`, `$S/c2`, `$S/work`, `$S/battery-tmp` were
  mutated; every run started from a fresh copy.
- The target sha256 at the final battery run equals its sha256 after the run:
  `ExecSelftest19.sh d2c947b4…`, `ExecGateCore.claim-package-check.py 8b6f8493…`,
  `ExecGateSelftest.selftest.py 04951ca0…`. The owners updated the gate and the selftest
  earlier in the wave (`bdb50a82…`/`bc34fff5…` → `8b6f8493…`/`04951ca0…`); this seat
  only ever read them.
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain` shows
  nothing outside the pre-existing `.ufo/waves/round-43/` wave directory; the fleet
  root was never written by this seat.
- Scratch `/fast/scratch/hyaku/kasegi-r43/MutSelftestDegenerate/` is removed after this
  receipt is written (`rm -rf`); `/tmp/kasegi-r43-degenerate-probe.txt` was removed by
  the probe itself.

## Limits

- The instruments are not committed; the verdicts pin to the sha256s above. Re-run the
  battery after the L1 lands `r43-closure.sh` and `claim-package-check.py`, because the
  C1 runner must be embedded and the C2 pair re-spliced.
- The 19-case full C1 grading needs the suite's in-process dispatch (the runner takes a
  callable); the battery exercised the runner's dispatch seam, grading internals, control
  probe, and transcript acceptor instead of a full nineteen-case suite run.
- Tooling installed/upgraded: **none** (python3 stdlib + bash only; recorded per the
  operator tooling rule).

Deliverables: none (receipt-only). This receipt is 167 lines.
