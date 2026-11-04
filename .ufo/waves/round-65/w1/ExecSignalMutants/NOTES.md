# NOTES — seat ExecSignalMutants (R65 signal-limb mutation battery)

## Deliverable
`signal-mutbat.py` — exact-once mutation battery over the C1 signal fail-closed limb of the
figure-audit derive gate, following the lane's mutbat convention
(`corpus/instruments/figure-audit-mutbat.py`: single-site anchors, compile check, controls,
summary line).

CLI (as dispatched):
```
python3 .ufo/waves/round-65/w1/ExecSignalMutants/signal-mutbat.py \
  --instrument <figure-audit.py> --work /fast/scratch/hyaku/kasegi-r65/ExecSignalMutants/work
```
Exit codes: 0 coherent run (verdict in printed lines), 2 incoherent (exact-once violation,
ambiguous anchor, mixed limb presence, compile failure on a live mutant, control that
compiles, probe infrastructure error). The battery is differential: every mutant is scored
against the SAME instrument's unmutated baseline; a mutant is killed when any probe outcome
(audit_exit, verdict, reason) changes.

## Probe engine — same collector contract, cross-checked
Six probes identical in derivation and observation shape to seat ExecSignalProbes'
`c1-signal-probes.py` (P1 SIGTERM producer, P2 SIGKILL producer, P3 final-stage signal,
P4 SIGPIPE non-final via >1 MiB writer into `head -1`, P5 clean pipeline, P6 grep no-match),
scored on audit_exit + verdict + reason. Implemented inside the battery so it is
self-contained; cross-checked against their `probes-base.txt`: native stage rcs
P1 −15, P2 −9, P3 final −15, P4 −13 (non-final), P6 grep exit1, and identical base verdicts
(p1/p2 ok false green, p3 `derive-exit--15`, p4/p5/p6 ok). My P4 helper restores
`SIGPIPE → SIG_DFL` before writing ~2.4 MiB so the writer dies with a real −13, not a
Python `BrokenPipeError`; the candidate's own selftest helper (`pipe.py`) uses the same
mechanism, independently corroborating it.

## Mutation anchors (verified against the candidate's actual text)
Instrument under test at run time: candidate `w1/ExecSignalGate/figure-audit.py`
(sha256 86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef). Real limb text:
- upstream limb, `upstream_stale` (candidate lines 90–91):
  `    if status < 0:` / `        return status != -signal.SIGPIPE`
- final-stage signal label, `run_derive` (candidate line 127), guarded by `if status < 0:`:
  `return None, out, "derive-signal-%d" % -status`

| id | old → new (single site) | expected kill |
|---|---|---|
| m1-negative-benign-again | two-line upstream limb → `if status < 0:` / `        return False` | p1+p2 stale→ok (false green restored; audit_exit 1→0) |
| m2-sigkill-benign | `return status != -signal.SIGPIPE` → `return status not in (-signal.SIGPIPE, -signal.SIGKILL)` | p2 stale→ok; p1 stays stale (partial limb) |
| m3-old-final-label | `"derive-signal-%d" % -status` → `"derive-exit-%d" % status` | p3 reason `derive-signal-15` → `derive-exit--15` (the old malformed label: `% status` carries the negative sign) |
| m4-no-sigpipe-exemption | `return status != -signal.SIGPIPE` → `return True` | p4 ok→stale `derive-upstream-signal-13` |
| eq1-extract-local | limb → `sigpipe = -signal.SIGPIPE` / `return status != sigpipe` | must hold (extract-local refactor) |
| eq2-abs-negation | label → `"derive-signal-%d" % abs(status)` | must hold: enclosing branch guard is `status < 0`, so `abs(status) == -status` on the whole reachable domain |
| ctrl-syntax-error | `def upstream_stale(head, status):` → `def upstream_stale(head status):` | must fail to compile → rejected, never counted killed |

m1 scope: the C1 regression is the UPSTREAM false green ("negative signal statuses remain
ignored" at base); a final-stage signal was already stale at base (as `derive-exit--15`), so
"benign again" applies to the upstream limb only; the final label regression is m3's subject.

On an instrument where a signal anchor is absent (the production gate), the mutant is
reported as a survivor with `anchor=absent`; all six anchors are required to be present
(limb=present) or absent (limb=absent) together — a mixed state is incoherent (exit 2).

## Results
- Candidate (`mutbat-candidate.txt`): `SUMMARY killed=4/4 survivors=0 equivalents_held=2
  controls_held=1 invalid_rejected=1`, `verdict limb-verified limb=present
  limb_contract=pass`. Baseline contract pass: p1 stale `derive-upstream-signal-15`, p2
  stale `derive-upstream-signal-9`, p3 stale `derive-signal-15`, p4/p5/p6 ok, audit_exit=1.
  Every mutant killed by exactly the expected probe flips (receipt lists them).
- Production gate at base a283189 (`mutbat-base.txt`, sha256
  8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9 — byte-identical to the
  instrument the probes seat measured): every signal anchor absent →
  `SUMMARY killed=0/4 survivors=4 equivalents_held=2 controls_held=1 invalid_rejected=1`,
  `verdict limb-absent-survivors limb=absent limb_contract=fail`. This is the absent-limb
  evidence and the not-always-red proof: the same battery kills 4/4 on the candidate.
  Base-run equivalents are vacuously held (anchor absent) and marked `vacuous=1` in the
  receipt. Base baseline matches the pinned control
  `.ufo/waves/round-65/controls/do-nothing-signal-base-r65.txt` figure-for-figure.
- Battery exit codes 0/0, embedded as `battery_exit=` lines in the receipts; interpreter
  recorded in `runlog.txt`.

## Defects found and fixed in my own battery before the final receipts
1. Control-anchor selection initially summed hits over both alternatives and declared the
   base run incoherent (both `def upstream_stale(...)` and `import json` match once each in
   any healthy gate). Fixed to: first alternative matching exactly once; none usable → exit 2.
2. m3's replacement first read `"derive-exit-%d" % -status`, printing `derive-exit-15`
   instead of the old malformed `derive-exit--15` (the sign must ride inside `% status`).
   The mutant was killed either way, but the delivered mutant now reproduces the specified
   regression label exactly.

## Bounds
Mutants were applied only to scratch copies under `--work`; no production byte changed; no
installs (stock `python3`, see `runlog.txt`); no git operations; no subagents; scratch is
`/fast/scratch/hyaku/kasegi-r65/ExecSignalMutants/` and is removed after the receipts.
