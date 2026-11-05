# ScoutSurface — kasegi round 75, wave 1: C2 source identity and capture integrity

Seat: ScoutSurface (leaf, read-only; no subagents dispatched).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin @ 748dfb666280adfb1e249fcf6a265c5d9951eefb (freeze commit; confirmed `git rev-parse HEAD` = 748dfb6, working tree clean except untracked `.ufo/waves/round-75/` wave files, exit 0).
Scratch: /fast/scratch/hyaku/kasegi-r75/ScoutSurface (deleted before yield; see "Scratch hygiene").
Scope note: this seat did **not** edit the lane tree. Every file written is under `.ufo/waves/round-75/w1/` (this report + named evidence files) or the seat scratch dir.

Tooling: no install was performed. Pre-existing host tools only: curl 8.23.0, poppler `pdftotext` 26.10.0, Python 3.14.8. Per the operator rule, PACMAN IS PAUSED host-wide; nothing needed installing (`pdftotext` is already present, which is what `capture-source.py --kind pdf` requires).

---

## Headline finding (changes what the C2 row may claim)

**The Fuzzilli README's href for the NDSS 2023 paper is NOT the PDF URL that C2 names.** The README (and the lane's own capture `S109.txt:243`) points at the NDSS **landing page**:

```
https://www.ndss-symposium.org/ndss-paper/fuzzilli-fuzzing-for-javascript-jit-compiler-vulnerabilities/
```

C2 names `https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf` as the capture URL. That PDF URL is nevertheless **correct and canonical**, reached by a different route (steps 1b/2b below): the DOI resolves to it in one hop, and the landing page's own PDF link (`https://www.ndss-symposium.org/wp-content/uploads/2023-290-paper.pdf`) 302-redirects to it. Both routes land on the same 918189-byte PDF with the same digest.

Consequence for the L1: the registry row S110's source cell must carry the **PDF URL** (that is the `url` the capture record pins and the URL `capture-binding-check.py` rule B5 compares byte-for-byte against the row). The README's landing-page href is the *provenance* of the paper's identity, not the capture URL. The claims' wording for C2 is unaffected — it already names the PDF URL — but no receipt may state that the README href equals the capture URL. This is the r74 "link-stripped form" gap closing: the lead at `corpus/SOURCES.md:175` said "the capture carries no URL for it", and that is now resolvable to exactly one canonical PDF URL.

---

## Step 1 — Provenance of the paper URL

### 1a. The exact markdown line in the Fuzzilli README

Command (cwd = scratch):
```
curl -s --max-time 60 -o fuzzilli-README.md https://raw.githubusercontent.com/googleprojectzero/fuzzilli/master/README.md; echo CURL_EXIT=$?
```
`CURL_EXIT=0`; file 249 lines.

```
grep -in 'ndss' fuzzilli-README.md
```
`GREP_EXIT=0`, exactly one hit — README **line 135**:

```
* A [paper](https://www.ndss-symposium.org/ndss-paper/fuzzilli-fuzzing-for-javascript-jit-compiler-vulnerabilities/) from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers.
```

**Verdict: the href does NOT equal the C2 capture URL.** It equals the NDSS landing page. Recorded as required.

The lane capture's link-stripped form is confirmed byte-for-byte:
```
sed -n '243p' .../corpus/source-snapshots/round-74/S109.txt
```
→ `A paper from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers.` (`exit 0`), and that capture line contains **zero** `https://` tokens (`grep -c 'ndss-symposium'` → 0, `grep -c http` on that line → 0). The README's other two `.pdf` references are the Offensive Con 2019 presentation and the master's thesis (`grep -in 'pdf'` → lines 131, 132) — neither is the NDSS paper. Only one `ndss-symposium.org` URL exists in the whole README (`grep -on 'https://www.ndss-symposium.org[^)]*'` → 1 hit, line 135).

The rendered repository page carries the same single href:
```
curl -s --max-time 60 -o fuzzilli_repo_page.html https://github.com/googleprojectzero/fuzzilli
```
`http=200 size=347566`; `grep -oE 'https://www\.ndss-symposium\.org[^"'\''<> ]*'` → the same landing-page URL (plus one backslash-escaped duplicate in the HTML source). No PDF URL anywhere on the repo page.

### 1b. The landing page's own PDF link resolves to the C2 capture URL

