# SentinelMisroot — round 41, wave 1 (receipt-only: fleet-root misroot watch)

Seat `SentinelMisroot` (leaf). Item: fleet-root misroot watch. Watch window
`2026-10-27T08:23:42Z` → `2026-10-27T08:31:00Z` UTC, continuous sampling (~36 s on channel A,
60 s on channel B) for the whole window; the wave-1 build was still landing receipts at close
(47 files in `wave1/`), so the detector below is re-runnable by the L1 for the remainder.

Refs verified at open (read-only `git cat-file -t`):
base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` → `commit`; claims-freeze
`fbba3d96cdf8d37c1ea41304a1ba35691329684b` → `commit`; round-40 judged head
`c7aea5ef97902f38289cbdc1cf267068876a62dd` → `commit`; lane tip at open
`b3b08b276af6146217efd89f7595243a644ed00b`. Disk guard green at open
(`/fast/scratch/hyaku 25% use, 605.0G free`).

Writes made by this seat: **this receipt only**, plus scratch
`/fast/scratch/hyaku/kasegi-r41/SentinelMisroot` (removed at yield). No fleet-root, shokuknow,
PATH-directory, sibling-lane or source-tree write. No git/jj mutation. No tool installed.

## 1 Verdict

**0 seat misroots.** At every sample, **no file outside the kasegi lane names kasegi together
with round-41/r41** (channel B, 5 samples, all `nonlane_hits=0`), and **no file was created or
modified at fleet-root level outside the 21 lane directories** (channel C, 0 at both sweep
passes). Two fleet-root writes did occur in the window; both belong to other lanes and both
triage to zero kasegi content (§5). The shokuknow dirty set is pre-existing drift, not this
wave: 0 of its files have an mtime or ctime inside the window, and 0 of 5,217 entries name
kasegi.

## 2 The prescribed check is structurally blind to the misroot it is meant to catch

`git -C /home/vgpnk/Projects/shokunin status --porcelain` reads 4,985 tracked fleet files plus
unignored untracked ones. Fleet `.gitignore` ignores every lane directory outright:

```
$ grep -n . /home/vgpnk/Projects/shokunin/.gitignore
1:*-shokunin/
2:# sources-census selftest fixtures are synthetic lanes, not lane repos
3:!scripts/fixtures/sources-census/**/*-shokunin/
4:# xsentinel w8-F7: per-wave cross-lane seat scratch is transient
5:.ufo/waves/*/*-scratch/
6:r80-baseline-frozen-worktree/
7:# driver runtime (AGENTS.md: never committed); files stay on disk
8:.ufo/state/*
9:!.ufo/state/.gitkeep
10:.ufo/watchdog.log
11:# tower orchestration comms/quarantine: local tool state, not fleet history
12:.tower/

$ git -C /home/vgpnk/Projects/shokunin check-ignore -v kasegi-shokunin/LOG.md
.gitignore:1:*-shokunin/        kasegi-shokunin/LOG.md
$ git -C /home/vgpnk/Projects/shokunin check-ignore -v mado-shokunin/.ufo/waves/round-48/x.md
.gitignore:1:*-shokunin/        mado-shokunin/.ufo/waves/round-48/x.md
```

Exposure arithmetic measured at 08:29Z:

| surface | files | visible to `status --porcelain` |
|---|---|---|
| tracked fleet files | 4,985 | yes |
| files inside the 21 `*-shokunin/` dirs | 522,607 | **no** (of which 514,411 are in sibling lanes, 8,196 in the kasegi lane) |
| ignored `.ufo/state/` entries | 82 | **no** |
| `.tower/`, `.ufo/watchdog.log`, `.ufo/waves/*/*-scratch/` | (ignored) | **no** |

So a seat that lands `kasegi round-41` bytes inside a sibling lane, in `.ufo/state/`, or in a
cross-lane `*-scratch/` dir produces `fleet=0`. Demonstrated on a throwaway fixture
(`mktemp -d`, `git init -q`, toplevel asserted equal to the fixture dir):

```
$ git -C "$D" status --porcelain -uall
?? .gitignore
$ bash detect2.sh "$D" '2000-01-01 00:00:00'
/fast/scratch/.../fix.1Ag5TH/mado-shokunin/.ufo/waves/round-41/SentinelMisroot.md
/fast/scratch/.../fix.1Ag5TH/.ufo/state/r41-seat.txt
```

Two misrooted files, porcelain silent on both. Every reading in §3 is therefore paired with a
mtime+content channel; a bare `fleet=0` is not evidence of no misroot.

## 3 Channels and their controls

Channel A — prescribed porcelain, both repos, ~36 s cadence (`samples.log`):

```
2026-10-27T08:24:06Z .. 2026-10-27T08:26:07Z  fleet=0  know=1918
2026-10-27T08:26:47Z .. 2026-10-27T08:26:47Z  fleet=1  know=1918
2026-10-27T08:27:27Z .. 2026-10-27T08:28:07Z  fleet=0  know=1918
2026-10-27T08:28:47Z .. 2026-10-27T08:28:47Z  fleet=1  know=1918
2026-10-27T08:29:27Z .. 2026-10-27T08:30:07Z  fleet=0  know=1918
samples_total=10  first=08:24:06Z  last=08:30:07Z
```

Channel B — mtime+content detector, ~60 s cadence (`detect-samples.log`):

```
2026-10-27T08:26:29Z .. 2026-10-27T08:30:32Z  nonlane_hits=0
detect_samples_total=5
```

Detector (`detect2.sh`), exactly as run:

```bash
#!/usr/bin/env bash
# files newer than marker that name BOTH kasegi and round-41/r41
root=$1; marker=$2
find "$root" -xdev -type f -newermt "$marker" -not -path '*/.git/*' -not -path '*/.jj/*' \
     -size -2M -print0 2>/dev/null \
 | xargs -0 -r grep -lIiEZ 'round-41|r41|round 41' 2>/dev/null \
 | xargs -0 -r grep -lIiE 'kasegi' 2>/dev/null || true
