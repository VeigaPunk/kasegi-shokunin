# OSV.dev GET /v1experimental/importfindings/{source}: the purpose, the audience, the not-imported consequence, the single source parameter, the URL template and the source.yaml name

source: S115 — https://google.github.io/osv.dev/get-v1-importfindings/ (anchor: the GET /v1experimental/importfindings page, capture corpus/source-snapshots/round-81/S115.txt)
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-81/manifest.json --source S115

## Attribution

This is the OSV.dev project's own reference page for one experimental endpoint of its API, the page headed `GET /v1experimental/importfindings` and `GET /v1experimental/importfindings/{source}` (S115.txt:22-23). Every claim below is that page's own declared behaviour, quoted from the pinned capture `corpus/source-snapshots/round-81/S115.txt` with the line the text occupies. The page sits at `https://google.github.io/osv.dev/get-v1-importfindings/`, the URL the manifest records as both the requested and the final URL at HTTP 200 (`corpus/source-snapshots/round-81/manifest.json`, `fetched_utc 2026-11-06T20:11:18Z`).

## Claim 1 — the purpose: a source's records that fail import-time quality checks

"Given a specific OSV.dev source, report any records that are failing import-time quality checks." (S115.txt:25). The input is one OSV.dev source and the output is that source's records that fail the checks OSV.dev runs at import time (S115.txt:25).

Falsifiable rule: a caller that uses this endpoint to look up vulnerabilities affecting a package has the wrong endpoint; the page's summary names records of a source that fail import-time quality checks, not affected packages (S115.txt:25). A reader checks it by reading the page's one-line summary.

Rejected over-generalization, not a page sentence: the endpoint reports every record a source publishes, with a pass or fail mark. The summary says it reports the records that are failing import-time quality checks (S115.txt:25).

## Claim 2 — the audience: operators of the home databases OSV.dev imports from

"It is targeted to operators of home databases that OSV.dev imports from." (S115.txt:32). The page names who the endpoint is for: the operators of the upstream databases OSV.dev imports records from (S115.txt:32).

Falsifiable rule: a bounty hunter or a scanner author is not the audience the page names; a plan that treats this endpoint as a consumer-side vulnerability feed contradicts S115.txt:32. A reader checks it by reading the second sentence of the Experimental endpoint paragraph.

Rejected over-generalization, not a page sentence: only home-database operators are allowed to call the endpoint. The page says the endpoint is targeted to them (S115.txt:32); it states no access restriction (see Limits).

## Claim 3 — the consequence: a record below the quality bar is not imported

"a machine-readable way to reason about records they have published that do not meet OSV.dev’s quality bar (and therefore have not been imported)." (S115.txt:34). A published record that fails the quality bar is a record OSV.dev has not imported, and the endpoint is the machine-readable report of such records (S115.txt:34).

Falsifiable rule: reading the absence of an advisory from OSV.dev as proof that the home database never published it contradicts S115.txt:34, which describes published records that were not imported because they failed the quality bar. A reader checks it by reading the Purpose paragraph.

Rejected over-generalization, not a page sentence: OSV.dev repairs a failing record and imports a corrected version. The page says records that do not meet the quality bar have not been imported (S115.txt:34); it states no repair step.

## Claim 4 — the only parameter is the source

"The only parameter you need for this API call is the source, in order to construct the URL." (S115.txt:36). The call takes one parameter, and that parameter is part of the URL, not a request body (S115.txt:36).

Falsifiable rule: a request that sends a JSON body with a package or a version to this endpoint carries parameters the page does not name; the page states the source is the only parameter and that it builds the URL (S115.txt:36). A reader checks it by reading the Parameters paragraph.

Rejected over-generalization, not a page sentence: the endpoint accepts a list of sources in one call. The page names a single source as the only parameter (S115.txt:36).

## Claim 5 — the URL template

"https://api.osv.dev/v1experimental/importfindings/{source}" (S115.txt:37). The source is the last path segment under `api.osv.dev/v1experimental/importfindings/` (S115.txt:37).

Falsifiable rule: a call to `https://api.osv.dev/v1/importfindings/<source>` is not the template the page gives; the template carries `v1experimental` (S115.txt:37). A reader checks it by reading the line after the Parameters sentence.

Rejected over-generalization, not a page sentence: the source may be passed as a query-string parameter. The page gives the source as a path segment of the URL template (S115.txt:37).

## Claim 6 — the source value is the name value in source.yaml

"The source value is the same as the name value in source.yaml" (S115.txt:38). The string a caller puts in the URL is the `name` a source carries in OSV.dev's `source.yaml` (S115.txt:38).

Falsifiable rule: an operator who passes the display name of its project, or a record-id prefix it does not use as its `source.yaml` name, is not passing the value S115.txt:38 names. A reader checks it by reading the sentence after the URL template.

Rejected over-generalization, not a page sentence: the source value is the record-id prefix of the source's advisories. The page ties the value to the name value in source.yaml only (S115.txt:38); the sample's `EX-1234` id and `example` source (S115.txt:41-43, not pinned) are sample data.

## Distinctness