```
curl -s --max-time 60 -o ndss_landing.html https://www.ndss-symposium.org/ndss-paper/fuzzilli-fuzzing-for-javascript-jit-compiler-vulnerabilities/ -w 'http=%{http_code} size=%{size_download}\n'
```
`http=200 size=69585`, `exit 0`. `<title>` = `FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities - NDSS Symposium`.

PDF hrefs on that page (`grep -oE 'https://www\.ndss-symposium\.org[^"'\'' ]*\.pdf' | sort -u`):
- `https://www.ndss-symposium.org/wp-content/uploads/2023-290-paper.pdf` (the paper)
- `https://www.ndss-symposium.org/wp-content/uploads/2024/09/2023-290-slides.pdf` (slides)

```
curl -sIL --max-time 60 https://www.ndss-symposium.org/wp-content/uploads/2023-290-paper.pdf
```
→ `HTTP/2 302`, `location: https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf`, then `HTTP/2 200`, `content-type: application/pdf`, `content-length: 918189`.

```
curl -sL --max-time 60 -o alt2.pdf https://www.ndss-symposium.org/wp-content/uploads/2023-290-paper.pdf
```
`http=200 size=918189`, `sha256=bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9` — **byte-identical to the C2 capture URL fetch** (`cmp alt2.pdf f1.pdf` → `CMP_EXIT=0`).

So the chain is: README → landing page → (302) → `ndss2023_f290_paper.pdf`. The C2 capture URL is the canonical destination of both the DOI and the landing page.

---

## Step 2 — Capture integrity (two independent fetches)

```
curl -s --max-time 60 -o f1.pdf https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf
curl -s --max-time 60 -o f2.pdf https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf
```
`CURL1_EXIT=0`, `CURL2_EXIT=0`.

| fact | value |
|---|---|
| f1 size | 918189 bytes (`stat -c '%n %s'`) |
| f2 size | 918189 bytes |
| f1 sha256 | `bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9` |
| f2 sha256 | `bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9` |
| identical? | **yes** — `cmp f1.pdf f2.pdf` → `CMP_EXIT=0` |
| type | `PDF document, version 1.6 (zip deflate encoded)` (`file f1.pdf`) |

**Drift vs freeze time: NONE.** The freeze-time record of 918189 bytes is reproduced exactly by both fetches; the digest above is new information (the freeze receipt recorded bytes only, not a digest).

Response headers (`curl -sI --max-time 60 ...`, `HEAD_EXIT=0`):
`HTTP/2 200`, `content-type: application/pdf`, `content-length: 918189`, `last-modified: Wed, 19 Feb 2025 12:42:12 GMT`, `etag: "e02ad-62e7e162b7577"`, `cache-control: public, max-age=14400`, `cf-cache-status: HIT`.

### 2b. The capture instrument reproduces the bytes deterministically

The lane's own capture path was exercised read-only into scratch (never into the lane tree):
```
python3 <lane>/corpus/instruments/capture-source.py --id S110 \
  --url https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf \
  --out <scratch>/S110_probe.txt --kind pdf
```
`CAP_EXIT=0`:
`S110 status=200 fetched_bytes=918189 snapshot_bytes=88072 sha256=0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef utc=2026-11-05T09:53:47Z`

A second identical run produced the **same** snapshot digest (`0780beae…`, `cmp S110_probe.txt S110_probe2.txt` → `CMP_EXIT=0`): the pdftotext→collapse pipeline is byte-deterministic on this host. Snapshot: 1869 lines / 88072 bytes. Precedent for `kind: pdf` records exists at `corpus/source-snapshots/round-67/manifest.json` (S101, FIRST PSIRT Maturity Document), which pins both the snapshot digest and `raw_sha256` / `raw_pdf_sha256` / `raw_bytes` / `pages` — the same field set the C2 manifest should mirror.

### 2c. Identity confirmation from the PDF's own text layer

`pdftotext f1.pdf -` (page 1) gives the title and byline:
- Title (line 1 of the snapshot): `F UZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities` — note the small-caps letter-spacing artifact `F UZZILLI` (a single space after `F`); a quote of the title must use the capture's exact bytes, not the claim's `FUZZILLI` spelling. Verified: `occ=0` for the `FUZZILLI:` form, `occ=1` + `anchor=1-ok` for the `F UZZILLI:` form.
- Authors (snapshot lines 2–8): `Samuel Groß`, `Simon Koch`, `Lukas Bernhard`, `Thorsten Holz`, `Martin Johns`. `Groß` is U+00DF (`od -c` shows `G r o 303 237`); the ASCII `Gross` does **not** occur in the capture. The claim's "Samuel Gross" is a transliteration, not a capture quote.
- DOI string on snapshot **line 60**: `https://dx.doi.org/10.14722/ndss.2023.24290` (`occ=1`, `anchor=60-ok`).

