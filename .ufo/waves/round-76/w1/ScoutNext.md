# ScoutNext — R114 distinctness subject sweep for F54 (OSV.dev API overview, S111)

Seat: ScoutNext (read-only scout). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze commit: `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e` (base `a788021675873a96e09e91aa033d8c26ac2fe212`).
Read-only seat: no lane file was edited by this seat. All measurements below were run at the freeze commit's
tree or in a scratch clone; the lane's own working tree (the L1's in-flight integration) is quoted where the
finding concerns the landing state.

**Verdict: F54's frozen ground is DISTINCT from every held row and every held knowledge entry. No OVERLAP.
One blocking defect was found and is NOT yet in the lane's committed bytes — see §6 (F54-1).**

---

## 1. Registry sweep — every row and lead naming OSV

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -n -i 'osv' corpus/SOURCES.md
```
exit 0, **11 matching lines**: 71, 86, 93, 120, 154, 170, 175, 233, 234, 270, 271.

Token census on those 11 lines: 11× `osv`, 24× `OSV` (case-insensitive; `grep -o -i 'osv' | sort | uniq -c`).
Full per-line token context: `ScoutNext-evidence/step1-osv-token-contexts.txt`; raw grep: `step1-sources-osv-grep.txt`.

| line | kind | what it names OSV | verdict |
|---|---|---|---|
| 71 | registry row **S065** | the OSV *schema* (ossf.github.io/osv-schema), `status=rejected`; its rejection cell mentions the sibling lane's `api.osv.dev/v1/vulns/CVE-2025-55305` sample record and a "flip" condition naming OSV range semantics | DISTINCT |
| 86 | registry row **S080** | the OSV *record format* spec page; scope cell excludes "the osv.dev service API" | DISTINCT |
| 93 | registry row **S086** | OpenSSF Scorecard docs; scope cell names "OSV-service-backed vulnerability detection" (a consumer, not the OSV project) | DISTINCT |
| 120 | registry row **S108** | OSV.dev `POST /v1/query` one-endpoint contract; scope cell excludes "the overview page", "the other endpoints", and "any rate-limit or API-key statement" | DISTINCT |
| 154 | search log | round-46 sweep note: S065/S068 rejections | not ground |
| 170 | search log | round-70 note: "the OSV-format sentence does not carry the OSV schema's fields, which stay with S080" | not ground |
| **175** | **Leads bullet** | the **OSV.dev overview page** — "lead, not evidence, not a row"; quotes both "Currently there are no limits on the API." and the 32 MiB sentence, and says "**Neither statement is admitted ground**" | DISTINCT (lead, explicitly not admitted) |
| 233, 234 | registry-changes log | round-54 S086 add; mentions the OSV entry's foundation naming | not ground |
| 270, 271 | registry-changes log | round-73 S108 add; round-74 S109 add + "OSV overview page and the NDSS paper are added as leads only (no row, no evidence)" | not ground |

Registry-section rows naming OSV = **4** (`grep -c` over the Registry section lines 3–123 → 4, exit 0; row ids
`| S065 | S080 | S086 | S108`). The spec's expectation of "S080, S108, and the overview-page lead bullet" is a
subset: **S065 (rejected schema row) and S086 (Scorecard row) also name OSV** and are swept below.

`grep -c '^| S111' corpus/SOURCES.md` → 0, exit 1 (S111 not yet a row at the freeze; it is now a row in the L1's
working tree). Registry rows at the freeze: `grep -c '^| S[0-9]'` → 110.

**F54 vs S065 (rejected).** S065's subject is the interchange *format* document; its own rejection cell names
`affected[].ranges[].events` / `database_specific extracted_events` as the flip condition. It states no request
type, no endpoint and no limit. The rejected row also excludes the service API by subject. DISTINCT.

**F54 vs S080 (record format, F31).** S080's scope cell (line 86, field 6) reads: "…**not the osv.dev service
API**, not the JSON Schema validation artifact…". PROVINCE.md:178 repeats it: "scope limit: the format's
range/event semantics only — the osv.dev service API … stay out". F54's ground is the request surface and the
page's limit answers, inside the explicitly vacated scope. DISTINCT — and the lane had already carved the gap
open before F54 was proposed.

**F54 vs S086 (Scorecard, F35).** S086 names OSV only as the service one Scorecard check consumes
(`osv-scanner.toml` suppression, S086.txt:710/718). Its scope cell excludes "the OSV data format (F31/S080)". It
holds no OSV API surface and no OSV limit statement. DISTINCT.

**F54 vs S108 (POST /v1/query, F51).** S108's scope cell excludes "the overview page, the other endpoints, and
any rate-limit or API-key statement (the page has none)". F54 is precisely that excluded gap: the overview, the
other endpoints, the rate-limit sentence. The two rows are complementary, not overlapping. DISTINCT.

**F54 vs the lead bullet (line 175).** The lead bullet states the page has "no limits" and the 32 MiB sentence,
but records them as **not admitted ground** — "Neither statement is admitted ground; a row needs its own capture
and manifest". A lead is not held ground, so it cannot be an OVERLAP; it is the pointer F54 discharges. This is
the r74/r73 disposition chain: `corpus/lessons/round-73.md:25`, `round-74.md:13`, `round-75.md:12` each rejected
the overview page as a row for want of a capture/manifest. S111 supplies exactly that. DISTINCT.

---

## 2. Knowledge sweep — every entry naming OSV

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -ril -i 'osv' corpus/knowledge/
```
exit 0, **5 of 91 files**:

```
corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md      (F52/S109)  1 line
corpus/knowledge/github-advisory-database-curation-semantics.md (F47/S105) 2 lines
corpus/knowledge/openssf-scorecard-checks.md                     (F35/S086) 12 lines
corpus/knowledge/osv-affected-range-events.md                     (F31/S080) 13 lines
corpus/knowledge/osv-post-v1-query-contract.md                   (F51/S108) 9 lines
```
(per-file `grep -c` counts: 1 / 2 / 12 / 13 / 9; files: `step2-knowledge-osv-files.txt`.)

F53 (`fuzzilli-ndss2023-jit-fuzzing-paper.md`): `grep -c -i 'osv'` → **0**, exit 1 — it names OSV not at all, so
it is not a subject-sweep hit.

| entry | what it says about OSV | verdict |
|---|---|---|
| **F51** `osv-post-v1-query-contract.md` | the `POST /v1/query` contract; §Limits :71-75 | DISTINCT — see below |
| **F31** `osv-affected-range-events.md` | the record format's `affected[].ranges[].events` timeline; :18 "osv.dev's service does with it, is outside these bytes" | DISTINCT |
| **F35** `openssf-scorecard-checks.md` | Scorecard's Vulnerabilities check consumes the OSV service; :77 "F31/S080 is the OSV data format; Q10 pins only that Scorecard consumes the OSV service" | DISTINCT |
| **F47** `github-advisory-database-curation-semantics.md` | :75 the GitHub Advisory DB's "Open Source Vulnerability (OSV) format" sentence; :120 "The OSV-format statement is a format fact; the OSV schema's own fields stay with S080" | DISTINCT |
| **F52** `fuzzilli-js-engine-fuzzing-framework.md` | :79 "F31 / S080 (OSV format ranges): unrelated. Not used here." | DISTINCT |

**F51 is the only genuine near-neighbour and it is still DISTINCT.** Its own text disclaims F54's ground three
ways, and the disclaims are the strongest possible distinctness evidence:

- `osv-post-v1-query-contract.md:73` — "the overview page at the API root (`api/`). **S108 is the query page only;
  the overview's own statements are not in this capture.**"
- `osv-post-v1-query-contract.md:71` — "rate limits or quotas on `POST /v1/query`. The capture has no sentence on
  either" — i.e. F51 explicitly leaves the rate-limit question open.
