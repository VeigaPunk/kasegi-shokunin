# R44Exec1 — C1 closure counter plan (read-only derivation)

- seat: R44Exec1 (leaf, read-only); item: *read-only derive a concise reproducible C1 closure counter plan for all eight R43 verifier defects; do not edit code*.
- lane `kasegi-shokunin`; frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`; freeze commit / HEAD `66314015122b9aa32dc40f2f1815df56624c26d1` (`round-44: freeze claims and validated wave`).
- inputs read first: `.ufo/waves/round-44/claims.json`, `.ufo/waves/round-44/controls/do-nothing.txt`, `corpus/lessons/round-43-verifier-spotcheck.md` §6, `/home/vgpnk/.omp/agent/RULES.md`.
- method: `git archive` exports of base and HEAD into scratch, then plain reads/greps and one `bash` absent-path run; no lane byte written, no git/jj mutation, no installs (nothing to install; `python3`, `git`, `awk`, `grep`, `od` already present).
- scratch: `/fast/scratch/hyaku/kasegi-r44/R44Exec1/` (exports `base/`, `head/`, `base43/`, transcript `measure-base.txt`); removed on exit (§7).
- writes: this report only.

## 0. Frozen contract and one blocking pointer defect

C1 counter string as frozen: `python3 corpus/instruments/r44-routed-defects.py --root <lane-export> --baseline <frozen-base>`; C1 control: `.ufo/waves/round-44/controls/c1-do-nothing.txt`.

**F0 — the C1 control pointer does not resolve (blocker, not one of the 8).**

```
$ git -C kasegi-shokunin cat-file -e HEAD:.ufo/waves/round-44/controls/c1-do-nothing.txt
fatal: path '.ufo/waves/round-44/controls/c1-do-nothing.txt' does not exist in 'HEAD'   rc=128
$ git -C kasegi-shokunin ls-files .ufo/waves/round-44/controls/
.ufo/waves/round-44/controls/do-nothing.txt
```

The frozen control exists at `controls/do-nothing.txt`, not at the path C1 names. C1 cannot be verified against a control that is absent at its cited path, and this is the same class as routed defect 8 (a cell citing a file that does not print what it is cited for). Append-only fix (no claims edit — `claims.json` is frozen and K19 pins its sha256): commit `.ufo/waves/round-44/controls/c1-do-nothing.txt` carrying the counter's do-nothing transcript (§4 control A) plus the base measurements in this report. Without it the C1 counter/control pair is half-resolvable.

## 1. Counter contract (what the instrument must be)

`corpus/instruments/r44-routed-defects.py` — stdlib-only, deterministic, read-only, export-mode only.

```
r44-routed-defects.py --root <lane-export> --baseline <frozen-base>
                      [--lane DIR] [--final-ref REF] [--fleet-report PATH]
                      [--work DIR] [--only D1,D5] [--selftest]
```

- `--root`: a `git archive` extraction of the final revision. Refused with exit 2 if it contains `.git` (a working tree is never graded) or if it resolves to the same realpath as `--lane`.
- `--baseline`: commit-ish resolved read-only in `--lane` (`git rev-parse --verify <ref>^{commit}`) and exported with `git -C <lane> archive <ref> | tar -x -C <work>/baseline`; a directory is also accepted (do-nothing replay). An unresolvable ref prints `baseline=ref-not-found exit=1`, never a vacuous pass.
- `--lane` default `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; `--final-ref` default `HEAD`; `--work` default `mktemp -d` honouring `TMPDIR`.
- Read-only surface: `git rev-parse`, `git archive`, `git diff --numstat`, `git status --porcelain`, `git show`; plain reads; one `bash` run of an absent path (§D8). No writes outside `--work`; no network; no clock value in any payload line (one `run-utc=` header line only).

Output (one committed run, 8 defect lines, stable order):

```
all-routed v1
root-digest=<64hex over sorted "rel<TAB>sha256" pairs>
baseline-ref=<40hex> baseline-digest=<64hex>
suite=closed=19/19|open=<n>|absent
D1 payload=... base=red|green final=red|green closed=0|1
...
D8 payload=... base=red|green final=red|green closed=0|1
routed=8 resolved=<n>/8 exit=0|1
```

`closed=1` for `D<n>` **iff** `final=green` **and** `base=red`. The red-before requirement is inside the counter, not a reviewer's promise: a defect already green at the frozen base can never be credited (C1 kill rule, do-nothing clause). `exit=0` only when `resolved=8/8` **and** `suite=closed=19/19`; a red `suite` line credits nothing (the corrections must not red K14–K19 — the "harm none" condition).

