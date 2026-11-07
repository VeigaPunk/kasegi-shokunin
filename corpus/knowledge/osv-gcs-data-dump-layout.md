# How OSV.dev lays out its GCS data dump: the full zip includes withdrawn records, per-record JSON paths, the [EMPTY]/ directory for ecosystem-less records, prefix-less per-ecosystem modified_id.csv rows, colon-suffixed ecosystems folded into their base directory, and no more prefixed exports

source: S118 — https://google.github.io/osv.dev/data/ (anchor: the OSV.dev "Data sources" page, sections "Data dumps", "Full database download", "Per-ecosystem downloads", "Format and Usage" and "Ecosystem naming", capture corpus/source-snapshots/round-84/S118.txt)
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-84/manifest.json --source S118

## Attribution

This is the OSV.dev project's own "Data sources" page; its navigation lists the API pages, the FAQ and the record-quality page beside it (S118.txt:2-17) and the page title is "Data sources | OSV" (S118.txt:1). Every quoted clause below is the page's own statement, quoted from the pinned capture `corpus/source-snapshots/round-84/S118.txt` with the line the text occupies; the paraphrases, falsifiable rules, rejected over-generalizations and the bounty-ground rationale are this entry's.

Why it is bounty ground: a researcher who argues from the OSV data set offline (a bulk count of advisories for a package, a diff of what changed since a report was filed, a check that an advisory exists for an ecosystem) reads the GCS export, not the query API. This page states which records that export holds and where: withdrawn records are inside the full zip, ecosystem-less records sit in their own directory, per-ecosystem change lists drop a path prefix, and colon-suffixed ecosystems are folded into their base directory. F59 (`corpus/knowledge/osv-faq-post-import-record-lifecycle.md`) holds the FAQ's statements of what happens to a record after import; this entry holds the export layout that a consumer reads those records from.

## Claim 1 — the full-database zip includes withdrawn records

"This bucket contains a zip file with all vulnerabilities across all ecosystems (including withdrawn records) at gs://osv-vulnerabilities/all.zip." (S118.txt:102). The page calls this the easiest way to download the entire OSV database (S118.txt:102, after the pinned span).

Falsifiable rule: a count of vulnerabilities taken from the full OSV zip overstates the live set unless the counter drops the records that are withdrawn, since that archive carries withdrawn records as well (S118.txt:102); the page does not name the field that marks them, which F59 gives as the withdrawn field (S117.txt:112). A reader checks it by reading the first sentence under "Full database download".

Rejected over-generalization, not a page sentence: every file in the OSV dump is an advisory that is still in force. The page says the full archive includes withdrawn ones (S118.txt:102), and F59 states that a withdrawn entry leaves POST query results (S117.txt:112).

## Claim 2 — each record is exported as its own JSON object under its ecosystem directory

"Individual vulnerability records can be found at gs://osv-vulnerabilities/<ECOSYSTEM>/<ID>.json." (S118.txt:104). The same paragraph adds a per-ecosystem zip at `<ECOSYSTEM>/all.zip` (S118.txt:104, after the pinned span).

Falsifiable rule: a single advisory can be fetched from the bucket by ecosystem name and identifier without downloading any zip, because the page names one JSON object per vulnerability at that path (S118.txt:104). A reader checks it by reading the first sentence under "Per-ecosystem downloads".

Rejected over-generalization, not a page sentence: the bucket only serves bulk archives, so a single advisory needs the whole ecosystem zip. The page lists per-record objects beside the per-ecosystem zip (S118.txt:104).

## Claim 3 — records without an ecosystem are exported to the [EMPTY]/ directory

"Vulnerabilities without an ecosystem (typically withdrawn ones) are exported to the gs://osv-vulnerabilities/[EMPTY]/ directory." (S118.txt:104).

Falsifiable rule: a scan that walks only the named ecosystem directories of the bucket misses records that carry no ecosystem, which the page places in a separate [EMPTY]/ directory and says are typically withdrawn (S118.txt:104). A reader checks it by reading the last sentence under "Per-ecosystem downloads".

