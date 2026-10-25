# ExecScopeSweep — kasegi-r30-build (round 30, wave 1, hyaku run 7)

Seat: `ExecScopeSweep` (L2 leaf executor, no subagent/labrat used).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope).
Wave start (cutoff): `2026-10-25T18:47:48Z` — `kasegi-r30-build.ready.dispatched`
(content `2026-10-25T15:47:48`, mtime `15:47:48.540 -0300` = `18:47:48Z`).
Final scans at `2026-10-25T18:52:32Z`. All mtimes below are local `-0300`.

## Verdict

**Clean sweep.** No out-of-bounds write attributable to any kasegi round-30 seat
was found. Every lane write lands inside the sanctioned areas (`.ufo/waves/round-30/`,
`corpus/` production files, `SKILL.md` append, no `SCORECARD.md`/`LOG.md` change yet).
Zero files were written into `/home/vgpnk/Projects/shokuknow` since cutoff (checked twice).
No sibling-lane file modified since cutoff contains both `kasegi` **and** `round-30` in a
way attributable to this wave; the apparent token co-occurrences are other lanes' own
dispatch/prompt artifacts and are listed as observations below so the L1 can judge.

## 1. Lane writes since cutoff (all sanctioned)

`find <lane> -type f -newermt '2026-10-25 18:47:48+00:00' ! -path '*/.git/*' ! -path '*/.jj/*'`
→ 152 files, all under:

- `.ufo/waves/round-30/` — wave artifacts: wave1 seat reports
  (`Scout*`, `Exec*`, `Scribe*`, `Rev*`, `Crit*`), `CritC2Kill-lab/` fixture copies,
  `CritC1Kill-attack/`, `ExecImplSourceRecheck-b2/`, `fetch/` (s037/s048/s054/s065
  re-fetch probes), `c1-controls/` (mutants, before-run-2.txt, digest-poll.log),
  `assimilation/` (quarantine-slice, reg-ids, staged-ids, collisions, guard/),
  `post-commit-recheck.sh`, `kasegi-r30-build.ready(.dispatched)`, `plan/run.*`.
- `corpus/source-snapshots/round-30/` — S041.txt (147,267 B), S046.txt (23,039 B),
  S047.txt (72,866 B), manifest.json (3,523 B).
- `corpus/instruments/` — `frontier-recheck-count.py` (9,418 B), `source-recheck.py`
  (16,711 B), `__pycache__/` (python bytecode, local runs).
- `corpus/README.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/considerthese-proposals-ledger.md` (proposal-4 landing, per claims.json
  frontier_step.considerthese), `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`
  (F14 entry), `SKILL.md` (88,708 B, append).

No writes to `SCORECARD.md`, `LOG.md`, `MANIFEST.json`, or a lane `.ufo/state`
(does not exist). Lane `considerthese/2026-10-25.md` untouched (read-only per spec).
No path outside the sanctioned set was modified or created.

VCS note: `<lane>/.git/index` mtime refreshed at `15:48:33 -0300`. Read-only
`git status --porcelain` / `git diff --cached --stat` show nothing staged (empty cached
diff) → consistent with an index stat-refresh (e.g. status), not a content write; no
HEAD/mutation observed. Not counted as an OOB write.

Measured byte labels (sha256, at scan time):
- `corpus/instruments/frontier-recheck-count.py` = `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` (9,418 B at 15:50:40; earlier 9,357-B draft at 15:50:24 was superseded)
- `corpus/instruments/source-recheck.py` = `0b841d5ddb80f96f0e802eec1e67a0b9ba0606609282d8991759db72ac71a243` (13,529 B at 15:50:24) → final 16,711 B at 15:51:26 (sha recomputed by impl seat; not re-hashed here)
- `corpus/source-snapshots/round-30/S041.txt` = `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`
- `corpus/source-snapshots/round-30/S046.txt` = `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3`
- `corpus/source-snapshots/round-30/S047.txt` = `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4`
- `.ufo/waves/round-30/claims.json` = `68d77757c71f1779be89ac97efe3f1299a5858187c7f95e06d9da4e52cae523b` (frozen, unedited)
- `c1-controls/before-run-2.txt` = `cf53d77dd8f9b6c55cfd2da8ffdbe54547acfd74c3d0af33b310349e9a0d1b06`
- `c1-controls/mutants/digest-poll.log` = `4e7877271f320f444ae87bfdb1095038efb1c8d71eb6fed6c3ec7cb3fb6addb6`

