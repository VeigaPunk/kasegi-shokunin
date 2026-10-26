# RevNoHarm — round-34 wave-1 independent no-harm review

Seat: RevNoHarm (reviewer, leaf). Round: kasegi-shokunin round 34 (hyaku run 8, L1 KasegiR34).
Lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`; wave-1 spec commit `206e5108f1190e61b3e2622d21cab8a5d921650c`.
Review time window: 2026-10-26 02:31–02:38 -03:00. All commands run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

**Measurement caveat (stated up front):** the wave-1 working tree is shared by ~65 in-flight seats and is *live*: identical commands at 02:31, 02:33 and 02:37 returned different numstats (instruments grew between snapshots). Every number below is a point-in-time snapshot; the L1 must re-run the numstat at integration/commit time. No numbers here are final-state claims.

## Report

### A. Append-only check — `git diff --numstat 014ee2d -- SKILL.md PROVINCE.md corpus SCORECARD.md LOG.md`

Snapshot T3, 2026-10-26 02:37:41 -03:00, exit 0:

```
31	3	SCORECARD.md
14	0	corpus/QUALITY.md
1	0	corpus/SOURCES.md
105	0	corpus/instruments/README.md
487	87	corpus/instruments/capture-binding-check.py
214	15	corpus/instruments/frontier-recheck-count.py
74	0	corpus/lessons/round-29.md
109	0	corpus/lessons/round-33.md
12	1	corpus/source-snapshots/round-26/manifest.json
3	3	corpus/source-snapshots/round-32/manifest.json
```

- **Untouched (absent from diff):** `SKILL.md`, `PROVINCE.md`, `LOG.md`. Zero changes.
- **Strictly append-only corpus records (0 deletions):** `corpus/QUALITY.md` (+14), `corpus/SOURCES.md` (+1, the S051 row), `corpus/instruments/README.md` (+105), `corpus/lessons/round-29.md` (+74), `corpus/lessons/round-33.md` (+109).
- **Deletions present: 109 lines total across 5 files.** Earlier snapshots: T1 (~02:31) showed 10 deletions in 4 files (capture-binding-check.py unmodified); T2 (~02:33) showed 100 in 5 files (487/87 capture-binding). The tree moved between snapshots — in-flight seat edits landing.

Deletion classification (each mapped to frozen-claim text in `.ufo/waves/round-34/claims.json`):

| File | −lines | Deleted content (from `git diff 014ee2d`) | Sanctioned by |
|---|---|---|---|
| SCORECARD.md | 3 | the two `` `<LANE_HASH>` `` marker bullet lines ("the L1 replaces this marker…", "Round-33 final lane commit: `<LANE_HASH>`…") | C1 before/after: "SCORECARD.md carries 2 <LANE_HASH> markers (R1)" → "count 0 + appended correction naming 7963976e/014ee2d (R1)". Verified: `grep -c '<LANE_HASH>' SCORECARD.md` → **0**; + side carries `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1)`. |
| corpus/instruments/capture-binding-check.py | 87 | old docstring/rules text ("The round-33 C1 counter…", rule A/B/C prose, output-format lines) rewritten for the hardened selftest | C1: selftest must reach N>=19 with named new cases (per-file binding, nested dir, strict-UTC, dup-record, dual-https row, rejected anchor, summary-only rejection). Worktree sanity run: `python3 corpus/instruments/capture-binding-check.py --selftest` → `selftest cases=23 failures=0`, exit 0. |
| corpus/instruments/frontier-recheck-count.py | 15 | old one-directional rule-A docstring lines ("no cross-entry credit, no dropped id", "must select a superset of the header ids (nothing dropped)…") | C1: "frontier-recheck-count.py rule A enforces both directions (R9)". Verified in worktree: `frontier-recheck-count.py:205` `declared_set.issubset(set(recheck_ids))` guard and `:207` `set(recheck_ids).issubset(declared_set)` guard — both directions enforced. |
| corpus/source-snapshots/round-26/manifest.json | 1 | old `purpose` line | C1: "S040-live.txt has a manifest record or explicit orphan listing; round-26 manifest purpose text corrected (R6)". + side adds `"orphans": [ { "path": "S040-live.txt", … "fetched_utc": "2026-10-25T12:34:27Z" } ]`. |
| corpus/source-snapshots/round-32/manifest.json | 3 | old `purpose` line + two `"fetched_utc": "2026-10-25T23:14:00-03:00"` records | C1: "round-32 manifest carries only strict-UTC fetched_utc instants (R8)". Verified: both `fetched_utc` now `"2026-10-26T04:16:06Z"` / `"2026-10-26T04:16:16Z"` (Z-suffix). The one remaining `-03:00` hit in the file is inside the `purpose` **prose** ("author time 2026-10-25T23:14:00-03:00" describing capture commit 288ea9ac), not a `fetched_utc` field — claim wording ("only strict-UTC fetched_utc") holds. |

**Axis A verdict:** no unauthorized deletion. Every deleted line is (i) the `<LANE_HASH>` marker removal the frozen C1 kill rule requires, or (ii) replacement text/data inside the two instruments and two manifests whose modification the frozen C1 claims themselves mandate. All corpus record files (lessons, QUALITY, SOURCES, instruments/README) are strictly append-only. Caveat: numbers are in-flight snapshots (see caveat above); the L1 re-measures at commit time.

### B. anchorcheck — `python3 corpus/instruments/anchorcheck.py SKILL.md`

Exit 0. Summary line:

```
== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

