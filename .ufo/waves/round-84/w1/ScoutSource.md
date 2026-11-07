# ScoutSource — round 84, attempt 1, w1

Seat: scout (read-only; no lane edits). Axes touched: `depth:verifiability`, `coverage`.
All probes ran 2026-11-06T23:47Z–23:54Z against the frozen S118 capture and the live public
surfaces. Scratch root `/fast/scratch/hyaku/kasegi-r84/ScoutSource` (deleted on exit); every cited
receipt was copied first into `.ufo/waves/round-84/w1/ScoutSource-receipts/`.

No tooling was installed this seat (no install needed; `curl`, `python3`, `sha256sum` were present).

---

## 1 — S118 re-open: the six manifest quotes

**Result: the frozen capture reproduces byte-identically, and all six quotes locate at their pinned
lines. Nothing in the C2 claim's quote layer is broken.**

| check | command | observed |
|---|---|---|
| refetch the page | `curl -sSL -o $S/data.html -w '%{http_code} %{size_download}' https://google.github.io/osv.dev/data/` | `HTTP=200`, 27,419 bytes raw, `time_total=0.178630` |
| re-derive the snapshot with the committed instrument's algorithm (`capture-source.py` `html_to_text`: script/style strip → block-tag→newline → tag strip → entity decode → per-line whitespace collapse) | see `ScoutSource-receipts/data.txt` | 5,820 bytes, sha256 `e824a73545bedd0abae5f84cd120a5c73e482d7e935bc1534a08a1e1adfa5359` |
| compare against the frozen bytes | `sha256sum corpus/source-snapshots/round-84/S118.txt` | `e824a735…fa5359` — **identical**, byte-for-byte |
| six manifest quotes in the tag-stripped text | occurrences per quote over the stripped lines | Q01=1 @L102, Q02=1 @L104, Q03=1 @L104, Q04=1 @L114, Q05=1 @L121, Q06=1 @L123 — every declared anchor holds |
| the lane's own frozen recheck instrument | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-84/manifest.json --source S118` | `S118:sha256 OK` + six `OK occurrences=1 anchor=N-ok`, exit 0 |

Quote word counts (all ≤ 25): 17, 8, 13, 7, 15, 12.

**Distinctness spot-check of the six quotes against the other corpus entries** (the F60 entry's own
`Distinctness` section claims 0 files each for a literal sweep):

