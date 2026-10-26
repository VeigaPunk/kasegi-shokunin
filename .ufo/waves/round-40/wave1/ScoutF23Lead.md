# ScoutF23Lead — round 40 wave 1 receipt (F23: CycloneDX v1.7 analysis subtree)

Deliverables beside this receipt: `ScoutF23Lead.capture.txt`, `ScoutF23Lead.manifest-record.json`. No lane file other than these was written; scratch `/fast/scratch/hyaku/kasegi-r40/ScoutF23Lead/` removed at yield. No tools installed.

## Captured source
- URL https://cyclonedx.org/docs/1.7/json/ (the CycloneDX v1.7 JSON Reference; page header "v1.7 October 2025, ECMA-424, 2nd Edition"). Command: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`.
- Fetch 1: HTTP 200, `text/html; charset=utf-8`, final URL = requested, 0 redirects, 6419901 bytes, 2026-10-26T21:16:18Z, raw sha256 `4d9c10da73aedb78727cbfeefd2a07551f25acae92a0dc6900cd976d6e947874`.
- Fetch 2: HTTP 200, 6419901 bytes, 2026-10-26T21:17:05Z, raw sha256 `9a551897fa5fb7eaa3dd935d84800386c52c13714c6e30eb82f3b710622be6c6` — **differs**: 3936 bytes differ, first at byte 74039, all inside Cloudflare `data-cfemail` email-obfuscation tokens. The `capture-source.py html_to_text()` full-page text is identical on both fetches: sha256 `ffe8c0b6c155dab46098754e7ee757c441f230810fd353135fb2bd149f5ba7f4`, 1041903 bytes, 22795 lines. Consequence: record `raw_sha256` as non-reproducible; the normalized text / slice digests are the reproducible binding.
- Secondary (not captured): spec repo schema `https://raw.githubusercontent.com/CycloneDX/specification/master/schema/bom-1.7.schema.json` HTTP 200, 315722 bytes, sha256 `73308edec3ab2d38bfffd993e96a042b594314143b6971a6e9ed98bbb6bd76ce`, 2026-10-26T21:16:18Z; `definitions.vulnerability.properties.analysis` has the same state/justification/response/detail/firstIssued/lastUpdated members (the `$ref`s are `impactAnalysisState`/`impactAnalysisJustification`). It is a mutable `master` URL, so not chosen as the pinned capture.

## Minimum scoped capture (determination)
The full text is 1.04 MB (6.4 MB raw) and only ~110 lines are on-point. Committed capture = **slice of the normalized page text**: capture L1 = page-text L1 (title/version line, binds "v1.7"); capture L2-L111 = page-text L16060-L16169 (capture line k>=2 = page line 16058+k): `vulnerabilities[].analysis` subtree (L16060-L16107 page; `state` L16064+, `justification`, `response`, `detail`, `firstIssued`, `lastUpdated`) plus `vulnerabilities[].affects[].versions[].status` enum (affected / unaffected / unknown, default affected; page L16134-L16169), the CycloneDX product-status counterpart. Anchor ids in the page HTML: `vulnerabilities_items_analysis{,_state,_justification,_response,_detail}`. Slice: 111 lines, 4889 bytes, sha256 `d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779`. The slice rule is declared in the manifest record (`scope`, `tool`, `normalized`).

## What the subtree says (from the capture)
- `analysis.state` (6 values): resolved, resolved_with_pedigree, exploitable, in_triage, false_positive, not_affected (capture L8-L15). `not_affected`: "Justification should be specified" (SHOULD-level; contrast CSAF S055 known_not_affected impact statement SHALL — S055 Q3).
- `analysis.justification` (9 values): code_not_present, code_not_reachable, requires_configuration, requires_dependency, requires_environment, protected_by_compiler, protected_at_runtime, protected_at_perimeter, protected_by_mitigating_control (capture L17-L29). CSAF has 5 flags (S055 §3.2.3.5); CISA S056 not re-read here.
- `analysis.response` (array, 5): can_not_fix, will_not_fix, update, rollback, workaround_available; "strongly encouraged" when state is exploitable (L30-L41). `detail` free text (L42). `firstIssued`/`lastUpdated` date-time (L45-L50) — per-analysis timestamps, comparable to the S057 issued/updated + reaffirmation discussion; no reaffirmation rule stated here.
- Structural difference: CycloneDX splits per-version `affects[].versions[].status` (affected/unaffected/unknown) from the analysis assessment; the analysis object is an impact/exploitability assessment embedded in a BOM, not a stand-alone advisory status list. [INFERENCE] state names map loosely: exploitable~known_affected, in_triage~under_investigation, not_affected~known_not_affected, resolved~fixed; false_positive and resolved_with_pedigree have no CSAF product-status twin I observed (CSAF eight lists per S055). The mapping is not stated by either source.

## Quotes (all <=25 words; verified with the lane instrument)
| id | words | capture line | text |
|---|---|---|---|
| Q1 | 15 | L7 (page L16065) | Declares the current state of an occurrence of a vulnerability, after automated or manual analysis. |
| Q2 | 18 | L15 (page L16073) | The component or service is not affected by the vulnerability. Justification should be specified for all not_affected cases. |
| Q3 | 11 | L50 (page L16108) | The date and time (timestamp) when the analysis was last updated. |

Verification (scratch manifest wrapping the record, real capture bytes), `python3 corpus/instruments/source-recheck.py --manifest rc/manifest.json --source S060`:
```
S060:sha256 OK
S060:Q1 OK occurrences=1 anchor=7-ok
S060:Q2 OK occurrences=1 anchor=15-ok
S060:Q3 OK occurrences=1 anchor=50-ok
exit=0
```
Landed-file check: `sha256sum ScoutF23Lead.capture.txt` = d686262…6779 (111 lines, 4889 bytes); `ScoutF23Lead.manifest-record.json` 57 lines, sha256 `192dd214c5f29390664854391adaf1f2a8d58703066ab605e1b39f6d42a42683`, parses as JSON.

## Notes for the L1 / scribes
- Record id and `path` use the provisional **S060** (the F23 row is expected to be the first new row); `path` stem must equal the final row id (source-recheck B1) — rename the capture to `<id>.txt` and fix `id`/`path`/`files` if ScribeNewRows assigns a different id. The row's anchor cell must carry exactly one URL token equal to the record `url` (capture-binding rule B); S059 (rejected) cannot anchor it (rule rejected-row-anchor).
- The record carries `raw_sha256` plus `reproducibility` note; if a later recheck compares raw bytes it will mismatch by design. Slice is derived from the page text, so a recheck must re-slice L1 + L16060-L16169 (line numbers could shift if the site changes; the capture is the committed evidence).
- Prior S059 ledger values (r38: 6419901 bytes, sha256 afb22b46…88f3f9, analysis.state L24562-L24582 of a differently stripped text) cannot be reconciled with this capture's L16064+ numbers (different stripper); this capture's own anchors govern. The raw hash also differs from afb22b46… (consistent with the non-reproducible email tokens, and not asserted otherwise).
- Reply sent to ScribeF23-2 with sha/lines/quotes/scope.
