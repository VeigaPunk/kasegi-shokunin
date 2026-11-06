# ScoutDistinct — B6 paraphrase distinctness sweep for C2 + live re-open of S113

Seat: ScoutDistinct (leaf, read-only). Wave: round-79 attempt 1, w1.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scratch: `/fast/scratch/hyaku/kasegi-r79/ScoutDistinct` (removed at exit).
Lane tree, corpus/, SKILL.md, PROVINCE.md, SCORECARD.md, LOG.md and all instruments were read only; nothing outside this wave dir was written. No git/jj writes. No tools installed.

---

## 1. Live fetch record (S113)

Command exactly as specified:

```
S=/fast/scratch/hyaku/kasegi-r79/ScoutDistinct
cd "$S"
curl -sS -A 'kasegi-shokunin/1.0' -o "$S/page.html" \
     -w '%{http_code} %{size_download}\n' \
     https://google.github.io/osv.dev/post-v1-determineversion/
```

**Result: `200 30242`** — HTTP status 200, 30242 bytes downloaded.

Fetched-raw sha256 (the HTML as served, before normalization): `44ec2ce41919899fee5e8d22706e782d2ccba89f6ab6b06bf741569e3b947aa7`.

### Normalization

Reproduced the committed instrument `corpus/instruments/capture-source.py` exactly (its `html_to_text` + `collapse` pair, read from the instrument source at `corpus/instruments/capture-source.py:34-53`): strip `<script>`/`<style>` blocks, break lines on closing `p|div|li|tr|h1-h6|section|article|br` and `<br>`, strip remaining tags, decode HTML entities, collapse horizontal whitespace per line, drop empty lines, join with `\n`.

| artefact | bytes | lines | sha256 |
|---|---|---|---|
| live raw page (curl) | 30242 | — | `44ec2ce4…3b947aa7` |
| live normalized text | 5669 | 127 | `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf` |
| committed snapshot `corpus/source-snapshots/round-79/S113.txt` | 5669 | 127 | `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf` |
| manifest `round-79/manifest.json` → `sources[0].sha256` | — | — | `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf` |

**The live normalized text is byte-identical to the frozen snapshot** (`live == snap` → True; same 30242 raw bytes the manifest records: "raw page 30242 bytes, snapshot 5669 bytes"). The served page has not drifted since the 2026-11-06T18:43:10Z capture.

### Per-quote occurrence counts (live normalized text)

Each of the eight manifest quotes occurs **exactly once** in the live normalized text, on the same line number as its declared anchor and as its line in the frozen snapshot.

| quote id | manifest anchor | live occurrences | live line | snapshot occurrences | snapshot line |
|---|---|---|---|---|---|
| Q01-purpose | 25 | 1 | 25 | 1 | 25 |
| Q04-library-set | 41 | 1 | 41 | 1 | 41 |
| Q05-coverage-limit | 41 | 1 | 41 | 1 | 41 |
| Q06-ranked-versions | 55 | 1 | 55 | 1 | 55 |
| Q07-file-hashes | 61 | 1 | 61 | 1 | 61 |
| Q08-hash-encoding | 62 | 1 | 62 | 1 | 62 |
| Q09-extensions | 66 | 1 | 66 | 1 | 66 |
| Q10-response-order | 85 | 1 | 85 | 1 | 85 |

Sum over the eight quotes of live occurrences = **8**; over the frozen snapshot = **8**. No quote is missing, duplicated, or relocated.

### Supporting B0 re-run (read-only, against committed bytes)

`TMPDIR=<scratch> python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-79/manifest.json --source S113` → **rc 0**:

```
S113:sha256 OK
S113:Q01-purpose OK occurrences=1 anchor=25-ok
S113:Q04-library-set OK occurrences=1 anchor=41-ok
S113:Q05-coverage-limit OK occurrences=1 anchor=41-ok
S113:Q06-ranked-versions OK occurrences=1 anchor=55-ok
S113:Q07-file-hashes OK occurrences=1 anchor=61-ok
S113:Q08-hash-encoding OK occurrences=1 anchor=62-ok
S113:Q09-extensions OK occurrences=1 anchor=66-ok
S113:Q10-response-order OK occurrences=1 anchor=85-ok
```

