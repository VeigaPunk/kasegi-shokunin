# ScribeEntryDivision — F11 knowledge entry: ISO/IEC 29147/30111 division of labour (wave 1, round 26)

- Seat: `L1Kasegi26.ScribeEntryDivision`
- Date: 2026-10-25 (UTC)
- Scope: create `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` (sole owner) satisfying QUALITY.md Q1–Q9 for C2/F11; report file + line count.

## File created

- `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` — **54 lines**, 6769 bytes.

## Headers (Q1, directly under H1)

- `source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 付録6 §2 p.45, division paragraph L1667-1672 and 図1 L1676-1678 (capture corpus/source-snapshots/round-26/S041.txt)`
- `verified-at: 2026-10-25`
- `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041` (exactly as assigned)
- `ground: F11 — this entry adopts the staged entry iso-29147-and-30111-division-of-labour-2026-10-23.md, re-grounded on the round-26 capture of the JPCERT/CC 2026 P-guideline (S041, 付録6 §2)` (one line)

## Content

- Claim: S041 付録6 §2 divides labour — 29147:2014 = the vendor's outward-facing dealings ("社外とのやりとり", L1669): receiving vulnerability info from outside and distributing advisories to users (L1669-1670); 30111:2013 = the in-house process: verification and mitigation development (L1671-1672). 図1 (L1676-1678) shows the correspondence, based on 29147:2014.
- Supporting mined rows: S039 Hitachi HIRT three-step mapping (L497 → 29147:2014; L498 → 30111:2013; L499 → 29147:2014) and S040 Cisco PSIRT alignment with 29147:**2018** (L58).
- 7 S041 quotes + 3 S039 quotes + 1 S040 quote, all verbatim contiguous substrings preserved ≤70 chars, with `S0XX.txt:<line>` locations in a `## Source`-style quoted-record table (two wrapped fragments pinned as manifest Q1a/Q1b; 図1 caption carries anchor L1678 because the string repeats at L1777/L1867/L1908/L1974).
- Two falsifiable rules (classification by direction; edition rule with concrete grep counts) and two rejected over-generalizations (29147 = intake only; "vendors follow 29147:2014") — Q5.
- Attribution kept per party (JPCERT/CC guideline, Hitachi HIRT, Cisco PSIRT) — Q4. Documentation-only, no credentials/probing — Q6.

## Verification exercised (commands actually run)

- `wc -l` → 54 lines.
- `bash -n -c '<recheck line>'` → PARSE_OK (Q10: parses, self-contained `cd` prefix).
- From `/tmp` cwd, the exact recheck line: exit 0; `S041:sha256 OK`; all pinned quotes OK (Q1a/Q1b occurrences=1; Q2a occurrences=2 anchor=1874-ok; Q2b/Q3/Q4/Q5 occurrences=1). sha256 e18acbf… matches the manifest and the capture log.
- Edition grep counts used in rule 2: `grep -c '29147:2018' corpus/source-snapshots/round-25/S040.txt` = 1; `grep -c '29147:2014' corpus/source-snapshots/round-26/S041.txt` = 24 (also 30111:2013 = 2 in S041, 3 in S039).

## Notes / limits

- The staged entry file `iso-29147-and-30111-division-of-labour-2026-10-23.md` does not exist anywhere in the lane or fleet (referenced only in wave specs/logs); the Ground line records the adoption-as-required without inventing its bytes.
- S041 is a pdftotext capture; two quoted sentences wrap across lines, so the 30111 sentence is pinned as the two manifest fragments Q1a/Q1b and the outward enumeration fragment starts at the wrapped word — matching the lane's Q8/Q9 conventions.
- Only my owned path was written; no VCS writes, no edits to claims/lessons/README/SOURCES.
