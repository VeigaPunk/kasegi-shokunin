# Report — ExecSignalMutants (R65 w1)

## Files changed (all under my seat dir)
- `.ufo/waves/round-65/w1/ExecSignalMutants/signal-mutbat.py` — exact-once mutation battery
  over the C1 signal limb (4 signal mutants m1–m4, 2 must-hold equivalents, 1 invalid
  control; differential scoring on the same six-probe collector contract as
  ExecSignalProbes: audit_exit + verdict + reason).
- `.ufo/waves/round-65/w1/ExecSignalMutants/mutbat-candidate.txt` — run against the
  ExecSignalGate candidate (sha256 86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef).
- `.ufo/waves/round-65/w1/ExecSignalMutants/mutbat-base.txt` — same battery against the
  production gate at base a283189 (sha256 8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9,
  byte-identical to the instrument ExecSignalProbes measured in `probes-base.txt`).
- `.ufo/waves/round-65/w1/ExecSignalMutants/NOTES.md`, `runlog.txt` — method, anchor table,
  defect log, interpreter (Python 3.14.8).

## Behavior / result
Commands actually run (both from `/fast/scratch/hyaku/kasegi-r65/ExecSignalMutants`):
```
python3 <seat>/signal-mutbat.py --instrument corpus/instruments/figure-audit.py \
  --work /fast/scratch/hyaku/kasegi-r65/ExecSignalMutants/work   -> mutbat-base.txt,   exit 0
python3 <seat>/signal-mutbat.py --instrument <w1>/ExecSignalGate/figure-audit.py \
  --work /fast/scratch/hyaku/kasegi-r65/ExecSignalMutants/work   -> mutbat-candidate.txt, exit 0
```
- Candidate: `SUMMARY killed=4/4 survivors=0 equivalents_held=2 controls_held=1
  invalid_rejected=1`; `verdict limb-verified limb=present limb_contract=pass`. Kill map:
  m1 flips p1+p2 stale→ok (false green restored), m2 flips p2 only (SIGKILL benign,
  SIGTERM still refused), m3 flips p3 `derive-signal-15`→`derive-exit--15`, m4 flips p4
  ok→stale `derive-upstream-signal-13`; eq1/eq2 zero flips; control rejected on
  `compile` (invalid syntax), never counted killed.
- Production gate at base: every signal anchor absent (verified present-or-absent as an
  all-or-nothing invariant) → `SUMMARY killed=0/4 survivors=4 equivalents_held=2
  controls_held=1 invalid_rejected=1`; `verdict limb-absent-survivors limb=absent
  limb_contract=fail`. Proves the limb is absent at base AND that the battery is not
  always-red (4/4 kills on the candidate) and not over-sensitive (2 equivalents held).
- Base baseline reproduces the pinned control
  `.ufo/waves/round-65/controls/do-nothing-signal-base-r65.txt` figure-for-figure
  (p1/p2 ok false green, p3 `derive-exit--15`, audit_exit=1), and agrees with
  ExecSignalProbes' `probes-base.txt` native rcs (−15, −9, −15, −13 non-final).

## Anchors (exact-once, verified against the candidate's real text)
- upstream limb (candidate `upstream_stale` L90–91): `    if status < 0:` /
  `        return status != -signal.SIGPIPE`
- final label (candidate `run_derive` L127, guarded by `status < 0`):
  `return None, out, "derive-signal-%d" % -status`
m1 scope note: the C1 regression is the upstream false green; final-stage signals were
already stale at base (as `derive-exit--15`), so "benign again" targets the upstream limb
and the malformed final label is m3's subject. eq2's `abs(status)` == `-status` holds on
the whole reachable domain because the branch guard is `status < 0`.

## Defects fixed in my own battery before final receipts
(1) control-anchor counting declared healthy gates incoherent (summed both alternatives);
now uses the first alternative matching exactly once. (2) m3 first printed
`derive-exit-15` instead of the old malformed `derive-exit--15` (sign must ride in
`% status`); killed either way, now reproduces the specified label exactly.

## Risks / blockers
- None blocking. Anchors are tied to the candidate's current spelling; a different
  candidate revision would report survivors with `anchor=absent` (visible in receipts),
  never a silent pass — and any mixed anchor state exits 2.
- My probe engine is an in-battery implementation of the shared collector contract
  (deliberately self-contained); it is cross-checked, not derived from,
  ExecSignalProbes' file.
- Bounds kept: no production byte touched (mutants live only under `--work`), no installs,
  no git operations, no subagents; scratch removed after receipts.
