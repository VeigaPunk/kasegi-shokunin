# SentinelScope — round-42 wave-1 scope-watch receipt

- Seat: `SentinelScope` (sentinel; leaf — no subagent dispatch, no labrat probe used).
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. My writes: this receipt and
  `S=/fast/scratch/hyaku/kasegi-r42/SentinelScope/` only; scratch removed before yield.
- Item: receipt-only scope watch — list `wave1/` at start, re-list every ~10 min, report any file
  outside `<SEATNAME>.<suffix>`+receipt shape, any write outside `.ufo/waves/round-42/wave1/`,
  any sibling/fleet-root touch.
- Window: **T0 2026-10-28T11:02:44Z → T1 2026-10-28T11:29:28Z** (26 m 44 s).
- Sampling: 5 wave1 listings at 30 s (11:03:09–11:05:11Z), then 25 hash+listing snapshots at 60 s
  (11:05:17–11:29:17Z); 28 live process samples at 45 s (11:08:55–11:29:11Z); plus manual re-lists
  between samples.
  Additionally: the executed-command stream of all 66 wave-1 seat session transcripts
  (`~/.omp/agent/sessions/-Projects-shokunin/2026-10-27T07-52-07-309Z_*/<Seat>[-N].jsonl`,
  mtime ≥ 10:58Z) was scanned for write/mutation targets (read-only).

## Verdict (scoped to wave-1 seat writes)

1. **Wave1 shape: 0 violations.** At T1: **84 files = 46 receipts + 37 deliverables + 1 harness
   registry**; every basename resolves to a registered seat (`<SEAT>.md` or `<SEAT>.<suffix>`);
   **0 subdirectories, 0 symlinks/non-regular entries, 0 hidden/temp/backup files, 0 duplicate
   SHA-256 groups, 0 names ever seen then vanished, 0 files with future mtimes, 0 zero-byte files,
   owner uid/gid 1000**. Modes 644 except `ExecJ5Scan.sh`/`ExecJ12J13.sh` 755 (seat chmod) and the
   harness `swarm-registry.json` 600.
2. **Lane writes outside wave1 by a seat: 0.** At T1 `git status --porcelain -uall` outside `wave1/`
   and the pre-wave ready files shows only `.ufo/waves/round-42/build-wave2-spec.py` (L1 wave-2
   builder, 08:06). HEAD moved three times in-window — **all three are L1 commits that each add one
   erratum file** (`27e18d2` +50, `8be06a9` +35, `514ff62` +3 lines); the commit identity is
   `kasegi-shokunin <kasegi@shokunin.local>`, never a seat. **No seat-authored commit exists.**
3. **Frozen inputs byte-identical to T0:** `claims.json`, `c1-controls/do-nothing.txt`,
   `c2-controls/before.txt`, `census-before.txt`, `wave1-spec.json`, `wave1-dispatch.json`,
   `build-wave1-spec.py`, `wave1/swarm-registry.json` — same SHA-256 as my T0 baseline (diff empty);
   `wave1-run.err` remains 0 bytes.
4. **Fleet root: 0 changes vs T0** — status and diffstat identical
   (`M .ufo/reports/round-58/chousa.md`, `?? .scratch/closure-mado-r50.json`,
   `?? .scratch/source-routing-queue.md`, `?? o.bin`; 1 file changed, 10 insertions — all pre-date
   the wave). Harness `.ufo/state/*.log` writes are the dispatcher/guard, not seats.
5. **Sibling lanes: 0 touches attributable to this wave.** Five lanes' HEADs moved in-window; the
   four non-kasegi ones carry their own rounds' subjects (`kaidoku 1e9c4a43 "round-44: freeze-review
   corrections…"`, `souji 2ae0dba "round-35: …"`, `tabi 8c84417 "round-41 w1 spec+ready…"`,
   `tsukuroi 5fdf062f "round-48: land inherited r47 leftovers…"`). No executed wave-1 command
   resolved a write target into a sibling lane, `shokuknow`, the fleet root, a PATH dir, or the
   operator config.
6. **Scratch binding: 1 violation (F-1)** — `ExecSuiteCore` created and left
   `/fast/scratch/hyaku/kasegi-r42/tmp-timing` (298 MB) outside its own seat dir, and pointed the
   suite's `--scratch-root` at the shared parent.
