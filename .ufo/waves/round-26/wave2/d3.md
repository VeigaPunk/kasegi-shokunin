# AttackD3 — LOG.md round-26 entry / PROVINCE.md F11 sentence spot-check vs final state

Seat: L1Kasegi26.AttackD3 (leaf, read-only). Wave 2, round 26.
Item: spot-check LOG.md round-26 entry and PROVINCE.md F11 sentence for factual consistency with the final state (frontier 11, S041 row, census 0, receipt digest). Quote any discrepancy.

## Verdict

No factual discrepancy found. All four named final-state facts are consistent with the LOG.md round-26 entry and the PROVINCE.md F11 sentence, with the observed measurements below. Two nuances are recorded (instrument digest timeline; "meta" qualifier), both documented elsewhere and not inconsistencies.

## What was checked (evidence)

1. **Frontier 11** — `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → `11` (ran). `corpus/README.md` F11 row: `| F11 | ISO/IEC 29147/30111 division-of-labour meta | admitted | knowledge/iso-29147-and-30111-division-of-labour.md, knowledge/iso-29147-divergence-and-clause-crosswalk.md | S041 | … |`.
   - LOG.md:1305/1310 says "Frontier 10 → **11** …" — consistent.
   - PROVINCE.md:38-41 says "under Frontier F01–F10 (…; 10/10 admitted). F11 — ISO/IEC 29147/30111 division-of-labour (JPCERT/CC 2026 guideline) — admitted round 26" — consistent (F01–F10 rows are all `admitted`; F11 has its own sentence).
2. **S041 row** — `corpus/SOURCES.md` row 47 exists: `S041 | 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC) — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf | spec | A | … | mined | 2026-10-25 | 180d | corpus/knowledge/iso-29147-and-30111-division-of-labour.md, corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`. Recheck cell is the bare cadence `180d` (per the `## Registry changes` note). LOG.md:1310 "staged S076 … / S064 … adopted by document as **S041**" — consistent. Manifest `corpus/source-snapshots/round-26/manifest.json` binds S041.txt sha256 `e18acbf9…`, 147,267 B — matches LOG.md:1311 ("snapshot 147,267 B, sha256 `e18acbf9…`").
3. **Census 0** — reran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit `0` (same two pre-existing W04 warnings S028/S029). LOG.md:1310 "sources census … exits 0 at round end" — consistent.
4. **Receipt digest** — `.ufo/waves/round-26/c1-instrument-digest.txt` and `c1-receipt-index.txt` carry `instrument=3fc0d751f2a58…`; `sha256sum corpus/instruments/recheck-audit.py` → `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` (matches). Selftest receipt line present: `selftest cases=15 failures=0 exit=0` (grep count 1). Live audit in `c1-live.json`: `lines=39 pass=39 strict=39`, `expect=present expected=39 missing=0 unexpected=0`, exit 0. `corpus/instruments/knowledge-expected.txt` holds 39 entry lines (2 header comments).

## Nuances (checked, not discrepancies)

- **Instrument digest timeline.** LOG.md:1309 records "Instrument unchanged at freeze, `recheck-audit.py` sha256 `c3c19adc…`". The landed digest is `3fc0d751…`. This resolves inside the receipt files themselves: `c1-receipt-index.txt`/`c1-instrument-digest.txt` carry `base_sha256_control=c3c19adc…  # pre-change bytes (round-25 pinned digest)` and a regeneration-history note ("regenerated at the landed instrument digest 3fc0d751… after ExecAuditFix landed (selftest cases 14 → 15; expect-list active; expected list regenerated to 39 entries)"). LOG.md:1311 "Tools touched … `recheck-audit.py` expected-list contract" explains the change. So the LOG's `c3c19adc…` is a freeze-point statement; the final receipt digest is `3fc0d751…` — both correct for their point in time, no conflict.
- **PROVINCE F11 topic wording** omits the README topic qualifier "meta" ("division-of-labour meta" vs "division-of-labour"). Cosmetic, not factual.
- LOG.md:1310's "at write, 1 knowledge file matches `^source: S04[0-9] ` — the round-25 F10 entry's S040" is an at-write observation; final grep now matches 3 files (the round-25 S040-citing entry + the two S041-citing F11 entries: `iso-29147-and-30111-division-of-labour.md`, `iso-29147-divergence-and-clause-crosswalk.md`), satisfying C2's ≥1 first-registered-this-round citation. No contradiction with the target sentence.

## Residual risk / verification gaps

- The deletion-fixture exit (C1(d) exit 1 naming the missing entry), fix-control restated BRE 0, frontier-recheck-count 14/14, and registry row grep 1 were not re-run by this read-only seat; they were measured by the L1 at integration time (census exit 0; frontier-recheck-count 14/14 exit 0; live audit 39/39 exit 0 expect=present; deletion fixture exit 1 missing=<name>; registry grep 1; selftest receipt line 1; fix-control restated BRE 0; awk frontier 11; precise S041-citing entries 2). The c1 receipts mirror those numbers (39/39, expect=present, cases=15).
- SCORECARD.md round-26 rows were out of scope for this item (LOG.md + PROVINCE.md only).

## Tooling

No tool installed or upgraded; no pacman transaction attempted (host-wide pacman paused).