Instrument note (`corpus/instruments/source-recheck.py:85-95`, `anchor_verdict`): the anchor check is `anchor=N-ok` = the declared anchor verifies. Independently of the instrument's semantics, I confirmed by direct string search of the live normalized text that each quote sits on exactly the declared line (the open R-77-D window-semantics question in `corpus/lessons/round-78.md:39` does not affect this manifest — all eight quotes are exactly on their declared lines, so the four-line window and the exact line agree).

---

## 2. B6 literal distinctness (frozen predicate half)

Frozen B6 requires: `grep -F -l` over `corpus/knowledge/*.md` excluding the new entry returns zero files for each of the eight quotes (measured 0/8 at freeze).

The new entry `corpus/knowledge/osv-determineversion-cc-library-versioning.md` **does not yet exist** in the tree (`corpus/knowledge/*.md` = 92 files), so the exclusion is vacuous here; the measurement is over the 92 admitted entries as they stand.

Literal check performed in Python (exact substring, equivalent to `grep -F -l`) over all 92 admitted `corpus/knowledge/*.md`, for each of the eight quote texts, and again for each quote's **full anchor line** (a stricter form — the anchor line contains the quote plus surrounding page text):

| quote id | files containing the quote text | files containing the full anchor line |
|---|---|---|
| Q01-purpose | 0 | 0 |
| Q04-library-set | 0 | 0 |
| Q05-coverage-limit | 0 | 0 |
| Q06-ranked-versions | 0 | 0 |
| Q07-file-hashes | 0 | 0 |
| Q08-hash-encoding | 0 | 0 |
| Q09-extensions | 0 | 0 |
| Q10-response-order | 0 | 0 |

**Total literal hits: 0.** B6's literal count is zero; no literal-count kill.

---

## 3. Per-clause paraphrase (substance) sweep

### Search space

- All 92 admitted `corpus/knowledge/*.md`.
- `SKILL.md` (1251 lines).
- `corpus/README.md` (coverage map + frontier rows), `corpus/lessons/*.md` (including the round-76/77/78 lessons that already adjudicated this endpoint).

### Grep commands run (verbatim, from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

```
grep -li 'oss-fuzz\|ossfuzz\|fuzz' corpus/knowledge/*.md
grep -li 'sbom\|vendored\|md5\|hash\|library version\|upstream' corpus/knowledge/*.md
grep -li 'oss-fuzz\|ossfuzz\|fuzz' SKILL.md
grep -li 'sbom\|vendored\|md5\|hash\|library version\|upstream' SKILL.md
```

Result of the first form over `corpus/knowledge/*.md` (5 files, rc 0):

```
corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md
corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md
corpus/knowledge/osv-post-v1-query-contract.md
corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md
corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
```

`grep -oi 'fuzz[a-z]*' corpus/knowledge/osv-post-v1-query-contract.md` → `7 fuzzy`. That file's match is the substring "fuzz" inside "fuzzy" (the fuzzy version match), **not** fuzzing — not a fuzzing entry. The other four are genuine fuzzing entries and were read.

Second form over `corpus/knowledge/*.md` returned 36 files; the substance-bearing candidates (SBOM / dependency / vendored-library / version-identification) were `cyclonedx-analysis-subtree.md`, `evidence-dir.md`, `target-checkouts.md`, `multiparty-vulnerability-coordination.md`, `linux-kernel-security-bugs-reporting-process.md`, `osv-affected-range-events.md`, `osv-post-v1-query-contract.md`, `osv-post-batch-query-contract.md`, `openssf-scorecard-checks.md`, `ai-assisted-finding-validation.md`, and were read in full or swept line-wise.

