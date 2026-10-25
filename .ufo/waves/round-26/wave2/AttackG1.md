# AttackG1 — final deliverables presence checklist (wave 2)

Seat: `L1Kasegi26.AttackG1`. Date: 2026-10-25 UTC. Mode: read-only; this report is the only write.
Item attacked: the wave-1 claimed AFTER state's final deliverables (contract milestones checklist).
Verdict: **13/14 deliverable groups present and non-empty; 1 gap — the `wave2/` report directory did not exist at check time** (in-flight wave-2 output; this report is its first artifact).

Tool installs: none (no tool needed beyond cores; no installs to record).

## Checklist (exists + non-empty)

| Deliverable | Path (lane-relative) | Exists | Non-empty | Evidence |
|---|---|---|---|---|
| Knowledge entry 1 | `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` | yes | yes | 6769 bytes |
| Knowledge entry 2 | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` | yes | yes | 10547 bytes |
| SOURCES S041 row | `corpus/SOURCES.md` line 47 | yes | yes | full row read raw; recheck cell bare `` 180d `` |
| SOURCES S040 row recheck cell | `corpus/SOURCES.md` line 46 | yes | yes | full row read raw; recheck cell bare `` 180d ``; prose recorded under `## Registry changes` (lines 74–76) |
| README F11 (names aligned) | `corpus/README.md` line 212 | yes | yes | F11 entry cites `knowledge/iso-29147-and-30111-division-of-labour.md, knowledge/iso-29147-divergence-and-clause-crosswalk.md` — matches actual filenames exactly |
| Lesson round-26 Gate/fixes/appendix | `corpus/lessons/round-26.md` | yes | yes | headings present: `## Gate — the assimilation set`, `## Fixes that can fail`, `## Appendix — counters, confirmation and access-date evidence` (plus Mistakes / Routed debt / Integration closure) |
| SCORECARD round-26 rows | `SCORECARD.md` | yes | yes | `## Round 26 — frozen claims C1/C2` section with C1 and C2 rows + round-26 capabilities row |
| knowledge-expected.txt (39) | `corpus/instruments/knowledge-expected.txt` | yes | yes | 41 lines = 2 `#` header lines + exactly 39 entry lines; both new knowledge entries listed; instrument receipt agrees (`expect=present expected=39 missing=0 unexpected=0`) |
| c1-receipt-index.txt | `.ufo/waves/round-26/c1-receipt-index.txt` | yes | yes | 1145 bytes; `instrument_sha256=3fc0d751…`, `selftest cases=15 failures=0`, live audit `strict pass=39/39` |
| c1-instrument-digest.txt | `.ufo/waves/round-26/c1-instrument-digest.txt` | yes | yes | 192 bytes; instrument `3fc0d751…`, base `c3c19adc…` |
| c1-live.json | `.ufo/waves/round-26/c1-live.json` | yes | yes | 40048 bytes; valid JSON dict; `pass=39`, `pass_strict=39`, `fail_closed=23`, `expect=present` |
| manifest.json | `corpus/source-snapshots/round-26/manifest.json` | yes | yes | 2517 bytes; S041 sha256 `e18acbf9…`, 7 pinned quotes |
| S041.txt | `corpus/source-snapshots/round-26/S041.txt` | yes | yes | 147267 bytes; PDF capture head confirmed (JPCERT signature block) |
| S040-live.txt | `corpus/source-snapshots/round-26/S040-live.txt` | yes | yes | 33463 bytes; Cisco policy page capture head confirmed |
| c1-controls/ | `.ufo/waves/round-26/c1-controls/` | yes | yes | 11 direct entries incl. `fixtures/` |
| c2-controls/ | `.ufo/waves/round-26/c2-controls/` | yes | yes | 2 direct entries (`m3-gameability.txt`, `do-nothing.json`) |
| wave1 reports | `.ufo/waves/round-26/wave1/` | yes | yes | 55 report files |
| wave2 reports | `.ufo/waves/round-26/wave2/` | **no (at check time)** | — | directory absent; no wave-2 report file found anywhere under `round-26/` before this write |

## Gap

1. **`wave2/` directory/reports missing at check time** — the only gap found. The wave-2 run is in flight (seats still running); at this check no `round-26/wave2/` directory existed and no wave-2 report file was present anywhere under `round-26/` (only `wave2-dispatch.json` / `wave2-spec.json` / `build-wave2-spec.py` spec artifacts in the round root). This report is written into that directory and is, at write time, the sole wave-2 report artifact; the gap is closed only when the remaining wave-2 seats land. All other 17 deliverable groups were present and non-empty at check time.
