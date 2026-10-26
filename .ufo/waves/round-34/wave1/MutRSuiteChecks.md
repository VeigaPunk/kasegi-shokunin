# MutRSuiteChecks — mutation test of `corpus/instruments/r-defect-closure.sh`

Round 34, wave 1, seat `MutRSuiteChecks`. Assignment: for each of the nine checks R1–R9, build a
mutant that makes the check vacuous (always exit 0) — the suite's `--selftest` must then fail — and
a mutant that deletes the check — the plain run must print `closed<9/9`. Controls: no-op and
non-compiling mutants rejected. All work on isolated scratch copies under
`/fast/scratch/hyaku/kasegi-r34/MutRSuiteChecks/`; the lane instrument bytes were never modified.

## Method

- **Pinning.** The pristine instrument was copied to scratch and pinned by digest; every mutant is
  derived from that pinned copy, so each mutant differs from its comparison base by exactly the
  assigned mutation.
- **LANE_ROOT shim (harness accommodation, applied uniformly).** The script derives
  `LANE_ROOT=$(cd -- "$SELF/../.." && pwd)` from its own location; a scratch-run copy would
  therefore source selftest fixtures from the scratch tree. Each experimental base changes exactly
  that one line to the literal lane root; everything else is byte-identical to the pin. Neutrality
  is proven: Baseline A (live lane file, unmodified bytes) and Baseline B (pinned+shim copy) produce
  **byte-identical stdout on both detectors** (matrix 2: `A2==B2 plain: True`, `A2==B2 selftest:
  True`).
- **Mutants.** `vac-R#`: line `  return 0  # MUTANT vacuous: check body unreachable` inserted as the
  first body line of `check_r#()` (smallest behavior-bearing point — the check can no longer fail on
  anything). `del-R#`: the whole `# --- R# ---` section span (marker + function) removed and the
  `R#` / `check_r#` tokens dropped from `CHECK_IDS` / `CHECK_FNS` (clean registry deletion).
- **Detectors.** Vacuous → `--selftest` must fail (nonzero exit, `failures>=1`, the case line reads
  `verdict=fail problems=fixture-not-rejected`). Deletion → plain run must print `closed<9/9`.
- **Validity gate.** Every mutant was `bash -n`-checked before execution (rc=0 for all 18; a
  non-compiling mutant would be rejected, not scored).
- **Environment.** `TMPDIR` and `--scratch` pointed into the seat scratch tree for every run; the
  suite's own fixture writes stayed inside it.

## Environment observation: concurrent writer on the pristine instrument

The lane instrument was being edited by another party throughout the seat's early phase. Observed
sha256 prefixes of `corpus/instruments/r-defect-closure.sh` (line counts where sampled):
`149f411b…` (655 ln) → `abcd3de0…` (655) → `7aca98b3…` (655, stable across a 10 s sample) →
`1cb16718…` (663, pinned as matrix-1 base) → `0beafed2…` (at matrix-1 runtime) → `b7ea976b…`
(pinned as matrix-2 base) → `357a7e49…` (at matrix-2 runtime, still live at seat end). The deltas
were: R4 DESC rewording, R8 check tightened from a loose shape regex to a real calendar-instant
parse, R8 broken-fixture value sharpened to `2026-10-25Tgarbage-not-a-timeZ` (a value the frozen
loose regex accepts but that is not an instant), and usage() reworked. Handling: two full matrices
were run on two consecutive pinned bases; within each matrix the suite-input digests were recorded
before and after and were identical (`inputs before==after: True`), and Baseline A (live bytes) was
byte-identical to Baseline B on both detectors — so verdicts are internally consistent and transfer
(see Transfer section).

## Baselines (matrix 2, primary)

`bash corpus/instruments/r-defect-closure.sh` (live lane bytes `357a7e49…`), exit 0:

```
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum open=0
R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0
R6 check=round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected open=0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
```

`--selftest --scratch <seat scratch>/tmp`, exit 0: nine
`selftest case=R# live=pass fixture=rejected verdict=pass` lines, then `selftest cases=9 failures=0`.
Baselines hold, so no verdict is inconclusive. Matrix 1 (base `1cb16718…`+shim) reproduced the same
baselines: `closed=9/9 exit=0` / `cases=9 failures=0`.

## Per-check outcomes (matrix 2, base `b7ea976b…` + shim = `64338818…`)

