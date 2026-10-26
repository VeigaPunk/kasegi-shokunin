# MutG3G4 — mutation test of r38-closure.sh G3/G4 limbs (round 38)

Seat: MutG3G4 (leaf, mutation-tester). Judged axis: depth:verifiability.
Suite under test: `corpus/instruments/r38-closure.sh`, taken from the wave1
deliverable `.ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh`.
All runs used `TMPDIR=$S` and `--work` under $S; every scratch git fixture had
`git rev-parse --show-toplevel` asserted equal to its own dir before any
mutating git command.

## Provenance

- Deliverable found on check 2/4 at 2026-10-26T18:44:24Z; no fallback minimal
  implementation was needed.
- The deliverable was revised twice mid-campaign by its author (ExecSuiteBuild):
  - 85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6 (1473 lines)
  - 7883c37cd3249a121d1f28c36fc06a0031d6cabcec513cf9b474df4bd52f8c9e (1716 lines)
  - 09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42 (1767 lines, current)
- The full 9-mutant campaign was run against 7883c37c. `check_g3`, `check_g4`,
  `g4_json`, `g4_fixture`, `selftest_case_G3` and `selftest_case_G4` were then
  verified byte-identical in 09d46673 (function-level diffs; 0 G3/G4-relevant
  lines in the 86-line revision diff; the only shared-harness identifier the
  revision touches is a new `st_neg` call site inside `selftest_case_G2`).
  Baselines and two spot-check mutants (survivor G3-M3, kill G4-M5) were re-run
  on 09d46673 with identical results, binding the table to the current bytes.
- Suite-level `--selftest --export-ref J -> selftest cases=8 failures=0` was NOT
  runnable: the judged head J does not exist yet (lane HEAD 7001535, wave1 still
  landing). Operative kill criterion: the per-case `selftest case=G3/G4` lines at
  a green fixture, whose pristine baseline IS green (below). The suite-level
  failures count drifted 5<->6<->7 across runs because G8's carry-over embeds
  r37-closure's live quiescence limb (shared live scratch flickers while sibling
  seats run); the G3/G4 case lines were stable throughout.

## Detectors

Per mutant, three detectors:

- D1 base-red: `bash <suite> --export-ref a173b0c2b98c5ae39599fa9be76027fbbead0b9e --work $S/wk-*`.
  Pristine: `G3 payload=resolutions-section=0,line-tokens=0,added-pending=0,added-placeholders=0,diff-read=ok closed=0`,
  `G4 payload=dispatches=0,pairs=0,seats-ok=0,read=fail closed=0`, `closed=0/8 exit=1`.
  A mutant that turns its limb green here escapes the base detector.
- D2 selftest: `bash <suite> --selftest --lane $S/gf --export-ref $c1 --work $S/wk-*`.
  Pristine (7883c37c/09d46673): `selftest case=G3 positive=pass mutants=2/2 verdict=pass`,
  `selftest case=G4 positive=pass mutants=4/4 verdict=pass`, `selftest cases=8 failures=6`.
  Pristine (85d33ea9): case=G3 2/2, case=G4 2/2, failures=5.
  Kill = the mutated limb's case flips to `verdict=fail`.
- D3 targeted red fixture per mutant class: pristine red vs mutant green on the
  same input bytes.

## Fixtures (all under $S)

- gf c1=bf7f225f1655cdff722dbec296ee9e914bda8b93 — verified-init repo, fetched
  lane HEAD, checked out base a173b0c2, appended a green
  `## Pending-marker resolutions (round 38)` section (all 8 L-tokens) to
  `corpus/lessons/round-37.md`, added `.ufo/waves/round-38/wave1-dispatch.json`
  (3 tasks) + `wave1-results.json` (3 seats, same wave). Pristine green run:
  G3 closed=1, G4 closed=1 (85d33ea9: closed=3/8 with G8 green; 7883c37c+:
  closed=2/8 with G8 red — G8 needs more bytes; not a G3/G4 matter).
- gf2 c2=4fa7e26890cf3791ef40edfa6bf2bff61ae4152a — gf + added line
  `set head to <LANE_HASH> (mutant probe line)` in `corpus/lessons/r38-probe.md`.
- gf3 c3=7094d4c84d8c36187f252a19fe36e90f2a93fd29 — verified-init repo WITHOUT
  base ancestry (green section in tree; `git diff a173b0c2..c3` fails: bad revision).