| quote prefix | files in `corpus/knowledge/` |
|---|---|
| "This bucket contains a zip file with all vulnerabilities across all ecosystems" | 1 (= the F60 draft itself) |
| "Individual vulnerability records can be found at gs://osv-vulnerabilities" | 1 (= the F60 draft itself) |
| "are exported to the gs://osv-vulnerabilities/[EMPTY]/ directory" | 0 (F60's own text carries a line break, so the literal prefix does not match it) |
| "The per-ecosystem files omit the" | 1 (= the F60 draft itself) |
| "the data dump will always contain an ecosystem directory without the" | 1 (= the F60 draft itself) |
| "OSV.dev has stopped exporting entries for ecosystems with prefixes" | 1 (= the F60 draft itself) |

So the sweep is clean against the 97 other entries; the hits are the new entry's own text.

## 2 — upstream `docs/data.md`: wording difference on the pinned lines

Fetched `https://raw.githubusercontent.com/google/osv.dev/master/docs/data.md` — HTTP 200, 9,938 bytes,
`time_total=0.231266`; copy at `ScoutSource-receipts/upstream-data.md`.

**Verdict: there is NO wording difference on any of the six pinned lines.** Each manifest quote is a
verbatim substring of the upstream markdown (after removing the markdown backticks the upstream uses
around the code spans); the upstream line numbers are 145, 149, 149, 168, 181, 187 (Q01, Q02, Q03,
Q04, Q05, Q06 respectively), and each quote occurs exactly once in the upstream file.

The only difference on a pinned line is a **markdown-rendering artefact, not a wording change**:

- **Q06 only.** Upstream L186–187 reads `**Note:** OSV.dev has stopped exporting entries …`;
  the rendered snapshot L123 reads `Note: OSV.dev has stopped exporting entries …`. The captured page
  therefore carries the literal prefix `Note: ` that the upstream markdown puts on its own
  preceding line. **The six pinned quotes themselves are unaffected** — Q06's quote begins at
  "OSV.dev has stopped…" — but any future quote that starts at "Note:" would exist only in the
  rendered form, not in the upstream source. Worth knowing for a round-85 re-capture against the
  upstream file rather than the site.

Two upstream-only phrases exist in the *same region* but outside the six pinned lines (the upstream
markdown carries links where the rendered page carries plain text):

- "aggregated and [continuously](…) exported to a GCS bucket" → rendered "continuously exported";
- "A list of all current ecosystems is available at [gs://osv-vulnerabilities/ecosystems.txt](…)";
- "the steps and [data licensing requirements](./new_source.md#data-licensing)" → rendered "the
  steps and data licensing requirements"; "to [REST API endpoints](./rest-api.md)" → "to REST API
  endpoints".

None of these is a wording change to a pinned clause; they are the upstream's link markup.

## 3 — the GCS layout claims are observable without credentials

**Result: YES — all four checked layout facts are directly observable with unauthenticated HEAD and
Range requests, and three of them are additionally corroborated by object listings. One F60 claim
is materially incomplete against the live bucket (see 3.4).**

### 3.1 HEAD probes (no bulk download)

| URL | HTTP | content-length | content-type | last-modified |
|---|---|---|---|---|
| `https://storage.googleapis.com/osv-vulnerabilities/ecosystems.txt` | 200 | 376 | `text/plain` | Tue, 27 Oct 2026 04:03:08 GMT |
| `https://storage.googleapis.com/osv-vulnerabilities/modified_id.csv` | 200 | 157,675,926 | `text/csv` | Fri, 06 Nov 2026 23:33:09 GMT |
| `https://storage.googleapis.com/osv-vulnerabilities/all.zip` | 200 | 2,926,598,695 | `application/zip` | Fri, 06 Nov 2026 23:48:34 GMT |

Both HEAD requests succeeded with no credentials (no `Authorization` header, no query parameter).

### 3.2 `ecosystems.txt` — `[EMPTY]` appears, no colon-suffixed name appears

Range request `Range: bytes=0-300` → HTTP 206, 301 bytes; remainder `Range: bytes=300-375` → HTTP 206,
76 bytes; whole object re-fetched clean (376 bytes, sha256 `8d788ecc0f2100cb4bc87cf994c2997d717a50e9441538b1264596d3770183d8`,
copy at `ScoutSource-receipts/eco-full.txt`).

- **47 ecosystem lines.**
- **`[EMPTY]` appears exactly once** (the last-but-few block, line 42 of 47) — the direct `[EMPTY]/`
  directory of F60 Claim 3 is listed in the project's own ecosystem listing.
- **No colon-suffixed directory name appears** — `grep -c ':'` over the whole listing = **0**. The
  listing carries `Alpine` (bare), never `Alpine:v3.17`. This is the live corroboration of F60
  Claim 5's ecosystem-naming rule.
- First 5 lines as served: `AlmaLinux`, `Alpaquita`, `Alpine`, `Android`, `Azure Linux`.

### 3.3 Per-ecosystem vs top-level `modified_id.csv` — the prefix rule is observable

F60 Claim 4's rule ("the per-ecosystem files omit the `<ecosystem_dir>/` prefix") is directly
observable from the first bytes of each file:

| file | first two rows (Range 0-120) | prefix present? |
|---|---|---|
| `modified_id.csv` (top level) | `2026-11-06T23:45:03.080570303Z,Echo/ECHO-5395-e69b-0d30` | **yes** — `Echo/` prefix |
| `PyPI/modified_id.csv` | `2026-11-06T22:45:03.160810421Z,MAL-2026-18741` | **no** — bare id |
| `npm/modified_id.csv` | `2026-11-06T23:30:04.346479598Z,MAL-2026-18737` | **no** — bare id |
| `Go/modified_id.csv` | `2026-11-06T20:00:05.902584949Z,GHSA-qx75-2p3r-pwm5` | **no** — bare id |

Same date, same schema, different prefixing — the rule is falsifiable and it holds live.

### 3.4 **FINDING — F60 Claim 5/6 is incomplete against the live bucket: the colon-suffixed directories still exist**

This is the one place where the live surface says something the F60 draft does not.

- The bucket's own directory listing (`GET https://storage.googleapis.com/osv-vulnerabilities/?delimiter=/&max-keys=1000&fields=prefixes`)
  returns **58 prefixes, of which 30 are colon-suffixed**: `Alpine:v3.2/` … `Alpine:v3.20/` (19) and
  `Debian:3.0/` … `Debian:13/` (11).
- Those directories **are still present and still served**, not deleted:
  `Alpine:v3.17/all.zip` → HTTP 200, 5,575,104 bytes; `Alpine:v3.16/all.zip` → 200;
  `Alpine:v3.15/all.zip` → 200; `Alpine:v3.10/all.zip` → 200.
- But they are **frozen**: every colon-suffixed `all.zip` carries `last-modified: Wed, 09 Oct 2024`
  (Alpine) / `04 Oct 2024` (Debian), while the base directories are live —
  `Alpine/all.zip` → `last-modified: Fri, 06 Nov 2026`, `Debian/all.zip` → `Fri, 06 Nov 2026`.
  Per-record objects under `Alpine:v3.17/` are likewise all `2024-10-09T…` (e.g.
  `Alpine:v3.17/CVE-2006-20001.json`, 14,312 bytes, 2024-10-09T01:20:13.981Z).
- Correspondingly, `Alpine:v3.17/modified_id.csv` → **404**, `Alpine:v3.20/modified_id.csv` → **404**.

**Reading.** F60's Claim 5 says the dump "will always contain an ecosystem directory without the
`:.*` suffix" and its falsifiable rule says "a script that looks for a dump directory named after a
release-suffixed ecosystem string such as an Alpine version **finds nothing**". The live bucket
shows the *base* directory is current — that half holds. But the suffixed directories are **not
absent**; they are present and stale. A reader who follows F60's stated rule verbatim would
conclude the lookup returns nothing, and would in fact get a populated-but-frozen directory
containing advisories from 2024 and earlier. The F60 text's "Not claimed" list already excludes
"when the prefixed exports stopped, or whether stale suffixed directories are deleted or only left
unrefreshed" — the live evidence answers that excluded question in one direction (**left
unrefreshed, not deleted**), which is exactly the sort of thing a falsifiable-rule sentence should
not leave a reader guessing about. The wording "finds nothing" is the defect; the observation is
not in conflict with the page's own sentence.

