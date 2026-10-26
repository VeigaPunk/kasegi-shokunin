# ExecNoHarmDensity — no-harm run on depth:density + anchor verdicts (round 31, wave 2)

Seat: ExecNoHarmDensity (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane HEAD at measurement: `eecad59db166e0626ca2472e96ea48bc28a35153` (wave-1 integration). Claims base: `b374febbb33ccadade78a787279707fd5d2e6e1d`.
Answering model route: `opencode-go/deepseek-v4.1-flash` (recorded per bounds item 10; no model passed, route table decided).
Tooling: none installed or upgraded for this seat.

## 0. Bytes pinned at measure time

```
$ sha256sum SKILL.md PROVINCE.md corpus/instruments/density.py corpus/instruments/anchorcheck.py corpus/instruments/resolve.py corpus/instruments/citation-survival.md
817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7  SKILL.md
b42e5fbbbcdd7332ea971d8f9f0500965cc22f485e7766536c488a7e31a96076  PROVINCE.md
ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710  corpus/instruments/density.py
d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912  corpus/instruments/anchorcheck.py
db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667  corpus/instruments/resolve.py
795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d  corpus/instruments/citation-survival.md
$ git status --porcelain -- SKILL.md PROVINCE.md corpus/instruments/density.py corpus/instruments/anchorcheck.py corpus/instruments/resolve.py
(no output)
```

Same-instrument-on-both-sides proof for the before/after columns:

```
$ git diff 5703f9f -- corpus/instruments/density.py | wc -l
0
$ git log --oneline -1 -- corpus/instruments/density.py
eb5b590 round-15: depth re-anchor after PROVINCE-root loss ...
$ git log --oneline -1 -- corpus/instruments/anchorcheck.py
0ab8929 round-29: land C1 selftest completeness/hermeticity + C2 F13 assimilation (v2 wave 64 seats)
```

density.py is byte-identical at r30 and r31; anchorcheck.py identical at r30 and r31.

## 1. depth:density — before/after (no form gaming)

### 1a. Before (r30 SKILL bytes, replayed from commit 5703f9f)

```
$ D=$(mktemp -d) && git show 5703f9f:SKILL.md > "$D/SKILL.md" \
  && python3 corpus/instruments/density.py "$D/SKILL.md" --label r30-replay | tail -6
| 21 | Round-29 Gates & probes registry addition (appended 2026-10-25) | 8 | 5 | 1 | 1 | 5 | 7 | 14 | 280.0 |
| 22 | Round-29 frontier note (appended 2026-10-25) | 5 | 2 | 2 | 0 | 1 | 1 | 4 | 200.0 |
| 23 | Round-30 Gates & probes registry addition (appended 2026-10-25) | 8 | 6 | 3 | 2 | 6 | 4 | 15 | 250.0 |
| | **mean dens** | | | | | | | | **171.1** |

Total path-citation instances: 662 across 23 blocks.
exit=0
```

This reproduces the r30 figures given in the assignment exactly (mean 171.1, 23 blocks, 662 cites) — the comparison column is not taken on trust.

### 1b. After (final lane SKILL.md, HEAD eecad59)

```
$ python3 corpus/instruments/density.py SKILL.md --label r31-final
# Density census — r31-final (1071 lines, 24 blocks)
| # | block | lines | nb | cites | tbl | num | sig | ev | dens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Pipeline (observed, not invented) | 18 | 15 | 1 | 0 | 0 | 1 | 2 | 13.3 |
| 2 | Program-rule checklist (step 1 of any mission) | 70 | 65 | 22 | 0 | 44 | 0 | 66 | 101.5 |
| 3 | Policy access playbook (fleet-learned) | 10 | 8 | 24 | 5 | 8 | 0 | 37 | 462.5 |
| 4 | Finding-triage decision table | 37 | 32 | 24 | 7 | 15 | 4 | 50 | 156.2 |
| 5 | Intake surface — the map is decorative, ingestion is hidden | 51 | 47 | 15 | 0 | 30 | 4 | 49 | 104.3 |
| 6 | Mission ledger & audit store | 27 | 24 | 21 | 0 | 16 | 6 | 43 | 179.2 |
| 7 | Mission control plane | 28 | 26 | 17 | 0 | 14 | 2 | 33 | 126.9 |
| 8 | UFO runtime workspaces — the untracked `.ufo/` layer + `.omp/` | 42 | 38 | 25 | 0 | 30 | 4 | 59 | 155.3 |
| 9 | Ops integrity layer — invariants, intake, finalize | 130 | 122 | 103 | 0 | 20 | 14 | 137 | 112.3 |
| 10 | VDP disclosure packages (sibling format) | 26 | 23 | 18 | 0 | 8 | 1 | 27 | 117.4 |
| 11 | Retirement lane — autopsies & the detail regex | 62 | 57 | 30 | 0 | 19 | 4 | 53 | 93.0 |
| 12 | Evidence-package anatomy | 28 | 24 | 20 | 6 | 13 | 3 | 42 | 175.0 |
| 13 | Disclosure anti-patterns (all observed in fleet wrap review) | 115 | 110 | 68 | 10 | 47 | 3 | 128 | 116.4 |
| 14 | Claim-hardening wave — the defect layer above the gates | 35 | 30 | 22 | 10 | 21 | 9 | 62 | 206.7 |
| 15 | Submitted-state registry — the do-not-refile set | 50 | 46 | 25 | 0 | 20 | 5 | 50 | 108.7 |
| 16 | Operator queue — live audit | 40 | 36 | 18 | 0 | 16 | 1 | 35 | 97.2 |
| 17 | Triage economics | 172 | 156 | 126 | 18 | 46 | 15 | 205 | 131.4 |
| 18 | Gates & probes registry | 9 | 6 | 1 | 2 | 4 | 7 | 14 | 233.3 |
| 19 | Cited paths (verified 2026-09-28 ...) | (one long line) | | | | | | | |
| 20 | Frontier decision table (round 22) | 13 | 10 | 10 | 5 | 3 | 2 | 20 | 200.0 |
| 21 | Round-29 Gates & probes registry addition (appended 2026-10-25) | 8 | 5 | 1 | 1 | 5 | 7 | 14 | 280.0 |
| 22 | Round-29 frontier note (appended 2026-10-25) | 5 | 2 | 2 | 0 | 1 | 1 | 4 | 200.0 |
| 23 | Round-30 Gates & probes registry addition (appended 2026-10-25) | 10 | 6 | 3 | 2 | 6 | 4 | 15 | 250.0 |
| 24 | Round-31 Gates & probes registry addition (appended 2026-10-25) | 12 | 8 | 27 | 2 | 18 | 6 | 53 | 662.5 |
| | **mean dens** | | | | | | | | **191.5** |

Total path-citation instances: 689 across 24 blocks.
density_exit=0
```

(Block 19's cells are omitted here only because its title is a multi-hundred-character paragraph in the raw output; its three metric cells are unchanged from the r30 replay — proven by the diff in 1c.)

### 1c. Where the delta comes from (block-by-block diff of the two runs)

```
$ diff r30-density.txt r31-density.txt
1c1
< # Density census — r30-replay (1057 lines, 23 blocks)
---
> # Density census — r31-final (1071 lines, 24 blocks)
32,33c32,34
< | 23 | Round-30 Gates & probes registry addition (appended 2026-10-25) | 8 | 6 | 3 | 2 | 6 | 4 | 15 | 250.0 |
< | | **mean dens** | | | | | | | | **171.1** |
---
> | 23 | Round-30 Gates & probes registry addition (appended 2026-10-25) | 10 | 6 | 3 | 2 | 6 | 4 | 15 | 250.0 |
> | 24 | Round-31 Gates & probes registry addition (appended 2026-10-25) | 12 | 8 | 27 | 2 | 18 | 6 | 53 | 662.5 |
> | | **mean dens** | | | | | | | | **191.5** |
35c36
< Total path-citation instances: 662 across 23 blocks.
---
> Total path-citation instances: 689 across 24 blocks.
table_diff_exit=1
```

Exact before/after:

| metric | r30 (5703f9f) | r31 (eecad59) | delta |
|---|---:|---:|---:|
| mean dens | 171.1 | 191.5 | +20.4 |
| blocks | 23 | 24 | +1 |
| path-citation instances | 662 | 689 | +27 |

**Every pre-existing block's row is byte-identical** (including 23, whose `lines` 8→10 is two blank separator lines: nb remains 6, ev remains 15, dens remains 250.0). The whole mean move is the appended block 24, and the mean is unweighted per block, so a dense 12-line append lifts it by construction. No existing block was repaired or reformatted; no score move is claimed or implied by this seat.

### 1d. Form-gaming audit of block 24

```
$ python3 - <<'EOF'   # imports the instrument's own split_blocks/is_pathlike, reads SKILL.md only
print("block:", title, "lines:", len(bl))
print("cite occurrences:", len(toks), "distinct:", len(set(toks)))
EOF
block: Round-31 Gates & probes registry addition (appended 2026-10-25) lines: 12
cite occurrences: 27 distinct: 27
```

All 27 path-like tokens are distinct — the count is not repetition. But not all are files; classified through the same definition as the census of record (lookup in the scratch-generated `citation-survival.tsv`):

```
INTERNAL  .ufo/waves/round-31/wave1/ExecLedgerMerge.md
INTERNAL  .ufo/waves/round-31/wave1/ExecScoreGap.md
RESOLVES  /tmp
GONE      LIMB <id> live=<exit>/<sig:y|n> mutant=<exit>/<sig:y|n> verdict=killed
INTERNAL  SCORECARD.md
GONE      census-lane: 134/1480 = 9.05%
GONE      census-skill: 32/506 = 6.32%
INTERNAL  corpus/
INTERNAL  corpus/instruments/citation-survival.md
INTERNAL  corpus/instruments/frontier-recheck-count.py
INTERNAL  corpus/instruments/limb-fixtures/fr/
INTERNAL  corpus/instruments/limb-fixtures/sr/
INTERNAL  corpus/instruments/recheck-audit.py
INTERNAL  corpus/instruments/source-recheck.py
GONE      cwd.md
GONE      elsewhere.md
GONE      frontier-recheck-count.py
GONE      ghost.md
GONE      instonly.md
GONE      limb-fixtures/
GONE      limb-ledger.json
GONE      limb-mutation-check.py
GONE      parseonly.md
GONE      resolve.py
GONE      score-gap.py
GONE      selftesty.md
GONE      strict pass=44/44
resolve-fraction: 11/27 = 40.74%
```

Reading: 16 of the 27 "citations" are bare fixture filenames (`parseonly.md`, `cwd.md`, `ghost.md`, `elsewhere.md`, `instonly.md`, `selftesty.md` — none exist on disk), bare basenames that live one directory down (`frontier-recheck-count.py`, `limb-mutation-check.py`, `limb-ledger.json`, `score-gap.py`, `resolve.py`, `limb-fixtures/`), or command-output fragments (`LIMB <id> ...`, `census-lane: ...`, `census-skill: ...`, `strict pass=44/44`). Block 24's `dens=662.5` is therefore a **volume/rule effect of the path-like definition**, not a measure of newly resolvable evidence: the instrument's own r16 conjunctive rule (dens ≥ BAR_R15 **and** ≥60% of path citations resolve) would **not** qualify this block, since 11/27 = 40.74%. This is the documented blind spot ("a fabricated `path:line` scores identically to a real one", `SCORECARD.md:53-57`), disclosed rather than argued around. No SCORECARD row should cite block 24's 662.5 as a density repair.

Density axis verdict: **held at 9**; no score move asserted; measurement recorded with its mechanism disclosed.

## 2. depth:verifiability — anchorcheck before/after

### 2a. Before (r30 SKILL bytes replayed in the scratch lane copy)

```
$ cp r30-SKILL.md SKILL.md && python3 corpus/instruments/anchorcheck.py SKILL.md; echo "exit=$?"
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
LOST-RECORDED md:57 [lost-tree] claims/bugcrowd-seek/... (not checked)
...
r30_anchor_exit=0
$ grep -c '^LOST-RECORDED ' r30-anchor.txt
306
```

(The full LOST-RECORDED trace is 306 lines; the count is quoted from `grep`, not retyped.)

### 2b. After (final lane SKILL.md)

```
$ python3 corpus/instruments/anchorcheck.py SKILL.md; echo "anchor_exit=$?"
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
... 306 LOST-RECORDED lines, 7 OK lines ...
anchor_exit=0
```

| verdict class | r30 | r31 |
|---|---:|---:|
| in-range instances | 7 | 7 |
| bad | 0 | 0 |
| LOST-RECORDED | 306 | 306 |
| PIN-BROKEN | 0 | 0 |
| ORIGIN | 0 | 0 |
| OUTSIDE-BASE | 0 | 0 |
| BASE-ABSENT | 0 | 0 |
| exit | 0 | 0 |

Unchanged in every class; exit 0 (fail-closed rule satisfied: no nonzero FAIL_CLASSES). The r30 summary line given in the assignment is confirmed by replay, not assumed.

## 3. depth:verifiability — resolve.py census of record vs final bytes (scratch only)

### 3a. Scratch construction and fidelity

```
$ D=$(mktemp -d /tmp/r31-noharm.XXXXXX) && rsync -a --exclude=.git ./ "$D/lane/"
$ diff -rq "$D/lane"/corpus /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus
Files corpus/instruments/citation-survival.md and .../citation-survival.md differ
Files corpus/instruments/citation-survival.tsv and .../citation-survival.tsv differ
diff_exit=1
$ diff -q "$D/lane"/SKILL.md .../SKILL.md ; echo "skill_diff_exit=$?"
skill_diff_exit=0
```

Only the two generated report files differ — i.e. only the files the instrument itself rewrites. The scratch lane is otherwise byte-identical to the lane (SKILL.md and every corpus file), so lane-relative resolvability inside the scratch is the lane's resolvability. `--exclude=.git` only: resolve.py reads no git object, and lane Git/jj state was never touched.

### 3b. Run (writes stay in the scratch lane)

```
$ cd "$D/lane" && python3 corpus/instruments/resolve.py "$D/lane"; echo "resolve_exit=$?"
distinct=2263 resolves=25 mirror=0 internal=363 other=0 gone=1875 skill=55/547 corpus=369/1924 all=388/2263
wrote /tmp/r31-noharm.fFRfHl/lane/corpus/instruments/citation-survival.tsv
wrote /tmp/r31-noharm.fFRfHl/lane/corpus/instruments/citation-survival.md
resolve_exit=0
```

Generated census headline (scratch copy):

```
Lane root: `/tmp/r31-noharm.fFRfHl/lane`
Scope: `SKILL.md` + `corpus/**/*.md` (85 files).
- distinct path-like citations: **2263** (total occurrences: 4444)
| RESOLVES | 25 |  MIRROR-EQUIVALENT | 0 |  GONE | 1875 |  INTERNAL | 363 |
- SKILL.md alone: **55/547 = 10.05%**
- corpus alone: **369/1924 = 19.18%**
- lane total (SKILL.md + corpus): **388/2263 = 17.15%**
```

Determinism (the docstring's byte-identical claim):

```
$ sha256sum corpus/instruments/citation-survival.* > first.sha
$ python3 corpus/instruments/resolve.py . ; sha256sum -c first.sha
corpus/instruments/citation-survival.md: OK
corpus/instruments/citation-survival.tsv: OK
distinct=2263 resolves=25 mirror=0 internal=363 other=0 gone=1875 skill=55/547 corpus=369/1924 all=388/2263
```

Spot-check of the resolving rows (resolved paths exist inside the scratch tree; `/`-rooted others exist on the host):

```
LOG.md        INTERNAL  .../lane/LOG.md
SKILL.md      INTERNAL  .../lane/SKILL.md
corpus/README.md INTERNAL .../lane/corpus/README.md
.ufo/         INTERNAL  .../lane/.ufo/
/tmp          RESOLVES  /tmp
~/Projects/ufo-fsd-alpha RESOLVES /home/vgpnk/Projects/ufo-fsd-alpha
/home/vgpnk/Projects/shokuknow/merge/kasegi RESOLVES (exists, read-only)
```

### 3c. Lane rate vs the committed census figures

| scope | committed `citation-survival.md` (census of record) | measured on final bytes (scratch) | delta |
|---|---|---|---|
| distinct citations | 1480 (2925 occ) | 2263 (4444 occ) | +783 |
| cited files in scope | 50 | 85 | +35 |
| SKILL.md alone | 32/506 = 6.32% | 55/547 = 10.05% | +3.73 pp |
| corpus alone | 118/1153 = 10.23% | 369/1924 = 19.18% | +8.95 pp |
| lane total | 134/1480 = 9.05% | 388/2263 = 17.15% | +8.10 pp |
| classes | RESOLVES 10 / MIRROR 0 / INTERNAL 124 / GONE 1346 | RESOLVES 25 / MIRROR 0 / INTERNAL 363 / GONE 1875 | — |

**These are not two measurements of the same population** (denominator 1480 → 2263), so the delta is not a rate "improvement" of the same denominator; it is growth in both numerator and denominator.

### 3d. Attributing the delta (bytes vs instrument revision)

Committed census provenance and reproduction on its own bytes:

```
$ git log -1 --format='%h %ad %s' -- corpus/instruments/citation-survival.md
644ed37 Wed Oct 14 21:23:34 2026 -0300 round-20: audit corrections ...
$ D2=$(mktemp -d) && git archive 644ed37 | tar -x -C "$D2" && cd "$D2" \
  && python3 corpus/instruments/resolve.py "$D2"
distinct=1480 resolves=11 mirror=0 internal=120 other=0 gone=1349 skill=31/506 corpus=115/1153 all=131/1480
```

Running the *current* instrument over the *same round-20 bytes*:

```
$ cp <lane>/corpus/instruments/resolve.py corpus/instruments/resolve.py \
  && python3 corpus/instruments/resolve.py .
distinct=1480 resolves=11 mirror=0 internal=120 other=0 gone=1349 skill=31/506 corpus=115/1153 all=131/1480
```

Identical class totals under both instrument revisions (only the file-size column differs, 516 → 623 lines). Therefore:
- the census of record reproduces its own distinct total (1480) and its denominators (506, 1153) exactly;
- the committed copy's class split differs from the archive replay by 4 citations (RESOLVES 10 vs 11, INTERNAL 124 vs 120, GONE 1346 vs 1349) because the original was produced in the live lane with untracked `.ufo/` files and `/tmp` targets present that an `git archive` tree does not carry — an expected live-tree artifact, not an instrument change;
- instrument revisions (r23/r24) do **not** move the totals;
- consequently the whole r31 delta (9.05% → 17.15%) is **corpus byte growth** since round 20 (rounds 21–31 added entries/instruments/lessons that cite lane-internal paths).

## 4. Diff verification: edits are additions only

```
$ git diff --stat b374febbb33ccadade78a787279707fd5d2e6e1d -- SKILL.md PROVINCE.md
 PROVINCE.md | 20 ++++++++++++++++++++
 SKILL.md    | 14 ++++++++++++++
 2 files changed, 34 insertions(+)
$ git diff --numstat b374febbb33ccadade78a787279707fd5d2e6e1d -- SKILL.md PROVINCE.md
20      0       PROVINCE.md
14      0       SKILL.md
$ git diff b374febbb33ccadade78a787279707fd5d2e6e1d -- SKILL.md PROVINCE.md | grep -E '^(diff|@@)'
diff --git c/PROVINCE.md w/PROVINCE.md
@@ -50,3 +50,23 @@ Sibling lanes are reported, not absorbed:
diff --git c/SKILL.md w/SKILL.md
@@ -1055,3 +1055,17 @@ F13 — program severity ladders and reward scales — admitted 2026-10-25; entr
```

Deleted lines: **0** in both files (numstat second column). Both hunks start at the old file's tail, i.e. end-of-file appends. Stronger form — every existing line keeps its number:

```
$ N1=$(git show b374feb:SKILL.md | wc -l); cmp <(git show b374feb:SKILL.md) <(head -n "$N1" SKILL.md)
SKILL_prefix_identical=yes          # base_lines SKILL=1057 -> current 1071 lines
$ N2=$(git show b374feb:PROVINCE.md | wc -l); cmp <(git show b374feb:PROVINCE.md) <(head -n "$N2" PROVINCE.md)
PROVINCE_prefix_identical=yes       # base_lines PROVINCE=52 -> current 72 lines
```

So the r31 SKILL.md change is the single appended block 24 (registry rows for `limb-mutation-check.py` + `limb-ledger.json`, `score-gap.py`), and the PROVINCE.md change is the appended F12–F15 frontier amendment + R9 correction paragraph; nothing pre-existing was edited, reflowed or deleted. (SKILL.md working-tree bytes are clean against HEAD; the diff is therefore HEAD-vs-base, not a working-tree artifact.)

## 5. No-harm verdict

- density.py: export 0, mean 171.1 → 191.5, blocks 23 → 24, cites 662 → 689; **all pre-existing block rows byte-identical**; the entire mean move is one appended block whose 40.74% resolve-fraction fails the instrument's own ≥60% conjunctive rule — disclosed, no density credit claimed.
- anchorcheck.py: exit 0, every verdict class identical to r30 (7 in-range, 0 bad, LOST-RECORDED=306, PIN-BROKEN/ORIGIN/OUTSIDE-BASE/BASE-ABSENT all 0).
- resolve.py: exit 0 in a scratch lane, deterministic (byte-identical second run), committed census figures reproduce on round-20 bytes; final-byte lane rate 388/2263 = 17.15% vs census-of-record 134/1480 = 9.05%, delta attributed to corpus growth.
- SKILL.md / PROVINCE.md edits since the claims base: 34 added lines, 0 deleted, prefix-identical line numbering.
- No lane write by this seat: the three instruments were run read-only (`density.py`, `anchorcheck.py`) or inside the scratch lane (`resolve.py`); `git status` clean for every measured path and the committed `citation-survival.md` still hashes `795ba4f…`. Scratch trees (`/tmp/r31-noharm.*`, `/tmp/r31-r20.*`, `/tmp/tmp.*` density replay) were deleted at the end of this seat.

## 6. Routes for the L1 (not fixed here — lane is read-only for this seat)

1. **Census of record is 11 rounds stale, and r31 quotes it as if current.** `corpus/instruments/citation-survival.md` was last generated at `644ed37` (round-20, 50 cited files, lane 134/1480 = 9.05%). The round-31 SKILL block 24 (line 1071 area) cites `census-lane: 134/1480 = 9.05%` and `census-skill: 32/506 = 6.32%`, and `score-gap.py` prints the same numbers in its `[3] citation-survival census (committed figures)` field. Both label them committed figures (no false claim of a live measurement), but a reader of the r31 row will take 9.05% as the lane's current rate when the final bytes measure 17.15%. Either regenerate the census as part of a future round's verifiability move, or have the quoting sites carry the census's generation point (round-20 / `644ed37`). This is the same stale-premise class as M31-1.
2. **Density mean is block-unweighted and block-24-inflated.** Appending a 12-line block lifted the mean 20.4 points with zero change to existing blocks. Any SCORECARD text that records "mean up" for r31 should record the mechanism (new block, 40.74% resolve-fraction) alongside the number, per the r15 no-self-inflation rule and the r16 conjunctive bar.
3. **Block 24's citation count includes 16 non-file tokens** (fixture filenames that do not exist, bare basenames resolvable only as `corpus/instruments/...`, and command-output fragments). Not a defect in the block's prose — it is the path-like rule's frontier — but it must not be read as 27 resolvable evidence pointers.

## 7. Risks / blockers

- None blocking. Wave-2 single-writer surfaces (QUALITY.md, SCORECARD.md, SHONEN.md, lessons/round-31.md, limb counter + ledger) are outside the measured bytes; if a later wave-2 edit changes SKILL.md, PROVINCE.md or the three instruments, these numbers must be re-run on the quiescent bytes (bounds item 6). No such edit is in any wave-2 write scope, so this measurement is stable for the current plan.
- environment caveat: `resolve.py` credits root-domain `other` paths (`/tmp`, `/`, `~/Projects/ufo-fsd-alpha`, `.../shokuknow/merge/kasegi`) as RESOLVES by its definition — the 25 RESOLVES are all such non-lane roots, matching the census of record's own statement.
- No live bounty target contacted; no fetches; no credential material; no delegation (the one permitted labrat was not needed).
