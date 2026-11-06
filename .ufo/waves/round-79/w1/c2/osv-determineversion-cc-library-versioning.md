# OSV.dev POST /v1experimental/determineversion: the purpose, the identifiable-library set and its coverage limit, the ranked-versions response, the MD5 file_hashes payload with base64 hashes, the extension-scoped hash collection and the closeness-sorted matches array

source: S113 — https://google.github.io/osv.dev/post-v1-determineversion/ (anchor: the POST /v1experimental/determineversion page, capture corpus/source-snapshots/round-79/S113.txt)
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-79/manifest.json --source S113

## Attribution

This is the OSV.dev project's own reference page for one endpoint of its API, the page headed `POST /v1experimental/determineversion` (S113.txt:23). Every statement below is that page's own declared behaviour, quoted from the pinned capture `corpus/source-snapshots/round-79/S113.txt` with the line the text occupies. The page's purpose sentence states what the endpoint does with its input: "Given the source code hashes of C/C++ libraries, this endpoint attempts to find the closest upstream library and version." (S113.txt:25). Its response section states the order of what comes back: "Returns an array of potential library matches, sorted by how close the match is." (S113.txt:85). The eight clauses claimed here are the ones the round-79 manifest pins (Q01, Q04, Q05, Q06, Q07, Q08, Q09, Q10); every other line of the page is either already-held ground named under Not claimed or located-but-unpinned text named under Limits. The OSV record format is not claimed here; the query and batch-query contracts are not claimed here.

## Claim 1 — the purpose: source-code hashes of a C/C++ library map to the closest upstream library and version

"Given the source code hashes of C/C++ libraries, this endpoint attempts to find the closest upstream library and version." (S113.txt:25). The input is source-code hashes and the output is an attempt at the closest upstream library and version (S113.txt:25).

Falsifiable rule: a caller that reads a returned library and version as the identified origin of a file set, rather than as the closest upstream match the endpoint found from the hashes it was given, asserts more than S113.txt:25 states. A reader checks it by reading that one sentence and noting the verb it uses for the endpoint's operation.

Rejected over-generalization, not a page sentence: the endpoint identifies the exact library and version a set of files came from. The page's sentence at S113.txt:25 says the endpoint attempts to find the closest upstream library and version from source-code hashes.

## Claim 2 — the identifiable set is the C/C++ projects integrated into OSS-Fuzz

"The list of libraries that can currently be identified are the C/C++ projects integrated into the OSS-Fuzz project." (S113.txt:41). Membership in the identifiable list is a property of that project integration, not of the language the library is written in (S113.txt:41).

Falsifiable rule: a C/C++ library that is not an OSS-Fuzz-integrated project is outside the list this clause names, and a reader checks it at S113.txt:41 rather than by the ecosystem label. A response naming such a library would contradict the membership rule stated on that line.

Rejected over-generalization, not a page sentence: every C/C++ library is in the identifiable list because the endpoint is described as a C/C++ endpoint. The page bounds the list to the C/C++ projects integrated into the OSS-Fuzz project (S113.txt:41).

## Claim 3 — the coverage limit: not all C/C++ packages are represented

"This means that not all C/C++ packages are represented in our database." (S113.txt:41). The clause is the second sentence of the same line that names the identifiable set, and it states a gap in the database's coverage (S113.txt:41).

Falsifiable rule: a lookup that returns no match is not evidence that the library does not exist upstream, because S113.txt:41 states that the database does not represent all C/C++ packages. A reader checks it by reading the two sentences of S113.txt:41 in order: the first names the set, the second bounds it.

Rejected over-generalization, not a page sentence: a miss from this endpoint means the library is absent or unversioned upstream. The page states only that not all C/C++ packages are represented in its database (S113.txt:41).

## Claim 4 — the response ranks candidate versions by match quality against the local copy

