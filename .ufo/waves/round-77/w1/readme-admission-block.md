# DRAFT — corpus/README.md end-of-file append for round 77 (ScribeEntry; NOT APPLIED)
# Status 2026-11-05: the L1 (KasegiR77) refused C2 at B6 distinctness, so this block was NOT landed and no `| F54 |` row exists in corpus/README.md. Retained as successor-round material.
# Placement: append after corpus/README.md line 1189 (the last line, the r75 amendment). Apply the text below the line of equals signs verbatim; this header is not part of the text.
# Sourcing: S112 (frozen capture, sha256 f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907, 216 lines, 4575 bytes, fetched 2026-11-05T12:22:10Z); manifest corpus/source-snapshots/round-77/manifest.json (13 pinned quotes, all anchor-located rc=0 at freeze).
# The F54 row's `next` cell names the held ground (F51 / S108) with a located 25-word quote, per the r73 F51 block's shape.
# If the successor round admits F54, the count line below reads 54/54; if it refuses F54 again, replace the count line with the refusal variant quoted at the end of this file.
==========

## Round-77 admission — coverage map row and Frontier F54 (2026-11-05)

Appended amendment (R6): the round-77 entry `corpus/knowledge/osv-post-v1-querybatch-contract.md` (Frontier F54, source S112) rests on the OSV.dev project's own reference page for the POST /v1/querybatch endpoint at https://google.github.io/osv.dev/post-v1-querybatch/, captured `corpus/source-snapshots/round-77/S112.txt` (sha256 f3ca0465...0907, 216 lines, 4575 bytes, fetched 2026-11-05T12:22:10Z), manifest `corpus/source-snapshots/round-77/manifest.json` (13 pinned quotes, all located rc=0 at freeze). The coverage map above is not edited in place (R6); the coverage-map row is appended here, and the F54 frontier row uses the same six-cell table shape as F53.

| Area | Entry | Source basis |
|---|---|---|
| OSV.dev batch query contract: the queries-array payload, the ids-and-modified-only return shape, the input-matched response ordering, the per-item version rules with their 400 Bad Request consequence, and the per-query pagination semantics with next_page_token, the 1,000/3,000 thresholds, the threading-variance note and the follow-up-request rule (round 77) | knowledge/osv-post-v1-querybatch-contract.md | S112, the OSV.dev project's own API reference for the batch query endpoint, opened 2026-11-05 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F54 | OSV.dev POST /v1/querybatch service contract — the queries-array batch payload, the ids-and-modified-only return shape, the input-matched response-ordering guarantee, the parameters-same-as-/v1/query sentence, the per-item version rules with their 400 Bad Request consequence, and the per-query pagination semantics (per-result next_page_token, the 1,000/3,000 thresholds, the threading-variance note, the follow-up-request rule) | admitted | knowledge/osv-post-v1-querybatch-contract.md | S112 | Read the per-item version rule as one place only, the top-level version field or a versioned purl (S108.txt:40) and never both; read a batch result carrying next_page_token as partial for that query alone (S112.txt:166), and the entry's Limits section records the measured greps for rate limits, credentials, response-size limits and time triggers, none of which this page states |

[r77 amendment, appended 2026-11-05] The frontier as of round 77 is F01-F54 admitted: 54/54 admitted — F54 at round 77. The C2 admission rests on S112 alone; the F51 single-query contract stays as written and is cross-referenced, not re-claimed, the OSV record format stays with F31, and the S111 overview page stays queued.

# Refusal variant (use this line instead of the count line above if F54 is not admitted again):
# [r77 amendment, appended 2026-11-05] The frontier as of round 77 is F01-F53 admitted: 53/53 admitted — no frontier row admitted this round. The C2 candidate F54 (OSV.dev POST /v1/querybatch, S112) was refused again on its distinctness clause; the S112 row stays `queued` with `used-by —`, and the capture corpus/source-snapshots/round-77/S112.txt stays committed as the round's held evidence.