7. **Freeze/provenance defects: F-2, F-3, F-4** (below). F-2 was independently re-found by the L1 and
   corrected out-of-band in `claims-erratum-3` (commit `514ff62`) before T1; F-3 and F-4 were still
   open at T1.
8. **Coverage limit at T1:** 18 of 64 seats had not yet written a receipt
   (`ExecControls, ExecJ10Isolate, ExecJ12J13, ExecJ1Evidence, ExecJ2Token, ExecJ3Registry,
   ExecJ4Decl, ExecJ5Scan, ExecJ6Bind, ExecJ7Flip, ExecJ8Receipt, ExecJ9NegCtl, ExecReplayHarness,
   ExecSelftest, ExecSuiteCore, ScribeC2Gate, SentinelMisroot, SentinelScope(self)`) — they were
   still running; their later writes fall outside this window. Assertions above are exact at T1.
9. **Cross-lane notice:** received `TsukuroiR48`'s STOP declaring tsukuroi round-48 `w1.ready`
   invalid. I am not a tsukuroi seat, touched no tsukuroi path, and surfaced the STOP here so no
   kasegi-side consumer treats it as live.

## Findings

### F-1 — [high for the Y receipt run] Scratch-binding violation: shared-root work dir left behind
**What.** `ExecSuiteCore` ran the r41 suite with `--work /fast/scratch/hyaku/kasegi-r42/tmp-timing`
and `--scratch-root /fast/scratch/hyaku/kasegi-r42` (the shared parent of all 64 seat dirs), then
never removed the work dir. At T1 the directory is 298 MB and holds
`export/` (a full lane export), `neg-base/`, `mut/`, `selftest-lines.txt` (0 B), and `payloads.tsv`.
**Exploit path.** (a) The assignment binds every seat to `S=/fast/scratch/hyaku/kasegi-r42/<SEAT>/`
and says "a seat whose scratch dir survives is a defect" — this dir has no seat name and survives.
(b) The L1's own `claims-erratum-1` E4 says the receipt run executes the suite with
`--scratch-root /fast/scratch/hyaku/kasegi-r42` and that "any leftover seat dir under that prefix
… is a red stray and must be cleaned before the receipt run". `tmp-timing` sits exactly under that
prefix; if it is still present when J13/J5 run at Y, the quiescence/scan limb sees a stray that is
not the run's own `--work` dir. (c) The seat's own later timing runs against the shared root record
the consequence: its final `payloads.tsv` line is
`I6  strays=46,read=fail,scanned=46  0` — the r41 scan could not even read the 46 sibling dirs under
that root. The F-SCAN class the r42 suite repairs is exactly this state, produced by a wave-1 seat.
**Evidence.**
- Executed command (transcript `ExecSuiteCore-2.jsonl`, tool call at `2026-10-28T11:02:54.795Z`,
  intent `Timing the r41 suite run`): `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && time bash
  corpus/instruments/r41-closure.sh --export-ref 1f7464612ac4c44e39886b82e812610d3c039b13
  --work /fast/scratch/hyaku/kasegi-r42/tmp-timing --scratch-root /fast/scratch/hyaku/kasegi-r42
  2>&1 | tail -30; echo "EXIT=$?"` (the session store truncates the tail; both arguments are visible).
