# ScoutPerish — round-83 w1 recon for C2's source frontier

Seat: ScoutPerish (leaf, no delegation). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scratch root used: `/fast/scratch/hyaku/kasegi-r83/ScoutPerish` (deleted at yield).
All fetches were read-only GETs; no lane file, corpus file, instrument, registry or git state was written.
Receipts: `.ufo/waves/round-83/w1/ScoutPerish-receipts/` (listed at the end).

---

## 1 — Public copy of "Managing the Perishability of OSV Records": **none found** (searched, exhaustively)

The companion named at `corpus/source-snapshots/round-82/S116.txt:27` has **no public copy** in the OSV.dev
project or anywhere else I could reach. Round-83's own record says the same
(`corpus/SOURCES.md:284`, `corpus/README.md:1271`: "stays unopened: no public copy found this round") —
this recon confirms it from more directions and can be cited as a stronger negative.

The only surviving trace is the forward reference itself. From
`https://raw.githubusercontent.com/google/osv.dev/master/docs/data_quality.md` line 13 (HTTP 200, 2026-11-06T22:09:38Z):

> "This does not discuss the problem of record bit rot over time, after initial successful import. The problem of continuous revalidation and treatment of records that have been successfully imported will be dealt with separately in the companion to this, *Managing the Perishability of OSV Records*."

(≤25-word located quote, verbatim from the upstream markdown; identical text to `S116.txt:27`.)

### 1a — Every URL opened, with status and access time

Access times are UTC 2026-11-06; full records in `ScoutPerish-receipts/url-access-times.json`
and `url-probe.json`.

| URL | HTTP | accessed (UTC) | note |
|---|---|---|---|
| https://google.github.io/osv.dev/faq/ | 200 | 22:09:38 | 34,381 B raw; re-capture byte-identical to frozen S117 (§3) |
| https://google.github.io/osv.dev/data_quality.html | 200 | 22:08:30 | rendered F58 source |
| https://raw.githubusercontent.com/google/osv.dev/master/docs/data_quality.md | 200 | 22:09:38 | the forward reference, md line 13 |
| https://raw.githubusercontent.com/google/osv.dev/master/docs/faq.md | 200 | 22:09:38 | upstream source of S117 |
| https://raw.githubusercontent.com/google/osv.dev/master/docs/data.md | 200 | 22:08:0x | upstream source of the /data/ page |
| https://api.github.com/repos/google/osv.dev/contents/docs?ref=master | 200 | 22:09:39 | docs/ tree, 21 entries |
| https://api.github.com/repos/google/osv.dev/git/trees/master?recursive=1 | 200 | 22:09:38 | full repo tree, 1,760 paths |
| https://api.github.com/search/issues?q=repo:google/osv.dev+perish | 200 | 22:09:39 | total_count 0 |
| https://api.github.com/search/commits?q=perishability+repo:google/osv.dev | 200 | 22:09:39 | total_count 0 |
| https://github.com/google/osv.dev/issues/2101 | 200 | 22:09:39 | issue page |
| https://github.com/google/osv.dev/issues/2294 | 200 | 22:09:40 | issue page |
| https://api.github.com/repos/google/osv.dev/issues/2101 | 200 | 22:09:41 | body JSON |
| https://api.github.com/repos/google/osv.dev/issues/2294 | 200 | 22:09:41 | body JSON |
| https://osv.dev/blog/posts/announcing-data-quality-initiatives/ | 200 | 22:09:42 | see §4 lead 1 |
| https://google.github.io/osv.dev/data/ | 200 | 22:09:42 | see §4 lead 2 |
| https://google.github.io/osv.dev/assets/js/search-data.json | 200 | 22:09:42 | site-wide search index (73 KB) |
| https://google.github.io/osv.dev/perishability.html | **404** | 22:09:42 | candidate path |
| https://raw.githubusercontent.com/google/osv.dev/master/docs/perishability.md | **404** | 22:09:42 | candidate path |
| https://google.github.io/osv.dev/revalidation.html | **404** | 22:08:26 | candidate path |
| https://google.github.io/osv.dev/perishability/ | **404** | 22:04:xx | candidate path |
| https://google.github.io/osv.dev/data_quality/perishability.html | **404** | 22:04:xx | candidate path |
| https://github.com/google/osv.dev/blob/master/docs/perishability.md | **404** | 22:04:xx | candidate path |
| https://github.com/google/osv.dev/issues/829 | 200 | 22:09:41 | PR that removed the Git deletion behaviour |
| https://github.com/google/osv.dev/pull/2193 | 200 | 22:08:27 | PR that added the F58 doc ("Part of #2186") |
| https://api.github.com/repos/google/osv.dev/issues/2186, 2187, 2188, 2189, 2190 | 200 | 22:07–22:08 | quality-bar issue family (§1c) |
| https://api.github.com/repos/google/osv.dev/issues/2030 | 200 | 22:10:0x | GCS deletion handling PR |

