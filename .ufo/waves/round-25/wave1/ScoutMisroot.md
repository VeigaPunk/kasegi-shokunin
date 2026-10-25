# ScoutMisroot — fleet-root misroot sweep, kasegi round 25 (wave 1)

Seat: `L1Kasegi25.ScoutMisroot` (read-only). Lane base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.
Question: which untracked/modified files at the fleet root, if any, were written by this round's seats.
Nothing was deleted, moved, or edited outside this file.

## a) Status output (verbatim)

`git -C /home/vgpnk/Projects/shokunin status --porcelain`

```
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 M scripts/hyaku/hyaku.env
 M scripts/hyaku/lane-addendum.md
?? .omp/mcp.json
?? .scratch/goal-20261025-hyaku-12h.md
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
```

22 entries, unchanged by `-uall` (no untracked directory collapses to hide a seat file).

Context that bounds the sweep: `*-shokunin/` is gitignored at the fleet root
(`git check-ignore -v kasegi-shokunin` → `.gitignore:1:*-shokunin/`), so no lane repo's files can appear
in this status. Lane-side untracked bytes are in-lane, not fleet-root misroots:
`git -C kasegi-shokunin status --porcelain` → `?? .ufo/waves/round-25/`, `?? corpus/instruments/recheck-audit.py`,
`?? corpus/source-snapshots/round-25/` — all under the lane, correctly placed.

## b) Disposition table

| path | author lane or driver | evidence (quoted) | action for the L1 |
|---|---|---|---|
| `.ufo/state/{chousa,kagi,kaidoku,kake,kama,kasegi,kengaku,kumitate,mado,mori,souji,tabi,tameshi,tsukuroi}.report-baseline` (14 modified) | driver — `scripts/shokunin-watchdog.sh` | script header: `#   .ufo/state/<lane>.report-baseline holds "round SHA256" for the report bytes` (`shokunin-watchdog.sh:31`; writer at `:122`). The kasegi one moved `23 e3b0c442…` → `25 e3b0c442…`, i.e. the round counter bumped 23→25, not a report hash change. | leave (driver state, never touch) |
| `.ufo/state/{kotoba,kotodama,revenger}.report-baseline` (3 new) | driver — same writer | `68 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (kotoba), `69 …` (kotodama), `68 …` (revenger): `"round SHA256"` format, empty-report digest, created 22:45 / 03:23 while the driver was arming run 6. | leave (driver state, never touch) |
| `.ufo/watchdog.log` (modified, +679 lines) | driver — `shokunin-watchdog.sh` | added lines are launch/complete records only: `2026-10-21T12:04:00-03:00 launch kagi round=27 pgid=571820 driver=hyaku-inline attempt=1`. Names no lane's seat artefact and no file. | leave (driver state, never touch) |
| `scripts/hyaku/hyaku.env` (modified) | driver — run-6 prep by the L1/orchestrator (not a seat) | `# operator directive 2026-10-25 (12h run): "all subagents run on m_flash" — every` / `L1_MODEL=@m_flash` replacing `L1_MODEL=@m_swe`; mtime `2026-10-25 03:22:37`, before the kasegi r25 dispatch commit `23629d98 2026-10-25 05:06:19 -0300`. | leave (fleet script, out of lane write scope) |
| `scripts/hyaku/lane-addendum.md` (modified) | driver — run-6 addendum by the L1/orchestrator | `## 6. Campaign addendum — hyaku (百) phases 3–6, operator directives of 2026-10-22/23/25 (binding this round; in-session)`; the diff is the run-5→run-6 rewrite plus the `.scratch/` never-a-misroot ruling. mtime `04:16:14`, pre-dispatch. | leave (fleet script, out of lane write scope) |
| `.omp/mcp.json` (untracked) | operator/harness (omp host config) | `"$schema": "https://raw.githubusercontent.com/can1357/oh-my-pi/main/packages/coding-agent/src/config/mcp-schema.json"` — one `rea` server, `"enabled": false`. mtime `2026-10-24 18:07:20`, a full day before run 6 armed (03:22) and before the r25 dispatch (05:06); names no lane and no round. Prior lanes reached the same verdict: kotoba r67 "`.omp/mcp.json` untracked at the fleet root (operator-owned, untouched)", kama r34 "`.omp/mcp.json`). Their contents name no kama lane and no round 34". | leave (operator state, never touch) |
| `.scratch/goal-20261025-hyaku-12h.md` (untracked) | driver/orchestrator run state | `<!-- ORCHESTRATOR-OWNED run state (hyaku run 6). Not a misroot: lanes and seats never move, copy-then-delete, or edit this file. -->` | leave — **never a misroot** (see c) |

No entry names kasegi round 25, or any other lane's round, as its author. **Zero fleet-root misroots this
round: nothing to copy back, nothing to delete.**

## c) `.scratch/` — explicitly never a misroot

`.scratch/goal-20261025-hyaku-12h.md` is the only `.scratch/` entry in the status. It is **never a misroot**
and must not be copied or deleted:

- It self-identifies: `<!-- ORCHESTRATOR-OWNED run state (hyaku run 6). Not a misroot: lanes and seats never
  move, copy-then-delete, or edit this file. -->`.
- The binding rule is in the driver addendum: `never touch {{FLEET_ROOT}}/.scratch/ — orchestrator-owned run
  state that names many lanes and rounds by design; it is never a misroot (incident 2026-10-25: the tracked
  tree was deleted mid-run).` (`scripts/hyaku/lane-addendum.md:133-135`).
- It does contain a kasegi string — `Steady state 5 L1s max + closures (6 L1s starved W2s: kasegi r24 W2
  refused 4x)` (line 38) — that is a fleet-wide concurrency note naming several lanes, exactly the
  "names many lanes by design" case, not a seat artefact. Its mtime `05:23:08` is also *after* the r25
  dispatch (`05:06:19`), i.e. it was written by the orchestrator while the lane was already running.

Rest of `.scratch/` (13 tracked files: `goal-20261018-game-dev-2d-training.md`, `goal-20261022-hyaku-12h.md`,
`goal-20261023-hyaku-24h.md`, `*.out`, …) is tracked and clean; `.scratch/` is not in `.gitignore`
(`git check-ignore` returns nothing for it), so it shows only by content change, never as a seat dump target.

## Method and limits

- Commands run: `git status --porcelain`, `git status --porcelain -uall`, `git check-ignore -v`,
  `git ls-files`, `git diff -- <path>`, `git show -s --format='%H %ci %s' 23629d98`,
  `git log --oneline -5`, `stat -c '%y %n'`, `sed -n '1,10p'` per non-driver path,
  `grep -rn "report-baseline" scripts/`, `grep -rn "\.omp/mcp\.json" .ufo/reports/ .ufo/waves/`.
- Read-only throughout; no VCS write, no pacman/uv/npx install (nothing needed).
- Limit: authorship is inferred from content, mtime and the writer script, not from a per-file write audit —
  the fleet root has no such log for untracked files. Confidence: driver/operator classification **high**
  (writer script or self-declared header for every row); "no seat wrote here" **high** (every entry is
  accounted for by a driver writer or an operator file, and none names kasegi/round 25).
