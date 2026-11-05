> **DRAFT — NOT LANDED, AND NOT FIT TO LAND AS WRITTEN.**
> The L1 (KasegiR77) refused C2 on 2026-11-05: the frozen predicate B6 failed the R125 admitted-entry sweep. This file is the seat's composed draft, retained as evidence of what was drafted and of where the draft repeats the failure. **Rows C6 (version rule, `S112.txt:35`), C7 (400 Bad Request, `S112.txt:36`) and C11 (threading variance, `S112.txt:170`) restate substance already held in admitted F51** (`corpus/knowledge/osv-post-v1-query-contract.md:21` for the version rule and the 400, `:47` for the page-size/threading sentence; `S108.txt:40,41,136`). A successor must drop those three rows from the claimed set and cite them as held, per the L1's reject line in `corpus/lessons/round-77.md:13` and the routed fix R-77-C (`:51`).
> Two further defects in the frozen predicate are recorded in `ScribeEntry.md` §Findings and are **not** corrected here: the round-77 manifest's declared anchors for `Q04-params-same` and `Q05-pagination-instructions` sit one line above the quoted text (`:30`/`:31` declared, `:31`/`:32` actual), and the frozen B6 permitted-line list admits `:194` while excluding `:32`. The frozen bytes are attacked here, never edited.

# OSV.dev POST /v1/querybatch contract: the batch payload, the ids-and-modified-only return, the input-matched ordering, the per-item version rule, and the per-query pagination

source: S112 — https://google.github.io/osv.dev/post-v1-querybatch/ — capture corpus/source-snapshots/round-77/S112.txt sha256 f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907
verified-at: 539a43877809bd90b6f506e8fd24a6d871598cd5
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112

## Attribution

This is the OSV.dev project's own reference page for one endpoint of its query service, `POST /v1/querybatch`. Every sentence below is that page's own text, quoted verbatim with the line in the pinned capture `corpus/source-snapshots/round-77/S112.txt`. This entry instructs no call against osv.dev or any other host; every check replays the pinned capture.

## Decision table — the batch contract, clause by clause

| # | Clause | The page's own sentence (verbatim) | Located at | Falsifiable rule a reader can check |
|---|---|---|---|---|
| C1 | One request queries many packages at once | "Query for multiple packages (by either package and version or git commit hash) at once." | S112.txt:24 | A payload carrying more than one query item is what the page describes; a reader checks the one sentence at :24. |
| C2 | The response returns vulnerability ids and the modified field only | "Returns vulnerability ids and modified field only." | S112.txt:24 | A response carrying any field beyond the vulnerability id and the modified timestamp contradicts :24. |
| C3 | The response order matches the input order | "The response ordering will be guaranteed to match the input." | S112.txt:24 | A result list whose i-th element does not correspond to the i-th input query contradicts :24. |
| C4 | The parameters are those of POST /v1/query, and a request may carry many queries | "The parameters are the same as those in POST /v1/query, but you can make multiple queries." | S112.txt:31 | A batch item using a parameter that POST /v1/query does not define contradicts :31. |
| C5 | Each query item follows the /v1/query item rules | "Each query item must follow the same rules as /v1/query:" | S112.txt:34 | An item that breaks an /v1/query item rule breaks it for the batch as well; the rules themselves are read at S108.txt:34-48, not here. |
| C6 | A version or a versioned purl, never both | "Use either version or a versioned purl, not both." | S112.txt:35 | An item naming a version and a versioned purl together contradicts :35. |
| C7 | Both together is a 400 Bad Request | "Items with both will return 400 Bad Request." | S112.txt:36 | The stated consequence is attached to the item that carries both, which a reader checks on the one line :36. |
| C8 | In a batch, only some of the queries are paginated | "However, a querybatch request may return results with a next_page_token for only a few of the total queries." | S112.txt:166 | A batch whose every result carries a next_page_token is not the partial shape the page describes at :166. |
| C9 | The per-query threshold is more than 1,000 vulnerabilities | "An individual query within the queryset returns more than 1,000 vulnerabilities" | S112.txt:168 | The 1,000 figure belongs to one query inside the queryset, which a reader checks on :168. |
| C10 | The whole-set threshold is more than 3,000 vulnerabilities | "The entire queryset returns more than 3,000 vulnerabilities total" | S112.txt:169 | The 3,000 figure belongs to the queryset as a whole, which a reader checks on :169. |
| C11 | The thresholds vary with threading | "These numbers can vary slightly because of threading and the page size may change in the future." | S112.txt:170 | The two figures are the page's stated thresholds, not a guarantee, which a reader checks on :170. |
| C12 | The follow-up request carries page_token only for the queries that returned one | "To get the next page of results, your next request should specify page_token only for the queries that returned next_page_token." | S112.txt:195 | A follow-up request that repeats a page_token for a query that returned none contradicts :195. |