### 1b — Search surfaces checked and their result

| surface | result |
|---|---|
| `google/osv.dev` full repo tree (1,760 paths) | no path matching perish/revalid/stale/bitrot/lifecycle; only `docs/data_quality.md`, `docs/faq.md`, `.github/workflows/staleness.yml` |
| `google/osv.dev` `docs/` tree (21 entries) | `data_quality.md`, `faq.md`, `data.md`, `new_source.md`, `rest-api.md`, `third-party.md`, `api/`, `contributing/` — no perishability file |
| all 7 non-master branches' `docs/` trees (`jess-lowe-patch-1`, `promote_prefix_ignore_prod`, `reducable-zip`, `temporary_modifications_for_mass_reimport`, `update-pr-permissions`, `upgrade-schema`) | same `.md` set, no perishability file |
| GitHub issue search `repo:google/osv.dev perish` / `revalidat` / `"bit rot"` | total_count 0 each |
| GitHub commit search `perishability repo:google/osv.dev` | total_count 0 |
| `google.github.io/osv.dev` site-wide search index (`assets/js/search-data.json`, 82 indexed sections over 17 pages) | exactly **one** hit for "Perishability" — the data_quality "Purpose" section quoting the same forward reference. No page of the site is about it. |
| `ossf/osv-schema` tree (169 paths, incl. `tools/osv-linter/`) | no perishability/revalidation doc |
| `google/osv-scanner` tree (1,412 paths) | none |
| 3 web searches for the exact title | no published copy; all results are the two known pages (data_quality, faq) |

### 1c — What *is* published in the same program (for the record)

`docs/data_quality.md` was added by PR #2193 ("Part of #2186"); `docs/data_quality.md` has only **2**
commits ever (8c2b48a 2024-07-15, 435d4e5c 2025-03-21 "include upstream"). The companion was never
created. The OSV project's own tracker holds the program it stands in for: issues
**#2186** (definition of the import bar, closed), **#2187** (linting tooling, open),
**#2188** ("The minimum quality bar is sustainably enforced by OSV.dev — Records below the quality bar are
not imported into or exported by OSV.dev", open), **#2189** (machine-readable import findings, closed
2025-05-21 — this is the ground F57 already holds), **#2190** (downstream users reasoning about records
absent from OSV.dev because of the quality bar, open).

### 1d — Statement *about* the document found in a live issue (≤25 words)

From issue #2101 body (HTTP 200, 2026-11-06T22:09:41Z), quoting the state of the "deleted upstream" rule:

> "records now showing as deleted are not marked as withdrawn in OSV.dev"

### 1e — Tool availability limits (recorded, not claimed as absence)

- `https://api.github.com/search/code?q=Perishability+repo:google/osv.dev` → **HTTP 401
  "Requires authentication"**. Code-level search was therefore **not** performed; the negative rests on
  the full recursive tree + commit search + site search index, not on code search.
- `https://grep.app/api/search?q=Perishability` → HTTP 429 (Vercel security checkpoint). Unavailable.
- Wayback Machine (`web.archive.org` CDX, availability API) → connection timeouts (25 s–136 s,
  `curl (28)`), and `archive.org/wayback/available` returned HTTP 429 "Too Many Requests" from
  this host. **Archive history was not checked**; an archived copy of a since-removed page cannot be
  excluded from this seat's evidence.
