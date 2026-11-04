# ExecMultiHeadDriver — round-67 w1 seat report (C1 committed-input driver)

Seat: ExecMultiHeadDriver (leaf; no spawns, no delegations, no `task`, no `agent://all`).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin at base 8e2a8fe8eb92d7c824902a4b70aab027a9aacee0
(= HEAD at seat start; production gate 51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac).
Scratch: /fast/scratch/hyaku/kasegi-r67/ExecMultiHeadDriver/ — deleted before yielding (verified below).

## Deliverables

- Driver: `.ufo/waves/round-67/w1/ExecMultiHeadDriver/verify.py` — sha256
  **bd82b15be71622f3550aeecf27b72c73b24bb6b125b44193e430138cbf227b6f**
  (fork of `.ufo/waves/round-66/w1/ExecCatDriver/verify.py`, architecture preserved).
- Pin manifest (authored): `.ufo/waves/round-67/controls/driver-pins.json` — file sha256
  **3a279dccde57ed1297ba785c5f6b47c2be3260a4a218ac7a3ff2a193032e836a**; canonical
  `pins_sha256` printed by both runs: `6cb4506fab9bed49965c48c2efa70df0c7ddeab3f09a326095b1d03d01cedd7d`.
- Raw demonstration outputs: `driver-base-r67.txt` (sha256 60ba79261592d001a6f556bfeaa1fbf3e2a9d4631e28c6e99b83fbcddf27e8f0)
  and `driver-candidate-r67.txt` (sha256 d84105234aa3743e4f527649ac381216eab13cb43206d287e336b3eecf6eb9ac).
- Per-child receipts: `receipts/base/` (287 files) and `receipts/candidate/` (263 files),
  including `index.json`, `closure.tsv`, `probes-base-paired.txt`, `probes-measured.txt`,
  `faces-base-paired.txt`, `faces-measured.txt` (every `FACE` line), per-shape/face gate
  outputs, `selftest.txt`, `mutbat.txt`, `multihead-mutbat.txt`, `real-ledger.txt`, `red-wrong-want.txt`.

## Architecture kept from round-66 (per seat spec)

Controls and pin manifest read from `--controls-revision` via `git show` (never the worktree);
measured tree exported in ONE scratch shared clone under `--work`; paired base gate bytes from
the manifest base; opaque fixture ids (`<key>-probe-spelling` vs `held-<sha10>`, and digest-based
face ledger ids) so a path- or id-keyed oracle cannot pass; receipts under `WORK/receipts`;
children in their own process group, group-killed on timeout; `VERIFY-SETUP reason=...` + exit 2
on setup failure; `MEASUREMENTS` exactly the ordered 12 names (driver-self-pin, controls-pins,
ledger-closure, probes-base-paired, probes-measured, shape-identity, selftest, mutbat-existing,
multihead-mutbat, real-ledger, red-wrong-want, identity-guards); final line
`VERIFY measurements=12 failures=N revision=REV mode=base|candidate|final`. `--final` still
refuses `--candidate`, reads only the lane repo, requires committed controls, and binds
`measured.gate_sha256` (fail-closed). No `--final` run was made: production is the L1's to change.

## Round-67 changes

- Constants to r67 paths (`SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r67`, wave, driver/pins/probes
  relpaths); `multihead-mutbat` replaces `cat-mutbat` unconditionally (12 names, no flag).
- Expectation tables from L1 evidence (`controls/base-matrix-r67.txt`, `controls/native-statuses-r67.txt`,
  `controls/dispatch-addendum-r67.md`, two L1 correction messages), not from probes.py: fixed rows
  P1/P2 stale signal-13 both modes, P5 derive-exit-1, P15 derive-upstream-exit-1, P8/P18 rc0 both
  modes, P12..P14/P16/P17 rc0. Repair rows P9/P10/P11 are FACE-CONDITIONAL (L1 ruling).
- `multihead-mutbat` measurement: committed battery (pinned 937f8677fb6276635501ac8b6fa6cbe631e7d5ef9dc3b8a2e1cc0c7f9b66e233)
  run as `--instrument <gate> --collector <probes.py> --work <dir>`; requires exit 0 and exactly
  `MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0 failures=0` at candidate kind
  (same want at base kind → honest red at base).
- Pin manifest carries content pins for: gate (base_gate_sha256 + measured.gate_sha256),
  probes (probes.py), mutbats (multihead-mutbat.py + tree figure-audit-mutbat.py), claims
  (donothing-multihead-r67.{txt,py}, native-statuses-r67.txt, base-matrix-r67.txt,
  dispatch-addendum-r67.md, c2-base-counters-r67.txt), ledger, driver self, plus expected blocks.
  8 controls pinned; `controls-pins` verified all 8 against the controls revision in both runs.

