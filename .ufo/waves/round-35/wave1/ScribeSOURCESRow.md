# ScribeSOURCESRow — round 35 draft: S052 registry row, search-log bullet, R8 registry-changes lines

Seat: ScribeSOURCESRow (leaf, scribe). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `3266c9937b03062d9bbc2f436e20820115ed179c`, claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`).
Axis owned by this seat: coverage (C2's S052 row). Date of all measurements: 2026-10-26.

**Coordination outcome up front.** A round-35 seat landed an S052 row, a round-35 search-log bullet and
three R8 lines at `corpus/SOURCES.md:58`, `:79` and `:108-110` *before this draft existed*, so nothing here
needed to be applied. I first addressed ExecRegistryAppend; that agent replied that it is the round-33
registry seat (S049/S050 only, `corpus/SOURCES.md:55-56`), disclaims the round-35 write and will not edit the
file again — so the writer of `:58/:79/:108-110` is an unnamed round-35 seat, and my F1 below records the
ordering event without attributing it to ExecRegistryAppend. The landed text is not a copy of this draft; it
is a different, valid shape.
This receipt therefore (a) preserves the draft as reference text, (b) verifies the landed bytes against the
committed capture line by line, and (c) reports the deltas and every defect I found. I did not edit
`corpus/SOURCES.md`, the entry, the capture or the manifest.

---

## 1. Draft (reference text — NOT applied; landed variant is at corpus/SOURCES.md:58/79/108-110)

### 1a. Registry row (11 cells, NF=13, no `|` inside any cell)

~~~text
| S052 | CISA Known Exploited Vulnerabilities catalog — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | dataset | A | CISA's own Known Exploited Vulnerabilities catalog feed: its title, version and record count, and the per-record keys each listed CVE carries on the 2026-10-26 release; no severity score and no prose definition of "known exploited" appear in it | capture corpus/source-snapshots/round-35/S052.txt (sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826, 27870 lines; manifest corpus/source-snapshots/round-35/manifest.json sha256 06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee, fetched 2026-10-26T06:32:40Z, requested URL == effective URL): L2 the feed's only descriptive line, the title "CISA Catalog of Known Exploited Vulnerabilities"; L3 catalogVersion "2026.10.23"; L4-L5 dateReleased 2026-10-23T19:30:18.9209Z and count 1756; L7-L21 the first record (L8 cveID CVE-2026-114625, L9 vendorProject, L10 product, L11 vulnerabilityName, L12 dateAdded, L13 shortDescription, L14 requiredAction, L15 dueDate, L16 knownRansomwareCampaignUse, L17 forensicTriage, L18 notes, L19-L21 cwes CWE-89); L15465-L15475 record CVE-2022-29499 with dueDate 2022-07-18 and knownRansomwareCampaignUse "Known"; L19161-L19168 record CVE-2019-12989 with dateAdded 2022-03-25 then dueDate 2022-04-15 | CISA titles the feed "CISA Catalog of Known Exploited Vulnerabilities" and every listed CVE carries dateAdded, a per-record dueDate and a requiredAction: read a listing as an exploitation record with a remediation clock, never as a severity grade, because the 12 per-record keys carry no CVSS, severity or score field and CVSS occurs 0 times in the capture — so a listing is not interchangeable with a severity ladder (S043/S044 platform ladders, S051 Immunefi table) and a high score is not the same signal as admission | mined | 2026-10-26 | 90d | corpus/knowledge/cisa-kev-catalog.md |
~~~

Shape proof of this draft (run on the draft string, not on the landed row):
`python3` split on `|` → `raw pipe count: 12`, `cells NF: 11 -> NF 13` (exit 0). No `|` appears inside a cell.

### 1b. `## Search log` bullet (PRISMA-shaped)