Re-runnable:
```
curl -sSI 'https://storage.googleapis.com/osv-vulnerabilities/Alpine:v3.17/all.zip' | grep -i last-modified
curl -sSI 'https://storage.googleapis.com/osv-vulnerabilities/Alpine/all.zip'      | grep -i last-modified
curl -sS 'https://storage.googleapis.com/osv-vulnerabilities/?delimiter=/&max-keys=1000&fields=prefixes' | grep -o '<Prefix>[^<]*</Prefix>' | grep ':'
```

### 3.5 Two further live observations, both strengthening F60

**(a) Claim 1 (the full zip includes withdrawn records) — verified without downloading the zip.**
`all.zip` is 2.9 GB, so it was not fetched whole. Instead: a `[EMPTY]` record was read directly
(`GET https://storage.googleapis.com/osv-vulnerabilities/[EMPTY]/ASB-A-145546313.json`) and it
carries `"withdrawn": "2026-11-06T16:30:33.305097686Z"` with `affected: []` and keys
`['id','modified','published','schema_version','withdrawn']` — i.e. a record with **no ecosystem**
and a **withdrawn timestamp**, exactly the "typically withdrawn ones" case Claim 3 names. The
`[EMPTY]/` prefix listing confirms the directory is populated and current
(`[EMPTY]/ASB-A-145546313.json`, last-modified 2026-11-06T17:00:15.357Z; `[EMPTY]/all.zip` 19,516,246
bytes, last-modified 2026-11-06).
Then, via `Range` requests into the zip's byte stream, the **name** `ASB-A-145546313.json` was
found inside `all.zip` (scanning bytes 9,000,000–20,000,000: 7,554 distinct `.json` names, 2,272 of
them `ASB-A-*`, target present = True). So the withdrawn record exists both in `[EMPTY]/` and
inside the full-database zip — Claim 1's substance is observable.

