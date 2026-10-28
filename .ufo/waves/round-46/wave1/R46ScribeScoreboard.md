VERDICT: DRAFT-READY

Seat R46ScribeScoreboard (scribe, round 46). Drafts only; nothing committed, no git/jj mutation, no shared file touched. Drafts written:
- `.ufo/waves/round-46/wave1/R46ScribeScoreboard.draft/scorecard-append.md` — `## Round 46 result` block (axis table at 4/8/9 held, per-axis promotion limbs, move-log, counting commands at base and freeze, capability row marked `proposed`, round-47 gates).
- `.ufo/waves/round-46/wave1/R46ScribeScoreboard.draft/LOG-entry.md` — `## Round 46 (attempt 1)` skeleton.
- `.ufo/waves/round-46/wave1/R46ScribeScoreboard.draft/SHONEN-notes.md` — one note per box, all `[~]`.

Every tip value is `[[FILL-BY-L1: ...]]`. Scratch: `/fast/scratch/hyaku/kasegi-r46/R46ScribeScoreboard/` (removed at exit).

## Setup and provenance

- Base tree: `cp -r /fast/scratch/hyaku/kasegi-r46/L1/pure/.` → `base/` (the pure export named in the spec).
- Freeze tree: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 | tar -x -C freeze/` (full tree, 9107 files; base-vs-freeze `diff -rq corpus` shows only `r46-c1-gate.py`, `r46-c2-gate.py`, `source-snapshots/round-46` added).
- Counter hashes at freeze, printed by `sha256sum` and matching `freeze.txt`:
  - `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294` r46-c1-gate.py
  - `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6` r46-c2-gate.py
  - `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930` S073.txt
  - `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34` manifest.json

## Findings

### F1 — Frozen C1 counter reads the claimed before-value at base and freeze (HOLDS)
Command: `python3 freeze/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base>`
- base: `c1-gate fixed=1/7 exit=1`; freeze: `c1-gate fixed=1/7 exit=1`.
- Seven gate lines at base and freeze are the do-nothing control in `controls/freeze-controls.txt` (lines `gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64` … `gate L7 pass=1 read=still-gated=24 changed=none`); `diff` of the printed block against the control's `== c1 do-nothing` block: no difference.

### F2 — Frozen C1 marker-only control reproduces and is graded 3/7 (HOLDS, control discriminates)
Scratch copy of base with `recheck:` lines in `corpus/knowledge/claim-gates.md:125` and `corpus/knowledge/claim-package-contract.md:68` replaced by `recheck: true`; the same counter run printed:
`gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64` … `c1-gate fixed=3/7 exit=1`.
`diff` against the recorded `== c1 marker-only` block: identical. The marker-only edit is not graded 7/7.

### F3 — Frozen C2 counter reads base 1/7 and freeze 2/7 (HOLDS)
Command: `python3 freeze/corpus/instruments/r46-c2-gate.py --root <tree>`. Note: this script takes `--root` only; `--baseline` is rejected (`r46-c2-gate.py: error: unrecognized arguments: --baseline ...`, rc 2). The claims' `counter_cmd` has no `--baseline`, so this is my invocation error, not a claim defect.
- base: `c2-gate fixed=1/7 exit=1`, with `gate G4 pass=0 read=manifest-absent` and `gate G7 pass=1 read=census-rc=0 ok-line=1`.
- freeze: `c2-gate fixed=2/7 exit=1`, with `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0` (the capture limb holds at freeze, as `claims.json` `freeze_tree_reading` states).
- `diff` of the base run against the recorded `== c2 do-nothing` block: identical.

### F4 — S073 capture binds at freeze, absent at base (HOLDS)
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073`
- base: `manifest UNAVAILABLE reason=missing`, rc 2.
- freeze: `S073:sha256 OK`, then `S073:Q1 OK occurrences=1 anchor=560-ok` through `S073:Q8 OK occurrences=1 anchor=578-ok`, rc 0.

