# ScoutSurface — evidence ledger, kasegi r75 w1 (C2 source identity / capture integrity)

All commands run from the seat scratch dir `/fast/scratch/hyaku/kasegi-r75/ScoutSurface` unless a path is absolute.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` @ `748dfb666280adfb1e249fcf6a265c5d9951eefb`.
Tooling: no installs. curl 8.23.0, poppler pdftotext 26.10.0, Python 3.14.8 (all pre-existing).

## E0 — lane state

```
git -C <lane> rev-parse HEAD                     → 748dfb666280adfb1e249fcf6a265c5d9951eefb
git -C <lane> status --porcelain | head -20      → exit 0; only untracked .ufo/waves/round-75/*
mkdir -p /fast/scratch/hyaku/kasegi-r75/ScoutSurface   → exit 0; df -h /fast/scratch → 419G avail
```

## E1 — Fuzzilli README href

```
curl -s --max-time 60 -o fuzzilli-README.md https://raw.githubusercontent.com/googleprojectzero/fuzzilli/master/README.md
CURL_EXIT=0 ; wc -l fuzzilli-README.md → 249

grep -in 'ndss' fuzzilli-README.md                GREP_EXIT=0 → exactly one hit, line 135:
* A [paper](https://www.ndss-symposium.org/ndss-paper/fuzzilli-fuzzing-for-javascript-jit-compiler-vulnerabilities/) from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers.

grep -in 'pdf' fuzzilli-README.md                → lines 131 (Offensive Con 2019 presentation), 132 (master's thesis)
grep -on 'https://www.ndss-symposium.org[^)]*'    → 1 hit, line 135 (the landing page only)
```

Href ≠ the C2 capture URL `https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf`.

Lane capture, link-stripped form:
```
sed -n '243p' <lane>/corpus/source-snapshots/round-74/S109.txt   → exit 0
A paper from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers.
grep -c 'ndss-symposium' <lane>/corpus/source-snapshots/round-74/S109.txt   → 0 (exit 1)
sed -n '243p' ... | grep -c http                  → 0 (exit 1)
```

Rendered repo page:
```
curl -s --max-time 60 -o fuzzilli_repo_page.html https://github.com/googleprojectzero/fuzzilli
http=200 size=347566
grep -oE 'https://www\.ndss-symposium\.org[^"'\''<> ]*'  → landing-page URL (+ one backslash-escaped duplicate); no PDF URL
```

## E1b — landing page → PDF redirect

```
curl -s --max-time 60 -o ndss_landing.html https://www.ndss-symposium.org/ndss-paper/fuzzilli-fuzzing-for-javascript-jit-compiler-vulnerabilities/ -w 'http=%{http_code} size=%{size_download}\n'
→ http=200 size=69585 (exit 0)
grep -oiE '<title>[^<]*' → FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities - NDSS Symposium
grep -oE 'https://www\.ndss-symposium\.org[^"'\'' ]*\.pdf' | sort -u
→ https://www.ndss-symposium.org/wp-content/uploads/2023-290-paper.pdf
→ https://www.ndss-symposium.org/wp-content/uploads/2024/09/2023-290-slides.pdf

curl -sIL --max-time 60 https://www.ndss-symposium.org/wp-content/uploads/2023-290-paper.pdf
→ HTTP/2 302 ; location: https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf
→ HTTP/2 200 ; content-type: application/pdf ; content-length: 918189   (exit 0)

curl -sL --max-time 60 -o alt2.pdf https://www.ndss-symposium.org/wp-content/uploads/2023-290-paper.pdf -w 'http=%{http_code} size=%{size_download} url=%{url_effective}\n'
→ http=200 size=918189 url=.../2023/02/ndss2023_f290_paper.pdf
sha256sum alt2.pdf → bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9
cmp alt2.pdf f1.pdf → CMP_EXIT=0
```

## E2 — capture integrity

```
curl -s --max-time 60 -o f1.pdf https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf   CURL1_EXIT=0
curl -s --max-time 60 -o f2.pdf https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf   CURL2_EXIT=0
stat -c '%n %s' f1.pdf f2.pdf → f1.pdf 918189 / f2.pdf 918189
sha256sum f1.pdf f2.pdf
  bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9  f1.pdf
  bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9  f2.pdf        SHA_EXIT=0
cmp f1.pdf f2.pdf → CMP_EXIT=0  (identical)
file f1.pdf → PDF document, version 1.6 (zip deflate encoded)
```
Freeze-time comparison: freeze recorded 918189 bytes → **reproduced exactly, no drift**; digest is new information.

```
curl -sI --max-time 60 https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf   HEAD_EXIT=0
HTTP/2 200 ; content-type: application/pdf ; content-length: 918189
last-modified: Wed, 19 Feb 2025 12:42:12 GMT ; etag: "e02ad-62e7e162b7577" ; cf-cache-status: HIT
```

## E2b — capture instrument determinism (scratch only)

```
python3 <lane>/corpus/instruments/capture-source.py --id S110 \
  --url https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf \
  --out <scratch>/S110_probe.txt --kind pdf
CAP_EXIT=0
S110 status=200 fetched_bytes=918189 snapshot_bytes=88072 sha256=0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef utc=2026-11-05T09:53:47Z
(second run) S110_probe2.txt → identical sha256 0780beae… ; cmp S110_probe.txt S110_probe2.txt → CMP_EXIT=0
wc -l S110_probe.txt → 1869 lines

Precedent: grep -rl '"kind": "pdf"' <lane>/corpus/source-snapshots/*/manifest.json → corpus/source-snapshots/round-67/manifest.json (S101)
S101 record fields: sha256(snapshot) raw_sha256 raw_pdf_sha256 bytes raw_bytes snapshot_bytes pages lines body_lines path
```

## E2c — identity from the PDF's own text layer

```
pdftotext -f 1 -l 1 f1.pdf -   → PDFTOTEXT_EXIT=0
line 1:  F UZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities
lines 2-8: Samuel Groß / Simon Koch / Lukas Bernhard / Google / saleo@google.com / TU Braunschweig / simon.koch@… / Ruhr University Bochum / lukas.bernhard@rub.de / Thorsten Holz / Martin Johns / CISPA … / TU Braunschweig / m.johns@…
od -c of line 1 → "F   U   Z   Z   I   L   L   I   :   …"   (single space after F)
od -c of line 2 → "S   a   m   u   e   l       G   r   o 303 237"   (U+00DF)
python3: 'Groß' in capture → True ; 'Gross' in capture → False
grep -n '10.14722' S110_probe.txt → line 60: https://dx.doi.org/10.14722/ndss.2023.24290
```

Crossref (content negotiation, one redirect to api.crossref.org):
```
curl -s --max-time 60 -H 'Accept: application/vnd.citationstyles.csl+json' -L https://doi.org/10.14722/ndss.2023.24290 -o doi_meta2.json -w 'http=%{http_code} url=%{url_effective}\n'
→ http=200 url=https://api.crossref.org/v1/works/10.14722%2Fndss.2023.24290/transform
title: FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities
DOI: 10.14722/ndss.2023.24290
container: Proceedings 2023 Network and Distributed System Security Symposium
published-print: 2023
authors: [('Samuel','Groß'),('Simon','Koch'),('Lukas','Bernhard'),('Thorsten','Holz'),('Martin','Johns')]
```

## E3 — DOI resolve

```
curl -sI --max-time 60 https://doi.org/10.14722/ndss.2023.24290   DOI_HEAD_EXIT=0
HTTP/2 302 ; location: https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf

curl -sIL --max-time 90 https://doi.org/10.14722/ndss.2023.24290 | grep -iE '^(HTTP/|location:|content-type:|content-length:)'   DOI_FOLLOW_EXIT=0
HTTP/2 302 ; content-type: text/html;charset=utf-8 ; location: https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf
HTTP/2 200 ; content-type: application/pdf ; content-length: 918189
```
One hop, straight to the PDF; no landing page in the DOI chain.

## E4 — sibling subject sweep

```
grep -rin 'fuzzilli\|ndss' <fleet>/revenger-shokunin/corpus/SOURCES.md <fleet>/kengaku-shokunin/corpus/SOURCES.md <fleet>/chousa-shokunin/corpus/SOURCES.md 2>/dev/null | head -20
PIPE_EXIT=0 ; 4 hits, all revenger, all 'ndss':
  :129  | S114 | No More Gotos … (NDSS 2015) … ndss2015 programme page
  :356  | S341 | Mens Sana In Corpore Sano — sound firmware corpora (arXiv 2404.11977, DOI 10.14722/ndss.2025.230669)
  :378  | S363 | DeGPT: Optimizing Decompiler Output with LLM, NDSS 2024
  :570  - 2026-10-29, operator-directed RE resource atlas … (Registry-changes prose, not a row)
