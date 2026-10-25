# AttackD2 — SCORECARD.md round-26 rows vs evidence pointers (scorecard consistency)

Role: L1Kasegi26.AttackD2 (leaf, read-only; report under wave2/).
Date: 2026-10-25 (UTC). Target: /home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md.

## Verdict summary
No drift found in any of the four checked pointers. All four checks PASS.

## 1. C1 row evidence file exists and matches current receipt — PASS
- Scorecard r26 C1 row (line 576) and the section lead (line 572) point to
  `c1-receipt-index.txt` under `.ufo/waves/round-26/`. File exists.
- Receipt matches the current (landed) instrument state:
  - Receipt line 2 `instrument_sha256=3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`
    == computed sha256 of live `corpus/instruments/recheck-audit.py`
    (3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1).
  - Same value in `c1-instrument-digest.txt`; `base=c3c19adc…` matches the receipt's
    `base_sha256_control`.
  - Receipt line 4 `selftest cases=15 failures=0 exit=0`: live `python3
    corpus/instruments/recheck-audit.py --selftest` ran with EXIT=0 and zero FAIL
    lines; code counts 13 per-entry fixtures + 2 tree-level expected-list fixtures
    (`total_cases = len(cases) + 2`) = 15, matching the receipt line.
  - Receipt references `c1-live.json` (exists in `.ufo/waves/round-26/`).
- No drift.

## 2. C2 row names match actual filenames — PASS
- Scorecard r26 C2 row entry paths:
  `knowledge/iso-29147-and-30111-division-of-labour.md` and
  `knowledge/iso-29147-divergence-and-clause-crosswalk.md`.
  Both files exist in `corpus/knowledge/` with exactly those names (directory
  listing; no dated suffix).
- `corpus/README.md` § Frontier F11 row (line 212) is `admitted` and cites the
  same two entry paths and S041.
- Both entries carry `source: S041 — …partnership_guideline2026.pdf …` with capture
  path `corpus/source-snapshots/round-26/S041.txt`; S041 source row exists in
  `corpus/SOURCES.md` (line 47, category spec, PDF URL).
- Observation (not scorecard drift): claims.json `staged_entries` used dated names
  (`…-2026-10-23.md`); the landed files are undated. The rename is recorded in
  each entry (`ground:` / `## Ground` line: "adopts the staged entry …-2026-10-23.md"),
  and the scorecard C2 row matches the actual filenames — so no drift on the
  checked surface.

## 3. Capability row source-capture-pdf evidence exists — PASS
- Scorecard capabilities row (line 584) evidence pointer: `capture-source.py`
  (`--kind pdf`); `corpus/source-snapshots/round-26/manifest.json` + `S041.txt`
  (sha256 `e18acbf9…`, 7 pinned quotes).
- `corpus/instruments/capture-source.py` exists; `--kind` choices include `pdf`;
  `pdf_to_text` uses `pdftotext -enc UTF-8` (poppler required, official binary).
- `manifest.json` exists; S041 record sha256
  `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`
  (prefix `e18acbf9…` matches) with 7 quote records (Q1a, Q1b, Q2a, Q2b, Q3, Q4, Q5).
- `S041.txt` exists; computed sha256 == manifest record exactly.

## 4. r27 planned row is plan-only, not marked done — PASS
- `## Planned` section: "**Round-26 planned for round 27** … The plan rows below
  are plans, not commits:" followed by two prose bullets (depth:verifiability
  `anchorcheck.py`/`CITE` arm; coverage frontier continuation). No verdict cells,
  no done markers, no result table.
- Saturation paragraph: "Planned round 27: see `## Planned` above."
- No Round-27 result section exists in SCORECARD.md (sections end at Round 26 +
  capabilities).

## Residual risk / verification gaps
- The live lane audit 39/39 is attested by `c1-live.json` (referenced by the
  receipt) and was not rerun; out of scope for the four evidence-pointer checks.
- No tools installed (only sha256sum/python3, both pre-existing). No VCS mutations.
