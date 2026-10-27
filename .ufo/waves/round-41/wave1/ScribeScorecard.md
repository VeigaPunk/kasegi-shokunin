# ScribeScorecard — round 41 wave 1 receipt

Seat: ScribeScorecard (scribe, leaf). Item: draft the SCORECARD.md `## Round 41 result` section.
Judged axes: depth:verifiability, coverage. Frozen claims read: `.ufo/waves/round-41/claims.json` (not edited).

## Deliverable

`.ufo/waves/round-41/wave1/ScribeScorecard.round41-table.txt` — 17 lines, 4365 bytes,
sha256 `ff1d63e33e39f082677c7fdb7261ddc02c294d10d5f6976af62032d383b130d8`.

Revision 2 (after `CORRECTIONS-L1.md` item 2, mid-wave): the depth:verifiability cell now reads "the CritKillRule eight escape states (F1–F8; the L1 freeze correction supersedes the file's \"7 distinct escape states\" prose)" instead of "seven escape states". Revision 1 was 4274 bytes, sha256 `8693ff241c47d2041303907b6756838fcd3bf94d4cd67a3154882c29d4c2d4a8`.

Landable bytes only: `## Round 41 result` heading; the 5-column table (`Axis | Score before r41 | Score after r41 | Evidence pointer | Last change`) with the three required rows (depth:verifiability 4→4 held, coverage 8→8 held, depth:density 9→9 non-target guard); the measured-before block citing freeze `fbba3d96…` and the three before-control files; the measured-at-Y block; the capabilities line; the saturation line; the `Planned for round 42` stub. No validation table, no notes inside the deliverable.

Shape check (ran on the deliverable): every table row has 6 pipes / 5 cells (header, separator, three rows); 0 lines with trailing whitespace or tabs; placeholders `<<<Y>>>` ×5 and `<<<W2-VERDICT>>>` ×1.

## Placeholder contract (for L1 substitution after wave 2)

- `<<<Y>>>` ×5: (a) depth:verifiability evidence cell `At Y <<<Y>>>`, (b) same cell `--selftest --export-ref <<<Y>>>`, (c) measured block `Measured at Y <<<Y>>>`, (d) measured block `--export-ref <<<Y>>>`, (e) measured block `--selftest --export-ref <<<Y>>>`.
- `<<<W2-VERDICT>>>` ×1: end of the depth:verifiability evidence cell (`Wave-2 verdict: \`<<<W2-VERDICT>>>\`.`). Nothing is pre-graded: the score-after cell reads `**4 (held)**` and no wave-2 outcome is asserted, per the r40 D1 overclaim class (r40 graded C1 verified while its kill rule fired).
- No hash is written for J or Y anywhere in the section (`judged_head_rule`: a commit cannot contain its own hash); base and round-40 judged head are cited by resolvable 8-char prefixes only.

## Commands run (read-only; exact output)

1. Freeze object and its claims file:
   - `git -C <lane> cat-file -e fbba3d96cdf8d37c1ea41304a1ba35691329684b:.ufo/waves/round-41/claims.json` → present.
   - `git -C <lane> log -1 --format='%H %cI %s' fbba3d96…` → `fbba3d96cdf8d37c1ea41304a1ba35691329684b 2026-10-27T05:07:54-03:00 round-41: claims freeze (C1 r41-closure.sh I1-I12; C2 F24 RFC 9116) + do-nothing controls + census baseline`.
2. Base commit resolution (see Finding F1):
   - `git -C <lane> cat-file -t 5b29ea1439450b712581edf5f0bf98dfb262ab` → `fatal: Not a valid object name`.
   - `git -C <lane> rev-parse --verify --quiet 5b29ea1439450b712581edf5f0bf98dfb262ab` → exit 1.
   - `git -C <lane> rev-parse 5b29ea1` → `5b29ea1439450b712581edf5f0f0bf98dfb262ab`; `cat-file -t` → `commit`; `merge-base --is-ancestor <that> HEAD` → exit 0; subject `round-40 verifier spot-check (integrator, hyaku): non-author admit/reject`.
   - Round-40 judged head: `git -C <lane> rev-parse c7aea5e` → `c7aea5ef97902f38289cbdc1cf267068876a62dd`, `cat-file -t` → `commit`.
