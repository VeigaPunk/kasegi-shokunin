# OSV.dev POST /v1/query service contract: the payload, the version rule, the Git-tag query, pagination and the response size limit

source: S108 — https://google.github.io/osv.dev/post-v1-query/ (anchor: the POST /v1/query page, capture corpus/source-snapshots/round-73/S108.txt)
verified-at: 2026-11-05
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-73/manifest.json --source S108

## Attribution

This is the OSV.dev project's own reference page for one endpoint of its query service, `POST /v1/query`. Every statement below is that page's declared contract for the endpoint's request and response. The page's own summary of the endpoint is "Lists vulnerabilities for given package and version. May also be queried by commit hash." (S108.txt:24). The page states how a request is shaped and what a response may carry. It does not state how a returned vulnerability record is structured; that is the record format held by F31 (`corpus/knowledge/osv-affected-range-events.md`, S080). This entry instructs no call against osv.dev or any other host, and every check replays the pinned capture.

## Claim 1 — the payload has four top-level keys; a commit query carries no version

The payload object's keys sit at S108.txt:58-67. Two of them are quoted here: `"commit": "string",` (S108.txt:59) and `"page_token": "string"` (S108.txt:66). The commit form is named in the parameter table: "commit string The commit hash to query for. If specified, version should not be set." (S108.txt:34). The package object is optional when a commit hash is given: "When a commit hash is given, this is optional." (S108.txt:36).

Falsifiable rule: a payload that sets `commit` and also sets a top-level `version` contradicts S108.txt:34. A reader checks it by reading the two lines of the parameter table.

Rejected over-generalization, not a page sentence: a commit query needs a package name, as a package-and-version query does. The page's own sentence at S108.txt:36 says the package object is optional with a commit.

## Claim 2 — the version goes in exactly one place, and the version match is fuzzy

The page's version rule: "Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both." (S108.txt:40). "Requests that specify the version in both places return 400 Bad Request." (S108.txt:41). The page labels its invalid example "Invalid (400 Bad Request):" (S108.txt:47). The example itself is `{ "package": { "purl": "pkg:pypi/jinja2@3.1.4" }, "version": "3.1.4" }` (S108.txt:48). The valid form with the version only at top level is `{ "package": { "purl": "pkg:pypi/jinja2" }, "version": "3.1.4" }` (S108.txt:46).

The version parameter's own description states the exclusion: "If set, commit must not be used, and package.purl must not include a version." (S108.txt:35). The top-level version is a fuzzy match, not an exact one: "A fuzzy match is done against upstream versions." (S108.txt:35).

Falsifiable rule: a request whose purl ends in `@<version>` and whose top-level `version` is also set is a 400 by S108.txt:41. A reader checks the pair by printing S108.txt:46-48 and reading the purl against the version.

Rejected over-generalization, not a page sentence: the version is matched exactly, so `1.0` and `1.0.0` are different queries. The page's only version-matching sentence is the fuzzy one (S108.txt:35), and it states no exact-match rule.

## Claim 3 — package names match exactly, with three named ecosystem exceptions

The name rule: "Package names are matched exactly, except in ecosystems whose registry treats other spellings as the same package:" (S108.txt:54). The page then names three exceptions on that line: "PyPI names are normalized as described in PEP 503," and "NuGet names are matched case-insensitively," and "crates.io names are matched case-insensitively with" (each S108.txt:54). Parameter names and values are case-sensitive: "Case Sensitivity: API requests are case-sensitive." (S108.txt:53).

Falsifiable rule: a name in an ecosystem the page does not list at S108.txt:54 is matched as an exact string. A reader checks it by counting the exceptions on that one line.

Rejected over-generalization, not a page sentence: every package name is matched case-insensitively. The page states exact matching and names three exceptions; a universal case-insensitive rule is not on the page.

## Claim 4 — the Git-tag query: ecosystem GIT, a repository URL in name, the tag in version

The page states the Git-tag form: "To do so, set the ecosystem to GIT, enter the full URL of the repository to the name field," and "and the tag into the version field." (S108.txt:56). The example payload is `{"package": {"name": "https://github.com/curl/curl.git", "ecosystem": "GIT"}, "version": "8.5.0"}` (S108.txt:79).

Falsifiable rule: a Git-tag query names `GIT` as the ecosystem, puts a full repository URL in `name`, and puts the tag in `version`. A reader checks each part against S108.txt:56 and the example at S108.txt:79.

