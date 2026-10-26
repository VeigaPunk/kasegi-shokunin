# CritCounterSoup — round-40 falsify wave 2 receipt

Seat: `CritCounterSoup` (critic, godspeed). Attack: the r40 suite as a whole —
environment/perturbation robustness of the claim-C1 counting commands at the
verification ref Y.

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane repo).
- Y = judged head J = `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (HEAD)
  + the untracked receipt `.ufo/waves/round-40/final-gates/all-gates.txt`
  (all-gates v4; `export-ref=3074c767…`; `suite-sha256=bdbd18a3…12897f1e`;
  `run-utc=2026-10-26T21:56:22Z` = committer instant of J).
- Instrument: `corpus/instruments/r40-closure.sh` (sha256
  `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`,
  identical in the export and the working tree).
- Baseline refs: base `a7af2ce63bce153757d39bf66b366a96caf30c13`, r39 judged
  head `8371e7ac9f32cae5ed72f8c28205634603f836fa`.
- Disk guard `disk-guard.sh status` ran before the pass: `/tmp` 3%,
  `/var/tmp` 35%, `/fast/scratch/hyaku` 24% — no guard trip.
- All runs executed in scratch `S=/fast/scratch/hyaku/kasegi-r40/CritCounterSoup`
  (removed after this receipt; no lane/fleet file was written; git used
  read-only with `--no-optional-locks`).

## Runs performed (all at ref Y unless stated)

| # | Perturbation | Invocation (mods) | Result | Verdict |
|---|---|---|---|---|
| R0 | baseline | clean scratch root `S/r0-root`; `TMPDIR=$S`; cwd `S`; `--receipt-out S/driver/r0-receipt.txt` | `closed=10/10 exit=0` rc=0; receipt byte-identical to Y all-gates.txt | reproduced (green) |
| R1 | (a) scratch root containing leftovers from other seats | scratch root `S/r1-root` with `kasegi-r40-leftover/seat/leftover.txt`, empty `kasegi-r39-old-seat/`, plus `kasegi-r40-work-family/` holding `--work` and a nested leftover `nested-leftover/junk.txt` | `H6 payload=strays=2,read=ok closed=0`; `closed=8/10 exit=1` rc=1 (H7 red is the downstream cascade of the red H6) | gate detects leftovers (designed); empty r39 family entry counts too; nested leftover inside the work-holding family is excluded — documented semantics confirmed |
| R2 | (b) pre-populated `export/` etc. in `--work` | `--work S/r2-work` pre-seeded with stale `export/SCORECARD.md`, bogus `export/corpus/instruments/r40-closure.sh`, `mut/old.bin`, `neg-base/old.txt`, `neg-r39/`, `h5/forged.txt` | `closed=10/10 exit=0` rc=0; receipt byte-identical to Y | reproduced — stale-byte clearing works; no stale export/fixture satisfies a check |
| R3 | (c) `TMPDIR` unset | `env -u TMPDIR`; auto work dir lands in `/tmp`; clean scratch root `S/r3-root` | `closed=10/10 exit=0` rc=0; receipt byte-identical to Y; stdout byte-identical to R0 | reproduced |
| R4 | (d) different cwd | cwd `/`; clean scratch root `S/r4-root`; `TMPDIR=$S` | `closed=10/10 exit=0` rc=0; stdout byte-identical to R0 | reproduced |
| R5 | (d) different cwd | cwd = lane root; clean scratch root `S/r5-root`; `TMPDIR=$S` | `closed=10/10 exit=0` rc=0; stdout byte-identical to R0 | reproduced |
| R6/R7 | (e) twice back-to-back | identical args, same clean scratch root `S/r6-root`, `TMPDIR=$S` | both `closed=10/10 exit=0` rc=0; R6 vs R7 receipts byte-identical; stdout byte-identical | deterministic |
| R8 | default live scratch root (`/fast/scratch/hyaku`), `TMPDIR=$S` | auto work dir under `S` (inside family entry `kasegi-r40`) | `H6 payload=strays=0,read=ok closed=1`; `closed=10/10 exit=0` rc=0 | green |
| R9 | default live scratch root, `TMPDIR` unset | auto work dir in `/tmp` (outside family entry) | `H6 payload=strays=1,read=ok closed=0`; `closed=8/10 exit=1` rc=1 | **RED — G6-class environment flip** |
| R11 | isolation control for R8/R9 | default live scratch root; `TMPDIR=$S`; explicit `--work S/outside-work` (still inside family entry) | `H6 payload=strays=0,read=ok closed=1`; `closed=10/10 exit=0` rc=0 | confirms the only variable is work-dir containment in the family entry |
| R10 | claims.json literal counting command (no `--receipt-out`) | clean scratch root `S/r10-root`; `TMPDIR=$S`; `--export-ref <Y>` only | `H7 payload=receipt=0,… closed=0`; `closed=9/10 exit=1` rc=1 | **contradicts claim C1 counting command #1** |
| ST | claims.json selftest counting command | `--selftest --export-ref <Y>`, clean scratch root `S/st-clean`, `TMPDIR=$S` | `selftest cases=10 failures=1` rc=1; `selftest case=H7 positive=fail mutants=6/6 verdict=fail`; judge `own-report accepted=0`; all six forged-report judges reject (forged-summary/caselines/failed-cases/detail-free/9-cases/no-verdict all rejected=1) | **contradicts claim C1 counting command #2** |
| R12 | plain run (no `--export-ref`, no `--selftest`) | no args | exit 2 with refusal text `r40-closure: refusing to run against the live worktree: this suite is export-mode only.` | reproduced (claim counting command #5) |
| — | base/r39 negative controls | every H8 payload above: `base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1` (R0, R10 identical) | closed<10/10 exit=1 on both negative refs, in every run | reproduced (claim H8) |

## Defects found

### D1 — the frozen C1 counting commands cannot reproduce their promised outputs at Y as written (verifiability contradiction)

1. `bash corpus/instruments/r40-closure.sh --export-ref <Y>` (claims.json C1
   counting command #1, promised `closed=10/10 exit=0`) prints
   `closed=9/10 exit=1` in my re-run (R10). Cause: H7 verifies the receipt
   inside the **export**, but the receipt `.ufo/waves/round-40/final-gates/all-gates.txt`
   is an *untracked working-tree file* — `git log --all -- <path>` shows it
   was never committed at any commit, so `git archive` cannot carry it into
   the export (`H7 payload=receipt=0`). The run only goes green with
   `--receipt-out` (R0), which the frozen counting command does not include.
2. `bash corpus/instruments/r40-closure.sh --selftest --export-ref <Y>`
   (counting command #2, promised `selftest cases=10 failures=0 exit=0`)
   prints `selftest cases=10 failures=1` and exit=1 (ST). Cause: H7's graded
   positive case reads `$EXPORT/$RECEIPT`, which is absent for every export of
   every commit in lane history (receipt never committed); `run_selftest`
   pins `H7_TARGET=$EXPORT/$RECEIPT`, so no documented CLI (and no `H7_TARGET`
   env override — tested, line 1356 overwrites it) can make the selftest
   green at any ref. The wave-1 claim of `selftest cases=10 failures=0` is
   therefore not reproducible from the committed bytes.
   The mutant limb still works: 6/6 H7 fixture mutants rejected; the other 9
   cases pass (positive=pass, mutants=N/N all rejected).
3. Both defects are pure invocation/byte-state facts at Y — independent of
   the perturbation matrix (they show in R10/ST on a clean scratch root).

### D2 — G6-class environment dependence persists: green↔red flips on host state, not byte state

With identical committed bytes and the same command shape, the suite flips
green↔red purely on where the auto work dir lands:

- R8 (`TMPDIR=$S` → work inside family entry `kasegi-r40`) → green, strays=0.
- R9 (`TMPDIR` unset → work in `/tmp`, outside the family entry) → **red**,
  strays=1, `closed=8/10 exit=1`.
- R11 (explicit `--work` inside the family entry) → green, confirming the
  variable is work-dir containment in the top-level family entry, not TMPDIR
  itself.

Why this bites: the live scratch root currently has the top-level family entry
`/fast/scratch/hyaku/kasegi-r40/` with 13 live seat scratch dirs (including
this seat). H6 counts every top-level `kasegi-r39*|kasegi-r40*` entry that
does not contain the run's work dir as a stray. A run whose work lands outside
that family is therefore red *because other seats are legitimately working right
now*, i.e. the suite's greenness at Y is a function of concurrent host scratch
state. The round-39 G6 fix (name-family scanning — confirmed live by the H6
selftest mutants rejecting both `r39-sibling-family` and `r40-sibling-family`
fixtures) reduces but does not remove the live-state dependence; the claim's
unconditional `closed=10/10 at Y` promise is thus only true on a quiet scratch
root or with work deliberately placed inside the family. This is a fixable
defect/tradeoff the claim text does not state (the instrument header documents
it at lines 138–144).

## Repro of the claim's other promised facts (evidence)

- R0 receipt is **byte-identical** to Y's `all-gates.txt` — the committed/teed
  transcript reproduces exactly (H7 determinism, `cmp` on all 16 lines).
- R2/R3/R6/R7 receipts also byte-identical to Y.
- Base/r39 negative controls red in every run: `base=3/10,base-exit=1,r39=2/10,r39-exit=1`
  (H8 green on both negative refs).
- Plain-run refusal exit 2 reproduced.
- cwd invariance (R4/R5) and back-to-back determinism (R6/R7) hold.
- Selftest forgery judges: all six forged-report variants rejected (1 each).

## Verdict

- Reproduction: the suite's byte-level green run (with `--receipt-out`) and
  its negative controls reproduce at Y; determinism, cwd invariance, and
  stale-work clearing hold.
- Contradiction (D1): both primary C1 counting commands as frozen in claims.json
  fail at Y (9/10 and selftest failures=1). The claim's promised outputs need
  either `--receipt-out` (run mode) or a committed receipt — neither is in the
  claim text, and the selftest form is impossible under the committed bytes.
- Environment dependence (D2): a G6-class red-green flip exists between R8 and
  R9 caused solely by TMPDIR/host scratch layout; the C1 green result is
  host-state-conditional.

Receipt ends here — no lane/fleet file was written outside this receipt; all
run artifacts lived in `S=/fast/scratch/hyaku/kasegi-r40/CritCounterSoup` and
were removed after collection.