- `osv-post-v1-query-contract.md:75` — "the other endpoints in the page's navigation (POST /v1/querybatch,
  GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). **They are listed, not described.**"

F51 holds the *path strings* (as navigation names, explicitly "not described"); it holds **none** of F54's ground
clauses. F54's frozen ground is the six-request *surface* — the six one-line semantics (S111.txt:29-34), the
API-1.0/OpenAPI availability (S111.txt:21-22), and the rate-limit sentence (S111.txt:36). See §4 for the
per-clause absence proof.

**F47** is worth one more line because its subject is the *same organisation* (GitHub's advisory DB describing
OSV) — R114's subject sweep is about the organisation, not the string. Its two hits are a format sentence and an
explicit hand-off to S080; no request surface, no limit. DISTINCT.

---

## 3. Per-clause absence proof (the F54 ground clauses themselves)

Every F54 ground sentence was searched verbatim across all 91 knowledge files
(`grep -c -F` per file; counts in `step3-ground-sentence-overlap.txt`). **All zero:**

| F54 ground clause | capture line | files in `corpus/knowledge/*.md` holding it |
|---|---|---|
| "API (1.0)" | 21 | **0** |
| "Download the OpenAPI specification" | 22 | **0** |
| "There are six different types of requests that can be made of the API." | 28 | **0** |
| "Query vulnerabilities for a particular project at a given commit hash or version." | 29 | **0** |
| "Batched query vulnerabilities for given package versions and commit hashes." | 30 | **0** |
| "Return a Vulnerability object for a given OSV ID." | 31 | **0** |
| "Return a list of probable versions of a specified C/C++ project. (Experimental)" | 32 | **0** |
| "Retrieve records failing import-time quality checks, by record source (Experimental)" | 33 | **0** |
| "Map Ubuntu binary package names to their corresponding source package names. (Experimental)" | 34 | **0** |
| "Is the API rate limited?" | 35 | **0** |
| "Currently there are no limits on the API." | 36 | **0** |
| "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2." | 38 | **0** (held from S108 — cross-referenced, not claimed; §5) |

