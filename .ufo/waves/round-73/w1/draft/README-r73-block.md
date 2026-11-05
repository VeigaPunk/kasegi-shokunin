
## Round-73 admission — coverage map row and Frontier F51 (2026-11-05)

Appended amendment (R6): the round-73 entry `corpus/knowledge/osv-post-v1-query-contract.md` (Frontier F51, source S108) rests on the OSV.dev project's own reference page for the POST /v1/query endpoint at https://google.github.io/osv.dev/post-v1-query/, captured `corpus/source-snapshots/round-73/S108.txt` (sha256 304baa7d...c6b9, 150 lines, 31 pinned quotes), manifest `corpus/source-snapshots/round-73/manifest.json`. The coverage map above is not edited in place (R6); the coverage-map row is appended here, and the F51 frontier row uses the same six-cell table shape as F50.

| Area | Entry | Source basis |
|---|---|---|
| OSV.dev query service contract: the POST /v1/query payload, version rule, Git-tag query, pagination and HTTP/1.1 size limit (round 73) | knowledge/osv-post-v1-query-contract.md | S108, OSV.dev project's API reference for the query endpoint, opened 2026-11-05 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F51 | OSV.dev POST /v1/query service contract — the request payload (commit, version, package, page_token), the version rule (one place only, never both the top-level field and the purl), the Git-tag query, pagination with next_page_token and its 1,000-vulnerability and 20-second triggers, and the 32 MiB HTTP/1.1 response limit with no stated limit on HTTP/2 | admitted | knowledge/osv-post-v1-query-contract.md | S108 | Read the version in one place only (S108.txt:40-41) and read a response that carries next_page_token as partial until the token is absent (S108.txt:135, :144); the page states no rate limit and no API-key rule, so a reader must not supply either from the OSV overview page or another tracker, and the entry's Limits section records both absences as measured on the capture.

[r73 amendment, appended 2026-11-05] The frontier as of round 73 is F01-F51 admitted: F51 at round 73. The C2 admission rests on S108 alone; the F31 scope limit stays as written and the OSV record format is not claimed by this entry.