3. Before-state counters re-read on the resolved base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` with `git show <base>:<path>`:
   - frontier rows `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 23
   - registry rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 62
   - `git ls-tree --name-only <base> corpus/knowledge/ | grep -c '\.md$'` → 59
   - F24 rows in README → 0; S063 rows in SOURCES → 0; `corpus/instruments/r41-closure.sh` in tree → absent; `r40-closure.sh` → 1734 lines.
   These agree with `.ufo/waves/round-41/c2-controls/before.txt` (frontier 23, registry 62, knowledge 59, entries citing S063 0, harness `entries=26 pass=26`, binding `records=54 bound=54`, audit `expected=59`) and with `c1-controls/do-nothing.txt` (`bash: corpus/instruments/r41-closure.sh: No such file or directory`, `exit=127`). Census baseline: `census-before.txt` exit 0, W04 for S028/S029 only.
4. Density guard: `corpus/instruments/density.py` present at base (9472 bytes).
5. 0-gated distance figure used in the round-42 stub: `TMPDIR=<scratch> python3 corpus/instruments/score-gap.py` → `gap: 24 of 59 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`; threshold line read as `SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."`. Working tree at HEAD `b3b08b2`; `git diff --stat 5b29ea1439450b712581edf5f0f0bf98dfb262ab b3b08b276af6146217efd89f7595243a644ed00b` → `7 files changed, 1631 insertions(+)`, all under `.ufo/waves/round-41/`, so the corpus tree measured is the base tree.
6. `git -C <lane> status --porcelain` → only untracked `.ufo/waves/round-41/{kasegi-r41-build.ready,kasegi-r41-build.ready.partial,wave1-run.err,wave1/}`; no tracked file written by this seat.
7. Round-30..41 SCORECARD sections read for format (`sed`-range reads of `SCORECARD.md:1480-1600`), plus `SKILL.md:1095-1145` for the D6 blank-line breakage (round-40 registry block: header at offset 25, separator at 26, **blank line at 27**, `r40-closure.sh` row at 28).

## Findings (verbatim, for the canonical judge)