**(b) Claim 2 (per-record JSON path) — verified live.** `GET
https://storage.googleapis.com/osv-vulnerabilities/Go/GHSA-qx75-2p3r-pwm5.json` → **HTTP 200**;
the same id at the bucket root → 404, and `PyPI/OSV-2020-111.json` → 404 (that id is not a PyPI
record). The path shape `<ECOSYSTEM>/<ID>.json` holds exactly as claimed.

**(c) `ecosystems.txt` vs the bucket's directory list — one divergence worth a round-85 eye.**
`DWF/` and `JavaScript/` exist as bucket prefixes but are **absent from `ecosystems.txt`** and from
the page's covered-ecosystems list (S118.txt:66-96). Both are stale
(`DWF/all.zip` last-modified 2022-11-21, `JavaScript/all.zip` 2022-10-03) and neither has a
`modified_id.csv` (both 404). This is a legitimate new observation about the listing, but it is
**not** a defect in F60 — F60 explicitly does not claim the `ecosystems.txt` listing (its
"Not claimed" list names it at :122, context only). Recorded here as a round-85 lead candidate.

## 4 — the two leads

Both were opened read-only at the times shown; each quote is verbatim from the tag-stripped text,
each is ≤ 25 words, and each page was grepped against `corpus/SOURCES.md` first.

### Lead 1 — OSV.dev's own data-quality program post (the round-83 lead)

- **URL:** `https://osv.dev/blog/posts/announcing-data-quality-initiatives/`
- **HTTP 200**, 9,941 bytes raw, `time_total` 0.72–0.79 s; accessed 2026-11-06T23:50Z.
- **Located quote (12 words), snapshot line 46:**
  "Downstream data consumers often mistake OSV.dev as the originator for the data"
- Second located quote (14 words, **spans lines 59–60**): "Thereafter, we will begin gating record
  imports to records that meet the quality requirements."

**Important defect in the r83 hand-off.** The r83 ScoutPerish report offers as *the* located quote
"Thereafter, we will begin gating record imports to records that meet the quality requirements."
(15 words). That string **does not occur contiguously in the stripped text** — the capture's
per-line whitespace collapse splits it as `"…to records that meet the quality"` (L59) +
`"requirements."` (L60). It occurs only after whitespace normalisation. `source-recheck.py`
normalises whitespace before matching (`normalize()` = `" ".join(MARKUP_RE.sub("", text).split())`),
so the *manifest* would still bind it; but the corpus's own locating convention elsewhere in this
lane is a quote that sits **on its exact snapshot line**, and this one does not. A round-85 entry
built on this page should pin a quote that is contiguous on one line — the 12-word L46 sentence is
exactly that, and it is also the more distinctive claim (consumer-side originator confusion).

**Admissibility (PROVINCE.md):** fits as an OSV-family entry on the same grounds r83 argued. The
lane owns advisory-quality ground for a researcher who files or cites OSV records, and this is the
OSV project's own statement of how it treats record quality across the publication lifecycle, held
in a *different page* from F58 (`data_quality.html`), F57 (`get-v1-importfindings/`) and F59
(`faq/`). `[INFERENCE]` on registry `kind`: it is a project blog post; the registry `kind` enum
admits `docs`, and tier A would mean "primary or authoritative for that scope" — the OSV project's
own program post is primary for its own program. The L1 owns the `kind`/`tier` decision.