kengaku: 0 hits ; chousa: 0 hits
```
Per-hit verdicts are in `ScoutSurface.md` §Step 4 (S114 NDSS 2015 decompiler; S341 NDSS'25 firmware corpora; S363 NDSS 2024 LLM decompiler; :570 prose) — none is the NDSS 2023 Fuzzilli paper.

Expected rows S117 / S396 (present, but they do **not** match `fuzzilli|ndss`, so the named grep cannot surface them):
```
grep -nE '^\|[[:space:]]*S(117|396)[[:space:]]*\|' <fleet>/revenger-shokunin/corpus/SOURCES.md
  :132 | S117 | DecFuzzer — ISSTA'20 artifact (monkbai/DecFuzzer @ 8e109c12…) | code | A
  :411 | S396 | trailofbits/mishegos — differential fuzzer for x86 decoders | tool | A
```

No-hit checks:
```
grep -ril 'fuzzilli' ../revenger-shokunin/corpus            → GREP_RIL_EXIT=1, 0 files
for d in <fleet>/*-shokunin/corpus; do grep -ril 'fuzzilli' "$d" | wc -l; done
  → only kasegi = 15 files; all 19 other lanes = 0
for d in <fleet>/*-shokunin; do grep -ic fuzzilli SOURCES.md; grep -ic ndss SOURCES.md; done
  → kasegi fuzzilli=12 ndss=3 ; revenger fuzzilli=0 ndss=4 ; every other lane fuzzilli=0 ndss=0
```

Lane-internal cross-check on the capture:
```
grep -c 'BigSleep' S110_probe.txt  → 0
grep -c 'Big Sleep' S110_probe.txt → 0
grep -c 'FuzzIL' S110_probe.txt    → 0   (exit 1)
grep -ic 'fuzzil' S110_probe.txt   → 10  (all ten are the word "Fuzzilli": lines 867, 1080, 1184, 1208, 1486, 1488, 1533, 1537, 1573, 1603)
grep -n 'own intermediate language' → line 215
grep -n 'Superion\|SoFi\|DIE'  → 129, 225, 276 (the paper's own comparison ground)
```

## E5 — lead lines at the freeze commit

```
git -C <lane> show 748dfb666280adfb1e249fcf6a265c5d9951eefb:corpus/SOURCES.md | grep -n 'ndss-symposium\|NDSS'   GREP_EXIT=0
  121: | S109 | Google Project Zero, Fuzzilli README …
  175: - NDSS Symposium 2023 paper on Fuzzilli (named at kasegi capture S109.txt:243; the capture carries no URL for it) — unopened lead; existence and name only, outside the F52 scope limit.
  270: - Round-74 S109 added (docs, scoped tier A, mined, opened 2026-11-05, recheck 90d, …)
```

Per-line SHA-256 (line content only):
```
git show 748dfb6:corpus/SOURCES.md | sed -n '174p' | sha256sum → 902f017b1b152d3715fe2fafb5f1ee688802cf55ab7ef4b651610f3c1f012b00
git show 748dfb6:corpus/SOURCES.md | sed -n '175p' | sha256sum → 124b3a00b7923080293628af9531a1ae0d07a2341a0740b6f1f6ec8da2adb5a1
git show f9cc05b:corpus/SOURCES.md | sed -n '174p' | sha256sum → 902f017b1b152d3715fe2fafb5f1ee688802cf55ab7ef4b651610f3c1f012b00   (identical)
git show f9cc05b:corpus/SOURCES.md | sed -n '175p' | sha256sum → 124b3a00b7923080293628af9531a1ae0d07a2341a0740b6f1f6ec8da2adb5a1   (identical)
git diff 748dfb6 -- corpus/SOURCES.md                → empty   (DIFF_EXIT=0)
git diff --numstat f9cc05b 748dfb6 -- corpus/SOURCES.md → empty  (0 added, 0 removed)
git diff f9cc05b -- corpus/SOURCES.md | grep -c '^-[^-]' → 0   (exit 1)
```
Both leads are byte-present at freeze and byte-identical to base. Line 174 (OSV.dev overview) stays a lead; its flip condition is untouched by this round.

Full lead lines (from `git show 748dfb6:corpus/SOURCES.md | sed -n '170,180p'`, prefixed `## Leads (unopened)` at 171):
```
173: - Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.
174: - OSV.dev overview page https://google.github.io/osv.dev/api/ — lead, not evidence, not a row. Lead-only fetch 2026-11-05T08:43:42Z (round-74 ScoutSurface; 15262 raw bytes, 1810 converted bytes, sha256 6f92e5b7…). It states "Currently there are no limits on the API." and "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2." Neither statement is admitted ground; a row needs its own capture and manifest (source of this bullet: round-73 spot-check R73-V2).
175: - NDSS Symposium 2023 paper on Fuzzilli (named at kasegi capture S109.txt:243; the capture carries no URL for it) — unopened lead; existence and name only, outside the F52 scope limit.
```
Lane precedent for retiring a lead without editing it in place: `corpus/SOURCES.md:250` `- Leads reconciled against registry, old → new: ISO records → retired as opened S089/S090; …`.

## E6 — base counters (for the L1's landing diff)

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                              → 109   (base f9cc05b: 109; freeze: 109)
grep -cE '^\|[[:space:]]*S110[[:space:]]*\|' corpus/SOURCES.md                                   → 0     (S110 free in kasegi)
ls corpus/knowledge/*.md | wc -l                                                                 → 90
wc -l corpus/instruments/knowledge-expected.txt                                                  → 92 ; grep -vc '^\s*#' → 90
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt                                        → SORT_EXIT=0
python3 corpus/instruments/capture-binding-check.py     → records=88 bound=88 unbound=0            (exit 0)
python3 corpus/instruments/frontier-recheck-count.py    → FRONTIER-CENSUS rows=52 admitted=52 closed=52 problem-rows=0 registry=109 ; entries=55 pass=55 exit=0
scripts/sources-census.sh validate --root <fleet> kasegi → exit 0, six inherited W04 warnings unchanged
scripts/sources-census.sh validate --root <fleet>        → FLEET_VALIDATE_EXIT=0, no E03 duplicate-id
```
Fleet S110 occupancy (census `seen` is per-lane, so no cross-lane E03): revenger S110 = SoK disassembly paper; 14 lanes carry an S110 row; kasegi carries none.

## E7 — trap: DOI as an https:// token in the row source cell (scratch fixture)

```
python3 <lane>/corpus/instruments/capture-binding-check.py --root <scratch>/fixture_lane
source cell = …ndss2023_f290_paper.pdf (DOI 10.14722/ndss.2023.24290)…
  → MANIFEST round-75 records=1 url_bound=1 fetched=1 archival=0
    records=1 bound=1 unbound=0                                            BIND_EXIT=0

source cell = …ndss2023_f290_paper.pdf (DOI https://doi.org/10.14722/ndss.2023.24290)…
  → FAIL rule=double-https-row row=S110 n=2
    FAIL rule=url-ambiguous record=S110 row=S110 tokens=2 dir=round-75
    records=1 bound=0 unbound=1                                            BIND_DOI_HTTPS_EXIT=1
```

## E8 — trap: row must sit under `## Registry`

```
scripts/sources-census.sh validate --file <scratch>/fixture_lane/corpus/SOURCES.md
row NOT under "## Registry" → file E12 S110 row outside Registry section
row under "## Registry"    → file ok <path>                                 CENSUS_EXIT=0
```
Registry header: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (11 content cells; S109 row measures fields=11 via awk -F'|').
Census enums: kind ∈ (spec|docs|paper|code|tool|dataset|talk|book|community|own-work) → `paper` valid; tier ∈ [ABC]; status ∈ (queued|mined|rejected); opened ISO date not in the future; recheck ISO date or `NNd` or symbolic; used-by path must exist on disk (E11).

## E9 — quote anchors verified in the capture (all ≤25 words)

| id | quote | occ | anchor | words | anchor window holds |
|---|---|---|---|---|---|
| Q-claim-gap | `we close this gap and present the first fuzzer` | 1 | 33 | 9 | yes (33-ok) |
| Q-own-il | `we develop our own intermediate language` | 1 | 215 | 6 | yes (215-ok) |
| Q-superion | `Superion, a state-of-the-art open-source fuzzer` | 1 | 129 | 5 | yes (129-ok) |
| Q-design | `designed our approach called Fuzzilli specifically for finding` | 1 | 1080 | 8 | yes (1080-ok) |
| Q-sofi | `we were not able to directly compare our approach to SoFi` | 1 | 225 | 11 | yes (225-ok) |
| Q-die | `Park et al. [36] proposed DIE, a novel` | 1 | 276 | 8 | yes (276-ok) |
| Q-doi | `https://dx.doi.org/10.14722/ndss.2023.24290` | 1 | 60 | 1 | yes (60-ok) |
| title, claim spelling | `FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities` | **0** | 1 | 7 | **no** |
| title, capture spelling | `F UZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities` | 1 | 1 | 8 | yes (1-ok) |
| author ascii | `Samuel Gross` | **0** | 2 | 2 | **no** |
| author capture | `Samuel Groß` | 1 | 2 | 2 | yes (2-ok) |
| novelty, mis-span | `we present the first fuzzer that focuses on JIT vulnerabilities` | **0** | 33 | 10 | **no** (spans the 33/34 line break — use the shorter form) |

## E10 — end-to-end shape validation in a scratch mini-lane

Fixture (scratch only): registry row S110 with the bare-DOI source cell under `## Registry`; `corpus/source-snapshots/round-75/{S110.txt,manifest.json}`; entry `corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md` with `source: S110 — https://…ndss2023_f290_paper.pdf` / `verified-at: 2026-11-05` / `ground: F53` / `recheck: cd <fx2> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-75/manifest.json --source S110` plus an `S110.txt:33` citation; `corpus/README.md` frontier row `| F53 | NDSS 2023 Fuzzilli paper | admitted | \`knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md\` | S110 | keep |`.

```
python3 <lane>/corpus/instruments/frontier-recheck-count.py --root <scratch>/fx2
FRONTIER-CENSUS rows=2 admitted=2 closed=1 problem-rows=1 registry=1
FRONTIER-FAIL F52 status=admitted ids=S109 problems=missing-pass-line,source-id-absent:S109
FRONTIER-PASS F53 ids=S110
FAIL     F52  knowledge/fuzzilli-js-engine-fuzzing-framework.md    ids=-              exit=-    problems=missing-entry
PASS     F53  knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md     ids=S110           exit=0
entries=2 pass=1 exit=1
```
`exit=1` is the fixture's deliberately-absent F52 entry, not F53: **F53 passes with exit=0**.

```
python3 <lane>/corpus/instruments/source-recheck.py --manifest <fx2>/corpus/source-snapshots/round-75/manifest.json --source S110
S110:sha256 OK
S110:Q01-claim-gap OK occurrences=1 anchor=33-ok
S110:Q02-own-il OK occurrences=1 anchor=215-ok
S110:Q03-superion OK occurrences=1 anchor=129-ok
S110:Q04-design OK occurrences=1 anchor=1080-ok
S110:Q05-sofi OK occurrences=1 anchor=225-ok
S110:Q06-die OK occurrences=1 anchor=276-ok
RECHECK_EXIT=0
```
Same command from a foreign cwd (`cd /`): identical 7 OK lines, `FOREIGN_CWD_EXIT=0`.

Counter internals consulted (read-only): `frontier-recheck-count.py:104-111` (FRONTIER_ROW / FRONTIER_SOURCES / SOURCE_LINE / EVIDENCE_LINE / RECHECK_LINE / RECHECK_SOURCE / RECHECK_MANIFEST regexes), `:204-285` (the five contract limbs + `bash -c` recheck execution with `cwd=root`), `capture-binding-check.py:37-125` (rules B1-B5, C, D, E1-E3), `sources-census.sh:600-680` (kind/tier/status/opened/recheck enums, E01-E12, W01-W04), `:708-745` (per-lane validate loop — the duplicate-id `seen` map is per lane).

## E11 — scratch hygiene

```
rm -rf -- /fast/scratch/hyaku/kasegi-r75/ScoutSurface     (exit 0, run after this file was written)
```
