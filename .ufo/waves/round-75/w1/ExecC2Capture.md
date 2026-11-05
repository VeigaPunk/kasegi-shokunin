# ExecC2Capture — round 75, attempt 1, wave w1 — C2 (F53 / S110) draft fragments

Seat: ExecC2Capture (executor leaf). Scope: scratch-only C2 admission drafts for S110 (NDSS 2023 Fuzzilli paper). No lane file was written; the L1 (KasegiR75) owns every landed byte. No git/jj mutation. No tool installed (pdftotext and curl were already on the host; pacman not used).

Verdict on my scope: steps 1-4 done, all reported numbers carry their command and exit code below. C2 is NOT verified here by design (B1-B8 are integration checks owned by the L1).

## 1. Capture (step 1)

Command: `python3 corpus/instruments/capture-source.py --id S110 --url https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf --kind pdf --out $S/S110.txt` (run from the scratch cwd). Exit 0. Fallback (DOI landing) NOT needed.

Full tool stdout:
```
S110 status=200 fetched_bytes=918189 snapshot_bytes=88072 sha256=0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef utc=2026-11-05T09:51:07Z out=/fast/scratch/hyaku/kasegi-r75/ExecC2Capture/S110.txt
```
- The tool prints no line count. Line count 1869 = newline-byte count of the snapshot (Python `bytes.count(b"\n")`, equivalent to `wc -l`), exit 0.
- Final URL and content type came from one GET of the named PDF: `curl -sS -L -o /dev/null -w '%{http_code} %{url_effective} %{content_type} %{size_download}' <URL>` → `200 <same URL> application/pdf 918189`, exit 0. Matches the freeze-time receipt (918189 bytes).
- Known capture artifact: the PDF text layer renders the title as `F UZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities` (ligature split by pdftotext). The quotes are byte-exact to the snapshot, so the artifact is carried into the quote; the knowledge entry must name the paper's title as FUZZILLI and must not present the snapshot spacing as the title.

## 2. Manifest draft (step 2)

Scratch original: `$S/manifest-r75-S110.json`; evidence copy: `.ufo/waves/round-75/w1/ExecC2Capture-manifest-r75-S110.json` (sha256 093ce890aea2708b59d5799dc2d5ab8e3b948e43c50163682979880f7aa38b34, 5252 bytes).

Shape copied from `corpus/source-snapshots/round-74/manifest.json`: top-level `schema_version`, `note`, `sources[]`; record fields `id, url, capture_url, http{status, final_url}, kind, fetch_method, fetched_utc, path, sha256, bytes, lines, quotes[{id, quote, anchor}]`.
- url = capture_url = `https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf` (byte-equal to the capture URL).
- http.status = 200 (tool); final_url from the curl GET above.
- fetched_utc = `2026-11-05T09:51:07Z` (tool `utc=`).
- sha256 = 0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef; bytes = 88072; lines = 1869; path = `S110.txt`.
- 24 quotes, each a single-line byte-exact substring of the snapshot, each with its capture line anchor (1-based), no `|` character, every quote ≤ 25 words, longest = 12 words (Q07, Q10, Q20), shortest normalized length 12 chars (Q04 `Martin Johns`).

| id | anchor line | words | occurrences (normalized) | covers |
|---|---|---|---|---|
| Q01-title | 1 | 8 | 1 | title (`F UZZILLI: …`, artifact above) |
| Q02-author-bernhard | 4 | 2 | 1 | author block |
| Q03-author-holz | 11 | 2 | 3 | author block (non-unique, anchor verifies) |
| Q04-author-johns | 12 | 2 | 2 | author block (non-unique, anchor verifies) |
| Q05-venue | 57 | 8 | 1 | NDSS 2023 venue |
| Q06-doi | 60 | 1 | 1 | DOI 10.14722/ndss.2023.24290 |
| Q07-design-first-fuzzer | 33 | 12 | 1 | abstract design claim: first fuzzer on JIT vulnerabilities |
| Q08-design-ir | 35 | 8 | 1 | abstract design claim: IR design and implementation |
| Q09-design-ir-focus | 36 | 9 | 1 | abstract: IR focused on JIT compiler vulnerabilities |
| Q10-lift-javascript | 704 | 12 | 1 | IR lifts to JavaScript (§IV-B) |
| Q11-coverage-guided | 887 | 10 | 1 | coverage feedback (§IV-E) |
| Q12-compare-superion | 128 | 8 | 1 | comparison to other fuzzers (intro) |
| Q13-compare-comprehensive | 140 | 7 | 1 | comparison statement (intro contributions) |
| Q14-compare-superion-sota | 142 | 5 | 1 | comparison: Superion as state of the art |
| Q15-compare-competing | 1126 | 8 | 1 | comparison: vulnerabilities that eluded competing fuzzers (§VI-A) |
| Q16-comparability-caveat | 1080 | 8 | 1 | paper's own comparability caveat (§VII) |
| Q17-engines-v8 | 868 | 8 | 1 | three engines (V8) |
| Q18-engines-jsc-sm | 869 | 5 | 1 | three engines (JavaScriptCore, SpiderMonkey) |
| Q19-window-section | 872 | 9 | 1 | evaluation window, six months (§VI-A) |
| Q20-window-abstract | 38 | 12 | 1 | evaluation window, six months (abstract) |
| Q21-count-abstract | 39 | 8 | 1 | vulnerability count: 17 confirmed (abstract) |
| Q22-count-conclusion | 1377 | 7 | 1 | vulnerability count: 17 previously unknown (conclusion) |
| Q23-count-table | 1041 | 9 | 1 | vulnerability count: 17 with CVE or internal issue (§VI) |
| Q24-age | 1378 | 9 | 1 | age of the found vulnerabilities (conclusion) |

