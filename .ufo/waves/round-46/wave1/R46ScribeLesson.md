VERDICT: DRAFT-READY

Seat R46ScribeLesson (lesson drafter). Draft only: `.ufo/waves/round-46/wave1/R46ScribeLesson.draft/lesson-skeleton.md` (the skeleton of `corpus/lessons/round-46.md`). Nothing committed, nothing mutated, no shared file touched. The skeleton carries 39 `[[FILL-BY-L1: …]]` placeholders by design; the L1 fills them, and the committed lesson must contain none.

## Findings

### 1. Skeleton shape (`## Gate`, `## Mistakes`, `## SOURCES log`, `## Routed defects`)
- Attacked/built: the skeleton, shaped on `corpus/lessons/round-45.md` (its `## Mistakes` table has seven columns; its `## Gate` table has six).
- Command: `grep -n '^## ' .ufo/waves/round-46/wave1/R46ScribeLesson.draft/lesson-skeleton.md`
- Output: `16:## Mistakes` / `25:## Gate — frontier, source, and rejection` / `57:## SOURCES log` / `65:## Routed defects`.
- Command: `grep -c 'TBD\|XXX\|TODO'` (case-insensitive) on the same file → `no TBD/XXX/TODO`.
- Limitation: the round-45 `## Wave and result`, `## Score and trend verdicts` and `## SHONEN` sections are not in the skeleton, because the assignment named four sections; the L1 adds them.

