VERDICT: DRAFT-READY

Seat: R46ScribeQuality (scribe, QUALITY drafter). Lane: kasegi round 46. Base `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`; freeze `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5`; lane HEAD at draft `323d1f5`. Scope: the append-only `corpus/QUALITY.md` block (R50-R52). Not committed; `corpus/QUALITY.md` is untouched.

## Built

- `.ufo/waves/round-46/wave1/R46ScribeQuality.draft/quality-append.md`: 10 lines, 5856 bytes, sha256 `88172f1e0d269d1d9b6eaed1f56aefb7adb17f24f2bba220d6f978c26c6c0260`. One `## Round-46 additions - ...` heading, the header `| id | criterion | grounded in |`, rows R50 (class landing), R51 (scope/vacuous), R52 (number-drift/attribution). Each criterion cell names `corpus/lessons/round-46.md` § Mistakes as its lesson; that file does not exist yet (see Limitations).
- Scope note: the milestone's F28 entry and C1 re-grounds are other seats' items; this seat built no entry and no re-ground.

## Findings

### F1 — frozen C1 counter replayed at base (do-nothing) and at the freeze tree
Command (tool = freeze copy of `corpus/instruments/r46-c1-gate.py`; the base export has no counter): `python3 $S/freeze/corpus/instruments/r46-c1-gate.py --root $S/base --baseline $S/base`. Output (verbatim, last lines):
```
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
gate L3 pass=0 read=recheck-lines-clean=0
gate L4 pass=0 read=entry-mode-green=0
gate L5 pass=0 read=append-only=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
```
Freeze tree (`--root $S/freeze`): the same seven lines, final line `c1-gate fixed=1/7 exit=1`. Both trees read `1/7`, matching `claims.json` C1 `expect_before` and `freeze_tree_reading`. Counter sha256 at freeze `b0c730c834b4d7c6…`, matching `freeze.txt` `c1-gate-sha256`.

### F2 — frozen C2 counter replayed at base and freeze
`python3 $S/freeze/corpus/instruments/r46-c2-gate.py --root $S/base` → final line `c2-gate fixed=1/7 exit=1` (G1 `rows=27 admitted=27 dup=0`; G4 `manifest-absent`). `--root $S/freeze` → `c2-gate fixed=2/7 exit=1` (G4 `recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`; G7 `census-rc=0 ok-line=1`). Matches the claim's base `1/7` and freeze `2/7`. Counter sha256 `0ee958578b592370…` matches `freeze.txt`.

