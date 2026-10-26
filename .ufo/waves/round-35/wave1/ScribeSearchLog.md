# ScribeSearchLog — round-35 CISA KEV sweep (landed search-log bullet audit + measured delta, S052)

Seat: `ScribeSearchLog` (leaf, L2 wave). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Axes touched: `coverage` (C2's `where: …; date: …; identified/screened/included/excluded; stop`
ground) and `depth:verifiability` (every number below is a command output in § Report).
Assigns no verdict; the L1 integrates.

The target surface landed from another round-35 seat while this seat was measuring (§5): the S052 row
at `corpus/SOURCES.md:58` and a CISA sweep bullet at `:79`. This receipt therefore audits that landed
line, supplies the four measured facts it lacks (§5 items 1–4), records one defect in it (§5a), and
gives both sets of anchor coordinates with their digests (§6). It writes no file under `corpus/`.

## 1. Question this sweep answers

The frozen claim C2 admits F18 as "CISA Known Exploited Vulnerabilities catalog —
exploitation-status-based prioritization distinct from CVSS severity". The search log therefore has
to answer, before inclusion: *does the lane already hold a source that ranks or queues
vulnerabilities by exploitation status rather than by a severity score?* Answer measured at §4:
**no** — the lane's severity ground is S001/S015/S043–S047/S051, and its only exploitation-adjacent
strings are incidental quotations.

## 2. Surfaces measured (all 2026-10-26, `User-Agent: kasegi-shokunin/1.0`)

| # | surface | HTTP | bytes | lines | sha256 |
|---|---|---|---|---|---|
| 1 | `https://www.cisa.gov/known-exploited-vulnerabilities-catalog` (index) | 200 | 284330 | 3544 | `75a7af09177a570d283accd7eb9c5afc4f8f16c4a1447c5af3d003751f08aaa1` |
| 2 | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` (feed, **captured**) | 200 | 1807090 | 27869 | `97a6e54bc74c651ab3c55657191db9adec6c63b05ca54e4205327cfd97a8fb70` |
| 3 | `https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv` | 200 | 1073722 | 1757 | `cb77ba6ee61c8fa963d2eb16dda2cd4746c5b11e0353f079d3e0e569eb5d2778` |
| 4 | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json` | 200 | 3623 | 102 | `0d5865c98694c5bfba2c78a26caf814f406b3fce8bfb81bef79e99c7f288b0e7` |
| 5 | `https://www.cisa.gov/known-exploited-vulnerabilities.json` (conventional root path) | **404** | 46916 | 1450 | `6ac5c3172f19e90c70cb782e503eeb28af5d5586664a1bfc802d1b39285a1e66` |
| 6 | `https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities` | 200 | 87312 | 1868 | `cd842541aeba7e82f987c92a049ce6236f606e74b454d97bfd6a9a4a743235c4` |
| 7 | `https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk` | 200 | 84350 | 1930 | `678921ff952f4f8d813bbcbd3fc6e9fed5b06c390d0a5ff43083f07f2a98d1cd` |

Row 5 is the 404 the L1 steered in twice: its body is a `Page Not Found | CISA` HTML error page
(46,916 bytes), not a feed. Rows 1, 3, 4 are the three distributions the index page itself advertises
(`grep -oiE 'href="[^"]*known_exploited[^"]*"'` → exactly the CSV, the feed JSON and the schema).

## 3. Capture of record reconciles with the live feed

