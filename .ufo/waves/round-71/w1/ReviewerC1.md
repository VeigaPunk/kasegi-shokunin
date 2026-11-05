# ReviewerC1 — round-71 wave 1: independent reproduction of frozen claim C1

C1: VERIFIED

All frozen predicate values reproduce from committed bytes at base revision
`4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`. Two non-fatal discrepancies with the
pinned receipts are disclosed in §5 (lane-tree drift from in-flight C2 work, not
gate behaviour). No kill-rule clause is triggered.

## 1. Setup and pins (measured)

```
$ git clone --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    /fast/scratch/hyaku/kasegi-r71/ReviewerC1/clone
$ git -C <clone> checkout 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60
$ git -C <clone> rev-parse HEAD
4e33119e0167cac3fbfa15afb3f2f5b98a43cc60
```

```
$ sha256sum corpus/instruments/figure-audit.py .ufo/waves/round-71/controls/c1-probe-run-r71.py
182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603  corpus/instruments/figure-audit.py
80020705e1ff8c3cd8b0d2d20485589d8f17b65e9d1aae9eb9af2f748dd61c0b  .ufo/waves/round-71/controls/c1-probe-run-r71.py
```

Both match the assignment's frozen values. Note: `.ufo/waves/round-71/controls/pins-r71.txt`
at `4e33119e` has five lines (counter, `c1-base-r71.txt`, `c1-donothing-r71.txt`,
`c2-base-counters-r71.txt`, `claims.json`) and does NOT pin the gate itself; the
gate hash above was verified against the assignment text and the trial receipt's
`GATE` line. The counter pin line matches pins-r71.txt line 1 exactly.

Round-70 gate bytes exported for the do-nothing control:

```
$ git -C <clone> show 39cde8a:corpus/instruments/figure-audit.py > donothing-gate.py
$ sha256sum donothing-gate.py
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  donothing-gate.py
```

