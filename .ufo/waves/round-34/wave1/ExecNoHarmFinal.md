# ExecNoHarmFinal — round-34 no-harm sweep on the landed bytes

Seat: `ExecNoHarmFinal` (executor, leaf). Round: kasegi-shokunin round 34, hyaku run 8.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope). Lane base
`014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`.

Write scope exercised: **this receipt only** (`.ufo/waves/round-34/wave1/ExecNoHarmFinal.md`) plus
scratch under `/fast/scratch/hyaku/kasegi-r34/ExecNoHarmFinal/` (removed before yield). No lane
content file touched; no `git add`/`commit`/`push`, no `jj` invocation, no `pacman`/install, no
network fetch. Read-only git plumbing used: `rev-parse`, `status`, `diff`, `show`, `ls-files`,
`log`, `merge-base --is-ancestor`.

## Report

### 0. Capture point and provenance

Sweep trigger: four bounded polls of the wave report dir and the working-tree content signature
(`until`-style loops with caps; logs `poll1..poll4` in scratch, figures inlined below). Poll
timeline (UTC): `05:33` 1 receipt → `05:44` 40 → `05:50` 55 → `06:05` 64 → `06:07:54` **SETTLED**
(content signature stable 120 s, `corpus/lessons/round-34.md` present).

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && date -u +%FT%TZ; git rev-parse HEAD
2026-10-26T06:08:02Z
206e5108f1190e61b3e2622d21cab8a5d921650c
$ ls .ufo/waves/round-34/wave1/*.md | wc -l
64
```

- Lane tip is **`206e510`** (the spec/dispatch commit) and **did not move during the sweep**: the
  whole wave's content is uncommitted working-tree state; the L1 commits at integration. So "landed
  bytes" below = base `014ee2d` → working tree at `06:08Z`, with `HEAD` as the read-only anchor.
- 64 of 65 seat receipts present; the missing one is **this seat**. 63 match the 65-name roster
  exactly; the 64th is `wave1/ScribeReportDraft-2.md` (§4.4).
- Repo roots distinct: `lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
  `fleet=/home/vgpnk/Projects/shokunin`.
- **Post-capture re-read** at `06:12:04Z`, after this receipt was written: the content signature is
  byte-identical to capture (`7ffb2c7e` over `git status --porcelain -uall` minus the wave dir),
  `SKILL.md` is still `b11b6085…3ed84`, `SCORECARD.md` still `efa646c8…37e91`,
  `grep -c '<LANE_HASH>' SCORECARD.md` still 0, and the wave now holds all **65** receipts. Nothing
  measured here moved after capture.

### 1. `density.py SKILL.md` — identical to the round-33 record, exit 0

```
$ python3 corpus/instruments/density.py SKILL.md; echo exit=$?
# Density census — SKILL.md (1090 lines, 25 blocks)
| | **mean dens** | | | | | | | | **201.7** |
Total path-citation instances: 710 across 25 blocks.
exit=0
```

Comparison to the round-33 record — **mean 201.7, 25 blocks, 710 cites, i.e. exact equality** — and
the two records of that figure are `corpus/lessons/round-33.md:116` (`mean dens **201.7** (710 cites /
25 blocks, exit=0)`) and `SCORECARD.md:1003` (the round-33 `depth:density` row; round 34's row is at
`SCORECARD.md:1145`). Exact equality is not a coincidence and not a re-measurement of different
bytes: `SKILL.md` is **byte-identical to base** (§3), digest
`b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`, which is also the digest the
round-33 record names. Base bytes were re-measured on a scratch copy, same instrument:

```
$ git show 014ee2d:SKILL.md > $S/SKILL.base.md && sha256sum $S/SKILL.base.md
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  .../SKILL.base.md
$ python3 corpus/instruments/density.py $S/SKILL.base.md --label r34-base | tail -2
| | **mean dens** | | | | | | | | **201.7** |
Total path-citation instances: 710 across 25 blocks.     # dens_exit=0
```

**Verdict: no harm.** Same file bytes, same instrument bytes (§6.1), same mean, same block and
citation counts.

### 2. `anchorcheck.py SKILL.md` — every failure class 0, exit 0

```
$ python3 corpus/instruments/anchorcheck.py SKILL.md; echo exit=$?
== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors;
   LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
```

- Full stdout kept at scratch `anchor-final.txt`: **306** `LOST-RECORDED` lines, and the fail-class
  buckets are `PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` with `0 bad` — the exact vector
  the assignment names, and the same vector as base:
  `KASEGI_LANE_ROOT=$PWD python3 corpus/instruments/anchorcheck.py $S/SKILL.base.md` → identical
  header line, `anchor_base_exit=0`.
- Exit is the verdict, not the print (README round-28 amendment): `exit=0`.
- Note (reproduced, not a defect): piping the instrument into `head` yields `exit=1` from SIGPIPE,
  not from a verdict — observed once here and recorded the same way at
  `wave1/ScribeSkillGate.md:242-244`. Every exit code quoted in this receipt is unpiped.

**Verdict: no harm.** In-range 12 and LOST-RECORDED 306 on both sides; nothing moved.

### 3. `git diff --numstat <base>` on the assigned set — append-only, with one disclosed exception

```
$ git diff --numstat 014ee2d -- SKILL.md PROVINCE.md corpus/README.md corpus/SOURCES.md \
      corpus/QUALITY.md SCORECARD.md LOG.md; echo numstat_exit=$?
155	3	SCORECARD.md
15	0	corpus/QUALITY.md
26	0	corpus/README.md
5	0	corpus/SOURCES.md
numstat_exit=0
```

Absent from the output = 0/0 insertion/deletion: `SKILL.md`, `PROVINCE.md`, `LOG.md`. So
**6 of 7 files are pure-append (0 deletions)**; `SKILL.md`/`PROVINCE.md` are unchanged by
construction (`wave1/ScribeSkillGate.md:10`: "`SKILL.md` and `PROVINCE.md` were not written"), and
`LOG.md` is the L1's closing file and has not landed yet (§7.1).

`SCORECARD.md` carries **3 deletions**, and they are exactly the frozen C1 R1 subject — the two
`<LANE_HASH>` placeholder sentences:

```
$ git diff -U0 014ee2d -- SCORECARD.md | grep -E '^-' | grep -v '^---'
-`<LANE_HASH>`** — the L1 replaces this marker; the wave-1 value above is the commit the
-after-column seats measured, not the closing commit. Receipts land under
-**Round-33 final lane commit: `<LANE_HASH>`** — the L1 replaces this marker. Every value in
```

Replacement (same hunks) plus the appended correction:

```
+`7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1); the wave-1 value above
+is the commit the after-column seats measured, not the closing commit. Receipts land under
+**Round-33 final lane commit: `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1). Every value in
+Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33
+final hash `7963976e60b2564860553c6ab4838128d5ca06ea` (lane tip `014ee2d7…228c`
```

Sentence-text survival checked on the final file: `not the closing commit` → 1 hit,
`after-column seats measured` → 1, `Receipts land under` → 5; the only phrase that disappears is the
placeholder grammar `the L1 replaces this marker` (0 hits), replaced by `(filled in round 34, R1)`.
**No sentence was lost; 3 lines were rewrapped.** Marker count on the final file:

```
$ grep -c '<LANE_HASH>' SCORECARD.md
0
```

(2 at base and at `HEAD`: `git show 014ee2d:SCORECARD.md | grep -c LANE_HASH` → 2, same at
`29f606d` and `HEAD`.) The token still appears in 30 other `*.md` files, every one of them
historical prose or the round-34 evidence text itself (e.g. `corpus/lessons/round-34.md:71` is a
gate row *about* the count reading 0) — none is an unfilled placeholder in `SCORECARD.md`.

**Verdict: append-only holds for 6/7; `SCORECARD.md`'s 3 deletions are the frozen claim's required
R1 replacement (placeholder lines → real hash + appended correction), classified as disclosed, not
content loss.** If the L1 wants the strict "0 deletions" literal to hold on all seven, that is
impossible for SCORECARD.md without leaving the markers in place — flagged as a claim-literal
tension, not a harm.

### 4. `git status --porcelain` in the lane — no stray files at capture

Every changed path classified against the frozen roster
(`.ufo/waves/round-34/wave1-spec.json`, 65 names) with a read-only classifier over
`git status --porcelain -uall` + `git diff --name-status 014ee2d`:

```
== summary seat_receipt=63 seat_evidence=10 wave_other=30 content=13 content_new=6
            seat_unexpected=0 l1_scaffold=0 stray=0
```

- `content` 13 = **12 lane content paths** (`SCORECARD.md`, `SHONEN.md`, `corpus/QUALITY.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/README.md`,
  `corpus/instruments/capture-binding-check.py`, `corpus/instruments/frontier-recheck-count.py`,
  `corpus/lessons/round-29.md`, `corpus/lessons/round-33.md`,
  `corpus/source-snapshots/round-26/manifest.json`, `corpus/source-snapshots/round-32/manifest.json`)
  plus **one prior-round receipt**, `.ufo/waves/round-33/wave1/ScribeReportDraft.md`, amended
  append-only: `37 0`, a late-state appendix whose own header says "earlier text left byte-identical".
- `content_new` 6 = `corpus/instruments/kill-rule-check.py`, `corpus/instruments/r-defect-closure.sh`,
  `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, `corpus/lessons/round-34.md`,
  `corpus/source-snapshots/round-34/S051.txt`, `corpus/source-snapshots/round-34/manifest.json` —
  each an expected C1/C2 landing, all inside declared lane trees.
- `seat_evidence` 10 = per-seat evidence directories under `wave1/` (`ScribeSkillGate/`,
  `RevC1BeforeAfter/`, `SentCred/`, …). Same advisory class round 33 filed as ownership drift.
- `wave_other` 30 = `.ufo/waves/round-34/**` L1 scaffolding, `assimilation/`, `claims-erratum-1.md`,
  `wave1.ready`, `wave1.ready.dispatched`, `wave1/swarm-registry.json`.
- Junk-name scan for `*.orig *.rej *.bak *~ *.swp *.tmp core.*` over the whole lane:
  `junk_count=0`.

**4.1 The one stray this sweep actually caught — and its disposition.** At `05:37:05Z`
`selftest-baseline.txt` (1552 B, sha256 `ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51`,
24 lines of `capture-binding-check --selftest` output) sat untracked at the **lane root**. It was
independently flagged by three seats before I reached it (`wave1/RevC1BeforeAfter.md:238-243` F5,
`wave1/CritMistakes.md:247-251` M34-4, `wave1/ScribeAssimilationGate.md:367-368`). At capture:

```
$ git ls-files --error-unmatch selftest-baseline.txt
error: pathspec 'selftest-baseline.txt' did not match any file(s) known to git   # exit 1
$ ls -la selftest-baseline.txt
ls: cannot access 'selftest-baseline.txt': No such file or directory
```

A digest hunt over `.ufo/waves/round-34/` and `/fast/scratch/hyaku/kasegi-r34` for
`ca3759d1…` found **no copy**: the file was deleted, not relocated. **Stray count at capture: 0.**
The file's evidence value is not lost — the landed instrument's own `--selftest` reproduces it and
`RevC1BeforeAfter.md` quotes the same baseline.

**4.2 Non-roster receipt name.** `.ufo/waves/round-34/wave1/ScribeReportDraft-2.md` is a second
receipt from the `ScribeReportDraft` seat, outside the `<Seat>.md` naming convention. Receipt-shaped,
inside the wave dir, no content risk: naming observation only.

### 5. Fleet root — no kasegi seat wrote outside the lane

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -i kasegi
 M .ufo/state/kasegi.report-baseline        # harness baseline, one per lane (16 exist)
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | awk '{print $1}' | sort | uniq -c
      2 ??
    157 A
     19 M
```

- The 19 `M` are the 16 `<lane>.report-baseline` harness files plus `.ufo/watchdog.log`,
  `scripts/hyaku/hyaku.env`, `scripts/hyaku/lane-addendum.md` — harness/L1 state, not seat writes.
- The 2 `??` are `.ufo/reports/round-38/kengaku.md` and `.ufo/state/disk-guard.log`; **0** `A`
  entries exist outside `.tower/` and `.scratch/` (both pre-date this round).
- New-file scan of the whole fleet root since wave start (`05:29:00Z`), grouped by top-level:
  `tsukuroi-shokunin 703, souji-shokunin 553, kengaku-shokunin 463, tabi-shokunin 331,
  kasegi-shokunin 117, kaidoku-shokunin 57, .ufo 20, chousa-shokunin 6, MANIFEST.json 1`.
  Every non-lane path is **fleet-root/harness material for other lanes**: `.ufo/prompts/{kaidoku-37,
  kaidoku-38,souji-30,souji-31,tabi-29,tabi-30,tsukuroi-39}.md`, `.ufo/prompts/closure/*`,
  `.ufo/reports/{round-29/tabi,round-30/souji,round-37/kaidoku,round-37/kengaku,round-38/kengaku}.md`,
  `.ufo/state/*`, `.ufo/watchdog.log`. `MANIFEST.json` (mtime `06:00:22Z`, 2 010 023 B) shows **no
  content delta**: `git status --porcelain -- MANIFEST.json` is empty, i.e. the rounds-ledger rewrite
  reproduced HEAD bytes.
- 117 kasegi files newer than wave start at the `06:08:35Z` scan (176 at the `06:09:48Z` re-scan, as the
  last receipts landed) — all inside this lane (`kasegi-shokunin/**`: receipts, the content paths
  above, and `$HYAKU_SCRATCH`-free evidence). **No kasegi-seat misroot write found; nothing for the L1
  to sweep except the stray already deleted at §4.1.**

### 6. Supplementary read-only checks (not in the assigned five)

**6.1 The measurement instruments are byte-identical to base** — so §1/§2 are comparable to the
round-33 record, not a different ruler:

```
corpus/instruments/density.py      base=ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710  same=yes
corpus/instruments/anchorcheck.py  base=d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912  same=yes
$ git diff --name-only 014ee2d -- corpus/instruments/
corpus/instruments/README.md
corpus/instruments/capture-binding-check.py
corpus/instruments/frontier-recheck-count.py
```

Only the two **owned** instruments the round is chartered to change (`ExecCaptureBindingHarden`,
`ExecFrontierBidirectional`) plus the instrument README appear.

**6.2 Whole-tree deletion table** (every file with deletions, base → worktree), each classified:

| file | +/− | class of the deletions |
|---|---|---|
| `SCORECARD.md` | 155/3 | R1 placeholder lines → real hash + correction (§3) |
| `SHONEN.md` | 56/31 | rewrite-in-place of superseded round-33 evidence (§6.3) |
| `corpus/instruments/capture-binding-check.py` | 487/87 | owned instrument hardening (C1) |
| `corpus/instruments/frontier-recheck-count.py` | 220/15 | owned rule-A bidirectional rewrite (R9) |
| `corpus/source-snapshots/round-26/manifest.json` | 12/1 | R6 `purpose` text: the "S040 skipped" sentence replaced by the orphan listing |
| `corpus/source-snapshots/round-32/manifest.json` | 3/3 | R8 strict-UTC: 2 × `"fetched_utc": "2026-10-25T23:14:00-03:00"` → strict-UTC, plus the `purpose` sentence carrying the offset |

No other path in the lane has a nonzero deletion count (`git diff --numstat 014ee2d | awk '$2>0'`).

**6.3 `SHONEN.md` deletions are the document's established rewrite-in-place pattern, and no fact is
lost.** 42 → 67 lines; the deleted block is the round-33 `— evidence (round 33, …)` paragraphs
(…`density.py SKILL.md` prints mean dens 201.7 over 25 blocks and 710 path-citation instances…,
the LOG/`recheck-audit`/`PROVINCE` evidence lines). The same file moved `31 31` between `9f98488` and
`014ee2d` — i.e. round 33 replaced round-32 evidence the same way. The superseded figures survive in
their permanent records: `201.7` appears 2× in `SCORECARD.md` and 1× in `corpus/lessons/round-33.md`.

**6.4 New content carries no scratch paths-as-evidence and no secrets.** `grep -n
'/fast/scratch|HYAKU_SCRATCH'` over the 6 new content files + the 4 modified prose files returned 8
hits, **all** of them legitimate code/environment references (`kill-rule-check.py:388-392,424,688`
scratch-root resolution; `r-defect-closure.sh:52,750` `$HYAKU_SCRATCH` default; one SCORECARD
instrument row documenting the same default). No captured-evidence path points into
`/fast/scratch`. Secret shapes (`PRIVATE KEY`, `ghp_…`, `Authorization: Bearer`, 12+ char
`api_key=`) in the 6 new files: **0**.

**6.5 Final digests (sha256), captured `06:08-06:10Z`.**

```
7-file assigned set
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  SKILL.md      (= base)
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md   (= base)
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md
77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8  corpus/QUALITY.md
efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91  SCORECARD.md
e69e7b67227ada97cb02ab1735df5c13fe23146e2c510afed22f8e1b32af184c  LOG.md        (= base, L1 not yet)
other changed / new content
6d80dfd46940afec65e975cbfdd8a6d8e76e3a609f8d7bcf91446e3773e62fb9  SHONEN.md
c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61  corpus/instruments/kill-rule-check.py
809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d  corpus/instruments/r-defect-closure.sh
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
d021b317d2bad47d35d866617962906211df642730bc0f1c3849d4224ac19907  corpus/instruments/README.md
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
73b8bdbb400f83903113c9372984120001bfdc2f56d4b6a95b73b1c6ca14014c  corpus/lessons/round-34.md
4afb96be18355cd958f9ddccc4f9687c2c2afa4b2747d49f687add956484ecce  corpus/lessons/round-29.md
f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807  corpus/lessons/round-33.md
33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa  corpus/source-snapshots/round-26/manifest.json
72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6  corpus/source-snapshots/round-32/manifest.json
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
```

Base-side digests of the assigned set for the diff above: `SKILL.md b11b6085…3ed84`,
`PROVINCE.md b57de5d9…abd679`, `corpus/README.md 3779e77f…f754932`, `corpus/SOURCES.md
b22c7f01…44d13b`, `corpus/QUALITY.md 00781e09…0b087`, `SCORECARD.md e03fbefa…12aff3`,
`LOG.md e69e7b67…2af184c`.

### 7. Risks and open items for the L1

1. **`LOG.md` has not landed** (`0 0` at capture, digest equal to base). The round-34 `## Round 34`
   entry is the L1's closing edit, as every round; it is not a seat defect, but the append-only row
   for `LOG.md` is vacuous until it lands and must be re-read post-integration.
2. **`PROVINCE.md` amendment owed at integration.** `wave1/ScribeSkillGate.md:241` reports
   "`PROVINCE.md` amend-warranted at integration (§4a)" while leaving the file byte-identical
   (`b57de5d9…`). An L1 edit there would add to the `numstat` row this receipt reports as `0 0`.
3. **`SCORECARD.md` cannot be both 0-deletions and R1-fixed.** Its 3 deletions are the placeholder
   sentences; the claim's R1 fix *requires* them. Disclosed and quoted in §3 — the L1 should decide
   whether "append-only (0 deletions)" applies literally to `SCORECARD.md` or is satisfied by
   "placeholder replaced in place + correction appended".
4. **`SHONEN.md` deletions (31)** are outside my assigned seven and follow the document's
   rewrite-in-place pattern (§6.3); recorded so the L1 can confirm the convention rather than
   discover it at integration.
5. **Two advisory, non-content observations:** a non-roster receipt name
   (`wave1/ScribeReportDraft-2.md`, §4.2) and ten per-seat evidence directories under `wave1/`
   (§4), the same ownership drift round 33 filed.
6. **Not my verdict:** the claim-side findings that other seats already filed — notably
   `wave1/CritMistakes.md:26` on M34-2 ("2 of 3 corpus occurrences survive") and the missing M34-3
   row. I only measured the `SCORECARD.md` marker count (0) and the 30 surviving prose mentions (§3).
7. **No blocker for this seat:** every assigned command ran and exited as quoted.

### 8. Scratch cleanup

`/fast/scratch/hyaku/kasegi-r34/ExecNoHarmFinal/` (base `SKILL.md` copy, `poll1..poll4` logs,
`density-final.txt`, `anchor-final.txt`, `anchor-base.txt`, `classify.py`, `classify-final.txt`,
`numstat*.txt`, `digests-now.txt`) is removed before yield, after this receipt is written. Nothing
in this receipt depends on a surviving scratch path; every figure is inlined above.