"API (1.0)" appears nowhere in the knowledge corpus, so even the API-version clause — the shortest, most
collision-prone string — is unheld. Supporting sweeps: `grep -n -i 'experimental' corpus/knowledge/*.md` →
3 hits, all irrelevant (`cve-bench-agent-exploitation-benchmark.md:80` "the experimental configuration";
`project-zero-big-sleep-...md:28` "CPU-hour unit"; F51:75); `grep -n -i '\bsix\b'` → no OSV hit;
`grep -n -i 'openapi' corpus/knowledge/*.md` → 4 hits, all in `cve-services-publication-api.md` (the CVE
Program's own OpenAPI document — a different organisation, tier-B-adjacent, and it is the CVE Services API, not
OSV.dev's) (`step4c-experimental-sweep.txt`).

---

## 4. Negative sweep — the seven F54 strings across `corpus/knowledge/*.md`

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && for pat in 'querybatch' 'vulns/{id}' 'determineversion' \
  'importfindings' 'binary-to-source' 'no limits on the API' 'OpenAPI specification'; do
  grep -c -i -F "$pat" corpus/knowledge/*.md; done
```
Raw output: `step4-negative-sweep.txt`; broadened variants: `step4-negative-sweep-broadened.txt`.

| string | files with a hit (of 91) | raw `grep -c` exit | finding |
|---|---|---|---|
| `querybatch` | **1** | 0 | `osv-post-v1-query-contract.md:75` — F51's Limits bullet. **Does not contradict admission.** It names the path in a sentence that explicitly excludes it ("They are listed, not described"). No description, no semantics, no rate-limit statement. |
| `vulns/{id}` | **1** | 0 | same line, same bullet, same verdict |
| `determineversion` | **0** | 1 | unheld — the ground is unheld |
| `importfindings` | **0** | 1 | unheld |
| `binary-to-source` | **0** | 1 | unheld |
| `no limits on the API` | **0** | 1 | unheld — the rate-limit sentence is held nowhere |
| `OpenAPI specification` | **0** | 1 | unheld |

So: **five of seven strings are zero-hit** (ground unheld), and **two hit one line each** — F51's exclusion
bullet. Neither hit contradicts admission; both are the lane *declining* to describe those endpoints, which is
the opposite of an overlap. The one place the strings do appear as held ground is `corpus/SOURCES.md:175`
(the lead bullet, `"Currently there are no limits on the API."`), and that bullet states in its own text that
"Neither statement is admitted ground".

Broadened sweeps (same command shape, wider strings) confirm the same picture: `no limits` → 0 hits;
`six different types` / `types of requests` / `API (1.0)` / `API 1.0` / `rate limited` → 0 hits each;
`experimental` → 3 irrelevant hits; `v1experimental` → 0 hits; `OSV.dev API` / `OSV API` → 0 hits.

**Cross-organisation check.** `grep -n -i 'osv\.dev'` over `corpus/knowledge/*.md` → 7 hits, all inside F51, F31
and F35 (cited URLs, none an OSV API-overview claim). `grep -n -i 'google\.github\.io' corpus/knowledge/*.md` →
**1 hit only**: F51's own source line (`osv-post-v1-query-contract.md:3`). No held entry cites
`https://google.github.io/osv.dev/api/`. `grep -rn -i 'google\.github\.io/osv\.dev/api'` across the fleet root
(24 lanes) → only `kasegi-shokunin/corpus/SOURCES.md` (the lead bullet). **No sibling lane holds the OSV.dev API
overview**, so the R114 subject sweep finds no cross-lane overlap either. The nearest sibling ground is
`kaidoku-shokunin` row S015 (`api.osv.dev/v1/vulns/CVE-2025-55305`) — a single record instance, the opposite
subject from an API surface, and it is a different lane.

---

## 5. Cross-reference integrity (B6's "held ground" clause)

B6 requires that the response-size clauses at capture line 38 be **cross-referenced as already-held from S108**
and not claimed as new ground. Verified:

- S111.txt:38 is byte-identical to the prefix of S108.txt:148 (`'The API has a response size limit of 32MiB when
  using HTTP/1.1. There is no limit when using HTTP/2.' in S108:148` → True).
- S108.txt:148 = "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using
  HTTP/2. We recommend using HTTP/2 for queries that may result in large responses."
- round-73 manifest Q27 (`size-http1`) and Q28 (`size-http2`) both anchor 148; Q29 (`http2-recommend`) anchors 148
  too. F51 Claim 6 quotes that line.
- S111.txt:39 is the HTTP/2 recommendation **with an extra parenthetical** ("(e.g. big OSV Linux queries)") that
  S108:148 does not have → `'S111:39 in S108:148'` is False. So line 39 is *not* byte-identical ground; it is
  captured and pinned (manifest Q13) but the recommendation clause itself is already held from S108 Q29. The
  drafted entry correctly treats line 39 as "in the capture and manifest (Q13) but … not claimed here".

**Line 21 (`API (1.0)`) is the one manifest-anchor problem — see §6.**

---

## 6. FINDINGS

### F54-1 — BLOCKING for B5 — the frozen manifest's Q01 quote is 9 characters and `source-recheck.py` refuses it

The frozen manifest pins `{"id": "Q01-api-version", "quote": "API (1.0)", "anchor": 21}`. `source-recheck.py`
enforces `MIN_QUOTE_CHARS = 12` ("a shorter 'quote' matches any capture"), so it rejects the whole record:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111
```
→ `S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`, **exit 2**. Same with no `--source`
flag. **B5 ("reports sha256 OK and all 13 quotes anchor-located, exit 0") is FALSE on the frozen manifest bytes.**
Every other round's manifest passes: a loop over all 49 `corpus/source-snapshots/*/manifest.json` gives
**exit 0 for all 48 others and exit 2 for round-76 only** (`step4-final` block in `final-evidence-summary.txt`).

This is not cosmetic. The L1's in-flight manifest repair (visible in the working tree, `git diff
corpus/source-snapshots/round-76/manifest.json`) replaces Q01 with `"How does the API work?"` at **anchor 27**,
which fixes the exit code but moves the anchor:

| | frozen `located_anchors` (claims.json) | L1's working-tree manifest |
|---|---|---|
| anchors | 21, 22, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39 | 22, **27**, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39 |
| Q01 quote | `API (1.0)` | `How does the API work?` |

**Anchor 21 is dropped and 27 is added.** claims.json's C2 `located_anchors` names line 21 explicitly
("S111.txt lines 21, 22, 28, …, 38, 39 (manifest Q01-Q13)"), and the *knowledge entry* claims
"The page's heading reads \"API (1.0)\" (S111.txt:21)" — a line that, after the repair, no manifest quote
covers. The entry also never cites line 27 (`grep -c 'txt:27'` in the applied entry → 0, exit 1). So the repair
trades a defect the entry *does* rely on for one it does not.

**A better repair, verified end-to-end in a scratch clone:** keep the anchor at 21 and lengthen the quote so it
carries the API-version heading *and* the OpenAPI line, which is already the subject of Q02:

```json
{"id": "Q01-api-version", "quote": "API (1.0)\nDownload the OpenAPI specification", "anchor": 21}
```

Measured on a scratch copy of the frozen manifest:
- normalized length 44 ≥ 12 → passes the gate;
- `source-recheck.py … --source S111` → **13/13 OK, every line `anchor=N-ok`, exit 0**;
- the resulting anchor set is **exactly** claims.json's `located_anchors` — 21, 22, 28–36, 38, 39 — verified by
  set comparison (`EXACT MATCH: True`);
- the knowledge entry's `API (1.0)` (S111.txt:21) claim stays manifest-backed.

Multi-line quotes are established lane practice, so the newline form is not novel: `round-29/manifest.json`
S044 Q4 and S045 Q1/Q3/Q4, `round-50/manifest.json` S080 Q7, `round-62/manifest.json` S095 Q06/Q07 all use
`\n`-joined quotes.

This is a finding for the L1, not an edit by this seat (corpus/source-snapshots/* is an L1 integration surface
and the manifest is already under L1 amendment).

### F54-2 — the L1's manifest repair is already applied in the working tree and B5 now passes

Working tree (L1 state): `source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111`
→ `S111:sha256 OK`, Q01-api-heading-question OK anchor=27-ok, Q02…Q13 all OK anchor=N-ok, **exit 0**. B5's
*letter* ("sha256 OK and all 13 quotes anchor-located, exit 0") is satisfied. The open question raised by F54-1
is only whether the anchor move 21→27 is acceptable against the frozen `located_anchors` and against the
entry's own S111.txt:21 claim.

### F54-3 — the applied entry's `api.osv.dev` cross-reference is unsupported

`corpus/knowledge/osv-api-surface-and-limits.md:30` (L1 working tree) asserts: "Those six path strings are
already held ground: F51 records the other five as navigation names in its Limits bullet
(`osv-post-v1-query-contract.md:75`, S108.txt:5-9), **and `https://api.osv.dev/v1/vulns/<ID>` is held from
S080**."

Measured:
- `grep -c 'api\.osv\.dev' corpus/knowledge/osv-affected-range-events.md` → **0**, exit 1 (F31's entry never
  names the URL).
- `grep -c 'Formatted URL' corpus/knowledge/osv-affected-range-events.md` → **0**, exit 1.
- The URL *is* in the S080 **capture** — `grep -c -i 'api\.osv\.dev' corpus/source-snapshots/round-50/S080.txt`
  → 8, e.g. `S080.txt:185` "OSV Formatted URL: https://api.osv.dev/v1/vulns/<ID>" — but **no S080 manifest quote
  pins it** (a scan of `round-50/manifest.json` for quotes containing `api.osv.dev` or `v1/vulns` returns none).

So the URL is in S080's *bytes*, not in S080's *held ground* as the entry words it. The claim as written
("is held from S080") overstates what the lane holds. Either the capture line is cited as a capture location
rather than as held ground, or the sentence is dropped. This matters for B6's distinctness clause: an entry must
not cite as already-held something no held entry or pinned quote carries.

### F54-4 — the applied entry's path-paired-reading paragraph lost its cross-reference in the L1 edit

The wave draft `.ufo/waves/round-76/w1/f54-entry-draft.md` §Claim 2 said the nav list is at S111.txt:4-9 and
"the page repeats the same six paths at S111.txt:41-47". The applied entry (`:30`) keeps "S111.txt:4-9" and
"S111.txt:41-47". Measured: TOC lines 42-47 are the six paths; **line 41 is "API Quickstart"** and line 40 is
"Table of contents". So "41-47" over-runs by one line (harmless but imprecise — the accurate range is 42-47).
Minor.

### F54-5 — the applied entry cites `SOURCES.md:175` for the lead bullet, but the L1 has deleted that bullet

The L1's `git diff corpus/SOURCES.md` **removes** the OSV lead bullet (the r74 precedent — `git show dca80cf`
for the r74 landing — **kept** the Fuzzilli lead line byte-identical as history and added a note in
"Registry changes"; the r76 edit deletes the bullet outright). The applied entry `:72` still says "the lead-only
note for this page (`SOURCES.md:175`)" and "The lead note at SOURCES.md:175 is superseded by this row at
integration". After the deletion, `SOURCES.md:175` is now the *Fuzzilli* lead (`grep -c 'OSV.dev overview page'
corpus/SOURCES.md` → 0, exit 1), so the entry's own distinctness paragraph cites a line that no longer holds the
thing it names.

Two options for the L1: (a) keep the lead bullet byte-identical as history (r74 precedent) and point the entry
at it, or (b) delete the bullet as done and retarget the entry's citation to the Registry-changes note that
records the retirement. Either way the entry's `SOURCES.md:175` pointer must be made true.

Note B1 says "exactly one added S-row (S111) and zero removed rows" — a lead bullet is not a registry row, so the
deletion does not violate B1's letter; but `grep -c '^| S[0-9]' corpus/SOURCES.md` = 110 at freeze → 111 after
the add, with zero removed rows. B1 holds.

### F54-6 — F51's rate-limit boundary sentence is now stale and the L1 has routed the correction to round 77

`corpus/README.md:1159` (F51's coverage-map row) still instructs: "the page states no rate limit and no API-key
rule, **so a reader must not supply either from the OSV overview page**", and
`corpus/knowledge/osv-post-v1-query-contract.md:71` says the S108 capture "has no sentence on either". F54 admits
exactly that sentence from the overview page. The L1's `git diff corpus/README.md` states the F51 boundary is
"superseded for the rate-limit question only by a correction routed to round 77; F51 is not edited" — i.e. the
landing knowingly leaves a lane instruction that tells the reader not to use the newly admitted ground, and
defers it. This is a live correctness defect in the landed tree, not a scoring nicety: a reader following
`README.md:1159` is told to reject F54's rate-limit clause. Two coherent resolutions, both the L1's call:
amend F51's row + entry line 71 in the same landing (the F51 text itself is a *scope* statement about S108's
capture and stays true — only the "a reader must not supply either from the OSV overview page" instruction
becomes wrong), or keep the deferral but make the landing state explicitly self-consistent. Flagging only.

### F54-7 — no subject-sweep tool is missing

`grep -n -i 'osv' corpus/QUALITY.md` → 0 hits (exit 1); `grep -n -i 'osv' SKILL.md` → 0 hits (exit 1). Neither
surface constrains F54's admission. `corpus/README.md`'s F-rows naming OSV are F31, F35 and F51 only
(`grep -o 'F[0-9][0-9]'` over OSV lines → F01 F17 F18 F21 F23 F24 F25 F31 F35 F50 F51 — the non-OSV ones are
coincidental matches inside prose, e.g. "F21" inside "F21 (the CVE JSON record format…)"); F54 is absent from
README at the freeze (`grep -c 'F54' corpus/README.md` → 0, exit 1) and present in the L1's working tree.
`grep -rn 'F54' corpus/` at the freeze → 1 hit only, the round-76 manifest's own `note` field.

---

## 7. Command ledger (every number above, with exit code)

| # | command (cwd = lane root unless stated) | result | exit |
|---|---|---|---|
| 1 | `grep -n -i 'osv' corpus/SOURCES.md` | 11 lines: 71 86 93 120 154 170 175 233 234 270 271 | 0 |
| 2 | `sed -n '3,123p' corpus/SOURCES.md \| grep -c -i 'osv'` | 4 (S065 S080 S086 S108) | 0 |
| 3 | `grep -c '^| S111' corpus/SOURCES.md` (freeze tree) | 0 | 1 |
| 4 | `grep -c '^| S[0-9]' corpus/SOURCES.md` (freeze) | 110 | 0 |
| 5 | `grep -ril -i 'osv' corpus/knowledge/` | 5 files (listed in §2) | 0 |
| 6 | `grep -c -i 'osv' corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md` | 0 | 1 |
| 7 | 11× `grep -c -F '<F54 ground sentence>' corpus/knowledge/*.md` | all 0 files | 1 each |
| 8 | `grep -n -i -E 'querybatch\|vulns/{id}' corpus/knowledge/osv-post-v1-query-contract.md` | :75 (one line) | 0 |
| 9 | `grep -c -i -F 'determineversion'\|'importfindings'\|'binary-to-source'\|'no limits on the API'\|'OpenAPI specification' corpus/knowledge/*.md` | 0 files each | 1 each |
| 10 | `grep -n -i 'google\.github\.io' corpus/knowledge/*.md` | 1 hit (F51:3) | 0 |
| 11 | `grep -rn -i 'google\.github\.io/osv\.dev/api' --include='SOURCES.md' .` (fleet root) | only kasegi | 0 |
| 12 | `sha256sum corpus/source-snapshots/round-76/S111.txt` | 6f92e5b7…581ab (matches claims.json) | 0 |
| 13 | `cmp -s corpus/source-snapshots/round-76/S111.txt .ufo/waves/round-74/w1/ScoutSurface-osv-api-overview-snapshot.txt` | identical (exit 0 ⇒ round-74 lead-only fetch == round-76 capture, byte for byte) | 0 |
| 14 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111` (**frozen** manifest) | `reason=quote-too-short-to-be-evidence` | **2** |
| 15 | same, **L1 working-tree** manifest | sha256 OK, 13/13 OK | 0 |
| 16 | `python3 corpus/instruments/source-recheck.py --manifest <scratch copy with Q01="API (1.0)\nDownload the OpenAPI specification", anchor 21> --source S111` | sha256 OK, 13/13 OK, all `anchor=N-ok` | 0 |
| 17 | loop over all 49 `corpus/source-snapshots/*/manifest.json` | 48× exit 0, round-76 exit 2 | — |
| 18 | `python3 -B corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` from a foreign cwd, L1 working tree | `entries=92 noprefix=0 exit2_foreign=0 exit0_foreign=70 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` + `RECHECK-CWD-RESULT conformant` | 0 |
| 19 | same, on a C1-only tree (freeze SOURCES + freeze manifest, no F54 entry) | `entries=91 … exit0_foreign=69 … conformant` — byte-identical to the base receipt's `RECHECK-CWD` line except the expected C2 drift | 0 |
| 20 | `diff <base receipt RECHECK-CWD line> <L1 census line>` | differs only by entries 91→92 and exit0_foreign 69→70 (the drift A2 predicts) | 1 |
| 21 | `python3 corpus/instruments/frontier-recheck-count.py` (L1 tree) | `FRONTIER-CENSUS rows=54 admitted=54 closed=54 problem-rows=0 registry=111`, `FRONTIER-PASS F54 ids=S111`, `entries=57 pass=57` | 0 |
| 22 | `python3 corpus/instruments/capture-binding-check.py` (L1 tree, S111 row present) | `records=90 bound=90 unbound=0` | 0 |
| 23 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok …`, 6× W04, 0× E0x | 0 |
| 24 | `grep -c 'api\.osv\.dev' corpus/knowledge/osv-affected-range-events.md` | 0 | 1 |
| 25 | `grep -c -i 'api\.osv\.dev' corpus/source-snapshots/round-50/S080.txt` | 8 | 0 |
| 26 | `grep -n 'SOURCES.md:175' corpus/knowledge/osv-api-surface-and-limits.md` | 1 (stale pointer, F54-5) | 0 |
| 27 | `grep -c 'OSV.dev overview page' corpus/SOURCES.md` (L1 tree) | 0 (bullet deleted) | 1 |
| 28 | `grep -n 'bash\|subprocess\.run\|mkdtemp' corpus/instruments/recheck-cwd-census.py` | exactly one `subprocess.run(["bash","-c",value])` at :70, one `"-c"` at :70, `mkdtemp` at :65 and :136 only | 0 |