| chk | vac mutant sha256 (16) | vac selftest | verdict | del mutant sha256 (16) | del plain | verdict |
|---|---|---|---|---|---|---|
| R1 | bc489312e22049d8 | `cases=9 failures=1`, rc=1 | KILLED | 3b347e60d48a90da | `closed=8/9 exit=1`, rc=1 | KILLED |
| R2 | 5d0557ee5f928673 | `cases=9 failures=1`, rc=1 | KILLED | 99e488c003c3fa92 | `closed=8/9 exit=1`, rc=1 | KILLED |
| R3 | f0357d6241666198 | `cases=9 failures=1`, rc=1 | KILLED | 764552790f95aadd | `closed=8/9 exit=1`, rc=1 | KILLED |
| R4 | ac6b8cde438d1644 | `cases=9 failures=1`, rc=1 | KILLED | 7990dc0e10aa0ada | `closed=8/9 exit=1`, rc=1 | KILLED |
| R5 | cd7c27cff3788c60 | `cases=9 failures=1`, rc=1 | KILLED | 9cb986fc483f0376 | `closed=8/9 exit=1`, rc=1 | KILLED |
| R6 | c39395121d636887 | `cases=9 failures=1`, rc=1 | KILLED | fd29bd279b1b328a | `closed=8/9 exit=1`, rc=1 | KILLED |
| R7 | edf23a9e86175670 | `cases=9 failures=1`, rc=1 | KILLED | 8b93cf3bc1fa099b | `closed=8/9 exit=1`, rc=1 | KILLED |
| R8 | 99b27115a9ee8fb1 | `cases=9 failures=1`, rc=1 | KILLED | be74a23c00b380ae | `closed=8/9 exit=1`, rc=1 | KILLED |
| R9 | 8240a328b18f9da6 | `cases=9 failures=1`, rc=1 | KILLED | 8cba2e4a8adcc46a | `closed=8/9 exit=1`, rc=1 | KILLED |

**18/18 killed, 0 survived, 0 inconclusive.** Every vacuous mutant's failing case line reads exactly
`selftest case=R# live=pass fixture=passed verdict=fail problems=fixture-not-rejected` (the other
eight cases stay `verdict=pass`); every deletion mutant's plain run prints 8 `check=` lines and
`closed=8/9 exit=1`.

Verbatim evidence, vac-R1 `--selftest` (rc=1):

```
selftest case=R1 live=pass fixture=passed verdict=fail problems=fixture-not-rejected
selftest case=R2 live=pass fixture=rejected verdict=pass
...
selftest cases=9 failures=1
```

Verbatim evidence, del-R1 plain run (rc=1): R2–R9 case lines then `closed=8/9 exit=1` (R1 line
absent). Mutant shape, vac-R1:

```
check_r1() {
  return 0  # MUTANT vacuous: check body unreachable
  cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }
```

Mutant shape, del-R5: `CHECK_IDS=(R1 R2 R3 R4 R6 R7 R8 R9)`,
`CHECK_FNS=(check_r1 check_r2 check_r3 check_r4 check_r6 check_r7 check_r8 check_r9)`,
`check_r5 definition present: False`.

Corroboration: matrix 1 (base `1cb16718…`+shim, an earlier landed version) killed the same 18/18
with identical detector outputs (`vacuous killed 9/9, deletion killed 9/9`).

## Controls

- **No-op** (`mut2/noop.sh`, sha256 identical to base `64338818…`): plain and selftest outputs
  byte-identical to Baseline B (`identical-to-B2: True/True`, rc=0/0) — **rejected as equivalent**
  (no behavior change claimed; procedure introduces no drift).
- **Non-compiling, mid-file** (`mut2/nc-midfile.sh`, stray `if` after `set -uo pipefail`):
  `bash -n` rc=2 ("syntax error: unexpected end of file from `if` command on line 76"), run rc=2,
  no stdout — **rejected** by both gates.
- **Non-compiling, trailing** (`mut2/nc-trailing.sh`, stray `fi` appended after `exit $?`):
  `bash -n` rc=2 — **rejected at the parse gate** — but a plain *run* exits **0** printing
  `closed=9/9 exit=0`, because bash parses scripts incrementally and the stray token sits on an
  unreachable line. Measured pitfall: a mutation harness that gates on runtime exit codes alone
  would score this invalid mutant as "no behavior change"; the validity gate must be `bash -n`
  (whole-file parse), which is what this seat's harness applies to every mutant.

## Transfer to the final landed bytes (`357a7e49…`)

Pin2 (`b7ea976b…`) vs live diff at seat end is confined to `build_broken_fixture` R8: the fixture
value changed from `2026-10-25T23:14:00-03:00` to `2026-10-25Tgarbage-not-a-timeZ` plus a comment —
fixture content only. A vacuous or deleted R8 check cannot change behavior based on fixture
content, but the spotcheck was run anyway on the exact live bytes (pin3 = `357a7e49…`, base3
`2f15dd76…`, `bash -n` rc=0 all): base3 plain `closed=9/9 exit=0` rc=0; vac-R8 `--selftest` →
`selftest case=R8 live=pass fixture=passed verdict=fail problems=fixture-not-rejected`, then
`selftest cases=9 failures=1`, rc=1; del-R8 plain → 8 case lines, R8 line absent,
`closed=8/9 exit=1`, rc=1. Verdicts transfer.

