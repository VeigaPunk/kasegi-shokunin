# ExecScopeSweep — round-28 write-scope sweep

Seat: `ExecScopeSweep` (leaf, round 28 wave 1). Item: sweep the write scope after the
wave's edits land, best effort at run time, labelling what was checked.

- Snapshot wall clock: **2026-10-25T17:28:53Z** (further values below are from that run).
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD
  `94f387cbee71a532a51ce075f01701a557231e85` (dispatch commit).
- Base revision `c9f8b115a098c65356e4b3b6048af45a37ab8395` (claims freeze) verified as an
  **ancestor** of HEAD (`git merge-base --is-ancestor` → yes).
- Wave start used for every "since the wave" predicate: the freeze commit instant
  **2026-10-25T17:01:25Z**, derived with
  `date -u -d "$(git log -1 --format=%cI c9f8b115…)"` rather than hard-coded.
- **The wave was still in flight at snapshot time**: 22 seat receipts, 33 seat reports,
  238 wave-evidence paths, and `corpus/lessons/round-28.md` had not landed. This sweep
  certifies the working tree at 17:28:53Z, not a closed wave. Re-run line at the end.

## Instrument (read-only)

`.ufo/waves/round-28/wave1/ExecScopeSweep/scope-check.sh`
sha256 `0f30d2c86ea2b460162f99eaa8fbf88f0cb95f42bbbad816bf701dd88085cc00`.

Limbs: 1 fleet misroot (untracked) · 1b fleet modified tracked · 1c fleet ignored
surface · 2 lane status → ownership map · 2b lane ignored surface · 3 shokuknow delta.
It runs only `git status`/`log`/`merge-base`/`check-ignore`, `find`, `grep`, `awk`,
`sha256sum` — no writes, no VCS mutation, no network.

The classifier is self-proved, because a scope checker that cannot fail proves nothing:
`bash scope-check.sh --selftest` → `selftest cases=13 failures=0`, including five
off-map cases (`corpus/knowledge/rogue-r28.md`, `corpus/lessons/round-27.md`,
`templates/foo.md`, `.ufo/state/kasegi.r28.json`, `corpus/instruments/resolve.py`) that
must classify `VIOLATION`, plus a rename line that must resolve to the new path.

## Verbatim counters, 17:28:53Z

```
lane_prod_paths=12 lane_wave_paths=238 lane_violations=0
fleet_untracked_scanned=0 fleet_misroot=0
fleet_ignored_roots=15 fleet_ignored_files_scanned=0 fleet_ignored_misroot=0
shokuknow_head=8b94c5c12c0521e4cd9ed8e5b6939afd8518c715
shokuknow_status_paths=5217   (repo-wide: pre-existing staging dirt, all lanes)
shokuknow_merge_kasegi_status_paths=19
shokuknow_merge_kasegi_files_newer_than_wave=0 (max_mtime=2026-10-24T23:33:20.0436186320)
shokuknow_files_newer_than_wave_naming_kasegi=0
shokuknow_files_newer_than_wave_total=0
shokuknow_status_paths_touched_since_wave_start=0
shokuknow_kasegi_scoped_files_newer_than_wave=0
scope_check_exit=0
```

Raw output kept at `.ufo/waves/round-28/wave1/ExecScopeSweep/sweep-final2.txt`
(17636 bytes, sha256 `5a19abaf9149d7e73c6233cc43a40cca4790d5872af2f0a96063def086f10f9b`);
the two earlier exploratory dumps were deleted rather than committed (R14 economy).

