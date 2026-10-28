# SentinelMisroot — kasegi round 43 misroot watch

Seat: SentinelMisroot (leaf, receipt-only) · lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` ·
base `ab98fac9dce87130bc4f66de89e30650d63943dc` · claims frozen 2026-10-28T16:37:07Z.
Watch window: **2026-10-28T16:43:09Z → 16:53:20Z** (local 13:43:09 → 13:53:20), seven
`git status` polls. All work read-only outside my own scratch; nothing deleted.

## 1. Frozen inputs read first (unmodified)

```
$ sha256sum .ufo/waves/round-43/{claims.json,c1-controls/do-nothing.txt,c2-controls/before.txt,freeze.txt}
a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630  claims.json
221d20331e7d673f3ce3a3778ede2dccb0094620cd51867da0c609f6e2f7a08e  c1-controls/do-nothing.txt
14c58348252713bbd507fbef4e2680ab1709528b986d036a5e5157d48f9bf50b  c2-controls/before.txt
568b42229d8c62bb5754fcc08ee48685a4c11857dbf612b5d58857112230ed8e  freeze.txt
```

`freeze.txt` records `claims-sha256=a4c03e1e…`, equal to the live file, and all four paths are
tracked-clean in the lane (`git status --porcelain` shows no ` M` line). Frozen bytes intact.

## 2. Polls (the item's primary watch)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` at 16:43:09, 16:44:34, 16:45:47,
16:50:52, 16:52:30, 16:53:20, plus one expanded mid-poll at 16:51:19. Baseline output (verbatim,
8 lines):

```
 M .scratch/goal-20261028-hyaku-run11.md
?? .scratch/closure-mado-r50.json
?? .scratch/closure-r54/
?? .scratch/source-routing-queue.md
?? .ufo/reports/round-38/souji.md
?? o.bin
?? oldrep1.out
?? oldrep2.out
```

`-uall` form is 40 lines (1 ` M` + 39 `??`; 36 entries under `.scratch/`, 1 under `.ufo/`,
`o.bin`, `oldrep1.out`, `oldrep2.out`), sha256 `314dfc481a83f99fef15cd5c2551289dd843b36a658a06aa57a7a1f95b7af1a1`
identical at 16:43:09, 16:50:52 and 16:53:20. **No untracked file naming kasegi or round 43
appeared in the fleet worktree at any poll.** The only mid-window change was a *tracked* path
transient, resolved in §6.

Every baseline entry predates the window and is classified:

| path | size | mtime | first line / kind | kasegi/r43? |
|---|---|---|---|---|
| `.scratch/goal-20261028-hyaku-run11.md` | 4207 | 13:41:14 | `# …` run-11 goal (tracked, ` M`) | no (orchestrator, pre-window) |
| `.scratch/closure-mado-r50.json` | 3579 | 10-27 06:38 | JSON closure record | no |
| `.scratch/closure-r54/` (30 files) | — | 10-28 12:55 | coldread/witness scratch | no |
| `.scratch/source-routing-queue.md` | 3667 | 10-27 22:05 | routing queue | no |
| `.ufo/reports/round-38/souji.md` | 21866→21907 | 13:43:18 | `# souji round 38 — commit-arm citations…` (souji lane draft at the shared reports root) | no |
| `o.bin` | 5867 | 10-27 16:58 | `<!DOCTYPE html>…Just a moment…` (saved challenge page) | no |
| `oldrep1.out` | 15314 | 10-28 09:10 | `PASS healthy: all planes pass (exit 0, HEALTHY)` | no |
| `oldrep2.out` | 15314 | 10-28 09:11 | same generator | no |

`.ufo/reports/round-38/souji.md` grew during the window (21866→21907) — a souji-lane seat writing
its own round-38 draft into the shared fleet reports tree. Not kasegi, not round 43; recorded,
not touched.

## 3. Convention: what would *not* be a misroot

Fleet-root `.ufo/reports/round-N/<lane>.md` is the established landing place for lane reports, not
a misroot: `git ls-files .ufo/reports | wc -l` = 861, and `.ufo/reports/round-43/` already holds 11
lane reports (chousa, kaidoku, kake, kama, kengaku, kotodama, kumitate, mado, mori, tameshi,
tsukuroi). The w1 scribe skeleton names that path as its landing target
(`ScribeReportSkeleton.md:15  | Lands at | /home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kasegi.md |`).
So a new `.ufo/reports/round-43/kasegi.md` at landing is expected. Misroot for this seat = any
kasegi/round-43-named path outside the lane and outside that reports convention. Fleet `.gitignore:1`
is `*-shokunin/`, so the lane repo itself shows as `!! kasegi-shokunin/` — intended.

## 4. Protected paths, measured (premise partly false)

