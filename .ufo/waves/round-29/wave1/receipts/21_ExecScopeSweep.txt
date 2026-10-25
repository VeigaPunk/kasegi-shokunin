# ExecScopeSweep — round-29 wave1 misroot sweep receipt

- Seat: ExecScopeSweep-2 (leaf executor, no subagents, no labrat needed)
- Date: 2026-10-25 | Fleet root: /home/vgpnk/Projects/shokunin (read-only for this seat)
- Lane repo (only write scope): /home/vgpnk/Projects/shokunin/kasegi-shokunin
- Lane base revision: 7a6591c1eb8a14f427297980a96fa8bb339f29ee; claims-freeze f28ff5d26b29270f93163117e7255e24f0b1d947
- Answering model actually used for this seat's run: inception/mercury-3 (per session config; no model passed by me — the item is a filesystem sweep, facts are model-independent)

## 1. Fleet root sweep — method and results

Sweep rule: any untracked file a round-29/kasegi seat wrote into the FLEET root
(content names `kasegi`/`round-29`) must be byte-copied to the same relative path
under the lane repo, verified with `cmp`, then deleted from the fleet root.

### 1a. Non-ignored untracked files (the only candidate class)
`git -C /home/vgpnk/Projects/shokunin status --porcelain -uall` → **zero `??` entries**.

Full output (6 lines, all `M` = modified TRACKED files in protected areas, none ours):
```
 M .scratch/goal-20261025-hyaku-run7.md
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/watchdog.log
```
These are the explicitly protected paths (`.scratch/`, `.ufo/state/*`, `.ufo/watchdog.log`) — untouched by this seat.

### 1b. Ignored+untracked files (defense-in-depth)
`git ls-files --others -i --exclude-standard` (29,294 entries) was filtered to
non-lane, non-`.jj` paths, then (a) path-grepped for `round-29|wave1|kasegi`
and (b) content-grepped for `kasegi|round-29`:

- Path matches: only `kasegi-shokunin/` (the lane repo itself — outside fleet-root scope).
- Content matches: 9 files, ALL predating round-29 wave1 (mtimes 2026-10-13…2026-10-24):
  - `.tower/comms/{findings,inbox,missions,state.json}` — r18/r100 tower state of another runtime (2026-10-15 / 2026-10-24), includes r100 assimilation-census (pre-round, 2026-10-24).
  - `.tower/quarantine/kaika-fleetroot-20261019/` — archived 2026-10-19 quarantine, not round-29.
  - `.ufo/waves/shokunin-train-20261101-w10/xsentinel-scratch/audio-5415115-swept-files.txt` — old train census artifact (mtime 2026-10-14).
- Freshness check: `git ls-files --others -i --exclude-standard` intersected with
  mtime ≥ 2026-10-25 00:00 UTC → **zero files** (every ignored/untracked file outside
  lanes and `.jj/` has mtime ≤ 2026-10-24 19:00).
- Top-level mtime scan (`find -newermt 2026-10-25`, excluding lanes/protected):
  only tracked docs (SCORECARD.md, m-rev-vs-rev.py, .ufo/l0-questions.md, LOG.md,
  MANIFEST.json) — all tracked, none untracked, none with kasegi/round-29 content
  beyond their pre-existing tracked text.

### 1c. Verdict
**Strays found: 0.** Nothing was copied, nothing was `cmp`-verified against a copied
pair (no copy existed to verify), and no fleet-root deletion was made (the zero
allowed deletions available were unused). No byte-level operations were required.

## 2. Lane repo status verification

`git -C …/kasegi-shokunin status --porcelain -uall` → only `??` (untracked) entries,
no `M`/`A`/`D`, no staged changes; `git diff --stat` → empty.

Untracked set (all within wave scope):
```
?? .ufo/waves/round-29/assimilation/{collisions,quarantine-slice,reg-ids,staged-ids}
?? .ufo/waves/round-29/wave1-run.err
?? .ufo/waves/round-29/wave1.ready
?? .ufo/waves/round-29/wave1.ready.dispatched
?? .ufo/waves/round-29/wave1/{README.md,cwe.json,swarm-registry.json}
?? .ufo/waves/round-29/wave1/ExecCapS045.md
?? .ufo/waves/round-29/wave1/assimilation/{collisions,quarantine-slice,reg-ids,staged-ids}
?? corpus/source-snapshots/round-29/{S044.txt,S045.txt}
```
Every path is under `.ufo/waves/round-29/` or `corpus/source-snapshots/round-29/`
— the wave's intended change area. No tracked file was modified, no existing file
deleted, nothing written outside the round-29 scope. No conflicts with claims.json
(C1/C2 frozen files not touched — they are tracked and unmodified).

## 3. Bounds compliance
- Writes by this seat: only this receipt (`.ufo/waves/round-29/wave1/ExecScopeSweep.md`) inside the lane repo.
- Fleet root, sibling lanes, lane jj state / git index, shokuknow, templates/, scripts/hyaku/, .ufo/state/, .ufo/watchdog.log, MANIFEST.json: untouched.
- No git commits/fixtures created (not needed; no copy/delete operations occurred).
- No counter runs; PRE-STATE rule not applicable (no comparisons performed).
- No peer messaging needed (no owner conflicts found; scoped findings are self-contained).
- Tooling: no installs performed (no tool needed beyond git/coreutils already present) — nothing to record under the operator channel rule.

## 4. Risks / observations
- The only kasegi/round-29-naming files in the fleet root outside lanes are pre-existing
  tracked docs and another runtime's (`.tower`) / older-train state — none are wave-1
  strays; flagged for visibility only.
- .ufo/waves/round-29/wave1/{wave1-run.err,wave1.ready,wave1.ready.dispatched} are
  harness lifecycle files in the lane, not strays; left as-is.
- If a future wave writes stray files, they would surface as `??` in fleet `git status`
  (checked at scan time: none).