Re-run after this seat's own writes at **17:30:05Z**: `lane_prod_paths=12
lane_wave_paths=261 lane_violations=0`, `fleet_misroot=0`,
`shokuknow_kasegi_scoped_files_newer_than_wave=0`, `scope_check_exit=0` — unchanged.

## Limb 2 — lane ownership map: 12 production paths, 0 violations

Every changed path in the lane repo is either an unmapped-to-a-seat wave-evidence path
under `.ufo/waves/round-28/` or exactly one of the 13 map paths. Twelve had landed:

| path | status | map owner | owner evidence present at snapshot |
|---|---|---|---|
| `corpus/instruments/anchorcheck.py` | M (+259/−19) | ExecImplC1 | `wave1/ExecImplC1/` scratch; receipt landing |
| `corpus/instruments/README.md` | M (+93/−0) | ExecInstrReadme | `receipts/ExecInstrReadme.txt` |
| `SKILL.md` | M (+3/−0) | ScribeSkillGate | `wave1/ScribeSkillGate/` (7 files), receipt absent |
| `corpus/source-snapshots/round-28/S041.txt` | ?? 147267 B | ExecCaptureS041 | `receipts/ExecCaptureS041.txt` |
| `corpus/source-snapshots/round-28/S042.txt` | ?? 60508 B | ExecCaptureS042 | `receipts/ExecCaptureS042.txt` |
| `corpus/source-snapshots/round-28/manifest.json` | ?? 5038 B | ExecManifest | `receipts/ExecManifest.txt` |
| `corpus/knowledge/japanese-domestic-disclosure-workflow.md` | ?? 18452 B | ScribeEntryC2 | `receipts/ScribeEntryC2.txt` |
| `corpus/SOURCES.md` | M (+4/−1) | ScribeRegistryC2 | `receipts/ScribeRegistryC2.txt` |
| `corpus/README.md` | M (+28/−0) | ScribeReadmeC2 | `receipts/ScribeReadmeC2.txt` |
| `corpus/QUALITY.md` | M (+6/−0) | ScribeR14 | `receipts/ScribeR14.txt` |
| `LOG.md` | M (+49/−0) | ScribeLog | `receipts/ScribeLog.txt` |
| `SCORECARD.md` | M (+74/−0) | ScribeScorecard | `receipts/ScribeScorecard.txt` |
| `corpus/lessons/round-28.md` | **absent** | ScribeLesson | not landed |

No duplicate-writer evidence: each landed path's write claim is made only by its map
owner (`ScribeR14.md:47`, `receipts/ScribeRegistryC2.txt:6`, `receipts/ScribeReadmeC2.txt:9`,
`ScribeLog.md:5`, `receipts/ScribeScorecard.txt:8`, capture receipts' `out=` fields).
Other seats reference these paths as inputs — e.g. `ScribeScorecard.md:31-32` verifies
`corpus/README.md`/`corpus/SOURCES.md` and `ScribeCensusNote.md:111` records a
*pre-landing* observation of `corpus/SOURCES.md` — which is reading, not writing.

Structural facts that are inside this seat's remit because the map states them:

- Deletions are confined to `corpus/SOURCES.md` (−1). The diff shows the single deleted
  line is the **S041 row's `used-by` cell rewrite (old→new)**, with the `S042` row and two
  changelog lines added beneath it — i.e. exactly the C2 registry obligation, performed by
  the mapped owner. No unassigned row was touched.
- `LOG.md` (+49/−0) and `SCORECARD.md` (+74/−0) are pure appends at EOF (single hunk each).
- `corpus/QUALITY.md` (+6/−0) is a pure append at EOF.

## Limb 1 — fleet root: no misroot

`git -C /home/vgpnk/Projects/shokunin status --porcelain -uall`: **0 untracked paths**,
so there is nothing whose content could be a misrooted kasegi artifact to copy back.
The 15 ignored roots in the fleet repo (`.tower/`, pre-round `*/xconnector-scratch`,
`*/xsentinel-scratch`) contain **0 files newer than the freeze**. Modified tracked paths
are 5 and all sit in the excluded control plane: `.ufo/state/{kasegi,kengaku,souji,tabi}.report-baseline`
and `.ufo/watchdog.log`. `.scratch/goal-20261025-hyaku-run7.md` was transiently modified
when first observed (17:22:18Z) and is byte-identical to HEAD again at 17:28:41Z
(`git diff` empty); it is excluded either way.

`MISROOT` action taken: none needed — nothing to copy, nothing to delete. Recorded that
way rather than as "verified clean by inspection".

## Limb 3 — shokuknow: no kasegi-scoped write, but the "status empty" premise is false

The check as briefed was `git status --porcelain` empty. It is **not** empty and cannot be:
`8b94c5c` is a multi-lane staging repo with **5217** uncommitted paths across ~22 lanes
(3788 untracked, 1405 modified, 24 deleted) that predate this wave. What is measurable and
does hold:

- `merge/kasegi` has 19 status paths (3 modified: `MERGE-REPORT.json`, `MERGE-REPORT.md`,
  `SOURCES.append.md`; 16 untracked knowledge files) with **max mtime
  `2026-10-24T23:33:20-03:00` = 2026-10-25T02:33Z** — 14.5 h before the freeze commit.
- **0 files anywhere in shokuknow are newer than 2026-10-25T17:01:25Z**, and
  `shokuknow_status_paths_touched_since_wave_start=0`, so no status path was rewritten
  during the wave either.
- 0 of those recent-by-freeze files name kasegi; the kasegi-scoped delta is 0.

Verdict: no round-28 seat wrote under shokuknow; the read-only substrate held. The
"status empty" form of the check should be restated as a **delta-since-freeze** check,
which is what the checker now measures — a repo-wide-empty assertion is unsatisfiable here
and would have produced a false red on every wave.

## Advisories (no scope violation; L1 decision)

**A1 — `SKILL.md` was not appended strictly at EOF.** The brief says "append at end per R6;
never shift lines". The landed diff is 3 insertions, 0 deletions, in **two** hunks:
`@@ -981,0 +982 @@` inserts the `anchorcheck.py` row into the instrument table (mid-file)
and `@@ -1032,0 +1034,2 @@` appends two lines at EOF. Measured consequence of the mid-file
row: any `SKILL.md:<line>` anchor at line ≥ 982 shifts by +1.
- Live anchors (outside `.ufo/`) affected: **0** — the highest live anchor is `SKILL.md:977`
  (`3` at `:683`, `3` at `:821`, `1` at `:977`).
- Historical anchors affected: **52**, all inside frozen wave evidence
  (`.ufo/waves/round-23/falsify/`, `round-24/wave1/`, `round-25/wave1/` incl. its fixture
  copies) citing lines 993/1000/1014/1019/1021. Those are records, not live citations, and
  must not be renumbered.
So the deviation is real but currently harmless; the table row is where a reader looks for
it. Either accept it in place or ask ScribeSkillGate to move it to EOF — the seat's call, not
this seat's.

**A2 — ScoutAssimilation scratch aliases a production directory.** Three absolute symlinks
exist under `.ufo/waves/round-28/assimilation/`:
`schema2/corpus/knowledge`, `schema3/corpus/knowledge`, `schema4/corpus/knowledge` →
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge`. They were read paths for
schema fixtures (a legitimate R14 economy move versus copying the corpus), and **no write
went through them**: `find corpus/knowledge -newermt <freeze>` returns nothing.
Residual risk: a later write addressed through a scratch path would mutate production while
looking like scratch evidence. Recommend removing the three links before the wave closes,
or recording in the round lesson that they are read-only.