```

Controls (scratch tree, same script):

```
$ bash detect2.sh ctl2 '2026-10-27 00:00:00'          # positive: file says "kasegi round-41 seat receipt"
ctl2/misroot/r41.md
$ bash detect2.sh ctl2/clean '2026-10-27 00:00:00'    # specificity: "kasegi only, round-39" + "round-41 only, mado"
(no output, exit 0)
$ bash detect2.sh /home/vgpnk/Projects/shokunin '2026-10-27 08:00:00' | grep -v '/kasegi-shokunin/'
(no output — 0 non-lane hits, live)
```

Channel C — evasion and file-type checks, run at two independent full passes (08:29:29Z,
08:29:36Z) and again at close (08:30:40Z). Identical results all three times:

| check | result |
|---|---|
| non-lane files with mtime > 08:00Z at file level | 0 |
| backdating evasion: ctime > 08:00Z but mtime older, anywhere outside the kasegi lane | 0 (then content-filtered for kasegi+r41: 0) |
| new non-regular files (fifo/socket/device) outside lanes | 0 |
| setuid/setgid/world-writable files at fleet-root level (depth ≤ 3) | 0 |
| new symlinks outside lanes | 0 |
| symlinks inside the kasegi lane resolving outside it / dangling | 0 / 0 (58 pre-existing fixtures) |
| hardlinked files outside the lane (nlink>1) | 14, all pre-existing (kaidoku r19, mado r34, souji) — 0 name kasegi, 0 new |
| `/tmp`, `/var/tmp`, `/dev/shm` files newer than 08:00Z naming kasegi | 0 |
| other-lane scratch under `/fast/scratch/hyaku` naming kasegi+round-41 | 0 |
| `~/Projects` entries newer than 08:00Z outside shokunin/shokuknow | 0 |
| writes in `~/.local/bin`, `/usr/local/bin` | 0 |
| fleet `.git` admin files touched since 08:00Z (staging/reset trail) | 0 files; index mtime 08:27:27Z matches the `export from jj` commit, i.e. no seat staged anything in the fleet repo |
| case-variant paths naming kasegi outside the lane | 175, all `.ufo/reports/round-N/kasegi.md` (tracked, rounds 1-20/22/32); none written this wave |

Shokuknow, expanded (`status --porcelain -uall`: 5,217 entries = 3,788 `??`, 1,405 `M`, 24 `D`;
the collapsed reading is 1,918):

```
$ find /home/vgpnk/Projects/shokuknow -type f -newermt '2026-10-27 08:00:00' | wc -l
0
$ find /home/vgpnk/Projects/shokuknow -type f -newerct '2026-10-27 08:00:00' | wc -l
0
$ xargs -r -d '\n' grep -lIi 'kasegi' < know.mods.txt | wc -l            # 1,918 modified paths
0
$ xargs -r -d '\n' grep -lIiE 'round-41|r41' < know.mods.txt | wc -l
0
```

Dirty-set mtimes run 2026-10-24 16:46 → 2026-10-25 13:34 (-0300); the 24 deletions' parent
directories run 2026-10-24 23:33 → 2026-10-25 02:33Z. All two days older than this wave;
shokuknow HEAD is `8b94c5c12c0521e4cd9ed8e5b6939afd8518c715` (2026-10-24T11:02:02-03:00).

## 4 Landing-path integrity for this seat's own class of write

The wave-1 receipt path was confirmed symlink-free component by component, so seat receipts
cannot be redirected out of the lane by a planted link:

```
$ namei -l .../kasegi-shokunin/.ufo/waves/round-41/wave1
f: .../kasegi-shokunin/.ufo/waves/round-41/wave1     (every component drwxr-xr-x vgpnk, none 'l')
```

Landed receipts were also checked for path mislabelling: 0 of 47 name a fleet-root receipt path
(`/Projects/shokunin/.ufo/…`, i.e. missing the `kasegi-shokunin` component). One receipt
(`ScoutSibling.md`) quotes a sibling-lane file (`kake-shokunin/corpus/knowledge/security-txt-publishing.md`)
as read-only evidence — a citation, not a write claim.

## 5 Live events (both non-kasegi)

**E1 `2026-10-27T08:26:47Z` — `?? .ufo/reports/round-60/kake.md`.** First fleet-root capture,
channel A sample 5. Content: `# kake — round 60 report (attempt 2, run-10)`, kasegi mentions 0,
round-41 mentions 0 (kake tokens 6). Committed to the fleet repo at 08:27:10Z as `caddf63b`
"round-60: kake report" (reflog: `export from jj`), after which channel A returned to 0.
Verdict: the kake lane's L1 writing its own per-lane report to the sanctioned fleet reports
path. Not a kasegi seat, not a misroot.