Rejected over-generalization, not a page sentence: every exported record sits under one of the ecosystem directories listed on the page. The page names a separate directory for ecosystem-less records (S118.txt:104), and the covered-ecosystems list (S118.txt:66-96) has no such entry.

## Claim 4 — per-ecosystem modified_id.csv rows carry no ecosystem directory prefix

"The per-ecosystem files omit the <ecosystem_dir>/ prefix." (S118.txt:114). The top-level file's rows are `<iso modified date>,<ecosystem_dir>/<id>` (S118.txt:114, before the pinned span), and each ecosystem directory holds its own copy listing only that ecosystem (S118.txt:112).

Falsifiable rule: a parser written for the top-level modified_id.csv that splits the second column on a slash breaks on the per-ecosystem files, whose rows omit the directory prefix and give the bare identifier (S118.txt:114). A reader checks it by reading the two sentences under "Format and Usage".

Rejected over-generalization, not a page sentence: the top-level and per-ecosystem change lists share one row format. The page states the per-ecosystem files drop the directory part (S118.txt:114).

## Claim 5 — colon-suffixed ecosystems are folded into the base ecosystem directory

"the data dump will always contain an ecosystem directory without the :.* suffix (e.g. Alpine)." (S118.txt:121). That directory holds every advisory of the ecosystems sharing the prefix, the page's example being all Alpine release variants (S118.txt:121, after the pinned span).

Falsifiable rule: a script that resolves a release-suffixed ecosystem string such as an Alpine version to a dump directory of the same spelling is resolving a name the page does not export under: the advisories are exported under the base name without the suffix (S118.txt:121), and exports for the suffixed names have stopped (S118.txt:123). A reader checks it by reading the first paragraph under "Ecosystem naming" and the note at its end.

Rejected over-generalization, not a page sentence: every ecosystem value that appears in a record has its own directory in the dump. The page folds the suffixed values into the base directory (S118.txt:121).

## Claim 6 — OSV.dev no longer exports the prefixed ecosystem entries

"OSV.dev has stopped exporting entries for ecosystems with prefixes (e.g. All Alpine:.*)." (S118.txt:123). The note tells readers to use only the main ecosystem directory, the one without the suffix (S118.txt:123, after the pinned span).

Falsifiable rule: a mirror built before this change that still reads a suffixed Alpine directory is reading data the export no longer refreshes, so its changes after the stop are missing from that copy (S118.txt:123). A reader checks it by reading the note at the end of "Ecosystem naming".

Rejected over-generalization, not a page sentence: the suffixed directories remain a supported alternative view of the same data. The page says those exports stopped and points readers to the main directory (S118.txt:123).

## Distinctness

- F59 / S117 (`corpus/knowledge/osv-faq-post-import-record-lifecycle.md`) holds the FAQ's post-import statements, including that withdrawn records stay in the GCS exports with the withdrawn field (its Claim 2 paraphrase of S117.txt:117-118) and the modified_id.csv listing (its Claim 5, whose cited range S117.txt:94-100 also carries the FAQ's own statement that each per-ecosystem copy keeps the row format without the `<ecosystem_dir>` prefix in the second column — the same fact Claim 4 pins here from S118.txt:114, so Claim 4 is a second-source pin of F59 ground, not new ground). This entry pins the Data sources page's sentences: the full zip's withdrawn inclusion, the per-record path, the [EMPTY]/ directory, the per-ecosystem prefix rule and the ecosystem-naming rules. It claims nothing about the top-level format or the sort order beyond Claim 4's context paraphrase.
- F58 / S116 (`corpus/knowledge/osv-high-quality-record-import-bar.md`) holds the import bar the Data Quality section links to (S118.txt:97-98); this entry claims nothing about the bar.
- F57 / S115 (`corpus/knowledge/osv-importfindings-record-quality-feedback.md`) holds the import-findings endpoint; F51 / S108 (`corpus/knowledge/osv-post-v1-query-contract.md`) the POST /v1/query contract. Neither covers the bucket layout.
- Literal sweep over the other 97 entries for the six pinned quotes: 0 files each (`.ufo/waves/round-84/controls/c2-prefreeze-r84.txt`).

## Not claimed