`--selftest` builds mutants in `--work` and prints one `selftest case=<id> positive=pass|fail mutant=<name> verdict=pass|fail` line per case plus `selftest cases=<n> failures=<k>`; exit 0 only at 0 failures.

## 2. Per-defect predicates, with the measured frozen-base state

All base values below were measured on the `5ab3a60` export (`base/`); HEAD `6631401` is byte-identical for every file named (verified: `git diff --numstat 5ab3a60 6631401 -- <path>` empty for `SHONEN.md`, `SCORECARD.md`, `corpus/lessons/round-43.md`, `corpus/instruments/README.md`, `.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt`).

### D1 — `closed=13/19` is unbacked (spotcheck §6.1)

| leg | measured at base |
|---|---|
| sites of the literal | `SCORECARD.md:1685` (move-log row), `.ufo/waves/round-43/claims.json:41` (`after` cell); `claims.json` frozen by K19 (`freeze.txt` `claims-sha256`) |
| erratum naming it | `grep -l 'closed=13/19' base/.ufo/waves/round-43/claims-erratum-*.md` → **0** (one erratum file exists, names `10/12` and `frozen_at_utc` only) |
| per-limb base evidence | six transcripts exist and are red: K14 `literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0`; K15 `sentences=5,unbacked=3 closed=0`; K16 `payload=sections=491,promises=1,unresolved=1 closed=0`; K17 `claims=20,tokens=3,verified=2,unbacked=1 closed=0`; K18 `quotes=28,bound=27,unbound=1 closed=0`; K19 `freeze=absent,order=bad,sha=mismatch closed=0` |
| committed base run of the landed suite | none: `grep -rl 'export-ref=ab98fac9' base/.ufo/waves` finds only the stand-in control and seat receipts, no `closed=<n>/19` summary |

