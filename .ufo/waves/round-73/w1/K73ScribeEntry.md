# K73ScribeEntry — round 73, attempt 1, item C2 (frontier F51, OSV.dev POST /v1/query on S108)

Seat: K73ScribeEntry (scribe, leaf, no subagents). Item: C2 only — the F51 knowledge entry and its registry-side drafts. C1 (Q10 recheck cwd repair) is not mine and is not touched.
Mode: draft only. Nothing was written into the lane's `corpus/`, `PROVINCE.md`, `SCORECARD.md` or any git state. Lane tip observed read-only: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse --short HEAD` → `3b53ff8` (exit 0), the frozen commit.
Installs: none. Tools used: python3, bash, sha256sum, awk, sed, sort, diff, grep, the lane's own `corpus/instruments/capture-source.py`, `source-recheck.py`, `capture-binding-check.py` (read-only runs), and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (read-only). No pacman, no `~/.local/bin` write.

## 1. Result

Produced (all under `.ufo/waves/round-73/w1/draft/`, the wave report dir, not the lane corpus):

| file | content | bytes / lines |
|---|---|---|
| `draft/F51-entry.md` | knowledge entry for `corpus/knowledge/osv-post-v1-query-contract.md` (round-72 shape, Q1–Q6) | 10040 B / 80 lines |
| `draft/manifest.json` | `corpus/source-snapshots/round-73/manifest.json`, one record S108, 31 pinned quotes | 5427 B |
| `draft/SOURCES-S108-row.md` | the S108 registry row, 11 cells (NF=13 with edge pipes) | 1163 B, 1 line |
| `draft/README-r73-block.md` | append-only R6 block: coverage row, F51 frontier row, `[r73 amendment]` line | 2078 B |
| `draft/PROVINCE-r73-line.md` | the `[r73 Frontier amendment …] F51 — …` line, for end-of-file append | 739 B |
| `draft/evidence/K73ScribeEntry-verify.txt` | full transcript of the final verification run, with each step's exit code | 6753 B |
| `draft/evidence/{build.py,check_entry.py,final.sh}` | the scripts that produced the evidence | — |

Verified in scratch (`/fast/scratch/hyaku/kasegi-r73/K73ScribeEntry/`, not the lane): every pinned quote binds to its anchor line; the recheck command passes on a copy of the manifest and capture and fails on a one-quote-edited control; every prose quote in the entry is a manifest quote and an exact capture substring, under 25 words; the census accepts the S108 row (exit 0, zero E-lines); the knowledge-expected sorted insertion is line 66 of 91.