## 2. Fleet-root OOB scan (excluding lane, VCS, tower, orchestrator-owned)

Scan: `find /home/vgpnk/Projects/shokunin -type f -newermt '2026-10-25 18:47:48+00:00'`
excluding `*/kasegi-shokunin/*`, `*/.git/*`, `*/.jj/*`, `*/.tower/*`, `*/.ufo/state/*`,
`*/.scratch/*`, `*/.ufo/reports/*`, `*/.ufo/prompts/*`, `watchdog.log`.

Files modified since cutoff exist only in sibling lanes running their own waves
(kengaku round-34, souji round-28, tabi round-27 spotcheck) plus one fleet-root
protected file (below). Content greps (`kasegi`, `round-30`, combined regex
`(?s)kasegi.{0,4000}round-30|(?s)round-30.{0,4000}kasegi`):

- **No file outside the lane modified since cutoff contains both tokens in a
  kasegi-wave context.** The only both-token co-occurrences are kengaku's own artifacts.
- `MANIFEST.json` (fleet root, protected) — mtime `15:52:01 -0300` (`18:52:01Z`),
  1,854,685 B. Content names `kasegi` (roster/ledger) and round-30 records
  (e.g. `.ufo/reports/round-30/*` closures). Seats are forbidden to write it →
  presumed orchestrator/hyaku-runner bookkeeping during the wave; **L1 should confirm no
  seat touched it** (SentScope will re-check).
- kengaku `build-dispatch.json` / `build-plan.txt` / `build-spec.json` (round-34 root,
  NOT modified since cutoff — predate wave) contain `kasegi` only as a sibling-scan target
  name in R34 prompt text; their `round-30` mentions are kengaku's own lesson references.
- kengaku `.ufo/waves/round-34/build/R34SentWriteScope.md` (mtime `15:49:34 -0300`)
  mentions `kasegi` only inside a list of `.ufo/state/*.report-baseline` files
  (orchestrator-owned state); no `round-30`.
- souji `.ufo/waves/round-28/w1/SwarmCritic46.md` (mtime `15:47:50 -0300`) mentions
  `kasegi` only in the same `.ufo/state` baseline list; no `round-30`. `SwarmScout58.md`
  / `SwarmSentinel62.md` state zero kasegi tokens in souji's own scan (predate cutoff).
- tabi `corpus/lessons/round-27-verifier-spotcheck.md` modified `15:51:37 -0300` —
  no `kasegi` content (verified).
- chousa `.ufo/waves/round-33/w2/ReviewD1Repair/keep-s9001/root/` files carry **future
  mtimes** (2026-11-09 … 2026-12-29) and thus satisfy `-newermt`; content has no
  `kasegi`/`round-30` tokens. Pre-existing mtime anomaly, not a wave write.

`/home/vgpnk/Projects/shokuknow`: `find -type f -newermt <cutoff>` → **0 files**
(two independent passes at 18:50Z and 18:52Z).

## 3. Observation — kengaku `mut-entries-scratch/` explosion (sibling hygiene)

`kengaku-shokunin/.ufo/waves/round-34/mut-entries-scratch/` contains **418,907 files**
with path depth up to **226 components** (recursive copies of R34/R30 build artifacts).
6,326 of them have mtimes ≥ cutoff. This is inside kengaku's own lane (not a kasegi-wave
write) but is a significant fleet-hygiene/R14-bloat flag worth routing to kengaku/L1.
Example: `.ufo/waves/round-34/mut-entries-scratch/.ufo/waves/round-30/build-dispatch.json`
(first line `{`, benign `"schema": "ufo-swarm-wave-dispatch-v1"`), copies carry the
sibling-scan prompt text containing `kasegi`.

## 4. Tooling

No tool installed by this seat (no pacman/uv/cargo/npm action). No live network calls;
no target contacted.

## 5. Method/limits

- Wave-start cutoff pinned from the dispatched marker file mtime + content; scans use
  `-newermt '2026-10-25 18:47:48+00:00'` (UTC-explicit) to avoid TZ drift.
- The sweep is a snapshot taken during a live wave (seats still writing at scan time);
  SentScope runs the periodic post-wave sweep. Post-integration writes by the L1
  (commit/push, MANIFEST update) are expected and are not OOB.
- No file was deleted or edited; this report is the only write made by this seat.
