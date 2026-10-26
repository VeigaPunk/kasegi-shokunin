# ExecC2Capture — round-35 wave-1 receipt (C2 capture seat: S052)

Seat: ExecC2Capture (leaf, L1 = KasegiR35). Write scope used: `corpus/source-snapshots/round-35/S052.txt`,
`corpus/source-snapshots/round-35/manifest.json`, this receipt. No other lane file touched; no fleet repo,
sibling lane, `/home/vgpnk/Projects/bounties` or shokuknow write. No tool installed or upgraded (used the
`python3` and `curl` already on the host: Python 3.14.8, curl 8.23.0).

## Report

### 1. The dispatch URL is dead; the catalog's own JSON artifact is one path over

The ticket named `https://www.cisa.gov/known-exploited-vulnerabilities.json`. It is not served. Three user
agents, same result:

```
$ UA="kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"
$ curl -sS -o /dev/null -w "code=%{http_code} final=%{url_effective} size=%{size_download} ct=%{content_type}\n" -A "$UA" -L --max-time 60 https://www.cisa.gov/known-exploited-vulnerabilities.json
code=404 final=https://www.cisa.gov/known-exploited-vulnerabilities.json size=46916 ct=text/html; charset=utf-8
$ curl ... -A "Mozilla/5.0 (X11; Linux x86_64) ... Chrome/130.0 Safari/537.36" <same URL>
code=404 final=https://www.cisa.gov/known-exploited-vulnerabilities.json size=46916 ct=text/html; charset=utf-8
$ curl ... <same URL, curl default UA>
code=404 final=https://www.cisa.gov/known-exploited-vulnerabilities.json size=46916
```

A 46916-byte HTML error page, not JSON. The artifact is published under a different path, and the catalog page
names it itself:

```
$ curl -sS -A "$UA" -L "https://www.cisa.gov/known-exploited-vulnerabilities-catalog" -o catalog.html
$ grep -o 'href="[^"]*known_exploited_vulnerabilities[^"]*"' catalog.html
href="/sites/default/files/csv/known_exploited_vulnerabilities.csv"
href="/sites/default/files/feeds/known_exploited_vulnerabilities.json"
href="/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json"
```

Status of the two machine-readable candidates under the instrument UA:

```
code=200 final=https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json size=1807090 ct=application/json
code=200 final=https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv  size=1073722 ct=text/csv
```

**Commit decision (accepted by L1 in-channel at 06:35Z): S052 = the JSON feed.** The L1's interim steer was to
use the CSV because the named JSON path 404s; that steer's premise is false one path over, and the CSV is not
the narrower artifact it was assumed to be (§6). L1 reply: "Accepted: S052 = the JSON feed … No CSV recut
needed; discard the scratch CSV (do not commit it)."

### 2. Capture commands and fetch stats

The ticket's command form (`capture-source.py <url> --out …`) does not exist: `capture-source.py:main()` requires
`--id`, `--url` and `--out`, and defaults `--kind` to `html`. `--kind text` was chosen because `html_to_text()`
runs `SCRIPT_RE` tag-stripping and `html.unescape()` over the body, which for a JSON document would rewrite
`shortDescription`/`notes` strings if they carried markup or entities. Measured afterwards: a control capture
with the default `--kind html` produced byte-identical output for these bytes (`cmp` clean, same sha256), so the
capture is mode-independent here and `text` only removes the dependence. Both runs below wrote identical bytes:

```
$ python3 corpus/instruments/capture-source.py --id S052 \
    --url "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" \
    --out $S/S052.txt --kind text                      # scratch probe, 06:32:00Z
S052 status=200 fetched_bytes=1807090 snapshot_bytes=1479694 sha256=d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826 utc=2026-10-26T06:32:00Z out=$S/S052.txt
exit=0

$ python3 corpus/instruments/capture-source.py --id S052 \
    --url "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" \
    --out corpus/source-snapshots/round-35/S052.txt --kind text      # committed capture, 06:32:40Z
S052 status=200 fetched_bytes=1807090 snapshot_bytes=1479694 sha256=d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826 utc=2026-10-26T06:32:40Z out=corpus/source-snapshots/round-35/S052.txt
exit=0

$ wc -l -c corpus/source-snapshots/round-35/S052.txt
  27870 1479694 corpus/source-snapshots/round-35/S052.txt
```

Two fetches 40 s apart produced the same sha256, so the capture is reproducible at the pinned content (not a
claim that the feed cannot change later). Final URL:

```
instrument-UA effective_url: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
identical_to_requested: True
status: 200 content_type: application/json content_length_header: None
```

