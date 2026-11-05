# OSV.dev POST /v1/querybatch service contract: the batch definition, the ids-and-modified-only return, the input-matched ordering, the per-query next_page_token, the two stated counts and the follow-up page_token rule

source: S112 — https://google.github.io/osv.dev/post-v1-querybatch/ (anchor: the POST /v1/querybatch page, capture corpus/source-snapshots/round-78/S112.txt)
verified-at: 2026-11-05
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112

## Attribution

This is the OSV.dev project's own reference page for one endpoint of its query service, the page headed `POST /v1/querybatch` (S112.txt:22). Every statement below is that page's own declared contract, quoted from the pinned capture `corpus/source-snapshots/round-78/S112.txt` with the line the text occupies. The page's own one-line summary carries three of the seven clauses claimed here: "Query for multiple packages (by either package and version or git commit hash) at once." (S112.txt:24), "Returns vulnerability ids and modified field only." (S112.txt:24) and "The response ordering will be guaranteed to match the input." (S112.txt:24). The format of a returned vulnerability record is not claimed here; the batch response carries the vulnerability id and the modified field only (S112.txt:24), and that record format stays with F31 (`corpus/knowledge/osv-affected-range-events.md`, S080). This entry instructs no call against osv.dev or any other host, and every check replays the pinned capture.

## Claim 1 — the batch definition and the ids-and-modified-only return

The endpoint is one request that queries many packages at once, each item being either a package-and-version query or a commit-hash query: "Query for multiple packages (by either package and version or git commit hash) at once." (S112.txt:24). What comes back is bounded: "Returns vulnerability ids and modified field only." (S112.txt:24).

Falsifiable rule: a querybatch response that carries any field beyond the vulnerability id and the modified timestamp contradicts S112.txt:24, and a request that queries a single package is not the batch this page describes (S112.txt:24). A reader checks it by reading the one line the two sentences share.

Rejected over-generalization, not a page sentence: a batch response carries the whole vulnerability record, as a vulnerability database would normally return. The page's own sentence at S112.txt:24 says the response returns vulnerability ids and the modified field only.

## Claim 2 — the response ordering is guaranteed to match the input

"The response ordering will be guaranteed to match the input." (S112.txt:24). The guarantee is stated on the page's own summary line, as a guarantee and not as an option (S112.txt:24).

Falsifiable rule: a batch response whose i-th result does not correspond to the i-th input query contradicts S112.txt:24. A reader checks it by reading that one sentence and comparing its input and output positions.

Rejected over-generalization, not a page sentence: the service may reorder results for its own convenience, so a client must match ids itself. The page states the opposite at S112.txt:24.

## Claim 3 — a next_page_token belongs to one query, and only some queries of a set carry one

"However, a querybatch request may return results with a next_page_token for only a few of the total queries." (S112.txt:166). The token is per query of the queryset, and a single batch response may leave most of its queries without one (S112.txt:166).

Falsifiable rule: a querybatch response in which every query of the set carries a next_page_token is not the partial shape the page describes, and a reader checks it on the one line the sentence occupies (S112.txt:166).

Rejected over-generalization, not a page sentence: pagination is all-or-nothing for a batch, so either every query of the set is paginated or none is. The page says a request may return a next_page_token for only a few of the total queries (S112.txt:166).

## Claim 4 — the two counts the page states for a querybatch queryset

The page states two counts: "An individual query within the queryset returns more than 1,000 vulnerabilities" (S112.txt:168) and "The entire queryset returns more than 3,000 vulnerabilities total" (S112.txt:169). The first count belongs to one query inside the queryset, the second to the queryset as a whole (S112.txt:168) (S112.txt:169).

Falsifiable rule: reading 1,000 as the bound for the whole queryset, or 3,000 as the bound for a single query, contradicts S112.txt:168 and S112.txt:169 respectively. A reader checks it by reading the two lines side by side and seeing which scope each sentence names.