- Failure classes per the instrument's own definition (`anchorcheck.py:16-21`: MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT): **all 0** ("0 bad", exit 0).
- `LOST-RECORDED=306` is the recorded-not-fail class (`anchorcheck.py:24-27`: "deliberately non-openable historical anchor … NEVER a fail class") and matches the historical baseline (round-21 records in `.ufo/` show the same 306, e.g. `.ufo/continuations/round-21.md:111`).

**Axis B verdict:** failure classes 0. Pass.

### C. Density — `python3 corpus/instruments/density.py SKILL.md`

Exit 0. Output tail: `SKILL.md (1090 lines, 25 blocks)` … `| | **mean dens** | | | | | | | | **201.7** |` and `Total path-citation instances: 710 across 25 blocks.`

- **Mean dens = 201.7 — exactly the round-33 baseline of 201.7; not below by any amount.** Expected identity: `SKILL.md` is byte-unchanged from base (absent from the numstat diff), so the census reproduces the round-33 value. Measured anyway, as assigned.

**Axis C verdict:** density mean 201.7 (actual), ≥ round-33 201.7. Pass.

### D. Fleet root — no new lost-base/misroot files authored by this round

Method: `find /home/vgpnk/Projects/shokunin -maxdepth 1|2 -newermt <cutoff> -printf …` with cutoffs at 2026-10-26 00:00 (whole-day) and 02:29:48 (wave-1 dispatch commit time); `git -C /home/vgpnk/Projects/shokunin status --porcelain` and `ls-files` for tracked/untracked classification. Fleet root only read, never written.

Findings:

1. **`/home/vgpnk/Projects/shokunin/baseline-plain.txt` — misrooted round-34 artifact (finding).**
   - stat: `mtime=2026-10-26 02:37:04.340777462 -0300 size=850`; untracked (`git ls-files --error-unmatch` → "did not match any file(s) known to git"); sha256 `56f08a92037cc2520dc89f23f4acd0fdffc4a9331796e7cfbff7c534263a6038`.
   - It did not exist at my 02:35–02:36 sweep and appeared at 02:37:04 — **created during the wave**, seconds before my final sweep. The fleet-root dir mtime changed at 02:37:04.315 and the kasegi lane dir at 02:37:04.345 (same second).
   - Content is a `capture-binding-check.py` AUDIT baseline: per-round `MANIFEST round-N records=…` lines, `AUDIT records=41 … orphans=1 orphan=S040-live.txt`, and the pre-fix failure `FAIL rule=no-row record=S051 dir=round-34` / `records=41 bound=40 unbound=1` — i.e. a **before-state capture of the C1/C2 instrument** (S051 not yet in the registry at capture time).
   - Classification: **misroot** — a round-34 lane artifact written at the fleet root, which is read-only to lane seats; per seat rules it belonged in the author's `/fast/scratch/hyaku/kasegi-r34/<seat>/` or the lane's `.ufo/waves/round-34/`. Content harm: none (new 850 B file, nothing overwritten, fleet repo untracked). Process harm: a write outside lane write scope by some round-34 participant.
   - Authorship: not provable from the filesystem. [INFERENCE] author is a round-34 wave participant capturing C1/C2 before-evidence (candidate profiles: the C1/C2 before-after/regression seats or the L1's census-before step); 31 seat scratch dirs exist under `/fast/scratch/hyaku/kasegi-r34/` (ExecBeforeReceipts, ExecCensusAfter, ExecDoNothingReject, ExecFrontierBidirectional, ExecHarnessAfter, ExecNoHarmFinal, ExecRDefectClosureSuite, ExecRegistryAppend, ExecRegressionC1, ExecRegressionC2, ExecS040Orphan, ExecSnapshotR34, MutCaptureBindingLimbs, MutKillRuleMutants, RevC1BeforeAfter, RevC2BeforeAfter, RevCensus, RevClaimsFreeze-2, RevEntryF17, RevKillRule, RevNoHarm, RevRSuite, RevRowS051, ScoutDatawalk, ScoutQuarantine, ScribeAssimilationGate, ScribeEntryF17, ScribeLesson, ScribeQualityDraft, ScribeReportDraft, ScribeScorecard, ScribeShonen), so scratch space was available and used — the fleet-root write is a deviation, not a necessity. The L1 can attribute from its dispatch log and should remove the file or have the author re-root it.
2. **Two empty untracked directories at the fleet root: `156.0.8078.47/` and `154.0.8037.97/`** (Chromium-version-named, `total 0`, zero files, mtime 2026-10-26 02:11). They **predate the round-34 freeze (02:28:39) and dispatch (02:29:48)**, so they are not wave-seat authorship; likely tool droppings from dispatch prep or another lane. Zero-byte dirs, no content harm. Reported as an observation for the L1's fleet-root sweep, not a round-34 defect.
3. **Post-dispatch sweep (cutoff 02:29:48, excluding `.git`, `.jj`, `.tower`, `.ufo`, `.scratch`, `.omp`, lane dirs):** only `MANIFEST.json` (02:35:20, fleet bookkeeping at dispatch), the fleet `.git`, and `baseline-plain.txt` above. No other new files at the fleet root during the wave.
4. Fleet-root tracked files (`SCORECARD.md`, `README.md`, `LOG.md`, `AGENTS.md`, `.gitignore` — 02:27) and `.scratch/goal-20261026-hyaku-run8.md` (staged) are fleet-level bookkeeping around the hyaku run-8 dispatch, in the fleet's own convention — not lane files misplaced.
5. The kasegi lane's own new files are all correctly rooted inside the lane (untracked: `.ufo/waves/round-34/{assimilation,wave1,wave1.ready,claims-erratum-1.md}`, `corpus/instruments/r-defect-closure.sh`, `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, `corpus/source-snapshots/round-34/`).

**Axis D verdict:** one finding — `baseline-plain.txt` misrooted at the fleet root during the wave (content-harm-free, scope violation, author unattributable from filesystem). No lost-base files introduced; no other misroot files.

### E. Verdict

**No-harm: HOLDS on the production corpus, with one process finding.**

- Append-only: all corpus record files strictly append-only; `SKILL.md`/`PROVINCE.md`/`LOG.md` untouched; the 109 deleted lines across 5 files are exactly the frozen-C1-mandated marker removals, instrument hardening and manifest data corrections (each verified landed: `<LANE_HASH>`=0, strict-UTC fetched_utc, rule-A both-directions guards at `frontier-recheck-count.py:205,207`, S040 orphan record, capture-binding selftest `cases=23 failures=0`).
- anchorcheck failure classes 0 (exit 0; LOST-RECORDED=306 is recorded-not-fail and equals the historical baseline).
- Density mean 201.7 = round-33 baseline, not below.
- Fleet root: no lost-base files; one misroot finding (`baseline-plain.txt`, 850 B, untracked, during-wave, sha256 above) for L1 attribution/removal; two pre-round empty version dirs as observation.

### F. Residual risks / verification gaps

1. **Live working tree:** 65 seats edit the shared tree concurrently; numstat moved between my 02:31/02:33/02:37 snapshots (frontier-recheck-count.py deletions 3→9→15; capture-binding-check.py 0→87). The L1 MUST re-run `git diff --numstat 014ee2d -- SKILL.md PROVINCE.md corpus SCORECARD.md LOG.md` at integration and re-classify any deletion that appeared after 02:37:41.
2. Authorship of `baseline-plain.txt` is inferred, not proven; the L1's dispatch log is the attribution source.
3. I ran only the capture-binding selftest as a worktree sanity check; `r-defect-closure.sh`, `kill-rule-check.py` and the C2 harness are C1/C2 seats' items and were not exercised here (no-harm axis only).
4. The two empty Chromium-version dirs predate the freeze; if the L1's round-34 prep authored them at 02:11, they are still worth sweeping (zero-byte, untracked).

### G. Seat hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r34/RevNoHarm/` was created (mkdir -p) but never written to; deleted before yielding (`rm -rf`). No tree left on disk.
- No tools installed (none needed); no pacman use; no subagents; no `agent://all`; no writes outside the lane except none — the fleet root was only read.