No redirect: `urllib`'s effective URL equals the requested URL, so the manifest `url` is both request and final
URL. Fetch instant `2026-10-26T06:32:40Z` (instrument `strftime("%Y-%m-%dT%H:%M:%SZ")`, strict UTC), matching
the ticket's `opened 2026-10-26`. Size is 1479694 bytes (1.41 MiB), above 1 MiB and far below the 10 MiB ceiling;
it is committed in full as required.

### 3. Snapshot shape verification (the "is this the catalog JSON" check)

```
$ python3 - <<'PY'   # json.loads over the committed snapshot + field census over its lines
parse: keys= ['title', 'catalogVersion', 'dateReleased', 'count', 'vulnerabilities']
       count_field= 1756 len(vulnerabilities)= 1756
first cveID: CVE-2026-114625 last cveID: CVE-2020-29583
field-name census:
   1756 cveID / vendorProject / product / vulnerabilityName / dateAdded / shortDescription /
        requiredAction / dueDate / knownRansomwareCampaignUse / forensicTriage / notes / cwes
      1 title / catalogVersion / dateReleased / count / vulnerabilities
```

`catalogVersion` = `2026.10.23`, `dateReleased` = `2026-10-23T19:30:18.9209Z`, `count` = 1756 and the parsed
array length equals it. The snapshot remains valid JSON after `collapse()` (per-line whitespace collapse, no
blank lines), which is why `--kind text` is safe here.

Severity/CVSS token scan over the whole capture (the distinctness evidence — a capture cannot quote an absence,
so this is measured):

```
cvss         count=0 lines=[]
base score   count=0 lines=[]
risk rating  count=0 lines=[]
score        count=1 lines=[23592]      # prose inside a shortDescription
severity     count=2 lines=[5135, 11629]  # URL slugs inside notes strings
```

**Exact wording constraint for anything that reads this receipt:** "the record schema carries no severity
field" is true (12 per-record keys, none of them a score); "the capture contains no severity token" is false.
`severity` occurs twice and `score` once, all inside string values.

### 4. Manifest

`corpus/source-snapshots/round-35/manifest.json`, schema_version 1, one source record, shape matching round-34's
(`id`, `path`, `sha256`, `url`, `fetched_utc`, `quotes`) so QUALITY R20/R21 hold: the `url` is the feed URL the
registry row must carry byte-for-byte, and `fetched_utc` records the fetch instant. Five assertions, all
`occurrences=1`, all ≤25 words, each carrying a verified anchor line:

| id | anchor | words | lines | subject |
|---|---|---|---|---|
| Q1 | 2 | 7 | L2 | the feed's own title, `CISA Catalog of Known Exploited Vulnerabilities` |
| Q2 | 3 | 2 | L3 | `catalogVersion` 2026.10.23 |
| Q3 | 4 | 4 | L4-L5 | `dateReleased` + `count` 1756 (wraps a line break; normalized) |
| Q4 | 15472 | 8 | L15472-L15475 (record cveID L15465 = CVE-2022-29499) | per-record exploitation-status fields: dueDate, `knownRansomwareCampaignUse": "Known"`, forensicTriage, NVD notes URL |
| Q5 | 19165 | 19 | L19165-L19168 (record cveID L19161 = CVE-2019-12989) | the remediation clock on one record: dateAdded 2022-03-25 → dueDate 2022-04-15 with requiredAction |

Q1/Q2 are literal single-line quotes; Q3-Q5 span line breaks and are asserted under the instrument's declared
normalization (`normalized=markup-whitespace`), the same route round-34's S051 manifest used. Uniqueness of Q4
rides on its `notes` URL; of Q5 on the shortDescription sentence plus the date pair. The manifest's `purpose`
records the 404 measurement, the `--kind text` reason, the 1.41 MiB size, the two-fetch determinism, the
CSV comparison and the absence of a prose definition of "known exploited" in the feed.

### 5. Self-check

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
exit=0
```

Every assertion reports `occurrences=1`, the sha256 matches, and the run exits 0. Digests:

```
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt   (1479694 bytes, 27870 lines)
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json (5631 bytes)
```

### 6. CSV comparison — measured, then discarded (not committed)

```
$ python3 corpus/instruments/capture-source.py --id S052CSV \
    --url "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv" \
    --out $S/S052CSV.txt --kind text
S052CSV status=200 fetched_bytes=1073722 snapshot_bytes=1073433 sha256=f0bff4f7c748b0eb38c1ab8825e63a37208fa691a51891abed0525e0132f9c8a utc=2026-10-26T06:34:16Z
exit=0
$ wc -l -c $S/S052CSV.txt
   1757 1073433