- F51 / S108 (`corpus/knowledge/osv-post-v1-query-contract.md`) holds the single-query contract, the case-sensitivity rule for API requests (`corpus/knowledge/osv-post-v1-query-contract.md:31`, quoting S108.txt:53) and a Limits bullet listing "the experimental endpoints" without describing them (`corpus/knowledge/osv-post-v1-query-contract.md:75`). This page repeats the case-sensitivity note (S115.txt:39); it is not pinned and not claimed here. No F51 clause is restated.
- F54 / S112 (`corpus/knowledge/osv-post-batch-query-contract.md`) holds the batch contract; F55 / S113 (`corpus/knowledge/osv-determineversion-cc-library-versioning.md`) and F56 / S114 (`corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md`) hold the two pre-query experimental endpoints. All three are consumer-side calls; this endpoint is the publisher-side report on import failures, and none of its six clauses is held by them.
- F31 / S080 (`corpus/knowledge/osv-affected-range-events.md`) holds the OSV record's affected-range events format; this entry holds no schema rule, and the example response's field names (S115.txt:43) are not claimed.
- Subject sweep `grep -rli 'importfindings' corpus/knowledge/` (2026-11-06, before this entry) prints nothing and exits 1; `grep -rli 'source.yaml' corpus/knowledge/` and `grep -rli 'home database' corpus/knowledge/` likewise print nothing.

## Not claimed

Not claimed: the experimental-status sentences of S115.txt:32 other than the audience sentence ("This API endpoint is still considered experimental." and the feedback request) — F51's Limits bullet already lists the experimental endpoints (`corpus/knowledge/osv-post-v1-query-contract.md:75`); the case-sensitivity note of S115.txt:39 — held by F51 (`corpus/knowledge/osv-post-v1-query-contract.md:31`); the request sample (S115.txt:41) and the example 200 response (S115.txt:43) — sample data, not rules.

## Gate — S115 (OSV.dev GET /v1experimental/importfindings/{source})

- **URL:** https://google.github.io/osv.dev/get-v1-importfindings/ (HTTP 200; the manifest records the final URL equal to the requested URL).
- **Access date:** 2026-11-06. The committed capture's `fetched_utc` is 2026-11-06T20:11:18Z (`corpus/source-snapshots/round-81/manifest.json`); the capture is `corpus/source-snapshots/round-81/S115.txt` (sha256 `e304eb88c7d79a6d2a1e4369c3e9a4fcf18f3ff4aabd6ad86466e85daf3f6f7f`, 44 lines, 2224 snapshot bytes; the served page was 16418 raw bytes before the capture instrument stripped tags and collapsed whitespace per line).
- **Six located quotes, one per claimed clause, each verbatim at its snapshot line, word counts by `len(quote.split())`:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| cl1 purpose | Q01-purpose | S115.txt:25 | 14 | Given a specific OSV.dev source, report any records that are failing import-time quality checks. |
| cl2 audience | Q02-audience | S115.txt:32 | 12 | It is targeted to operators of home databases that OSV.dev imports from. |
| cl3 not imported | Q03-not-imported | S115.txt:34 | 23 | a machine-readable way to reason about records they have published that do not meet OSV.dev’s quality bar (and therefore have not been imported). |
| cl4 only parameter | Q04-only-parameter | S115.txt:36 | 18 | The only parameter you need for this API call is the source, in order to construct the URL. |
| cl5 URL template | Q05-url-template | S115.txt:37 | 1 | https://api.osv.dev/v1experimental/importfindings/{source} |
| cl6 source.yaml name | Q06-source-yaml-name | S115.txt:38 | 12 | The source value is the same as the name value in source.yaml |

- **Recheck receipt:** the `recheck:` line above, run against the committed bytes, printed `S115:sha256 OK` and one `S115:<pin> OK occurrences=1 anchor=<n>-ok` line per pinned quote, exit 0 (`.ufo/waves/round-81/controls/c2-prefreeze-r81.txt`); the six anchors are the exact lines the quotes occupy in the capture (25, 32, 34, 36, 37, 38).

## Limits

The page does not establish, and this entry does not claim:

- rate limits, quotas, an API key or any credential: `grep -n -i -E 'rate limit|ratelimit|quota|api key|api_key|authenticat|credential' corpus/source-snapshots/round-81/S115.txt` prints nothing and exits 1.
- pagination: `grep -n -i -E 'paginat|page_token|next_page_token' corpus/source-snapshots/round-81/S115.txt` prints nothing and exits 1.
- an error or status-code contract beyond the heading of the 200 example: `grep -n -i -E 'error|status code|throttl|404|400' corpus/source-snapshots/round-81/S115.txt` prints nothing and exits 1.
- the list of finding types or what each means; the one value shown, `IMPORT_FINDING_TYPE_INVALID_JSON`, sits in the example response (S115.txt:43), not pinned.
- the quality bar itself: the page links it as a separate document ("Properties of a High Quality OSV Record", S115.txt:14, navigation only), which this entry does not open.
- the current state of the page or of api.osv.dev. The manifest records the fetch instant 2026-11-06T20:11:18Z; this entry made no call to api.osv.dev.

Scope limit: the importfindings endpoint's own six clauses — the purpose (S115.txt:25), the audience (S115.txt:32), the not-imported consequence (S115.txt:34), the single source parameter (S115.txt:36), the URL template (S115.txt:37) and the source.yaml name (S115.txt:38) — as stated on the GET /v1experimental/importfindings page only. The query contracts stay with F51 (S108) and F54 (S112), the pre-query experimental endpoints with F55 (S113) and F56 (S114), and the OSV record format with F31 (S080).