Not verified until the L1 lands the files (these depend on the lane's state, which I did not change): the lane-root recheck run from a foreign cwd, `frontier-recheck-count.py`, the C2 counters `FRONTIER-CENSUS`/`entries`/`capture records`, the 89-file count, and the in-lane census. The reason and the observed pre-landing values are in § 5.

## 2. Commands and exit codes (the evidence)

Every number below is the output of a command run in this seat; the transcript is `draft/evidence/K73ScribeEntry-verify.txt`.

| step | command (abridged) | exit | observed |
|---|---|---|---|
| capture re-run into scratch | `python3 corpus/instruments/capture-source.py --id S108 --url https://google.github.io/osv.dev/post-v1-query/ --out <scratch>/cap/S108.txt --kind html` | 0 | `status=200 fetched_bytes=33417 snapshot_bytes=6563 sha256=304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9 utc=2026-11-05T07:47:23Z` |
| capture byte-compare | `cmp <scratch>/cap/S108.txt corpus/source-snapshots/round-73/S108.txt` | 0 | identical bytes |
| capture facts | `sha256sum`, `wc -c`, `wc -l` on the lane capture | 0 | `304baa7d…12ffc6b9`, 6563 bytes, 150 lines |
| 31-quote binding | `python3 build.py` (grep -nF and occurrence count per quote) | 0 | `ALL_OK`; each quote on its anchor line, occurrences=1 |
| manifest JSON | `json.load` of draft manifest | 0 | 1 source, 31 quotes |
| recheck, positive | `source-recheck.py --manifest <scratch>/recheck-ok/manifest.json --source S108` (draft manifest + pinned capture) | 0 | `sha256 OK` and 31 × `Qnn … OK occurrences=1 anchor=N-ok` |
| recheck, negative control | same, capture with one quote line edited | 1 | `sha256 MISMATCH expected=304baa7d… actual=22ca95dc…` |
| entry quote check | `python3 check_entry.py F51-entry.md manifest.json S108.txt` | 0 | `prose_quotes=27 not_ok=0`; 5 JSON code spans all in manifest and capture; `manifest_quotes=31 unused_in_entry=[]` |
| word count (awk) | `sed 's/`[^`]*`//g' F51-entry.md \| grep -o '"[^"]*"' \| awk …` | 0 | `segments_le25=27`, no `OVER25` |
| recheck line parses | `bash -n -c "<recheck line>"` | 0 | parses; the `recheck:` line starts with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` (count 1) |
| knowledge-expected base sort | `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` | 0 | base sorted |
| knowledge-expected insert | cat base + entry, `LC_ALL=C sort` | — | `lines=91 rows=89 index=66`; `diff` base vs new = one added line (`65a66`) |
| README F-rows | `grep -cE '^\| F[0-9]+ \|'` before / after scratch append | 0 | before 50, after 51, F51 rows = 1 |
| census, draft row (scratch) | `sources-census.sh validate --root <scratch>/R4 <scratch>/R4/kasegi-shokunin` (SOURCES with S108 row after line 119, full knowledge tree, lessons link, entry copy) | 0 | `E-lines=0`, `S108-lines=0` |
| census, lane as-is | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | 0 | `kasegi ok …/corpus/SOURCES.md` |
| negative sanity | `grep -n -i 'rate limit\|ratelimit\|quota\|api key\|api_key\|authenticat\|credential' S108.txt` | 1 | no match (no rate-limit, quota, API-key or credential sentence on the capture) |
| capture-binding, lane as-is (read-only) | `capture-binding-check.py --root <lane>` | 1 | `FAIL rule=missing-manifest dir=round-73`; `records=86 bound=86 unbound=0`; also `orphan=S040-live.txt` (pre-existing) |
| recheck from foreign cwd, pre-landing (read-only) | `bash -c 'cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-73/manifest.json --source S108'` from a scratch cwd | 2 | `manifest UNAVAILABLE reason=missing` (fail-closed; the manifest is not yet in the lane) |

## 3. The 31 pinned quotes (manifest `quotes`, anchor = S108.txt line)

Each is an exact substring of its anchor line (grep -nF confirms one line each, occurrences=1). Word count is whitespace-split. All are ≤25 words (max 20). Every one is used in the entry (`unused_in_entry=[]`).

| id | line | words | quote (byte-exact) |
|---|---|---|---|
| Q01-scope | 24 | 14 | Lists vulnerabilities for given package and version. May also be queried by commit hash. |
| Q02-commit-param | 34 | 15 | commit string The commit hash to query for. If specified, version should not be set. |
| Q03-version-fuzzy | 35 | 8 | A fuzzy match is done against upstream versions. |
| Q04-version-exclusive | 35 | 14 | If set, commit must not be used, and package.purl must not include a version. |
| Q05-package-optional | 36 | 9 | When a commit hash is given, this is optional. |
| Q06-page-token-param | 37 | 15 | If your previous query fetched a large number of results, the response will be paginated. |
| Q07-version-rule | 40 | 14 | Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both. |
| Q08-both-places-400 | 41 | 12 | Requests that specify the version in both places return 400 Bad Request. |
| Q09-invalid-label | 47 | 4 | Invalid (400 Bad Request): |
| Q10-invalid-example | 48 | 9 | `{ "package": { "purl": "pkg:pypi/jinja2@3.1.4" }, "version": "3.1.4" }` |
| Q11-valid-example | 46 | 9 | `{ "package": { "purl": "pkg:pypi/jinja2" }, "version": "3.1.4" }` |
| Q12-case | 53 | 6 | Case Sensitivity: API requests are case-sensitive. |
| Q13-name-exact | 54 | 17 | Package names are matched exactly, except in ecosystems whose registry treats other spellings as the same package: |
| Q14-pypi | 54 | 9 | PyPI names are normalized as described in PEP 503, |
| Q15-nuget | 54 | 5 | NuGet names are matched case-insensitively, |
| Q31-crates | 54 | 6 | crates.io names are matched case-insensitively with |
| Q16-git-set | 56 | 19 | To do so, set the ecosystem to GIT, enter the full URL of the repository to the name field, |
| Q17-git-tag-field | 56 | 7 | and the tag into the version field. |
| Q18-git-example | 79 | 7 | `{"package": {"name": "https://github.com/curl/curl.git", "ecosystem": "GIT"}, "version": "8.5.0"}` |
| Q19-payload-commit | 59 | 2 | `"commit": "string",` |
| Q20-payload-page-token | 66 | 2 | `"page_token": "string"` |
| Q21-pagination-trigger | 136 | 20 | pagination will occur when there more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds. |
| Q22-token-mechanism | 135 | 19 | When pagination is used, the next_page_token is given in the response, indicating that there are more results to return. |
| Q23-repeat-until | 135 | 12 | repeating queries until the next_page_token is no longer included in the response. |
| Q24-next-page | 144 | 13 | To get the next page of results, your next request must include page_token: |
| Q25-rare-token-only | 149 | 10 | In rare cases, the response might contain only the next_page_token. |
| Q26-keep-querying | 149 | 18 | please keep querying with the next_page_token until either results are returned, or no more page tokens are returned. |
| Q27-size-http1 | 148 | 12 | The API has a response size limit of 32MiB when using HTTP/1.1. |
| Q28-size-http2 | 148 | 7 | There is no limit when using HTTP/2. |
| Q29-http2-recommend | 148 | 12 | We recommend using HTTP/2 for queries that may result in large responses. |
| Q30-page-size-vary | 136 | 15 | The page size can vary slightly because of threading and may change in the future. |

Note on the quote split: S108 line 148 carries 31 words in one sentence. It is split into Q27 (12 words) and Q28 (7 words) so each quote stays ≤25; the split is exact, with no words dropped.

## 4. The entry (F51-entry.md) — what it claims and where each claim lives

Header (the three lines directly under the H1, in the spec's order, round-72 blank-line spacing kept):
- `source: S108 — https://google.github.io/osv.dev/post-v1-query/ (anchor: the POST /v1/query page, capture corpus/source-snapshots/round-73/S108.txt)`
- `verified-at: 2026-11-05`
- `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-73/manifest.json --source S108` (one executable command; `bash -n` exit 0)

Body: Attribution; six claims (payload and commit query; version in one place and fuzzy match; exact name matching with three named ecosystems; Git-tag query; pagination; 32 MiB limit on HTTP/1.1 only); Distinctness (F31/S080, F25, F47/S103, F36/S087); Limits (rate limits and quotas, authentication, overview page, record format, other endpoints, fuzzy algorithm, tag matching, live state); Scope limit line. Each claim carries a falsifiable rule and a rejected over-generalization. Rejected over-generalizations are written without quote marks, so the only double-quoted strings in the entry are the 27 verified page quotes.

Q-criteria self-check against QUALITY.md (the lane's own bar):
- Q1: three header lines under the H1 in order; `recheck:` is a single command with the cd prefix (Q10 form).
- Q2: the only support is S108, tier A (row in § 6), opened in this round.
- Q3: 27 prose quotes plus 5 code spans, all located on their anchor lines; all ≤25 words.
- Q4: attribution kept — "the OSV.dev project's own reference page"; no generalized universal rule.
- Q5: a falsifiable rule and a rejected over-generalization in every claim.
- Q6: no call instructed; no curl; no credential or private URL; the entry states it made no query against osv.dev.

## 5. Placement for the L1 (exact) and what the lane looks like now

The L1 owns the lane. The drafts are placed as follows; I did not place them.
1. `corpus/knowledge/osv-post-v1-query-contract.md` ← `draft/F51-entry.md` (new file; the name is free, `ls corpus/knowledge | grep osv` shows only `osv-affected-range-events.md`).
2. `corpus/source-snapshots/round-73/manifest.json` ← `draft/manifest.json`, landed in the SAME commit as `corpus/source-snapshots/round-73/S108.txt`. Observed now: that directory is untracked (`git -C <lane> ls-files corpus/source-snapshots/round-73` prints nothing; `git -C <lane> status --porcelain -- corpus/source-snapshots/round-73` prints `?? corpus/source-snapshots/round-73/`). Until the manifest lands, `capture-binding-check.py` reports `FAIL rule=missing-manifest dir=round-73` (exit 1, § 2). This is the R20/R105 pattern; it must not land as a snapshot-without-manifest.
3. `corpus/SOURCES.md`: insert `draft/SOURCES-S108-row.md` after line 119 (the S107 row); the new row is line 120, and the blank line and `## Paths` heading shift down by one. The row's `used-by` cell names the entry path, which must exist on disk (census rule E11), so the entry lands first or in the same commit.
4. `corpus/README.md`: append `draft/README-r73-block.md` after line 1147 (the file ends in a newline; the block starts with a blank line). The F51 row is the 51st `^| F[0-9]+ |` row.
5. `PROVINCE.md`: append `draft/PROVINCE-r73-line.md` after line 217 (the current last line, the r72 amendment), with the blank line in the draft.
6. `corpus/instruments/knowledge-expected.txt`: insert `corpus/knowledge/osv-post-v1-query-contract.md` so that `LC_ALL=C sort` places it at 1-based line 66 of 91 (89 rows). The diff against the base is a single added line.

Pre-landing observed values (for the L1 to compare after landing; C2's frozen predicates are named in `.ufo/waves/round-73/claims.json`):
- `FRONTIER-CENSUS`: base `rows=50`. With the F51 row appended in scratch the `^| F[0-9]+ |` count is 51 (exit 0). The lane's own `frontier-recheck-count.py` run is not done here (it executes every entry's recheck line, which needs the manifest in the lane first).
- `entries`, `capture records`: base `records=86 bound=86` observed in this seat (§ 2); the base `entries=53` is the claims file's `before_values` (`.ufo/waves/round-73/claims.json`, C2), not re-run here. After landing the predicates are `entries=54` and `records=87 bound=87`. Pre-landing the lane prints `records=86 bound=86 unbound=0` and the `FAIL missing-manifest` line (§ 2).
- The sources census: base exit 0 (§ 2); scratch with the draft row exit 0, zero E-lines.

## 6. Registry row (S108) and README/PROVINCE content, checked

The S108 row cells, in order: `S108` | title and URL | `docs` | `A` | scope | anchor (capture path, sha256 `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9`, 150 lines, 6563 bytes, fetched `2026-11-05T07:40:48Z`, 31 quotes in the manifest, line anchors) | teaches (one grounded benefit: one version place, and a `next_page_token` response is partial until the token is absent, S108.txt:40-41, :135, :144) | `mined` | `2026-11-05` | `90d` | `corpus/knowledge/osv-post-v1-query-contract.md`. No `|` inside any cell (the awk NF count gives 13, the census's 11-column shape). Its URL is unique in the registry (census W04 lists only pre-existing duplicates).

The README block follows the round-72 block: the coverage-map row and the F51 frontier row use the same six-cell shape as F50 (`id | topic | status | entry | sources | next`); its `next` cell names the S108 lines the reader reads.

The PROVINCE line states F51's scope limit as the query endpoint only and names the record format as F31's (`PROVINCE.md:178` already puts "the osv.dev service API" out of F31's scope; F51 fills that named gap).

## 7. Findings and discrepancies (the attack surface on the brief)

1. **F25 is not OSV's record owner.** The brief says the record format "stays F25/F31". F25 in this lane is the CVE JSON record format (`corpus/README.md:591`, source S064); it is a different format. The OSV record format is F31 alone (`corpus/README.md:743`, `corpus/SOURCES.md:86` S080 row, `PROVINCE.md:178`). The drafts cite F31 only; F25 appears in the entry's Distinctness list as "not the OSV record owner". The L1 should confirm this reading before landing, because the brief's "F25/F31" is not supported by the lane's own rows.
2. **The fetch method and final URL are only partly verified.** The lane records no command line for the original S108 fetch. I re-ran the same tool (`capture-source.py --kind html`, default UA) into scratch at 07:47:23Z, status 200, 33417 fetched bytes to a 6563-byte snapshot with the identical sha256 (§ 2). That reproduces the bytes but does not prove the original command. `capture-source.py` prints no final URL and records no redirect, so `http.final_url` in the draft manifest is set to the requested URL and is not verified. The entry's Limits section says the capture is the 07:40:48Z fetch; the re-run is recorded here, not in the entry.
3. **The snapshot directory must not land alone.** It is untracked and has no manifest (§ 5 item 2). Landing `S108.txt` before `manifest.json` reproduces the `missing-manifest` failure (R105/M70-2).
4. **The lane-root recheck cannot pass until the manifest lands.** From a foreign cwd the line exits 2 with `reason=missing` (§ 2). The line itself is correct: it starts with the absolute `cd`, parses, and the scratch copy passes. The C1 census population is the 88 base entries and excludes the C2 entry (claims.json, C1 `tree_scope`), so the C1 numbers do not move with this entry; the entry's own foreign-cwd exit is a C2 kill-rule item, and it is unrun here until the manifest is in the lane.
5. **Header shape.** The round-72 entry carries a fourth header line, `ground:`. The brief specified three header lines (source, verified-at, recheck) and QUALITY Q1 requires only those three, so the draft has three. If the L1 wants the `ground:` line, it is a one-line addition after `verified-at:` and does not move any cited line.
6. **Fuzzy versus exact.** The page says the version is a fuzzy match (S108.txt:35) and names exact matching only for package names (S108.txt:54). The entry records that split and rejects both "the version matches exactly" and "every name matches case-insensitively" as over-generalizations (§ 4).
7. **Draft-directory neighbour.** `.ufo/waves/round-73/w1/draft/round-73.md` exists and is being written by a process other than this seat (its size changed between my two listings). I did not read it for content beyond its listing and did not touch it.

## 8. What was attacked and what was produced

- Attacked: the brief's claim that S108 states the Git-tag query, pagination and size limit as cited; each claim was checked against S108.txt by line, not by the brief's wording (§ 3). The brief's "record format stays F25/F31" (finding 1). The brief's fetch and manifest fields (finding 2). The S080/F31 scope wording (`PROVINCE.md:178`) and the "not the osv.dev service API" sentence in the S080 row (`corpus/SOURCES.md:86`), which together show the named gap is F51's to fill.
- Produced: the F51 entry, the manifest, the S108 registry row, the README block, the PROVINCE line, the knowledge-expected index, and the verification transcript with its scripts.

## 9. Not run

- The lane-root recheck from a foreign cwd after landing (needs the manifest in the lane).
- `frontier-recheck-count.py`, the in-lane `capture-binding-check` after landing, and the in-lane census after landing (each needs the landed files; the scratch equivalents are in § 2).
- `recheck-cwd-census.py` (C1's counter; not my item).
- No live query of osv.dev by any step here. The only network access was the single capture re-run of the documentation page into scratch (§ 2).
