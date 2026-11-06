# OSV.dev POST /v1experimental/ubuntu/binary-to-source: the purpose, the source-name indexing it answers, the scanner use, the ecosystem forms, the bounded binary_names array and the empty-object result for an unmapped name

source: S114 — https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/ (anchor: the POST /v1experimental/ubuntu/binary-to-source page, capture corpus/source-snapshots/round-80/S114.txt)
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-80/manifest.json --source S114

## Attribution

This is the OSV.dev project's own reference page for one experimental endpoint of its API, the page headed `POST /v1experimental/ubuntu/binary-to-source` (S114.txt:22-23). Every statement below is that page's own declared behaviour, quoted from the pinned capture `corpus/source-snapshots/round-80/S114.txt` with the line the text occupies. The page sits at `https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/`; the experimental-path form of the URL (`.../post-v1experimental-ubuntu-binary-to-source/`) answered HTTP 404 on 2026-11-06, so the round-79 lead's path name is not the page's address. The six clauses claimed here are the ones the round-80 manifest pins (Q01, Q02, Q03, Q04, Q05, Q07).

## Claim 1 — the purpose: Ubuntu binary package names map to source package names

"Map Ubuntu binary package names to their corresponding source package names." (S114.txt:25). The input is binary package names and the output is the source package names that correspond to them (S114.txt:25).

Falsifiable rule: a caller that sends source package names and expects binary names back has reversed the direction S114.txt:25 states. A reader checks it by reading that one summary sentence.

Rejected over-generalization, not a page sentence: the endpoint maps package names between any two Linux distributions' naming schemes. The page's summary names Ubuntu binary package names and their corresponding source package names only (S114.txt:25).

## Claim 2 — the reason: OSV indexes Ubuntu advisories by source package name

"Ubuntu vulnerability advisories in OSV are indexed by source package name rather than binary package name." (S114.txt:35). The page states the indexing key for Ubuntu advisories in OSV and names the key it is not (S114.txt:35).

Falsifiable rule: an OSV query for an Ubuntu advisory keyed by an installed binary package name (for example a library package whose name differs from its source package) is keyed on the name S114.txt:35 says OSV does not index by. A reader checks it by reading the first sentence of the Purpose paragraph.

Rejected over-generalization, not a page sentence: every OSV ecosystem indexes advisories by source package name. The page states the indexing rule for Ubuntu vulnerability advisories in OSV only (S114.txt:35).

## Claim 3 — the use: scanners query OSV with the resulting source package names

"allowing callers such as scanners to query OSV using the resulting source package names." (S114.txt:35). The endpoint's output is meant as the input to a later OSV query, and the page names scanners as one such caller (S114.txt:35).

Falsifiable rule: reading the endpoint's result as vulnerability information contradicts S114.txt:35, which describes the result as source package names a caller then uses to query OSV; this entry's [INFERENCE] is that the query step is a separate call, since the response shape the page shows carries `source_names` only (S114.txt:60-71, not pinned). A reader checks it by reading the closing clause of the Purpose paragraph.

Rejected over-generalization, not a page sentence: the endpoint returns the vulnerabilities affecting each binary package. The page says it resolves names so that callers can query OSV with the resulting source package names (S114.txt:35).

## Claim 4 — the ecosystem parameter names an Ubuntu release, in three stated forms

"The Ubuntu release ecosystem (e.g. Ubuntu:24.04, Ubuntu:24.04:LTS, or Ubuntu:Pro:24.04:LTS)." (S114.txt:38). The parameter is one string per request, and the page's examples show a plain release, an LTS release and a Pro LTS release (S114.txt:38).

Falsifiable rule: a request whose ecosystem is the bare string `Ubuntu`, with no release, does not follow the form the examples at S114.txt:38 show ([INFERENCE] whether the service rejects it is not stated). A reader checks it by reading the parameter row.

Rejected over-generalization, not a page sentence: one request may carry binary names from several Ubuntu releases. The parameter table gives one `ecosystem` string, described as the Ubuntu release ecosystem (S114.txt:38).

