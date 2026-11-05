# DRAFT — SCORECARD.md "## Round 76" section skeleton (ScribeLedger, not applied)
# Placement: end-of-file append after SCORECARD.md's last line (the r75 section's last line), per R6. Every <FILL> is an evidence value the L1 measures at integration; scores are carried from the r75 section. This header is not part of the text.
==========

## Round 76 — the recheck-cwd census forged-relabel kill, load-bearing RESULT limb and both-headers fixture (C1, depth:verifiability, nominal 4 held per R58) and F54, the OSV.dev API overview on S111 (C2, coverage, held at 8)

Frozen claims: `.ufo/waves/round-76/claims.json` (freeze `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e`, base `a788021675873a96e09e91aa033d8c26ac2fe212`, controls committed at the freeze). Wave `w1` (13 seats). Measured on the landed bytes at integration; no self-referential hash is asserted here.

| Axis | Score before r76 | Score after r76 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | <FILL: 4 (held, nominal per R58) — state the verdict on A1-A5> | `corpus/instruments/recheck-cwd-census.py`; selftest `cases=6 failures=0` → <FILL: cases=8 failures=0>; real-tree census base `entries=91 … restoration_only=0` → <FILL: diff vs base receipt>; receipt `.ufo/waves/round-76/controls/` <FILL: landing receipt name> | r76 |
| coverage | 8 | 8 (held; F54 admitted; the denominator is operator-owned) | `frontier-recheck-count.py` base `rows=53 admitted=53 … entries=56` → <FILL: rows=54 … FRONTIER-PASS F54 ids=S111, entries=57 pass=57>; `capture-binding-check.py` base `records=89 bound=89` → <FILL: records=90 bound=90>; receipts `.ufo/waves/round-76/controls/c2-base-counters-r76.txt` (base) and <FILL: landing receipt> | r76 |
| depth:density | 9 | 9 (not targeted; not re-measured) | — | r15 (held) |

Claim verdicts. C1: <FILL: VERIFIED or FAILED on frozen A1-A5; any mutant that survived the amended selftest named; kill rule state>. C2: <FILL: VERIFIED or FAILED on frozen B1-B7; distinctness B6 state; kill rule state>. No predicate was rewritten after any seat scored.

Counting commands and their receipts: `corpus/lessons/round-76.md` § Counters and § Counting commands.

### Round-76 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 76 | depth:verifiability | census selftest `cases=6`; census has no pair case for a neither-header file and no both-headers fixture | <FILL: selftest cases=8; the three red-before mutant classes each exit nonzero> | <FILL: landing receipt>; `corpus/instruments/recheck-cwd-census.py` |
| 76 | coverage | rows=53 registry=110 entries=56 capture=89 knowledge=91 | <FILL: rows=54 registry=111 entries=57 capture=90 knowledge=92>; F54/S111 admitted | `.ufo/waves/round-76/controls/c2-base-counters-r76.txt`; <FILL: landing receipt>; `corpus/knowledge/osv-api-surface-and-limits.md`; `corpus/source-snapshots/round-76/` |
| 76 | calibration | <FILL: any QUALITY criterion adopted this round, with its before state> | <FILL: after state> | <FILL: `corpus/QUALITY.md` lines> |

Saturation: <FILL: line per owned axis; lowest non-retired axis remains depth:verifiability (4), worked nominally unless C1 verifies on its frozen predicate>. No retirement, split or nudge waiver.

### Planned after round 76 (not frozen)

1. **depth:verifiability (4, lowest):** <FILL: the residual classes this wave's attack seats find, named by class and by file; M75-4- and M75-5-style routing or misroot classes count here if the wave reproduces them>.
2. **coverage (8):** the five non-query OSV endpoint contracts as candidate frontier rows, each needing its own capture, manifest and entry: `POST /v1/querybatch`; `GET /v1/vulns/{id}`; `GET /v1experimental/importfindings`; `POST /v1experimental/determineversion` (the capture renders this path with an interior space at S111.txt lines 8 and 46; a row must quote the path it names from its own capture); `POST /v1experimental/ubuntu/binary-to-source`. None is claimed in round 76.
3. **calibration:** <FILL: any new QUALITY criterion the round mines, and the frozen-clause amendment it routes>.