"The API will return a number of possible versions for your package, ranked by how well the version matched your local copy." (S113.txt:55). The ordering key is match quality against the caller's local copy, and the number of candidates returned is not fixed by the sentence (S113.txt:55).

Falsifiable rule: a caller that treats the first element as the only candidate, or that reads the ranking as a confidence or probability figure, contradicts S113.txt:55, which ranks by how well the version matched the local copy. A reader checks it by reading that one sentence and its stated ranking key.

Rejected over-generalization, not a page sentence: the ranking is a probability that the top match is correct. The page names match quality against the local copy as the ranking key (S113.txt:55) and states no probability.

## Claim 5 — the request identifies a library by an array of MD5 hashes of its files

"An array of MD5 hashes of each relevant file in the library to identify." (S113.txt:61). The identifying input is per-file hashes of the library's own files, and the array form means more than one file's hash is supplied (S113.txt:61).

Falsifiable rule: a request that identifies the library by a name or version alone, or that sends one hash computed over a whole library tree, is not the payload this clause describes (S113.txt:61). A reader checks it by reading the parameter row that carries the sentence.

Rejected over-generalization, not a page sentence: a single digest of the library directory is enough to identify it. The page states an array of MD5 hashes of each relevant file in the library to identify (S113.txt:61).

## Claim 6 — the hash value is the MD5 bytes encoded in base64

"the MD5 hash bytes encoded in base64." (S113.txt:62). The encoding is stated for the hash bytes themselves, in base64 (S113.txt:62).

Falsifiable rule: a request whose hash field carries the MD5 as a hex string is not the encoding S113.txt:62 states, even though hex is how digest tooling commonly prints the same hash. A reader checks it by comparing the field's value with the row's own sentence.

Rejected over-generalization, not a page sentence: the endpoint accepts the MD5 digest in the hex form most tools print. The page states that the hash is the MD5 hash bytes encoded in base64 (S113.txt:62).

## Claim 7 — hash collection is scoped to an extension list printed below the instruction

"saving the MD5 hash of every file with the following extensions:" (S113.txt:66). The collection instruction is scoped by a list that the page prints immediately after it (the list at S113.txt:67-72), so the scope is the listed extensions and not the whole directory (S113.txt:66).

Falsifiable rule: hashing a file whose extension the page does not print after this instruction rests on no rule this page states; a reader checks it by reading S113.txt:66 and the lines of the list that follow it.

Rejected over-generalization, not a page sentence: hash every file in the library directory. The page's instruction is scoped to every file with the following extensions (S113.txt:66).

## Claim 8 — the matches array is sorted by how close the match is

"Returns an array of potential library matches, sorted by how close the match is." (S113.txt:85). The return is an array of potential matches, and its order is closeness rather than input position (S113.txt:85).

Falsifiable rule: an array whose order does not follow closeness contradicts S113.txt:85, and a reader who pairs response entries with request entries by position has assumed a batch shape this page does not describe. A reader checks it by reading that one sentence.

Rejected over-generalization, not a page sentence: the endpoint returns the single verified library match. The page returns an array of potential library matches, sorted by how close the match is (S113.txt:85).

## Distinctness