Rejected over-generalization, not a page sentence: 3,000 is a per-query count and 1,000 is a whole-set count. The page attaches the 1,000 count to an individual query within the queryset (S112.txt:168) and the 3,000 count to the entire queryset (S112.txt:169).

## Claim 5 — the follow-up request carries a page_token only for the queries that returned one

"To get the next page of results, your next request should specify page_token only for the queries that returned next_page_token." (S112.txt:195). The follow-up request is selective: it repeats a token for the queries that returned one and sends none for the others (S112.txt:195).

Falsifiable rule: a follow-up request that sends a page_token for a query that returned no next_page_token, or that omits the token for a query that returned one, contradicts S112.txt:195. A reader checks it by reading that one sentence against the tokens present in the preceding response.

Rejected over-generalization, not a page sentence: the follow-up request repeats the original batch unchanged and carries one token for the whole set. The page says the next request should specify page_token only for the queries that returned next_page_token (S112.txt:195).

## Distinctness

- F51 / S108 (`corpus/knowledge/osv-post-v1-query-contract.md`) holds the single-query contract in six claims of its own: the payload keys (`corpus/knowledge/osv-post-v1-query-contract.md:11`), the version rule and its 400 Bad Request consequence (`corpus/knowledge/osv-post-v1-query-contract.md:19`), the package-name matching rules (`corpus/knowledge/osv-post-v1-query-contract.md:29`), the Git-tag query (`corpus/knowledge/osv-post-v1-query-contract.md:37`), the pagination basics (`corpus/knowledge/osv-post-v1-query-contract.md:45`) and the 32 MiB HTTP/1.1 response-size limit (`corpus/knowledge/osv-post-v1-query-contract.md:53`). This entry claims none of that ground.
- The single-query pagination trigger F51 holds is scoped to one response and to a time limit (`corpus/knowledge/osv-post-v1-query-contract.md:47`, quoting S108.txt:136); the two counts claimed here are scoped to one query inside a queryset and to the queryset as a whole (S112.txt:168) (S112.txt:169), and the 3,000 figure has no counterpart in F51 at all (`grep -c '3,000' corpus/knowledge/osv-post-v1-query-contract.md` prints 0). The two overlaps are therefore different scopes of the same number, not the same ground stated twice.
- F31 / S080 (`corpus/knowledge/osv-affected-range-events.md`) holds the OSV record format; the batch response carries the vulnerability id and the modified field only (S112.txt:24), so no record field is claimed here.
- The subject sweep `grep -rli -i 'osv' corpus/knowledge/*.md | grep -v osv-post-batch-query-contract` (2026-11-05) returns five admitted entries; the OSV ground already held among them is the single-query contract above, the record format (F31) and Scorecard's own use of the OSV service (`corpus/knowledge/openssf-scorecard-checks.md`, S086), while the other two mentions are a format statement that defers to F31 and a distinctness line. None of the five states a clause of this page.
- The endpoint path string `POST /v1/querybatch` is already-held listed-not-described ground: F51's own Limits bullet lists it among the single-query page's navigation (`corpus/knowledge/osv-post-v1-query-contract.md:75`). It is not claimed here.

## Not claimed

Not claimed: the parameters pointer (S112.txt:31), the pagination-instructions pointer (S112.txt:32), the item-rules pointer (S112.txt:34), the version rule (S112.txt:35), the 400 Bad Request consequence (S112.txt:36) and the threading-variance note (S112.txt:170). The parameters pointer and the item-rules pointer point at the single-query contract, the instructions pointer points at a separate instructions document this entry does not claim, and the version rule, the 400 consequence and the threading-variance note restate ground F51 already holds at `corpus/knowledge/osv-post-v1-query-contract.md:21` and `corpus/knowledge/osv-post-v1-query-contract.md:47` (S108.txt:40,41,136). No manifest quote pins those six lines, so this entry grounds no clause on them.