## Claim 5 — binary_names is a non-empty array of at most 1000 names per request

"A non-empty array of Ubuntu binary package names (maximum 1000 per request)." (S114.txt:39). Two bounds are stated on the one row: the array is non-empty, and it holds at most 1000 names per request (S114.txt:39).

Falsifiable rule: a request with an empty `binary_names` array, or with more than 1000 names, is outside the bounds S114.txt:39 states. A reader checks it by reading the parameter row; the page states no error behaviour for an out-of-bounds request, and this entry claims none (see Limits).

Rejected over-generalization, not a page sentence: the 1000 limit is the same per-queryset limit as the batch query endpoint. The binary-to-source row states its own maximum, 1000 binary package names per request (S114.txt:39); F54's counts concern vulnerabilities returned by a query (`corpus/knowledge/osv-post-batch-query-contract.md:37`), a different quantity.

## Claim 6 — an unmapped binary name yields an empty object in the results

"with an empty object {} for binary package names that have no known source package mappings in that Ubuntu release" (S114.txt:58). A name with no known mapping still gets an entry in the results, and that entry is the empty object `{}` (S114.txt:58).

Falsifiable rule: a caller that reads a missing `source_names` key as an error, or that drops empty objects and then pairs the remaining results with its input names, misreads S114.txt:58. A reader checks it by reading the sentence that introduces the example response.

Rejected over-generalization, not a page sentence: an empty result means the binary package does not exist in Ubuntu. The page says only that the name has no known source package mappings in that Ubuntu release (S114.txt:58).

## Distinctness

- F51 / S108 (`corpus/knowledge/osv-post-v1-query-contract.md`) holds the single-query contract and lists "the experimental endpoints" in its Limits bullet without describing them (`corpus/knowledge/osv-post-v1-query-contract.md:75`). This entry's input is a package-name array plus a release ecosystem and its output is source names, not vulnerabilities; no F51 clause is restated.
- F54 / S112 (`corpus/knowledge/osv-post-batch-query-contract.md`) holds the batch contract, including the input-matched ordering guarantee (`corpus/knowledge/osv-post-batch-query-contract.md:19`). The binary-to-source page states an ordering guarantee of the same shape for its own results (S114.txt:58, leading clause); that clause is not pinned and not claimed here, so no second copy of the ordering rule-shape enters the corpus. Claim 6 pins only the empty-object clause of that line.
- F55 / S113 (`corpus/knowledge/osv-determineversion-cc-library-versioning.md`) holds the other pre-query experimental endpoint, which turns C/C++ file hashes into a library version; this entry's input is Ubuntu binary package names, and no F55 clause is restated.
- F31 / S080 (`corpus/knowledge/osv-affected-range-events.md`) holds the OSV record format; the binary-to-source response is a `results` array of `source_names` lists, not an OSV record.
- Subject sweep `grep -rli 'ubuntu' corpus/knowledge/` (2026-11-06, before this entry) prints nothing and exits 1: no admitted entry carries the word, so no admitted entry states a clause of this page under that term. Literal sweep: none of the six pinned quotes occurs in any of the 93 admitted entries (`.ufo/waves/round-80/controls/c2-prerecheck-r80.txt`).

## Not claimed

Not claimed: the experimental-status paragraph (S114.txt:33) — F51's Limits bullet already lists the experimental endpoints (`corpus/knowledge/osv-post-v1-query-contract.md:75`); the leading ordering clause of S114.txt:58 ("The response results array is guaranteed to match the ordering of the input binary_names") — the rule-shape F54 holds for querybatch; the payload skeleton (S114.txt:41-46); and the request sample and example response values (S114.txt:48-72) — sample data, not rules.

## Gate — S114 (OSV.dev POST /v1experimental/ubuntu/binary-to-source)