- The seat's own reasoning at `2026-10-28T11:11:51.297Z`: "…it also created
  /fast/scratch/hyaku/kasegi-r42/tmp-timing (outside my seat scratch — oops, that's the fleet
  scratch area; I must clean it up … I'll remove /fast/scratch/hyaku/kasegi-r42/tmp-timing at the
  end." At T1 it had not.
- Process evidence: 24 samples, 47 distinct `--work/--scratch-root/--root` pairs — 40 seat-scoped,
  and exactly 3 offending, all this run: `--scratch-root /fast/scratch/hyaku/kasegi-r42` (54
  samples), `--work …/tmp-timing` (30), `--work …/tmp-timing/neg-base` (18). Every other process in
  every sample used a `<SEAT>`-scoped path.
- Filesystem at T1: `mtime=2026-10-28 08:04:48 -0300`, `du -sm` = 298, `payloads.tsv` =
  `I1 …closed=1 / I3 …closed=1 / I4 …closed=1 / I5 …closed=1 / I6 strays=46,read=fail,scanned=46 0 /
  I7 …closed=1`.
- Post-T1 confirmation (independent 5-minute probe at `2026-10-28T11:32:48Z`): wave1 = 88 files,
  scratch entries = 17, **`tmp-timing` still 298 MB**, HEAD still `514ff62`, lane outside wave1 still
  only `build-wave2-spec.py` — the stray was still outstanding 3 m 20 s after T1.
**Impact.** A red J13/J5 at the Y receipt run and 298 MB unreferenced scratch under the prefix the
L1 declares as the receipt scan root; also evidence that at least one "base defeat" measurement in
this round was taken with a non-isolated scan root (`strays=46, read=fail`).
**Smallest remediation.** Remove `/fast/scratch/hyaku/kasegi-r42/tmp-timing` before the receipt run
(and before any J5/J13 transcript is taken); for the remaining pace, `ExecSuiteCore` should use
`S=/fast/scratch/hyaku/kasegi-r42/ExecSuiteCore/` (which it already has, 0 MB at T1) for work dirs
and pass `--scratch-root "$S"`, never the shared parent.

### F-2 — [medium; corrected out-of-band at T1] `claims.json.frozen_at_utc` is future-dated
**What.** `claims.json` declares `frozen_at_utc = 2026-10-28T12:05:00Z`. Observed: file mtime
`2026-10-28T10:51:52.149Z` (`stat -c '%y'` → `07:51:52 -0300`), commit `0566bd6` committer instant
`2026-10-28T11:00:01Z`, first seat write `11:03:09Z`, my observation `11:11Z`. The declared freeze
instant is **+73 min after the file's own bytes, +65 min after the commit that carries it, and
later than the start of the wave it is supposed to precede.**
**Exploit path.** Any ordering predicate that treats `frozen_at_utc` as the pre-data cutoff accepts
every wave-1 artifact as "pre-freeze" and cannot distinguish a claim written before data from one
written after it — the exact guarantee the round's before-controls exist to establish. A verifier
comparing `claims.json` to `stat`/`git show` gets a false statement.
**Evidence.** Table above; precedent that the lane already classes this as a defect: SCORECARD.md
§Round 25 errata 1 — "`frozen_at_utc` in `claims.json` says `2026-10-25T00:00:00Z`; the file's real
creation time is `07:09:47Z` … The date is corrected here". Round-41's own freeze shows the same
pattern (+41 min); round-40's is ~consistent (+95 s), so this is drift, not a house convention.
**Status at T1.** Independently re-found and corrected by the L1 in `.ufo/waves/round-42/
claims-erratum-3.md` (mtime `08:26:33 -0300`, commit `514ff62`, +3 lines): it states the observed
mtime `10:51:52Z` and says the correction "replaces only the inaccurate timestamp label".
**Residual (why it is still reported).** `claims.json` itself is unchanged (`frozen_at_utc` still
`12:05:00Z`) and its own `errata` array is still `[]`; the correction lives only in two sibling
files. A consumer that reads `claims.json` as the authoritative freeze (as the frozen-claims summary
instructs) still sees the false value and no pointer to the errata.
**Smallest remediation.** In the freeze/errata record, cite `claims-erratum-1..3` from
`claims.json.errata` (or state in the report that the errata files supersede the timestamp field);
never let a counter or kill clause compare against `frozen_at_utc`.

### F-3 — [medium] "Frozen" claims were amended three times mid-wave, each amendment derived from wave-1 data
**What.** In-window commits: `27e18d2` (+50 lines, `claims-erratum-1.md`, 08:15:30), `8be06a9`
(+35, `claims-erratum-2.md`, 08:24:48), `514ff62` (+3, `claims-erratum-3.md`, 08:27:22) — all by the
L1, all append-only new files. Erratum-1 is titled "scope clarifications (**pre-data**, pre-scoring)"
and in the same paragraph says it was "Found via wave-1 seat receipts (`wave1/ConnWave2Seed.txt`
items 1, 8, 9, 46-49; `wave1/RevRegistry.md` F1-F3; `wave1/ScoutF25Lead.facts.txt` row-id
suggestion)". Erratum-2 says "No seat had scored a claim when this was written" — but the landable
SCORECARD table with score cells was written at `08:03:44 -0300` (`ScribeScorecard.round42.txt`).
**Exploit path.** A claim whose target can be re-specified after attack seats have measured it is
not frozen in the sense C1/C2's before-controls assert. Concretely, erratum-1 changes C2's concrete
registry after-value to **66** (63 + S064 + S065 + S066) while the *frozen* counting command's
stated expectation remains `63 -> 64`, and `claims.json` still carries `63 -> 64+R`. A verifier
reading only `claims.json` and its counting commands reaches a different after-state than a verifier
reading the errata.
**Evidence.** `git log --oneline 0566bd6..HEAD` (three commits, each `1 file changed, N
insertions(+)`); erratum-1 text quoted above; `python3 -c` over `claims.json` at T1 →
`errata= [] frozen_at_utc= 2026-10-28T12:05:00Z`.
**Impact.** C2's after-state is now ambiguous between `64+R` (claims.json + counting command) and
`66` (erratum-1); wave-1 seats measured under the pre-erratum text. The report must state which text
the final measure uses, and the errata must be discoverable from `claims.json`.
**Smallest remediation.** Land the errata reference into `claims.json.errata` (or a line in the
report naming the three files as operative), and state in the C2 row that the measured after-value
follows erratum-1 E1 (`63 -> 66`) rather than the frozen command text.