### Lead 2 — OSV.dev's `GET /v1/vulns/{id}` reference page (new; not registered anywhere)

- **URL:** `https://google.github.io/osv.dev/get-v1-vulns/`
- **HTTP 200**, 19,961 bytes raw, `time_total` 0.017–0.025 s; accessed 2026-11-06T23:50Z.
- **Located quote (19 words), snapshot line 29:**
  "The only parameter you need for this API call is the vulnerability id, in order to construct the URL."
- Second located quote (8 words, line 24): "Returns vulnerability information for a given vulnerability id."
- Stripped text kept at `ScoutSource-receipts/getv1vulns.txt` (2,338 bytes, sha256
  `0b1232d66716cb3220bcd8b13379e47139c50880de2ed27670f6ce15759bda04`).

**Why it is not registered.** `grep -c 'get-v1-vulns' corpus/SOURCES.md` = **0**; the URL does not
appear in any `corpus/knowledge/` entry, nor in `corpus/README.md`. It appears only in
`corpus/lessons/round-77.md:14` and `corpus/lessons/round-78.md:41` as one of the four endpoint
leads deferred by R-77-F, whose recorded flip condition is precisely "one live slug captured with a
located quote and its own distinctness sweep, in a successor round". This seat has now discharged
that flip condition for this endpoint: live slug confirmed HTTP 200, located quotes pinned, and the
distinctness sweep run below.

**Distinctness sweep** (against `corpus/knowledge/`, 97 entries):

| candidate clause | held elsewhere? |
|---|---|
| "Returns vulnerability information for a given vulnerability id." | 0 files |
| "The only parameter you need for this API call is the vulnerability id…" | 0 files |
| "API requests are case-sensitive" | **1 file** — F51 (`corpus/knowledge/osv-post-v1-query-contract.md:31`), from S108.txt:53 |

So the endpoint's own parameter rule and its purpose sentence are unheld; the case-sensitivity
sentence is **already F51's** and must not be re-claimed (this is the same reject-line shape as the
round-77 R-119 line for F54's Q07/Q08/Q12).

**Additional unheld ground on this page** (none of it is on the get-v1-vulns page's own text but all
is observable on it): the sample 200 response shows the record shape `id`, `summary`, `details`,
`modified`, `published`, `references`, `type`, `url`, `affected[]` with `package`/`name`/`ecosystem`/
`purl`, `ranges[]` with `events` (`introduced`, `fixed`), `ecosystem_specific`, `severity`,
`database_specific`, `source`, `schema_version` (the sample carries `"schema_version": "1.4.0"`).
F59 already claims the *withdrawn* behaviour of this endpoint (Claim 2, from the FAQ page); the
get-v1-vulns page **contains no mention of "withdrawn"** (`grep -in 'withdrawn' → no match`), so a
scoped entry here would be disjoint from F59's Claim 2 and would sit beside F51's POST /v1/query
contract (F51 lists `GET /v1/vulns/{id}` as navigation only, in its Limits).

**Admissibility (PROVINCE.md):** fits as a round-85 lead on the same family grounds as F51–F59
("the same OSV API family as F51-F58"). It is an OSV-project primary page (tier A shaped like
S108–S117), it is the **read** side of the API — the counterpart of the POST query contracts the
lane already holds — and it is the last un-admitted member of the R-77-F four-endpoint set
(`determineversion` → F55, `ubuntu/binary-to-source` → F56, `importfindings` → F57; only
`GET /v1/vulns/{id}` remains). `[INFERENCE]` on the `kind`/`tier` cell remains the L1's.

**Other candidates opened and rejected, with reasons** (recorded so the L1 need not re-open them):

