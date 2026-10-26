# MutFixedPins — round-39 wave-2 falsify receipt (pinned-constants mutation probe)

Seat: MutFixedPins (leaf, mutation-tester). Date: 2026-10-26.
Item: mutate the pinned-constants of the landed r39 suite in a sandbox copy; run
`--selftest` and `--export-ref <Y>`; record that G8 goes red or selftest fails.
Deliverable: `.ufo/waves/round-39/wave2/MutFixedPins.mutations.txt` (262 lines, sha256
`d76c6b391a520ef54cdcc0cb390c9e5e701b336595c956317dfc610642bfa569`; every capture in it
was cat'd from disk, not retyped).

## Target and binding
- Suite under attack: `corpus/instruments/r39-closure.sh` at lane tip
  Y = `5006097a84305267c9a3e8c1e1d560e60fe41d37`, sha256
  `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` — equal to the git
  HEAD blob and to the committed receipt's `suite-sha256` in
  `.ufo/waves/round-39/final-gates/all-gates.txt`; that receipt carries
  `export-ref=46c66c268502abd1b2c342fc71bf88ccf721845b` = J (full hash), and
  `git diff --name-only J Y` lists only the receipt, so the verification ref is Y per
  erratum E4. All runs below use `--export-ref Y`.
- G8 pinned constants (suite lines 198/199/951): `PIN_REF=2387dcf6ccfefcfb703783387b9aade8fc82abfa`,
  `PIN_R37_SHA=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`,
  `local suite=corpus/instruments/r37-closure.sh`. The path variable feeds BOTH the
  `git show "$PIN_REF:$suite"` extraction and the export-copy check.

## Detector (identical on pristine / mutated / restored bytes)
`bash <suite-copy> --export-ref 5006097a… --lane $S/lane --work $S/work[-<id>] --scratch-root $S/g6root`,
plus the `--selftest` variant of the same command. Two documented suite options were used
uniformly (both print `deviation=` lines in every capture):
- `--lane` = clean `git clone --no-local file://` of the lane, checked out at Y, status
  clean. Reason (measured, PROBE in the deliverable): the real lane worktree holds
  untracked wave-2 files from concurrent sibling seats, and the pinned r37 suite's live E9
  limb (`git status --porcelain` must be empty; lane HEAD == export ref) reds G8 by
  construction on any run against it — the pristine suite vs the real lane prints
  `G8 …r37-closed=0,r37-exit=1 closed=0` → `closed=7/8 exit=1`. The clone carries
  identical objects (Y, J, base `480b1a50…`, PIN_REF `2387dcf6…`, root `aeddcd2e…` all
  rev-parse-verified in it).
- `--scratch-root` = empty isolated dir. Reason (measured, PROBE-2): the default
  `/fast/scratch/hyaku/kasegi-r39` held 26 sibling seat dirs at probe time; G6 reds
  fail-closed on them (`r39=present` → `closed=7/8 exit=1`) even pristine.

## Results (all at Y; full captures in the deliverable)
| run | export mode | selftest mode | verdict |
|---|---|---|---|
| pristine baseline | `closed=8/8 exit=0` (1 s) | `cases=8 failures=0`, all mutants rejected, 6 forgeries rejected (9 s) | baseline green |
| real-lane probe | `closed=7/8`, G8 `r37-closed=0` | — | E9 dirtiness by construction; proves the r37-run limb is live |
| default-scratch-root probe | `closed=7/8`, G6 `r39=present` | — | mid-wave G6 red by construction |
| M0 comment-only (control) | `closed=7/8`, G2-only red, G8 green | `failures=1` (G2), G8 case passes | digest collateral isolated |
| M1 digest `0da98e37…`→`1da98e37…` | `closed=6/8`, G8 `pinned-sha=0,export-copy=0,r37-closed=0` | `failures=2`, `case=G8 positive=fail` | **KILLED** |
| M2a `PIN_REF`→base `480b1a50…` | `closed=7/8`, **G8 green** (`pinned-sha=1,export-copy=1,r37-closed=1`) | `failures=1` (G2), G8 case passes | **SURVIVED — equivalent mutant** |
| M2b `PIN_REF`→root `aeddcd2e…` (file absent) | `closed=6/8`, G8 `pinned-sha=0` with `export-copy=1` | `failures=2`, `case=G8 positive=fail` | **KILLED** (pin limb alone) |
| M3 path `…/r37-closure.sh`→`….pinned` | `closed=6/8`, G8 `pinned-sha=0,export-copy=0,r37-copy=0` | `failures=2`, `case=G8 positive=fail` | **KILLED** |
| restored (M1 copy ← pristine bytes) | `closed=8/8 exit=0` | — | hash-equal `2856a210…`, green again |

## Findings
1. **Coverage finding (equivalent mutant M2a).** G8's commit pin is not independently
   behavior-bearing across same-content commits: r37-closure.sh bytes are identical at
   PIN_REF `2387dcf6…`, base `480b1a50…` and J `46c66c26…` (all sha256 `0da98e37…`,
   measured), so re-pointing the `git show` ref at the base commit passes every limb and
   no check compares the `pin-ref` payload VALUE (suite-documented limit: "The cross-run
   payload VALUE comparison is not a limb"). The digest constant is the effective
   binding; the commit ref adds provenance only. Recorded as a coverage finding, not a
   contract change.
2. **Attribution control (M0).** Any byte change to the suite flips G2 `digest-match=0`
   (executing bytes vs the receipt's committed `suite-sha256`); the comment-only control
   shows this in isolation (G2 red, G8 green, both modes). The G8 reds above are
   attributable to the pinned-constant mutations themselves — M2b kills via the pin limb
   alone (`export-copy=1`), M3 kills both limbs with the single path variable.
3. **Operational (measured).** G8's inner r37 run is live and fail-closed; mid-wave runs
   against the real lane red via E9 worktree dirtiness, and default-scratch-root runs red
   G6 on sibling dirs. The same overridden detector was used on pristine, mutated and
   restored bytes, so the A/B/C comparison is valid.
4. **Bottom line.** No defect found in the landed pinned constants: pristine green at Y
   (`closed=8/8 exit=0`; `selftest cases=8 failures=0`) and 3 of 4 pinned-constant mutants
   killed. C1's G8 limb stands as frozen; the only soft spot is the same-content-commit
   equivalence in (1).

## Environment / compliance
- Tooling installed: none (bash, git, coreutils only). No pacman. No network fetches.
- Writes: only `.ufo/waves/round-39/wave2/MutFixedPins.mutations.txt` and this receipt;
  all work copies under `/fast/scratch/hyaku/kasegi-r39/MutFixedPins` (removed before
  yield). No writes to the fleet root, `.ufo/state/`, templates/, scripts/, or any
  sibling repo.
- Lane repo: read-only git only (`rev-parse`, `log`, `status`, `diff`, `show`, `ls-tree`,
  `rev-list`, and one `git clone --no-local file://` whose only writes landed in
  scratch). `git diff --stat` empty at close; the suite itself ran with
  `--no-optional-locks` and wrote nothing under the lane.
- Scratch footprint peaked at ~156 MB (the clone); removed before yield.