## Restoration / no-drift evidence

The lane instrument was never written by this seat; mutation happened only on scratch copies.
Suite-input digests recorded before and after each matrix were identical (matrix 2:
`SCORECARD.md b8fc8c66…`, `corpus/QUALITY.md 77d99df9…`, `corpus/lessons/round-33.md f69472f3…`,
`corpus/source-snapshots/round-26/manifest.json 33ac33c3…`,
`corpus/source-snapshots/round-32/manifest.json 72ab4e68…`,
`corpus/instruments/capture-binding-check.py 3d9e5e0d…`,
`corpus/instruments/frontier-recheck-count.py 1be79af6…`,
`.ufo/waves/round-34/c2-controls/junk-f17.md 2752a994…`). Baseline reruns at matrix end were
byte-identical to the matrix-start baselines (`B2==B2r` both detectors `True`). The only lane write
by this seat is this receipt file. (The instrument digest changes recorded above are the concurrent
writer's landings, not restorations by this seat.)

## Tooling

No tools installed or upgraded (bash, python3, coreutils only; nothing added to `~/.local/bin`).

## Report

Commands (all from the lane root unless noted; scratch base
`/fast/scratch/hyaku/kasegi-r34/MutRSuiteChecks`, `S`):

1. `sha256sum corpus/instruments/r-defect-closure.sh` ×2 (2 s apart) — digests differed
   (`149f411b…` → `abcd3de0…`), exposing the concurrent writer; follow-up 10 s sample stable at
   `7aca98b3…`.
2. `cp -p corpus/instruments/r-defect-closure.sh $S/pristine-r-defect-closure.sh` — pinned
   `1cb16718db160660227031542bd4cd08edfea3ac42d1c4b65c63a10697b19e7f` (663 lines).
3. `python3 $S/gen.py 2 <sha>` — built `base2.sh` (`64338818bcaa65b4f9759ff2fd2ab5f5000acca639f00a3993b73103ba697f32`
   = pin + 1-line LANE_ROOT shim), 18 mutants, 3 controls; `bash -n` rc=0 on all 18 mutants, rc=2
   on both NC controls. (Matrix 1 used the equivalent `base.sh`/`mut/` set from pin `1cb16718…`.)
4. `$S/run-matrix2.sh` — 46 detector runs (baselines A2/B2, NOOP2, NCt/NCm parse+run, 9×
   {vac,del}×{plain,selftest}, B2r rerun), exit-code files under `$S/out2/*.rc`, `DRIVER2-DONE`,
   wall 7.5 s; matrix 1 (`run-matrix.sh`, 9.4 s) identical in design.
5. Analysis pass over `$S/out2/` — verdicts above; `bash -n` gate re-verified per mutant.
6. Pin3 spotcheck on live bytes `357a7e49…`: `base3.sh`/`mut3-{vac,del}-R8.sh` (`bash -n` rc=0) →
   base3 plain rc=0 `closed=9/9 exit=0`; vac-R8 selftest rc=1 `cases=9 failures=1`; del-R8 plain
   rc=1 `closed=8/9 exit=1`.
7. Key digests: pin1 `1cb16718…`, pin2 `b7ea976b0954b834d0e958b0a0cc82ee0917bf27ce5ea9b20ac4802a0fbf4d7c`,
   pin3/live `357a7e4923bf784cd513dfaa94258d4cb6d5dfc1cbb677b36accbab86a05bc2d`, base2
   `64338818…`, base3 `2f15dd7652adb89b…`(16), all 18 matrix-2 mutant digests in the table above.

**Findings for the L1:**
1. The C1 suite's self-discipline is real: all 18 targeted mutants (9 vacuous, 9 deletions) are
   killed by the assigned detectors; no coverage gap found at the check level.
2. Deletion mutants are caught only by the plain run's counted `closed=K/9` (selftest merely prints
   `cases=8 failures=0`); the count is derived, not hardcoded — `closed=9/9` cannot print with a
   check missing.
3. Harness-design pitfall measured (applies to any future mutation harness on this suite): gate
   mutant validity on `bash -n`, never on runtime exit codes — a trailing syntax error after
   `exit $?` runs to completion with exit 0.
4. Environment: the pristine instrument was landed iteratively by a concurrent writer during the
   seat (six observed digest states); all verdicts were re-established on the final bytes via pin3.