- `timetravel.mementoweb.org` → DNS resolution failed.

**Confidence:** high that no *currently published* copy exists in the OSV.dev project, the ossf
schema project, osv-scanner, or the OSV.dev website (tree-level, commit-level and site-index-level
negative, plus web search). **Unresolved:** pre-2026 archived or private copies (Wayback/CDX
unreachable from this host) and code-search-level occurrences (401).

---

## 2 — Is the S117 FAQ ground held by any sibling lane? **No.**

Command run (read-only, exactly as the item specified):
`grep -rl 'osv.dev/faq' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md 2>/dev/null`

- **Hits: `kasegi-shokunin/corpus/SOURCES.md` only (1 hit).** No sibling lane's `SOURCES.md` holds it.

Widened checks (read-only greps only, no sibling tree written):

| check | result |
|---|---|
| `grep -rl 'osv\.dev/faq' */corpus` (all lanes, .md/.txt/.json) | kasegi only |
| `grep -rl 'google\.github\.io/osv\.dev' */corpus` | kasegi only — `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/osv-faq-post-import-record-lifecycle.md`, `corpus/source-snapshots/round-83/manifest.json` |
| `*/corpus/SOURCES.md` rows mentioning "osv" | `kasegi-shokunin/corpus/SOURCES.md` (23), `kaidoku-shokunin/corpus/SOURCES.md` (1) |
| kaidoku's one osv row | S015 = a single OSV *record instance* (`https://api.osv.dev/v1/vulns/CVE-2025-55305`, a dataset) — a different ground, not the FAQ page |
| sibling lanes whose `SOURCES.md` has an `S117` | `chousa-shokunin` S117 = the PRISMA 2020/S paper — an unrelated source in an unrelated lane; no id collision problem (ids are lane-local) |

**Verdict:** the FAQ ground is unclaimed outside kasegi; no sibling-lane conflict, no duplication risk.

---

## 3 — Live re-open of the FAQ vs the six manifest quotes

Re-opened `https://google.github.io/osv.dev/faq/` live with `curl -sSL` (HTTP 200, 34,381 B) and
stripped tags/entities with the same procedure `corpus/instruments/capture-source.py` uses
(script/style removed, block tags → newline, tags stripped, entities decoded, whitespace collapsed).
Receipt: `ScoutPerish-receipts/faq-live-tagtostripped.txt`.

**Counts of each of the six manifest quotes in the tag-stripped live text — all 1 occurrence each,
each at exactly its manifest anchor line:**

| quote id | count | live line | manifest anchor |
|---|---|---|---|
| Q01-withdrawn-excluded | 1 | 112 | 112 |
| Q02-withdrawn-get | 1 | 116 | 116 |
| Q03-gcs-ten-percent | 1 | 121 | 121 |
| Q04-rest-git-orphaned | 1 | 122 | 122 |
| Q05-modified-id-csv | 1 | 94 | 94 |
| Q06-aliases-bump-modified | 1 | 108 | 108 |

Stronger check, run with the lane's own instrument (scratch output only):
`python3 corpus/instruments/capture-source.py --id S117 --url https://google.github.io/osv.dev/faq/ --out $S/S117-recheck.txt --kind html`
→ `status=200 fetched_bytes=34381 snapshot_bytes=10229 sha256=0a5fa51c987544789d3c84fee6be2b1246a7a6a865457668f9e94a37e60bd53e utc=2026-11-06T22:10:04Z`,
i.e. **byte-identical to the frozen
`corpus/source-snapshots/round-83/S117.txt`** (`cmp` clean; receipt
`ScoutPerish-receipts/S117-recapture-byteidentical.txt`). The round-83 capture is reproducible today.

---

## 4 — Two new unopened leads for round 84