header: cveID,vendorProject,product,vulnerabilityName,dateAdded,shortDescription,requiredAction,dueDate,knownRansomwareCampaignUse,forensicTriage,notes,cwes
```

Two corrections this measurement supports, both already sent to the L1 and the S052 row author: the CSV header
carries **twelve** field names, not the nine the steer assumed, so the CSV is not a narrower artifact; and both
artifacts hold the same 1756 records, while only the JSON carries title/catalogVersion/dateReleased/count. The
scratch CSV was deleted with the rest of the scratch tree (§8); nothing CSV-shaped is committed.

### 7. Findings, risks and handoff constraints

1. **Dispatch URL defect (fixed by choice of artifact, not by edit).** The URL in the round-35 dispatch text,
   and in any row drafted from it, 404s for three user agents. The committed manifest `url` is
   `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`; the S052 registry row
   must carry exactly that string or QUALITY R20's url↔row match fails. Sent to `ExecRegistryAppend-3` and
   `ScribeEntryF18`; L1 confirmed the choice.
2. **No prose definition in the feed.** The catalog JSON's only descriptive text is its title (Q1). A knowledge
   entry that states what "known exploited" means cannot cite S052 for that sentence — it must attribute it to
   the catalog page, or state it as field semantics with Q4 as evidence. Flagged to `ScribeEntryF18`.
3. **Absence is measured, not quoted.** F18's distinctness from CVSS rests on the schema having no severity
   field (`cvss` 0, `base score` 0, `risk rating` 0 over 12 keys × 1756 records). Any wording claiming zero
   `severity`/`score` tokens in the capture would be false (2 and 1 prose occurrences).
4. **Live-document risk (declared in the manifest).** The snapshot pins bytes at catalogVersion 2026.10.23 /
   count 1756. A later fetch will differ by design; `source-recheck.py` is a local byte check and does not
   assert upstream freshness.
5. **Quote fragility if the capture is ever re-cut.** Q4's uniqueness depends on a `notes` URL and Q5's on one
   record's text; both were re-measured against the committed bytes (`occurrences=1`) after the file landed, so
   they are correct for this digest and must be re-measured if the capture changes.
6. **Size.** 1.41 MiB committed as the capture, above the 1 MiB mark the ticket asked to report and well under
   the 10 MiB ceiling.
7. **Not mine to run.** I did not run the round's census, harness, digest or SCORECARD checks; the L1 owns
   post-integration gates. The only instrument runs here are the capture and `source-recheck --source S052`.

### 8. Scratch

All work under `/fast/scratch/hyaku/kasegi-r35/ExecC2Capture/` (`kev.json`, probe `S052.txt`, `S052-html.txt`,
`S052CSV.txt`, `catalog.html`, `evidence.txt`, `capture.log`, `htmlmode.log`) was removed at the end of this
seat's run; `test -e` on the directory reports it gone (`scratch removed`).

### 9. Cross-seat reconciliation (ScribeSOURCESRow-2, ScribeEntryF18, ExecRegistryAppend-3)

Two independent instrument runs by other seats produced the same bytes as this capture, so the digest is not
seat-local: `ScribeSOURCESRow-2` reports sha256 `d69349e8…9e8826`, snapshot 1479694, 27870 lines at 06:33:07Z;
this seat's committed run fetched at 06:32:40Z with the same values. Their four numeric claims were re-measured
here against the committed capture and agree, with one refinement:

```
records 1756
BOD 26-04 in requiredAction: 139 records
BOD 22-01 in requiredAction: 340 records   (0 in notes)   [the row draft said 341]
literal 'BOD 26-04' occurrences in the file: 557 (139 records repeat it)
literal 'BOD 22-01' occurrences in the file: 340
distinct requiredAction values: 46, most frequent value repeats 893 times
knownRansomwareCampaignUse 'Unknown': 1395
dateAdded '2026-10-23': 2 records      dueDate '2026-10-26': 2 records
```

So the current requiredAction cites BOD 26-04 (139 records) and the older BOD 22-01 text survives on 340
records, not 341; the record count is 1756. Any manifest or entry sentence repeating "BOD 22-01" verbatim as a
quote is non-unique (340 occurrences) and would break the frozen `occurrences=1` clause — the committed manifest
carries no such quote. The two `dateAdded`/`dueDate` values on today's release date are each duplicated, which
is why the clock assertion (Q5) is a whole-record span instead of a bare date line.