- F51 / S108 (`corpus/knowledge/osv-post-v1-query-contract.md`) holds the single-query contract in six claims of its own: the payload keys (`corpus/knowledge/osv-post-v1-query-contract.md:11`), the version rule and its fuzzy match (`corpus/knowledge/osv-post-v1-query-contract.md:19`), the package-name matching rules (`corpus/knowledge/osv-post-v1-query-contract.md:29`), the Git-tag query (`corpus/knowledge/osv-post-v1-query-contract.md:37`), pagination with next_page_token (`corpus/knowledge/osv-post-v1-query-contract.md:45`) and the 32 MiB HTTP/1.1 response-size limit (`corpus/knowledge/osv-post-v1-query-contract.md:53`). This entry claims none of that ground: its input is a file-hash array rather than a package-and-version or commit query, and its return is a matches array rather than vulnerability records.
- F51 also holds the case-sensitivity sentence at `corpus/knowledge/osv-post-v1-query-contract.md:31` (S108.txt:53), which is the same statement the determineversion page makes at S113.txt:64. That line is therefore not claimed here, and the entry adds no second copy of it.
- The endpoint path is already-held listed-not-described ground: F51's Limits bullet lists "the other endpoints in the page's navigation (POST /v1/querybatch, GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). They are listed, not described." (`corpus/knowledge/osv-post-v1-query-contract.md:75`). That bullet names the experimental endpoints without stating any clause of this page, so it is not claimed here and this entry does not re-list them.
- F54 / S112 (`corpus/knowledge/osv-post-batch-query-contract.md`) holds the batch contract: the batch definition and the ids-and-modified-only return (`corpus/knowledge/osv-post-batch-query-contract.md:11`), the input-matched ordering guarantee (`corpus/knowledge/osv-post-batch-query-contract.md:19`), the per-query partial next_page_token (`corpus/knowledge/osv-post-batch-query-contract.md:27`), the two queryset counts (`corpus/knowledge/osv-post-batch-query-contract.md:35`) and the follow-up page_token rule (`corpus/knowledge/osv-post-batch-query-contract.md:43`). The determineversion page's follow-up pointer at S113.txt:39 sends the reader to those two endpoints' ground; it is a cross-reference, and no clause of F51 or F54 is restated here.
- F31 / S080 (`corpus/knowledge/osv-affected-range-events.md`) holds the OSV record format: the envelope fields (`corpus/knowledge/osv-affected-range-events.md:21`) and the events timeline (`corpus/knowledge/osv-affected-range-events.md:33`). The determineversion response is a matches array with score and repo information (S113.txt:85-100), not an OSV record, so no record field is claimed here.
- The subject sweep `grep -rli 'determineversion\|indexer' corpus/knowledge/` (2026-11-06) prints nothing and exits 1: no admitted entry carries either the endpoint name or the indexer tooling's name, so no admitted entry states a clause of this page in paraphrase under those terms.

## Not claimed

Not claimed: the experimental-status line (S113.txt:37) — the page says the endpoint is still experimental, and F51's Limits bullet already lists the experimental endpoints (`corpus/knowledge/osv-post-v1-query-contract.md:75`), so this entry claims no status clause of its own; the query/querybatch follow-up pointer (S113.txt:39) — the sentence is a signpost from a probable version to the two query endpoints, and the ground it points at is held by F51 and F54, not by this entry; the case-sensitivity line (S113.txt:64) — held by F51 at `corpus/knowledge/osv-post-v1-query-contract.md:31` (S108.txt:53); and the sample-response values (S113.txt:101-126) — the example identifies one library at two tags with its own scores and match counts, which are example values and not a rule. No manifest quote pins any of those lines, so this entry grounds no clause on them.

## Gate — S113 (OSV.dev POST /v1experimental/determineversion)

- **URL:** https://google.github.io/osv.dev/post-v1-determineversion/ (HTTP 200; the manifest records the final URL equal to the requested URL).
- **Access date:** 2026-11-06. The committed capture's `fetched_utc` is 2026-11-06T18:43:10Z (`corpus/source-snapshots/round-79/manifest.json`); the capture is `corpus/source-snapshots/round-79/S113.txt` (sha256 `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf`, 127 lines, 5669 snapshot bytes; the served page was 30242 raw bytes before the capture instrument stripped tags and collapsed whitespace per line).
- **Eight located quotes, one per claimed clause, each verbatim at its snapshot line, word counts by `wc -w`:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| C1 purpose | Q01-purpose | S113.txt:25 | 19 | "Given the source code hashes of C/C++ libraries, this endpoint attempts to find the closest upstream library and version." |
| C2 identifiable set | Q04-library-set | S113.txt:41 | 18 | "The list of libraries that can currently be identified are the C/C++ projects integrated into the OSS-Fuzz project." |
| C3 coverage limit | Q05-coverage-limit | S113.txt:41 | 12 | "This means that not all C/C++ packages are represented in our database." |
| C4 ranked versions | Q06-ranked-versions | S113.txt:55 | 22 | "The API will return a number of possible versions for your package, ranked by how well the version matched your local copy." |
| C5 file_hashes array | Q07-file-hashes | S113.txt:61 | 14 | "An array of MD5 hashes of each relevant file in the library to identify." |
| C6 hash encoding | Q08-hash-encoding | S113.txt:62 | 7 | "the MD5 hash bytes encoded in base64." |
| C7 extension-scoped collection | Q09-extensions | S113.txt:66 | 11 | "saving the MD5 hash of every file with the following extensions:" |
| C8 closeness order | Q10-response-order | S113.txt:85 | 14 | "Returns an array of potential library matches, sorted by how close the match is." |