Scratch: `/fast/scratch/hyaku/kasegi-r76/ScoutNext/` (4 read-only clones of the lane, all outside the lane tree;
removed on exit). Evidence copied to `.ufo/waves/round-76/w1/ScoutNext-evidence/` before cleanup.

---

## 8. Summary for the L1

1. **R114 subject sweep: F54 is DISTINCT.** Every registry row (S065, S080, S086, S108) and every one of the five
   OSV-naming knowledge entries either disclaims F54's subject or covers a different subject; the two near
   neighbours (S080/F31 and S108/F51) each carry an explicit scope limit that vacates exactly the ground F54
   fills. All eleven F54 ground sentences are held by **zero** of the 91 knowledge entries; five of the seven
   F54 strings are zero-hit corpus-wide, and the two that hit do so in the lane's own *exclusion* bullet.
   No sibling lane holds the overview page.
2. **F54-1 (blocking for B5 as frozen):** the frozen Q01 quote `API (1.0)` is 9 chars, below
   `source-recheck.py`'s `MIN_QUOTE_CHARS=12`, so the frozen manifest makes B5 exit 2. The L1's working-tree
   repair (quote → "How does the API work?", anchor 21 → 27) restores exit 0 but breaks the frozen
   `located_anchors` set and orphans the entry's own `S111.txt:21` claim. The verified alternative that satisfies
   both is Q01 = `"API (1.0)\nDownload the OpenAPI specification"` at **anchor 21** (§6, command 16).
3. **F54-3:** the applied entry's "`https://api.osv.dev/v1/vulns/<ID>` is held from S080" is not supported — the
   URL is in S080's capture (8 hits) but in no S080 knowledge entry and no S080 manifest quote.
4. **F54-5:** the applied entry still cites `SOURCES.md:175` for the lead bullet the L1 deleted; line 175 is now
   the Fuzzilli lead. Either keep the bullet as history (r74 precedent) or retarget the citation.
5. **F54-6:** F51's README/entry instruction "a reader must not supply [a rate limit] from the OSV overview
   page" is now contradicted by F54's admission; the L1 has deferred the correction to round 77, which leaves the
   landed tree self-contradictory on the reader's instructions.

Tooling: no tool was installed or upgraded by this seat (no pacman, no uv, no downloads). `grep`, `git`,
`sed`, `python3`, `sha256sum`, `cmp`, `bash` only.