- **URL:** https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/ (HTTP 200; the manifest records the final URL equal to the requested URL).
- **Access date:** 2026-11-06. The committed capture's `fetched_utc` is 2026-11-06T19:42:42Z (`corpus/source-snapshots/round-80/manifest.json`); the capture is `corpus/source-snapshots/round-80/S114.txt` (sha256 `e1ccfb9bd13bb3f9a077feb60ae5d738ccb47bc85f630aef9a7a5776ca8788d2`, 73 lines, 2365 snapshot bytes; the served page was 18769 raw bytes before the capture instrument stripped tags and collapsed whitespace per line).
- **Six located quotes, one per claimed clause, each verbatim at its snapshot line, word counts by `wc -w`:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| cl1 purpose | Q01-purpose | S114.txt:25 | 11 | "Map Ubuntu binary package names to their corresponding source package names." |
| cl2 source-name indexing | Q02-source-indexing | S114.txt:35 | 16 | "Ubuntu vulnerability advisories in OSV are indexed by source package name rather than binary package name." |
| cl3 scanner use | Q03-scanner-use | S114.txt:35 | 14 | "allowing callers such as scanners to query OSV using the resulting source package names." |
| cl4 ecosystem forms | Q04-ecosystem-forms | S114.txt:38 | 9 | "The Ubuntu release ecosystem (e.g. Ubuntu:24.04, Ubuntu:24.04:LTS, or Ubuntu:Pro:24.04:LTS)." |
| cl5 binary_names bounds | Q05-binary-names-limit | S114.txt:39 | 12 | "A non-empty array of Ubuntu binary package names (maximum 1000 per request)." |
| cl6 unmapped name | Q07-unmapped-empty-object | S114.txt:58 | 20 | "with an empty object {} for binary package names that have no known source package mappings in that Ubuntu release" |

- **Recheck receipt:** the `recheck:` line above, run against the committed bytes, printed `S114:sha256 OK` and one `S114:<pin> OK occurrences=1 anchor=<n>-ok` line per pinned quote, exit 0 (`.ufo/waves/round-80/controls/c2-prerecheck-r80.txt`); the six anchors are the exact lines the quotes occupy in the capture (25, 35, 35, 38, 39, 58).

## Limits

The page does not establish, and this entry does not claim:

- rate limits, quotas, an API key or any credential: `grep -n -i -E 'rate limit|ratelimit|quota|api key|api_key|authenticat|credential' corpus/source-snapshots/round-80/S114.txt` prints nothing and exits 1.
- pagination of this endpoint's results: `grep -n -i -E 'paginat|page_token|next_page_token' corpus/source-snapshots/round-80/S114.txt` prints nothing and exits 1.
- an error or status-code contract, including what an empty or oversized `binary_names` array returns: `grep -n -i -E 'error|status code|throttl|400' corpus/source-snapshots/round-80/S114.txt` prints nothing and exits 1.
- a severity, CVE or CVSS statement: `grep -n -i -E 'severity|CVE|cvss' corpus/source-snapshots/round-80/S114.txt` prints nothing and exits 1.
- any distribution other than Ubuntu, or Debian's naming: `grep -n -i -E 'Debian|deb|dpkg' corpus/source-snapshots/round-80/S114.txt` prints nothing and exits 1.
- the list of valid ecosystem strings beyond the three examples at S114.txt:38; the page gives examples ("e.g."), not an enumeration.
- the current state of the page or of any osv.dev host. The manifest records the fetch instant 2026-11-06T19:42:42Z, and the capture bytes carry no timestamp. This entry made no query against osv.dev.

Scope limit: the binary-to-source endpoint's own six clauses — the purpose (S114.txt:25), the source-name indexing and the scanner use (S114.txt:35), the ecosystem forms (S114.txt:38), the binary_names bounds (S114.txt:39) and the empty-object result for an unmapped name (S114.txt:58) — as stated on the POST /v1experimental/ubuntu/binary-to-source page only. The single-query contract stays with F51 (S108), the batch contract and the ordering rule-shape with F54 (S112), the C/C++ version determination with F55 (S113), and the OSV record format with F31 (S080).