- **Recheck receipt:** the `recheck:` line above, run against the committed bytes, printed `S113:sha256 OK` and one `S113:<pin> OK occurrences=1 anchor=<n>-ok` line per pinned quote, exit 0; the eight anchors are the exact lines the quotes occupy in the capture (25, 41, 41, 55, 61, 62, 66, 85).

## Limits

The page does not establish, and this entry does not claim:

- rate limits, quotas, an API key or any credential. The capture carries no such sentence: `grep -n -i -E 'rate limit|ratelimit|quota|api key|api_key|authenticat|credential' corpus/source-snapshots/round-79/S113.txt` prints nothing and exits 1.
- pagination of this endpoint's results. The capture carries no such sentence: `grep -n -i -E 'paginat|page_token|next_page_token' corpus/source-snapshots/round-79/S113.txt` prints nothing and exits 1; the 1,000/3,000 thresholds and the page_token rule stay with F54.
- a timeout, a size limit or any maximum for the request or the response. The capture carries no such sentence: `grep -n -i -E 'timeout|limit|maximum' corpus/source-snapshots/round-79/S113.txt` prints nothing and exits 1; the 32 MiB response-size limit stays with F51.
- a severity, CVE or CVSS statement. The capture carries no such sentence: `grep -n -i -E 'severity|CVE|cvss' corpus/source-snapshots/round-79/S113.txt` prints nothing and exits 1; the endpoint returns library and version candidates, and severity is not its subject.
- an error or status-code contract. The capture carries no such sentence: `grep -n -i -E 'error|status code|throttl' corpus/source-snapshots/round-79/S113.txt` prints nothing and exits 1; the 400 Bad Request consequence stated for the single-query endpoint stays with F51.
- worker, thread or proxy behaviour. The capture carries no such sentence: `grep -n -i -E 'worker|thread|proxy' corpus/source-snapshots/round-79/S113.txt` prints nothing and exits 1.
- the extension list itself (S113.txt:67-72), the payload example (S113.txt:75-83), the response schema with its score and repo fields (S113.txt:86-100), the sample response (S113.txt:101-126) and the indexer-api-caller tool section (S113.txt:46-53): they are located in the capture, but no manifest quote pins them, so this entry grounds no clause on them.
- the current state of the page or of any osv.dev host. The manifest records the fetch instant 2026-11-06T18:43:10Z (`corpus/source-snapshots/round-79/manifest.json`), and the capture bytes carry no timestamp. This entry made no query against osv.dev.

Scope limit: the determineversion endpoint's own eight clauses — the purpose (S113.txt:25), the identifiable-library set and its coverage limit (S113.txt:41), the ranked-versions response (S113.txt:55), the MD5 file_hashes array and its base64 encoding (S113.txt:61, S113.txt:62), the extension-scoped hash collection (S113.txt:66) and the closeness-sorted matches array (S113.txt:85) — as stated on the POST /v1experimental/determineversion page only. The single-query contract stays with F51 (S108), the batch contract with F54 (S112), and the OSV record format with F31 (S080).