**Predicate.** Green iff a blank-line-separated entry of `.ufo/waves/round-43/claims-erratum-*.md` (K17's own shape, `k17-claims-before.sh:224-235`: paragraph contains whole token `closed=13/19` and `supersed`, case-insensitive) **and** it names at least one of the six transcript basenames **and** all six exist and each prints a `closed=0` payload line **and**, if the entry asserts any composite `closed=<n>/19`, a committed transcript with `export-ref=ab98fac9…` and `closed=<n>/19 exit=1` exists (fail-closed: the replacement may not be a second unbacked number). Append-only leg: a new `claims-erratum-2.md`; `claims.json` untouched.

**Base** = red (0 errata naming the literal). **Green** = the erratum above. Red-before control: prose-only mutant (names `13/19`, no per-limb evidence) → red.

### D2 — no check can see D1 (§6.2)

| leg | measured at base |
|---|---|
| K17 escape scope | erratum files **in the graded round's own dir** (`k17-claims-before.sh:224-235`); K18 escape accepts a `claims-erratum*.md` entry carrying `superseded` in the round-42/43 dirs (`k18-transcript.sh:60-95`, `WAVE_ROUND_DIRS`) |
| erratum naming `13/19` | 0 |
| K18 bytes | `sha256sum corpus/instruments/r43-limbs/k18-transcript.sh` = `3551a0fc5a18d9e94e4f3f11a07520f6fd8082842cafad00d1b98f862495a89e` at base **and** at HEAD (unchanged, so not widened) |

**Predicate.** Green iff a `.ufo/waves/round-43/claims-erratum-*.md` entry carries whole token `closed=13/19` + `supersed` (same-round-dir, K17 escape shape) **and** it names `K17` (the escape that covers it — "say which") **and** `sha256(k18-transcript.sh)` at final equals the base digest (no widening). Append-only leg: the same erratum-2 file. **Base** = red (no entry). Red-before controls: wrong-dir mutant (entry in `round-44/`) → red; k18-widened mutant (one byte changed) → red.

### D3 — lesson numeral wrong (§6.3)

| leg | measured at base |
|---|---|
| claimed value | `corpus/lessons/round-43.md:90` and `:101` "29-character prefix" (2 occurrences) |
| measured value | capture line 97 `Fixed-in: https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6`; token after `commit/` → **len 26** |
| correction markers | 5 `grep` hits in the file, **all inside table rows** (lines 37–41) — none is a marker: the r42 engine's `CORRECTION_RX = ^Correction \(round (\d+)\)` (`r42-closure.sh:476`) is matched against the raw line, so a marker must start at column 0 |
| append-only | `git diff --numstat 5ab3a60 6631401 -- corpus/lessons/round-43.md` empty |

**Predicate.** Green iff (i) the counter re-derives `len == 26` from the capture's `Fixed-in:` line (not hardcoded); (ii) a column-0 line matching `^Correction \(round 43\)` exists at a line number greater than the last `29-character` occurrence, naming `29-character`, `26`, the capture path `corpus/source-snapshots/round-43/S067.txt` and a counting token (`awk` or `RLENGTH`); (iii) every `29-character` occurrence precedes that line; (iv) numstat deletions for the file base→final = 0. **Base** = red (no marker, measured 2 unbacked occurrences). Red-before control: mutant with the marker placed *above* the occurrences → red; mutant naming only `26` without the counting token → red.

Note for the fixer: the correction line introduces no `closed=`/`cases=` token, so K18's population (`corpus/lessons/round-43*.md`) is unaffected; K14 has no `corrections=` literal to grade on it; K15/K16 treat a `Correction (round 43)` line as non-assertive.

### D4 — report omissions (§6.4)

| leg | measured at base |
|---|---|
| round-43 report | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kasegi.md` sha256 `02704332cfeede3a…`: `planner` lines **0**, `L2` lines **0**, `residual` lines **0** |
| round-44 report | absent (`ls .ufo/reports/round-44/` → No such file or directory); the report is committed in the **fleet** repo (`fdf719a9 round-43: kasegi report`), not in the lane export |
| required content | `scripts/hyaku/lane-addendum.md:233-241` and `.ufo/prompts/kasegi-round-44.md:374-379`: record the planner=L1 mapping and the wave seat count / role mix / dead seats / residual call / round total |

**Predicate.** Green iff a report is found at the declared path — default `--fleet-report /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kasegi.md`, or the lane-committed report block under `.ufo/waves/round-44/w1/` bound by a landing receipt (`report-path=` + `report-sha256=` + `block-sha256=` equal to the block's own sha256) — and it carries a line matching `planner` **and** `L1`, and a line matching `L2` **and** (`residual`|`residual call`); the counter prints the report's sha256 and `landing=bound|asserted`. Absent report → red, never vacuous. **Base** = red (round-43 0/0; round-44 absent). Red-before control: mutant with the planner line only → red.

### D5 — wave-evidence hygiene (§6.5), three conjuncts

| leg | measured at base |
|---|---|
| a. registry names | `.ufo/waves/round-43/w1-REGISTRY.txt:7` `names=` empty while `seats=73`; no `.ufo/waves/round-44/w1-REGISTRY.txt` in the export; round-44 dispatch `registry.members` = **66** seats (`counts={"spawn":66,"resume":0,"total":66}`) |
| b. transcript self-identification | `.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt` has `^export-ref=` lines **0**; the run sibling carries `export-ref=de09313e8edb98280b19767d0094bb2dd8031d73` |
| c. aborted-write leftover | `find base/.ufo/waves -name '*.tmp'` → **0**; `ls .ufo/waves/round-43/final-gates/*.tmp` → No such file (the 2137 B leftover named by the spotcheck is absent from the worktree at HEAD; untracked, so no commit records its removal). This leg is **already green** |

**Predicate.** Green iff all three: (a) `.ufo/waves/round-44/w1-REGISTRY.txt` exists with `names=` non-empty and its name count equal to `seats=` and to `len(dispatch.registry.members)`, and a committed lane emitter (`corpus/instruments/wave-registry.py`, read-only re-run over the export's `wave1-dispatch.json`) reproduces the `names=`/`seats=`/`counts=` lines byte-identically; (b) the r42 selftest file contains `^export-ref=de09313e8edb98280b19767d0094bb2dd8031d73$` matching the run sibling, appended (numstat deletions 0); (c) no `*.tmp` under `.ufo/waves/` in the export and none in the lane worktree (`git status --porcelain`). **Base** = red by conjunction (a red, b red, c green). Red-before controls: registry mutant `names=` count ≠ `seats` → red; transcript mutant with a different ref → red; `.tmp` planted → red.

Ownership note: no registry emitter is committed in this lane (`grep -rln 'attack_seats'` inside the lane finds only `w1-REGISTRY.txt` and `ScribeReportSkeleton.md`; the token appears in other lanes' repos, which this lane must not touch), so "fix the emitter" has no lane-owned bytes to fix. Committing the lane emitter above is the only durable, gradable closure; if L1 rules the emitter operator-owned, D5 stays open and C1 cannot reach 8/8 — that must be recorded, not papered over.

### D6 — `SHONEN.md` lost one base byte (§6.6)

| leg | measured at base |
|---|---|
| tail bytes | `ab98fac9` `…0a 0a`; `dbd2e10` and `5ab3a60`/`6631401` `2e 0a` (`…`[~]`.` + LF, no final empty line) |
| append-only | `git diff --numstat 5ab3a60 6631401 -- SHONEN.md` empty |
| structure | no `^## SHONEN` heading at any of `ab98fac9`/`dbd2e10`/`5ab3a60` (headings are `## BLOCK SHONEN.md`, `## Round 41 evidence`, `## Round 42 evidence`); 36 `- [~]` lines at `ab98fac9`, 40 after round 43 |

**Predicate.** Green iff the file's last two bytes are `0a 0a` **and** numstat deletions for `SHONEN.md` base→final = 0 (the blank line is restored when the file is next appended, never by rewriting a box). Do not pin heading/box counts: the round-43 append legitimately added four box lines. **Base** = red (`2e 0a`). Red-before control: mutant that appends an evidence line but leaves the single LF → red.

Observation outside the frozen list (not counted, no widening): the spotcheck §1 row `grep -c '^## SHONEN' → 1` is itself false at `dbd2e10` and `5ab3a60` (0). The D6 predicate above deliberately does not use it.

### D7 — report pointer retarget (§6.7)

| leg | measured at base |
|---|---|
| claim | SHONEN bullet: "the two new instruments are registered in `corpus/instruments/README.md`" |
| reality | `grep -cE '^\|.*r43-closure\.sh' corpus/instruments/README.md` → **0**; `grep -cE '^\|.*claim-package-check\.py'` → **0** |

**Predicate.** Green iff `corpus/instruments/README.md` has ≥1 line starting with `|` containing `r43-closure.sh` and ≥1 containing `claim-package-check.py` (whole basenames), append-only (numstat deletions 0). This takes the defect's own second option ("append the two rows"), which makes the existing pointer true instead of adding a second pointer sentence. **Base** = red (0/0). Red-before control: a row naming a near-basename (`r43-closure.sh.bak`) → red.

### D8 — before-cell token (§6.8)

| leg | measured at base |
|---|---|
| cited control | `.ufo/waves/round-43/c1-controls/do-nothing.txt` §A: `ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory` then `exit=2` (its `ls`); the file's tokens are `exit=1` (stand-in summary) and `exit=2` — no `127` |
| claimed token | `claims.json` C1 `before` (and round-43 report C1 cell) say the absent suite run exits `127` |
| re-derived value | export of `ab98fac9`, then `bash corpus/instruments/r43-closure.sh` → `bash: corpus/instruments/r43-closure.sh: No such file or directory` **exit=127** |
| committed measurement | `grep -rl 'absent-run exit=127' base/.ufo/waves` → **0** |

**Predicate.** Green iff the counter re-derives `127` from the `ab98fac9` export **and** either (M) a committed transcript under `.ufo/waves/round-4*/` carries `absent-run exit=127` on a line whose file also names `corpus/instruments/r43-closure.sh`, or (C) a committed correction (erratum entry with `supersed`, or a column-0 `Correction (round 43)` line) names `127` **and** `exit=2` together; and the re-derived code equals the value the correction names (a correction asserting another code reds). **Base** = red (neither M nor C; control token measured `exit=2`). Red-before controls: correction naming `exit=127` without the control token → red; measurement transcript with `exit=126` → red.

## 3. Red-before control per changed gate

C1's after-state requires "at least one red-before control per changed gate". The changed gates and their controls:

| gate | change | red-before control |
|---|---|---|
| `r44-routed-defects.py` (new) | grades D1–D8 | `--root <base-export> --baseline <base>` → `resolved=0/8 exit=1` (control A); every `D<n>` line shows `base=red` |
| `wave-registry.py` (new, D5a) | emits `names=`/`seats=`/`counts=` from the dispatch | run over the frozen base dispatch with an emptied names list → `names=0 seats=66` mismatch, exit 1; the r43 registry (names empty, seats 73) is the committed red instance |
| landed r43 suite (unchanged) | must stay `closed=19/19` after the corrections | final export `suite=closed=19/19`; a correction that reds K14–K19 turns `suite` red and credits nothing |
| existing K14–K19 (unchanged) | bytes must not move | D2's `k18=unchanged` sha equality is the check; a widened K18 reds D2 |

No gate is changed by this seat; nothing here is a claim that a gate was run.

## 4. Do-nothing discrimination (exact commands, expected output)

```
# A. frozen base, base baseline (the C1 control)
python3 corpus/instruments/r44-routed-defects.py \
  --root /fast/scratch/hyaku/kasegi-r44/<seat>/base \
  --baseline 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a
→ routed=8 resolved=0/8 exit=1     (every D: base=red final=red; D5c green but conjunctive)

# B. final export against itself: the red-before rule is load-bearing
python3 corpus/instruments/r44-routed-defects.py --root <final-export> --baseline <final-ref>
→ routed=8 resolved=0/8 exit=1     (base=green for the fixed defects, so closed=0)

# C. worktree refusal
python3 corpus/instruments/r44-routed-defects.py --root kasegi-shokunin --baseline 5ab3a60…
→ exit=2, no payload lines

# D. unresolvable baseline
--baseline deadbeef… → baseline=ref-not-found exit=1
```

Control B is the one that makes the do-nothing kill rule mechanical: a tree cannot score its own fixes, because the same predicate must be red at the declared baseline. Controls A and B together are what `.ufo/waves/round-44/controls/c1-do-nothing.txt` must record (F0).

## 5. Reproduction recipe for the integrator

```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; W=/fast/scratch/hyaku/kasegi-r44/<seat>/verify
mkdir -p $W/base $W/final
git -C $L archive 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a | tar -x -C $W/base
git -C $L archive <final-ref> | tar -x -C $W/final
python3 $W/final/corpus/instruments/r44-routed-defects.py --root $W/final \
  --baseline 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a --work $W/run
# expect: suite=closed=19/19 ; D1..D8 base=red final=green closed=1 ; routed=8 resolved=8/8 exit=0
python3 $W/final/corpus/instruments/r44-routed-defects.py --selftest ...   # selftest cases=<n> failures=0
```

## 6. Findings that change the plan

1. **F0 (blocker):** the frozen C1 control path `controls/c1-do-nothing.txt` is absent; the control exists as `controls/do-nothing.txt`. Commit the file at the frozen path with the §4 transcript, or C1's control is dead (same class as D8).
2. **D4 is cross-repo.** The round report lives in the fleet repo (`.ufo/reports/round-44/kasegi.md`), not in the lane export, so the frozen `--root <lane-export>` invocation cannot see it. The counter needs a declared default `--fleet-report` (read-only, digest printed) or the lane-committed block + landing-receipt branch; without one, D4 must be red by absence, never green by assumption.
3. **D5a has no committed emitter to fix.** `grep -rln 'attack_seats'` over the fleet finds only emitted files, so the lane must commit the emitter (`corpus/instruments/wave-registry.py`) for the fix to be gradable; otherwise D5 stays open and C1 is capped at 7/8.
4. **D5c is already green at the frozen base** (the `.tmp` was removed before the freeze). It contributes no discrimination; D5's red-before comes from a/b. Saying so prevents a false "3 of 3 fixed" reading.
5. **The spotcheck's `grep -c '^## SHONEN' → 1` conformance row is false** (0 at `ab98fac9`, `dbd2e10`, `5ab3a60`). It is outside the frozen 8; recorded so no predicate inherits it.
6. **K19 pins `claims.json` sha256** (`freeze.txt` `claims-sha256`), so every correction must be an appended erratum/marker — no claims edit. The predicates above assume that and check numstat deletions = 0.

## 7. Limitations

- The `.tmp` leftover was untracked, so it is invisible to any export-based check; D5c is graded on the export (absence) **and** the lane worktree, and is disclosed as already satisfied.
- D4's fleet-file binding is asserted unless `--fleet-report` is supplied; the counter prints `landing=bound|asserted` so the weaker mode is visible.
- The counter cannot re-derive a composite base tally of the landed suite without running it; D1 therefore accepts the six per-limb transcripts and refuses an unbacked composite replacement (fail-closed), which is the spotcheck's own remedy.
- No predicate here was executed against a final tree (none exists yet); every base value was measured, every final value is a specification. That is the difference between this plan and a receipt.
- Scratch `/fast/scratch/hyaku/kasegi-r44/R44Exec1/` removed after writing this file; no tool installs; no pacman; no git/jj mutation; no lane byte outside this report.