Notes for the L1:
- The abstract does not use the words "coverage-guided"; the coverage-feedback statement is §IV-E (Q11, line 887). The knowledge entry must cite Q11 for that, not the abstract.
- "Samuel Groß" is NOT quoted: 11 normalized characters, below `MIN_QUOTE_CHARS = 12` in `source-recheck.py` (a shorter quote is rejected by the instrument). The first author is therefore covered only by the title/venue quotes and the DOI, and the knowledge entry must not claim a pinned quote for him.
- Q16 is quoted from the single line 1080 (the sentence begins on line 1079 with `We`; the pinned quote starts at `designed`, so it is single-line byte-exact).

## 3. Self-validation (step 3)

Command (cwd = scratch): `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest $S/manifest-r75-S110.json --source S110` → **exit 0**. Output: `S110:sha256 OK` and 24 × `OK occurrences=… anchor=N-ok` (full text in `.ufo/waves/round-75/w1/ExecC2Capture-recheck.txt`, sha256 f6af72ce1bc980b4d5185a8d1673031e15cfdfa86628f04a0497767deea8a9b7).
- Longest quote word count: **12** (`python3`, `len(q.split())`, exit 0).
- Negative control (scratch-only copy with Q01 text altered to a non-existent string): exit **1**, `S110:Q01-title MISMATCH reason=quote-not-found`. The instrument is therefore not passing vacuously.
- Snapshot copy in the wave dir is byte-identical to the scratch snapshot (`copy_snapshot_sha_matches=True`, sha256 0780beae…51ef).

## 4. Distinctness sweep (step 4, B8 narrowed screen)

Sweeps (grep tool, exit as tool reports):
- `ndss|NDSS` over `kasegi-shokunin/corpus/SOURCES.md`: matched lines 121 (S109 row), 134 (search-log), 175 (Leads: the NDSS lead itself), 270 (round-74 note).
- `Fuzzilli|fuzzilli` over the same file: matched lines include 100 (S093 row), 121 (S109 row), 134, 173, 175, 245, 247, 250, 253, 255, 267, 270 (match-marked lines in the sweep output).
- `(?i)fuzzilli` over `revenger-shokunin/corpus`: **No matches found** (path confirmed to exist via glob).
- `S110` over `kasegi-shokunin/corpus/SOURCES.md`: **No matches found** (lane registry has no S110 at all).
- `JIT Compiler Vulnerabilities|ndss2023|10\.14722|NDSS Symposium` over `kasegi-shokunin/corpus`: hits only in SOURCES.md 174-175, knowledge `fuzzilli-js-engine-fuzzing-framework.md` line 73, source-snapshots/round-74 S109.txt line 243 and manifest.json line 98, lessons/round-74.md lines 13-14 — all S109 README references or lead bookkeeping; none is a holding of the NDSS paper.

Per-hit verdicts (SOURCES.md):
| line | subject | verdict |
|---|---|---|
| 121 | S109 row: Fuzzilli README | distinct; the row says "not the NDSS 2023 paper's content" (read raw) |
| 100 | S093 row: Project Zero Fuzzilli-vs-BigSleep comparison (2026-Oct-27) | distinct subject (production pipeline comparison on V8, against BigSleep). It also contains "six-month production window": NOT the NDSS evaluation window. Q19/Q20 must be attributed to the NDSS paper only. |
| 175 | the NDSS 2023 Fuzzilli paper as an unopened lead (named at S109.txt:243, no URL) | the lead this round advances; kept byte-identical as history per claims.json C2 target |
| 270 | round-74 registry note: "the NDSS paper [is] added as leads only (no row, no evidence)" | history; no holding |
| 134 | round-61 search log: "unopened Fuzzilli docs not needed or counted as screened" | history; no holding |
| 173, 245, 247, 250, 253, 255, 267 | Fuzzilli primary-docs lead bookkeeping, S093 row addition, lead reconciliation | history of S109/S093; no holding |