### F3 — the claims' plain second measurements, run verbatim at both trees
Run in each export (base, then freeze), output as printed:
- C1 `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` → `23` (both). Also `grep -c` over `^recheck:` lines → `64` (both).
- C1 `python3 corpus/instruments/recheck-audit.py --root . --quiet | grep '^executes='` → `executes=40 gated=24 broken=0` (both).
- C1 `python3 corpus/instruments/score-gap.py | grep '^gap:'` → `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims` (both).
- C2 frontier rows → `27` (both); SOURCES rows → `72` (both); `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `64` (both).
- C2 before-grep `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` → no output, rc=1 (both).
- C2 secondary `python3 corpus/instruments/r44-frontier-count.py --root . --expect 28` → `frontier expected=28 admitted=27 verdict=SHORT exit=1` (both).
Every declared before-value reproduces at both trees. The S073 `source-recheck.py` line declares no before and was not run.

### F4 — freeze controls rerun into scratch and diffed against the committed receipt
`python3 .ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba --work <scratch>` → exit 0; `diff controls/freeze-controls.txt <rerun>` → no output (0 lines); final line `controls total=9 red=9 green=0`. Rows that R51 cites, as printed: `c1 marker-only` → `gate L1 pass=1`, `gate L2 pass=1`, `gate L3 pass=0` … `gate L6 pass=0`, `gate L7 pass=1`, `c1-gate fixed=3/7 exit=1`; `c1 gutted-entry` → `gate L5 pass=0`, `gate L6 pass=1`, `c1-gate fixed=6/7 exit=1`; `c1 fabricated-anchors` → `c1-gate fixed=0/7 exit=1`. Discrimination: the do-nothing control reads `1/7`, so these red readings are not a counter that passes everything.

### F5 — R50 evidence: the landing gate and the round-45 pair do not reproduce here
- `find / -name 'r46-landing-gate*' 2>/dev/null` → no output. The wave spec names it (`.ufo/waves/round-46/wave1-spec.json` mentions `r46-landing-gate.py` as a stdlib reads-only gate), but it is absent at `9f23aab`, `914ca0b` and `323d1f5`. R50's `enforced-by` cell says so; the row is a review duty until the instrument lands.
- `git cat-file -t a1f7761` → `fatal: Not a valid object name a1f7761`. `git log --all --grep=a1f7761 | wc -l` → `0`. `git log --all --oneline -- .ufo/reports/round-45` → no output. The lesson's report commit (`corpus/lessons/round-45-verifier-spotcheck.md:13,22,95`) is not in this clone; its "hash resolves" statement is not reproducible here.
- `git ls-remote origin refs/heads/master` → `323d1f5d825a61cfd0dbf93f9580e092ee21c72a	refs/heads/master`; `git merge-base --is-ancestor 2998baa 323d1f5` → ancestor (exit 0).
- `git log -1 --format='author=%ad committer=%cd' --date=format:%H:%M:%S 2998baa` → `author=19:36:30 committer=19:36:31`. The spot-check's `19:36:30` is the author date and does not name its field (R50 and R52 require the field be named).

### F6 — the R50 date rule discriminates on a fixture repo
Fixture `git -C "$D" init` (toplevel asserted equal to `$D`), two commits: report at `19:30:06 -0300`, lane commit at `19:36:30 -0300` (the round-45 order). Plain test `[ "$A" -le "$B" ]` on committer timestamps (`git log -1 --format=%ct`): `FAIL lane=1793226991 report=1793226606`. Reversed control (report at `19:40:00 -0300`): `PASS lane=1793226991 report=1793227200`; `git merge-base --is-ancestor <lane> <report2>` → `yes`. The test fails the bad order and passes the good one.

### F7 — R6 preamble and append-only check
`git show 914ca0b:corpus/QUALITY.md | head -c 83551 | sha256sum` → `7b57b312d6e6298508df05e877ef630c26a09f67cf0e530431d7580e7455792f`; `wc -lc` → `382 83551`. HEAD `323d1f5` gives the same hash (QUALITY.md is identical at base and HEAD). Scratch copy: base file plus the draft appended → `lines=392`; `head -n 382 | cmp - <base>` → identical; heading count `1`.

### F8 — every cited anchor re-read
`sed -n '22p;95p;97p;99p' corpus/lessons/round-45-verifier-spotcheck.md` gives conformance (a), §6 item 1 "Report/commit ordering", §6 item 3 "Counters are pinned-artifact graders", §6 item 5 "Scores held". `.ufo/waves/round-45/counter-errata.md:26` → `## Claims erratum 1 — the before-value is tree-relative`. `corpus/lessons/round-45.md:11` → `M45-1 | number-drift`. `corpus/lessons/round-44.md:16` → `M44-4 | Draft C1 counter accepted marker-only evidence`. `grep -c 'Distance-to-next-score' SCORECARD.md` → `1`.

### F9 — R52's enforcement claim checked
`grep -n plain corpus/instruments/freeze-check.py` → no output: the freeze checker never reads a `plain` field, so R52 is correctly stated as a review duty, not a gate.

## Limitations and open items for the L1

1. `corpus/lessons/round-46.md` does not exist; the criteria cite its § Mistakes, with the M46 ids unminted. The landing commit must mint them or the cells dangle.
2. `r46-landing-gate.py` is absent; R50 is a review duty until it lands. Its ordering evidence is reported by the spot-check, not reproduced in this clone (F5).
3. R51's per-claim naming is semantic; L6 checks only that rows are load-bearing (stated in the cell).
4. R52's plain list is not mechanised (F9); the freeze-tree reading is checked only by the claim text.
5. Not run: `freeze-check.py`, the counter selftests, `source-recheck.py --source S073`, and the F28 entry (not my item).
6. The draft's R6 hash is for the base file; the landing commit must re-run `head -c 83551 corpus/QUALITY.md | sha256sum` at its own tree.
7. Round-45 spot-check item 2 ("counter classification") is settled in its own erratum and not re-opened here.

Tool installs/updates: none. Scratch `$HYAKU_SCRATCH/kasegi-r46/R46ScribeQuality` removed after the checks. No commit, push, index or git mutation; `git ls-remote` and read-only log/show/diff only. No edits to `corpus/QUALITY.md`, the fleet repo, sibling lanes, MANIFEST.json, `.ufo/state` or ~/Projects/shokuknow. The `R46ExecPlain.draft/` and `R46ScribeRegistry.draft/` directories in `wave1/` are other seats' and were not touched.
