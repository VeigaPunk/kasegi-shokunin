# Report — ExecSignalProbes (kasegi r65 w1)

Seat scope: author the six-probe signal collector, run it base/candidate/selfcheck,
deliver receipts. Leaf; no commits; nothing admitted by itself.

## Files written (all under `.ufo/waves/round-65/w1/ExecSignalProbes/`)

- `c1-signal-probes.py` — collector, CLI `--instrument PATH --work PATH --mode base|candidate` + `--selfcheck`
- `probes-base.txt` — base run vs production gate (exit 1, `PROBES probes=6 failures=1`)
- `probes-candidate.txt` — candidate run vs ExecSignalGate's candidate (exit 0, `PROBES probes=6 failures=0`)
- `selfcheck.txt` — always-green stub run (exit 0, `SELFCHECK probes=6 runs=2 failures=6 want=6 verdict=pass`)
- `NOTES.md` — full measurement record, exact native returncodes, falsification detail
- `work/` — fixture root, per-probe ledgers, stub (rebuilt by every run under `--work`, never /tmp)

## What ran (exact commands)

```
python3 <seat>/c1-signal-probes.py --instrument corpus/instruments/figure-audit.py --work <seat>/work --mode base
python3 <seat>/c1-signal-probes.py --instrument .ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py --work <seat>/work --mode candidate
python3 <seat>/c1-signal-probes.py --selfcheck --work <seat>/work
```

Each receipt is the unedited stdout+stderr of one invocation, written by that
invocation. Instrument identities are pinned in every receipt header (sha256):
base `8d92eaa0…`, candidate `86becbde…`, stub `62a308f2…`.

## Findings

1. **P1/P2 false green confirmed at base.** Native stage rcs prove real signals
   (P1 producer -15 SIGTERM, P2 producer -9 SIGKILL); the base gate reads both
   figures `ok` (audit_exit=0). Matches the pinned selftest case
   `upstream-python-signal-ignored` (exit 0) and extends it to SIGKILL, which no
   base selftest case covers.
2. **Claim defect — base P3 does NOT read ok.** The assigned base expectation
   "P1/P2/P3 read ok" is falsified for P3: with the signal-killed producer as
   FINAL stage, the gate reports `verdict=stale reason=derive-exit--15`
   (audit_exit=1). Base's P3 defect is the LABEL (signal death printed as an
   exit status), not a missed stale verdict. Recommend restating the frozen
   base expectation before data: *P3 base = stale with `derive-exit--N` label;
   candidate obligation = exact `derive-signal-N` relabel* (R22/R25-style
   satisfiability fix, pre-freeze).
3. **ExecSignalGate's candidate passes all six probes** (candidate poll hit —
   file present, so no throwaway candidate was used): P1
   `derive-upstream-signal-15`, P2 `derive-upstream-signal-9`, P3 exact
   `derive-signal-15` (no `derive-exit--` spelling), P4 SIGPIPE -13 non-final
   stays benign with output intact, P5/P6 positives green.
4. **Selfcheck discriminates.** Against a deliberately always-green stub the
   collector reports failures=6 (three signal probes flagged in each mode,
   fail-closed lens 3x2) and exit 0 only on exactly 6. The selfcheck caught a
   lens bug during development (12 vs 6); all delivered receipts come from the
   fixed collector bytes.

## Exact native returncodes (printed as NATIVE lines in every receipt)

P1: -15/0 · P2: -9/0 · P3: 0/-15 · P4: -13/0 · P5: 0/0 · P6: 1/0
(stage0/stage1; collector cross-binds stale expectations to these measured rcs
and prints NATIVE-ANOMALY + fails if they diverge).

## Verification others should run

```
python3 .ufo/waves/round-65/w1/ExecSignalProbes/c1-signal-probes.py --instrument corpus/instruments/figure-audit.py --work .ufo/waves/round-65/w1/ExecSignalProbes/work --mode base   # expect exit 1, failures=1 (P3)
python3 .ufo/waves/round-65/w1/ExecSignalProbes/c1-signal-probes.py --instrument .ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py --work .ufo/waves/round-65/w1/ExecSignalProbes/work --mode candidate  # expect exit 0
python3 .ufo/waves/round-65/w1/ExecSignalProbes/c1-signal-probes.py --selfcheck --work .ufo/waves/round-65/w1/ExecSignalProbes/work  # expect exit 0, failures=6
```

## Risks / blockers

- None blocking. The candidate matcher accepts `derive-signal-N` or
  `derive-upstream-signal-N` for the upstream probes (intent pins "a reason
  naming the signal") but pins P3 to exactly `derive-signal-15` and rejects any
  `derive-exit--` spelling — if L1's freeze wants a different upstream spelling,
  only `CANDIDATE_STALE` matching in `probe_matches` needs a look.
- Tools installed: none. Scratch `/fast/scratch/hyaku/kasegi-r65/ExecSignalProbes/`
  removed on exit after receipts landed in-lane.
