# RevNoHarm — round-35 independent no-harm review (kasegi)

Seat: RevNoHarm (reviewer, leaf of the round-35 L2 wave-1, hyaku run 8).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Lane base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`; wave-spec commit `da2d3c687f82a9814ee71c91c930cb733050d37c` (HEAD at review start).
Review window: 2026-10-26T06:33Z – 2026-10-26T06:52Z (host TZ `-03:00`). The wave was **live during this review** (peer seats were landing files concurrently; every observation below is timestamped).

Instrumentation note: no `lsp` device is mounted in this session (tool inventory: read/bash/edit/eval/glob/grep/task/wait/web_search/write/yield; MCP routes: aseprite/blender/godot/tripo/unity). All checks are textual/instrument-based; semantic LSP checks were not applicable to the assigned probes.

## Report

### A. Append-only numstat over production files

Command (first run, ~06:34Z):

```
git diff --numstat 3266c9937b03062d9bbc2f436e20820115ed179c -- SKILL.md PROVINCE.md corpus SCORECARD.md LOG.md
33  15  SCORECARD.md
13   0  SKILL.md
numstat_exit=0
```

Command (final re-run, 06:51:10Z — the tree gained landings between runs; flux disclosed):

```
git diff --numstat 3266c9937b03062d9bbc2f436e20820115ed179c -- SKILL.md PROVINCE.md corpus SCORECARD.md LOG.md
33  15  SCORECARD.md
13   0  SKILL.md
28   0  corpus/README.md
 7   0  corpus/SOURCES.md
 1   0  corpus/instruments/knowledge-expected.txt
