# ScoutQuoteRelocation — S5 quote re-location (round 26, wave 1)

UTC access date: 2026-10-25. Seat: L1Kasegi26.ScoutQuoteRelocation (leaf, no subagent dispatch, no production edits).

## Assignment
Independently re-locate in the ORIGINAL source (not lane capture) the quotes used by the two staged target entries (`iso-29147-and-30111-division-of-labour-2026-10-23.md` → staged S076; `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` → staged S064) from `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf`.

## What I did
1. Fetched the PDF with the instrument UA (`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, same UA as `capture-source.py`): HTTP 200, 1,338,665 bytes, sha256 `0ff7a6b6b4fa4a9aeffa924e9a1775fbcf044773d79491e0d47aca78eb004f03`. pdfinfo: PDF-1.7, 64 pages A4, Producer “Microsoft® Word for Microsoft 365”, CreationDate 2026-09-28T22:54:43-03:00.
2. Ran `pdftotext` (v26.08.0, Poppler; no `-layout`) three ways: full text (2,860 lines), PDF pages 45-47 (`-f 45 -l 47`), PDF pages 53-54 (`-f 53 -l 54`). sha256 of extractions: full `eee97733f127850429f5033e88d8e72341a11be445085d3e663f2c604045e8a5`, p45-47 `4c200c420fd791d19c43d1544053039fffd210eb605564dc1db72d3a89358993`, p53-54 `31a706e52ce5843c4fcd683a08e67b8de7dc401983ec2345aac0f6745a7f1dbc`.
3. Matched every quote under whitespace normalization (all whitespace stripped), reporting the exact extracted line numbers (single-line and multi-line match starts).

Full detail in `.ufo/waves/round-26/wave1/s5-quote-relocation.txt`.

## Findings (exact extracted lines)

Pagination note: the PDF carries a constant +2 offset vs the printed page numbers (printed p.N = PDF page N+2; PDF page 47 prints “45”).

| Quote | FULL text line(s) | PDF page (= printed) | p45-47 file | p53-54 file |
|---|---|---|---|---|
| 30111 division-of-labour sentence (“ISO/IEC 30111:2013 は…指針を提供します。”) | 2009–2010 (2 lines) | 47 (=45), rel 23-24 | 114–115 | — |
| 図1 caption “（出所：ISO/IEC 29147:2014 を元に作成）” — 5 occurrences | 2020 / 2140 / 2237 / 2283 / 2355 | 48(=46) / 50(=48) / 52(=50) / 53(=51) / 54(=52) | — | 32 (2283) / 104 (2355) |
| §4(2) divergence “P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません” | 2238 | 52 (=50), rel 34 | — | — |
| 7-day acknowledgement “受信した旨を 7 日以内に返信することが必要となります。” | 2291 | 53 (=51), rel 40 | — | 40 |
| 6.2 Minimum policy aspects | 2180 | 51 (=49), rel 27 | — | — |
| 6.3 Optional policy aspects | 2225 | 52 (=50), rel 21 | — | — |
| 参考1 header “参考 1 ISO/IEC 29147:2014 と情報セキュリティ早期警戒パートナーシップガイドラインの対応” | 2382–2383 | 56 (=54), rel 3-4 | — | — (table body continues on PDF 57 = printed 55) |

Context anchors: §2 “2. 国際標準の概要” FULL 2004; §4 heading FULL 2036 (printed 47); (2) 脆弱性公開ポリシー FULL 2158; (3) 脆弱性の受領 FULL 2261; (4) 中間ベンダ FULL 2294. Related shorter table-row variant “受信した旨を 7 日以内に返信する。” FULL 2076 (PDF 49 = printed 47).

## Staged-anchor deltas (observed in the original PDF)
- S076 anchor “p.45” for §2 holds for the 30111 sentence, but the 図 1 caption is on printed p.46 (PDF 48), not p.45.
- S064 anchor “§4 p.46-47” does not match the clause reproductions: §4 heading is on printed p.47 (PDF 49), (1) printed 48, (2) printed 49-50 (6.1/6.2/6.3 + divergence sentence), (3) printed 51, (4) printed 51-52.
- S064 anchor “参考1 p.53-54” is one page early: the 参考 1 header/table sits on printed p.54-55 (PDF 56-57).
- The exact 7-day quote (with “ことが必要となります”) is the §4(3) closing recommendation (FULL 2291, printed 51); the summary-table row on printed 47 uses the shorter “…返信する。” form.

## Verification
- All five “（出所：ISO/IEC 29147:2014 を元に作成）” occurrences counted by scanning the normalized joined full text (exactly 5; each is single-line).
- Every multi-line quote start line double-checked against both the full-text and page-range extractions; the p45-47/p53-54 file line numbers were cross-derived from the full-text page map and verified by direct file search.
- No tool installations performed (pdftotext 26.08.0 already present; python3/urllib standard). No production edits; outputs are this report and `s5-quote-relocation.txt`.

## Gate
- Access date: 2026-10-25 (UTC). Source URL opened 2026-10-25, HTTP 200, sha256 of PDF bytes `0ff7a6b6…f03`.
- The two output files are the only writes by this seat.