### F5 — Depth:verifiability before-value is 24 gated of 64 at base and at freeze (HOLDS)
- `python3 corpus/instruments/recheck-audit.py --root . --quiet | grep '^executes='` → base and freeze: `executes=40 gated=24 broken=0`.
- `python3 corpus/instruments/score-gap.py | grep '^gap:'` → base and freeze: `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.
- `grep -c '^recheck:' corpus/knowledge/*.md` summed → 64 at both trees.
- `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` → 23 at both trees.

### F6 — Coverage criterion is already 1.000 and cannot register C2 (FINDING against the 7→8 framing; not a counter defect)
Command and printed output (base and freeze identical):
```
queued=0          awk -F'|' '$2 ~ /^ *S[0-9]+ *$/ && $9 ~ /^ *queued *$/ {n++} END{print n+0}' corpus/SOURCES.md
F=27              grep -cE '^\| F[0-9]+ \|' corpus/README.md
admitted=27       awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
ratio=(20+27)/(20+27+0)=1.000
```
SOURCES status counts over the 72 rows: `mined=57 rejected=15 other=0`. The nine r39 queued rows (S016/S017/S019/S020/S021/S023/S025 mined; S022/S024 rejected) were decided at round 40 (`SCORECARD.md:1596`). So the `## Distance-to-next-score` 7→8 criterion is met and the expression stays at 1.000 after F28 (+1 admitted row, `queued` still 0). The draft's coverage limb therefore names an 8→9 criterion as the next limb and records that none is stated in `SCORECARD.md`; it does not claim a coverage-ratio move from C2.

### F7 — Frontier count and secondary counters (HOLDS as printed; one unreconciled number)
- `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 27 at both trees; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 72 at both; `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → 64 at both.
- `r44-frontier-count.py --root <tree> --expect 28` → `frontier expected=28 admitted=27 verdict=SHORT exit=1` at both trees.
- `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` → empty at both trees (no F28 before the entry lands).
- `frontier-recheck-count.py` → `entries=30 pass=30 exit=0` at both trees. The counter prints 30 entries against 27 frontier rows; I did not reconcile that 3-row difference (it is the counter's own count; not verified here).

### F8 — Remaining C1 controls are not reproduced by this seat (LIMITATION)
I reproduced the do-nothing (C1, C2) and marker-only (C1) controls. Not reproduced: C1 `gutted-entry` (recorded 6/7), `fabricated-anchors` (0/7), `single-anchor-file` (0/7); C2 `junk-row` (4/7), `fabricated-quote` (4/7), `uncited-filler` (5/7). Their recorded values are quoted from `controls/freeze-controls.txt` only.

### F9 — Capability row: no demonstration exists (HOLDS as a null result)
`find <base> <freeze> -name '*landing-gate*'` → nothing in either tree; `find <lane working tree> -name '*landing-gate*'` → nothing. The `r46-landing-gate.py` row is therefore drafted as `proposed` with no capability claimed.

### F10 — Score-5 threshold text differs between the scorecard and an instrument fixture (OBSERVATION)
`SCORECARD.md:331` reads "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims." The live reporter `corpus/instruments/score-gap.py` regex (`THRESHOLD_RE`, line 76) matches that wording; its fixture "b" (around line 388) uses "all source chains passing a non-author audit with 0 unsupported current claims". The fixture is a test input; no score is computed from it. Noted for the L1's Distance section only; the draft quotes `SCORECARD.md:331`.

## Limitations

- Tip values are not measured: no lane commit beyond freeze is inspected. Every tip value is `[[FILL-BY-L1]]`.
- No non-author 25/25 source-chain audit exists in the record; the score-5 limb is stated as not run.
- The C1 re-grounds and the F28 entry are not drafted by this seat (those are other seats' items); the scoreboard quotes only the freeze-tree and base-tree counter outputs.
- The `score-gap.py` and `recheck-audit.py` runs are read-only; no tree was mutated except the scratch marker-only copy.
- `density.py` was not run; the depth:density line is held and marked for L1.
- No tool installed or updated; pacman not invoked.