numstat_exit=0
```

Attribution: `git show --numstat 617496b` touches only `.ufo/waves/round-35/{c1-controls/before.txt,c2-controls/before.txt,census-before.txt,claims.json}`; `git show --numstat da2d3c6` touches only `.ufo/waves/round-35/{build-spec.py,wave1-dispatch.json,wave1-plan.err,wave1-plan.out,wave1-run.err,wave1-spec.json}`. **Every production-file change is working-tree, authored by round-35 wave seats.**

Per-file result:

| file | Δ | verdict |
|---|---|---|
| SKILL.md | +13 / −0 | append-only PASS (EOF append, lines 1092–1104, block 26 "Round-35 Gates & probes registry addition"; 1091 → 1104 lines; sha `daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc`) |
| PROVINCE.md | unchanged | PASS (`git diff --stat 3266c99 -- PROVINCE.md` empty, exit 0) |
| LOG.md | unchanged | PASS (same; round-35 LOG entry is the L1 closing-commit job, consistent with r33/r34 pattern) |
| corpus/README.md | +28 / −0 | append-only PASS (F18 row + round-35 sweep bullets) |
| corpus/SOURCES.md | +7 / −0 | append-only PASS (S052 row + search-log bullet; observed growing 5→7 during the window) |
| corpus/instruments/knowledge-expected.txt | +1 / −0 | append-only PASS |
| **SCORECARD.md** | **+33 / −15** | **DEVIATION — see A.1** (sha `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7`) |

New untracked additions (0 deletions by construction): `corpus/instruments/r35-defect-closure.sh`, `corpus/instruments/r35-fixtures/`, `corpus/knowledge/cisa-kev-catalog.md`, `corpus/source-snapshots/round-35/`, `.ufo/waves/round-34/wave1-results.json` + `.provenance.md`, `.ufo/waves/round-35/{assimilation/,c1-controls/fake-suite.sh,c2-controls/junk-f18.md,claims-erratum-d5.md,wave1/,wave1.ready,wave1.ready.dispatched}`.

Line-count check: `git show 3266c99:SCORECARD.md | wc -l` = 1243; `wc -l SCORECARD.md` = 1261; delta +18 = 33−15 ✓.

#### A.1 The 15 SCORECARD.md deletions, enumerated

All 15 deleted lines (from `git diff 3266c993… -- SCORECARD.md | grep -E '^-[^-]|^-$'`, count 15; additions 33):

Hunk 1 (@ −1126,11 lines deleted / +6) — the round-34 preamble placeholder paragraph:

```
-`c2-controls/before.txt`) and `census-before.txt`. **Final lane commit: the L1 fills this line in the
-closing commit.** This section is written at the wave-1 integration state on the bytes digested under
-§ Measurement state, claims no lane-commit hash, and deliberately introduces no placeholder token —
-round-33 R1's defect was a published placeholder, the C1 counter reads that count as 0, and nothing
-here moves it. Receipts land under `.ufo/waves/round-34/` (`c1-controls/`, `c2-controls/`,
-`census-before.txt`, `claims-erratum-1.md`, `assimilation/`, `wave1/`; 58 seat receipts at this
-seat's read). The last round heading at this round's base is round 33, so C1's and C2's last-change
-column stays 33 and every before-column below is the frozen control measured at this round's base
-bytes. The round-34 subject is instrument-soundness closure for the nine round-33 verifier-routed
-defects R1–R9 (C1) and frontier F17 / Immunefi Vulnerability Severity Classification System v2.2
-(C2).
```

Hunk 2 (@ −1237,4 lines deleted / +27) — the closing placeholder paragraph (D1's literal counter target):

```
-**Round-34 final lane commit: filled by the L1 in the closing commit.** Every value in this section
-was measured at the wave-1 integration state on the quiescent bytes digested under § Measurement
-state; the closing commit may add seat receipts, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-34.md`
-and this section itself, none of which any counter above reads.
```

Both replacements name `c1c6a5f826d2425446347173de527c42991b78b0`; hunk 2 additionally appends the D2 density erratum (mean 201.2 bound to blobs `206e510:SKILL.md` / `3266c993:SKILL.md`), its measurement-state paragraph, and the correction note ("the two lane-commit placeholder sentences above … were replaced … Neither placeholder spelling occurs in this file any more … Nothing else in this section changed.").

Classification:

1. Hunk 2 is **mandated by frozen C1**: the kill rule lists "`filled by the L1` placeholder prose still present in SCORECARD.md", the counting command is `grep -c 'filled by the L1' SCORECARD.md -> 0`, and the D1 after-state requires an appended correction naming c1c6a5f. The frozen before-state recorded 1 such line; hunk 2 removes exactly that line.
2. Hunk 1 goes **beyond the literal counter**: its deleted text says "the L1 fills this line in the closing commit", a spelling the closure suite does not grep (`corpus/instruments/r35-defect-closure.sh:148` counts only `-F 'filled by the L1'` plus `<LANE_HASH>` markers). It is the same placeholder-prose defect class (a lane-commit placeholder naming the L1 as filler, sitting in the same section), it was replaced with the same hash, and the substitution is disclosed in the replacement text itself — but strictly it is an extra 11-line deletion + rewrite that the frozen claim text does not require by counter.
3. R6 line-stress (`corpus/QUALITY.md` R6: "keeps every existing line at its number"): the net +18 shift is at lines ≥1126. The only production line-cites of SCORECARD.md are `LOG.md:880` → `SCORECARD.md:88-96` and SCORECARD's own errata at `SCORECARD.md:839`/`:951` → `:813-819` — all before 1126. No production line-cite breaks. anchorcheck before/after (§B) prints identical cited source lines for every surviving SKILL.md anchor.
4. The item's literal criterion "append-only (0 deletions)" is therefore **not met for SCORECARD.md**. My judgment as reviewer: this is the frozen claim's own subject executed as disclosed, not silent harm — but it is a deviation from the review template's wording, and the L1 should adjudicate the hunk-1 scope call (claims-mandated vs beyond-counter) before scoring.

### B. `anchorcheck.py SKILL.md` failure classes

Instrument: `corpus/instruments/anchorcheck.py`, sha256 `d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912` (unchanged across all runs; canonical runtime = the lane's own bytes, run from the lane root).

Base tree (honest before-limb): `git show 3266c99:SKILL.md` extracted to scratch; sha256 `ba5ebe5d9417b1801d48bbdb8fa533eb9df586f588bbad398eacd062e408163e`, 1091 lines — **exactly the blob and line count the D2 erratum in SCORECARD.md declares** (independent corroboration of the erratum's figures). Run with `KASEGI_LANE_ROOT=<lane>`:

```
exit=0; anchored fail classes: BASE-ABSENT=0 MISSING-FILE=0 PAST-EOF=0 OUTSIDE-BASE=0 PIN-BROKEN=0 BOUNTIES-ABSENT=0
OK=12, LOST-RECORDED=306
```

Landed tree, runs 2 and 3 on pinned bytes (sha256 `daeff71b…` verified identical before and after each run):

```
python3 corpus/instruments/anchorcheck.py SKILL.md
run2_exit=0, run3_exit=0
anchored fail classes: 0 (all six classes 0)
OK=16, LOST-RECORDED=306 (run 3); OK=16 (run 2)
```

So: **failure classes 0 — criterion MET on the settled bytes**, and the verdict-class vector is unmoved vs base (0 fail classes, LOST-RECORDED 306→306; in-range 12→16 from the appended block).

**Transient disclosure (must-read for the L1).** My run 1 (~06:34Z, concurrent with other seats' landings) printed `exit=1` with exactly one fail line:

```
BASE-ABSENT md:1097 S050.txt:70 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/S050.txt)
```

at a moment when the OK lines at md:1100/md:1102 already matched the landed bytes. On the pinned final bytes this is **not reproducible** (runs 2+3 clean), and the landed line 1097 (the `r-defect-closure.sh` registry row) carries the fully lane-prefixed token `corpus/source-snapshots/round-32/S050.txt:70` (630-line file, line 70 exists): extracting line 1097 alone and running the same instrument gives `OK … S050.txt:70 [本標準适用于…]`, `BASE-ABSENT=0`, exit 0. The same token string cannot classify two different ways inside a per-line tokenizer, so run 1 read **different (mid-write) bytes** — the scribe seat was rewriting SKILL.md in that window (the same batch's density run saw the final 26-block state). Cause class: torn/mid-write read during concurrent wave writes, not a landed defect and not instrument nondeterminism (two consecutive runs on pinned bytes are clean; the base run is clean). jj snapshot archaeology to recover the intermediate bytes was attempted and abandoned: `jj op log -T 'opid()…'` fails (template function `opid` doesn't exist in the installed jj), and the default-template listing shows only my own probe-triggered `snapshot working copy` ops. **Recommendation: re-run `anchorcheck.py SKILL.md` post-quiescence before scoring** (the tree was still fluxing at 06:51Z: corpus/README.md +28 and SOURCES.md +7 landed during this review).

### C. Density mean vs the round-34 201.2 floor

Command and output on the pinned landed bytes (`daeff71b…`, unchanged instrument `density.py` sha `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`):

```
python3 corpus/instruments/density.py SKILL.md --label RevNoHarm-r35-pinned
density_exit=0
1104 lines, 26 blocks, 742 path-citation instances
mean dens **220.9**
```

- Round-34 comparison figure: **201.2** (the D2-corrected depth:density row; erratum bound to `git show 3266c993:SKILL.md` = `ba5ebe5d…`, 1091 lines — both independently re-verified in §B).
- Actual 220.9 is **+19.7 above** the floor → **criterion MET** (the check is "not below 201.2 by more than noise").
- Mechanism, disclosed per the round-31 convention: the move is entirely the EOF-appended block 26 (12 lines, nb=8, 31 cites, dens 712.5) through the block-unweighted mean; zero existing lines changed (numstat −0), so no reflow or form-gaming occurred (the r15 form-sensitivity hazard is structurally excluded by the 0-deletion diff on SKILL.md).
- Corroborating run at ~06:34Z (pre-pinning) printed the identical mean 220.9 / 26 blocks / 742 cites.

### D. Fleet root — no new lost-base/misroot files

Host TZ is `-03:00`; `date` = Mon 26 Oct 2026 03:43:18 AM -03. Fleet root `/home/vgpnk/Projects/shokunin`, read-only sweep:

```
find /home/vgpnk/Projects/shokunin -maxdepth 1 -type f -newermt '2026-10-26 00:00' -printf '%TY-%Tm-%Td %TH:%TM %p\n'
2026-10-26 02:27 ./AGENTS.md
2026-10-26 02:27 ./.gitignore
2026-10-26 02:27 ./LOG.md
2026-10-26 02:27 ./README.md
2026-10-26 03:26 ./MANIFEST.json
2026-10-26 03:32 ./SCORECARD.md
```

All six are pre-existing fleet-repo files, and all were last touched at 02:27–03:32 local (05:27–06:32Z) — the round-35 wave dispatched after `da2d3c6` (06:4xZ window); none is round-35-authored and none is a kasegi lane artifact. Stray-name mtimes: `demo-cwd.txt` 2026-10-25 20:54, `ok` 16:43, `m-rev-vs-rev.py` 09:36, `shokunin.conf` 2026-10-19 — all pre-round. No new file of any name appeared at the root during the review window. **Criterion MET** (no new lost-base/misroot files at the fleet root authored by this round).

### E. Digests of record

```
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md (landed)
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md (landed)
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md (06:51Z)
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md (06:51Z)
ba5ebe5d9417b1801d48bbdb8fa533eb9df586f588bbad398eacd062e408163e  SKILL.md @ 3266c99 (base blob)
d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912  corpus/instruments/anchorcheck.py
ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710  corpus/instruments/density.py
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  corpus/instruments/r35-defect-closure.sh
```

## Verdict

**No-harm: PASS with one deviation for L1 adjudication and one watch-item.**

1. **Append-only** — MET for SKILL.md (+13/−0), PROVINCE.md, LOG.md, corpus/README.md (+28/−0), corpus/SOURCES.md (+7/−0), knowledge-expected.txt (+1/−0). **NOT literally met for SCORECARD.md (+33/−15)**: the 15 deletions are exactly the two round-34 lane-commit placeholder paragraphs, replaced with the c1c6a5f hash plus the appended D2 erratum/measurement/correction notes. Hunk 2 is mandated by frozen C1's kill rule; hunk 1 (the preamble paragraph, a different spelling of the same placeholder class that the suite's grep does not count) goes beyond the literal counter but is disclosed in-place. No production line-cite breaks (R6 stress: all SCORECARD line-cites target lines <1126). Nothing else in any production file was deleted.
2. **anchorcheck failure classes** — MET on the settled bytes: exit 0, all six fail classes 0, 16 OK, LOST-RECORDED=306; base-blob run also exit 0 (12 OK, 306), so the verdict-class vector is unmoved. Watch-item: one transient exit-1 (`BASE-ABSENT md:1097 bare S050.txt:70`) was observed mid-write at ~06:34Z and is not reproducible on the pinned final bytes — re-run anchorcheck post-quiescence before scoring.
3. **Density** — MET: mean **220.9** (1104 lines / 26 blocks / 742 cites), +19.7 above the round-34 corrected 201.2; move is the EOF-appended block 26, no reflow (0 deletions). The D2 erratum's declared base blob/line-count figures independently re-verified.
4. **Fleet root** — MET: no new files at `/home/vgpnk/Projects/shokunin` depth 1; the only files modified today are pre-existing fleet-repo files last touched before the wave window.

Residual risks / verification gaps: (a) the tree was still landing during this review (corpus/README.md, corpus/SOURCES.md grew between 06:34Z and 06:51Z) — all four probes should be re-run at quiescence by the L1; (b) the intermediate SKILL.md bytes behind the §B transient were not reconstructed (jj template incompatibility, disclosed); (c) the hunk-1 scope call in A.1 is a claims-vs-template tension that only the L1 can adjudicate. No tooling was installed or upgraded (none needed); scratch dir usage and removal are recorded below.

## Scratch

Work tree `/fast/scratch/hyaku/kasegi-r35/RevNoHarm/` (SKILL-r34base.md, line1097.md, anchorcheck-skill.txt, anchorcheck-base.txt, anchorcheck-skill-run2.txt, anchorcheck-skill-run3.txt, density-skill.txt, density-skill-pinned.txt) — removed before yielding; removal verified in-session.