### F-4 — [medium; open at T1] Frozen C1 "before" text states a base count that the committed control and an independent seat run both contradict
**What.** `claims.json` C1 `before`: "the r41 suite at base prints `closed=10/12 exit=1`". Observed at
base `5053a7f4…`:
- committed control `.ufo/waves/round-42/c1-controls/do-nothing.txt` lines 15–16:
  `selftest cases=12 failures=8` / `closed=8/12 exit=1`;
- independent seat run `wave1/RevC1Counters.md` lines 80–81: identical `failures=8` / `closed=8/12`;
- the landable SCORECARD row `wave1/ScribeScorecard.round42.txt:28` repeats `closed=10/12` and
  `selftest cases=12 failures=6`, while that scribe's own receipt line 68 records `8/12`.
The value 10/12 belongs to the **r41 judged head** (`0f64b8c5…`), not base — `ConnWave2Seed.txt`
item 11 states the same: "claims.json says the r41 suite at base prints closed=10/12; observed base
is closed=8/12 exit=1 (10/12 is the r41 judged head). Record as an errata before the Y receipt."
**Exploit path.** A verifier checking the `before` column against the committed control finds a
false statement; the landed SCORECARD row then carries a base number that no committed artifact
supports (and a `failures=6` that matches neither base nor the control).
**Impact.** Correctness of the frozen before-state and of the landable table; not a kill-clause
trigger (both values are `<13/13`, `exit=1`), but it is exactly the "named defect present while the
table reads green" class the round exists to close.
**Evidence.** Quoted lines above; `grep -rn '10/12\|8/12\|failures=6' wave1/` shows the split.
**Smallest remediation.** Correct the before text to the base observation (`closed=8/12 exit=1`,
`selftest cases=12 failures=8`) and either label the r41-head figures as such in the SCORECARD row
or drop them from the base cell; do this before Y, since the row is landable bytes.

### F-5 — [info] Observations that are not violations
- `/tmp` residue during the window: `/tmp/r41block.md` 3 437 B (08:03), plus other lanes' small
  files (`d41.txt`, `declared.txt`, `dbg.sh`, `kama-completion-live-*`, squashfs image) — all
  ≤ 6.9 kB, inside the assignment's `<50 MB` allowance; attribution of `r41block.md` unresolved.
- `~/.local/bin`, `/usr/local/bin`, `/usr/bin` contain **no entries newer than wave start**;
  `~/.omp/agent/config.yml` mtime `07:42:12` (pre-wave), `mcp.json` `2026-10-25` — untouched.
- Transient receipt rewrite observed and resolved: `ScribeCorrections.md` (08:13:54) briefly quoted
  the pre-edit digest `77e6d8f1…`/`11 4276` for `ScribeCorrections.blocks.txt`; the seat rewrote the
  receipt at 08:14:21 so it now records the delivered bytes `5a26e1e5…`/`11 4259`. No receipt now
  claims a digest that differs from the delivered bytes (provenance scan at T1: 0 mismatches).
- Executable limbs `ExecJ5Scan.sh`, `ExecJ12J13.sh` are mode 755 (chmod by seat) — expected for
  landed `bash` limbs; no setuid bits anywhere.
