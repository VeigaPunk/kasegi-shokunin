# ExecDriver — r65 predata C1 driver (verify-r65.py)

Seat: ExecDriver (leaf). Scope: author the frozen-shape committed-input driver for
claim C1 and prove its red-at-base and green-with-candidate shapes. No production
file was edited; all writes are under `.ufo/waves/round-65/w1/ExecDriver/` plus this
report and the sanctioned scratch `/fast/scratch/hyaku/kasegi-r65/ExecDriver/`
(removed after receipt copy).

## Files delivered

- `w1/ExecDriver/verify-r65.py` — the driver (sha256
  `064404510b71825016b71a8db0d7a341ee17e6317cc5758ac0a3b9c89d754a60`).
- `w1/ExecDriver/driver-trial-base.txt` (+ `.command.json`) — trial at base
  a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b: `VERIFY measurements=8 failures=6`,
  exit 1 (required: failures>=3, exit 1).
- `w1/ExecDriver/input-list.txt` (+ `.command.json`) — `--print-inputs` at the base.
- `w1/ExecDriver/driver-trial-candidate-fixture.txt` (+ `.command.json`) — extra
  predata evidence: full 8/8 green (`failures=0`, exit 0) on a fixture commit with
  the real sibling artifacts; NOT a final run (pins absent).

## Driver shape

