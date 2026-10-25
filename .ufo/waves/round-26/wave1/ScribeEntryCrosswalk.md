# ScribeEntryCrosswalk — round-26 wave-1 report

Role: UFO-FSD scribe leaf (L1Kasegi26.ScribeEntryCrosswalk). Lane: kasegi-shokunin, base `1b076fa7f2fb5e7dd9d87449514eba526043421b`. Item: F11 entry (crosswalk) under frozen claim C2 (coverage).

## Behavior

Created `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (sole owner) — **67 lines**, 10,547 bytes.

- Headers directly under H1 (Q1): `source: S041` (line 3), `verified-at: 2026-10-25` (line 4), `recheck:` = the exact mandated command (line 5): `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041`.
- `## Ground` one-liner: "Adopts the staged entry `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` re-grounded on the fresh S041 capture of the JPCERT/CC 2026-10 guideline (2026-10-25)" (lines 8-9).
- Content (all load-bearing claims rest on S041, tier-A, opened this round — Q2):
  - The P-guideline's own contrast sentence (`S041.txt:1868-1870`): the guideline does not require a vendor to adopt a disclosure policy; ISO/IEC 29147:2014 does require formulation and publication of part of it. No-major-contradiction claim attributed to §3 (`S041.txt:1680-1681`).
  - Operational additions the guideline names for conforming vendors: documentation + record-keeping, pre-notified updates for online services, policy contents list, external window, 7-day receipt, intermediate-vendor triage (L1697-1732, L1778-1791, L1873-1884, L1913-1916, L1984-1992).
  - 6.2/6.3 republication: minimum six lettered elements a)-f) (L1813, L1819-1835, Japanese L1838-1855) vs optional three a)-c) (L1856, L1859-1861, Japanese L1862-1866).
  - 参考1 clause cross-reference table (p.53-54, L1996-2079), noting clause 6 and clause 8 rows read "－" (no guideline counterpart; L2027-2028, L2054-2059).
  - S040 (Cisco) referenced only as the real-world example the guideline itself cites in 参考2 (L2086-2088, URL matches the R25-5 final URL); the alignment claim ("The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018", S040.txt:58) is pointed to the round-25 F10 entry and not re-made here, so the header `source:` keeps only S041 and the R12 recheck-coverage rule holds.

Quotes, all located at `S041.txt:<line>` (manifest id where one exists):

| id | manifest | verbatim | location |
|---|---|---|---|
| q-policy-not-required | Q3 | "P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません" | S041.txt:1868 |
| q-policy-required | — | "ISO/IEC 29147:2014 では、脆弱性公開ポリシーを策定することや、その一部を公開することを求めています。" | S041.txt:1869-1870 (wraps; matches under declared markup-whitespace normalization, Q8) |
| q-seven-day-receipt | Q4 | "受信した旨を 7 日以内に返信することが必要となります。" | S041.txt:1916 |
| q-min-policy-aspects | Q5 | "6.2 Minimum policy aspects" | S041.txt:1813 |
| q-optional-policy-aspects | — | "6.3 Optional policy aspects" | S041.txt:1856 |
| q-secure-comm-option | Q2b | "b）セキュアな通信オプション" | S041.txt:1851 |

Four falsifiable rules and three rejected over-generalizations included (Q5); attribution kept throughout (Q4); no probing/scanning instruction (Q6).

## Verification (evidence, run 2026-10-25 UTC)

- Mandated recheck command, run from the lane root: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041` → exit **0**; output: `S041:sha256 OK`; `Q1a OK occurrences=1`, `Q1b OK occurrences=1`, `Q2a OK occurrences=2 anchor=1874-ok`, `Q2b OK occurrences=1`, `Q3 OK occurrences=1`, `Q4 OK occurrences=1`, `Q5 OK occurrences=1`.
- Recheck line parses under `bash -n` (exit 0).
- Capture `S041.txt` sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` equals the manifest sha256.
- Occurrence audit under the instrument's normalization (markup-whitespace): q-policy-not-required → 1; q-seven-day-receipt → 1; "6.2 Minimum policy aspects" → 1; "6.3 Optional policy aspects" → 1; "b）セキュアな通信オプション" → 1; "6.脆弱性公開ポリシーにおける考慮事項" → 1; U+FFFD count in capture → 0.

## Discrepancy: assigned quote vs capture (recorded per honesty rule)

The assignment's quote "ISO/IEC 29147:2014 では、脆弱性公開ポリシーを策定することや、その一部を公開することが必要" does **not** occur verbatim in `S041.txt` (0 hits raw and normalized). The capture's actual wording is "…その一部を公開することを求めています。" spanning L1869-1870 (the PDF line wrap splits at その一/部). The entry quotes the verbatim capture sentence and declares the wrap; the differing phrasing is noted here rather than fabricated. The manifest (built by ExecManifestRecheck; not an owned path, not edited) carries no assertion for q-policy-required or q-optional-policy-aspects; their occurrence counts were verified directly as above.

## Gates / quality

- Q1-Q10 addressed as above; Q9 satisfied (quotes exactly-once in capture; Q2a anchor verified `1874-ok` by the instrument).
- Hard rules: wrote only owned paths (entry + this report); no VCS writes (no git/jj mutations); no fleet-root writes; no installs performed (no new tool needed; all pacman transactions untouched).
- `source-recheck.py --source` is single-valued, so the mandated single-source recheck line is used as given (round-25 routed debt unchanged).

## Touched surfaces

- `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (created — 67 lines)
- `.ufo/waves/round-26/wave1/ScribeEntryCrosswalk.md` (this report)

## Out of scope (other seats' owned paths, not touched)

- `corpus/README.md` frontier row / `corpus/SOURCES.md` S041 registry row updates (executor/registry seats).
- The sibling division-of-labour entry `iso-29147-and-30111-division-of-labour.md`.
- `corpus/source-snapshots/round-26/manifest.json` (ExecManifestRecheck).
