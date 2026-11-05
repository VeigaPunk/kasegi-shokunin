# ScribeEntry — round 77, wave 1 (kasegi)

Seat: `ScribeEntry` (scribe, leaf; no delegation, no background jobs). Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `2e53fc74776824898b5c5eb914aeddc19a091157`; freeze commit `539a43877809bd90b6f506e8fd24a6d871598cd5`.

**HEAD moved during the session.** Every measurement below was taken against the freeze bytes `539a4387`; while the seat was working the L1 landed `4a1ab1cdb12d8b7937a21f292dcc79530866b67a` ("round-77: record C1 and C2 NOT VERIFIED (honest stop); wave w1 evidence, lesson mistakes M77-1..9, SCORECARD and LOG"), which is now HEAD. The files this seat measured are **byte-identical across the two commits** — `git diff 539a4387 4a1ab1cd -- <path>` reports `changed=0` for `corpus/source-snapshots/round-77/S112.txt`, `corpus/source-snapshots/round-77/manifest.json`, `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `corpus/instruments/knowledge-expected.txt` and `corpus/instruments/source-recheck.py` — so every measurement stands at HEAD as well. The one file the landing commit changed among those this seat reads is `corpus/lessons/round-77.md`; every lesson line cited below (`:5`, `:13`, `:14`, `:41`, `:51`) was re-read at `4a1ab1cd` and holds there.

**Outcome: C2 is NOT admitted this round.** The L1 (KasegiR77) refused C2 on 2026-11-05 because the frozen predicate B6 fails the R125 admitted-entry sweep (`corpus/lessons/round-77.md:5`, reject line `:13`, mistake M77-5 `:41`, routed fix R-77-C `:51`). The four drafts this seat was asked to produce exist as wave-dir evidence only; **none of them is a landing surface and none was applied**. The lane tree was not modified: the only files written are the seven files under `.ufo/waves/round-77/w1/` named below.

## Artifacts (all under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-77/w1/`)

| file | what it is | applied? |
|---|---|---|
| `ScribeEntry.md` | this report | — |
| `entry-osv-post-v1-querybatch-contract.md` | the composed knowledge entry for `corpus/knowledge/osv-post-v1-querybatch-contract.md` (F54 / S112), with a banner marking it not-landed and not-fit-to-land, and naming the three rows that must be dropped | **no** |
| `readme-admission-block.md` | the `corpus/README.md` end-of-file `## Round-77 admission` block (coverage-map row + six-cell `F54` frontier row + count line), plus the refusal-variant count line | **no** |
| `province-f54-line.md` | the one-line `PROVINCE.md` end-of-file F54 Frontier amendment, shaped on the r75 F53 line | **no** |
| `expected-and-row-flip.md` | the `corpus/instruments/knowledge-expected.txt` row (with its INSERT placement) and the `corpus/SOURCES.md` S112 cell flips (`queued`→`mined`, `—`→`corpus/knowledge/osv-post-v1-querybatch-contract.md`) with the old→new registry-changes note | **no** |
| `ScribeEntry-recheck-S112.txt` | receipt: the frozen recheck command run at the lane root and from a foreign cwd (both rc=0) | — |
| `ScribeEntry-measurements.txt` | receipt: anchor-drift comparison across the three manifests, the B6 permitted-line set vs the manifest anchors vs the true quote locations, the `:194` coverage test, the manifest window coverage of the payload/request-sample/response regions, per-quote word counts and uniqueness, and the S112 row cell flip | — |

## Behavior

The seat's task was to draft the F54 admission surfaces for the OSV.dev `POST /v1/querybatch` contract on S112. It did so, then stopped on the L1's order once B6 was refused.

Work performed, in order:

1. Read the frozen bytes at the freeze commit: `.ufo/waves/round-77/claims.json` (C1/C2 predicates A1–A6, B0–B7, `located_anchors`), `corpus/source-snapshots/round-77/S112.txt` (216 lines, sha256 `f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907`), `corpus/source-snapshots/round-77/manifest.json` (13 quotes), the `S112` registry row (`corpus/SOURCES.md:124`), the r73 house-style entry (`corpus/knowledge/osv-post-v1-query-contract.md`), the r75 F53 block (`corpus/README.md:1177-1189`), the r75 F53 PROVINCE line (`PROVINCE.md:223`), and the r76 drafts as the placement precedent.
2. Ran the frozen recheck command at the lane root and from a foreign cwd — rc=0 both times (`ScribeEntry-recheck-S112.txt`).
3. Located every candidate ground clause in the capture and measured each quote's word count and occurrence count (`ScribeEntry-measurements.txt`): all 13 quotes occur exactly once and none exceeds 25 words.
4. Composed the four drafts listed above, each carrying its own placement header and the frozen provenance trio.
5. On the L1's stop order: annotated the entry draft with the not-landed banner, wrote this report, removed the scratch directory.

## Gates measured (results, not intentions)

| check | command | rc | result |
|---|---|---|---|
| frozen recheck, lane root | `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112` | 0 | `S112:sha256 OK` + 13 `OK occurrences=1 anchor=<n>-ok` lines |
| frozen recheck, foreign cwd | same, absolute paths, cwd = scratch | 0 | identical 14 lines, rc=0 |
| recheck line parses | `bash -n -c 'cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112'` | 0 | parses (`bash_n_ok`) |
| every draft quote unique in the capture | per-quote substring sweep over S112.txt | 0 | 13/13 occurrences=1; 0 quotes over 25 words |
| draft anchor cites resolve | `python3 -B corpus/instruments/anchorcheck.py .ufo/waves/round-77/w1/entry-osv-post-v1-querybatch-contract.md` | 0 | `3 in-range cite instances, 0 bad; 3 distinct anchors` (cites `corpus/SOURCES.md:123`, `corpus/knowledge/osv-post-v1-query-contract.md:75`, `corpus/instruments/source-recheck.py:110`) |
| rate-limit / quota / API-key / credential sentence | `grep -n -i -E 'rate limit\|ratelimit\|quota\|api key\|api_key\|authenticat\|credential' corpus/source-snapshots/round-77/S112.txt` | 1 | no match — the page states none |
| response-size sentence | `grep -n -i -E 'MiB\|size limit\|response size' corpus/source-snapshots/round-77/S112.txt` | 1 | no match — the 32 MiB clause stays with F51 (`S108.txt:148`) |
| time-based pagination trigger | `grep -n -i 'second' corpus/source-snapshots/round-77/S112.txt` | 1 | no match — the 20-second clause stays with F51 (`S108.txt:136`) |
| sibling-lane overlap (querybatch) | `grep -rli 'querybatch' <lane>/corpus/knowledge` for kasegi, kake, kengaku, chousa, kagi, tabi, souji | 0 | kasegi 1 file (F51's own Limits bullet), the other six lanes 0 files |
| registry rows / frontier rows / knowledge files at freeze | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` / `grep -cE '^\| F[0-9]+ \|' corpus/README.md` / `ls corpus/knowledge/*.md \| wc -l` | 0 | 112 / 53 / 91 (the S112 row is present at the freeze, `queued`) |
| expected-list shape at freeze | `wc -l` + `grep -cE '\.md$'` + `LC_ALL=C sort -c` | 0 | 93 lines / 91 `.md` rows, sort clean |

## Findings

**F1 (this seat's own finding, routed; frozen bytes not edited) — the round-77 manifest's declared anchors for two quotes are one line above the quoted text, and the frozen B6 permitted-line list inherits and extends the mismatch.**
Measured (`ScribeEntry-measurements.txt`, "anchor vs true line"):

- `Q04-params-same`: declared anchor **30**, quoted text actually on **S112.txt:31** ("The parameters are the same as those in POST /v1/query, but you can make multiple queries.").
- `Q05-pagination-instructions`: declared anchor **31**, quoted text actually on **S112.txt:32** ("Instructions are available for handling pagination for querybatch requests.").
- Every other quote in the manifest sits exactly on its declared anchor. The same sweep over the round-73/S108 manifest (31 quotes) and round-76/S111 manifest (13 quotes) reports `anchor_drift=[]` for both, so the drift is specific to the round-77 manifest.

Why it hides: `corpus/instruments/source-recheck.py:110` verifies an anchor against a four-line window, `raw_lines[max(0, anchor - 1):anchor + 3]`, so a quote one line below its declared anchor still prints `anchor=30-ok` / `anchor=31-ok` and the receipt looks clean. The `occurrences=1` path also makes the anchor advisory (`corpus/instruments/source-recheck.py:192` only fails a *non-unique* quote whose anchor is broken). A reader who opens the capture at the declared line finds the section heading "Parameters" (`S112.txt:30`) instead of the quoted sentence.

Consequence for the frozen predicate: the B6 permitted-line list (`claims.json` → `C2.predicate.B6`, and `C2.located_anchors`) reads "S112.txt lines 24, 30, 31, 34, 35, 36, 166, 168, 169, 170, 194 and 195". Measured against reality that list is wrong in three ways:

- it **admits `:194`**, which no manifest quote covers: the nearest anchor is 195, whose window is lines 195–198, so `:194` falls outside every anchor window (measured: `is line 194 inside any manifest anchor window (anchor..anchor+3)? False`). A clause grounded at `:194` (the "each result has a distinct next_page_token" sentence) cannot be verified by the named recheck line at all;
- it **excludes `:32`**, the true location of the `Q05-pagination-instructions` quote, so an entry that cites that quote where it actually sits violates the frozen list;
- it carries the drifted `:30` and `:31` forward as if they were the Q04/Q05 locations.

The frozen manifest and predicate are attacked here, never edited. A successor that fixes the predicate should list the true quote locations (`24, 31, 32, 34, 35, 36, 166, 168, 169, 170, 195`) and either pin `:194` in the manifest or drop it from the permitted set; and the manifest anchors for Q04/Q05 should be moved to 31/32 (or the instrument's window narrowed) so the receipt stops printing an `anchor=N-ok` for a line that does not hold the quote.

**F2 (confirms the L1's refusal) — three of the thirteen clauses restate ground already held in admitted F51.**
`corpus/lessons/round-77.md:13` (L1 reject line) and `:41` (M77-5) record the R125 sweep result; the seat re-verified the cited held-ground locations independently: `corpus/knowledge/osv-post-v1-query-contract.md:21` carries the version rule ("Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both." `S108.txt:40`) and the 400 ("Requests that specify the version in both places return 400 Bad Request." `S108.txt:41`); `:47` carries the pagination trigger and the page-size sentence ("The page size can vary slightly because of threading and may change in the future." `S108.txt:136`). The batch page's `S112.txt:35`, `:36` and `:170` say the same three things. **The seat's composed entry draft repeats exactly this defect** — rows C6, C7 and C11 claim those three clauses — and the draft's banner says so explicitly, so a successor does not lift them unchanged. The successor's claimed set should be the batch-specific clauses only: Q01–Q06, Q09–Q11, Q13, with Q07/Q08/Q12 cited as held.

**F3 (drafting consequence, recorded so the next round does not repeat it) — the payload/response JSON regions carry no pinned ground.**
The `S112` registry row's scope cell claims "the queries-array payload" and its anchor cell reads "POST /v1/querybatch page, lines 24-36 and 166-195" (`corpus/SOURCES.md:124`). Measured: the payload JSON block sits at `S112.txt:37-61` — outside that anchor range — and the manifest's anchor windows cover only lines 37–38 of it; the request sample (`:63-83`) and the sample 200 response (`:84-164`) are covered by no manifest quote window at all. So a batch-payload claim can only be grounded on the prose at `:24` ("Query for multiple packages (by either package and version or git commit hash) at once."), not on the JSON. The composed draft takes that route and records the JSON regions in Limits as excluded, with their line spans named.

**F4 (measurement hygiene, no defect) — the drafts' own citations stay inside the capture and the lane.**
`anchorcheck.py` on the composed entry reports 3 in-range cite instances, 0 bad. Every `S112.txt` line the draft cites resolves to real text in the frozen capture (24, 31, 32, 34, 35, 36, 166, 168, 169, 170, 194, 195 as ground and quoted clauses; 37-61 and 84-164 named as excluded regions in Limits). No draft instructs a call against osv.dev or any other host, and none carries credential material, a private URL or a vault URI.

## Touched surfaces

Write-only, all inside `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-77/w1/`: the seven files listed in §Artifacts. Read-only everywhere else: `git -C … rev-parse / log / status / show / ls-tree / diff` (no mutating git or jj command was run; no commit, push, stash, checkout, switch, reset or pull), and file reads under `corpus/` and `.ufo/waves/round-77/`. No write outside the wave dir and the seat's own scratch dir; the scratch dir `/fast/scratch/hyaku/kasegi-r77/ScribeEntry-21/` was removed before this report was filed. No tool was installed or upgraded in this session (the 2026-10-19 tooling authorization was not exercised; the host-wide pacman pause was untouched). `MANIFEST.json`, the fleet root's `templates/` and `scripts/`, `.ufo/state/`, `.ufo/watchdog.log`, sibling repos and `/home/vgpnk/Projects/shokuknow` were not written.

## Out of scope / not done

- **C1** (the recheck-cwd census counter amendment): this seat's seat spec is the C2 drafting surface only; C1 was not scored, measured or touched here. Other seats' C1 receipts are in the same wave dir and are not mine to summarize.
- **No admission, no landing.** The `F54` README row, the PROVINCE line, the expected-list row and the S112 registry cell flips are **not** applied; `corpus/SOURCES.md:124` remains `queued` with `used-by —`; `corpus/instruments/knowledge-expected.txt` remains 93 lines / 91 `.md` rows; `corpus/README.md` remains 53 frontier rows and `PROVINCE.md` remains 223 lines. The B3 counter `FRONTIER-CENSUS rows=54 admitted=54 … registry=112` was therefore **not** re-measured at a landing tree, because no landing tree exists this round; it is a successor's check.
- **Landing state verified at HEAD, not assumed.** Re-read at `4a1ab1cd` (`git show 4a1ab1cd:<path>`): registry rows 112, frontier rows 53, `PROVINCE.md` 223 lines, `knowledge-expected.txt` 93 lines; `corpus/SOURCES.md:124` status cell `queued`, used-by cell `—`; `grep -c '^| F54 ' corpus/README.md` → 0; `git show 4a1ab1cd:corpus/knowledge/ | grep -c 'osv-post-v1-querybatch'` → 0 (no entry file was landed). The diff of the S112 row between the freeze and the landing commit is empty (`git diff 539a4387 4a1ab1cd -- corpus/SOURCES.md | grep -c '^[+-]| S112'` → 0).
- **Nothing about the four sibling endpoint pages** (`GET /v1/vulns/{id}`, the three `/v1experimental/` pages): not captured, not claimed. The L1's reject line (`corpus/lessons/round-77.md:14`) routes them to a successor round with their own captures.
- **No mutation of any frozen byte.** `claims.json`, `c1-amended-reference.py`, `c1-mutant-transforms.md`, `controls/`, the S112 capture, the round-77 manifest and the `S112` registry row are as committed at `539a43877809bd90b6f506e8fd24a6d871598cd5`; the only changes anywhere are the seven files above.

## Findings summary for the judge

1. C2 is not admitted this round; the L1's B6 refusal is reproduced and its three restated clauses (Q07 `:35`, Q08 `:36`, Q12 `:170`) are confirmed as already held by F51 (`:21`, `:47`).
2. The round-77 manifest carries two one-line-high anchors (Q04 → declared 30/actual 31; Q05 → declared 31/actual 32) that `source-recheck.py`'s four-line anchor window (`corpus/instruments/source-recheck.py:110`) reports as `anchor=30-ok`/`anchor=31-ok`; the round-73 and round-76 manifests show no such drift.
3. The frozen B6 permitted-line set admits `:194` (unpinned, outside every manifest anchor window) and excludes `:32` (the true location of Q05) — the predicate is not satisfiable as written against the capture, independently of the distinctness failure.
4. The batch-payload and response JSON regions (`S112.txt:37-61`, `:63-83`, `:84-164`) carry no pinned manifest ground, so the payload clause is groundable only on the prose at `:24`.
5. Four drafts exist as evidence in this wave dir and are marked not-landed; nothing in the lane tree was modified.