- Pattern hits in receipts that I examined and **cleared** (not violations, not writes):
  - 18 `pacman` mentions, all policy statements ("no pacman / pacman paused"): e.g.
    `ExecAssimilation.md:404`, `ExecJ11Corr.md:164-165`, `RevC1Counters.md:134`,
    `RevengerReceipt.md:450`, `ScoutDefeatsR40.md:120`, `ScribeShonenLog.md:132,175`,
    `ScoutF25Lead.md:43`, `ScoutPrecedent.md:103`, `CritKillRule.md:259`.
  - quoted landing forms (describe what the L1 will do, not a seat write): `RevQuality.md:35`,
    `ScribeShonenLog.md:19`.
  - read-only git in transcripts: `git merge-base --is-ancestor` (`ScribeLesson.md:46`,
    `CritReceiptUtc` session), `git rev-parse`/`cat-file`/`archive`/`status`/`diff` — no verb that
    mutates. `git add -A --dry-run` was run **by the peer sentinel `SentinelMisroot`** in the fleet
    root as a read-only probe (dry-run; fleet status unchanged at T1).
  - `--dry-run`/design prose ("…J13's clone", "git status --porcelain") in `SimplifierSuite.md`.

## Evidence appendix (commands and actual output)

E1 — T0 baseline.
```
$ date -u; ls -la .../.ufo/waves/round-42/wave1/
Wed 28 Oct 2026 11:02:44 AM UTC
-rw------- 1 vgpnk vgpnk 29287 Oct 28 07:59 swarm-registry.json
$ git -C .../kasegi-shokunin status --porcelain -uall
?? .ufo/waves/round-42/kasegi-r42-build.ready
?? .ufo/waves/round-42/kasegi-r42-build.ready.dispatched
$ git -C .../kasegi-shokunin rev-parse HEAD
0566bd66e93d429b2df8b6751cf10cbdc391e79b
```

E2 — T1 close snapshot (`CLOSE 2026-10-28T11:29:28Z`).
```
HEAD=514ff62d61ee9bc717a20a02a22c65ec0c5124ed
TREE=6c77f7cd86cafb2f6b97760a8f1a9d551e98bedc
-- lane status excluding wave1+ready --
?? .ufo/waves/round-42/build-wave2-spec.py
-- wave1 dirs --            (empty)
-- wave1 non-regular entries --   (empty)
-- fleet status --
 M .ufo/reports/round-58/chousa.md
?? .scratch/closure-mado-r50.json
?? .scratch/source-routing-queue.md
?? o.bin
-- fleet diffstat --
 .ufo/reports/round-58/chousa.md | 10 ++++++++++
 1 file changed, 10 insertions(+)
```
Frozen diff vs T0 baseline: empty (`FROZEN-INPUTS-IDENTICAL-TO-T0`).

E3 — shape validator at T1 (`validate.py`, reads `wave1-dispatch.json` member set).
```
wave1 files=84 receipts=46 deliverables=37 dirs=0 violations=0
```

E4 — expected-deliverable comparator at T1. Every seat-produced deliverable is named in that
seat's prompt (`seats-writing-deliverables-not-named=0`); only two prompt-named deliverables were
still pending (`ExecJ12J13.transcript.txt`, `ExecJ5Scan.transcript.txt`).

E5 — no deletions/renames in wave1: the 60 s sampler observed 85 distinct names through its last
snapshot; `ever_seen − current = []` (nothing vanished) and the only current file absent from the
sampler is this receipt itself, written after the last sample. Duplicate-hash groups = 0.

E6 — receipt ordering at T1: `receipt-before-deliverable: []` (no seat wrote its receipt before the
last byte of its own deliverables).

E7 — cleanup claims at T1: `receipts claiming scratch removal while dir survives: []`; surviving
scratch = 18 seat dirs (all still-running seats) + `tmp-timing`; sizes 0–3433 MB.

E8 — wave1 growth (60 s hash sampler; file count; all 25 in-window snapshots).
```
11:05:17Z 9   11:10:17Z 26  11:15:17Z 61  11:20:17Z 72  11:25:17Z 79
11:06:17Z 10  11:11:17Z 32  11:16:17Z 63  11:21:17Z 73  11:26:17Z 79
11:07:17Z 13  11:12:17Z 44  11:17:17Z 65  11:22:17Z 74  11:27:17Z 81
11:08:17Z 15  11:13:17Z 50  11:18:17Z 66  11:23:17Z 74  11:28:17Z 83
11:09:17Z 18  11:14:17Z 58  11:19:17Z 71  11:24:17Z 79  11:29:17Z 84
(T1 close snapshot 11:29:28Z: 84 files)
```