Third form (`SKILL.md`, fuzz) → **rc 1, no match**: SKILL.md holds no fuzzing/OSS-Fuzz ground. Fourth form (`SKILL.md`, sbom/vendored/md5/hash/library version/upstream) → 1 file, SKILL.md itself; the only hits are `SKILL.md:1023` ("`~/Projects/bounties/pendle-core-v2-public/` — vendored hunt target (shallow clone, `f242659` = v6.10.0, pinned by `claims/cantina-pendle/…/provenance.json`)") and unrelated gate-hash rows (`SKILL.md:1113-1123`).

Narrowed substance sweeps run across `corpus/knowledge/*.md` + `SKILL.md`:

```
grep -ril 'oss-fuzz' corpus/knowledge/*.md                       -> 1 file
grep -ril 'ossfuzz'  corpus/knowledge/*.md                       -> 0 files
grep -ril 'md5'      corpus/knowledge/*.md                       -> 1 file
grep -ril 'base64'   corpus/knowledge/*.md                       -> 0 files
grep -ril 'file_hash' corpus/knowledge/*.md                      -> 0 files
grep -ril 'closest upstream' corpus/knowledge/*.md               -> 0 files
grep -ril 'source code hash' corpus/knowledge/*.md               -> 0 files
grep -ril 'sorted by how close' corpus/knowledge/*.md            -> 0 files
grep -ril 'possible versions' corpus/knowledge/*.md              -> 0 files
grep -ril 'not all .*packages are' corpus/knowledge/*.md         -> 0 files
grep -ril 'hash of every file' corpus/knowledge/*.md             -> 0 files
grep -ril 'file extension' corpus/knowledge/*.md                 -> 0 files
grep -ril 'upstream library' corpus/knowledge/*.md               -> 1 file
grep -ril 'ranked by' corpus/knowledge/*.md                      -> 1 file
grep -ril 'indexer' / 'API caller' corpus/knowledge/*.md         -> 0 files
grep -ril 'determineversion' corpus/knowledge/*.md               -> 0 files
grep -ril 'v1experimental' corpus/knowledge/*.md                 -> 0 files
grep -ril 'experimental endpoint' corpus/knowledge/*.md          -> 1 file
grep -ril 'sbom|vendored|md5|hash|library version|upstream' corpus/lessons/*.md SKILL.md corpus/README.md  (broad sweep)
grep -rn  'oss-fuzz' corpus/lessons/*.md                          -> corpus/lessons/round-61.md
grep -rn  'md5'       corpus/lessons/*.md                          -> corpus/lessons/round-35.md, round-9-aggregator-corpus-verdict.md
grep -rn  'determineversion' corpus/lessons/*.md                  -> round-76-verifier-spotcheck.md, round-77.md, round-78.md
grep -rn  'file hash' corpus/lessons/*.md                         -> round-30.md, round-31.md
grep -rn  'base64|file_hash|closest upstream|possible versions|sorted by how close' corpus/lessons/*.md SKILL.md corpus/README.md  -> 0 files
```

### The three named holders, read for the eight clauses

- **F51 `corpus/knowledge/osv-post-v1-query-contract.md`** (80 lines) — read in full. Its six claims are the /v1/query payload, the version rule, name matching, the Git-tag query, pagination, and the 32 MiB HTTP/1.1 limit. Its only "hash" mentions are the *commit* hash (`osv-post-v1-query-contract.md:9`, `:13` — "May also be queried by commit hash.", "The commit hash to query for") and "fuzzy" (7×). **No MD5, no file_hashes, no base64, no library-identification, no ranking.** Its Limits bullet at `:75` says the other endpoints "are listed, not described"; `corpus/source-snapshots/round-73/S108.txt:5-9` lists the endpoint *path strings* only.
- **F54 `corpus/knowledge/osv-post-batch-query-contract.md`** (92 lines) — read in full. Its seven claims are the batch definition, ids-and-modified-only return, input-matched ordering, partial next_page_token, the 1,000/3,000 counts, and the follow-up page_token rule. Its "hash" mentions are the git commit hash only (`:9`, `:13`, `:71`). **No file hashing, no library set, no version ranking.**
- **F31 `corpus/knowledge/osv-affected-range-events.md`** (121 lines) — the OSV *format* (ranges/events). Its only "SBOM" is a distinctness aside at `:111`; its scope limit (`PROVINCE.md:178`) excludes "the osv.dev service API" entirely.