~~~text
- Known-exploited prioritization source sweep (round 35); question: does the lane already hold a source that ranks or prioritizes by known in-the-wild exploitation rather than by severity — CISA's Known Exploited Vulnerabilities catalog and the risk-based-update directive that consumes it — and does that feed add ground the lane's severity-ladder entries do not; where: CISA's own KEV JSON feed at https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json, the rendered catalog page at https://www.cisa.gov/known-exploited-vulnerabilities-catalog, and the path the round spec named, https://www.cisa.gov/known-exploited-vulnerabilities.json; plus a read-only negative sweep over the lane's own corpus — 51 registry rows and 46 knowledge entries (both pre-append) — for known exploited, Known Exploited, KEV, BOD 22-01, BOD 26-04 and exploited in the wild, 0 hits in every row and in every entry; date: 2026-10-26; identified 3 external candidates, screened 3, included 1 (the feed, captured as S052 with sha256 d69349e8…), excluded 2 — the spec-named .json path returns HTTP 404 (a 46916-byte HTML error page under the instrument, desktop-Chrome and curl-default user agents alike) and the rendered page repeats the same catalog as HTML without adding a field the feed lacks. The lane-internal sweep's KEV tokens are 33 across six round-24 captures plus one manifest line and one lesson line, and none of them is a KEV source: `S015` 27 (nav heading "Top 10 KEV Weaknesses" :28, the "CVEs in KEV" column :60 and "CVEs in KEV: 7" :214), `S008` 2 nav, `S013` :28 and `S014` :28 nav headings, `S001` :1082 names "CISA KEV" as one data source in prose, `S009` :122 already quotes a secondhand KEV statistic ("The CISA KEV says only about 400 new vulnerabilities were tracked as exploited, and only around 40 of those were zero-days when initially exploited"), `corpus/source-snapshots/round-24/manifest.json` 1 and `corpus/lessons/round-22.md:91` 1. So the negative result is source-level, not string-level: the lane held a secondhand KEV number but no row pinned CISA's own feed, which is exactly the gap S052 closes. Stop: the feed is the stating party's own machine-readable record set, it answers every load-bearing question the row needs (title L2, count L5, per-record clock L15, ransomware-use label L16), and no secondary aggregator can add ground it lacks, so a wider sweep would only re-read the same 1756 records.
~~~

### 1c. `## Registry changes` R8 lines