### 2. M46-1 (class `landing`) — the mined mistake, and a finding that weakens its evidence
- Attacked: `corpus/lessons/round-45-verifier-spotcheck.md` §1 defect (a) (`:22`) and §6 item 1 (`:95`).
- Command: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin cat-file -t a1f7761`
- Output: `fatal: Not a valid object name a1f7761`
- Command: `git log --format='%h %ad %s' --date=iso -- .ufo/reports/round-45/kasegi.md` (lane repo)
- Output: (empty). `git ls-files .ufo/reports | wc -l` → `1` (`round-21` only).
- Command: `git log -1 --format='%h %ad %s' --date=iso 2998baa` → `2998baa 2026-10-28 19:36:30 -0300 round-45: wave 2 results, final measurement, errata, lesson, LOG, SCORECARD`. `git merge-base --is-ancestor 2998baa 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba` → ancestor (exit 0).
- Reading: the spot-check's report-ordering evidence names a report commit `a1f7761` (19:30:06) that this lane repository does not hold, so the report's ordering against `2998baa` cannot be reproduced from the lane. The closure's claim "the report precedes the commit it cites" is therefore not re-measurable here. The mistake is still carried as M46-1 (the spot-check's own §6 item 1 names it), but the lesson must state that its evidence is the closure's reading, not a lane-side re-run. The report file is not in the lane repo at all (`git ls-files .ufo/reports` → `round-21` only).
- Also: `2998baa` and its sibling commits `47ed5b5` and `6e9bb8c` share the second `19:36:30`; no ordering inside that second is observable.
- Fix status: `r46-landing-gate.py` is absent at freeze (`git ls-tree -r --name-only 9f23aab | grep -i landing` → only `.ufo/waves/round-34/...f17-landing-state.txt` and `.ufo/waves/round-41/...RevErratumLanding.md`); QUALITY `R50` absent (`git show 9f23aab:corpus/QUALITY.md | grep -c 'R50'` → `0`). Fix counts only after its red-before receipt on the round-45 pair, which cannot be produced in the lane repo while the report bytes are absent: this is a blocker for the L1 (where are the round-45 report bytes committed, or is a fixture allowed to stand in and labelled as such).
- Relation to considerthese proposal 3 (`considerthese/2026-10-26.md:31`): ledger row `corpus/knowledge/considerthese-proposals-ledger.md:140` reads `landed — unchanged`. [INFERENCE, not run] its checks do not read a report's cited hashes; the skeleton records this as an inference for the L1 to confirm.

### 3. Counter and control falsification (the frozen counters, re-run by this seat)
- Attacked: `corpus/instruments/r46-c1-gate.py` and `r46-c2-gate.py` at freeze `9f23aab`; the frozen digests.
- Command: `sha256sum` of both files from a `git archive 9f23aab` export → `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294` and `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`; `freeze.txt` records `c1-gate-sha256 b0c730c8…2294` and `c2-gate-sha256 0ee95857…c6f3` — both match.
- Command (base tree): `python3 -I <frz>/corpus/instruments/r46-c1-gate.py --root <base> --baseline <base>` → last line `c1-gate fixed=1/7 exit=1`.
- Command (base tree): `python3 -I <frz>/corpus/instruments/r46-c2-gate.py --root <base>` → last line `c2-gate fixed=1/7 exit=1`.
- Command (freeze tree, full export of 9f23aab: corpus SKILL.md PROVINCE.md SCORECARD.md SHONEN.md LOG.md): `c1-gate fixed=1/7 exit=1`; `c2-gate fixed=2/7 exit=1`.
- Reading: the do-nothing reading matches the claims' `expect_before` (C1 `1/7`) and the freeze-tree reading (C1 `1/7`, C2 `2/7`) exactly. The frozen counters are not falsified on their before-values. They have not been tested against the tip; that is the non-author closure's.
- Command (base): `python3 corpus/instruments/recheck-audit.py --root . --quiet` (base export) → `executes=40 gated=24 broken=0 (…)` and the summary line `lines=64 total=64 pass=64 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1`. The claimed "before" is `gated=24` (matches). The recheck-audit process exits 1 at base because 24 lines fail closed; this is the lane's own reading and is recorded, not hidden.
- Limitation: the milestone "falsify the frozen counters and controls" (building the C1 re-grounds, the F28 entry, and the counter mutants) is other seats' work; this seat did not build or run the F28 entry or any re-ground, and did not run the control set (`controls/freeze-controls.txt` records `total=9 red=9 green=0`, from the freeze's own run, which this seat did not repeat).

### 4. Plain measures (claims' §6 item 3) — base values re-run by this seat
- Command: `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` (base export) → `23`.
- Command: `grep -c '^recheck:' corpus/knowledge/*.md` summed → `64`. `python3 corpus/instruments/score-gap.py | grep '^gap:'` → `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.
- Command: `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `27`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `72`; `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `64`.
- Command: `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` → no output (exit 1).
- Reading: all base before-values in the claims match the measured base. The tip values are the L1's to fill.

### 5. S073 capture and quotes (the skeleton's quote block)
- Command: `sha256sum corpus/source-snapshots/round-46/S073.txt` (freeze) → `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`; manifest pins the same.
- Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` (from a `git archive 9f23aab` export) → `S073:sha256 OK`, `S073:Q1 OK occurrences=1 anchor=560-ok` … `S073:Q8 OK occurrences=1 anchor=578-ok`, exit 0.
- Command: a read-only check of each manifest quote against its anchor ±2 lines, whitespace-normalised: Q1 `:560` (10 words), Q2 `:563` (6), Q3 `:564` (13), Q4 `:566` (18), Q5 `:573` (14), Q6 `:574` (13), Q7 `:577` (20), Q8 `:578` (15): all located at their anchor, all ≤25 words.
- Limitation: the capture is the sha-pinned copy; the live page was not re-fetched by this seat (the non-author closure's slot in the skeleton).

### 6. The S070/S072 registry pair (§6 item 4), base reading
- Command: `grep -n -E 'S070|S072' corpus/SOURCES.md` (base) → rows `:76` (S070), `:78` (S072), and round-44 notes `:107` and `:156`. `:156` reads "S070 is the tier-C rejected directory page"; no line records that S072 supersedes S070.
- Limitation: the S072-supersedes-S070 note itself is the L1's to write at the tip.

### 7. considerthese proposal 3 and ledger old → new
- Command: `grep -n 'quiescence' considerthese/2026-10-26.md` → `31:3. **Add a quiescence gate before `complete`.**`.
- Command: `grep -n '^| 3. Add a quiescence' corpus/knowledge/considerthese-proposals-ledger.md` → rows at `:56`, `:83`, `:103`, `:125`, `:140`; the `## Round-42 dispositions` heading is at `:134`, so `:140` is in that block and reads `landed — unchanged`.
- Reading: the ledger's own note at `:73` says the numeric label is not stable across tables; the skeleton cites the 2026-10-26 proposal and the `:140` row, and leaves the new wording to the L1.

### 8. C2 gate and counts at the tip — not measured here
- The C2 gate and the other counts at the lane tip were not run by this seat (no lane tip exists yet). Left as placeholders.

## Limitations
- The skeleton is a draft; 39 placeholders remain by design and must all be filled by the L1 before commit. The validator-facing check is the placeholder grep: `grep -c '\[\[FILL-BY-L1' corpus/lessons/round-46.md` must print `0` on the committed file.
- M46-1's ordering evidence is not reproducible from the lane repository (finding 2); the lesson must say so.
- No F28 entry, no C1 re-ground, no counter mutant was built by this seat; those are other seats' work.
- Scratch (`$HYAKU_SCRATCH/kasegi-r46/R46ScribeLesson/`, default `/fast/scratch/hyaku/...`) was removed; `ls` on it reports no such directory.
- No install or upgrade was performed by this seat (tooling not needed: `python3` and `git` only).