**E2 `2026-10-27T08:28:47Z` — `?? .ufo/waves/round-43/w1/artifacts/R43Simplify/removal-ledger.json`.**
Channel A sample 8. Content read while present: 138 lines, `"seat": "R43Simplify"`,
`"round": 43`, kasegi lines 0, r41 lines 0. Gone by 08:29:27Z, never tracked
(`ls`: directory `R43Simplify/` absent), no commit in the fleet log. Verdict: transient artifact
of the kaidoku round-43 wave, removed by its own seat/L1; zero kasegi content, not a misroot.
This event is the sensitivity proof that channel A does move on real traffic inside the window.

No kasegi-content fleet-root write occurred at any point in the window.

## 6 Adjacent findings (not misroots; for the L1)

**A1 — severity med — an unresolvable base literal is still being shipped to seats.**
`5b29ea1439450b712581edf5f0bf98dfb262ab` is 38 hex chars;
`git cat-file -t` → `fatal: Not a valid object name`, while
`5b29ea1439450b712581edf5f0f0bf98dfb262ab` (40) → `commit`. `claims.json` itself is clean —
`base` (len 40), `judged_head_rule`, `claims[0].predicate` and `claims[0].counting_commands[2]`
all carry the 40-char form; only `errata[0].correction` quotes the bad string, deliberately.
The bad literal survives in:

| file | where | blast radius |
|---|---|---|
| `.ufo/waves/round-41/wave1-spec.json` | `.context` (×2) | all 60 seat prompts |
| `.ufo/waves/round-41/wave1-dispatch.json` | `.taskCall.context` (×2) | all 60 seat prompts |
| `wave1-spec.json` `.items[19]` / `wave1-dispatch.json` `.tasks[19]` | task text (×1) | **ScribeLesson** — writes the base into the `corpus/lessons/round-41.md` frontmatter |
| `wave1-spec.json` `.items[37]` / `wave1-dispatch.json` `.tasks[37]` | task text (×1) | **RevC2Shape** — "run every frozen C2 counting command on the base tree <38-char>" |
| `.ufo/waves/round-41/c1-controls/do-nothing.txt` | lines 1-2 | frozen before-control; the file carries its own in-line erratum paragraph |

Impact if uncorrected: the round-41 lesson lands an unresolvable base hash in committed bytes,
and the C2 base-tree discriminator runs die at ref resolution instead of producing the BEFORE
values. Notified by `write agent://`: `ScribeLesson` confirmed it had already used the 40-char
form in both frontmatter positions (73-line deliverable, sha256 `2f54ae0a…b102664`, 0
occurrences of the short form) and logged the claims string verbatim in its §Conflicts;
`RevC2Shape` confirmed all runs use the 40-char form and will record the short form as a
claims-literal defect, not as evidence. ScribeLesson's added caveat is the sharp one for C1:
**a base negative control run on the short hash reds through git resolution failure, not through
the instrument**, so I10/I12 could be green for the wrong reason — the suite's base/round-40
negative controls must be parameterised on the 40-char literals and `I12` must assert the
distinct `ref-not-found` red separately from `closed<12/12`.

**A2 — severity low (instrument, this seat's own remit) — bare porcelain cannot discharge this
watch.** §2 is the evidence; recommend the L1's close-out sweep use
`git status --porcelain --ignored=matching` plus the channel-B detector above (mtime and ctime
variants) rather than the porcelain reading alone.

**A3 — severity info — surviving scratch at 08:28:25Z:** 43 seat dirs under
`/fast/scratch/hyaku/kasegi-r41`, 27 non-empty (my own is removed at yield). Listed for the L1's
I6-class sweep; ownership is not mine to act on.

**A4 — severity info — the fleet reports path is a sanctioned fleet-root write for an L1, not for
a seat.** `.ufo/reports/round-N/<lane>.md` is tracked and holds 175 kasegi-named files from
rounds 1-20/22/32; `.ufo/reports/round-41/kasegi.md` was absent at close. When the kasegi L1
lands its own report there it will appear as an untracked fleet-root entry exactly like E1 —
triage on content (channel B) not on the bare entry.

## 7 Reproduction

```bash
FR=/home/vgpnk/Projects/shokunin; K=/home/vgpnk/Projects/shokuknow
git -C "$FR" status --porcelain -uall | wc -l                       # channel A (blind, see §2)
git -C "$K"  status --porcelain -uall | wc -l
find "$FR" -xdev -type f -newermt '2026-10-27 08:00:00' -not -path '*/.git/*' -not -path '*/.jj/*' \
  | grep -vE "^$FR/[^/]+-shokunin/" | wc -l                         # non-lane writes
find "$FR" -xdev -type f -newerct '2026-10-27 08:00:00' -not -newermt '2026-10-27 08:00:00' \
  -not -path '*/.git/*' -not -path '*/.jj/*' | wc -l                # backdating evasion
bash detect2.sh "$FR" '2026-10-27 08:00:00' | grep -v "/kasegi-shokunin/"   # content channel
find /tmp /var/tmp /dev/shm -xdev -type f -newermt '2026-10-27 08:00:00' -size -1M -print0 \
  | xargs -0 -r grep -lIi kasegi                                     # tmp leakage
```

Scratch `/fast/scratch/hyaku/kasegi-r41/SentinelMisroot` (watch scripts, logs, controls, the
git fixture) removed before yield; the fixture directory was deleted inline after its transcript
was taken.