| candidate | HTTP | why not |
|---|---|---|
| `https://google.github.io/osv.dev/architecture/` | 200, 19,375 B | Highly substantive (the exporter/worker/importer pipeline description, "GCS acts as the primary source of truth"), and **not** registered anywhere in `corpus/`. But it is adjacent to F60's ground (the same exporter that writes the bucket F60 describes) and would need its own distinctness argument against F60; kept as the **second-choice** round-85 lead, not the primary. Text kept at `ScoutSource-receipts/architecture.txt`. |
| `https://google.github.io/osv.dev/contributing/` | 200, 12,465 B | Stripped body is 853 bytes / 32 lines of navigation chrome plus two content lines — no claim-bearing ground. |
| `https://google.github.io/osv.dev/quickstart/` | 200, 13,873 B | Two content lines (a two-run curl example); restatement of F51's request shape, not new ground. |
| `https://google.github.io/osv.dev/new-data-source/` | **404** | Wrong slug. |
| `https://osv.dev/data/` / `post-v1-vulns/` / `introduction/` / `third-party-tools/` / `docs/` | 404 | Wrong slugs (the live slugs are `google.github.io/osv.dev/data/` etc.). |

## 5 — what this seat recommends for round 85

1. **Re-capture `S118` is unnecessary** — the frozen capture reproduces byte-identically
   (`e824a735…fa5359`) and all six quotes hold at their anchors; the frozen `source-recheck.py`
   exits 0. The recheck is reproducible on demand, not a new claim.
2. **One routed defect for the L1**: F60's Claim 5 falsifiable rule says a lookup for a
   release-suffixed directory "finds nothing". The live bucket returns HTTP 200 for
   `Alpine:v3.17/all.zip` and 30 colon-suffixed prefixes exist; they are **stale** (frozen
   2024-10-09 / 2024-10-04) while the base dirs are current (2026-11-06), and their
   `modified_id.csv` files 404. The rule should say the suffixed directory is *present but frozen*,
   not absent. Re-runnable commands are in §3.4.
3. **Round-85 lead A (primary):** `GET /v1/vulns/{id}` — live, unregistered, flip condition
   already discharged, distinctness swept; do not re-claim the case-sensitivity sentence (F51
   holds it) and do not re-claim the withdrawn behaviour (F59 holds it).
4. **Round-85 lead B:** the data-quality program post — but pin the **12-word, single-line**
   L46 quote, not the r83 15-word quote, which is split across two snapshot lines.
5. **Round-85 observation to consider:** `ecosystems.txt` (47 entries) omits the stale `DWF/` and
   `JavaScript/` directories that the bucket still serves; F60 does not claim the listing, so this
   is additive, not a repair.
6. **Cross-check for the C2 gate:** the `ecosystems.txt` listing contains no colon-suffixed name
   (0 colons) while the bucket directory list contains 30 — the *listing* and the *bucket* are not
   the same surface, and a future entry must not treat the listing as the directory inventory.

## Files written by this seat

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-84/w1/ScoutSource.md` (this report)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-84/w1/ScoutSource-receipts/data.txt`
  (re-derived S118 snapshot, 5,820 B, sha256 `e824a735…fa5359`)
- `…/ScoutSource-receipts/upstream-data.md` (upstream `docs/data.md`, 9,938 B)
- `…/ScoutSource-receipts/eco-full.txt` (live `ecosystems.txt`, 376 B, sha256 `8d788ecc…183d8`)
- `…/ScoutSource-receipts/lead1.txt` (stripped data-quality blog post, 4,174 B, sha256 `487f3d04…6df8`)
- `…/ScoutSource-receipts/getv1vulns.txt` (stripped GET /v1/vulns/{id} page, 2,338 B, sha256 `0b1232d6…da04`)
- `…/ScoutSource-receipts/architecture.txt` (stripped architecture page, 3,884 B, sha256 `1f54ffdf…beac`)

No file outside `.ufo/waves/round-84/w1/ScoutSource*` was created or modified. No git/jj write of any
kind was performed; no lane, corpus, instrument or frozen byte was touched.