## Face-conditional semantics (L1 ruling + measured refinement)

The gate re-executes the derive itself, so a replay's stage0 and a gate run's internal face can
desync (observed: replay −13 while the base gate's own run printed stale:derive-upstream-exit-1).
Per-run face is therefore attributed by the run's own observable (its stale reason); the replay
loop proves −13 reachability. Assertions per repair shape: replay hits −13 ≥1 in ≤20 attempts
(else FAIL); base column: every run ok or stale:{exit-1,exit-2}, never stale:signal-13, and ≥1 ok
run per shape (= the masked −13 faces, the false green, re-derived); measured column: every run
stale with reason in {signal-13, exit-1, exit-2} and ≥1 stale:signal-13 run per shape (the
SIGPIPE-face refusal observed). Deviation from the ruling's literal attempt-pairing reported to L1
(desync makes literal pairing flake red); FACE line format unchanged.

## Demonstrations (no production bytes modified; scratch fixture source repo)

No lane commit carries the round-67 controls yet, so both runs used a fixture source repo:
lane `clone --shared --no-checkout` at 8e2a8fe8 + one commit adding the pinned controls
(`user.name=ExecMultiHeadDriver-fixture`, inside the scratch fixture only; toplevel asserted equal
before commit). Controls revision: 8099db4ac9d2b61948efbd7baf433201ff47c819.

(a) Base: `--revision 8e2a8fe8… --controls-revision 8099db4a… --work …/run-base`
→ `VERIFY measurements=12 failures=3 revision=8e2a8fe8… mode=base`, driver exit 1.
PASS: driver-self-pin, controls-pins, ledger-closure (28 entries, unresolved 0), probes-base-paired
(base battery 18/18 green + faces-clean: P9 sig20/other0, P10 sig18/other2, P11 sig20/other0 —
base read ok on every masked −13 face and stale exit-N on error faces), selftest (cases=67,
failures=0), mutbat-existing (killed=5/5), real-ledger (35/35 green), red-wrong-want, identity-guards.
FAIL (the claim, correctly red at base): probes-measured (P9/P10/P11 rc0 — the masking),
shape-identity (P9/P10/P11 ok under both id spellings — the false green), multihead-mutbat
(exit 1, `MUTBAT killed=0/7 survivors=0 equivalents=0 invalid_rejected=10 failures=5`,
baseline-not-satisfied — honest battery red).

(b) Candidate: same + `--candidate .ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py`
(overlay digest recorded unpinned: d5e8fcae6f1523d0ffbe8f21540fde839a24abbe98958378e54da284eec38c05)
→ `VERIFY measurements=12 failures=0 revision=8e2a8fe8… mode=candidate`, driver exit 0. All 12 PASS;
probes-measured face-recorded P9/P10/P11 = rc1/derive-upstream-signal-13 with faces-clean
(P9 sig20/other0, P10 sig20/other0, P11 sig20/other0); shape-identity 18/18; selftest cases=71
failures=0; multihead-mutbat `MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0
failures=0` exit 0; real-ledger 35/35; identity-guards clean (tree unchanged, only GATE_REL dirty
under --candidate).

## Pin values (measured, then frozen; reproducible by L1 in final mode)

expected.ledger_summary `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`; base selftest_cases 67,
candidate 71; both kinds mutbat_summary `mutbat killed=5/5 survivors=0 invalid=0 controls=pass`;
both kinds multihead_mutbat_summary `MUTBAT killed=7/7 survivors=0 equivalents=3
invalid_rejected=0 failures=0`. measured.gate_sha256 stays the base production sha and binds only
in final mode — L1 must update it to the landed candidate sha at integration or the final run
fails closed (by design).

## Risks / named residuals

- P11 frozen at derive-upstream-signal-13 (addendum). The gate seat saw one exit-1 face on P11 in
  its own base-graft run; my 40 measured-face candidate runs and 40 base-face runs of P11 never
  showed it. Exposure is real; widening to the P10-style any-of tuple is a one-line change if L1
  observes it.
- `COLLECTOR ignored=…/probes.py reason=AttributeError` in the multihead-mutbat receipt: probes.py
  exposes no `probe_table(root)`, so the battery used its builtin table; summary/exit unaffected
  (7/7 killed both mutbat-seat repeats and my run).
- P16 sort native stage0 raced in the wild (L1 control [0,0]; gate seat −13×5): accepted {0,−13};
  verdict-neutral (single-input exempt either way). P18 native noted, never enforced (positive
  control, collector ruling).
- Driver fork bug found and fixed during demonstration 1: `parse_fig` assumed single-token
  `derived=` and misparsed multi-token deriveds (wc/sha256sum) as stale/- — fixed to split on
  ` derived=`/` ok`; earlier partial runs were discarded and both saved outputs are from the final
  driver bytes (driver-self-pin PASS pins bd82b15b… in both).
- The driver is not a sandbox; it executes the measured gate, batteries and selftests (documented
  in-file). No claim is made about general shell correctness or emulator resistance.

## Checks for the parent/integrator

- Commit the round-67 controls into the lane (driver-pins.json, probes.py, multihead-mutbat.py +
  claim evidence), update measured.gate_sha256 to the landed candidate sha, then run
  `python3 -B .ufo/waves/round-67/w1/ExecMultiHeadDriver/verify.py --revision <landed-rev>
  --controls-revision <controls-commit> --final --work <scratch>` from the lane; expect
  `VERIFY measurements=12 failures=0 … mode=final`.

## FREEZE SUPERSESSION (L1 ruling, post-demonstration — read before using any receipt above)

L1 froze the driver/controls after landing the production gate at
8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247 (selftest 73/0) and the final
probes.py at d56a1437cdd1463d99e5f7f9c15877d855c836bad8236efd0cef0afc370ae34a (20 probes,
P19/P20 mid-argv `--` repair rows, shared `probe_table(root, mode)`). Supersession facts:

- The demonstrations above ran against gate **d5e8fcae…** and probes **3f2d38a6…** (18 probes)
  with driver **bd82b15b…**. All three are superseded. The demos are PREDATA; the L1 `--final`
  run at the measured revision is the measured evidence for the landed gate.
- Frozen verify.py (as it stands): sha256 **61d5a048e6f598edf14ea7f010776cf06d5edddcbf6f54c2e12f9446c50be403**
  — carries the three ordered Critic defect fixes (marker-split parse_fig; kind-explicit
  multihead-mutbat expectation: base kind pins the battery's red line with exit 1, candidate kind
  exit 0 + green line; `COLLECTOR ignored=…` = FAILED sub-assertion) PLUS the bounded-unfreeze
  probe wiring: 20-key probe set, REPAIR_KEYS=(P9,P10,P11,P19,P20), NATIVE_STAGE0 P19=P20=(-13,),
  two driver-owned P19/P20 shapes (derives from the final probes.py; `-missing.txt` and
  `missing.txt` asserted absent in every driver fixture root), candidate selftest pin 73.
  NOT demonstrated (L1 runs --final). Demo receipts remain predata.
- multihead-mutbat.py as it stands: **e6d54540da721ff2622da32249e0898d411ee832607d677c387508717467b9d2**
  (battery seat superseded 937f8677…, which the receipts above pinned and ran).
- driver-pins.json as it stands: **9cc41af6d0bc748425373e4d61e49301377ed8d7534da0d6bdd975371bcccd65**
  — driver_sha256 61d5a048… and candidate selftest_cases 73 updated under the bounded unfreeze;
  still stale BY DESIGN (L1-owned refresh): probes control pin 3f2d38a6… → d56a1437…, battery
  control pin 937f8677… → e6d54540…, measured.gate_sha256 → 8147350c…, and the base-block red
  multihead summary (base kind currently carries only the green string, so a base/final-kind run
  of multihead-mutbat fails loudly until L1 pins the observed red line — expected shape
  `MUTBAT killed=0/7 survivors=0 equivalents=0 invalid_rejected=<n> failures=<n>`, re-observe
  against the 20-row collector table).

MEASUREMENTS final tuple: driver-self-pin, controls-pins, ledger-closure, probes-base-paired,
probes-measured, shape-identity, selftest, mutbat-existing, multihead-mutbat, real-ledger,
red-wrong-want, identity-guards (12; identity-guards evaluated last; final line
`VERIFY measurements=12 failures=N revision=REV mode=base|candidate|final`).

## Seat hygiene

Writes confined to `.ufo/waves/round-67/w1/ExecMultiHeadDriver/` (verify.py, two raw outputs,
receipts/) and the assigned pin manifest `.ufo/waves/round-67/controls/driver-pins.json` plus this
report. No production, ledger, SOURCES, knowledge, fleet, sibling-lane, lane git/jj state or index
writes; no commits/checkout/stash outside the scratch fixture repo; scratch fixture commits used a
throwaway identity inside that fixture only. Scratch
`/fast/scratch/hyaku/kasegi-r67/ExecMultiHeadDriver/` removed before yielding (verified absent below).
Tooling authorization (operator 2026-10-19): read; **no tools installed or updated** — none needed.
Failed setups: none (one mid-seat driver bug, found by the base demonstration, fixed and re-run).