**`.scratch/` — untouched.** Aggregate `find .scratch -printf '%P %s %T@\n' | sort | sha256sum`
= `9b56e5bb11cbb657059c97c591c6333baa8ba45bbbc0e1f01d1e7d024da73d79` at every poll (16:43:09 →
16:52:39). The one tracked modification (run-11 goal, mtime 13:41:14) predates the window.

**`.ufo/watchdog.log` — APPENDED during the window, by the host watchdog, not a seat.**

```
T0 16:43:09Z  067512b4bedeb259dafea74e15fb502d4eee183d55f30e5ce2519156011ef205  175479 B  mtime 13:36:07
T4 16:52:39Z  9a6f10b384e28a740c04e6dbbe62ca5176596bda253acc01fd9b1b56f21cb025  175552 B  mtime 13:52:38
$ tail -c 73 .ufo/watchdog.log
2026-10-28T13:52:38-03:00 complete mori round=60; hyaku-inline attempt=1
```

Delta = exactly that one 73-byte line (mori lane round-60 completion). The kasegi entry in the log
is pre-window: `1851:2026-10-28T13:29:27-03:00 launch kasegi round=43 pgid=3638835
driver=hyaku-inline attempt=1`; there is no kasegi `complete` line at close (round still live).

**`.ufo/state/` — NOT untouched; two host log files grow continuously.**

```
T0 hash f5279d4654d7b8708a822d677d33ef23ebc5550e347c469dc8d317acf9a22bd1  (83 files)
T4 hash 6ba7a25cb99c5c323a5d2bb16575d324b3ffa53db5cc6d9076252b4feebb1b11
$ find .ufo/state -type f -newermt '2026-10-28 13:43:09' -printf '%P|%s\n'
disk-guard.log|11657551
inline-dispatcher.log|9981119
```

Only those two files changed; `disk-guard.log` was 11,654,665 B at 16:44 and 11,657,551 B at 16:52,
`inline-dispatcher.log` 9,971,648 → 9,981,119 — host tooling appends. The kasegi-specific entry was
written pre-freeze by L1 setup, 68 B, mtime 13:29:26:

```
$ stat -c '%s|%y' .ufo/state/kasegi.report-baseline ; cat .ufo/state/kasegi.report-baseline
68|2026-10-28 13:29:26.078016278 -0300
43 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The fleet prompt file is tracked and clean: `.ufo/prompts/kasegi-round-43.md`, 56,413 B,
mtime 13:29:26, `git ls-files --error-unmatch` succeeds, no ` M` line.

Verdict for §4: **zero seat writes** to the three protected paths; the literal "untouched" claim is
false for `.ufo/state/` and `.ufo/watchdog.log` only because host append-only logging continues
throughout a round. Restate the control as "no seat modifies them; only host-owned logs append".

## 5. Out-of-tree misroot inventory (`/tmp`) — the substantive findings

`/tmp` is a 128 GiB xfs (`reflink=1`) with 22 GiB used and 3,579 top-level entries; `du -sh /tmp`
reports 92 GiB because reflink clones are counted per file (shared extents are one copy on disk).

### 5.1 (medium) Landed instruments default their work root to `/tmp` — live leak, 25 dirs

```
$ ls -d /tmp/k17-work.* | wc -l           → 25
$ first/last: 13:45:36.588 (.4tC5KIDy) … 13:53:12.251 (.EXkDT0OC)
$ all empty?  empty=25 of 25 ; du -sb → 0 bytes
```

Root cause, in the landed deliverable bytes (shas pinned):

```
ExecK17ClaimsBefore.sh:570  37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348
    K17_WORK=$(mktemp -d "${TMPDIR:-/tmp}/k17-work.XXXXXXXX") || exit 2
ExecSelftest19.sh:918       d2c947b4a5004d49f9677479f6142a10b1d796f638da3fd3481863ffb5a11848
    root = opts["scratch_root"] or os.environ.get("TMPDIR") or "/tmp"
ExecC2Counters.bundle.sh:21 b3b0075dc6785700254eb4c6a8913d81c3aee588cd98d8c3ea8c12ef00a08576
    export TMPDIR=${TMPDIR:-/tmp}