Crossref metadata (via `curl -s -H 'Accept: application/vnd.citationstyles.csl+json' -L https://doi.org/10.14722/ndss.2023.24290`, exit 0) — title `FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities`; DOI `10.14722/ndss.2023.24290`; container `Proceedings 2023 Network and Distributed System Security Symposium`; `published-print` 2023; authors exactly `Samuel Groß, Simon Koch, Lukas Bernhard, Thorsten Holz, Martin Johns`. **The claim's author list and DOI match Crossref exactly.**

---

## Step 3 — DOI resolve chain

```
curl -sI --max-time 60 https://doi.org/10.14722/ndss.2023.24290
```
`DOI_HEAD_EXIT=0`:
```
HTTP/2 302
location: https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf
```

```
curl -sIL --max-time 90 https://doi.org/10.14722/ndss.2023.24290 | grep -iE '^(HTTP/|location:|content-type:|content-length:)'
```
`DOI_FOLLOW_EXIT=0`:
```
HTTP/2 302
content-type: text/html;charset=utf-8
location: https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf
HTTP/2 200
content-type: application/pdf
content-length: 918189
```

**One hop, directly to the PDF** — no landing page in the DOI chain. The DOI's target URL is byte-identical to the C2 capture URL, and the 918189-byte content-length matches both fetches. The DOI is therefore an independent, first-party confirmation that the C2 capture URL is the NDSS 2023 paper.

---

## Step 4 — Sibling subject sweep

Named command, verbatim, from the fleet root:
```
grep -rin 'fuzzilli\|ndss' /home/vgpnk/Projects/shokunin/revenger-shokunin/corpus/SOURCES.md \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md 2>/dev/null | head -20
```
`PIPE_EXIT=0` (grep found matches). **4 hits total, all in revenger, all `ndss`, none `fuzzilli`:**

| # | file:line | id | subject | verdict |
|---|---|---|---|---|
| 1 | revenger `corpus/SOURCES.md:129` | S114 | "No More Gotos" (NDSS 2015) — decompilation structuring, `ndss-symposium.org/ndss2015/…` programme page | revenger holds an **NDSS 2015 decompiler** paper; different venue year, different subject, no Fuzzilli, no JIT fuzzing. Not the NDSS 2023 Fuzzilli paper. |
| 2 | revenger `corpus/SOURCES.md:356` | S341 | "Mens Sana In Corpore Sano" — sound firmware corpora, arXiv 2404.11977, DOI 10.14722/ndss.2025.230669, NDSS'25 | revenger holds an **NDSS 2025 firmware-corpora** paper; arXiv primary, NDSS'25 accepted manuscript. Different subject (firmware corpora, not JS JIT fuzzing), different year. Not the NDSS 2023 Fuzzilli paper. |
| 3 | revenger `corpus/SOURCES.md:378` | S363 | "DeGPT: Optimizing Decompiler Output with LLM", NDSS 2024 | revenger holds an **NDSS 2024 LLM-decompiler** paper. Different subject, different year. Not the NDSS 2023 Fuzzilli paper. |
| 4 | revenger `corpus/SOURCES.md:570` | — (Registry-changes prose) | "…opened primary pages (arXiv/USENIX/NDSS/IEEE/ACM abstract pages…)" | prose mentioning the NDSS venue generically; not a registry row and names no Fuzzilli document. Not a competing row. |

`kengaku` and `chousa` returned **zero** hits for either term.