## Gate — S112 (OSV.dev POST /v1/querybatch)

- **URL:** https://google.github.io/osv.dev/post-v1-querybatch/ (HTTP 200; the manifest records the final URL equal to the requested URL).
- **Access date:** 2026-11-05. The committed capture's `fetched_utc` is 2026-11-05T12:22:10Z (`corpus/source-snapshots/round-78/manifest.json`); the capture is `corpus/source-snapshots/round-78/S112.txt` (sha256 `f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907`, 216 lines, 4575 snapshot bytes; the served page was 30406 raw bytes before the capture instrument stripped tags and collapsed whitespace per line).
- **Seven located quotes, one per claimed clause, each verbatim at its snapshot line, word counts by `wc -w`:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| C1 batch definition | Q01-batch-definition | S112.txt:24 | 15 | "Query for multiple packages (by either package and version or git commit hash) at once." |
| C2 return shape | Q02-return-shape | S112.txt:24 | 7 | "Returns vulnerability ids and modified field only." |
| C3 ordering | Q03-ordering | S112.txt:24 | 10 | "The response ordering will be guaranteed to match the input." |
| C4 partial next_page_token | Q09-partial-tokens | S112.txt:166 | 18 | "However, a querybatch request may return results with a next_page_token for only a few of the total queries." |
| C5 per-query count | Q10-individual-1000 | S112.txt:168 | 11 | "An individual query within the queryset returns more than 1,000 vulnerabilities" |
| C6 queryset count | Q11-total-3000 | S112.txt:169 | 9 | "The entire queryset returns more than 3,000 vulnerabilities total" |
| C7 follow-up request | Q13-next-request | S112.txt:195 | 20 | "To get the next page of results, your next request should specify page_token only for the queries that returned next_page_token." |

- **Recheck receipt:** the `recheck:` line above, run against the committed bytes, printed `S112:sha256 OK` and one `S112:<pin> OK occurrences=1 anchor=<n>-ok` line per pinned quote, exit 0; the seven anchors are the exact lines the quotes occupy in the capture.

## Limits

The page does not establish, and this entry does not claim:

- rate limits, quotas, an API key or any credential. The capture carries no such sentence: `grep -n -i -e 'rate limit' -e 'ratelimit' -e 'quota' -e 'api key' -e 'api_key' -e 'authenticat' -e 'credential' corpus/source-snapshots/round-78/S112.txt` prints nothing and exits 1.
- a response-size limit for this endpoint. The capture carries no such sentence: `grep -n -i -e 'MiB' -e 'size limit' -e 'response size' corpus/source-snapshots/round-78/S112.txt` prints nothing and exits 1; the single-query page's size limit stays with F51.
- a time-based pagination trigger. The capture carries no such sentence: `grep -n -i -e 'second' corpus/source-snapshots/round-78/S112.txt` prints nothing and exits 1; the single-query page's time trigger stays with F51.
- the sentence about distinct per-result tokens (S112.txt:194): it is located in the capture, but no manifest quote pins it, so this entry grounds no clause on it.
- the request and response JSON examples, the payload shape, or any field name beyond what the seven quotes carry.
- the current state of the page or of any osv.dev host. The manifest records the fetch instant 2026-11-05T12:22:10Z (`corpus/source-snapshots/round-78/manifest.json`), and the capture bytes carry no timestamp. This entry made no query against osv.dev.

Scope limit: the batch endpoint's own seven clauses — the batch definition and the ids-and-modified-only return (S112.txt:24), the input-matched ordering guarantee (S112.txt:24), the per-query next_page_token rule (S112.txt:166), the two counts stated for a querybatch queryset (S112.txt:168, S112.txt:169) and the follow-up page_token rule (S112.txt:195) — as stated on the POST /v1/querybatch page only. The single-query contract stays with F51 (S108); the OSV record format stays with F31 (S080).