```

`ExecK17ClaimsBefore.sh` also installs no cleanup: the only `rm -rf` is
`574: rm -rf -- "$K17_WORK/export"`; there is no `trap` and the work root is never removed, so every
default-mode invocation leaks one empty directory. Failure path: any drive script or reviewer that
runs the limb without `--work` lands its tree in `/tmp`; the `/tmp` directory is shared, world-writable
(`drwxrwxrwt`), and outside both the lane and `/fast/scratch`. Impact today is noise (0 bytes, 25
dirs in 7.5 min), but it is the exact scratch-binding rule this wave enforces, it will recur on every
suite run after landing, and `$TMPDIR` fallback makes the root nondeterministic per process.
Smallest remediation: require the root — `--work`/`--scratch-root` mandatory (exit 2 when absent,
matching C1's plain-run-refuses posture) — or default to a path under `/fast/scratch/hyaku`, never
`/tmp`; and `trap 'rm -rf -- "$K17_WORK"' EXIT` only when the script minted the directory itself.

### 5.2 (low) Round-42 kasegi scratch still resident on `/tmp`

```
/tmp/kasegi-r42-judge     62G du / 57,970,573,036 B apparent   dir mtime 10-28 12:44   first entry: a1
/tmp/verif-kasegi-r42     26G du / 23,974,690,812 B apparent   dir mtime 10-28 12:30
```

Both predate the freeze (12:30/12:44 vs 13:37:07) and belong to round 42. They are 88 GiB of logical
tree on the `/tmp` partition; the whole partition reports only 22 GiB used of 128 GiB because reflink
clones share extents. Other kasegi-named survivors:
`/tmp/kasegi-base` 149M, `/tmp/kasegi-forge` 171M, `/tmp/kasegi-r40-draft` 52K,
`/tmp/kasegi_r41_outside_probe` (empty dir), `/tmp/closure-kasegi-r41.json` 3679 B,
`/tmp/kasegi-r42-closure.json` 4153 B (first line `{`, `"round": 42,`). Sweeper candidates; I deleted
nothing.

### 5.3 (low) Files created *during this window* by round-43 kasegi seats

| path | size | mtime | first line / content |
|---|---|---|---|
| `/tmp/k18prompt.txt` | 1534 | 13:40:02 | `/skill:godspeed  Read /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/claims.json first (frozen claims; never edit). Deliverables: ExecK18Transcript.sh (source…` (truncated at 180 bytes) |
| `/tmp/revk19.out` | 58 | 13:43:15 | `K19 payload=freeze=present,order=ok,sha=mismatch closed=0` |
| `/tmp/revk19.err` | 0 | 13:43:15 | empty |
| `/tmp/revk19.src` | 0 | 13:44:16 | empty |
| `/tmp/k14_k14-m1.sh.py` | 4395 | 13:46:03 | `import os` … `# MUTANT K14-M1: stale-literal comparison dropped` |
| `/tmp/k14_k14-m2.sh.py` | 4489 | 13:46:03 | K14 mutant driver (3 `K14` refs) |
| `/tmp/k14_k14-m3.sh.py` | 4374 | 13:46:03 | K14 mutant driver |
| `/tmp/k17-work.*` | 25 × 0 | 13:45:36–13:53:12 | empty dirs, §5.1 |

`k18prompt.txt` is the strongest of these: it is a verbatim seat assignment naming kasegi round 43,
parked in `/tmp`. `revk19.*` and `k14_k14-m*` are scratch for the K19 and K14 limbs. Each is a
misroot of the same class (scratch outside `$S`); none exceeds 50 MB, so the disk rule is not
breached, but the binding rule is.

### 5.4 Not kasegi — recorded to prevent false attribution

`/tmp/r43p/` (5 files, 10-27 05:28), `/tmp/kaidoku-r43/`, `/tmp/r43-tool.py` 20507 B,
`/tmp/r43-freeze-files.txt` 2,223,039 B, `/tmp/r43-manifest-before.sha` 116 B,
`/tmp/r43c1gen_scratch_path` (content `/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Gen`) are **kaidoku's**
round 43, days older. `/tmp/sc_base.md` 299,172 B is tameshi's scorecard; `/tmp/census.out` and
`/tmp/w1_{log,q,sc}_land.txt` are souji round-38; `ecc-metrics-*.json`, `bash-manual.html`,
`playwright_firefoxdev_profile-*` are harness/browser artifacts. "Round 43" is per-lane, not fleet-wide.

## 6. Git mutation audit

Fleet repo HEAD advanced twice **during** the window, both jj→git exports for the mori lane:

```
55ed7910  → eeedfd53  13:51:32  round-60: mori report — C1 verified met; C2/C3 … ; wave 64/64
          → 667c5c55  13:52:39  round-60: hyaku closure dispatch for mori
$ git show --stat --oneline eeedfd53 | head -3
eeedfd53 …  .ufo/reports/round-60/mori.md | 191 ++
$ git show --stat --oneline 667c5c55 | head -3
667c5c55 …  .ufo/prompts/closure/mori-round-60.md | 97 ++
$ git diff --name-only 55ed791..667c5c55 | grep -i kasegi ; echo rc=$?
rc=1
```

No kasegi path in either export. This also explains the only anomalous poll: at 16:51:19 the expanded
status reported `?? .ufo/reports/round-60/mori.md` (written untracked at 13:51, one second after the
13:51:32 export cut), and at 16:53:20 the path is tracked (`100644 e91c0d2b…`) and clean — a
mid-flight race with another lane's export, not a kasegi write.

Lane repo: `HEAD 4cb6d4ae768481e1a14afbedc2d865a060ebacfd` at every poll; last reflog entry
`4cb6d4a HEAD@{2026-10-28 13:37:11} export from jj`; 5 porcelain entries, **all** `??` under
`.ufo/waves/round-43/`; zero tracked modifications (`git status --porcelain | grep -v
'.ufo/waves/round-43/'` → empty, rc=1). No staged changes anywhere in the fleet repo
(`git diff --cached --stat` empty). No seat ran a mutating git command in the window.

Fleet `.git/index` mtime is 13:53:20 — the stat-cache refresh of my own read-only `git status` polls;
size 610,912 B, no `index.lock` present, no content change.

## 7. Wave-dir byproducts (landing caution)

```
w1/__pycache__/ExecGateChain.rules.cpython-314.pyc          18063  13:44:56
w1/__pycache__/ExecGateManifest.rules.cpython-314.pyc       21232  13:44:56
w1/__pycache__/ExecGateProvReport.rules.cpython-314.pyc     25485  13:47:43
w1/__pycache__/ExecGateCore.claim-package-check.cpython-314.pyc 46859 13:50:46
```

Python bytecode written into the deliverable directory (precedent in rounds 24/25 wave dirs). Not a
fleet-root misroot, but if the L1 lands with `git add .ufo/waves` these four binary blobs enter the
lane. Exclude `__pycache__/` from the landing set; the delivered `.py` sources are the artifacts.
Related observation, not a misroot: `ExecTranscriptDe0931.txt` was 0 bytes at 13:42:45 and was no
longer zero-size later — a transient, its owner's concern.

## 8. Tooling and host compliance

`grep -cE '^\[2026-10-28T1[3-9]' /var/log/pacman.log` → **0** (last transaction line 11:43:17, before
the round): the host pause is observed. `~/.local/bin` newest entries are 11:52 / 11:42 / 10:50
(omp, OpenBot) — no PATH write during the round. I installed no tool, edited no config, ran no
service command, and did not run `disk-guard.sh` (a heavy pass never occurred; running it would itself
append the state log audited in §4).

## 9. Scratch accounting and cleanup

`/fast/scratch/hyaku/kasegi-r43` held 58 seat dirs / 68 GiB at 16:45 (largest: ExecK18Transcript 11G,
RevK19 7.9G, ExecTranscriptDe0931 7.3G, ExecCarryChecks 6.1G, ExecK14Corrections 4.4G); `/fast` was
227G/577G at 16:52. Cross-check of receipt-vs-scratch found no yielded seat leaving a live scratch
tree (`ScoutConsiderthese` had one at a 16:44 probe and it was gone by 16:45 — transient, its own
cleanup). My scratch `/fast/scratch/hyaku/kasegi-r43/SentinelMisroot` is removed at close; every
work file in this receipt was produced there first.

## 10. Verdict

| # | finding | severity | evidence |
|---|---|---|---|
| 1 | Three landed instruments default work/scratch to `/tmp`; K17 leaks one empty dir per run, 25 observed live | **medium** | §5.1 |
| 2 | Round-42 kasegi scratch (62G + 26G du) still on `/tmp` | low | §5.2 |
| 3 | Seat assignment prompt copied to `/tmp/k18prompt.txt`; K19/K14 scratch in `/tmp` | low | §5.3 |
| 4 | `__pycache__` (4 blobs, 112 KB) inside the deliverable dir | low | §7 |
| 5 | "`.ufo/state/`, `.ufo/watchdog.log`, `.scratch/` untouched" is false as written for the first two | info | §4 |

**Zero kasegi round-43 misroot in the fleet worktree across seven polls**: none of the 39 untracked
entries names kasegi or round 43, the lane repo has no tracked modification and no new commit, and the
only fleet-HEAD movement is two mori round-60 exports carrying no kasegi bytes. All kasegi/round-43
bytes written outside the lane sit in `/tmp` and are listed above with sizes, mtimes and first lines.

Sweep list for the L1 (nothing deleted by me):
`/tmp/kasegi-r42-judge`, `/tmp/verif-kasegi-r42`, `/tmp/kasegi-base`, `/tmp/kasegi-forge`,
`/tmp/kasegi-r40-draft`, `/tmp/kasegi_r41_outside_probe`, `/tmp/closure-kasegi-r41.json`,
`/tmp/kasegi-r42-closure.json`, `/tmp/k18prompt.txt`, `/tmp/revk19.src`, `/tmp/revk19.out`,
`/tmp/revk19.err`, `/tmp/k14_k14-m1.sh.py`, `/tmp/k14_k14-m2.sh.py`, `/tmp/k14_k14-m3.sh.py`,
`/tmp/k17-work.*` (25 empty dirs).