**A3 — the last map path has not landed.** `corpus/lessons/round-28.md` (ScribeLesson) is
absent, so the map's 13th production path is uncovered by this snapshot. Re-run required.

**A4 — protected files untouched.** `git diff --name-only HEAD` and `git status` over
`.ufo/waves/round-27/`, `.ufo/waves/round-26/`, `corpus/lessons/round-27.md` and
`.ufo/waves/round-28/claims.json` are empty; mtimes are pre-freeze
(`claims.json` 2026-10-25T16:58:45Z, `lessons/round-27.md` 2026-10-25T14:34Z). No seat
edited the frozen claims, a prior-round lesson, or a prior-round receipt.

## Bounds — what this sweep did not do

- **Sibling lane repos were not status-audited.** 21 sibling `*-shokunin` repos exist; 4
  were active since the freeze (kengaku 75 files, souji 49, tabi 37, chousa 6). An 8-file
  content scan found "kasegi" only as a sibling reference inside those lanes' own files
  (e.g. `kengaku-shokunin/.ufo/waves/round-33/build-spec.json:167` roster prompt,
  `tabi-shokunin/SKILL.md`), never a kasegi production path or byte copy. No per-lane status
  audit — out of this seat's remit and owned by each lane.
- No content or verdict verification of the landed production edits (C1/C2 counters,
  manifest Q9 assertions, registry row shape) — other seats' claims.
- Nothing landing after 17:28:53Z. The wave was still in flight.

## Re-run (exact, any cwd)

```
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/wave1/ExecScopeSweep/scope-check.sh
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/wave1/ExecScopeSweep/scope-check.sh --selftest
```

Expected after the wave closes: `--selftest` → `selftest cases=13 failures=0`;
sweep → `lane_violations=0`, `fleet_misroot=0`, `fleet_ignored_misroot=0`,
`shokuknow_kasegi_scoped_files_newer_than_wave=0`, `scope_check_exit=0`,
and `lane_prod_paths` = 13 once `corpus/lessons/round-28.md` lands. Any `VIOLATION` line
names the path and its unowned status; any `MISROOT` line names a fleet-root file whose
content references this lane.