Revenger (read-only, `revenger-shokunin/corpus/SOURCES.md`):
- S117 = DecFuzzer (ISSTA'20 artifact, decompiler testing, line 132): distinct subject (decompiler correctness, not JIT).
- S396 = trailofbits/mishegos (x86 decoder differential fuzzer, line 411): distinct subject.
- Revenger NDSS hits are other papers: S114 (NDSS 2015, DREAM goto-free structuring, line 129), S341 (NDSS'25 firmware corpora, DOI 10.14722/ndss.2025.230669, line 356), S363 (DeGPT, NDSS 2024, line 378). None mentions Fuzzilli; the revenger case-insensitive sweep returned no Fuzzilli hit at all.

Conclusion (B8): the paper's design/comparison/evaluation ground is distinct from S109, S093, S117 and S396. No registry row or sibling row holds the NDSS 2023 paper; the registry has it only as a lead (line 175) and as the S109 exclusion. The B8 narrowed screen does not claim that no sibling holds fuzzer documentation (per the claim text), and the verdicts above are the round-lesson Gate record the claim asks for.

Sibling-ID note for the L1 (not a lane collision): revenger's registry uses `S110` for its own disassembly-slice row(s) (its SOURCES.md line 571 names slice rows "S110–S133"). This is a separate repo; the lane's S110 is unused (verified above).

## 5. Proposed registry row (fragment for the L1 — NOT written)

`| S110 | NDSS Symposium 2023, "FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities" (Groß, Koch, Bernhard, Holz, Johns; DOI 10.14722/ndss.2023.24290) — https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf | paper | A | the paper's own statements on its IR-based JIT fuzzing design (abstract and §IV), its comparison to Superion and to the other fuzzers it names (intro, §VII), the six-month evaluation window and the three engines (§VI-A), and its 17 reported vulnerabilities; not the Fuzzilli README (S109), not Project Zero's comparison post (S093), not any listed CVE's specifics, and not any live fuzzing | capture corpus/source-snapshots/round-75/S110.txt (sha256 0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef, 1869 lines, 88072 snapshot bytes, fetched 2026-11-05T09:51:07Z; 24 pinned quotes in corpus/source-snapshots/round-75/manifest.json; title line renders as "F UZZILLI" in the pdftotext layer) | mined | 2026-11-05 | 90d | corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md |`

Registry arithmetic the L1 must check (not run here): 109 → 110 rows; the S110 id is new.

## 6. What the L1 must run at integration (not run by me)

- Copy `ExecC2Capture-S110.txt` → `corpus/source-snapshots/round-75/S110.txt` and `ExecC2Capture-manifest-r75-S110.json` → `corpus/source-snapshots/round-75/manifest.json` (both byte-identical to my scratch files; verify sha256 before copying: snapshot 0780beae…51ef, manifest 093ce890…b34).
- B5 from a foreign cwd: `cd <foreign> && python3 <lane>/corpus/instruments/source-recheck.py --manifest <lane>/corpus/source-snapshots/round-75/manifest.json --source S110`, expect exit 0.
- B1, B3, B4, B6, B7 per claims.json (grep counts, knowledge count, capture-binding-check, frontier-recheck-count, sources-census.sh validate).
- B8 verdicts above go into the round lesson Gate.
- Entry first recheck line exactly as claims.json `entry_recheck`.

## 7. Tools and blockers

- Tools used: `python3` (host), `/usr/bin/pdftotext` (already installed, not installed or upgraded by me), `curl` (already installed). No install, no upgrade, no pacman, no sudo. Nothing added to any PATH directory.
- Blockers: none for the drafts. Risk: the title artifact (above) and the unquoted first author (above) must be disclosed in the entry, not hidden.
- Scratch dir `/fast/scratch/hyaku/kasegi-r75/ExecC2Capture/` removed after this report and the evidence copies were written (see last line).

Evidence under this dir: `ExecC2Capture-S110.txt`, `ExecC2Capture-manifest-r75-S110.json`, `ExecC2Capture-recheck.txt`, `ExecC2Capture-capture-stdout.txt`.