- gf4 c4=c6337f3052ebd7eb6197a76981ca4de4f7948da4 — gf with
  `wave1-results.json` removed and `kasegi-r38-build-results.json` added whose
  `wave` is `kasegi-r38-build-MISMATCH` (exercises the fallback path).
- gf5 c5=bd577c8412124cac53ce42eaced02a1f90748b4b — gf with results
  `{"lane":"kasegi","round":38,"wave":"kasegi-r38-build"}` (valid JSON, no
  results/seats -> seats reader prints -1). Did NOT discriminate G4-M4 (first
  probe attempt; recorded honestly).
- gf5b c5b=ad8dbebc338345f02ea7131bc9f4963acea62a08 — gf with results
  `not json at all {{{` (invalid JSON -> g4_json prints ERR).
- gf6 c6=b43b8610cfca49b8c0668d02c66ab6fa8d777a8d — gf with zero-task dispatch
  (`taskCall.tasks=[]`) + zero-seat results (`results=[]`, `seats=0`).

## Mutant table (7883c37c bytes; G3/G4 byte-identical in 09d46673, spot-checked)

| id | limb | class | find -> replace | D1 base export | D2 selftest at gf | D3 escape fixture | verdict |
|---|---|---|---|---|---|---|---|
| G3-M1 | G3 | delete condition | `[ "$sect" -eq 1 ] && [ "$tokens" -eq 8 ] && [ "$pending" -eq 0 ] \` -> `[ "$sect" -eq 1 ] && [ "$pending" -eq 0 ] \` | G3 closed=0 (red) | case=G3 mutants=1/2 verdict=fail (`missing-line-token` accepted: `rejected=0 rc=0 payload=...line-tokens=7`) | — | KILLED (selftest) |
| G3-M2 | G3 | invert condition | `[ "$pending" -eq 0 ]` -> `[ "$pending" -ne 0 ]` | G3 closed=0 (red) | case=G3 positive=fail mutants=2/2 verdict=fail | green run: G3 closed=1 -> 0 | KILLED (selftest positive) |
| G3-M3 | G3 | gut added-token vocabulary | `for tok in "⟨pending" '<fill>' 'filled by the L1' '<LANE_HASH>' '<r38-'; do` -> `for tok in "⟨pending"; do` | G3 closed=0 (red) | case=G3 positive=pass mutants=2/2 verdict=pass (UNCHANGED) | gf2: pristine `added-pending=1 closed=0` -> mutant `added-pending=0 closed=1` | SURVIVED |
| G3-M4 | G3 | fail-closed read -> default | init `... placeholders=0 diffread=fail` -> `... diffread=ok` | G3 closed=0 (red) | case=G3 positive=pass mutants=2/2 verdict=pass (UNCHANGED) | gf3: pristine `diff-read=fail closed=0` -> mutant `diff-read=ok closed=1` | SURVIVED |
| G4-M1 | G4 | delete condition | `&& [ "$seatsok" -eq "$disp" ] && exit 0` -> `&& exit 0` | G4 closed=0 (red) | case=G4 mutants=3/4 verdict=fail (`seat-count-short` accepted) | — | KILLED (selftest) |
| G4-M2 | G4 | invert condition | `[ "$pairs" -eq "$disp" ]` -> `[ "$pairs" -ne "$disp" ]` | G4 closed=0 (red) | case=G4 positive=fail mutants=4/4 verdict=fail | green run: G4 closed=1 -> 0 | KILLED (selftest positive) |
| G4-M3 | G4 | delete wave-match limb | delete `rwave=$(g4_json "$res" wave)` + `if [ -z "$rwave" ] || [ "$rwave" != "$wave" ]; then continue; fi` | G4 closed=0 (red) | case=G4 mutants=3/4 verdict=fail (`results-for-another-wave` accepted: `rejected=0 rc=0`) | gf4: pristine `pairs=0 closed=0` -> mutant `pairs=1 seats-ok=1 closed=1` | KILLED (selftest) |
| G4-M4 | G4 | fail-closed read -> default | `case $rseats in ''\|*[!0-9-]*) continue ;; esac` -> `... rseats=$rtasks ;; esac` | G4 closed=0 (red) | case=G4 positive=pass mutants=4/4 verdict=pass (UNCHANGED) | gf5b: pristine `pairs=0 closed=0` -> mutant `pairs=0 closed=0` (NO delta) | INCONCLUSIVE (equivalent mutant) |
| G4-M5 | G4 | delete zero-task limb | delete `[ "$rtasks" -ge 1 ] \|\| continue` (+ its 2 comment lines) | G4 closed=0 (red) | case=G4 mutants=3/4 verdict=fail (`zero-task-dispatch` accepted) | gf6: pristine `pairs=0 closed=0` -> mutant `pairs=1 seats-ok=1 closed=1` | KILLED (selftest) |

Mutant sha256 prefixes (7883c37c campaign): G3-M1 cb3f0e93d78c, G3-M2 cd31de9b1cd5,
G3-M3 857450429fe5, G3-M4 f4f7ce5133cd, G4-M1 feebae086f84, G4-M2 ecf74cefc132,
G4-M3 5512d147051c, G4-M4 7918252524a0, G4-M5 361abd31a92f. Spot-checks on
09d46673 bytes: G3-M3 1b18c353d77e (survived, identical), G4-M5 721ead48d9c7
(killed, identical).

## Findings (survivors -> missing fixtures)

1. **G3-M3 SURVIVED** — `selftest_case_G3`'s only added-line fixture plants
   `TODO` (`added-placeholder-token`); no fixture plants `⟨pending`, `<fill>`,
   `filled by the L1`, `<LANE_HASH>` or `<r38-` in the base..REF added lines.
   Gutting four of the five widened-token classes (the D-C lesson's actual
   widened vocabulary) leaves `selftest case=G3 positive=pass mutants=2/2
   verdict=pass` while the limb's red state on a defect input is lifted (gf2:
   pristine red, mutant green). Missing fixture: one added-line probe per
   non-TODO token class; the gf2 `<LANE_HASH>` probe is a working template.
2. **G3-M4 SURVIVED** — no selftest fixture forces the
   `git -C "$LANE" diff BASE_REF ref` read to fail; replacing the fail-closed
   `diffread=fail` init with `diffread=ok` leaves case=G3 fully green while an
   unresolvable-BASE_REF fixture (gf3) flips pristine red (`diff-read=fail
   closed=0`) to mutant green (`diff-read=ok closed=1`). Missing fixture: a
   fixture lane lacking BASE_REF ancestry (gf3 is a working template).

## Inconclusive (equivalent mutant — not a coverage finding)

- **G4-M4**: in the revised G4 the wave-match limb runs before the seats read,
  so every input that would make `g4_json seats` unparseable (invalid JSON ->
  ERR; python3 broken -> empty stdout) already dies at
  `case $wave in ''|ERR) continue` or the `[ -z "$rwave" ]` half. The
  `case $rseats in ''|*[!0-9-]*)` guard is shadowed (unreachable
  defense-in-depth); no CLI-reachable input distinguishes the mutant (gf5b:
  pristine and mutant both `pairs=0 closed=0`). The old-revision (85d33ea9)
  version of this mutant DID survive (gf5b escape: pristine `seats-ok=0
  closed=0` -> mutant `seats-ok=1 closed=1`); the revision closed the
  reachability by construction, not via a selftest fixture. No action needed
  beyond noting the seats guard is now dead code through the CLI.

## Old-revision provenance (85d33ea9, superseded mid-campaign)

- G3-M1 KILLED (mutants=1/2), G3-M2 KILLED (positive=fail), G3-M3 SURVIVED,
  G3-M4 SURVIVED — identical outcomes (check_g3 byte-identical across revisions).
- G4-M1 KILLED (mutants=1/2), G4-M2 KILLED (positive=fail).
- G4-M3 SURVIVED then (wave-match existed only in the fallback branch and no
  fixture covered it) — the revision moved the check to the main path and added
  the `results-for-another-wave` fixture; re-run on the revision: KILLED.
- G4-M4 SURVIVED then (gf5b escape demonstrated) — see Inconclusive above.

## Process notes

- One edit misfire: the first G4-M1 attempt (old revision) deleted the `exit 1`
  line instead of the condition; caught on the edit diff, pristine restored,
  correct mutation applied. The misfired bytes were never executed.
- No tools installed (none needed); no pacman; no network fetches.
- Writes: this receipt only, plus scratch under $S. The lane repo was never
  written by this seat; `git status --porcelain` shows
  `?? corpus/instruments/r38-closure.sh` (the author's own untracked landing),
  untouched here.
- Restoration: the scratch working copy was restored to the current pristine
  bytes 09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42 before
  cleanup; the deliverable file was never written by this seat (its hash
  changes above are the author's own revisions).

## Scratch

$S=/fast/scratch/hyaku/kasegi-r38/MutG3G4 — removed before this seat yielded.