E9 — L1 commits in-window.
```
$ git -C lane log --oneline 0566bd6..HEAD
514ff62 round-42: claims-erratum-3 (correct freeze timestamp from file mtime)
8be06a9 round-42: claims-erratum-2 (F-TOKEN boundaries, kill/replay scope)
27e18d2 round-42: claims-erratum-1 (C2 registry count 66, J11/J3/J5/J13/J12 scope clarifications)
$ git -C lane log -1 --format='%an <%ae> %cI' 27e18d2
kasegi-shokunin <kasegi@shokunin.local> 2026-10-28T08:15:30-03:00
```

E10 — freeze-timestamp facts.
```
$ stat -c '%y' .ufo/waves/round-42/claims.json
2026-10-28 07:51:52.149991752 -0300            (10:51:52Z)
$ python3 -c "import json;d=json.load(open('.../claims.json'));print(d['frozen_at_utc'], d['errata'])"
2026-10-28T12:05:00Z []
$ git -C lane log -1 --format='%cI' 0566bd6
2026-10-28T08:00:01-03:00                      (11:00:01Z)
```

E11 — F-4 quotes.
```
claims.json C1 before : "the r41 suite at base prints closed=10/12 exit=1 with the I1
                         evidence-not-named and I3 mangled-token defeats alive"
c1-controls/do-nothing.txt:15-16 : selftest cases=12 failures=8 / closed=8/12 exit=1
wave1/RevC1Counters.md:80-81     : selftest cases=12 failures=8 / closed=8/12 exit=1
wave1/ScribeScorecard.round42.txt:28 : … r41 suite `closed=10/12 exit=1`,
                                       `selftest cases=12 failures=6` …
wave1/ConnWave2Seed.txt:11       : "claims.json says … closed=10/12; observed base is
                                    closed=8/12 exit=1 (10/12 is the r41 judged head)."
```

E12 — ExecSuiteCore attribution (see F-1 for the full quote): tool call `2026-10-28T11:02:54.795Z`,
intent `Timing the r41 suite run`; reasoning admission `2026-10-28T11:11:51.297Z`; 3/47 distinct
flag-path pairs offending across 24 process samples; directory 298 MB at T1 with
`I6 strays=46,read=fail,scanned=46 0`.

## Attribution limits (what this watch can and cannot prove)

- Authorship of a wave1 file is inferred from the filename (seat registry) and, for disputed writes,
  from the seat's session transcript. All wave1 basenames matched a registered seat, and every
  disputed artifact was traced to a named session.
- Writes whose shell target is a variable (`> "$S/..."`, `--work "$W"`) cannot be classified from a
  transcript alone: 62 such targets were seen and left unclassified. The filesystem evidence
  (lane tree clean outside wave1; no untracked non-wave1 file except the L1's two scripts) bounds
  what they could have touched.
- Session stores truncate long command strings (`…` in the JSON), so long heredoc/`cp` commands are
  adjudicated from their visible prefix plus filesystem state; five such flags were cleared on that
  basis, not on a full command text.
- Other lanes were concurrently active in the fleet (kaidoku, souji, tabi, tsukuroi, kama, …). Their
  commits and `/tmp` files are outside this watch and are reported only to show they are not
  kasegi-wave-1 writes.
- I cannot observe read-only accesses that leave no trace; this watch covers writes and mutations.

## Hygiene

- Wrote only: this receipt; `S=/fast/scratch/hyaku/kasegi-r42/SentinelScope/` (samplers, snapshots,
  auditors) — removed before yield. Nothing written to the fleet root, sibling lanes, `shokuknow`,
  PATH dirs, or the operator config; no mutating git/jj anywhere (all my git calls were
  `status/log/rev-parse/show/ls-files/cat-file/diff/archive` on the lane).
- No tools installed or upgraded (none needed); no network fetches; disk guard green at start
  (`/fast/scratch/hyaku` 27 %, 592.6 G free) and not re-checked under load.
- Scratch-binding note for the L1: the shared root currently holds 298 MB of non-seat scratch
  (`tmp-timing`, F-1) in addition to the live seat dirs; that is the set J13/J5 will see if the
  receipt run uses `--scratch-root /fast/scratch/hyaku/kasegi-r42`.