CLI `--revision <rev> --work <dir> [--final] [--candidate PATH] [--print-inputs]`.
Exports the committed tree with `git archive` into `--work` (guarded to
`/fast/scratch/hyaku/kasegi-r65`, >=7 path parts), writes a `gitdir:` pointer to the
lane object store, sets `GIT_NO_REPLACE_OBJECTS=1` (host-bound, not hermetic).
Enumerated inputs: production gate, ledger, old mutbat, collector
(`w1/ExecSignalProbes/c1-signal-probes.py`), signal battery
(`w1/ExecSignalMutants/signal-mutbat.py`), plus the driver itself and
`.ufo/waves/round-65/claims.json` (pins source). `--print-inputs` lists each with
sha256 or `INPUT-MISSING` (that is the freeze list for the L1's `input_sha256`).

Eight measurements, each ending `RESULT <name> PASS|FAIL`, summary
`VERIFY measurements=8 failures=<n> revision=<rev>`, exit 1 on any failure, 2 on
setup error:

1. `collector-base` — collector, base expectations, against the production gate
   blob pinned at the round base a283189b. Pinned expectation is the documented
   false green: exit 1 + `PROBES probes=6 failures=1` (base flags only the
   final-stage signal P3; upstream signals P1/P2 stay swallowed).
2. `candidate-collector` — collector, candidate expectations, against the overlay
   if given else the committed gate: exit 0 + `PROBES probes=6 failures=0`. Must
   FAIL on a limbless tree (demonstrated: candidate mode on the base gate gives
   failures=3).
3. `collector-selfcheck` — `--selfcheck` (no instrument/mode, per collector CLI):
   exit 0 + `SELFCHECK probes=6 runs=2 failures=6 want=6 verdict=pass`.
4. `selftest` — candidate-or-merged gate `--selftest`: exit 0, one
   `selftest cases=<n> failures=0` with n>=59, every case line `verdict=pass`,
   case count == summary count. Fails closed without overlay (predata trial).
5. `old-mutbat` — committed `figure-audit-mutbat.py --instrument <measured>`:
   exit 0 + `mutbat killed=5/5 survivors=0 invalid=0 controls=pass`.
6. `signal-mutbat-and-equivalents` — committed `signal-mutbat.py --instrument
   <measured> --work <work>/battery`: exit 0 + one
   `SUMMARY killed=<k>/<k> survivors=0 equivalents_held=2 controls_held=1
   invalid_rejected=1` (regex backreference pins killed==total) + one
   `verdict limb-verified limb=<x> limb_contract=pass`. Fails closed without
   overlay (predata trial).
7. `collector-forgeries` — driver-built, both rejected by the collector's own
   mode comparison in candidate mode: (a) forged receipt = the base gate's honest
   per-probe transcripts captured with the collector's own
   `build_fixtures/write_ledger/run_audit`, replayed keyed by probe id; (b) an
   independently written always-green counterfeit. Each must exit 1 with exactly
   `PROBES probes=6 failures=3` and no `HARNESS-ERROR`/`NATIVE-ANOMALY` line.
8. `real-ledger` — measured gate on the committed ledger: exit 0 +
   `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`.

Guards verified by execution: `--final --candidate` ->
`VERIFY-ERROR final-refuses-construction-override` exit 2; `--final` at a revision
without `claims.json` -> `pins-missing-at-revision` exit 2; `--work` outside the
floor -> `work-not-owned` exit 2; committed-driver byte identity enforced whenever
the driver exists at the revision (`driver-not-committed-bytes`), and required in
`--final` (`driver-not-committed-at-revision`). In `--final`, every input must
exist at the revision and match `claims.json:input_sha256`.

## Evidence (commands actually run)

- `python3 -B <w1>/verify-r65.py --revision a283189b… --work
  /fast/scratch/hyaku/kasegi-r65/ExecDriver/trial` -> exit 1, failures=6:
  collector-base / candidate-collector / collector-selfcheck /
  collector-forgeries FAIL `missing-committed-input` (round files are not in the
  base tree), selftest + signal-mutbat FAIL `candidate-overlay-absent`;
  old-mutbat PASS (`killed=5/5 survivors=0 invalid=0 controls=pass`), real-ledger
  PASS (`figures=35 ok=35 stale=0 exit=0`). Receipt delivered.
- Fixture clone (the one sanctioned clone,
  `/fast/scratch/hyaku/kasegi-r65/ExecDriver/clone-r65`, toplevel asserted, throwaway
  identity used only inside it, commit 6cb9a995266bfaab6bda15551bb228d5de0e4252 =
  base tree + collector + battery + driver at `.ufo/waves/round-65/verify-r65.py`),
  then `--revision 6cb9a995… --candidate w1/ExecSignalGate/figure-audit.py` ->
  exit 0, all 8 RESULT PASS, `failures=0`. Candidate sha256
  `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`. This also
  cross-validates the sibling artifacts: candidate selftest `cases=63 failures=0`,
  battery `limb-verified` with `derive-upstream-signal-15/9`, `derive-signal-15`,
  P4 SIGPIPE stays ok, forgeries rejected 3/3, old mutbat anchors intact on the
  candidate, real ledger 35/35 under the candidate.
- Guards as listed above; `--print-inputs` at the base lists the production trio
  (gate `8d92eaa0…`, ledger `28ad7fef…`, mutbat `7a61cf1e…`) and the round files
  `INPUT-MISSING`.

## Interpretations the L1 should ratify at freeze

1. `collector-base` is anchored to the base-revision gate blob (r64 `BASE` pin
   pattern) so it stays green after the limb lands; measured-revision-gate +
   base expectations would go red at final by construction.
2. The `collector-base` pin is `failures=1`, not 0: at base the gate already
   flags the final-stage signal (`derive-exit--15`); only the upstream signals
   are swallowed. The probes seat's own `probes-base.txt` shows the same.
3. Without `--candidate` (predata shape): M2 runs and fails against the committed
   tree (this is the limbless-tree red evidence), M4 and M6 fail closed without
   running (`candidate-overlay-absent`). At `--final` (no overlay allowed) M2/M4/M6
   run against the merged committed gate.
4. `--print-inputs` includes `claims.json`; `input_sha256` keys should cover the
   five PATHS entries plus `verify-r65.py` (r64 convention).

## Risks / limits

- The fixture green run is host-bound (signals, PATH tools, lane git objects) and
  used a clone, not the freeze commit; it is predata evidence, not the claim.
- M4's floor (>=59 cases) admits candidate-added cases (63 observed); it does not
  pin 63 exactly — the candidate may legitimately add cases.
- If a sibling file changes after my run (collector `855af8df…`, battery
  `5050d853…`, candidate `86becbde…` as measured in the fixture smoke), the L1
  must re-run the smoke before freezing pins.

No tool installs were needed (python3 + system git/tar only). No pacman
transactions. Scratch removed on exit.
