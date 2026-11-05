# K73ConnectSiblings — sibling-overlap scan for the F51 candidate (OSV.dev POST /v1/query)

Seat: K73ConnectSiblings (leaf, read-only). Attack/produce: sibling-overlap attack on C2 (coverage, frontier F51, source S108) and the C1 knowledge set is not touched. No lane file was written; the only writes are this report and the `K73ConnectSiblings-evidence-*.txt` copies beside it. No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r73/K73ConnectSiblings/` was removed after the copies (`rm -rf` exit 0).

Base-state note: the lane has no F51 yet (`grep -E '\bF51\b' PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/knowledge/*.md`, exit 1, no output), and no S108 row (below). Consistent with claims.json before-values (registry=107).

## 1. Sibling lanes (`ls -d /home/vgpnk/Projects/shokunin/*-shokunin`, exit 0)

20 siblings plus the lane: audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi.

Scan command (read-only; the path set is `corpus/`, `PROVINCE.md`, `SKILL.md` per sibling):

```
grep -rnIi -E '(^|[^A-Za-z0-9])osv([^A-Za-z0-9]|$)|osv\.dev|v1/query|querybatch' <sibling>/{corpus,PROVINCE.md,SKILL.md}
```

Result: 6 hit lines in 4 files (evidence: `.ufo/waves/round-73/w1/K73ConnectSiblings-evidence-sibling-osv-hits.txt`). The loop's own status line is not a per-grep exit code; the per-term runs below carry their exit codes.

Per-term runs (`grep -rnIli -E '<term>' <each sibling>/corpus <PROVINCE.md> <SKILL.md>`):

| term | hits | files | exit |
|---|---|---|---|
| `osv\.dev` | 3 | kaidoku-shokunin (SOURCES.md, lessons/round-13.md, evidence/round-30/c1/pypi-uv-0.13.0.json) | 0 |
| `v1/query` | 0 | — | 1 |
| `querybatch` | 0 | — | 1 |
| `OSV` (whole word) | 4 | kaidoku x3 files, kotodama-shokunin/corpus/knowledge/linguistics/syntax-typology.md | 0 |

Unbounded first pass (`grep -rn -i -E 'osv\.dev|OSV|v1/query|querybatch'`, no word bounds) returned 414 lines across 10 siblings. These are substring matches inside base64, minified or binary fixture bytes (e.g. audio-shokunin fixtures `measure_audio.py`, tokens such as `R83OSV`, `posVarCount`, `dofCount`) and are not counted. The word-bounded scan above is the count used.

## 2. Overlap table — sibling hits

| # | repo : path : line | what the hit is | verdict |
|---|---|---|---|
| S1 | kaidoku-shokunin : corpus/SOURCES.md : 21 | S015 "OSV CVE-2025-55305 record — https://api.osv.dev/v1/vulns/CVE-2025-55305" (per-record GET of an OSV record) | sibling-owned: report only. Same host, different endpoint (`/v1/vulns/{id}`, not `POST /v1/query`). No overlap with the F51 contract. |
| S2 | kaidoku-shokunin : corpus/lessons/round-13.md : 42 | same S015 record cited in a lesson | sibling-owned: report only |
| S3 | kaidoku-shokunin : corpus/lessons/round-13.md : 59 | "the opened OSV JSON's `details` prose names a 36.8.1 fix …" (S015 limitation note) | sibling-owned: report only |
| S4 | kaidoku-shokunin : corpus/evidence/round-30/c1/pypi-uv-0.13.0.json : 1 | PyPI JSON fixture with two `https://osv.dev/vulnerability/<id>` link fields (GHSA-hq85-5cpj-mr62, PYSEC-2026-4321) | sibling-owned: report only. Evidence of a PyPI page, not a query contract. |
| S5 | kotodama-shokunin : corpus/knowledge/linguistics/syntax-typology.md : 11, 32 | "OSV" = Object-Subject-Verb word order (linguistics) | no overlap (term collision, not the service) |

v1/query and querybatch: zero hits in every sibling. No sibling admits, quotes or names the OSV POST /v1/query contract, a request payload, the Git-tag query, pagination, or the 32 MiB limit. F51 has no sibling duplicate. Sibling ids are not ours to renumber; no sibling action is requested.

## 3. Lane hits (`grep -rnIi osv` over the lane; per-file exit 0)

Lane evidence files: `K73ConnectSiblings-evidence-lane-knowledge-osv.txt` (27 lines), `…-lane-province-osv.txt` (2), `…-lane-readme-osv.txt` (5).

### 3a. corpus/knowledge (27 hits, 3 files)

| path : lines | owner row (PROVINCE / README) | verdict |
|---|---|---|
| osv-affected-range-events.md : 1, 3, 10, 17, 18, 25, 26, 52, 83, 93, 94, 106, 113 (13) | F31 (PROVINCE.md:178; README.md:743) | owned by F31. Line 18: "What any particular OSV producer publishes, and what osv.dev's service does with it, is outside these bytes" — the F31 boundary that F51 fills. |
| openssf-scorecard-checks.md : 1, 31, 34, 35, 36, 37, 38, 40, 42, 77, 82, 83 (12) | **F35** (PROVINCE.md:197; README.md:841). Not one of F25/F30/F31/F33. | owned by F35. Adjacency: line 31 "consumes the OSV service" and line 35 `[OSV …](https://osv.dev/) service` state Scorecard's USE of OSV (S086 Q10). F51 admits the query contract; neither claim covers the other. F35 text says "the OSV format stays F31". No overlap in claimed content. |
| github-advisory-database-curation-semantics.md : 75, 120 (2) | file row **F48** (corpus/README.md:1097); line 120 defers "the OSV schema's own fields" to S080 | owned by F48; the OSV schema boundary is F31. Line 75 quotes S105.txt:567 "Open Source Vulnerability (OSV) format" (a name statement). No overlap with the query contract. |

### 3b. PROVINCE.md (2 hits)

- Line 178 — F31 amendment (r50, 2026-11-01). Owned by F31. Exact scope-limit words, quoted verbatim:

  > scope limit: the format's range/event semantics only — **the osv.dev service API**, the JSON Schema validation artifact, individual database exports and per-database database_specific values stay out

  This is the named gap C2 fills. claims.json non_claims says the F31 scope limit "stays as written"; F51 admits the service contract, not the OSV record format. Verdict: owned by F31; direct overlap is intended, no F31 edit is needed.

- Line 197 — F35 amendment (r54). Owned by F35. Its scope limit says "the publisher/API endpoints … are unasserted, the OSV format stays F31".

### 3c. corpus/README.md (5 hits)

- 731, 732, 739, 743 — F31 admission block and coverage-map rows (`| F31 | OSV affected-range events — … |`). Owned by F31.
- 841 — the F35 row (`| F35 | OpenSSF Scorecard check documentation — … OSV-service-backed vulnerability detection …`). Owned by F35.

### 3d. Rows the seat was asked to check (F25, F30, F33)

`sed -n '<n>p' corpus/README.md | grep -c -i osv` on the F25 row (591), F30 row (718) and F33 row (792): counts 0, 0, 0 (each exit 1). No lane OSV hit is owned by F25, F30 or F33. The only frontier rows carrying OSV text are F31 and F35 (and F48 for the GitHub Advisory file).

## 4. S108 registry collisions

- Lane: `grep -n -E '(^|[^A-Za-z0-9])S108([^0-9]|$)' corpus/SOURCES.md` → no output, exit 1. Expected: none. The lane's next id is S108, unused.
- Siblings (`grep -c` per `corpus/SOURCES.md`, exit 0 when any match; evidence `…-evidence-s108-siblings.txt`): S108 is a live row id in 15 siblings with unrelated content — chousa (2 lines, PRISMA 2020 statement), kaidoku (2, unblob SquashFS handler), kake (1, sitemaps.org FAQ), kama (6, llama.cpp slots), kengaku (2, Terminal-Bench regex-log grader), kotoba (6, Cursor Rules), kotodama (1, Plato Cratylus), kumitate (3, Idempotent Consumer), mado (2, CPython subprocess), mori (1, DeepSeek with Oh My Pi), revenger (2, REA evidence ledger), souji (2, Python RecursionError), tabi (2, Chromium Dash), tameshi (3, TFF golden tests zh-cn), tsukuroi (2, pacman downgrading). Audio, game-dev-2d, game-dev-3d, kagi and lore have no S108 (grep exit 1).
- Verdict: **no collision for the lane**. Each lane's registry is its own `corpus/SOURCES.md`; the sibling ids are sibling-owned and report only. The lane must not reuse or renumber them. One sibling line (kotoba SOURCES.md:348–349) discusses its own S108/S049 pair; that is internal to kotoba.

## 5. considerthese/ (lane)

Directory listing (`ls -la`, exit 0): 8 daily files, 2026-10-19 through 2026-10-26.

- `grep -rnIi -E 'osv|vulnerability[- ]query|vulnerab[a-z]* (api|service)|service contract|v1/query|querybatch|query api' …/considerthese` → no output, exit 1.
- `grep -rnIi -E 'osv|v1/query|querybatch' …/considerthese` → no output, exit 1.
- Broader `grep -rnIi -E 'vulnerab|CVE|advisor|API' …/considerthese` (exit 0) returned CRA/CNA rule discussion (2026-10-21.md:27, 28, 34, 69, 70, 77; 2026-10-23.md:29, 44; 2026-10-24.md:22, 27, 28, 29; 2026-10-25.md:18, 48 — the last being "GitHub's compare API"). None names OSV, a vulnerability-query API, or a service contract.

Result: **none**. No unimplemented proposal in considerthese/ overlaps F51.

## 6. Verdict summary for C2 (sibling-overlap axis)

- No sibling admits or quotes the POST /v1/query contract (v1/query, querybatch: 0 hits). Sibling OSV use is per-record GET (kaidoku S015) or unrelated linguistics (kotodama).
- Lane overlap with the F51 candidate is F31's named boundary (PROVINCE.md:178) — intended, the gap F51 fills — and adjacency to F35 (Scorecard's use of the OSV service, lines 31/35 of openssf-scorecard-checks.md). F35 and F51 claim different things; the F51 entry must not assert Scorecard's consumption of the service, and must not restate the F31 range/event semantics.
- The lane's F48 file (github-advisory) defers the OSV schema to S080/F31; no change needed for F51.
- No sibling owns or duplicates S108 content; the lane's S108 is free (grep exit 1).

## 7. Commands and exit codes (for verification)

| # | command (abbreviated) | exit |
|---|---|---|
| 1 | `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` | 0 |
| 2 | `cat .ufo/waves/round-73/claims.json` | 0 |
| 3 | sibling scan (word-bounded, per-sibling loop) → 6 lines | loop; see per-term rows |
| 4 | per-term `grep -rnIli` for `osv\.dev`, `v1/query`, `querybatch`, `OSV` | 0, 1, 1, 0 |
| 5 | unbounded `grep -rn -i -E 'osv\.dev\|OSV\|v1/query\|querybatch'` (noise, 414 lines) | 1 (loop) |
| 6 | `grep -rnIi osv corpus/knowledge` | 0 (27 lines) |
| 7 | `grep -nIi osv PROVINCE.md` | 0 (2 lines) |
| 8 | `grep -nIi osv corpus/README.md` | 0 (5 lines) |
| 9 | `grep -n -E '\bF51\b' PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/knowledge/*.md` | 1 |
| 10 | `grep -n S108 corpus/SOURCES.md` (lane) | 1 |
| 11 | `grep -c -E S108 <sibling>/corpus/SOURCES.md` ×19 | 0 (15 siblings), 1 (5 siblings) |
| 12 | `ls -la …/considerthese` | 0 |
| 13 | `grep -rnIi -E 'osv\|vulnerability[- ]query\|…' …/considerthese` | 1 |
| 14 | `grep -rnIi -E 'osv\|v1/query\|querybatch' …/considerthese` | 1 |
| 15 | broad `grep -rnIi -E 'vulnerab\|CVE\|advisor\|API' …/considerthese` | 0 |
| 16 | `sed -n '<n>p' corpus/README.md \| grep -c -i osv` for rows 591, 718, 792 | 0 each (count 0; grep exit 1) |

Install/update record: none. No package, tool or runtime was installed or upgraded; pacman was not touched.

Evidence files (written under the wave dir): `K73ConnectSiblings-evidence-sibling-osv-hits.txt`, `…-lane-knowledge-osv.txt`, `…-lane-province-osv.txt`, `…-lane-readme-osv.txt`, `…-s108-siblings.txt`.