## Rejected over-generalizations

- The batch endpoint has its own parameter set, separate from POST /v1/query. Not a page sentence: the page says the parameters are the same (S112.txt:31) and that each item follows the same rules (S112.txt:34).
- A version and a versioned purl may both be set on one item, since the page says the exclusion only for the single-query endpoint. Not a page sentence: the batch page states the exclusion for its own items (S112.txt:35) and the 400 consequence (S112.txt:36).
- The 1,000 and 3,000 figures are hard limits a client may rely on. Not a page sentence: the page says the numbers can vary slightly because of threading and that the page size may change (S112.txt:170).
- A batch response is paginated as one unit, so every result carries a next_page_token. Not a page sentence: the page says a request may return tokens for only a few of the queries (S112.txt:166).

## Distinctness

- F51 / S108 (`corpus/knowledge/osv-post-v1-query-contract.md`) holds the single-query contract: the payload keys (S108.txt:58-67), the version rule in full (S108.txt:40-41), the package-name matching rules (S108.txt:54), the Git-tag query (S108.txt:56), the pagination basics with the 1,000-vulnerability and 20-second triggers (S108.txt:135-136) and the 32 MiB HTTP/1.1 response-size limit (S108.txt:148). This entry claims none of them; the batch page's two "same as /v1/query" sentences (S112.txt:31, :34) point at them instead of restating them.
- F31 / S080 (`corpus/knowledge/osv-affected-range-events.md`) holds the OSV record format. The batch page returns vulnerability ids and the modified field only (S112.txt:24) and states no record field.
- The API overview page (S111, `corpus/SOURCES.md:123`) stays queued; nothing here is claimed from it.
- The endpoint path string `POST /v1/querybatch` is already-held listed-not-described ground — the navigation listing at S108.txt:5-9 and F51's own Limits bullet at `corpus/knowledge/osv-post-v1-query-contract.md:75`. It is not claimed here.

## Limits

The page does not establish, and this entry does not claim:

- rate limits, quotas, an API key or any credential: `grep -n -i -E 'rate limit|ratelimit|quota|api key|api_key|authenticat|credential' corpus/source-snapshots/round-77/S112.txt` prints nothing and exits 1.
- a response-size limit on this endpoint: `grep -n -i -E 'MiB|size limit|response size' corpus/source-snapshots/round-77/S112.txt` prints nothing and exits 1. The 32 MiB HTTP/1.1 clause stays with F51 (S108.txt:148).
- a time-based pagination trigger: `grep -n -i 'second' corpus/source-snapshots/round-77/S112.txt` prints nothing and exits 1. The 20-second clause stays with F51 (S108.txt:136).
- a per-item parameter list of its own: the item rules are the /v1/query ones (S112.txt:34), read at S108.txt:34-48.
- the request-body and response JSON examples: the capture holds them at S112.txt:37-61 and S112.txt:84-164, outside the located-anchor set of the round-77 C2 predicate (`.ufo/waves/round-77/claims.json` B6, `located_anchors`), and no manifest quote pins them.
- the sentence at S112.txt:194 ("Notice that each result has a distinct next_page_token and that the third result does not include a next_page_token."): it is located in the capture, but the round-77 manifest pins no quote at :194, so this entry does not ground a clause on it.
- the current state of the page or of any osv.dev host. The manifest records the fetch instant 2026-11-05T12:22:10Z; the capture bytes carry no timestamp. This entry made no query against osv.dev.

Scope limit: the batch endpoint's own contract clauses — the queries-array batch semantics, the ids-and-modified-only return, the input-matched ordering, the per-item version rule with its 400 Bad Request consequence, and the per-query pagination thresholds and follow-up-request rule — as stated on the POST /v1/querybatch page only. The single-query contract stays with F51 (S108); the OSV record format stays with F31 (S080); the API overview page stays with S111; the endpoint path string stays listed-not-described ground.

## Verification

Every quoted sentence above is one of the 13 quotes pinned in `corpus/source-snapshots/round-77/manifest.json`. The recheck line above was run against the frozen manifest bytes: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112` printed `S112:sha256 OK` and 13 `OK occurrences=1 anchor=<n>-ok` lines, exit 0 (receipt: `.ufo/waves/round-77/controls/c2-prerecheck-r77.txt`).

One anchor note for a re-verifier: the manifest's declared anchor for `Q04-params-same` is 30 and for `Q05-pagination-instructions` is 31, while the quoted text sits on S112.txt:31 and S112.txt:32 respectively. The instrument's anchor window is a four-line window (`corpus/instruments/source-recheck.py:110`, `raw_lines[max(0, anchor - 1):anchor + 3]`), so both still verify (`anchor=30-ok`, `anchor=31-ok`); this entry cites the lines the text actually occupies.