F1 — **frozen base hash is malformed (38 hex chars, not a git object).**
`claims.json.base` = `5b29ea1439450b712581edf5f0bf98dfb262ab` (length 38). The lane base commit is `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (length 40; the claims string is missing `f0` at index 26). `git rev-parse --verify --quiet <claims string>` → exit 1.
Consequence: C1 counting command 3 as frozen (`--export-ref 5b29ea1439450b712581edf5f0bf98dfb262ab`) cannot print `closed<12/12 exit=1`; it fails on a bad revision first. The I12 base limb is unreachable as literally written, and the same string was carried by `c1-controls/do-nothing.txt`, `build-wave1-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`, `build-wave2-spec.py` (grep -rl over `.ufo/waves/round-41/` at my first read; no occurrence of the 40-char form existed then). I did not edit claims or controls.

State at my final read (working tree, uncommitted): `git status --porcelain` reports ` M .ufo/waves/round-41/{claims.json,c1-controls/do-nothing.txt,build-wave1-spec.py}`. `git diff` shows the literal replaced by `5b29ea1439450b712581edf5f0f0bf98dfb262ab` in `claims.json` (4 occurrences; file still parses, `base` length 40), in `build-wave1-spec.py` (`BASE = "…"`), and this line appended to `c1-controls/do-nothing.txt`, quoted verbatim: `Erratum (freeze, same round): the base hash literal committed in the freeze files was a 38-hex transcription (…f5f0bf98…, missing f0) that resolves to no object; corrected to the 40-char 5b29ea1439450b712581edf5f0f0bf98dfb262ab (same commit, prefix 5b29ea14) — caught by seat ScribeShonenLog. This control's verdict is unchanged: the suite was absent (exit 127) at base either way. Mined as the round's freeze-typo mistake; the freeze-time dry-run guard (git rev-parse --verify of every 40-char literal) is the fix.` Residual 38-char occurrences remain in `.ufo/waves/round-41/wave1-spec.json`, `wave1-dispatch.json` and `build-wave2-spec.py` (the last drives the wave-2 spec), so the defect is not fully swept; that sweep is the L1's call, and wave-2 seats reading those two files still inherit the bad literal.

Peers messaged with the exact strings before that correction: `ExecSuiteCore`, `ExecI10NegCtl` (negative controls), `ScribeCorrections`, `ExecI1Blocks`.
The L1's authoritative note on both freeze defects is `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` ("AUTHORITATIVE, read first"), whose item 1 reads, verbatim: "The real round-41 base is the 40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (prefix 5b29ea14). The freeze files wrote a 38-char literal missing `f0`, which resolves to no git object. Any seat running `--export-ref <base>` or `git archive <base>` MUST use the 40-char hash above. Suites must report an unresolvable `--export-ref` as a distinct red (`ref-not-found` in payload), never as a vacuous `closed<12/12 exit=1` — that T-class vacuity is what the freeze punishes."
My deliverable therefore cites the base only as `5b29ea14` (8-char prefix, resolves uniquely to the 40-char object under both the pre- and post-erratum reading); it needs no change for the correction.

Independent corroboration (peer message, not a run by this seat): `ScribeCorrections` reports `5b29ea1` resolving to `5b29ea1439450b712581edf5f0f0bf98dfb262ab` on its side and will carry the same claims-base note in `.ufo/waves/round-41/wave1/ScribeCorrections.md`; its correction blocks never name the base, so no deliverable change follows there.

F2 — **item spec wording vs its own column list.** The item says "four columns: Axis | Score before r41 | Score after r41 | Evidence pointer | Last change" — that list is five columns, and the round-40 model section is five columns. I landed the five-column form (`Axis`, `Score before r41`, `Score after r41`, `Evidence pointer`, `Last change`); no cell was dropped.

F3 — **round-40's own result table has no depth:density row** (it lists depth:verifiability and coverage only). My item requires three rows, so the density row is added in the round-39 style (`9 | 9 | Non-target guard only … | r15 (held r41)`).

F4 — **D6 repair vs I12 "SKILL.md append-only" (resolved by the wave-1 spec, not by me).** D6 is a blank line splitting the round-40 registry table; a row after a blank line is rejected by the planned I7 limb. `ExecI7Registry`'s item resolves the tension: the L1 appends a re-declared block (header + separator + the verbatim r40 row) instead of deleting the blank line, so SKILL.md stays append-only. The density row states exactly that and claims no density move.

F5 — **I11 escape count: committed bytes say eight, the frozen claims and the file's own prose say seven.** `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` item 2 reads, verbatim: "The committed `.ufo/waves/round-40/wave2/CritKillRule.md` carries EIGHT `### F` escape states (F1-F8), not seven. I11's target is all eight committed states; the I11 payload must read `escapes=8` and `red=8`, naming F1-F8. (The file's own intro prose says \"7 distinct escape states\"; the committed headings are authoritative.)" I re-derived the count myself at the freeze commit: `git show fbba3d96cdf8d37c1ea41304a1ba35691329684b:.ufo/waves/round-40/wave2/CritKillRule.md | grep -cE '^### F[0-9]+'` → 8, headings `F1 … F8` at lines 41, 58, 80, 94, 107, 127, 142, 152, with line 9 prose "**Verdict: 7 distinct escape states reproduced.**".
Residual conflict, reported not fixed: `claims.json` still reads "I11 each of the seven committed CritKillRule escape states reds the limb it escapes" and its C1 kill rule still says "the CritKillRule seven escape states" — the L1 correction changes the target count but not those two literals. A suite implementing I11 from claims.json alone would name F1–F7 and leave F8 unred. My deliverable follows the authoritative correction (`eight … (F1–F8)`) so it stays consistent with the `escapes=8 red=8` payload the L1 specified.

## Unverified at draft (stated as such)

- Every after-state value is claims-derived: Y and J are not committed while wave 1 is in flight. The C1 row's `closed=12/12`/`selftest cases=12 failures=0` and the base/`c7aea5ef` reds are the frozen counting commands' expected outputs, not runs of a suite that does not exist yet at this seat's read (`r41-closure.sh` absent from base, verified in step 3).
- The C2 row's counters are the claims.json after-state; the `PASS F24 ids=S063` line and the junk-twin rejection are named as the harness/ExecControls control outputs, not re-run by this seat.
- The `Correction (round 41)` clause in the depth:verifiability cell describes the I1 limb (drafted by `ExecI1Blocks`/`ScribeCorrections`), not bytes I read.

## Scope compliance

Writes: the deliverable above plus this receipt, scratch under `/fast/scratch/hyaku/kasegi-r41/ScribeScorecard/` (removed before yield). No mutating git, no edits to claims/controls/SCORECARD/LOG/SHONEN/SKILL/PROVINCE/corpus, no fleet-root or source-tree writes, no subagent dispatch, no installs (no tool changes; nothing recorded under the tooling authorization).

Known limits: the section asserts no closing commit; placeholders must be substituted by the L1 after wave 2; the F1 erratum is required before any seat runs the frozen base export command as written.
