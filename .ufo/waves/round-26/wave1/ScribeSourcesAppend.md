# ScribeSourcesAppend — SOURCES.md append block (wave 1, round 26)

- Seat: `L1Kasegi26.ScribeSourcesAppend` (SOLE OWNER of `corpus/SOURCES.md` edits this round)
- Date: 2026-10-25 (UTC)

## Behavior

Appended the S041 row (JPCERT/CC 2026 partnership guideline) to
`corpus/SOURCES.md`, updated the S040 row's `recheck` cell old→new per R25-5, and
logged the change in a `## Registry changes` note at the bottom. No other row was
altered.

## Exact appended lines

New S041 row (line 47):

```
| S041 | 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC) — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf | spec | A | The JPCERT/CC 2026 partnership guideline's annex (付録6) on international-standard conformance: the mapping between the early-warning framework and ISO/IEC 29147:2014 / ISO/IEC 30111:2013, plus the points where conforming to 29147 requires more than the guideline states | 付録6 §2 p.45 (ISO/IEC 29147:2014 vs ISO/IEC 30111:2013 division of labour, 図1), §4 p.46-47 (points to note when conforming to ISO/IEC 29147:2014: vulnerability disclosure policy, 7-day receipt acknowledgement, intermediate vendors, online services), 参考1 p.53-54 (clause correspondence table ISO/IEC 29147:2014 ↔ P-guideline) | ISO/IEC 29147:2014 and ISO/IEC 30111:2013 divide labour between a vendor's outward-facing disclosure and its in-house handling; the P-guideline maps onto both, and 参考1 pairs each 29147 clause with its guideline section, exposing divergences where a 29147-conforming vendor must go beyond the guideline (e.g. a 7-day receipt acknowledgement). | mined | 2026-10-25 | 180d — re-fetch with capture-source.py instrument UA (browser UA 403s); canonical anchor is the PDF | corpus/knowledge/iso-29147-and-30111-division-of-labour.md, corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md |
```

`## Registry changes` note (tail of file):

```
## Registry changes

- S040 recheck cell old → new: `180d` → `180d — final URL https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html (2 redirects); instrument UA required (browser UA 403s)` (R25-5).
```

S040 row (line 46) recheck cell, old → new:

- old: `180d`
- new: `180d — final URL https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html (2 redirects); instrument UA required (browser UA 403s)`

All other S040 cells byte-identical to the base (git diff shows a single hunk per row).

## Gates

- S041 `used-by` names exactly the two F11 entries w2/w3 are drafting
  (`corpus/knowledge/iso-29147-and-30111-division-of-labour.md`, `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` — names confirmed from `.ufo/waves/round-26/build-wave1-spec.py` w2/w3 task specs and `wave1-dispatch.json`). Only S041 was appended; no other staged row is cited by an admitted entry, so none was added (C2 kill rule).
- Row shape: 11 columns, no pipe swallowed (verified per-row `split("|")` → 11 cells for S040 and S041).
- Only S040/S041 carry the new recheck text; all other rows still read plain cadences (`180d`/`90d`/`730d`/`on-release`).
- `git diff` (read-only, lane root): `corpus/SOURCES.md | 7 ++++++-`, `1 file changed, 6 insertions(+), 1 deletion(-)` — the deletion is the old S040 line, insertions are the S041 row + `## Registry changes` block. No other rows touched.

## Provenance

- Capture evidence: `.ufo/waves/round-26/wave1/ExecCaptureS041.md` — `capture-source.py --id S041 --url https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf` exit 0, http 200, `fetched_bytes=1338665`, `snapshot_bytes=147267`, sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` (matches on-disk `sha256sum`), utc `2026-10-25T12:34:17Z`, snapshot `corpus/source-snapshots/round-26/S041.txt` (2354 lines, pdftotext 26.08.0).
- Anchor grounding in `S041.txt`: 付録6 starts at line 1652 (TOC: 付録６ → p.45); §2/図1 division-of-labour block at lines 1667–1678; §4 "ISO/IEC 29147:2014 について留意すべき事項" at line 1691 (7-day receipt acknowledgement at lines 1720–1722, online services 1734–1789, intermediate vendors 1920–1991); 参考1 correspondence table at lines 1996–2053 (maps ISO/IEC 29147:2014 clauses, e.g. 5.2, to P-guideline sections incl. 5. 製品開発者の対応).
- S040 R25-5 basis: `corpus/lessons/round-25.md` R25-5 ("registry URL now 301-redirects to sec.cloudapps.cisco.com/… and 403s a browser UA; record the final URL / UA requirement in the row's next recheck") and `round-25-verifier-spotcheck.md` (browser UA 403; instrument UA returns 200).

## Known limits

- The two F11 entries were still being drafted by w2/w3 at report time; the source census (`sources-census.sh validate`) is a round-end check and was not run here.
- No manifest for round-26 captures exists yet (executor e6 owns it); `source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041` will be the entries' recheck.
- No tool installed or updated (pdftotext pre-existing; no pacman transaction).

## Files changed

- `corpus/SOURCES.md` (this seat only).
- `.ufo/waves/round-26/wave1/ScribeSourcesAppend.md` (this report).
