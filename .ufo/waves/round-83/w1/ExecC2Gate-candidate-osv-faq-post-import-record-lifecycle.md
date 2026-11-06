# What OSV.dev does to a record after import: withdrawn records leave query results but stay retrievable by ID, upstream deletions become withdrawn (GCS, with a 10% abort) or stay valid but orphaned (REST and Git), the modified_id.csv listing, and alias recomputation that bumps modified

source: S117 — https://google.github.io/osv.dev/faq/ (anchor: the OSV.dev FAQ page, sections "I want to only download the recently added/changed records", "What does OSV.dev do to the records it imports?", "How does OSV.dev handle withdrawn records?" and "How does OSV.dev handle deleted records?", capture corpus/source-snapshots/round-83/S117.txt)
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-83/manifest.json --source S117

## Attribution

This is the OSV.dev project's own FAQ page; its navigation lists the API pages and data-source pages beside it (S117.txt:2-12) and the page title is "FAQ | OSV" (S117.txt:1). Every quoted clause below is the page's own statement, quoted from the pinned capture `corpus/source-snapshots/round-83/S117.txt` with the line the text occupies; the paraphrases, falsifiable rules, rejected over-generalizations and the bounty-ground rationale are this entry's.

Why it is bounty ground: a researcher who cites an OSV record as evidence that a package is (or is not) affected relies on what a query returns today. This page states the ways a record that was imported can drop out of query results, stay listed after its upstream source deleted it, or change after import; F58 (`corpus/knowledge/osv-high-quality-record-import-bar.md`) holds the bar a record meets at import and leaves this later state to a separate document (S116.txt:27).

## Claim 1 — withdrawn records are excluded from POST query results

"Records that have the withdrawn field set will be excluded from:" (S117.txt:112). The exclusion list that follows names the responses to POST API queries and the main list page with related search results (S117.txt:113-114, outside the pinned span).

Falsifiable rule: a researcher who reads an empty POST /v1/query answer as proof that no advisory exists has not ruled out a record excluded because its withdrawn field is set (S117.txt:112-113). A reader checks it by reading the first sentence and its first list item under the withdrawn-records question.

Rejected over-generalization, not a page sentence: a withdrawn advisory is erased from OSV.dev entirely. The same answer says the entry remains in the database (S117.txt:115, not pinned) and lists where it is still served (Claim 2).

## Claim 2 — a withdrawn record is still returned by the GET-by-ID API

"returned by the /vulns/<ID> GET API" (S117.txt:116). After withdrawal the entry remains in the database and the by-ID GET API still returns it; the same list adds the osv.dev vulnerability page, marked withdrawn, and the GCS exports with the withdrawn field (S117.txt:115-118, Q02 pins line 116 only).

Falsifiable rule: a tool that treats a 200 from the vulns GET by ID as proof the advisory is live misses the withdrawn case the page names, since that API still returns withdrawn entries (S117.txt:116). A reader checks it by reading the list after "The entry remains in the database".

Rejected over-generalization, not a page sentence: every OSV.dev surface hides withdrawn records. The page excludes them from POST queries and lists (S117.txt:112-114) and keeps them on the by-ID API, the vulnerability page and the exports (S117.txt:116-118).

## Claim 3 — GCS-sourced deletions become withdrawn, with a 10% abort threshold

"if more than 10% of records are about to be marked as withdrawn, OSV.dev aborts and does not proceed." (S117.txt:121). For GCS sources a record deleted upstream is marked withdrawn, and the threshold guards against feed availability issues (S117.txt:121, the sentences before the pinned span).

Falsifiable rule: a GCS import that is about to mark more than 10% of records as withdrawn aborts and does not proceed, so a mass upstream deletion can leave those records unmarked after that import (S117.txt:121); the page does not state whether the 10% is measured over the source's records or over all records. A reader checks it by reading the GCS sources sentence under the deleted-records question.

Rejected over-generalization, not a page sentence: OSV.dev applies the 10% threshold to every import source. The page states it for GCS sources (S117.txt:121) and describes REST and Git sources separately (Claim 4).

## Claim 4 — REST and Git deletions leave records valid but orphaned

"REST and Git sources: OSV.dev leaves the existing records valid but orphaned." (S117.txt:122). A record whose upstream REST or Git source deleted it is still a valid OSV.dev record at the capture instant; the page says this will change to match the GCS handling and links two issues (S117.txt:122, after the pinned span).

Falsifiable rule: a record still served for a REST or Git source is not proof its upstream advisory exists, because deleted upstream records there stay valid but orphaned (S117.txt:122). A reader checks it by reading the REST and Git sentence under the deleted-records question.

Rejected over-generalization, not a page sentence: OSV.dev withdraws every record its upstream deletes. The page marks withdrawn only for GCS sources (S117.txt:121) and names the REST and Git behaviour as still to be changed (S117.txt:122).

## Claim 5 — modified_id.csv lists recently added or changed records

"we provide a modified_id.csv file that can be used to identify recently added or changed vulnerability records" (S117.txt:94). The file sits at the root of the GCS bucket, with rows formatted `<iso modified date>,<ecosystem_dir>/<id>` (S117.txt:94-98), and a per-ecosystem copy sorted in reverse chronological order (S117.txt:99-100; Q05 pins line 94 only).

Falsifiable rule: a mirror that tracks the modified_id.csv file can find recently changed vulnerability records without a full download, since the page names it for identifying added or changed records and describes streaming the reverse-chronological file since the last download (S117.txt:94, 100). A reader checks it by reading the answer under the recently added/changed records question.

Rejected over-generalization, not a page sentence: a mirror must download the full database to learn which records changed. The page names modified_id.csv for identifying added or changed records and describes streaming the reverse-chronological file since the last download (S117.txt:94, 100); deletion handling is a separate answer (S117.txt:119-122).