`corpus/source-snapshots/round-35/S052.txt` (sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`,
1,479,694 bytes, 27,870 lines) is the **feed**, not the CSV: the manifest
(`corpus/source-snapshots/round-35/manifest.json`, sha256 `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`)
binds it to `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`,
`fetched_utc` `2026-10-26T06:32:40Z`, `fetched_bytes=1807090`, `snapshot_bytes=1479694`, `--kind text`
(chosen so the instrument's `html_to_text()`/`html.unescape()` does not rewrite entity sequences
inside `shortDescription` and `notes`).

Cross-checked against this seat's own fetch (§2 row 2), record for record:

- top-level `title`, `catalogVersion` (`2026.10.23`), `dateReleased` (`2026-10-23T19:30:18.9209Z`) and
  `count` (`1756`) identical; `len(vulnerabilities)=1756` on both sides.
- cveID multiset identical: `diff -q` of the two sorted lists exits **0**, 1,756 ids on each side.
- 239 of 1,756 records differ, in 240 string fields, and **every one of those differences is
  whitespace-only** (`a.split()==b.split()` holds for each pair). That is the `--kind text` collapse()
  at work, not a content delta — and it is why the search log may not claim byte-identity with a live
  re-fetch, only object identity.
- the CSV reconciles the same object: 1,756 data rows, and its 12-column header equals the feed's 12
  record fields as a set (`diff -q` of sorted lists exits **0**). CSV header order: `cveID,
  vendorProject, product, vulnerabilityName, dateAdded, shortDescription, requiredAction, dueDate,
  knownRansomwareCampaignUse, forensicTriage, notes, cwes`.

## 4. Negative sweep (PRE-STATE)

Scope command: `grep -rIl --include=*.md -F "$t" "$L/corpus" "$L/SKILL.md"` over every markdown file
under `corpus/` plus `SKILL.md` — **105 files**; the domain subset cited in the bullet is **99**:
`corpus/*.md` 3, `corpus/knowledge/*.md` 46, `corpus/lessons/*.md` 49, `SKILL.md` 1. The 6 files
outside that subset are instrument fixtures and generated census pages
(`corpus/instruments/{README.md,citation-survival.md}`, `corpus/instruments/limb-fixtures/**` 3,
`corpus/instruments/r35-fixtures/README.md`); no term hits there, so both denominators give the same
counts.

PRE-STATE pinned by measurement: registry rows **51**, knowledge entries **46**, frontier admitted
**17** — this round's S052 row and F18 entry had not landed at 06:36Z (§ Report `registry_rows=51`,
`entries=46`, `grep -nE '^\| *S052 *\|'` empty).

| term | files | hits | where |
|---|---|---|---|
| `KEV` | 1 | 1 | `corpus/lessons/round-22.md:91` — quoted CWE Top 25 cell "CVEs in KEV: 7" for S015 |
| `known exploited` | 0 | 0 | — |
| `CISA` | 4 | 14 | `knowledge/authorization-safe-harbor-and-scope.md:24,38`; `knowledge/coordinated-disclosure-timelines.md:34`; `lessons/round-22.md`; `SOURCES.md` — VDP template S008, CVD program S003, CRA duty, registry cells. **14 is the case-sensitive `-F CISA` count; case-insensitive `-i` gives 44 over the same 4 files** because every `https://www.cisa.gov/…` URL matches too |
| `exploited vulnerabilities` | 1 | 1 | `corpus/knowledge/cra-manufacturer-reporting-duties.md:10` — "actively exploited vulnerabilities and severe incidents …", a CRA reporting duty, not a prioritized catalog |
| `BOD 22-01` | 0 | 0 | — |
| `EPSS` | 0 | 0 | — |
| `exploit maturity` | 0 | 0 | — |
| `exploitation status` | 0 | 0 | — |
| `prioritiz` | 2 | 2 | `corpus/README.md:206` (F05 "methodology-specific prioritization"); `corpus/SOURCES.md:61` (CVSS→CWE path line) |

No hit is a source that prioritizes by exploitation. The lane's nearest neighbours are severity
ground (S001, S015, S043–S047, S051), which the question explicitly excludes.

### 4b. Capture bytes (non-markdown) — the sweep's blind side, measured

My §4 command is `--include=*.md`, so it never looks inside `corpus/source-snapshots/**/*.txt`. A
`KEV` grep over the captures finds tokens in six round-24 captures, in a manifest, and in this round's
own `S052.txt`; **none of the round-24 captures is the catalog** — each is another source's page that
names it:

| capture | registry source (round-24 manifest `url`) | `KEV` hits | what it is |
|---|---|---|---|
| `round-24/S015.txt` | CWE Top 25 2025 list | 27 | site nav "Top 10 KEV Weaknesses" (`:28`) **plus the table's own "CVEs in KEV" column** — header `:60`, and `:214` is the `CVEs in KEV: 7` cell the round-22 lesson quotes under S015 |
| `round-24/S008.txt` | CISA VDP template | 2 | site nav item "KEV Catalog" (`:10`, `:67`) |
| `round-24/S001.txt` | FIRST CVSS v4.0 user guide | 1 | "such as the ISAC's …, CISA KEV or private …" (`:1082`) |
| `round-24/S009.txt` | UK NCSC AI-finding questions | 1 | `:122`: "The CISA KEV says only about 400 new vulnerabilities were tracked as exploited, and only around 40 of those were zero-days when initially exploited. This is why prioritised patching is so important." |
| `round-24/S013.txt` | CWE Top 25 2025 methodology | 1 | site nav "Top 10 KEV Weaknesses" (`:28`) |
| `round-24/S014.txt` | CWE Top 25 2025 key insights | 1 | site nav "Top 10 KEV Weaknesses" (`:28`) |
| `round-24/manifest.json` | — | 1 | the manifest text |
| `round-35/S052.txt` | this row | 3 | the catalog's own title/description |

Token accounting measured: **33 in the six round-24 captures + 1 in `round-24/manifest.json` + 1 in
`corpus/lessons/round-22.md:91` = 35 pre-existing**, plus **3 in this round's `S052.txt`** (the
catalog's own title/description). After the F18 landing the markdown side adds up to 23
(`cisa-kev-catalog.md` 11, `SOURCES.md` 8, `README.md` 3, `round-22.md` 1), which is a different
denominator from the one below and must not be mixed with it.

So the honest statement is **source-level, not string-level**: the lane held no *catalog* before this
round, but it held *sentences about* the KEV catalog inside other sources' pages. `S009.txt:122` is the
one that matters — it reports secondary figures (≈400 exploited in 2025, ≈40 zero-days) that must be
read as a quotation inside the NCSC page, never as catalog ground; the catalog's own `count` is 1,756
records and it carries no such aggregate. A reader who repeats "KEV 0" without this table would
overstate the negative result.

**Consequence for the landed bullet's scope correction (F-11).** The landed bullet's PRE-STATE sweep is
scoped to `corpus/knowledge/*.md`, `README.md`, `SOURCES.md` and `SKILL.md`, and the R8 correction at
`:112` names only the omitted `corpus/lessons/` tree. It does not name `corpus/source-snapshots/`,
which holds **33 of the 35** pre-existing tokens and the only substantive sentence (`S009.txt:122`).
So "0 hits" is scope-true and whole-corpus false, and an erratum that names one omitted tree while
leaving the larger one unnamed is still partial. The registry-level gap the same measurement proves is
the one S052 closes: at base `3266c993` the registry held no KEV row (and no `BOD 22-01`/`BOD 26-04`
row), while the lane's *captures* quoted KEV from NCSC/CISA/CWE pages.

**Post-measurement state change (06:39Z).** While this receipt was being written another round-35 seat
landed the S052 row and its own CISA sweep bullet, so `corpus/SOURCES.md` is now
`510e3bba…` / 110 lines (`S052` row at `:58`, R8 lines `:108`–`:110`, its CISA bullet at `:79`). The
counts above remain the state they were measured at (`4c85ff86…`, registry 51, entries 46); §5 audits
the landed bullet against them. Its sweep scope is narrower than mine (knowledge, README, SOURCES,
SKILL — no `corpus/lessons/**`), which is why it reports `KEV 0` where I report `KEV 1 file/1 hit`
(the one hit is `corpus/lessons/round-22.md:91`); both are true of their stated scopes, and the landed
line states its scope. At the final state the markdown counts are higher again because the F18 entry
and its README row landed: `KEV` now appears in `corpus/knowledge/cisa-kev-catalog.md` (11),
`corpus/SOURCES.md` (8), `corpus/README.md` (3) and `corpus/lessons/round-22.md` (1) — i.e. the
PRE-STATE table is a timestamp, not a property of the lane.

## 5. The bullet, and what this sweep adds to the one already landed

**No append is pending.** When this seat started, `## Search log` ended at the round-34 Immunefi
bullet (line 77 of `4c85ff86…`); by 06:39Z another round-35 seat had appended both the `S052` row and
its own CISA bullet, now `corpus/SOURCES.md:79` under digest `510e3bba…`. This seat wrote no corpus
file and appends nothing. What follows is (a) the audit of the landed line against my measurements,
(b) the draft below, kept because it supplies four facts the landed line lacks, and (c) one defect in
the landed line.

Landed line at `:79`, 2,387 characters / 2,393 bytes (its own digest, line plus newline, is
`f2ab0a647031489dd96f5e5fe35b20318ebae7ed9bd8cdcb6fbc51e8ff42ab54` — which is what `:111` cites, and
that citation resolves): it names the question, the catalog page, the JSON
feed and its capture flags/digests, the eight-term sweep with its scope and PRE-STATE counts, `date:
2026-10-26`, `identified 5, screened 5, included 1, excluded 4` with per-item exclusion reasons, and a
`Stop:` rationale. Independently corroborated by me: the 404 on the guessed path (two of my fetches,
46,916 bytes, `Page Not Found | CISA`), the feed's capture flags (`fetched_bytes 1807090`,
`1479694` snapshot bytes, `27870` lines), and `requested URL == effective URL, no redirect`
(my `curl -w 'num_redirects=%{num_redirects}'` → `num_redirects=0 http=200 size=1807090`).

Four facts it does not carry, all measured here (§3, §8):

1. the CSV is the same object **record for record** — `diff -q` of the 1,756 sorted `cveID`s exits 0,
   and the CSV's 12 columns equal the feed's 12 record fields (`diff -q` exit 0). The landed line
   asserts "the same records in another serialization" without that check; the check is what makes the
   exclusion safe rather than plausible.
2. the feed carries **no severity field** (`CVSS` 0 occurrences; `severity` in 2 of 1,756 record
   texts) — the measurement that grounds F18's "distinct from CVSS severity" distinction.
3. **BOD 22-01 is revoked** and superseded by BOD 26-04 (both directive pages read: title
   `… (Revoked)`, body "This Directive has been revoked. It is superseded by BOD 26-04."), while the
   feed still prints `BOD 22-01` in **340** records and `BOD 26-04` in **139**. The landed line lists
   both directives only as sweep terms.
4. a re-fetch is **object-identical, not byte-identical**: same `catalogVersion`, same 1,756 `cveID`s,
   239 records differing in **whitespace only** (240 string fields, each `a.split()==b.split()`).
   Without this, a verifier hashing a fresh fetch against `S052.txt` will read a false alarm.

### 5a. Defect in the landed line (D-R35-SL-1): digest abbreviation

`:79` prints `sha256 d69349e8…77e8826`. The captured file's digest is
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, whose last eight characters are
`779e8826`; the substring `77e8826` does not occur anywhere in it (`python3: '77e8826' in d` →
`False`), so the printed suffix dropped the `9` — the abbreviation should read at least
`d69349e8…779e8826` (or the full digest). The manifest, the row cell (`:58`) and §2/§3 above carry
the correct value, so the search-log copy is the outlier. Route: whoever owns `corpus/SOURCES.md` this
round (a `corpus/` write; this seat is read-only there). **Still present at the final state
measured** (`corpus/SOURCES.md` sha256 `0f95a132…`, 112 lines): probes `'77e8826'`=1, `'779e8826'`=0.

### 5b. The draft, kept for the four deltas above (not for appending as-is)

One line, 4,460 characters, exactly one `|` (inside the quoted 404 title `Page Not Found | CISA`);
safe in a bullet list, but an owner reflowing it into a table must drop or escape that pipe.

```
- CISA Known Exploited Vulnerabilities sweep (round 35); question: does the lane already hold a known-exploited-vulnerabilities prioritization source — one that ranks or queues vulnerabilities by exploitation status rather than by a severity score — and does CISA's own catalog add that ground beyond the severity ground the registry already holds (S001, S015, S043–S047, S051); where: CISA's own KEV surfaces — the catalog page https://www.cisa.gov/known-exploited-vulnerabilities-catalog (status 200, 284330 bytes, 3544 lines, sha256 75a7af09…08aaa1; prints "Showing 1 to 20 of 1756 results" and links the CSV, the JSON feed and a schema), the machine-readable JSON feed https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json captured under the instrument UA into corpus/source-snapshots/round-35/S052.txt (fetched 2026-10-26T06:32:40Z, status 200 served directly, 1807090 served bytes collapsing to 1479694 snapshot bytes, 27870 lines, sha256 d69349e8…9e8826, catalogVersion 2026.10.23, dateReleased 2026-10-23T19:30:18.9209Z, count 1756), the CSV distribution https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv (status 200, 1073722 bytes, 1757 lines = header + 1756 data rows, sha256 cb77ba6e…5d2778), the JSON Schema https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json (status 200, 3623 bytes, 102 lines, sha256 0d5865c9…88b0e7), the conventional root path https://www.cisa.gov/known-exploited-vulnerabilities.json (HTTP 404, "Page Not Found | CISA", 46916-byte HTML error page), and the two directives that govern it: https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities (status 200, 87312 bytes; title "… (Revoked)", body "This Directive has been revoked. It is superseded by BOD 26-04.") and https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk (status 200, 84350 bytes; "supersedes and hereby revokes … BOD 22-01 … (Nov. 3, 2021)"); plus a nine-term negative sweep (KEV, "known exploited", CISA, "exploited vulnerabilities", "BOD 22-01", EPSS, "exploit maturity", "exploitation status", prioritiz) over every markdown file under corpus/ plus SKILL.md (105 files; the 99 domain files are corpus/*.md 3, corpus/knowledge/*.md 46, corpus/lessons/*.md 49 and SKILL.md, and every hit lies in them), at PRE-STATE: registry 51 rows, 46 knowledge entries before this round's S052 row and F18 entry; date: 2026-10-26; identified 7 candidate URL surfaces, screened 7, included 3 surfaces for 1 registry object — S052 is the JSON feed, the catalog page serves as its index and the CSV reconciles it record for record (1756 cveIDs identical as a multiset; the CSV's 12 columns are exactly the feed's 12 record fields) — excluded 4: the root .json path does not exist (404), BOD 22-01 is revoked and superseded by BOD 26-04, BOD 26-04 is a federal remediation directive with no vulnerability rows, and the schema carries field definitions only. The negative sweep found no prior lane source for exploitation-status prioritization: KEV 1 file/1 hit and "exploited vulnerabilities" 1 file/1 hit are incidental — the quoted CWE Top 25 cell "CVEs in KEV: 7" under S015 (corpus/lessons/round-22.md:91) and the CRA reporting-duty phrase "actively exploited vulnerabilities …" (corpus/knowledge/cra-manufacturer-reporting-duties.md:10); "known exploited" and "BOD 22-01" 0; CISA 4 files/14 hits are the VDP-template, CVD-timeline and CRA uses (S003, S008, S023); EPSS, "exploit maturity" and "exploitation status" 0; "prioritiz" 2 files/2 hits are F05's "methodology-specific prioritization" wording (corpus/README.md:206) and the CVSS-to-CWE path line (corpus/SOURCES.md:61). The feed carries no severity or CVSS field at all (0 occurrences of "CVSS"; "severity" in 2 of 1,756 record texts) — only exploitation-status fields: dateAdded 2021-11-03 to 2026-10-23, 513 distinct dueDate values, knownRansomwareCampaignUse Known on 361 records and forensicTriage Yes on 91 — and it still prints "BOD 22-01" in 340 records while 139 name BOD 26-04, so a row registered against it must not present the revoked directive as current policy. The two advertised distributions, the schema and the governing directive were all opened and the catalog reconciles with its CSV, so one object answers the bounded question and the sweep stopped without widening into EPSS or NIST surfaces.
```

Row-shape notes for the registry owner (measured, not prescriptive beyond the L1 correction):

- **URL cell byte-exact**: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
  — the string the manifest's `sources[0].url` carries. Any other KEV string (the index page, the CSV,
  the 404 root) makes the row disagree with the capture of record.
- **kind `dataset`** (L1 correction, 2026-10-26); the `sources-census.sh` enum at
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:655` accepts
  `spec|docs|paper|code|tool|dataset|talk|book|community|own-work`.
- **recheck**: the feed versions itself (`catalogVersion 2026.10.23`), so `on-release` is the cadence
  that leaves a comparable value behind; `S045` (a maintained JSON dataset) uses a day window instead.
  Owner's call, stated here so the choice is deliberate.

## 6. Anchor coordinates, both measured (R6: never quote a line without its digest)

| anchor | after the round-34 freeze, `4c85ff86…` (this seat, 06:36Z) | with round 35 landed, `510e3bba…`, 110 lines (06:39Z) |
|---|---|---|
| last registry row | 57 (`S051`) | 58 (`S052`) |
| `## Paths` | 59 | 60 |
| `## Search log` | 66 | 67 |
| last search-log bullet | 77 (round-34 Immunefi, 2,657 chars incl. newline) | 79 (round-35 CISA, 2,387 chars) |
| `## Leads (unopened)` | 79 | 81 |
| `## Registry changes` | 85 | 87 |

The +2 on `Leads`/`Registry changes` against +1 on `Paths`/`Search log` is the second appended line
between the last bullet and `## Leads` — i.e. the new bullet itself, inserted after the round-34 one.
Both rows are measurements (`grep -n '^## ' corpus/SOURCES.md` + `wc -l` at each digest); no inference
is needed and none is offered. `## Registry changes` at `:87` holds **21** bullet lines (`awk 'NR>87 &&
/^- /'`), `:108`–`:110` being this round's three (`S052 row added`, `S052 cells not edited`, `No
status/recheck/used-by cell changed`), matching the round-33 precedent of three R8 lines per row
(`corpus/lessons/round-33.md:79`).

The file moved again after this table was measured: `0f95a132…`, **112 lines**, with two more R8
lines at `:111`-`:112` appended *after* `## Registry changes`, so every heading coordinate in this
table still holds (re-verified: `Paths` 60, `Search log` 67, `Leads` 81, `Registry changes` 87). What
changed is only what `:111`-`:112` say — see R-14/F-10.

Consequence for citations: the stale `SOURCES.md:83` trail (`corpus/lessons/round-29.md:214`,
`corpus/lessons/round-29-verifier-spotcheck.md:74`) has deepened by the same two lines since round 34
recorded +9; it remains a `corpus/lessons/**` repair, not this seat's work. I measured the heading
positions, not which line the `:83` citation originally meant, so I state the shift rather than a new
offset.

## 7. Decision record (both L1 steers, verbatim)

1. `KasegiR35`, first steer, 2026-10-26T~06:32Z: "the KEV JSON endpoint
   https://www.cisa.gov/known-exploited-vulnerabilities.json returns HTTP 404 (measured 2026-10-26),
   so the official CSV distribution https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv
   is the primary data source (kind dataset, row S052). Search log should name both endpoints and the
   choice."
2. `KasegiR35`, correction, 2026-10-26T~06:34Z: "the JSON feed that works is
   https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json (200,
   application/json, catalogVersion 2026.10.23, count 1756); the root .json URL 404s (record both).
   S052 row URL must be byte-exact https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json.
   Search-log bullet: where searched = CISA KEV catalog page, JSON feed, CSV distribution, root .json
   (404); kind dataset; date 2026-10-26."

Both the landed row (`:58`) and the landed bullet (`:79`) follow steer 2: the URL cell and the
manifest carry the byte-exact feed URL. Steer 1's CSV-as-primary clause is superseded — the capture of
record (`S052.txt`, manifest `url`/`sha256`/`fetched_bytes`) is the JSON feed, so a CSV URL on the row
would have disagreed with the manifest. The CSV is still named in the landed bullet and this receipt
reconciles it record for record (§3), which is what steer 1's "name both endpoints" asked of the log.
This seat measured both rather than accepting either steer on assertion: rows 2/3/5 of §2 are its own
fetches.

**Routing note (coordination, not a finding about the corpus).** My first message went to
`agent://ScribeSOURCESRow`, which is the round-34 instance: it replied that it is closed at round 34,
that it wrote nothing at round 35, and that `.ufo/waves/round-35/wave1/swarm-registry.json` still shows
`agentId: null` for all round-35 members. The roster visible to this seat carries
`ScribeSOURCESRow-2` and `ExecRegistryAppend-3`, which is where the three pins were also sent; the
round-34 seat then re-measured and confirmed the `510e3bba…` / 110-line state and its own `:58`/`:79`
coordinates. Its first coordinate set (`## Registry changes` `:101`, 105 lines) did not match any state
I measured; its correction matched `510e3bba…` exactly, and that correction is what §6 now carries.

## 8. Findings for the L1 (not verdicts)

- **F-1 (material, for the entry, not for the row): BOD 22-01 is revoked.** Its page title reads
  "BOD 22-01: … (Revoked)", carries an "Archived Content" banner, and states "This Directive has been
  revoked. It is superseded by BOD 26-04." BOD 26-04 states it "supersedes and hereby revokes … BOD
  22-01 … (Nov. 3, 2021)". The feed still prints `BOD 22-01` in **340** records and `BOD 26-04` in
  **139**; newer rows (`CVE-2026-114625`, `dateAdded 2026-10-23`) instruct "BOD 26-04". Any entry
  sentence that renders "BOD 22-01" as the current rule is wrong; the KEV catalog's own status is the
  BOD 26-04 regime. I did not read BOD 26-04's operative text beyond its supersession clause and its
  KEV paragraph — that is the limit of this seat.
- **F-2 (supports the F18 distinction): the feed carries no severity field.** `CVSS` occurs **0**
  times in the whole 1,756-record capture; the string `severity` appears in **2** record texts. The
  record fields are `cveID, vendorProject, product, vulnerabilityName, dateAdded, shortDescription,
  requiredAction, dueDate, knownRansomwareCampaignUse, forensicTriage, notes, cwes`. So
  "exploitation-status-based prioritization, distinct from a severity ladder" is a property of the
  object, not an interpretation of it.
- **F-3 (currency, for the lesson's limits): a re-fetch is object-identical, not byte-identical.**
  Same `catalogVersion`/`count`/cveID set at 06:35Z, 239 records differing only in whitespace, because
  the capture is `--kind text`. A verifier comparing sha256 against a fresh fetch will see a mismatch
  that means nothing; compare `catalogVersion` + the cveID multiset instead.
- **F-4 (index/CSV not separable sources):** the index page is a 1,756-row listing wrapper ("Showing
  1 to 20 of 1756 results") and the CSV is the same rows in 12 columns; neither adds a second object.
  Registering more than one row for this catalog would be row inflation.
- **F-5 (route hygiene):** `https://www.cisa.gov/known-exploited-vulnerabilities.json` is the shape a
  reader guesses first and it 404s. That belongs in the bullet (it does) so the next round does not
  guess it again.
- **F-6 (defect, landed line): the search-log digest abbreviation is wrong.** `corpus/SOURCES.md:79`
  prints `d69349e8…77e8826`, a suffix that does not occur in
  `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` while the manifest and the row
  cell (`:58`) carry the correct one. Detail and route in §5a. This seat cannot repair it (no
  `corpus/` write scope).
- **F-7 (for the entry): the revocation is not in the search log.** The landed bullet names `BOD
  22-01` and `BOD 26-04` only as negative-sweep terms; the measured fact that 22-01 is revoked (and
  that 340 catalog records still say 22-01 while 139 say 26-04) lives in this receipt's F-1 and §5.
  If the F18 entry asserts the catalog's policy basis, it must take F-1, not the older directive name.
- **F-8 (surface accounting differs):** the landed line counts `identified 5` (feed, 404 path, index,
  CSV, schema); I measured seven opened 200/404 surfaces because I also read BOD 22-01 and BOD 26-04.
  The landed 5 is defensible if the directives are treated as background rather than candidate
  sources — but then the bullet should say so, because it cites their content (`BOD 22-01` 0 files,
  `BOD 26-04` 0 files) as sweep results while the pages themselves return 200.
- **F-9 (cross-reference with `ScribeSOURCESRow-2` F8/V11, checked here):** the same seat filed two
  further defects on the landed text; I re-measured both rather than endorsing them.
  (a) **Confirmed** — `:79` says `CISA 2 knowledge files and 7 SOURCES rows`. Registry rows whose
  source cell contains `CISA` are **6** now (`S003, S008, S021, S023, S026, S052`) and **5** at base
  `3266c993` (S052 being this round's), so `7` matches no state; the two knowledge files and
  `exploited vulnerabilities 1` do reproduce.
  (b) **Not a defect as described** — the row's spans are `exploitation-status span L15472-L15475` and
  `remediation-clock span L19165-L19168`. Read at the capture: `L15472` `dueDate`, `L15473`
  `knownRansomwareCampaignUse`, `L15474` `forensicTriage`, `L15475` `notes`; `L19165` `dateAdded`,
  `L19166` `shortDescription`, `L19167` `requiredAction`, `L19168` `dueDate`. The row's own sentence
  enumerates exactly those fields ("the remediation deadline, the known-ransomware flag, the
  forensic-triage flag, and the NVD reference"), so the span is accurate and only its *label*
  ("exploitation-status") is a grouping name that starts on the deadline. A status-only span would be
  `L15473-L15474`; the span as written is not wrong. I record the wording difference, not a repair.
- **F-10 (registry citation integrity, from the final churn record):** One half of `:111` checks out:
  its digest for `:79` (`f2ab0a64…`) is the line plus newline, verified here. The defect is the other
  half. `corpus/SOURCES.md:111` cites
  this receipt's §5 as "4495 bytes, sha256 `dc1a549a…`"; the receipt was 34,565 bytes /
  `4c1ef7ae…` when that record was written and 41,362 bytes / `d6204728…` when this finding was
  added, and any further revision changes it again, so a fixed digest quoted here would be stale by
  construction — the current digest is the file's, not this sentence's. The cited 4,495 bytes /
  `dc1a549a…` matches no state this seat produced. The
  same record calls the landed `:79` bullet "superseded by the wider draft", which a `.ufo/waves/…`
  draft cannot be — either the bullet is replaced in `corpus/` or the draft remains an input. Details
  and the byte-level quotes: R-14. Not repairable from this seat's write scope.
- **F-11 (incomplete scope correction in the landed R8):** `:112` repairs the omission of
  `corpus/lessons/` from the bullet's zero-hit sweep but not the omission of
  `corpus/source-snapshots/`, where 33 of the 35 pre-existing `KEV` tokens live (§4b). An erratum that
  names one tree and not the other still leaves "0 hits" readable as a whole-corpus claim.


## 9. Limits

- I measured the feed at one instant and diffed it against the capture fetched 2.5 minutes earlier; I
  did not test behaviour across a `catalogVersion` rollover.
- I read BOD 22-01's and BOD 26-04's supersession/revocation clauses and the feed's directive mentions,
  not either directive's full operative text.
- The negative sweep is a fixed nine-term literal sweep plus the enumerated hit files; it is not a
  semantic search. A source that prioritizes by exploitation without using any of those nine strings
  would not have been found by it.
- I did not touch `corpus/SOURCES.md`, the manifest, `S052.txt` or any other seat's file. All numbers
  here are reproducible from § Report; the fetched pages lived in scratch and were deleted per the
  seat rule, so the digests in §2 are the durable record of them.
- The round-35 search-log bullet at `corpus/SOURCES.md:79` was written by another seat while I was
  measuring; I never saw its author or its receipt, so my audit is of the landed text only. Its
  narrower sweep scope is quoted from the line itself, not from that seat's report.

## Report

Scratch: two trees, both created with `mkdir -p` and deleted with `rm -rf` before yield with absence
verified — `/fast/scratch/hyaku/kasegi-r35/ScribeSearchLog` (fetch phase) and
`/fast/scratch/hyaku/kasegi-r35/ScribeSearchLog-verify` (redirect check); proofs at R-9 and R-12. No
tool installed or upgraded (nothing needed; `curl`, `python3`, `grep`, `wc`, `sha256sum` from the base
system).

### R-1 endpoint measurements (one pass, `curl -sS -L -A 'kasegi-shokunin/1.0' -o <n>.re -w '%{http_code}'`)

```
jsonroot http=404 curl_exit=0 bytes=46916 lines=1450 sha256=6ac5c3172f19e90c70cb782e503eeb28af5d5586664a1bfc802d1b39285a1e66
jsonfeed http=200 curl_exit=0 bytes=1807090 lines=27869 sha256=97a6e54bc74c651ab3c55657191db9adec6c63b05ca54e4205327cfd97a8fb70
csvfeed http=200 curl_exit=0 bytes=1073722 lines=1757 sha256=cb77ba6ee61c8fa963d2eb16dda2cd4746c5b11e0353f079d3e0e569eb5d2778
schema http=200 curl_exit=0 bytes=3623 lines=102 sha256=0d5865c98694c5bfba2c78a26caf814f406b3fce8bfb81bef79e99c7f288b0e7
kevpage http=200 curl_exit=0 bytes=284330 lines=3544 sha256=75a7af09177a570d283accd7eb9c5afc4f8f16c4a1447c5af3d003751f08aaa1
bod2201 http=200 curl_exit=0 bytes=87312 lines=1868 sha256=cd842541aeba7e82f987c92a049ce6236f606e74b454d97bfd6a9a4a743235c4
bod2604 http=200 curl_exit=0 bytes=84350 lines=1930 sha256=678921ff952f4f8d813bbcbd3fc6e9fed5b06c390d0a5ff43083f07f2a98d1cd
```

Exit code of the block: `exit=0`.

### R-2 capture vs live feed, and CSV reconciliation

```
$ grep -o '"cveID": "[^"]*"' jsonfeed.re | sort > f.ids
$ grep -o '"cveID": "[^"]*"' corpus/source-snapshots/round-35/S052.txt | sort > c.ids
$ diff -q f.ids c.ids ; echo $?
cveid_diff_exit=0 ids_fresh=1756 ids_capture=1756
$ printf 'csv_data_rows=%s csv_fields=%s\n' "$(($(wc -l <csvfeed.re)-1))" "$(head -1 csvfeed.re | awk -F, '{print NF}')"
csv_data_rows=1756 csv_fields=12
$ <sorted CSV header> vs <sorted JSON record fields>; diff -q ; echo $?
cols_eq_fields_exit=0
```

Per-field comparison (Python, `json.load` both, 1,756 records): `records_with_diffs 239`,
`diff_records 239`, `kinds {'whitespace-only': 240}` — no non-whitespace difference. Top-level
`catalogVersion/dateReleased/count/title` equal on both sides. Exit 0.

### R-3 negative sweep and scope

```
$ for t in 'KEV' 'known exploited' 'CISA' 'exploited vulnerabilities' 'BOD 22-01' 'EPSS' 'exploit maturity' 'exploitation status' 'prioritiz'; do
    printf '%-24s files=%-2s hits=%s\n' "$t" \
      "$(grep -rIl --include=*.md -F "$t" "$L/corpus" "$L/SKILL.md" | wc -l)" \
      "$(grep -rIo --include=*.md -F "$t" "$L/corpus" "$L/SKILL.md" | wc -l)"; done
KEV                      files=1  hits=1
known exploited          files=0  hits=0
CISA                     files=4  hits=14
exploited vulnerabilities files=1  hits=1
BOD 22-01                files=0  hits=0
EPSS                     files=0  hits=0
exploit maturity         files=0  hits=0
exploitation status      files=0  hits=0
prioritiz                files=2  hits=2
scope_files=99
$ find corpus -name '*.md' -type f | wc -l
104          # + SKILL.md = 105 walked; 99 = domain subset listed in §4
```

Hit locations (exact, re-grepped): `corpus/lessons/round-22.md:91`;
`corpus/knowledge/cra-manufacturer-reporting-duties.md:10`;
`corpus/knowledge/authorization-safe-harbor-and-scope.md:24,38`;
`corpus/knowledge/coordinated-disclosure-timelines.md:34`; `corpus/README.md:206`;
`corpus/SOURCES.md:61`. `grep -rIl -F CISA` → the 4 files named in §4.

### R-4 feed-content facts quoted in §8

```
$ python3 - (json.load of S052.txt)
BOD 22-01 (340, 340)          # records / occurrences
BOD 26-04 (139, 557)
CVSS (0, 0)
severity (2, 2)
ransomware Known records 361
forensicTriage Yes 91
distinct dueDate 513
```

### R-5 directive status (page text, tag-stripped)

```
$ grep -oiE '<title>[^<]*</title>' bod2201.re bod2604.re
bod2201.re:<title>BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Revoked) | CISA</title>
bod2604.re:<title>BOD 26-04: Prioritizing Security Updates Based on Risk | CISA</title>
$ grep -oiE '.{0,110}(supersed|rescind|archiv|BOD 26-04).{0,110}' bod2201.re | sed 's/<[^>]*>//g'
    Archived Content    In an effort to keep CISA.gov current, the archive contains outdated information …
          This Directive has been revoked. It is superseded by BOD 26-04.
$ grep -oiE '.{0,110}(BOD 22-01|supersed|replac).{0,110}' bod2604.re | sed 's/<[^>]*>//g'
… This Directive supersedes and hereby revokes BOD 19-02 … and BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Nov. 3, 2021). …
$ grep -oiE 'BOD [0-9]{2}-[0-9]{2}' kevpage.re | sort | uniq -c
    101 BOD 26-04
```

### R-6 SOURCES coordinates and PRE-STATE

```
$ grep -n '^## ' corpus/SOURCES.md
3:## Registry
59:## Paths
66:## Search log
79:## Leads (unopened)
85:## Registry changes
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
51
$ ls corpus/knowledge/*.md | wc -l
46
$ grep -nE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md ; echo "grep_exit=$?"
grep_exit=1        # row not landed at measurement time
$ sed -n '77p' corpus/SOURCES.md | wc -c
2657
$ awk 'NR>=55 && NR<=60' corpus/SOURCES.md   # last row 57, blank 58, Paths 59
```

### R-7 digests of cited artifacts (read-only; no lane write by this seat)

```
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md   # 06:36Z, PRE-STATE (51 rows; line count not measured then)
510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829  corpus/SOURCES.md   # 06:39Z, round 35 landed (110 lines, 52 rows)
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md
```

`corpus/SOURCES.md` is being written by sibling seats, so its digest only identifies a state: the two
above are the states this seat measured, and the current file must be re-hashed before any citation
made from this receipt is trusted.

### R-8 touched surfaces

This seat wrote exactly one path: `.ufo/waves/round-35/wave1/ScribeSearchLog.md`. No `corpus/`,
`SKILL.md`, `SCORECARD.md`, manifest, claims, or `.ufo/waves/round-35/claims.json` write; no git/jj
mutation; no fleet/sibling/shokuknow access beyond the read-only `scripts/sources-census.sh` enum
grep in §5.

### R-9 scratch cleanup (performed, after the measurements above)

```
$ S=/fast/scratch/hyaku/kasegi-r35/ScribeSearchLog; rm -rf -- "$S"; echo "rm_exit=$?"
rm_exit=0
$ ls -d "$S"
ls: cannot access '/fast/scratch/hyaku/kasegi-r35/ScribeSearchLog': No such file or directory   # ls_exit=2
```

The fetched pages that produced §2's digests existed only in that tree and are gone; the digests are
the durable record. Nothing of this seat's remains on disk outside the lane wave dir.

### R-10 redirect/transport check on the feed (independent of the capture seat)

```
$ curl -sS -A 'kasegi-shokunin/1.0' -o /dev/null -w 'num_redirects=%{num_redirects} http=%{http_code} url_effective=%{url_effective} size=%{size_download}\n' \
    https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
num_redirects=0 http=200 url_effective=https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json size=1807090
```

Note the difference from R-1: R-1 followed redirects (`-L`) and reported the same 1,807,090 bytes;
without `-L` the request still returns 200 with the effective URL equal to the requested one, so the
landed bullet's "requested URL == effective URL with no redirect" is corroborated by this seat.

### R-11 post-append state of `corpus/SOURCES.md`, and the landed bullet audit

```
$ wc -lc corpus/SOURCES.md ; sha256sum corpus/SOURCES.md
  110 64172 corpus/SOURCES.md
510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829  corpus/SOURCES.md
$ grep -n '^## ' corpus/SOURCES.md
3:## Registry   60:## Paths   67:## Search log   81:## Leads (unopened)   87:## Registry changes
$ grep -nE '^\|[[:space:]]*S05[12][[:space:]]*\|' corpus/SOURCES.md | cut -c1-30
57:| S051 | Immunefi Vulnerabi
58:| S052 | CISA Catalog of Kno
$ grep -n 'Immunefi severity-classification sweep' corpus/SOURCES.md | cut -c1-40
78:- Immunefi severity-classification sw
$ awk 'NR==79{print length($0)}' corpus/SOURCES.md
2387
$ awk 'NR>=67 && NR<=82 && /^- /{c++} END{print "bullets="c}' corpus/SOURCES.md
bullets=11
$ awk 'NR>=108 && NR<=110{printf "%d:%s\n", NR, substr($0,1,60)}' corpus/SOURCES.md
108:- S052 row added: new row (id `S052`, kind `dataset`, tier A scoped to
109:- S052 cells not edited after append: the row is authored and applied
110:- No status/recheck/used-by cell changed on any pre-existing row; S001
```

Landed-bullet probes (`python3`, `b.count(probe)` on line 79): `identified 1`, `screened 2`,
`included 1`, `excluded 1`, `stop 0` (the rationale is spelled `Stop:` capitalised, which the
lowercase probe misses — the text is there), `404 1`, `csv/known_exploited 1`, `schema 2`,
`BOD 22-01 2`, `BOD 26-04 2`, `Revoked 0`, `PRE-STATE 1`, `date: 1`, `2026-10-26 2`.
`Revoked 0` is the material gap named in §5/F-7: the revocation finding is absent from the landed
line.

### R-12 second scratch cleanup

```
$ S=/fast/scratch/hyaku/kasegi-r35/ScribeSearchLog-verify; mkdir -p "$S"; cd "$S"; curl …; cd /; rm -rf -- "$S"
cleanup_exit=0
$ ls -d "$S"
ls: cannot access '/fast/scratch/hyaku/kasegi-r35/ScribeSearchLog-verify': No such file or directory
```

### R-13 cross-check of peer-reported defects, measured at two states

Peer: `ScribeSOURCESRow-2` reported (a) that `:79`'s "7 SOURCES rows" is wrong and (b) that the row
`:58` span labels are misaligned. I re-measured both.

```
$ git show 3266c9937b03062d9bbc2f436e20820115ed179c:corpus/SOURCES.md | grep -icE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|.*CISA'
5                                    # base: S003, S008, S021, S023, S026
$ grep -icE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|.*CISA' corpus/SOURCES.md
6                                    # + S052: 6
$ awk 'NR>=15470 && NR<=15476 {printf "%d:%s\n", NR, substr($0,1,60)}' corpus/source-snapshots/round-35/S052.txt
15472:"dueDate": "2022-07-18",
15473:"knownRansomwareCampaignUse": "Known",
15474:"forensicTriage": "No",
15475:"notes": "https:\/\/nvd.nist.gov\/vuln\/detail\/CVE-2022-29499",
$ awk 'NR>=19164 && NR<=19169 {…}' corpus/source-snapshots/round-35/S052.txt
19165:"dateAdded": "2022-03-25",
19166:"shortDescription": "Citrix SD-WAN and NetScaler SD-WAN allow SQL Injection.",
19167:"requiredAction": "Apply updates per vendor instructions.",
19168:"dueDate": "2022-04-15",
```

- **(a) confirmed**: 5 CISA rows at base, 6 now; `7` matches neither. Recorded as F-9(a).
- **(b) not a defect as described**: `L15472-L15475` is `dueDate, knownRansomwareCampaignUse,
  forensicTriage, notes` and `L19165-L19168` is `dateAdded, shortDescription, requiredAction,
  dueDate` — the fields the row's own sentence enumerates ("the remediation deadline, the
  known-ransomware flag, the forensic-triage flag, and the NVD reference"). A status-only span would
  start at `L15473`; the span as written is accurate, only its label is a grouping name.

CISA token counts are state-dependent and I publish them with that caveat: base `3266c993` → **9**
uppercase-`CISA` occurrences over the four files (SOURCES 9, `authorization-safe-harbor-and-scope.md`
2, `coordinated-disclosure-timelines.md` 1, README 0); `4c85ff86…` (06:36Z) → **14**; current
`0f95a132…` → **24** (SOURCES 19, README 2, 2, 1) and **44** case-insensitive, because every
`https://www.cisa.gov/…` URL matches. §4's table records the 06:36Z value; the +5 between base and
06:36Z predates the append I measured and that intermediate tree state was never committed, so I do
not claim to explain it. The sweep's conclusion does not depend on the count: each hit was read, and
none is a prioritization source.

### R-14 `corpus/SOURCES.md` moved twice more after §6 (churn record)

```
$ sha256sum corpus/SOURCES.md ; wc -l corpus/SOURCES.md
4c85ff86…e77b6    # 06:36Z, 51 rows  (PRE-STATE used in §4/R-6)
510e3bba…b8829    # 06:39Z, 110 lines, 52 rows  (§6's landed state)
0f95a132…2f6ba    # 06:4xZ, 112 lines, 52 rows  (two more R8 lines at :111-:112)
$ sed -n '111,112p' corpus/SOURCES.md | cut -c1-200
- Round-35 Search-log bullet superseded: the bullet now at :79 (sha256 `f2ab0a64…`) is superseded by the wider draft in `.ufo/waves/round-35/wave1/ScribeSearchLog.md` §5 (4495 bytes, sha256 `dc1a549a…`), …
- Round-35 Search-log bullet scope correction: the PRE-STATE zero-hit counts in the bullet at :79 (KEV 0, …) are scoped to corpus/knowledge/*.md (46 files), corpus/README.md, corpus/SOURCES.md and SKILL.md only; …
```

Two consequences, both findings rather than repairs (F-10):

1. `:111` cites this receipt's §5 at "4495 bytes, sha256 `dc1a549a…`". This receipt is **34,565
   bytes, sha256 `4c1ef7ae…`** at the state that record was written, and §5 has been revised since
   (it now audits the landed line rather than proposing an append). A registry record that quotes a
   digest of a document which no longer has it is unresolvable — the R8 line must cite the final
   digest or name a copied artifact.
2. `:111` calls the landed bullet "superseded by the wider draft". A draft under `.ufo/waves/…` is
   not the registry; either the bullet is replaced (a corpus write) or the draft stays an input. As
   written, the registry says a landed line is superseded by an unlanded one.
3. `:112` records the scope correction for the zero-hit counts and names
   `corpus/lessons/round-22.md:91` — matching §4 of this receipt; that one is consistent.

### R-15 capture-byte sweep and line digest (closes §4b)

```
$ grep -rIl 'KEV' corpus/source-snapshots/
corpus/source-snapshots/round-24/{S001,S008,S009,S013,S014,S015}.txt
corpus/source-snapshots/round-24/manifest.json
corpus/source-snapshots/round-35/S052.txt
$ for f in $(grep -rIl 'KEV' corpus/source-snapshots/); do printf '%-52s hits=%s\n' "$f" "$(grep -o KEV "$f" | wc -l)"; done
round-24/S001.txt 1 · S008.txt 2 · S009.txt 1 · S013.txt 1 · S014.txt 1 · S015.txt 27 · manifest.json 1 · round-35/S052.txt 3
$ grep -rIn 'Top 10 KEV\|KEV Catalog\|CISA KEV' corpus/source-snapshots/round-24/*.txt
S001.txt:1082:such as the ISAC’s (Information Sharing and Analysis Center), CISA KEV or private
S008.txt:10:…Cybersecurity Awareness MonthKEV CatalogReport A Cyber Issue
S008.txt:67:…Cybersecurity Awareness MonthKEV CatalogReport A Cyber Issue
S009.txt:122:A system or product might have a lot of vulnerabilities, but … The CISA KEV says only about 400 new vulnerabilities were tracked as exploited, and only around 40 of those were zero-days …
S013.txt:28:Top 10 KEV Weaknesses
S014.txt:28:Top 10 KEV Weaknesses
S015.txt:28:Top 10 KEV Weaknesses
$ grep -n 'KEV' corpus/source-snapshots/round-24/S015.txt | head -3
28:Top 10 KEV Weaknesses
60:CVEs in KEV
214:CVEs in KEV: 7
$ python3 -c "import json;m=json.load(open('corpus/source-snapshots/round-24/manifest.json'));[print(s['id'],s['url']) for s in m['sources'] if s['id'] in ('S001','S008','S009','S013','S014','S015')]"
S001 https://www.first.org/cvss/v4.0/user-guide
S008 https://www.cisa.gov/vulnerability-disclosure-policy-template
S009 https://www.ncsc.gov.uk/blogs/10-questions-ask-using-ai-models-find-vulnerabilities
S013 https://cwe.mitre.org/top25/archive/2025/2025_methodology.html
S014 https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html
S015 https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html
$ python3 -c "import hashlib;b=open('corpus/SOURCES.md','rb').read().split(b'\n')[78];print(len(b), hashlib.sha256(b+b'\n').hexdigest())"
2393 f2ab0a647031489dd96f5e5fe35b20318ebae7ed9bd8cdcb6fbc51e8ff42ab54
```

Note the last line: `:79` is 2,393 **bytes** / 2,387 characters (the six-byte difference is two `…`
and one `—`), so a character count and a byte count of that line differ without any edit having
happened.

### R-16 KEV token totals used in §4b and F-11

```
$ cat corpus/source-snapshots/round-24/S0{01,08,09,13,14,15}.txt | grep -o KEV | wc -l
33
$ grep -o KEV corpus/source-snapshots/round-24/manifest.json | wc -l
1
$ grep -o KEV corpus/lessons/round-22.md | wc -l
1
$ grep -o KEV corpus/source-snapshots/round-35/S052.txt | wc -l
3
$ echo $((33+1+1))
35                                     # pre-existing tokens, S052 excluded
$ cat corpus/knowledge/cisa-kev-catalog.md corpus/SOURCES.md corpus/README.md corpus/lessons/round-22.md | grep -o KEV | wc -l
23                                     # markdown side after the F18 landing
```
