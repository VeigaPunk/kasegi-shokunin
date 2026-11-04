# NOTES — ExecSignalProbes (kasegi r65 w1)

Predata signal-fail-closed probe receipts. Nothing here is admitted by itself; L1
(KasegiR65) is the sole production integrator.

## Deliverables (this directory)

| file | what it is |
|---|---|
| `c1-signal-probes.py` | the collector: `--instrument PATH --work PATH --mode base\|candidate`, plus `--selfcheck` |
| `probes-base.txt` | one collector run (exit 1) against the production gate, mode=base |
| `probes-candidate.txt` | one collector run (exit 0) against ExecSignalGate's candidate, mode=candidate |
| `selfcheck.txt` | one `--selfcheck` run (exit 0): always-green stub must tally failures=6 |
| `work/` | fixture root + per-probe ledgers + stub, rebuilt byte-identically by every run (`--work`) |

Each receipt is the unedited stdout+stderr of exactly one collector invocation,
written by that invocation itself. Fixture helpers are built under `--work`
(never /tmp): `work/root/g.txt` ("35\n"), `work/root/corpus/instruments/{kill.py,
sigkill.py,bigwriter.py}`, `work/ledgers/P1..P6.json`, `work/stub-figure-audit.py`.
`kill.py` is byte-identical to the gate's own selftest fixture
(`import os, signal\nos.kill(os.getpid(), signal.SIGTERM)`); `sigkill.py` is its
SIGKILL twin; `bigwriter.py` restores `SIGPIPE` to `SIG_DFL` and writes ~2.5 MiB
in flushed 64-byte lines so `head -1` kills it with a real SIGPIPE (Python's
default SIGPIPE-ignore would turn the death into a BrokenPipeError exit 1, which
is a different, non-benign defect class).

## Instruments under test (sha256, printed in each receipt header)

| mode | instrument | sha256 |
|---|---|---|
| base | `corpus/instruments/figure-audit.py` (production, base master a283189b) | `8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9` |
| candidate | `.ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py` (polled once — present, so no throwaway candidate was needed) | `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef` |
| selfcheck | `work/stub-figure-audit.py` (deliberately always-green) | `62a308f22bd7b5e6149841404347a2a54727e071f7097cf2401eb91c57a6eb5d` |

## Exact native returncodes (measured, identical across all three receipts)

Printed as `NATIVE <id> stage=<i> rc=<n>` lines in every receipt; the collector
replays each pipeline with a plain subprocess harness (argv only, no shell, no
gate) independently of the audit:

| probe | pipeline | stage 0 rc | stage 1 rc |
|---|---|---|---|
| P1 | `python3 corpus/instruments/kill.py \| wc -l` | **-15 (SIGTERM)** | 0 |
| P2 | `python3 corpus/instruments/sigkill.py \| wc -l` | **-9 (SIGKILL)** | 0 |
| P3 | `cat g.txt \| python3 corpus/instruments/kill.py` | 0 | **-15 (SIGTERM)** |
| P4 | `python3 corpus/instruments/bigwriter.py \| head -1` | **-13 (SIGPIPE)** | 0 |
| P5 | `cat g.txt \| wc -l` | 0 | 0 |
| P6 | `grep absent g.txt \| wc -l` | **1 (no match)** | 0 |

The signals are real, not simulated: the collector cross-binds each stale
expectation to the NATIVE rc of the dying stage measured in the same run and
prints `NATIVE-ANOMALY` + fails the probe if they ever disagree.

## Measured results

### base (probes-base.txt, exit 1, `PROBES probes=6 failures=1`)

| probe | assigned base claim | measured |
|---|---|---|
| P1 | ok (false green) | `verdict=ok reason=-` audit_exit=0 — **false green confirmed** |
| P2 | ok (false green) | `verdict=ok reason=-` audit_exit=0 — **false green confirmed** |
| P3 | ok (false green) | `verdict=stale reason=derive-exit--15` audit_exit=1 — **claim falsified, see below** |
| P4 | ok | `verdict=ok reason=-` audit_exit=0 (SIGPIPE non-final benign at base) |
| P5 | ok | `verdict=ok reason=-` audit_exit=0 |
| P6 | ok | `verdict=ok reason=-` audit_exit=0 (grep exit1 ordinary no-match) |

**Falsification — the assigned base expectation "P3 reads ok" does not hold at
base master a283189b.** With the producer as the FINAL stage, `run_derive`'s
`if status != 0` fires on the negative returncode and the gate reports
`derive-exit--15`: the figure is already stale at base, so no ok-flip is
available for the candidate. What base actually gets wrong on P3 is the LABEL:
a signal death is printed as an exit status (`derive-exit--15`), so a consumer
cannot distinguish "died by SIGTERM" from "exited -15", and the gate docstring's
"negative signal statuses remain ignored" overstates the safety. The corrected
base statement for the freeze is: *P3 base = stale with the malformed
`derive-exit--N` label; candidate obligation = relabel to `derive-signal-N`
(never `derive-exit--N`), not flip to stale.* (QUALITY R22/R25-style
satisfiability: fix the literal before data.)

### candidate (probes-candidate.txt, exit 0, `PROBES probes=6 failures=0`)

ExecSignalGate's candidate fails closed exactly as intended: P1
`derive-upstream-signal-15`, P2 `derive-upstream-signal-9`, P3 exact final label
`derive-signal-15` (no `derive-exit--` spelling), P4/P5/P6 stay ok. The
collector accepts either `derive-signal-N` or `derive-upstream-signal-N` for the
upstream probes (the intent pins "a reason naming the signal", not a spelling)
but pins P3 to exactly `derive-signal-15` per the intent, and rejects any
`derive-exit--` spelling outright.

### selfcheck (selfcheck.txt, exit 0)

`--selfcheck` rebuilds an always-green stub gate, runs the full suite against it
in BOTH modes under the fail-closed (candidate) expectation model, and requires
failures=6 = the three signal probes flagged in each mode (3 x 2). Measured:
`PROBES probes=6 failures=3` per run, `SELFCHECK probes=6 runs=2 failures=6
want=6 verdict=pass`, exit 0. This proves the collector is not a rubber stamp:
an instrument that greens everything fails all six-selfcheck assertions, and the
receipt shows the stub reading `verdict=ok` on stages the NATIVE lines show died
by -15/-9. During development the selfcheck caught a real lens bug (first
version demanded stale on all six probes per run, tallying 12); the fixed
collector produced all three receipts above, so every receipt comes from the
delivered bytes.

## Expectation model (as assigned, encoded verbatim)

- base: P1..P6 all `verdict=ok reason=-`.
- candidate: P1/P2/P3 `verdict=stale` with reason naming the signal (P3 exactly
  `derive-signal-15`); P4/P5/P6 `verdict=ok reason=-`. Signal numbers are
  cross-bound to the measured NATIVE rcs (15/9/15; P4's -13 is the documented
  benign non-final SIGPIPE positive control).

## Tools installed

None (no RULES.md authorization needed; host pacman pause untouched).