Both are OSV-project primary documents, both fit PROVINCE.md's OSV API family (F51–F59: "the same OSV
API family as F51-F58"), and neither is held by any corpus entry, registry row or citation-survival row
(grepped `corpus/knowledge/`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/instruments/citation-survival.tsv`
for `announcing-data-quality`, `osv.dev/data/`, `all.zip`, `gs://osv-vulnerabilities`, `Data sources` → **0 hits**).

### Lead 1 — OSV.dev's own data-quality program post
`https://osv.dev/blog/posts/announcing-data-quality-initiatives/` (HTTP 200, 9,941 B, accessed 2026-11-06T22:09:42Z)

Located quote (15 words): "Thereafter, we will begin gating record imports to records that meet the quality requirements."

Second located quote (17 words): "No way for record providers to know there are problems with records they have already published"

Why it fits PROVINCE.md: the lane owns advisory-quality ground for a researcher who files or cites
OSV records; this is the OSV project's own statement of how it treats a record's quality over its
publication life (the "record publication lifecycle" phrase is the page's own), and it is the closest
published substitute for the missing perishability companion — it names the *ongoing* obligations
(linter, import gating, home-database operator's review of import findings) rather than the
one-time import bar that F58 holds. It is a different page from F58 (`data_quality.html`), F57
(`get-v1-importfindings/`) and F59 (`faq/`), so a scoped claim set would not collide.
`[INFERENCE]` on admissibility: it is a project blog post; the registry `kind` enum admits `docs`,
and tier A would mean "primary or authoritative for that scope" — the OSV project's own program
post is primary for its own program, but the L1 should decide `kind`/`tier` before opening a row.

### Lead 2 — OSV.dev's data-sources / export page
`https://google.github.io/osv.dev/data/` (HTTP 200, 27,419 B, accessed 2026-11-06T22:09:42Z;
upstream source `https://raw.githubusercontent.com/google/osv.dev/master/docs/data.md`, HTTP 200)

Located quote (18 words): "This bucket contains a zip file with all vulnerabilities across all ecosystems (including withdrawn records) at"

Second located quote (17 words): "Vulnerabilities without an ecosystem (typically withdrawn ones) are exported to the gs://osv-vulnerabilities/[EMPTY]/ directory."

Why it fits PROVINCE.md: it is the export-side counterpart of F59. The F59 entry deliberately leaves
the GCS-export retention unpinned (`S117.txt:118` is context only), and this page states the export
layout that makes F59's withdrawn/deletion claims checkable by a consumer — the full-database zip
that *includes* withdrawn records, the `[EMPTY]/` directory that withdrawn records land in when they
carry no ecosystem, the per-ecosystem `modified_id.csv` copies and the reverse-chronological order the
FAQ only half-states (`S117.txt:99-100`, explicitly "not claimed" by F59). It is the same OSV docs
family and tier-A shaped like S108–S117, and it is not covered by any existing entry.

### Also opened but already recorded as leads (not new)
`corpus/SOURCES.md:284` already registers "the two upstream issues linked at S117.txt:122
(google/osv.dev issues 2101 and 2294)" as round-83 leads, so they are not counted as new above.
Their content is now known and is in §5.

---

## 5 — Routed findings for C2 (re-runnable, no lane edit by me)

**F-1 (evidence, strengthens F59's Claim 4 / Rejected over-generalization).** The FAQ says the REST/Git
behaviour "will be changed to match the GCS source" (`S117.txt:122`). Both linked issues are still
**open** as of 2026-11-06, so the change has not landed and F59's rejected over-generalization holds:

- #2101 — "Advisories deleted from source Git repository not being marked as withdrawn", state **open**,
  labels `data quality`, `backlog`, created 2024-04-10, updated 2025-04-02. Body: "records now showing as
  deleted are not marked as withdrawn in OSV.dev"; it names PR #829 (the change that removed the behaviour)
  and says a threshold-based operation "like what's being done for GCS in #2030" would be safer.
- #2294 — "Advisories deleted from REST sources  not being marked as withdrawn", state **open**, labels
  `enhancement`, `infra`, `backlog`, created 2024-06-07, updated 2024-08-07. Body: "Similar to #2101, we
  are not handling deletions for REST sources by marking the advisories as withdrawn."
- #829 (closed 2022-11-16) is the earlier decision: "The supported way to handle making entries as invalid
  is to mark them as 'withdrawn' and leave the entry intact."
Re-run: `curl -sSL https://api.github.com/repos/google/osv.dev/issues/2101 | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['state'],d['title'])"` (same for 2294).

**F-2 (depth:verifiability — G6 tie limb recomputed independently on the uncommitted draft).** I re-implemented
the gate's `tied_ok`/`words()` from `.ufo/waves/round-83/c2/entry-gate.py` and ran it over the
L1-authored draft `corpus/knowledge/osv-faq-post-import-record-lifecycle.md` (read-only copy in scratch).
All six Claim sections tie (content-word stems shared between the rule text and the located span at the
cited line): Claim 1 = 4 stems, Claim 2 = **2**, Claim 3 = 3, Claim 4 = 6, Claim 5 = 8, Claim 6 = 6;
`TIE_WORDS = 2`, so all pass. **Caution for the L1:** Claim 2 sits exactly on the threshold (its only tie
stems are `retur`, `vulns` against the quote "returned by the /vulns/<ID> GET API"). Any single-word edit
to Claim 2's rule line that drops one of those two stems flips it to fail — Claim 2 is the thin one.
Re-run (scratch-safe, writes nothing in the lane):
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -c "import importlib.util,re;s=importlib.util.spec_from_file_location('eg','.ufo/waves/round-83/c2/entry-gate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);t=open('corpus/knowledge/osv-faq-post-import-record-lifecycle.md').read();print([m.tied_ok(b.split(chr(10)+'## ')[0],'S117',re.findall(r'\"([^\"\\n]+)\" \\(S117\\.txt:(\\d+)\\)',b)) for b in re.split(r'(?m)^## ',t) if re.match(r'Claim \\d+\\b',b)])"`

**F-3 (coverage note for the C2 seat, not a defect).** The FAQ's own answer "Why isn't a record available?"
(`S117.txt:79-83`) states a post-import fact no entry holds and no manifest quote pins: a record that
failed the quality bar yields a 404 page that says so, and the reader is pointed at the home database.
It needs no new capture (same S117 source); F59's scope limit and manifest note currently leave
`S117.txt:86-88` (the data-quality issue route) unpinned, and `:79-83` sits just above it — a natural
round-84 in-source extension rather than a new source.

**F-4 (round-83 negative strengthened, cite-worthy).** "No public copy of 'Managing the Perishability of
OSV Records'" now has a much wider evidence base than one web search: full recursive repo tree, all seven
branches' `docs/` trees, both issue and commit search, the site's own search index, the ossf schema repo
and osv-scanner — all negative; only the forward reference survives (quoted in §1). Caveat to state
honestly in any landing text: Wayback/Archive was unreachable from this host and GitHub code search
returned 401, so the negative is "no currently published copy found", not "no copy has ever existed".

---

## 6 — Unresolved / not established

- Archived (pre-removal) copies of a perishability document: not excluded (Wayback/CDX unreachable,
  archive.org availability API 429).
- GitHub code-level occurrences: not searched (code-search API 401, unauthenticated).
- Whether OSV intends to ever publish the companion: unknown; only the tracker family §1c is evidence.
- I did not run any lane gate suite, mutbat battery or instrument selftest; only the single
  `capture-source.py` invocation above (output into scratch) and read-only greps/GETs.

## Files written by this seat

- `.ufo/waves/round-83/w1/ScoutPerish.md` (this report)
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/url-access-times.json`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/url-probe.json`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/faq-live-tagtostripped.txt`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/S117-recapture-byteidentical.txt`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/blog-data-quality-initiatives.txt`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/osv-data-page.txt`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/docs-data.md`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/docs-data_quality.md`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/docs-faq.md`
- `.ufo/waves/round-83/w1/ScoutPerish-receipts/i2030.json`, `i2186.json`, `i2187.json`, `i2188.json`, `i2189.json`, `i2190.json`, `i829.json`

Nothing outside `.ufo/waves/round-83/w1/` was written; the scratch root was removed at yield.