### Per-clause verdict table

| clause | quote id | snapshot line | substance | verdict | basis |
|---|---|---|---|---|---|
| Purpose: source-code hashes of C/C++ libraries → closest upstream library and version | Q01 | 25 | identify an upstream library+version from the bytes of a local copy | **novel** | No admitted entry turns a source copy into an upstream library/version. The nearest admitted ground is `corpus/knowledge/target-checkouts.md:11`, `:19-20` — a *git commit pin* binds the vendored `pendle-core-v2-public` checkout to `f242659…` = v6.10.0. That is the opposite mechanism (exact commit SHA, one known repo, no search) and it says nothing about C/C++ libraries, closest-match, or upstream discovery. `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:18` ("A stable identifier such as a commit ID or an exact version is required") states that an identifier must be stable, not how to derive one from bytes. `corpus/knowledge/ai-assisted-finding-validation.md:11` ("identify the code or package version to which the finding applies") is an *evidence-checklist item*, not a mechanism. `grep -ril 'closest upstream' \| 'source code hash' \| 'file_hash'` → 0 files. |
| Identifiable-library set: the C/C++ projects integrated into OSS-Fuzz | Q04 | 41 | the *set* of libraries this endpoint can name is bounded by OSS-Fuzz integration | **novel** | The only admitted OSS-Fuzz ground is `corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md:26` — "OSS-Fuzz lacked generate_series, while fuzzingshell.c contained an older unaffected seriesBestIndex (S094.txt:112, Q4)": a *harness-configuration* fact about one SQLite fuzz target. `corpus/lessons/round-61.md:37` carries the same quote as Q4 of S094. Neither states that a library-identification service's coverage equals the OSS-Fuzz project set. The three Fuzzilli entries hold no "oss-fuzz" string at all. `grep -ril 'oss-fuzz'` over corpus/knowledge → 1 file, and that file's clause is the harness gap. **Note the split**: Q04 (the set) and Q05 (the limit) are one sentence pair at :41 and are held or not independently; the OSS-Fuzz-as-fuzzing-project fact at `project-zero-big-sleep-sqlite-variant-analysis.md:26` is not the same proposition as OSS-Fuzz-as-the-library-catalogue. |
| Coverage limit: not all C/C++ packages are represented in the database | Q05 | 41 | the identification service's coverage is partial | **novel** | No admitted entry states a coverage limit for a library/version-identification service. The admitted "coverage" hits are code-coverage senses (`fuzzilli-js-engine-fuzzing-framework.md:14`, `:39` — "(coverage-)guided fuzzer", "e.g. code coverage"; `project-zero-fuzzilli-vs-bigsleep-comparison.md`) and corpus-coverage senses. `grep -ril 'not all .*packages are'` → 0 files. F51's `osv-post-v1-query-contract.md:76` records that the fuzzy-match algorithm "names no method" — a *limit of F51's own claim*, not a coverage statement about a library catalogue. |
| Ranked-versions response: possible versions ranked by how well the version matched the local copy | Q06 | 55 | the service returns several candidate versions, ranked by match quality | **novel** | The only admitted "rank" is `corpus/knowledge/mission-ledger.md:42` (`RANKED` = EV-ranked by `ops/rank.mjs`) — the lane's own finding ledger, an unrelated ranking of hunts. F54's input-matched ordering guarantee (`osv-post-batch-query-contract.md:9`, "The response ordering will be guaranteed to match the input") is a *batch-response position* guarantee, not a match-quality ranking of candidate versions. F51's fuzzy match (`osv-post-v1-query-contract.md:23`, "A fuzzy match is done against upstream versions.") is a *request-side* one-version lookup, and `:76` explicitly records that no method is named — the opposite direction of travel. `grep -ril 'possible versions'` → 0 files. |
| Payload field: `file_hashes` = an array of MD5 hashes of each relevant file in the library to identify | Q07 | 61 | the request payload carries per-file MD5 hashes | **novel** | The only admitted "md5" is `corpus/knowledge/source-tree-loss-2026-09-28.md:172` — "output, md5 `ab25833e897822af3e87b371a3d4eeff`", a *checksum of the lane's own lost tree*, a single digest of an archive, with no per-file array, no file_hashes field, and no library identification. `grep -ril 'file_hash'` → 0 files; `grep -ril 'md5'` → 1 file (that one). |
| Hash encoding: the MD5 hash bytes encoded in base64 | Q08 | 62 | the encoding of the transmitted hash bytes | **novel** | `grep -ril 'base64'` over all 92 admitted entries → **0 files**. No admitted entry states any base64 encoding. |
| Hashed-file extension list: hash every file with the following extensions | Q09 | 66 | the caller walks the library dir hashing files of a named extension set | **novel** | `grep -ril 'file extension'` → 0 files; `grep -ril 'hash of every file'` → 0 files. The six extensions themselves (`.c .cc .h .hh .cpp .hpp`, S113.txt:67-72) appear in no admitted entry. Fuzzing corpus entries describe a *fuzzer's* corpus, not a caller's file-selection set for hashing. |
| Response order: an array of potential library matches sorted by how close the match is | Q10 | 85 | the response is an array of candidate library matches sorted by closeness | **novel** | `grep -ril 'sorted by how close'` → 0 files. F54's ordering guarantee (`osv-post-batch-query-contract.md:9`) is "the response ordering will be guaranteed to match the input" — an input-position guarantee, the opposite axis from closeness sorting. No admitted entry describes a *matches array*, a *score*, or a closeness sort. (`corpus/knowledge/openssf-scorecard-checks.md` holds a 0-10 aggregate score with its own scope limit, unrelated.) |

