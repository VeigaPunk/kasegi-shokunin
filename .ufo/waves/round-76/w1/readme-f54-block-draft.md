# DRAFT — corpus/README.md end-of-file append for round 76 (ScribeLedger, not applied)
# Placement: append after corpus/README.md line 1189 (the last line, the r75 amendment). Apply the text below the line of equals signs, verbatim; this header is not part of the text.
# Sourcing: S111 (frozen capture, sha256 6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab); the claim is C2 of .ufo/waves/round-76/claims.json.
==========

## Round-76 admission — coverage map row and Frontier F54 (2026-11-05)

Appended amendment (R6): the round-76 entry `corpus/knowledge/osv-api-surface-and-limits.md` (Frontier F54, source S111) rests on the OSV.dev project's own API overview page at https://google.github.io/osv.dev/api/, captured `corpus/source-snapshots/round-76/S111.txt` (sha256 6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab, 48 lines, 1810 bytes), manifest `corpus/source-snapshots/round-76/manifest.json` (<FILL: pinned quote count at integration; the committed manifest holds 13, and its Q01 fails the 12-character floor of source-recheck.py>, anchors S111.txt lines 21-39). The coverage map above is not edited in place (R6); the coverage-map row is appended here, and the F54 frontier row uses the same six-cell table shape as F53. The page is the API surface overview only: it is not the record format (S080, F31) and not the single-endpoint POST /v1/query contract (S108, F51). Its response-size clause at S111.txt line 38 is already-held ground from S108 and is cross-referenced here, not claimed.

| Area | Entry | Source basis |
|---|---|---|
| OSV.dev API surface overview: the six request types and their one-line purposes (three of them experimental), the API 1.0 and OpenAPI specification availability, and the rate-limit statement that the API has no limits (round 76) | knowledge/osv-api-surface-and-limits.md | S111, the OSV.dev project's own API overview page, opened 2026-11-05 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F54 | OSV.dev API surface overview and limits | admitted | knowledge/osv-api-surface-and-limits.md | S111 | Read the six request types as the overview page's own list (S111.txt:28-34) and the no-limits sentence at :36 as the page's statement, not as a measured service limit; the response-size clause at :38 is already held from F51 and is not claimed here, and the five non-query endpoints have no per-endpoint contract in this row. |

[r76 amendment, appended 2026-11-05] The frontier as of round 76 is F01-F54 admitted: F54 at round 76. The F54 admission rests on S111 alone; the F51 scope limit (the POST /v1/query contract only) and the F31 record-format limit stay as written, and the response-size clause is not re-claimed.

Counts at integration (frozen after-state from claims B1-B4; the measured values are recorded in LOG.md under Round 76): registry 110 -> 111 (one S111 row added, none removed); knowledge entries 91 -> 92; frontier admitted 53 -> 54 (F54 on S111); capture records 89 -> 90 (S111 bound).