Not claimed: the list of current data sources and their licences (S118.txt:31-60); the converted-data pipelines (S118.txt:61-65); the covered-ecosystems list (S118.txt:66-96); the per-ecosystem zip beyond Claim 2's paraphrase (S118.txt:104); the top-level modified_id.csv location and reverse-chronological streaming advice, and its row format beyond Claim 4's context paraphrase of S118.txt:114 (S118.txt:109-119; F59 holds the FAQ statement of the same file); the ecosystems.txt listing (S118.txt:122); the contributing-data paragraph (S118.txt:124-126).

## Gate — S118 (OSV.dev Data sources)

- **URL:** https://google.github.io/osv.dev/data/ (HTTP 200; the manifest records the final URL equal to the requested URL).
- **Access date:** 2026-11-06. Capture `corpus/source-snapshots/round-84/S118.txt` (sha256 `e824a73545bedd0abae5f84cd120a5c73e482d7e935bc1534a08a1e1adfa5359`, 129 lines, 5820 snapshot bytes; the served page was 27419 raw bytes), `fetched_utc 2026-11-06T23:34:49Z`.
- **Six located quotes, one per claimed clause, each verbatim at its snapshot line, word counts by `len(quote.split())`:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| cl1 full zip includes withdrawn | Q01-allzip-withdrawn | S118.txt:102 | 17 | This bucket contains a zip file with all vulnerabilities across all ecosystems (including withdrawn records) at gs://osv-vulnerabilities/all.zip. |
| cl2 per-record path | Q02-record-path | S118.txt:104 | 8 | Individual vulnerability records can be found at gs://osv-vulnerabilities/<ECOSYSTEM>/<ID>.json. |
| cl3 [EMPTY]/ directory | Q03-empty-dir | S118.txt:104 | 13 | Vulnerabilities without an ecosystem (typically withdrawn ones) are exported to the gs://osv-vulnerabilities/[EMPTY]/ directory. |
| cl4 per-ecosystem csv prefix | Q04-per-ecosystem-csv-prefix | S118.txt:114 | 7 | The per-ecosystem files omit the <ecosystem_dir>/ prefix. |
| cl5 colon-suffixed folded | Q05-colon-prefix-dir | S118.txt:121 | 15 | the data dump will always contain an ecosystem directory without the :.* suffix (e.g. Alpine). |
| cl6 prefixed exports stopped | Q06-stopped-prefixed | S118.txt:123 | 12 | OSV.dev has stopped exporting entries for ecosystems with prefixes (e.g. All Alpine:.*). |

- **Recheck receipt:** the `recheck:` line above printed `S118:sha256 OK` and one `S118:<pin> OK occurrences=1 anchor=<n>-ok` line per pinned quote, exit 0 (`.ufo/waves/round-84/controls/c2-prefreeze-r84.txt`).

## Limits

The page does not establish, and this entry does not claim:

- the content of any object in the bucket: this entry read no GCS object, made no call to api.osv.dev and did not list `gs://osv-vulnerabilities`; the layout is the page's statement at the capture instant.
- when the prefixed exports stopped, or whether stale suffixed directories are deleted or only left unrefreshed; the page says only that exporting stopped (S118.txt:123). A round-84 scout seat's read-only probe of the public bucket found 30 colon-suffixed directories still served, with `Alpine:v3.17/all.zip` last modified 2024-10-09 against a current `Alpine/all.zip` (`.ufo/waves/round-84/w1/ScoutSource.md` §3.4); that observation is not a registered source and is recorded here only as a reason not to read Claim 6 as "the suffixed directories are gone".
- which records count as "typically withdrawn" in [EMPTY]/; the page gives no rule beyond the absence of an ecosystem (S118.txt:104).
- the current state of the page: the manifest records the fetch instant 2026-11-06T23:34:49Z.

Scope limit: six export-layout statements of the OSV.dev Data sources page only — the full zip's withdrawn inclusion (S118.txt:102), the per-record path and the [EMPTY]/ directory (S118.txt:104), the per-ecosystem modified_id.csv prefix rule (S118.txt:114), the folded colon-suffixed directories (S118.txt:121) and the stopped prefixed exports (S118.txt:123). Post-import record handling stays with F59 (S117), the import bar with F58 (S116).
