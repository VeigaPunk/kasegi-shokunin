# SentinelMisroot — fleet-root misroot watch (kasegi round 42, wave 1)

Seat: SentinelMisroot (leaf, receipt-only). Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Watch window: **2026-10-28T11:01:52Z → 2026-10-28T11:47:50Z** (45.97 min, 1-minute resolution), final poll 11:48:23Z.
Fleet repo at baseline: `c5f6ce9d4666575f03ff8b9f395fff2b12fe69d0`; at final poll: `fca0f3f0ea81a9a28041ce76d50a761602ea093f` (one non-kasegi lane commit landed mid-window, audited below).

**Verdict: no kasegi-seat misroot. Zero new fleet-root paths attributable to any kasegi round-42 seat** across the whole window; final `git status` is byte-identical to the baseline (4 pre-existing entries, none kasegi). One transient non-kasegi fleet report appeared and was committed by its own lane (detail §3).

## 1. Method

Baseline and every poll: `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all`.
Continuous watcher (`S=/fast/scratch/hyaku/kasegi-r42/SentinelMisroot/watch.sh`, pid 904569) polled every 60 s for 2700 s and logged every status change plus a 10-minute heartbeat; it wrote `=== WATCH-END 2026-10-28T11:47:50Z` and exited. Manual checkpoints at 11:12:36Z, 11:22:08Z, 11:32:05Z, 11:47:29Z all printed `STATUS_IDENTICAL`. Wave activity under watch: `kasegi-shokunin/.ufo/waves/round-42/wave1/` grew from 8 entries (4 `.md` receipts) at 11:03Z → 46 `.md` at 11:26Z → 55 `.md` at 11:48Z, so seats were landing files throughout the window.

Complete watcher log (all changes, nothing elided):

```
=== CHANGE 2026-10-28T11:02:49Z count=4
 M .ufo/reports/round-58/chousa.md
?? o.bin
?? .scratch/closure-mado-r50.json
?? .scratch/source-routing-queue.md
=== HEARTBEAT 2026-10-28T11:12:49Z count=4 unchanged
=== HEARTBEAT 2026-10-28T11:22:49Z count=4 unchanged
=== HEARTBEAT 2026-10-28T11:32:49Z count=4 unchanged
=== CHANGE 2026-10-28T11:33:49Z count=5
 M .ufo/reports/round-58/chousa.md
?? o.bin
?? .scratch/closure-mado-r50.json
?? .scratch/source-routing-queue.md
?? .ufo/reports/round-35/souji.md
=== CHANGE 2026-10-28T11:34:49Z count=4
 M .ufo/reports/round-58/chousa.md
?? o.bin
?? .scratch/closure-mado-r50.json
?? .scratch/source-routing-queue.md
=== HEARTBEAT 2026-10-28T11:42:50Z count=4 unchanged
=== WATCH-END 2026-10-28T11:47:50Z
```

## 2. Baseline entries (pre-window; none kasegi, all left in place)

| path | kind | size | sha256 | mtime |
|---|---|---|---|---|
| `o.bin` | untracked file | 5867 | `5d670538e975a622f5380465e444002f71c30e5a392570b4fc6abce6d8d23757` | 2026-10-27 16:58:36 -0300 |
| `.scratch/closure-mado-r50.json` | untracked file | 3579 | `dd7024d4de2e79ac58fdb3ec0561e8ec076a73b04717906ba2dbb9c8fa702149` | 2026-10-27 06:38:17 -0300 |
| `.scratch/source-routing-queue.md` | untracked file | 3667 | `8441ee954d5f4af1a0624588f72ea2d65dc5899d1426c7e14a68c9a5c55d7428` | 2026-10-27 22:05:28 -0300 |
| `.ufo/reports/round-58/chousa.md` | tracked, modified | `+10` lines | `git diff --numstat` → `10 0` | 2026-10-27 15:04:52 -0300 |

Attribution evidence:

- `.scratch/closure-mado-r50.json` is mado round-50 driver input (`{"round": 50, ..., "lane": "mado" ...}`); `.scratch/source-routing-queue.md` is the operator routing queue ("Source-routing queue — operator directives 2026-10-27"). Neither is kasegi.
- `.ufo/reports/round-58/chousa.md` carries a chousa round-58 closure addendum (10 new lines: closure-notes digest + "Closure conformance and routing"); uncommitted, other lane's.
- `o.bin` is a Cloudflare challenge page (`file` → `HTML document, ASCII text, ... no line terminators`; `<title>Just a moment...</title>`), i.e. a blocked fetch saved under a bare filename. `grep -c -i kasegi o.bin` = 0; `grep -c 'r42\|round-42' o.bin` = 0. Prior sentinels reached the same conclusion without attribution: `.ufo/reports/round-58/kama.md:15` ("a Cloudflare challenge page written 16:58:36 ... not attributed to any kama seat and I did not delete it; named for the operator") and `.ufo/reports/round-40/tabi.md:70` ("no match; ... untouched"). It has now survived ≥18 h and three sentinel sweeps with no operator disposition. Not deleted (another session's artifact); named here again.

## 3. The only change during the window (non-kasegi, benign)

11:33:49Z `.ufo/reports/round-35/souji.md` appeared untracked; 11:34:49Z it was gone and `HEAD` moved `c5f6ce9d → faa89dcb → fca0f3f0`. The write is the sanctioned fleet report path (`scripts/hyaku/inline.sh:155`: `rep=".ufo/reports/round-$n/$lane.md"`), executed by the souji L1 whose cwd *is* the fleet root, then committed through `fleet-commit.sh`:

```
$ git show --name-status fca0f3f0
A	.ufo/reports/round-35/souji.md
$ git log -1 --format='%H %an <%ae> %s' fca0f3f0
fca0f3f0ea81a9a28041ce76d50a761602ea093f souji-shokunin <souji@shokunin.local> report souji round 35 partial closure
```

The commit added exactly one path — **no pre-existing stray (`o.bin`, `.scratch/*`) was swept in**, which is the empirical check that the pathspec-limited committer holds under a live commit (§4).

## 4. Mechanism: why misroots happen, and what contains them

1. **Every seat starts in the fleet root.** `scripts/hyaku/inline-dispatcher.py:103` (SEAT_GUARD): "Your process cwd is the fleet root {FLEET}: not your lane, not your scratch." The spawn calls pass no cwd: `:205` (`agent(L1_PROMPT..., agent='task')`), `:214`, `:257` (`h = agent(prompt, agent=t['agent'], label=t['name'])`). Any relative write from a seat therefore lands at the fleet root.
2. **The guard is advisory only.** No spawn-time assertion, no sandbox, no PATH/cwd enforcement; `ls .git/hooks | grep -v '\.sample$'` → `none`.
3. **The ignore list does not cover bare strays.** `.gitignore` ignores `*-shokunin/` and `.ufo/waves/*/*-scratch/`, but `git check-ignore -v o.bin` → `NOT-IGNORED`, `git check-ignore -v .scratch` → `NOT-IGNORED` (`.scratch` is a *tracked* directory whose new contents are untracked).
4. **A blanket add would stage them.** `git add -A --dry-run` at the fleet root printed `add '.ufo/reports/round-58/chousa.md'`, `add '.scratch/closure-mado-r50.json'`, `add '.scratch/source-routing-queue.md'`, `add 'o.bin'`. No hook or script in this repo stops that.
5. **History is protected by the sanctioned committer.** `scripts/hyaku/fleet-commit.sh:5` — "pathspec-limited (only the named paths; untracked strays are never tracked)"; `:44-47` reject absolute paths, `..` and driver runtime; `:74` requires the named paths to exist. Empirically confirmed by `fca0f3f0` above. The fleet repo is jj-colocated (`.jj` present) and its `fleet-commit.sh` calls pass `--config 'snapshot.auto-track="none()"'`, but no repo/user `snapshot.auto-track` is configured (`cat .jj/repo/config.toml` → empty; no `snapshot` key in `~/.config/jj/config.toml`), so any *other* `jj` invocation in the fleet root snapshots strays into `@` by default [INFERENCE: jj's unset `snapshot.auto-track` default is `all()`]. They still cannot reach history unless someone commits `@`.
6. **The destructive variant is unmitigated.** `git ls-tree HEAD` shows tracked fleet-root files `LOG.md`, `SCORECARD.md`, `MANIFEST.json`, `PROTOCOL.md`, `MISSION.md`, …. A relative write from cwd = fleet root can truncate them before any commit-level check runs. This has already happened once and is recorded in the dispatcher itself: `scripts/hyaku/inline-dispatcher.py:99-100` — "a kasegi fixture driver wrote relative paths before cd and truncated the fleet root's LOG.md and SCORECARD.md".

## 5. Realized precedent — this is a recurrent class, not a hypothetical

Other lanes' L1s recorded actual fleet-root landings and paid a manual copy-back each time:

- `.ufo/reports/round-19/mado.md:162` — seat output "at the fleet root `.ufo/waves/round-19/`; copied byte-exact into the lane (`cmp` equal)".
- `.ufo/reports/round-26/kaidoku.md:84` — "two round-26 seat files ... (`.ufo/waves/round-26/w2/CustodyNoteReview.md`, `kaidoku-r26/seats/EntryCorrection/final-report.md`)".
- `.ufo/reports/round-51/kotodama.md:21` — `ReopenS113.md` under fleet-root `.ufo/waves/round-51/falsify/`.
- `.ufo/reports/round-71/kotodama.md:81` — "seven fetch artifacts (s795.pdf, s796.pdf, s804/s814/s816/s817.html, s820.pdf) written by a wave-1 seat into the fleet root".
- `.ufo/reports/round-75/kotodama.md:18` — "one seat file at the fleet root, `.ufo/waves/round-75/w1/RevEntryQuality.md`".
- Inherited-but-unowned sightings: `.ufo/reports/round-26/tameshi.md:69`, `round-39/kumitate.md:215`, `round-49/chousa.md:100`, `round-63/kumitate.md:29`, `round-64/kumitate.md:19` (fleet-root `.ufo/waves/round-30/`, `round-41/`, `round-49/`).

Note the shape: the recurring path is `.ufo/waves/round-N/<wave>/<Seat>.md`, i.e. exactly the `Report:` trailer path resolved against the fleet root instead of the lane. This round's dispatch removes most of that risk (§6).

## 6. This round's affordances (checked, not assumed)

- The shared `taskCall.context` anchors write scope absolutely for all 64 seats: "Write scope. Your ONLY allowed writes are (1) your receipt at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42/wave1/<SEATNAME>.md` … Every `Report:` trailer path is relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — write it at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/<that path>`."
- The 64 per-seat `task` strings still end with the relative form (`.ufo/waves/round-42/wave1/<Name>.md`, 64/64 without an absolute anchor in the task itself); the context sentence disambiguates it. A seat that reads only its task line retains the historical trap.
- One task contains an unanchored *write verb* against a lane path: `ScribeC2Entry` — "Write corpus/knowledge/<slug>.md for the F25 topic". If taken literally from cwd = fleet root this creates `/home/vgpnk/Projects/shokunin/corpus/knowledge/…`. It was **not** realized: fleet root has no `corpus/` (`ls -d /home/vgpnk/Projects/shokunin/corpus` → No such file or directory), the seat wrote its deliverable beside the receipt (`ScribeC2Entry.entry.md` exists), and its receipt opens with "no mutating git/jj, no write outside this seat's wave-1 receipt/deliverable and that scratch dir." Latent vector, not an incident.

## 7. Severity, exploit path, impact, smallest remediation

- **Untracked stray at fleet root — LOW.** Exploit: a seat runs `curl ... -o o.bin`, `tee x.txt`, `> out.json` or `mkdir -p corpus/... && cat > ...` from its inherited cwd. Impact: permanent `git status` noise that masks real lane changes and survives rounds (`o.bin`, 18 h+, three sentinels); cannot enter history through `fleet-commit.sh`. Detected here: zero kasegi instances in 45.97 min across 55 `.md` files in the wave dir.
- **Truncation/overwrite of a tracked fleet-root file — MEDIUM.** Same exploit, but the relative path collides with `LOG.md` / `SCORECARD.md` / `MANIFEST.json`; realized once already (inline-dispatcher.py:99). No hook, no cwd assertion, no pre-commit path check stops it; recovery is manual restore.
- **Fleet history pollution — LOW.** Pathspec-limited committer plus `snapshot.auto-track="none()"` in `fleet-commit.sh`; verified live on `fca0f3f0`, which added only its one named report path.

**Smallest remediation (one change, no harness API dependency):** spawn each seat with a cwd outside the fleet root — run the `agent(...)` calls in `scripts/hyaku/inline-dispatcher.py` (`:205`, `:214`, `:257`) from the seat's scratch directory, or prepend `cd "$S" || exit 1` (with `$S` the seat scratch, already mandated by the seat spec) as the first line of every spawned prompt. Keep the current SEAT_GUARD prose as defence in depth; it is not a control. A cheap detector alongside it: at report-commit time, diff `git -C "$FLEET" status --porcelain` against the wave-start baseline and name any new non-ignored path, so a stray is caught in the round it appears instead of three sentinel sweeps later.

## 8. Bounds and hygiene

- Writes: this receipt only (receipt-only item), plus scratch under `/fast/scratch/hyaku/kasegi-r42/SentinelMisroot/` (removed before yield). No deliverable file.
- No mutating git/jj command anywhere (`git add -A` was run with `--dry-run` only); no writes to the fleet root, sibling lanes, `~/Projects/*`, or PATH directories; no subagents; no `agent://all`; no swarm.
- No tool installs or upgrades; `pacman` untouched. No network fetches (no HTTP status/bytes to record).
- Disk guard green before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0, `/fast/scratch/hyaku` 27 % used, 592.6 G free.
