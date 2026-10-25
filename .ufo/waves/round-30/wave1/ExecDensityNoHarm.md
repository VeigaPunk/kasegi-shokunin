# ExecDensityNoHarm — round 30, wave 1 no-harm gate (before → after)

Seat: `ExecDensityNoHarm-2` (L2, leaf; no subagent dispatch, no tool installed — nothing was
needed, and no `pacman`/`uv`/`cargo`/`npm` channel was used). Answering model:
`inception/mercury-3` (operator route; no model passed). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Fleet root `/home/vgpnk/Projects/shokunin` and
`/home/vgpnk/Projects/shokuknow` were never written to; no `git`/`jj` mutation; no live target
contacted. This report is the only file written by this seat.

## Axes (godspeed)

1. **Before-measurement correctness** — capture the three instrument runs + hashes at the wave
   start against labeled bytes, before production edits.
2. **After-measurement completeness** — poll for the C2 F14 landing (frontier row, knowledge
   entry, registry rows, captures, expected-list regeneration) and re-run all three instruments at
   the settled bytes.
3. **No-harm verdict** — before/after numbers, verdict-class movement (must be none beyond
   documented appends), and owned-axis score confirmation (depth:density 9, depth:verifiability
   4 held, coverage 7 held). No production file edited by this seat.

## Before (r30-before, measured 2026-10-25 ~18:49Z; instruments at frozen base digests)

Command set (cwd = lane root), all read-only:

```
python3 corpus/instruments/density.py SKILL.md --label r30-before
python3 corpus/instruments/anchorcheck.py SKILL.md
python3 corpus/instruments/recheck-audit.py
sha256sum SKILL.md PROVINCE.md
```

| measurement | before value |
|---|---|
| density.py SKILL.md | **1047 lines, 22 blocks, mean dens 167.5, 659 path-citation instances** |
| anchorcheck.py SKILL.md | `== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0 |
| recheck-audit.py | strict pass=41/41, cdroot_fail=0 instrument_fail=0 own_fail=0; executes=17 gated=24 broken=0; lines=41 total=41 pass=41 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0; `expect=present expected=41 missing=0 unexpected=0 exit=0` |
| SKILL.md sha256 | `82bdced5d5c46b6847a169f5ce6bec172dbf0c57d51bc5ec5361e2bd4731ee70` |
| PROVINCE.md sha256 | `98f7a9dcf9d13e93baf05629fd2033406fb4118827deb01af8a28aa8d2d92304` |
| instrument digests | frontier-recheck-count.py `c8a62888…`; source-recheck.py `9fe6a4a0…`; knowledge-expected.txt `6d26f6d5…` (density.py `ee803726…`, anchorcheck.py `d0f35f8…`, recheck-audit.py `3fc0d751…`) |

The before bytes reproduce the committed frozen receipts: `.ufo/waves/round-30/c1-controls/before.txt`
(instrument digests), `c2-controls/before.txt` (frontier 13, citations to S04[6-7] 0, rows 45),
`census-before.txt` (frontier 13, harness entries=16 pass=16). C2's do-nothing control was
intact at measurement: no F14 row, no S046/S047 rows, no round-30 captures, no
`knowledge/japanese-severity-vocabulary-and-impact-model.md`.

## Landing timeline (polled; sleep 30s loops, ceiling 60 min — completed in ~8 min)

| UTC | observed state |
|---|---|
| 18:50:39Z | F14 row present in `corpus/README.md` (line 284); frontier-recheck-count.py `bab0d321…`; source-recheck.py `0b841d5d…` (instrument edits in flight; source-recheck settled at `33602a9d…` by 18:52:18Z) |
| 18:52:48Z | entry `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` present; S046/S047 rows in `corpus/SOURCES.md` (lines 52–53); captures `corpus/source-snapshots/round-30/{S041,S046,S047}.txt` + `manifest.json` present |
| 18:53–18:57Z | recheck-audit transiently red while `knowledge-expected.txt` was regenerated: unexpected 2 → 1 → 0, expected 41 → 42 → 43 |
| 18:57:20Z | audit settled green: `expect=present expected=43 missing=0 unexpected=0 exit=0`; knowledge-expected.txt now `98282841943…` |

## After (r30-after, settled, measured 2026-10-25 ~18:58Z)

| measurement | after value | vs before |
|---|---|---|
| density.py SKILL.md | **1057 lines, 23 blocks, mean dens 171.1, 662 path-citation instances** | density changed **167.5 → 171.1** (block 23 "Round-30 Gates & probes registry addition (appended 2026-10-25)" added; **measurement change disclosed, not claimed** — no score move) |
| anchorcheck.py SKILL.md | `== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0 | **verdict classes identical** (7/0/7/306/0/0/0/0) |
| recheck-audit.py | strict pass=43/43, cdroot_fail=0 instrument_fail=0 own_fail=0; executes=19 gated=24 broken=0; lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0; `expect=present expected=43 missing=0 unexpected=0 exit=0` | green on both sides (expected list regenerated 41 → 43 entries to match the two new entries; documented R6/round-29 append pattern) |
| SKILL.md sha256 | `a05c1b47afd4498b107ff962497d0c9d7e938a6feca88fa4f0cbddd749599cfc` | changed (append-only) |
| PROVINCE.md sha256 | `98f7a9dcf9d13e93baf05629fd2033406fb4118827deb01af8a28aa8d2d92304` | **unchanged** |
| instrument digests | frontier-recheck-count.py `aa60b581…`; source-recheck.py `33602a9d…`; knowledge-expected.txt `98282841943…` (density.py `ee803726…`, anchorcheck.py `d0f35f8…`, recheck-audit.py `3fc0d751…`) | the two C1 instruments changed; this seat's three no-harm instruments are byte-identical before/after |

Landing evidence (context, read-only counters):
- frontier harness: `entries=17 pass=17 exit=0` incl. `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0`.
- registry: S046/S047 rows present (tier A, mined); census `validate` exit 0 (W04 S028/S029 only).
- round-30 manifest per-id `source-recheck` exit 0 for S046/S047/S041; every assertion either
  `occurrences=1` or carries a verified anchor (S047 Q1 occurrences=3 anchor=123-ok, Q3
  occurrences=2 anchor=130-ok).

## Verdict

- **No verdict-class movement** on this seat's instruments beyond documented appends: anchorcheck
  classes identical before/after; recheck-audit green before (41/41) and after (43/43) with the
  mid-wave regeneration transient recorded above (new entries appeared before
  `knowledge-expected.txt` was regenerated — the exact R6 / round-29 pattern, not a harm).
- **No owned axis score changes**: depth:density **9** held (density mean change disclosed, not
  claimed); depth:verifiability **4** held; coverage **7** held. PROVINCE.md hash unchanged.
  Consistent with SCORECARD round-29 close-out (depth:verifiability 4, coverage 7, density 9).
- Scope/safety: no write to fleet root, sibling lanes, `shokuknow`, lane git/jj state,
  `.ufo/state`, or MANIFEST.json; no live target contacted; no tool installed; no production file
  edited by this seat.