~~~text
- S052 row added: new row (id `S052`, kind `dataset`, tier A scoped to CISA's own Known Exploited Vulnerabilities catalog feed statements, status mined, opened 2026-10-26, recheck `90d`, used-by `corpus/knowledge/cisa-kev-catalog.md`), anchor pinned to the round-35 capture `corpus/source-snapshots/round-35/S052.txt` (sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, 27870 lines) and to the manifest that binds it (`corpus/source-snapshots/round-35/manifest.json`, sha256 `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`, quotes Q1-Q5 at L2, L3, L4, L15472, L19165, each occurrences=1). New authority, not a supersede: no pre-existing row or entry names the KEV catalog or either risk-based-update directive (0 hits at base 3266c993 across 51 rows and 46 entries), so no row is displaced and the feed URL appears once in the registry (no W04).
- S052 source URL recorded against the round spec: the spec-named `https://www.cisa.gov/known-exploited-vulnerabilities.json` returns HTTP 404 on 2026-10-26 (instrument UA, desktop-Chrome UA and curl default all 404; 46916-byte error page), so the row's source cell names the working feed `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` (HTTP 200, fetched_bytes 1807090, requested URL == effective URL, no redirect). The 404 path is logged here and nowhere in the registry.
- S052 append order: land the row only after `corpus/knowledge/cisa-kev-catalog.md` exists on disk, because census E11 fails closed on a used-by path missing from the lane; the row's used-by and the F18 entry's `source: S052` are the same pair, and the digest in the anchor cell is the committed capture's, not a later re-fetch (the feed is a living dataset: a re-fetch changes the count and every byte digest).
- No status/recheck/used-by cell changed on any pre-existing row; S001–S051 untouched (logged). Registry 51 rows pre-append → 52 post-append (R8).
~~~

---

## 1d. Ready-to-paste R8 correction for the bullet's digest abbreviation (NOT applied — this seat holds no append authority)

Three seats independently found the same defect in `corpus/SOURCES.md:79` (mine F8, ScribeSearchLog-3's
D-R35-SL-1, SimplifierDocs's R4 C-4): the bullet abbreviates the capture digest as `d69349e8…77e8826`, but
`77e8826` does not occur in `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`; its last
eight characters are `779e8826`. No appended line at `:108-112` repairs it. The line below is the smallest
conforming fix (an appended statement under R8/R9; it changes no row cell and states no new claim):

~~~text
- Round-35 search-log bullet digest abbreviation corrected (R9): the bullet at :79 prints `sha256 d69349e8…77e8826`, whose suffix `77e8826` does not occur in the capture digest; the committed capture `corpus/source-snapshots/round-35/S052.txt` ends `…6779e8826` (full digest `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, byte-identical to the value pinned in `corpus/source-snapshots/round-35/manifest.json` and in row S052's anchor cell). Nothing in the bullet changes: the abbreviation is the only error, no cell, manifest assertion or entry value depends on it, and the correct suffix is `779e8826`.
~~~

I am not the writer: the S052 row, bullet and R8 lines at `:58`, `:79`, `:108-110` were landed by an unnamed
round-35 seat before this draft existed, `:111-112` by another after my V-table, and ExecRegistryAppend (the
agent my item names as the applier) is the round-33 seat and has disclaimed any round-35 write. Per the
append-only discipline that pair of facts routes the fix to the round-35 writer or the L1, not to me; the
line above is supplied verbatim so no one has to re-derive it.

---

## 2. Verification of the landed text (ground truth, not a summary)

Landed: `corpus/SOURCES.md:58` (row), `:79` (round-35 search-log bullet), `:108-110` (R8 lines).
`corpus/SOURCES.md` sha256 at measurement: `510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829`.

| # | claim in the landed text | command | output | exit |
|---|---|---|---|---|
| V1 | row shape 11 cells / NF=13, id S052 | `python3` split of `corpus/SOURCES.md:58` | `NF: 13 cells: 11`; `starts/ends with pipe: True True`; `id cell: S052` | 0 |
| V2 | registry 52 rows, one S052 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` / same with `S052` | `52` / `1` | 0 |
| V3 | census clean | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi W04 S028 duplicate url …safe-harbor-overview-faq across scopes`; `kasegi W04 S029 duplicate url …2024/2847/oj/eng across scopes`; `kasegi ok …/corpus/SOURCES.md` | **0** |
| V4 | used-by target exists (E11) | `test -f corpus/knowledge/cisa-kev-catalog.md` | exists | 0 |
| V5 | capture digest | `sha256sum corpus/source-snapshots/round-35/S052.txt` | `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`; `27870` lines, `1479694` bytes | 0 |
| V6 | manifest digest and quote anchors | `sha256sum corpus/source-snapshots/round-35/manifest.json`; `json` dump of `sources[0]` | `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`; url = feed URL; `fetched_utc 2026-10-26T06:32:40Z`; Q1 anchor 2, Q2 3, Q3 4, Q4 15472, Q5 19165 | 0 |
| V7 | anchor line locators resolve | `sed -n '2,5p;8,21p' …/S052.txt`; `sed -n '22p'`; `sed -n '15465,15475p;19161,19168p'` | L2 title; L3 `"catalogVersion": "2026.10.23",`; L4 `dateReleased`; L5 `"count": 1756,`; L6 `"vulnerabilities": [`; L22 `},`; L15465 `"cveID": "CVE-2022-29499",` … L15472 `"dueDate": "2022-07-18",`; L19161 `"cveID": "CVE-2019-12989",` … L19168 `"dueDate": "2022-04-15",` | 0 |
| V8 | "no cvss field and no severity field on any record" | `grep -c 'CVSS' …/S052.txt`; key set of `vulnerabilities[0]` | `0`; `['cveID','vendorProject','product','vulnerabilityName','dateAdded','shortDescription','requiredAction','dueDate','knownRansomwareCampaignUse','forensicTriage','notes','cwes']` | 0 |
| V9 | count 1756 | `json.load` of the capture | `records 1756 count 1756`; `grep -c '^"cveID"'` = `1756` | 0 |
| V10 | entry ↔ row agree | `sed -n '3p' corpus/knowledge/cisa-kev-catalog.md`; `sha256sum corpus/knowledge/cisa-kev-catalog.md` | `source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture corpus/source-snapshots/round-35/S052.txt (27,870 lines; sha256 d69349e8…`; digest `da81204b3fbca378aa311406fd3a46394759967ecc3445297335a7526c573acf` | 0 |
| V11 | bullet's PRE-STATE sweep, measured at base | `git show 3266c993:corpus/SOURCES.md` then `grep`; `git grep -li` at `3266c993` | `base rows: 51`; `base KEV: 0 known_exploited: 0 known-exploited: 0 BOD22: 0 BOD26: 0`; `base knowledge files with cisa (ci) = 2` (`authorization-safe-harbor-and-scope.md`, `coordinated-disclosure-timelines.md`); `exploited vulnerabilities` = 1 file (`cra-manufacturer-reporting-duties.md`); `exploitation` = 3 knowledge files (+ `SOURCES.md`) | 0 |
| V12 | bullet's excluded siblings are real | `curl -sSL -A <instrument UA> -o /dev/null -w 'status=%{http_code} bytes=%{size_download} type=%{content_type}'` on the CSV and schema URLs | CSV `status=200 bytes=1073722 type=text/csv`; schema `status=200 bytes=3623 type=application/json` | 0 |
| V13 | spec's named URL is dead | same curl on `https://www.cisa.gov/known-exploited-vulnerabilities.json` | `status=404 bytes=46916` (HTML error page) | 0 (curl; the fetch itself is a 404) |

`V11`'s one mismatch, decomposed: the bullet says the PRE-STATE sweep found **"7 SOURCES rows"** bearing CISA.
At base `3266c993`, `git show 3266c993:corpus/SOURCES.md | grep -ci cisa` → **7 lines**, of which row lines
(`grep -E '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' | grep -ci cisa`) → **5** (`S003`, `S008`, `S021`, `S023`,
`S026`) and non-row lines → **2** (the base's search-log bullets at lines 69 and 70, the CVD and AI-validation
sweeps); total occurrences (`grep -o -i cisa | wc -l`) → **14**. The same row grep on the current tree, with
S052 added, is `6`. So the emitted `7` is a file-wide line count wearing a row's label. The "2 knowledge
files" half of that clause reproduces exactly.

**State drift after this table was taken.** Every V-row above was measured against `corpus/SOURCES.md` at
sha256 `510e3bba…b8829`, 110 lines. Another round-35 seat then appended `:111-:112` (see F9), moving the file
to sha256 `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba`, **112 lines**. The row at `:58`
and the bullet at `:79` were not rewritten by that append (line 79 still carries `77e8826` and "7 SOURCES
rows"), so V1–V13 remain true of the current bytes; only the file digest and line count in R10 need the
later value, recorded in R14.

---

## 3. Deltas: landed text vs this draft

| cell / item | landed | this draft | verdict |
|---|---|---|---|
| source cell | `CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed) — <feed URL>` | `CISA Known Exploited Vulnerabilities catalog — <feed URL>` | equivalent; both cite the feed URL byte-identically (entry's `source:` line matches) |
| scope | version/release, per-record field set, remediation clock | same, plus the explicit boundary "no severity score and no prose definition of `known exploited`" | draft is tighter; landed omits the definitional boundary that ExecC2Capture flagged |
| anchor | byte count + `L6 vulnerabilities array` + `L7-L22` + manifest Q1–Q5 pins | same line locators, no byte count, no manifest-pin sentence | **landed is stronger** on the manifest pin |
| teaches | "states exploitation status per record … a prioritization signal a severity score cannot supply" | names the absence proof (`CVSS` occurs 0 times) | landed asserts the consequence the draft (and the entry) prove; both grounded |
| search log | identified 5 surfaces (feed, catalog page, 404 path, CSV, schema), screened 5, included 1, excluded 4; eight-term sweep with per-token counts | identified 3, screened 3, included 1, excluded 2; six-term sweep | **landed is stronger** (it screened the CSV and schema siblings, both verified live at V12); one count in it is wrong (V11) |
| R8 lines | 3 lines (row added / no post-append cell edit / no pre-existing cell changed) | 4 lines (row added / URL substitution vs spec / append order for E11 / no pre-existing cell changed) | landed keeps the R8 essentials; it omits the append-order note and the spec-URL substitution record |

No landed cell is factually contradicted by the capture. The row passes census, the entry's `source` line
matches it, and the anchor lines resolve (V1–V10).

---

## 4. Findings

- **F1 (process).** A round-35 seat applied S052 before the scribe draft existed, although the executor item
  text says "exactly per the ScribeSOURCESRow draft (coordinate via agent message when it is written; do not
  proceed with a different shape)". ExecRegistryAppend — the agent I addressed as that executor — replied
  that it holds only the round-33 item and disclaims the round-35 write, so the appending seat is unnamed in
  my evidence. The landed shape differs from the draft (section 3) and is nonetheless valid on every frozen
  counter, so nothing needs undoing; the L1 decides whether the ordering rule needs a lesson row.
- **F2 (defect, one unit error).** `corpus/SOURCES.md:79` states the PRE-STATE sweep found **"7 SOURCES rows"**
  bearing CISA. Decomposed at base `3266c993`: **7 lines** contain `cisa` case-insensitively, of which **5
  are registry rows** (`S003`, `S008`, `S021`, `S023`, `S026`) and **2 are search-log prose** (the base's
  lines 69 and 70 — the CVD and AI-validation sweep bullets), with **14 total occurrences**. So `7` is a
  file-wide line count, not a row count: it is a unit error, not an invented number, and the correct row
  figures are **5 at base / 6 now** (S052 added). The corpus's own KEV/BOD zero-hit claims in the same bullet
  reproduce exactly (V11). An R9-style appended correction, not a rewrite, is the conforming fix (R8/R9) —
  ExecRegistryAppend's reply routes it the same way ("filed by the round-35 writer in that round's
  lesson/receipt, not silently rewritten into :79"). ScribeSearchLog-3 and SimplifierDocs reached the 5-row
  figure independently; SimplifierDocs supplied the 7-lines decomposition that makes the unit error explicit.
- **F8 (defect, one abbreviated digest).** The same bullet prints `sha256 d69349e8…77e8826`, but the
  capture's digest ends `…6779e8826`: the abbreviation dropped a `9`, and `77e8826` is **not** a substring of
  `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`. Verified by computation, not by eye:
  `d[-8:] = 779e8826`, `'77e8826' in d = False`, `'779e8826' in d = True` (R12). The row at `:58` and the
  manifest carry the full digest, so no claim rests on the abbreviation; the fix is an appended correction
  naming the correct suffix.
- **F3 (label drift, no wrong fact).** The landed anchor calls `L15472-L15475` an "exploitation-status span",
  but L15472 is `dueDate` (a deadline) and L15475 is `notes`; the exploitation-status field is L15473
  `knownRansomwareCampaignUse`. Likewise "remediation-clock span L19165-L19168" spans `dateAdded` (L19165),
  `shortDescription` (L19166) and `requiredAction` (L19167) before `dueDate` (L19168). Both are range
  locators that resolve; the labels, not the facts, are loose. ScribeSearchLog-3 read the row's own sentence
  and qualified this the other way: the sentence enumerates exactly those four fields in capture order, so the
  spans are accurate and only the grouping name "exploitation-status" starts on a deadline; a status-only span
  would be `L15473-L15474`. I accept that reading — F3 is a wording difference, not a repair request.
- **F4 (spec vs source).** The build spec's command names `https://www.cisa.gov/known-exploited-vulnerabilities.json`,
  which is **404** (V13). The landed row, manifest, entry and bullet all pin the working feed
  `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` (200, no redirect);
  ExecC2Capture confirmed all three user agents 404 on the spec path and the L1 accepted the substitution.
- **F5 (stale spec facts, all avoided in landed text).** The spec's F18 prompt says "~1,300 records" (capture:
  **1756**, V9), "BOD 22-01" as the consuming directive (current first record's `requiredAction` cites
  **BOD 26-04**; 340 records carry `BOD 22-01`, 139 carry `BOD 26-04`, zero both), and asks for a
  definitional sentence for "known exploited" (the feed has **no prose definition**; its only descriptive
  line is the title at L2 — the landed entry rejects that over-generalization at its lines 52 and 76).
- **F6 (measurement trap, reusable).** Counting `22-01` as a bare token yields **341** records; the extra one
  is `CVE-2022-0185`, whose own id string contains `22-01` inside `2022-0185`. The correct basis is the
  directive literal `BOD 22-01` → 340 rows. ScribeEntryF18 measured 340 independently; the row cites no
  directive count, so row and entry cannot diverge.
- **F7 (out of this seat's scope, observation only).** At my measurement instant
  `grep -cE '^\| F[0-9]+ \|' corpus/README.md` = **17**, i.e. the F18 frontier row was not yet in README's
  table when I measured; that admission belongs to the C2 README seat, not to this one.
- **F9 (defect in a later appended line, 2026-10-26 after this receipt's V-table).** `corpus/SOURCES.md:111`
  states the :79 bullet "is superseded by the wider draft in `.ufo/waves/round-35/wave1/ScribeSearchLog.md` §5
  (4495 bytes, sha256 `dc1a549a…`)". Two problems: (a) a wave-draft artifact in `.ufo/` is not registry
  authority and cannot supersede a registry line — only an appended registry statement can, and a
  "superseded" label there leaves the :79 defects (F2, F8) unrepaired; (b) the cited size and digest match no
  state of that file per its own author (34,565 B / `4c1ef7ae…`, then 41,362 B / `d6204728…`; the seat's own
  final cross-reference is `.ufo/waves/round-35/wave1/ScribeSearchLog.md`, 48,898 bytes / 670 lines, sha256
  `ee89a8185a9d07d271bc04962a809176adac21f942f143722cc3f81260519c63`, per its completed result — so the `:111`
  citation matches none of the three measured states and should be corrected to that final digest or replaced
  by a copied artifact). What is verifiable, I verified: `:111`'s own citation of the bullet's sha256 is
  **correct** — sha256 of `SOURCES.md` line 79
  plus a trailing newline = `f2ab0a647031489dd96f5e5fe35b20318ebae7ed9bd8cdcb6fbc51e8ff42ab54`, and the same
  line still contains `77e8826` and still says "7 SOURCES rows" (R14). `:112`'s scope correction
  (the KEV zero-hit sweep is scoped to knowledge/README/SOURCES/SKILL and excludes `corpus/lessons/`, where
  `corpus/lessons/round-22.md:91` carries the CWE Top 25 "CVEs in KEV" cell) matches my own sweep in F5/V11.
- **F10 (my own draft was too strong; corrected).** My first draft said the lane's prior KEV tokens were
  "borrowed labels, not KEV sources". That is true of the label sources but not of the corpus: `S009` (UK
  NCSC, round-24 capture) line 122 already quotes a secondhand KEV statistic — "The CISA KEV says only about
  400 new vulnerabilities were tracked as exploited, and only around 40 of those were zero-days when
  initially exploited" — and `S001` line 1082 names "CISA KEV" as a data source in prose. Measured inventory:
  35 tokens total, i.e. 33 across six round-24 captures (`S015` 27, `S008` 2, `S001`/`S009`/`S013`/`S014` 1
  each) plus 1 in `round-24/manifest.json` and 1 in `corpus/lessons/round-22.md`. Section 1b now states this
  and says the negative result is **source-level, not string-level**: the lane held a secondhand KEV number
  but no row pinned CISA's own feed — which is the gap S052 closes. Consequence for the landed bullet: its
  PRE-STATE sweep scope is `corpus/knowledge/*.md`, `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`, so it
  excludes both `corpus/lessons/` (corrected by the `:112` append) and `corpus/source-snapshots/` (not yet
  corrected anywhere) — its "0 hits" is scope-true and whole-corpus false.

---

## 5. No-harm / write scope

- Files I created or modified in the lane: this receipt only. I did not run `git add`/`commit`/`jj`, did not
  touch the fleet root, sibling lanes, `/home/vgpnk/Projects/bounties` or `shokuknow`.
- Scratch tree: `/fast/scratch/hyaku/kasegi-r35/ScribeSOURCESRow/` (captures `S052.txt`, `S052-html.txt`,
  `S052-page.txt`, base export `SOURCES.base.md`, census fixture `censusroot/`, draft `row.txt`) — removed
  before yielding; see Report R9.
- Tooling: nothing installed or upgraded. `capture-source.py`, `source-recheck.py`-adjacent reads, `curl`,
  `cksum`-family tools and the fleet `sources-census.sh` were used as checked-in.

---

## Report

Every command below ran in `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless a path says otherwise.
`S=/fast/scratch/hyaku/kasegi-r35/ScribeSOURCESRow`.

R1. Capture of the feed (my own, to derive anchors before the committed capture existed):
`python3 corpus/instruments/capture-source.py --id S052 --url https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json --out "$S/S052.txt"`
→ `S052 status=200 fetched_bytes=1807090 snapshot_bytes=1479694 sha256=d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826 utc=2026-10-26T06:33:07Z`, exit 0.
Re-run with the default `--kind html` (`$S/S052-html.txt`) → same `sha256=d69349e8…`, and
`cmp -s "$S/S052.txt" "$S/S052-html.txt"` → identical, exit 0: the capture is mode-independent for these
bytes. `wc -l -c` → `27870 1479694`.

R2. The spec's URL is dead: `curl -sSL -A '<instrument UA>' -o /dev/null -w 'status=%{http_code} bytes=%{size_download}' https://www.cisa.gov/known-exploited-vulnerabilities.json`
→ `status=404 bytes=46916`, exit 0. Same UA and curl default against the feed URL → `status=200
bytes=1807090 final=<same URL>`, exit 0.

R3. Committed bytes match mine: `sha256sum corpus/source-snapshots/round-35/S052.txt` →
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt`;
`ls -l` → `1479694` bytes. `sha256sum corpus/source-snapshots/round-35/manifest.json` →
`06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`. Both exit 0. Manifest record:
`id S052 path S052.txt sha d69349e8… url <feed URL> fetched 2026-10-26T06:32:40Z`, quotes Q1–Q5 at anchors
2, 3, 4, 15472, 19165. ExecC2Capture reported the same digest from two independent fetches (06:32:00Z,
06:32:40Z), so the digest is not a single-draw artifact.

R4. Landing check on the real tree: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` →
`52`, exit 0; same with `S052` → `1`, exit 0; `python3` cell split of `corpus/SOURCES.md:58` → `NF: 13
cells: 11`, exit 0; `test -f corpus/knowledge/cisa-kev-catalog.md` → exit 0.

R5. Census: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
→ `kasegi W04 S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across
scopes`; `kasegi W04 S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes`;
`kasegi ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`; **exit 0**. W04 S028/S029 only,
as the frozen C2 clause requires.

R6. Draft-row fixture check (isolated, in scratch): a copy of the *current-tree* `SOURCES.md` with the row
replaced by my draft row, plus a stub `corpus/knowledge/cisa-kev-catalog.md`, run as
`bash scripts/sources-census.sh validate --root "$S/censusroot" "$S/censusroot/kasegi-shokunin"` → exit 1
with `E03 S052 duplicate id`, `W04 S052 duplicate url …` and `E11` on every pre-existing used-by. The
`E03`/`W04` pair is my fixture's own artifact (it still contained the landed row at the time of the copy,
so two S052 rows existed); the `E11` block is the missing-knowledge-tree artifact of a stub lane. The row's
own shape (`NF: 13`, 11 cells, no inner `|`) is proven separately in R4/section 1a, and the real-tree census
in R5 is the authoritative verdict. This fixture run is reported because it happened, not as evidence of a
defect in the landed row.

R7. Deltas and findings evidence: `grep -c 'CVSS' corpus/source-snapshots/round-35/S052.txt` → `0`, exit 0;
`python3` key dump → 12 keys, no cvss/severity/score key, exit 0; `grep -c '^"cveID"'` → `1756`; python
`records 1756 count 1756`; `grep -n 'severity'` → two hits, both inside `notes` strings (L5135 a Grafana
advisory URL, L11629 a third-party-patching sentence), i.e. no severity *field*; `grep -c 'BOD 22-01'` on
requiredAction = 340 records, `BOD 26-04` = 139 records, both = 0, and the record behind a bare-token
`22-01` count of 341 is `CVE-2022-0185` (its id contains `2022-0185`). Exit 0 throughout.

R8. Base-commit PRE-STATE re-derivation: `git show 3266c993:corpus/SOURCES.md > "$S/SOURCES.base.md"` (exit 0);
row count `51`; `KEV` 0, `known exploited` 0, `known-exploited` 0, `BOD 22-01` 0, `BOD 26-04` 0;
`git grep -li 'cisa' 3266c993 -- corpus/knowledge` → 2 files; CISA-bearing registry rows (case-insensitive,
row lines only) → **5**, against the emitted bullet's "7". The 7 decomposes against the base blob, re-measured
without scratch (`git show 3266c993:corpus/SOURCES.md | …`): all lines with `cisa` (ci) → **7**; row lines → **5**;
non-row lines → **2** (base lines 69 and 70, the CVD and AI-validation search-log bullets); total occurrences
(`grep -o -i cisa | wc -l`) → **14**. `git grep` for `exploited vulnerabilities` → 1
file; `exploitation` → 3 knowledge files (+ `SOURCES.md`). Excluded-sibling liveness: CSV `status=200
bytes=1073722 type=text/csv`, schema `status=200 bytes=3623 type=application/json`.

R9. Scratch removal: `rm -rf -- /fast/scratch/hyaku/kasegi-r35/ScribeSOURCESRow` after this receipt was
written into the wave dir; the seat ends with no tree on disk.

R10. Digests recorded: `corpus/SOURCES.md` `510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829`;
`corpus/source-snapshots/round-35/S052.txt` `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`;
`corpus/source-snapshots/round-35/manifest.json` `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`;
`corpus/knowledge/cisa-kev-catalog.md` `da81204b3fbca378aa311406fd3a46394759967ecc3445297335a7526c573acf`;
this receipt's own sha256 is reported in the seat's yield message rather than inside the file: a file cannot
contain a stable digest of itself, and any digest embedded here would be invalidated by the edit that added it
(this line was itself edited after the first digest was taken — `1ae0b5d9…2f3a632` at 233 lines, superseded).

R11. Tooling: none installed or upgraded this seat (nothing attempted, nothing recorded).

R12. Abbreviated-digest check (F8): `D=$(sha256sum corpus/source-snapshots/round-35/S052.txt | cut -d' ' -f1)`
→ `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`; `D[-8:]` → `779e8826`;
`'77e8826' in D` → `False`; `'779e8826' in D` → `True`; `grep -o 'sha256 d69349e8[^)]*' corpus/SOURCES.md`
→ the row's full digest (first hit) and the bullet's `sha256 d69349e8…77e8826` (second hit). Exit 0 for the
Python check; the grep chain returns exit 1 only because a later `grep -c 'S117'` matched nothing.
Cross-check on an unrelated question from a peer seat, same command: `grep -cE '^\|[[:space:]]*S117[[:space:]]*\|' corpus/SOURCES.md`
→ `0` and `grep -c 'S117'` → `0` (no S117 row exists in this lane; I own no append for it and told that seat
so).

R13. Peer-reported, NOT verified by this seat (recorded so the L1 can route them): ScribeSearchLog-3 reports
(a) the CSV sibling reconciles record-for-record with the feed (`diff -q` of 1756 sorted cveIDs exit 0; CSV's
12 columns == the feed's 12 fields), (b) BOD 22-01 is revoked and superseded by BOD 26-04 per the directive's
own page, while 340 catalog records still carry the 22-01 string and 139 carry 26-04, and (c) a re-fetch is
object-identical rather than byte-identical (same catalogVersion and cveIDs; 239 records differ
whitespace-only). I verified only the parts that appear in V8/V9/V11/R7: CSV and schema liveness (V12,
`status=200`), the 340/139 row counts, `CVSS` 0 occurrences, and `severity` appearing in exactly two record
texts. The revocation claim, the record-for-record CSV diff and the 239-record whitespace drift are that
seat's measurements.

R14. Registry state at finalisation (F9): `wc -l corpus/SOURCES.md` → `112`; `sha256sum corpus/SOURCES.md` →
`0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba`; `sed -n '109,112p'` shows the three R8
lines plus the two later appends. Line-level check of the appended claim: `python3` sha256 of
`SOURCES.md` line 79 → `930274a1dfc0a7f053ee02914a4401dd274928d123d2cc056b08543e1bb4addf` without the trailing
newline and `f2ab0a647031489dd96f5e5fe35b20318ebae7ed9bd8cdcb6fbc51e8ff42ab54` with it (the value `:111`
prints, so that citation is correct); `'77e8826' in line79` → `True`, `'779e8826' in line79` → `False`,
`'7 SOURCES rows' in line79` → `True`, i.e. the append did not repair F2 or F8. Exit 0 throughout.

R15. KEV-token inventory behind F10 and section 1b: `grep -o 'KEV' <file> | wc -l` per file →
`S001` 1, `S008` 2, `S009` 1, `S013` 1, `S014` 1, `S015` 27, `round-24/manifest.json` 1,
`corpus/lessons/round-22.md` 1; summed across those eight files → `35` (33 in the six captures). Context
lines read directly: `S009:122` (the secondhand statistic quoted in F10), `S001:1082` ("such as the ISAC's
(Information Sharing and Analysis Center), CISA KEV or private"), `S013:28`/`S014:28`/`S015:28` ("Top 10 KEV
Weaknesses"), `S015:60` ("CVEs in KEV"), `S015:214` ("CVEs in KEV: 7"). All exit 0. ScribeSearchLog-3
re-derived the same per-file counts independently and its §4b credits this sweep; the source-level
conclusion is unchanged — `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` at base
`3266c993` has no KEV or BOD-bearing row (V11: `KEV 0`, `BOD 22-01 0`, `BOD 26-04 0`).
Whole-tree form of the same check at the current bytes: `grep -rl 'KEV' corpus/source-snapshots/ | sort` →
`round-24/manifest.json`, `round-24/S001.txt`, `S008.txt`, `S009.txt`, `S013.txt`, `S014.txt`, `S015.txt`,
`round-35/S052.txt`; `| wc -l` → **8** (7 pre-existing + the round-35 capture). Independently re-derived by
SimplifierDocs, which records it as the material half of F10/F-11: the landed bullet's four-surface sweep
excludes a tree where the token demonstrably exists in 8 files.