**Verdict summary: 8 novel, 0 partly-held, 0 held.** No clause restates admitted ground, so the B6 paraphrase half does not kill C2.

### Why the round-76 rejection of a determineversion C2 does not apply here

`corpus/lessons/round-76.md:11` rejected a r76 C2 with: "rejected as new ground: the six endpoint path strings and the api.osv.dev/v1/vulns/<ID> form — already held from S108.txt:5-9 (F51 Limits bullet, `corpus/knowledge/osv-post-v1-query-contract.md:75`)". The r76 verifier spot-check (`corpus/lessons/round-76-verifier-spotcheck.md:59-64`) says the same and names `POST /v1experimental/determineversion` among the *path strings* already held.

That rejection was of the **endpoint path string as new ground** — the identity of the endpoint, which F51 already lists. Round 79's C2 does not claim the path string as a new clause; it claims the endpoint's *contract clauses* (purpose, library set, coverage limit, ranked versions, MD5 file_hashes, base64, extension list, closeness-sorted matches), none of which any admitted entry states. The r77 lesson records the same requirement as an open lead: `corpus/lessons/round-77.md:14` — "one live slug captured with a located quote and its own distinctness sweep, in a successor round" — and `corpus/lessons/round-78.md:41` (R-77-F) keeps the three sibling endpoints open, "each needing its own capture, its own located quotes and its own distinctness sweep in a successor round". This seat's sweep is that distinctness sweep for the determineversion slug.

Two residual adjacency facts the L1 should weigh, both of which I judge **not** to be clause holdings:

1. `corpus/knowledge/osv-post-v1-query-contract.md:75` (F51's own Limits bullet) lists the experimental endpoints, including determineversion, as "listed, not described". An entry that re-states *the endpoint exists* would restate that; an entry that states its contract clauses does not.
2. The frozen manifest's own `note` records that the S113 lines **not** pinned are: the experimental-status line (:37), the query/querybatch follow-up pointer (:39), the case-sensitivity line (:64), and the sample-response values. The case-sensitivity line is separately held by F51 (`corpus/knowledge/osv-post-v1-query-contract.md:31`, "Case Sensitivity: API requests are case-sensitive."), and the follow-up pointer is a cross-reference to F51/F54 ground — the manifest correctly declines to pin them, and the C2 statement repeats that exclusion. Consistent.

### Observations for the L1 (findings, not verdicts)

- **B0/B5 live re-open is clean**: the served page is byte-identical to the frozen capture after the committed instrument's normalization, and the committed recheck prints `S113:sha256 OK` plus eight `OK occurrences=1 anchor=<n>-ok` lines, rc 0.
- **B6 literal half is clean**: 0/8 quote texts and 0/8 full anchor lines occur in any of the 92 admitted entries.
- **B6 paraphrase half is clean**: 8/8 clauses novel.
- **The new entry does not yet exist** in `corpus/knowledge/` (92 files). B2 expects 92 → 93 with `corpus/instruments/knowledge-expected.txt` at 95 lines/93 `.md` rows; the entry, the F55 coverage-map row, the F55 frontier row, and the S113 `status: queued → mined` / `used-by` flip are all still outstanding at the freeze tree. The S113 registry row already exists at `corpus/SOURCES.md:125` with `status: queued`, `used-by: —`, and the registry row count is **113** (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 113), matching B1/B3's frozen expectation. `F55` is not yet in `corpus/README.md`.
- **Unpinned but load-bearing line**: Q09's quote at S113.txt:66 is the sentence that introduces the extension list; the six extension literals sit on S113.txt:67-72 and are not covered by any pinned quote. A clause that claims "the hashed-file extension list" is therefore claimable from the pinned quote (which names the list as such) but the six literal extensions are not themselves evidence-pinned. If the entry enumerates `.c .cc .h .hh .cpp .hpp`, each should cite S113.txt:67-72 as the line range. This is a drafting observation for the entry author, not a B6 kill and not a change to the frozen manifest.
- **Manifest anchor integrity**: all eight quotes are exactly on their declared lines (independently re-derived by direct line search of the live normalized text), so the open R-77-D four-line-window semantics question (`corpus/lessons/round-78.md:39`) does not bite on this manifest.

## 4. Commands run (full list, for replay)

```
S=/fast/scratch/hyaku/kasegi-r79/ScoutDistinct; mkdir -p "$S"
cd "$S"; curl -sS -A 'kasegi-shokunin/1.0' -o "$S/page.html" \
  -w '%{http_code} %{size_download}\n' https://google.github.io/osv.dev/post-v1-determineversion/
sha256sum "$S/page.html"

cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR="$S" python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-79/manifest.json --source S113
ls corpus/knowledge/*.md | wc -l
grep -li 'oss-fuzz\|ossfuzz\|fuzz' corpus/knowledge/*.md
grep -li 'sbom\|vendored\|md5\|hash\|library version\|upstream' corpus/knowledge/*.md
grep -li 'oss-fuzz\|ossfuzz\|fuzz' SKILL.md
grep -li 'sbom\|vendored\|md5\|hash\|library version\|upstream' SKILL.md
# plus the narrowed -ril sweeps listed in §3
```

No counting command wrote outside TMPDIR. No lane instrument was run beyond the single named read-only `source-recheck.py` invocation; the lane's full gate suite was not run.

## 5. Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/ScoutDistinct.md` (this report)

Scratch directory `/fast/scratch/hyaku/kasegi-r79/ScoutDistinct` removed at exit. Nothing else was written; the lane tree is unmodified.
