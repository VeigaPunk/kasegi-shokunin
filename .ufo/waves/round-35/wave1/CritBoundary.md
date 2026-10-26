# CritBoundary — scope guard (round-35 wave-1)

Seat: CritBoundary (leaf critic, no subagents). Lane: `kasegi-shokunin`. Lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`, claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.
Observation window: 2026-10-26T06:38:5x–06:46Z (03:38:5x–03:46 -0300), i.e. while the wave was
still landing; every time-sensitive statement below is stamped. Assignment: (a) files written outside
the lane write scope, (b) fleet-root `git status` for untracked `kasegi`/`round-35` paths, (c) sibling
repos and `shokuknow` untouched, (d) no lane git/jj state mutated by seats, (e) every seat used
`/fast/scratch/hyaku/kasegi-r35` and deleted its tree. Verdict only — the L1 integrates and decides.

Axis reading used: C1 `depth:verifiability` (receipts-as-evidence, D4 "landed means committed" class),
C2 `coverage` (source provenance of S052).

## Report

### 1. Commands, outputs, exit codes

| # | Command | Output | Exit |
|---|---|---|---|
| 1 | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | 177 lines; the **only** line matching `kasegi\|round-35\|round35`: `160: M .ufo/state/kasegi.report-baseline` | 0 |
| 2 | `git -C /home/vgpnk/Projects/shokunin diff -- .ufo/state/kasegi.report-baseline` | `-27 e3b0c44298…` → `+35 e3b0c44298…`; `stat` mtime `2026-10-26 03:26:28 -0300`, i.e. 3 min before the wave dispatch (03:29) = hyaku harness round-open write, not a seat | 0 |
| 3 | `find /home/vgpnk/Projects/shokuknow -newermt '2026-10-26 03:20' -print` | first run: `COUNT=0`; later run: exactly one hit, `/home/vgpnk/Projects/shokuknow/.git` (dir, 03:40:09). `stat .git/index` = 2026-10-24 23:33:24, `.git/HEAD` = 2026-10-23 21:39:10, `find .git/refs .git/logs -newermt 03:20` = **empty** (see §5: my own `git status` lock churn) | 0 |
| 4 | `find /home/vgpnk/Projects/bounties -newermt '2026-10-26 03:20' \| wc -l`; same for `the-bounty-hunter` | `0`; `0` | 0 |
| 5 | `git -C <lane> log -3 --format='%H %ci %s'` | `da2d3c6… 03:29:16 round-35: wave-1 spec + dispatch (64 seats, v2)` / `617496b… 03:28:03 round-35: claims freeze + before controls` / `3266c99… 03:25:36 round-34 verifier spot-check` | 0 |
| 6 | `git -C <lane> reflog -n 8 ; git stash list ; git branch -av ; git worktree list` | newest reflog entry `da2d3c6 HEAD@{2026-10-26 03:29:16 -0300}: export from jj` (nothing after); stash empty; `master` = `remotes/origin/master` = `da2d3c6`; one worktree, `.git/worktrees` absent | 0 |
| 7 | `jj op log -n 22 -T '<id> <time> <description>'` | after the L1's last commit `9af495ff24b3 03:29:16 commit …` the log holds **only** `snapshot working copy` ops (03:31:25, 03:34:05, 03:34:49, 03:36:15, 03:36:50, 03:38:02, 03:39:01); no `commit`/`describe`/`bookmark`/`new`/`track paths` op after 03:29:16 | 0 |
| 8 | `git -C <lane> diff 617496b -- .ufo/waves/round-35/claims.json \| wc -l` | `0` (frozen claims byte-identical to the freeze commit) | 0 |
| 9 | `git -C <lane> status --porcelain` | 19 entries, all named by ≥1 wave-1 receipt (script in §4), no `*.tmp/*.bak/*.orig/*.rej/core.*` newer than 03:20, no `/home/vgpnk/Projects/**` or `/fast/scratch` absolute path in any new artifact (`grep -rnE` on `corpus/source-snapshots/round-35`, `wave1-results.json.provenance.md`, `cisa-kev-catalog.md`, `claims-erratum-d5.md` = **empty**) | 0 / grep 1 |
| 10 | ledger of `/fast/scratch/hyaku/kasegi-r35/*/` (python, per-dir newest mtime + receipt/trailer/absence-claim) | 03:38: 29 dirs → 03:41: 31 → 03:44:20: 24 → 03:45:57: 23; root-level files `0`; monotonically shrinking = wave in flight | 0 |
| 11 | `grep -hoE '/fast/scratch/[A-Za-z0-9._/-]+' wave1/*.md \| grep -v '^/fast/scratch/hyaku/kasegi-r35'` | one non-conforming path: `/fast/scratch/kasegi-d5/S051` (F4, documentation only) | 1 |
| 12 | `grep -cE '^Report: ' wave1/*.md` | 7 of 44 receipts carry the trailer at 03:45 (round-34: 14/67, round-33: 3/64 → convention is not regressed); `grep -c '^## Report'` fails only on `ScribeReportDraft.md` (helper drafting seat) | 0/1 |

### 2. Verdict (scope guard)

**PASS with two recorded defects and three hygiene notes.** No seat wrote outside
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; the fleet root carries no untracked `kasegi`/`round-35`
file; `shokuknow`, `bounties`, `the-bounty-hunter` hold zero round-window content writes; siblings
touched only themselves under their own round commits; the lane's git/jj state has **no**
commit/stage/bookmark/describe mutation from any seat. The defects are (F1) a durable receipt that
asserts its own scratch deletion before it is true, and (F2) an uncommitted plan edit whose factual
claim contradicts the landed capture. Both are C1-visible, neither breaks C2's counters.

### 3. Findings

**F1 — defect, must-fix-or-record: a receipt asserts `scratch-absent` and is then contradicted by
its own later writes (D4 class re-instantiated in round 35).**
`ExecClosureSuite` owns C1's closure instrument. Its receipt mtime is `2026-10-26 03:41:35`, sha256
`f8f99970c581eb89cccd77cb25f32b0f5d8956f03f855bd002e5cd3551b33367` (382 lines), and §12 reads
verbatim:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite
$ ls -d /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite 2>/dev/null || echo scratch-absent
scratch-absent
```

`No work tree of mine is left on disk.` — lines 367–371. Measured afterwards:
`03:42:59 ExecClosureSuite/live-selftest.txt`, `03:43:36 ExecClosureSuite/clean/.git/objects/…` +
`live.txt`, `03:43:43 ExecClosureSuite/green.txt`; `ls -d` at **03:44:26** returned the directory
(PRESENT). It is **ABSENT** again at 03:45:57. So the assertion was false for ≳200 s and true only
after a second cleanup the receipt does not record; the durable record is a *prediction*, not an
observation. If the seat had been killed in that window the lane would hold a receipt claiming
absence over a 6 930-file base export. Second, milder instance of the same ordering:
`ScribeEntryF18` line 101 says the root was "**removed before this receipt was filed** (`rm -rf --`
executed; `ls` of the parent afterwards showed no seat directory)" (receipt 03:40:42) while
`bod2604.html`/`bod2604.txt` were written into that path at 03:41; absent at 03:43:42.

**Resolved by the owner before my yield (re-verified, not taken on trust):** the seat re-filed the
receipt at 03:47:32 (06:47:32Z) — now 398 lines, sha256 `0b0e0abefaf47fff8b668a701dde2d625d140ab605ce14d03313097badb44ee3` — and §12 (lines 377–398) states the
ordering, quotes `rm_exit=0` and `2026-10-26T06:47:16Z`, and names the re-runnable check; I measured
`ls -d /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite` = **absent** at 06:47:48Z, and the instrument
bytes are unchanged (`corpus/instruments/r35-defect-closure.sh` sha256 `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f`, 834 lines), so no measured limb of
C1 moved. The defect was real at observation; the class (predicted rather than observed cleanup text)
is the one to guard at close.
*Smallest safe correction:* receipt §cleanup is the **last** act of the seat, phrased as executed
output, or phrased prospectively ("removed at exit, verified by the L1 gate"); and the L1 close adds
one gate: `find /fast/scratch/hyaku/kasegi-r35 -mindepth 1 -maxdepth 1 -type d -printf '%f\n'` must
show only dirs whose seat has no receipt, with the leftover list written into the lesson.

**F2 — defect, low: the uncommitted `build-spec.py` steer contradicts the landed capture and its own
executor's receipt.** `git -C <lane> diff -- .ufo/waves/round-35/build-spec.py` (mtime 03:32:50,
sha256 `a56179ca60e9f89105405609dd4729f6360c5fa00dbbefb3c7bc5b3081c0bd29`) replaces the ExecC2Capture
task with: "the JSON endpoint `https://www.cisa.gov/known-exploited-vulnerabilities.json` returns
HTTP 404 (measured 2026-10-26), so the official CSV distribution is the primary data source."
Measured facts: the 404 is that **short** URL only (`ExecC2Capture.md:18`
`code=404 final=https://www.cisa.gov/known-exploited-vulnerabilities.json`); the landed capture is the
**long JSON feed** — `corpus/source-snapshots/round-35/manifest.json` (sha256 `06bfcc71…`) records
`url = https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`,
`path = S052.txt`, sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, and
`head -c 400 S052.txt` is `{"title": "CISA Catalog of Known Exploited Vulnerabilities",
"catalogVersion": "2026.10.23", …}`. `ExecC2Capture.md:44` says so itself: "use the CSV because the
named JSON path 404s; that steer's premise is false one path over, and the CSV is not [needed]".
`corpus/README.md`'s round-35 amendment and the knowledge entry both cite the JSON feed correctly, so
C2's chain is clean. The hazard is the *plan* artifact: the edit has **no consumer** (the frozen
dispatch `wave1-dispatch.json` mtime is 03:29:04, i.e. never regenerated from the patched generator),
and it is uncommitted — if the L1 commits the working set wholesale it lands a false provenance
sentence next to the capture. Authorship is **unattributed**: no receipt declares editing
`build-spec.py`, and the only receipts that name it quote it as plan text (`ExecD4ResultsTrack.md:123`,
`ScribeIntegrationNotes.md:210`, `ScoutDatawalk.md:84`).
*Smallest safe correction:* revert `build-spec.py` to the dispatch-time bytes, or narrow the sentence
to the short URL and note the CSV was not needed; the L1 states authorship in the lesson.

**F3 — hygiene: attempt-suffix stripping collapses attempts into one scratch dir.**
Receipts address `/fast/scratch/hyaku/kasegi-r35/<seat>/` by the un-suffixed name while the roster
carries `-2`/`-3` attempts, so a resample inherits its predecessor's fixtures. Evidence:
`ExecNoHarmFinal/` holds `anchor.out 03:31`, `snap/ 03:32`, `anchor.cur.out 03:33` (attempt 1) beside
`base/ 03:37`, `closure.*.out 03:37`, `closure.t5.out 03:45` (attempt 3, still live at 03:45:57) in one
directory; `RevC2BeforeAfter-2/` nests a second `RevC2BeforeAfter-2/` under itself.
*Smallest safe correction:* scratch dir = full seat id (`ExecNoHarmFinal-3`), and the receipt records
`test ! -e` of the path before `mkdir -p`.

**F4 — hygiene: one committed artifact prescribes a scratch path outside the mandated root.**
`claims-erratum-d5.md` §3's reproduction recipe names `/fast/scratch/kasegi-d5/S051`; the citing seat's
own runs used the mandated root (`RevD5D6D7.md:73`, its F3, already on record).
*Smallest safe correction:* rewrite the recipe to `$HYAKU_SCRATCH`/the round-35 root or label the old
path as a round-34 historical path.

**F5 — note: one seat declares a `jj` invocation.** `ScoutPackageThemes.md:106`: "one `jj st` was run
once to see lane state (it snapshots the working copy; no description, bookmark, commit or file content
was changed by me)." This matches the op log's `snapshot working copy` entries (§1 row 7) and nothing
stronger; the lane has no seat-made commit, bookmark move, `describe`, `track paths`, or staged entry.
My own single `jj status` at 03:39:01 added snapshot op `ceaba0281e58` (disclosed in §5).

### 4. Clean limbs, quoted

- **Changed-path reconciliation.** Every one of the 19 `git status` entries is mentioned by at least one
  wave-1 receipt under a substring match of its basename (`corpus/instruments/r35-defect-closure.sh`,
  `r35-fixtures/`, `cisa-kev-catalog.md`, `source-snapshots/round-35/`, `claims-erratum-d5.md`,
  `c1-controls/fake-suite.sh`, `c2-controls/junk-f18.md`, `assimilation/`, `wave1.ready`,
  `wave1.ready.dispatched`, `round-34/wave1-results.json{,.provenance.md}`, `SCORECARD.md`, `SKILL.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt`,
  `build-spec.py` — the last only as quoted plan text, see F2). No unclaimed path.
- **Fleet root.** Only ` M .ufo/state/kasegi.report-baseline` names kasegi; the other round-window
  fleet writes are harness state (`.ufo/watchdog.log`, `.ufo/state/inline-dispatcher.log`,
  `.ufo/state/disk-guard.log`, 03:38–03:39) and other lanes' own rounds
  (`.ufo/reports/round-38/kengaku.md`, `.ufo/reports/round-39/tsukuroi.md`,
  `.ufo/prompts/{kengaku-round-39,kaidoku-round-38,tsukuroi-round-39}.md`). `.ufo/prompts/kasegi-round-35.md`
  is 03:26:28 = harness, tracked, unmodified. `.scratch/goal-20261026-hyaku-run8.md` = 02:28:22.
- **Siblings.** `git -C <sibling> log -1`: kaidoku `077e212b 03:33:18 round-38: c1-0 control re-scored
  under freeze v3`; tsukuroi `a6ca817 03:36:27 round-39: final self-assessment (27/0) …`;
  kengaku `6a1eb5e 03:40:45 round-39: first recorded git-leak probe run`. Their dirty/untracked paths
  are their own round's; no kasegi/round-35 string appears in kasegi's receipts as a write target
  outside the lane (grep §1 row 9 = empty).
- **Scratch root.** All cited paths under `/fast/scratch/hyaku/kasegi-r35/<seat>` (33 distinct seat dirs at the
  03:43 grep, 45 at the 03:46 recount — the set grew with the wave; includes the
  `ScribeSearchLog-verify` sub-dir), zero files at the root level, zero `/tmp` artifacts from
  round 35 (`find /tmp -maxdepth 3 -iname '*kasegi*'` returns only the six 01:18 round-33 peer-message
  files), `grep -c 'kasegi-r35' .ufo/state/disk-guard.log` = `0` (no guard-driven deletion explains
  any absence).

### 5. My own footprints (disclosed, none are content writes)

1. `jj status` in the lane at 03:39:01 — read intent; jj snapshotted the already-present working copy
   (op `ceaba0281e58`). No file byte, description, bookmark or commit changed.
2. `git status --porcelain` in `/home/vgpnk/Projects/shokuknow` — created and unlinked
   `.git/index.lock`, which is the `.git` dir mtime bump at 03:40:09; `.git/index` (10-24 23:33),
   `HEAD`, `refs/`, `logs/` unchanged, so **no** shokuknow state was written. This is the single
   round-window mtime in shokuknow and it is mine, not a seat's.
3. `/tmp/cb-fleet-status.txt` (scratch copy of §1 row 1) and `/fast/scratch/hyaku/kasegi-r35/CritBoundary/`
   (ledger) — both removed before yield (§6). No tool installed or upgraded.

### 6. Scratch cleanup proof

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r35/CritBoundary /tmp/cb-fleet-status.txt
$ ls -d /fast/scratch/hyaku/kasegi-r35/CritBoundary 2>/dev/null || echo scratch-absent
scratch-absent
$ test -e /tmp/cb-fleet-status.txt && echo PRESENT || echo tmp-absent
tmp-absent
```

Impacted axes: `depth:verifiability` (F1, F2 — receipt-vs-state ordering and plan-vs-capture
provenance are the two ways C1's evidence chain can lie while its counters still read 7/7), `coverage`
untouched (C2's S052 chain re-checked clean in §3 F2). No kill-rule is tripped by anything above.

Report: .ufo/waves/round-35/wave1/CritBoundary.md


Receipt self-digest: `head -n -1 .ufo/waves/round-35/wave1/CritBoundary.md | sha256sum` = `87132e13c1f48e0f891a8d182a375db4a1120dc944551003658815af0f1e4adc` (the digest line is the only line excluded; it covers this `## Report` and every quoted output above).