**Expected verdict confirmed, with one refinement:** the task text expected "revenger S117 DecFuzzer and S396 mishegos tool docs" among the sweep hits. Those two rows are real and present (`grep -nE '^\|[[:space:]]*S(117|396)[[:space:]]*\|'` → revenger `corpus/SOURCES.md:132` = S117 `monkbai/DecFuzzer` (kind `code`, ISSTA'20 artifact), `:411` = S396 `trailofbits/mishegos` (kind `tool`, differential x86-decoder fuzzer)). But **neither row contains the strings `fuzzilli` or `ndss`**, so the named `grep` does not surface them — they are fuzzer-*tooling* rows, not NDSS-Fuzzilli-paper rows. They are the rows the B8 distinctness screen must be distinct *from*, and they are confirmed present in revenger.

No-hit checks:
```
grep -ril 'fuzzilli' ../revenger-shokunin/corpus        → GREP_RIL_EXIT=1, 0 files
grep -ril 'fuzzilli' <each of all 20 sibling lanes>/corpus → only kasegi hits (15 files); every sibling = 0
```
Per-lane `SOURCES.md` term counts across the whole fleet: `kasegi fuzzilli=12 ndss=3`, `revenger fuzzilli=0 ndss=4`, **every other lane `fuzzilli=0 ndss=0`** (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, souji, tabi, tameshi, tsukuroi).

**Conclusion for B8:** the NDSS 2023 Fuzzilli paper is held by **no sibling lane** — no lane's corpus names it. revenger holds three unrelated NDSS papers (2015 decompiler, 2024 LLM decompiler, 2025 firmware corpora) and two fuzzer-tooling rows (DecFuzzer S117, mishegos S396); none of the five is the NDSS 2023 Fuzzilli paper, and the corpus-wide `grep -ril fuzzilli` finds zero sibling files. The distinctness screen holds on its narrowed form: the paper's design/comparison/evaluation ground is distinct from S109 (tool README), S093 (PZ comparison post), and revenger's S117/S396 (fuzzer tool docs). It does **not** require that no sibling holds fuzzer documentation — revenger does, at S117/S396.

### Lane-internal cross-check (the paper is not the README, and not the PZ post)
```
grep -c 'BigSleep' <capture>  → 0
grep -c 'Big Sleep' <capture> → 0
grep -c 'FuzzIL'   <capture>   → 0   (case-sensitive; the 10 case-insensitive "fuzzil" hits are all "Fuzzilli")
```
The paper never mentions BigSleep (so it cannot be confused with S093/F41) and never uses the name **FuzzIL** (it says "we develop our own intermediate language", snapshot line 215). The F52 README entry's scope limit ("not the NDSS 2023 paper's content (existence and name only)") and the F53 scope limit are therefore cleanly separable: the paper's own intermediate-language/design/comparison/evaluation ground is unheld by F52. The paper *does* compare to Superion, SoFi and DIE (snapshot lines 129, 225, 276) — those are the paper's own comparison ground, distinct from revenger's DecFuzzer/mishegos rows.

---

## Step 5 — Lead lines byte-present at the freeze commit

```
git -C <lane> show 748dfb666280adfb1e249fcf6a265c5d9951eefb:corpus/SOURCES.md | grep -n 'ndss-symposium\|NDSS'
```
`GREP_EXIT=0` → three hits: line 121 (S109 row), **line 175 (the NDSS lead)**, line 270 (Registry-changes prose).

Per-line SHA-256 (of the single line, via `git show … | sed -n 'Np' | sha256sum`):

| line | content | sha256 | present at base f9cc05b? | present at freeze 748dfb6? |
|---|---|---|---|---|
| **174** | OSV.dev overview lead | `902f017b1b152d3715fe2fafb5f1ee688802cf55ab7ef4b651610f3c1f012b00` | **yes — identical hash** | **yes** |
| **175** | NDSS Symposium 2023 paper on Fuzzilli lead | `124b3a00b7923080293628af9531a1ae0d07a2341a0740b6f1f6ec8da2adb5a1` | **yes — identical hash** | **yes** |

Both lead lines are byte-identical between the base commit and the freeze commit, and both are present in the freeze tree. The working tree's `corpus/SOURCES.md` is also identical to the freeze commit (`git diff 748dfb6 -- corpus/SOURCES.md` → empty, `DIFF_EXIT=0`), and `git diff --numstat base freeze -- corpus/SOURCES.md` → empty, i.e. **0 added and 0 removed lines** between base and freeze — the B2 "registry-unchanged" precondition currently holds.

Full text of the two lines (from `git show 748dfb6:corpus/SOURCES.md | sed -n '170,180p'`):
- **174**: `- OSV.dev overview page https://google.github.io/osv.dev/api/ — lead, not evidence, not a row. Lead-only fetch 2026-11-05T08:43:42Z (round-74 ScoutSurface; 15262 raw bytes, 1810 converted bytes, sha256 6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab). …` — **it stays a lead; its flip condition is unchanged by this round.** Nothing in the NDSS paper bears on the OSV API overview's flip condition.
- **175**: `- NDSS Symposium 2023 paper on Fuzzilli (named at kasegi capture S109.txt:243; the capture carries no URL for it) — unopened lead; existence and name only, outside the F52 scope limit.` — **the parenthetical "the capture carries no URL for it" is now false in substance**: the URL is resolvable (steps 1–3), and the F53 admission supersedes the lead. The C2 target in claims.json says the lead is "kept byte-identical as history", so the L1 must decide the reconciliation form: the claims bind "kept byte-identical", so **line 175 must remain byte-identical** and the supersession must be recorded elsewhere (Registry-changes prose / the round lesson), exactly as r74 reconciled the S110 line and the retired leads at `corpus/SOURCES.md:250`. Note the existing precedent at line 250: `- Leads reconciled against registry, old → new: …` — the lane's own convention for retiring a lead is a Registry-changes bullet, not an in-place edit of the lead line.

---

## Landable-shape findings the L1 will hit (all exercised, not predicted)

Base counters measured at freeze (`git show 748dfb6:corpus/SOURCES.md`, live instrument runs):
- registry rows `S…` = **109** (base and freeze identical) — B1 wants 110.
- `ls corpus/knowledge/*.md | wc -l` = **90** — B3 wants 91.
- `capture-binding-check.py` → `records=88 bound=88 unbound=0`, exit 0 — B4 wants 89.
- `frontier-recheck-count.py` → `FRONTIER-CENSUS rows=52 admitted=52 … registry=109`, `entries=55 pass=55 exit=0` — B6 wants F53 admitted / entries=56.
- `corpus/instruments/knowledge-expected.txt` = **92 lines / 90 non-comment rows**; `LC_ALL=C sort -c` exit 0. **B3's "93 lines / 91 non-comment rows" is the post-landing value** (90 + 1 knowledge entry = 91 files ⇒ 91 rows ⇒ 92 lines at base becomes 93 lines / 91 rows — consistent with the claims' "expected 93/91 sort-clean" phrasing, and with the base receipt's 92/90).
- `sources-census.sh validate --root <fleet> kasegi` → exit 0 with the six inherited W04 warnings, unchanged.
- Fleet-wide `sources-census.sh validate --root <fleet>` → exit 0, **no E03 duplicate-id** across lanes: the census's `seen` map is per-lane (`row_pass` is invoked per file in the `while IFS=$'\t' read -r lane f dir` loop), so kasegi claiming **S110** does not collide with revenger's S110 (SoK disassembly paper) or the 13 other lanes' S110 rows. The S110 id is free inside kasegi (`grep -cE '^\|[[:space:]]*S110[[:space:]]*\|' corpus/SOURCES.md` → 0).

### Trap 1 (high cost if missed): the DOI must not appear as an `https://` token in the row's source cell

`capture-binding-check.py` rule B4 requires the source cell to carry **exactly one** `https://` token, and B5 requires the capture record's `url` to equal it byte-for-byte. Exercised on a scratch fixture lane:

- source cell with `(DOI 10.14722/ndss.2023.24290)` (bare DOI, no scheme) → `records=1 bound=1 unbound=0`, **exit 0**.
- source cell with `(DOI https://doi.org/10.14722/ndss.2023.24290)` → `FAIL rule=double-https-row row=S110 n=2`, `FAIL rule=url-ambiguous record=S110 row=S110 tokens=2`, `records=1 bound=0 unbound=1`, **exit 1** → B4's `unbound=0` predicate fails.

**Write the DOI as a bare `10.14722/ndss.2023.24290` string in the source cell** (exactly as claims.json's C2 target text already does), and keep the PDF URL as the single `https://` token.

### Trap 2: the row must live under a `## Registry` heading

`census validate --file <fixture>` on a SOURCES.md whose only row was **not** under `## Registry` → `file E12 S110 row outside Registry section`, exit 0 but a finding printed. With the row under `## Registry` → `file ok <path>`, exit 0. Append the S110 row inside the existing `## Registry` table (11 content cells, `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` — the S109 row measures `fields=11`).

### Trap 3: the capture's line numbering, not the PDF's page layout, is the anchor space

Anchors are line numbers in the **collapsed text snapshot** (1869 lines), not PDF pages and not the raw `pdftotext` line numbers. Verified anchors (all `occ=1`, `anchor=N-ok`, all ≤25 words): `we close this gap and present the first fuzzer` @33; `we develop our own intermediate language` @215; `Superion, a state-of-the-art open-source fuzzer` @129; `designed our approach called Fuzzilli specifically for finding` @1080; `we were not able to directly compare our approach to SoFi` @225; `Park et al. [36] proposed DIE, a novel` @276; `https://dx.doi.org/10.14722/ndss.2023.24290` @60. Word counts 2–11, all under the 25-word bound.

### Trap 4: the title and the author name cannot be quoted in their ordinary spellings

`FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities` → `occ=0` (the capture has `F UZZILLI: …`). `Samuel Gross` (ASCII) → `occ=0` (the capture has `Samuel Groß`). Quote the capture's own bytes or not at all.

### End-to-end shape validation (scratch fixture, never in the lane tree)

A miniature lane was built in scratch (registry row with bare-DOI source cell, `corpus/source-snapshots/round-75/{S110.txt,manifest.json}`, a `knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md` entry carrying `source: S110 — …` / `verified-at:` / `ground: F53` / `recheck: …` and an `S110.txt:33` citation, and a `corpus/README.md` frontier table row `| F53 | … | admitted | \`knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md\` | S110 | … |`):

```
python3 <lane>/corpus/instruments/frontier-recheck-count.py --root <scratch>/fx2
```
→ `FRONTIER-CENSUS rows=2 admitted=2 closed=1 problem-rows=1 registry=1`, `FRONTIER-PASS F53 ids=S110`, `PASS F53 knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md ids=S110 exit=0`, `entries=2 pass=1 exit=1`.

The `exit=1` is **the fixture's F52 row failing**, not F53: the fixture deliberately carries a real `| F52 |` row whose entry file was not copied into the miniature lane, so F52 reports `missing-entry` / `source-id-absent:S109`. **F53 itself PASSES with exit=0.** The takeaway for the L1: the F53 row shape (entry path in the `entry` cell, `S110` in the `sources` cell, `admitted` status, one `source:` header line, one `recheck:` line whose `--manifest` and `--source` resolve) satisfies the frontier counter's five contract limbs.

Also validated: `source-recheck.py --manifest <fixture>/manifest.json --source S110` → 7 OK lines (`sha256 OK` + 6 `Q-*-OK … anchor=N-ok`), **exit 0**, both from the fixture cwd and from a foreign cwd (`cd /` — exit 0). This is the shape B5 requires.

Note on the `recheck:` line: the frontier counter executes it with `bash -c` and `cwd=root` (`frontier-recheck-count.py:269`), and its `RECHECK_MANIFEST` regex takes the `--manifest` token relative to that root. The lane's existing entries all use the `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-NN/manifest.json --source SNNN` form (F41/S093, F51/S108, F52/S109). The C2 `entry_recheck` clause names the same form for S110.

---

## Remaining unknowns (not resolvable by this seat)

1. **Whether the L1 will keep lead line 175 byte-identical or amend it.** claims.json says "kept byte-identical as history"; the lead's own text ("the capture carries no URL for it") is now substantively false. I have recorded both the byte-preservation fact (hashes, base==freeze) and the lane's own reconciliation precedent (line 250, Registry-changes bullets). The choice is the L1's; the claims bind it, so the conservative reading is byte-identical + a supersession bullet elsewhere.
2. **The exact registry `scope` / `teaches` / `anchor` cell wording for S110** — a content decision, not a fact I can resolve; the F52 row's cell style is the template.
3. **Whether the `## Registry` table's row order matters for B2's "0 removed lines"** — base→freeze currently shows 0 added and 0 removed lines, so any *append-only* edit keeps that property; an in-place edit of line 175 would not, and would also contradict "kept byte-identical".
4. **Frontier row count:** `FRONTIER-CENSUS rows=52` at base; the claims' B6 says base `rows=52 admitted=52, entries=55 pass=55` and after `entries=56 pass=56` — so exactly one frontier row (F53) is appended to `corpus/README.md` (end-append per R6) and one `corpus/README.md` amendment section, plus one `PROVINCE.md` r75 line.

---

## Scratch hygiene

Scratch root `/fast/scratch/hyaku/kasegi-r75/ScoutSurface` was created explicitly and used for all fetches and fixtures (`TMPDIR` was never relied upon; `capture-source.py`'s own temp files are `NamedTemporaryFile` under the system temp and are deleted by its `finally: os.unlink`). **The scratch dir was deleted before yield** (`rm -rf -- /fast/scratch/hyaku/kasegi-r75/ScoutSurface`); the lane tree contains no scratch residue — the only files this seat wrote in the lane are `.ufo/waves/round-75/w1/ScoutSurface.md` and the evidence files named below.

## Evidence files (this seat's writes, all under `.ufo/waves/round-75/w1/`)

- `ScoutSurface.md` — this report.
- `ScoutSurface-evidence-sources.md` — every command + exit code + raw output quoted above, in one file.