## Claim 6 — a change to the aliases field updates the record's modified field

"any time the aliases field changes, the record’s modified field is updated" (S117.txt:108). OSV.dev recomputes aliases in repeated batches after import, and that recomputation is one of four listed post-import operations beside version enumeration, purl computation and Git commit enumeration (S117.txt:104-108).

Falsifiable rule: a researcher who reads a newer modified timestamp as a changed affected range may be looking at an alias change, which the page says also updates the modified field (S117.txt:108). A reader checks it by reading the fourth item under the records-it-imports question.

Rejected over-generalization, not a page sentence: the modified field records only changes made by the upstream source. The page lists OSV.dev's own batch alias recomputation as a cause (S117.txt:108).

## Distinctness

- F58 / S116 (`corpus/knowledge/osv-high-quality-record-import-bar.md`) holds the import bar: what a record must meet to be imported. It names revalidation after import as out of scope and points to a companion document (S116.txt:27, not pinned there). This entry holds what OSV.dev does after import, from a different page (the FAQ), and does not claim that companion document's content.
- F57 / S115 (`corpus/knowledge/osv-importfindings-record-quality-feedback.md`) holds the endpoint that reports records that failed import; this entry holds records that were imported.
- F51 / S108 (`corpus/knowledge/osv-post-v1-query-contract.md`) holds the POST /v1/query contract and lists GET /v1/vulns/{id} as navigation only (its Limits). Claims 1 and 2 add the withdrawn exclusion and retention the FAQ states; they do not restate the query contract.
- F47 / S103 (`corpus/knowledge/github-global-security-advisories-rest-api.md`) carries an `is_withdrawn` field of GitHub's own API (S103.txt:306-307); that is GitHub's schema, not OSV.dev's handling.
- Literal sweep over the other 96 entries for the six pinned quotes: 0 files each (`.ufo/waves/round-83/controls/c2-prefreeze-r83.txt`).

## Not claimed

Not claimed: the withdrawn exclusion's second list item (main list page and search, S117.txt:114) beyond Claim 1's paraphrase; the osv.dev page and GCS export retention (S117.txt:117-118) beyond Claim 2's paraphrase; the two upstream issue links (S117.txt:122, unopened leads); the per-ecosystem modified_id.csv and its sort order (S117.txt:99-100) beyond Claim 5's paraphrase; version enumeration, purl computation and commit-to-tag mapping (S117.txt:105-107) and the affected.versions[] notes (S117.txt:109-110); the data-correction route (S117.txt:86-88); the database download and contribution answers (S117.txt:89-92, 101-103); the rate-limit, response-size and SLO answers (S117.txt:123-136), including the 15-minute data freshness objective (S117.txt:136).

## Gate — S117 (OSV.dev FAQ)

- **URL:** https://google.github.io/osv.dev/faq/ (HTTP 200; the manifest records the final URL equal to the requested URL).
- **Access date:** 2026-11-06. Capture `corpus/source-snapshots/round-83/S117.txt` (sha256 `0a5fa51c987544789d3c84fee6be2b1246a7a6a865457668f9e94a37e60bd53e`, 137 lines, 10229 snapshot bytes; the served page was 34381 raw bytes), `fetched_utc 2026-11-06T21:55:29Z`.
- **Six located quotes, one per claimed clause, each verbatim at its snapshot line, word counts by `len(quote.split())`:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| cl1 withdrawn excluded | Q01-withdrawn-excluded | S117.txt:112 | 11 | Records that have the withdrawn field set will be excluded from: |
| cl2 withdrawn by ID | Q02-withdrawn-get | S117.txt:116 | 6 | returned by the /vulns/<ID> GET API |
| cl3 GCS 10% abort | Q03-gcs-ten-percent | S117.txt:121 | 19 | if more than 10% of records are about to be marked as withdrawn, OSV.dev aborts and does not proceed. |
| cl4 REST/Git orphaned | Q04-rest-git-orphaned | S117.txt:122 | 12 | REST and Git sources: OSV.dev leaves the existing records valid but orphaned. |
| cl5 modified_id.csv | Q05-modified-id-csv | S117.txt:94 | 17 | we provide a modified_id.csv file that can be used to identify recently added or changed vulnerability records |
| cl6 aliases bump modified | Q06-aliases-bump-modified | S117.txt:108 | 12 | any time the aliases field changes, the record’s modified field is updated |

- **Recheck receipt:** the `recheck:` line above printed `S117:sha256 OK` and one `S117:<pin> OK occurrences=1 anchor=<n>-ok` line per pinned quote, exit 0 (`.ufo/waves/round-83/controls/c2-prefreeze-r83.txt`).

## Limits

The page does not establish, and this entry does not claim:

- the content of "Managing the Perishability of OSV Records" (S116.txt:27): the round-83 search found no public copy; this FAQ is the OSV.dev page that states post-import handling, not that document.
- that any specific record is withdrawn, orphaned or alias-updated; this entry made no call to api.osv.dev and read no GCS object.
- when the REST and Git behaviour changes; the page states the intent and links two issues (S117.txt:122) that this entry did not open.
- the current state of the page: the manifest records the fetch instant 2026-11-06T21:55:29Z.

Scope limit: six post-import statements of the OSV.dev FAQ only — the withdrawn exclusion (S117.txt:112), withdrawn retrieval by ID (S117.txt:116), the GCS 10% abort (S117.txt:121), REST and Git orphaning (S117.txt:122), the modified_id.csv listing (S117.txt:94) and the alias-driven modified update (S117.txt:108). The import bar stays with F58 (S116) and the import-findings endpoint with F57 (S115).