Rejected over-generalization, not a page sentence: the Git-tag query matches the tag exactly. The page gives no exact-match rule for Git tags, and the only matching sentence for the version field is the fuzzy one (S108.txt:35).

## Claim 5 — pagination: a next_page_token means more results, and the query repeats with page_token

The page says when a response is paginated: "If your previous query fetched a large number of results, the response will be paginated." (S108.txt:37). It states the trigger for the v1/query endpoint: "pagination will occur when there more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds." (S108.txt:136). It states what the token means: "When pagination is used, the next_page_token is given in the response, indicating that there are more results to return." (S108.txt:135). It states the loop: "repeating queries until the next_page_token is no longer included in the response." (S108.txt:135). The next request must carry the token: "To get the next page of results, your next request must include page_token:" (S108.txt:144). A response may carry only the token: "In rare cases, the response might contain only the next_page_token." (S108.txt:149), and "please keep querying with the next_page_token until either results are returned, or no more page tokens are returned." (S108.txt:149). The page size is not fixed: "The page size can vary slightly because of threading and may change in the future." (S108.txt:136).

Falsifiable rule: a response that contains `next_page_token` is not the complete answer to the query. The page's sample of the paginated response is at S108.txt:137-143, with the token beside `vulns`, and the loop rule is at S108.txt:135.

Rejected over-generalization, not a page sentence: the API lists every vulnerability for a package in one response. The page states the trigger at S108.txt:136 (more than 1,000 vulnerabilities, or more than 20 seconds of query time), and the token mechanism exists for that case (S108.txt:135).

## Claim 6 — the 32 MiB limit is an HTTP/1.1 limit; HTTP/2 has no stated limit

The size sentence sits on one line: "The API has a response size limit of 32MiB when using HTTP/1.1." (S108.txt:148). The same line continues: "There is no limit when using HTTP/2." (S108.txt:148). The page then recommends a protocol: "We recommend using HTTP/2 for queries that may result in large responses." (S108.txt:148).

Falsifiable rule: the 32 MiB sentence is conditioned on HTTP/1.1. A HTTP/2 response above 32 MiB is not contrary to S108.txt:148. A reader checks it on the one line.

Rejected over-generalization, not a page sentence: every OSV response is capped at 32 MiB. The same line states no limit under HTTP/2, so the cap is conditioned on the protocol.

## Distinctness

- F31 / S080 (OSV record format, `corpus/knowledge/osv-affected-range-events.md`): the record's `affected[].ranges[].events` timeline. S108 shows a sample record only as a response body (S108.txt:82-133) and states no record field. The S080 registry row (`corpus/SOURCES.md:86`) excludes the osv.dev service API from its scope, and F31's scope limit names the service API as out of scope (`PROVINCE.md:178`). This entry admits that named gap and leaves the record format to F31.
- F25 (the CVE JSON record format, `corpus/README.md:591`) is a different format and does not own the OSV record.
- F47 / S103 and F36 / S087 are GitHub's advisory REST interfaces; no route, parameter or limit of this page is theirs.

## Limits

The page does not establish, and this entry does not claim:

- rate limits or quotas on `POST /v1/query`. The capture has no sentence on either: `grep -n -i 'rate limit\|ratelimit\|quota\|api key\|api_key\|authenticat\|credential' S108.txt` prints nothing. The only limit sentences are the pagination trigger (S108.txt:136) and the HTTP/1.1 size limit (S108.txt:148).
- authentication, an API key or any credential. The same grep prints no sentence stating either.
- the overview page at the API root (`api/`). S108 is the query page only; the overview's own statements are not in this capture.
- the OSV record format. The sample response (S108.txt:82-133) is shown as a response; its fields belong to F31.
- the other endpoints in the page's navigation (POST /v1/querybatch, GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). They are listed, not described.
- the algorithm of the fuzzy version match: "A fuzzy match is done against upstream versions." (S108.txt:35) names no method.
- which tags a Git query returns. The page gives one example (S108.txt:79) and no tag-matching rule beyond the version sentence.
- the current state of the page or of any osv.dev host. The pinned capture is the 2026-11-05T07:40:48Z fetch; this entry made no query against osv.dev.

Scope limit: the request and response contract of `POST /v1/query` only. The OSV record format stays with F31; the other endpoints stay out.