Base gate pin: `sha256sum .ufo/waves/round-70/controls/base-gate-r70.py` =
`c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde` (matches
claims.json). Host: `sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8`
(same as every frozen receipt's HOST line).

## 2. The three frozen-counter runs (measured, verbatim VERIFY lines)

All three runs: `cd <clone> && python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py
--gate <gate> --work /fast/scratch/hyaku/kasegi-r71/ReviewerC1/<WORK> --mode <mode>`
(`--lane` left at its default `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
exactly as claims.json's counting_command specifies).

Candidate (`--gate corpus/instruments/figure-audit.py --work FINAL --mode candidate`), exit 0:

```
VERIFY measurements=25 failures=0 gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
```

Base (`--gate .ufo/waves/round-70/controls/base-gate-r70.py --work BASE --mode base`), exit 1:

```
VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
```

Do-nothing (`--gate <scratch>/donothing-gate.py --work DONOTHING --mode donothing`), exit 1:

```
VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing
```

Exit codes observed: `CANDIDATE_EXIT=0`, `BASE_EXIT=1`, `DONOTHING_EXIT=1`.

## 3. Kill-rule check against claims.json (C1)

claims.json declares no per-line values for C1; the falsifiable values live in the
`predicate` text. Each clause:

- Candidate `VERIFY measurements=25 failures=0` + exit 0: REPRODUCED (§2).
- Candidate gate sha256 equals the frozen measured sha256 `182f4e…4603`: YES —
  printed in both `GATE` and `VERIFY` lines; file hash independently measured in §1.
- Do-nothing `measurements=25 failures=13` (≥ ten), exit 1: REPRODUCED. N8:
  `MEASURE N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0`
  (recheck payload ran through bash -c, marker_runs=1). All eight R rows refused:
  R1–R8 all `gate_rc=2 admitted=0` in donothing.out.
- r69 base gate `measurements=25 failures=14`, exit 1, every N row admitted:
  REPRODUCED — N1–N12 all `rc=1 refused=0` (admitted, derive-failed) in base.out.
- Any FAIL MEASURE line, nonzero candidate exit, or candidate sha256 mismatch defeats C1:
  candidate.out has zero FAIL lines, exit 0, and the candidate sha256 equals the frozen
  `182f4e…4603`. Nothing defeats C1.
- Blanket-refusal forgery limb: not part of this seat's three runs; claims.json
  marks it "to be produced at the wave". Not assessed here.

No 25-measurement line disagrees with any value claims.json declares for C1.

## 4. Selftest pin re-derived from bytes

```
$ grep -cE '^\s+run_case\(' corpus/instruments/figure-audit.py
105
$ grep -n 'EXPECTED_CASES' corpus/instruments/figure-audit.py
221:EXPECTED_CASES = 106  # R17 pin: ... R71: +10 per-script census pins
```

105 `run_case(` call sites + one direct `cases.append(("python-census-covers-instruments", …))`
at figure-audit.py:921 = 106 cases = `EXPECTED_CASES`. The pin check at
figure-audit.py:930-932 fails the selftest if `len(cases) != EXPECTED_CASES`.

```
$ TMPDIR=<scratch> python3 -B corpus/instruments/figure-audit.py --selftest
selftest case=python-census-covers-instruments exit=0 want=0 verdict=pass
selftest cases=106 failures=0        (exit 0; 106 "selftest case=" lines)
```

Census cross-check: `corpus/instruments/` holds 44 `*.py` files; `PY_SCRIPT_CENSUS`
names exactly those 44 basenames (0 uncovered, 0 phantom); `PY_SELFTEST_FIXTURE_HEADS`
(8 heads) are fixture-only and absent from the instrument dir, as documented at
figure-audit.py:133-217. Denial tables present: `PY_DENIED_ANY = ("--out", "--output",
"--selftest")` (line 143), `PY_HEAD_REFUSED = ("frontier-recheck-count.py",)` (145-148),
`PY_DENIED_BY_SCRIPT` (150-166). Fail-closed rule at line 496: a head not in the
census and not a fixture head is refused.

## 5. Discrepancies vs the frozen receipts (disclosed, non-fatal)

`diff` of my three outputs against the in-repo receipts shows exactly two differing
MEASURE lines per run — R1 and R8 `direct_rc`/`gate_rc` fields only; every verdict,
failure count, exit code and gate hash is identical:

- candidate vs `controls/c1-candidate-trial-r71.txt`: lines 15, 22 —
  `R1-capture-binding-root ok direct_rc=1 gate_rc=1` (receipt: `direct_rc=0 gate_rc=0`);
  `R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1` (receipt: `0/0`).
- donothing vs pinned `controls/c1-donothing-r71.txt`: lines 15, 22 — same rows,
  `FAIL … direct_rc=1 gate_rc=2` (receipt: `direct_rc=0 gate_rc=2`); verdicts identical.
- base vs pinned `controls/c1-base-r71.txt`: lines 15, 22 — same pattern as candidate.

Cause (measured, not inferred): the lane working tree at `4e33119e` now carries C2's
S106 capture (`corpus/source-snapshots/round-71/S106.txt`, records=85) while C2's
registry/manifest binding is still in flight, so
`python3 corpus/instruments/capture-binding-check.py --root .` exits 1 with
`FAIL rule=no-row record=S106 dir=round-71` / `records=85 bound=84 unbound=1`
(R1 and R8 both derive from this counter). The frozen receipts were produced before
S106 entered the tree (records=84, exit 0). The counter re-derives each positive's
`want` from the live direct run (`c1-probe-run-r71.py:238-251`), so the measurement
stays self-consistent: in candidate and base `direct_rc == gate_rc` on R1/R8 with
`admitted=1 value_ok=1`; in do-nothing the gate refuses them (`gate_rc=2 admitted=0`) as it
refuses every R row there. Gate behaviour is unchanged; this is lane-tree
drift from concurrent C2 authoring. All five pins-r71.txt entries re-verified by `sha256sum`
at the frozen revision (§1 and this section), so the frozen receipts are unmodified; only the
live lane tree they were measured against has since gained S106.

Lane working tree also carries `M corpus/QUALITY.md` (+1 line, R110 row) and
untracked `.ufo/waves/round-71/w1*` files; none of these touch `corpus/instruments/`
or the gate bytes under test.

## 6. Full observed outputs

Candidate (exit 0) — `candidate.out`, 28 lines:

```
HOST sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8
GATE sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
MEASURE N1-python-root-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N2-python-root-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N3-python-root-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N4-python-out-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N5-python-out-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N6-python-out-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N7-python-json-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N8-python-no-option-head ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N9-python-selftest ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N10-python-short-o ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N11-python-output-long ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N12-python-unknown-head ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE R1-capture-binding-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R2-kill-rule-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R3-frontier-count-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R4-claim-package-json ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R5-citation-ground-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R6-gate-quote-audit-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R7-routed-defects-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest ok selftest cases=106 failures=0 rc=0 min=104
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=25 failures=0 gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
```

Do-nothing (exit 1) — `donothing.out`, 28 lines:

```
HOST sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8
GATE sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing
MEASURE N1-python-root-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N2-python-root-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N3-python-root-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N4-python-out-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N5-python-out-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N6-python-out-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N7-python-json-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N9-python-selftest FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N10-python-short-o ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N11-python-output-long ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N12-python-unknown-head FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE R1-capture-binding-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R2-kill-rule-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R3-frontier-count-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R4-claim-package-json FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R5-citation-ground-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R6-gate-quote-audit-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R7-routed-defects-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R8-capture-binding-pipeline FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest FAIL selftest cases=96 failures=0 rc=0 min=104
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=1
VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing
```

Base (exit 1) — `base.out`, 28 lines:

```
HOST sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8
GATE sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
MEASURE N1-python-root-space FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N2-python-root-equals FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N3-python-root-abbrev FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N4-python-out-space FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE N5-python-out-equals FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE N6-python-out-abbrev FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE N7-python-json-space FAIL rc=1 refused=0 marker_runs=1 wrote=1
MEASURE N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N9-python-selftest FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N10-python-short-o FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N11-python-output-long FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N12-python-unknown-head FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE R1-capture-binding-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R2-kill-rule-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R3-frontier-count-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R4-claim-package-json ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R5-citation-ground-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R6-gate-quote-audit-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R7-routed-defects-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest FAIL selftest cases=86 failures=0 rc=0 min=104
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=5
VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
```

## 7. Residual risk and verification gaps

- The counter's `--mode` flag is a label only (`c1-probe-run-r71.py:266-268` prints it;
  no branch reads it); gate bytes alone determine behaviour. Verified by reading the
  source, not by a mode-swapped run.
- The enumerated probe set (N1–N12, R1–R8, 8 controls, 5 whole-gate rows) is what was
  measured; positional-argument, `--`-separator, nested-python and non-enumerated exec
  classes remain open by the claim's own scope statement (claims.json `scope`).
- The blanket-refusal forgery control is unproduced at freeze time; C1's forgery limb
  is therefore verified only by the base run's R-row admissions, not by a forgery run.
- R1/R8 detail-field drift (§5) will disappear once C2's S106 binding lands; if the L1
  re-runs the counter after C2 closes, expect `direct_rc=0` again on those two rows.

Tool installs/upgrades: none. Scratch tree `/fast/scratch/hyaku/kasegi-r71/ReviewerC1/`
removed after this report was written; no lane-tree file was modified by this seat
except this report.
