# K73AttackC2 — attack on C2 (F51 admission of the OSV.dev POST /v1/query contract on S108)

Seat: K73AttackC2 (reviewer, leaf, no subagent dispatch). Item attacked: C2 frontier admission F51, the
draft entry `.ufo/waves/round-73/w1/draft/F51-entry.md` (80 lines) with its draft manifest
`draft/manifest.json` and draft registry row `draft/SOURCES-S108-row.md`. Read-only for the lane: no lane file
was written. Scratch: `/fast/scratch/hyaku/kasegi-r73/K73AttackC2/` (check.py, run1.txt, run2.txt, mirror/).
Host: installs none. Tools used: `read`, `bash` (grep, sha256sum, wc, python3, git read-only), `write` (this file only).

Verdict line: **C2 attack: WEAKENED on the Limits clause** (the "only limit sentences" statement is false, and the
`2026-11-05T07:40:48Z` fetch instant the Limits section relies on is not in the capture bytes). The contract claims
(Claims 1–6) HOLD. Landing gate is currently NOT met (see §6).

## 0. Setup checks (exit codes shown)

| check | command | observed |
|---|---|---|
| capture sha256 | `sha256sum corpus/source-snapshots/round-73/S108.txt` | `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9`, exit 0 — matches pin |
| capture lines | `wc -l` | 150, exit 0 — matches |
| capture bytes | `wc -c` | 6563, exit 0 — matches draft manifest `bytes` |
| draft present | `test -f .../draft/F51-entry.md` | exit 0 (absent at first check, present at re-check; attacked as present) |
| freeze commit | `git -C <lane> rev-parse HEAD` | `3b53ff839d0747530f95d432aec1ea7b4308fe96`, exit 0 (= freeze) |
| capture in freeze commit | `git -C <lane> cat-file -e 3b53ff83:corpus/source-snapshots/round-73/S108.txt` | exit 128 — NOT committed at freeze; `git status` shows `?? corpus/source-snapshots/round-73/` (untracked) |
| claims.json read | read in full | C2 `non_claims`: overview page, rate-limit and response-size statements of `api/` NOT claimed; no live osv.dev query by any lane check |

## 1. Province decision (PROVINCE.md)

Decision: **INSIDE the province by precedent — frontier documentation, not refused, not sibling-owned.**

Quotes (exact, from `PROVINCE.md`):
- Domain: "bounty & security research — scopes ~/Projects/bounties, program rules, claim packages" (line 3 region).
- Refuses: "anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it."
- Adjacent: lists chousa, kagi, kake, kengaku. None owns a vulnerability database. No adjacent sibling claims OSV.
- Refusal scope: "Live-target testing is refused; this corpus is documentation only." The draft instructs no call
  (its own line 9: "This entry instructs no call against osv.dev or any other host"), so a documentation entry is not
  the refused act.
- F31 scope limit (PROVINCE.md:178): "the format's range/event semantics only — the osv.dev service API, the JSON
  Schema validation artifact, individual database exports and per-database database_specific values stay out".
  Reading: "stay out" scopes **F31's row**, not the province. The phrase names the service API as a *gap left to a
  later row*, which F51 fills. It does not refuse it. Claims.json `non_claims` says the same ("F31 scope limit stays
  as written; F51 admits the service contract").
- Precedent that a vulnerability-database **service/retrieval contract** is admissible documentation, each with a
  scope limit of the same shape:
  - F30 (PROVINCE.md:176): "scope limit: the service interface only — the record's data model stays F25".
  - F33 (PROVINCE.md:192): "the retrieval interface's response contract as served for one record only … rate limits/
    authentication/the wider parameter surface are unasserted". This is the closest precedent (a paged retrieval API).
  - F36 (corpus/README.md:869 row, Round-55 admission): "scope limit: the REST interface contract only".
  - F47 (corpus/README.md:1087): global security advisories REST API admitted.
- Conclusion: F51 is the same admission shape as F30/F33/F36/F47 for a different database. Its scope limit must be
  "the request/response contract of POST /v1/query only" (the draft states exactly this, line 80). That is consistent.

## 2. Quotes (clause 3)

The draft contains 31 pinned quotes in its manifest and roughly 25 more in prose. Two independent passes:

**2a. Instrument pass (the lane's own bound checker, run from a scratch cwd).**
- Command: `cd /fast/scratch/hyaku/kasegi-r73/K73AttackC2 && TMPDIR=<scratch> python3 corpus/instruments/source-recheck.py --manifest <scratch>/mirror/manifest.json --source S108`
  (mirror = `S108.txt` copied byte-identical from the capture, sha verified `304baa7d…`; manifest = draft manifest).
- Output: `S108:sha256 OK`, then 31 lines `S108:Q01…Q31 OK occurrences=1 anchor=<line>-ok`. Count OK=31, FAIL=0. Exit **0**.
- Manifest quote count: 31 (`grep -o '"id": "Q' | wc -l`).

**2b. Prose quotes in the draft (grep -nF, both directions).**

| draft quote (abridged) | draft occ | capture occ | words | anchor |
|---|---|---|---|---|
| "Lists vulnerabilities for given package and version. May also be queried by commit hash." | 1 | 1 | 14 | :24 |
| "commit string The commit hash to query for. If specified, version should not be set." | 1 | 1 | 14 | :34 |
| "When a commit hash is given, this is optional." | 1 | 1 | 9 | :36 |
| "Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both." | — | 1 | 14 | :40 |
| "Requests that specify the version in both places return 400 Bad Request." | — | 1 | 12 | :41 |
| "A fuzzy match is done against upstream versions." | — | 1 | 8 | :35 |
| "Package names are matched exactly, except in ecosystems whose registry treats other spellings as the same package:" | — | 1 | 17 | :54 |
| "To do so, set the ecosystem to GIT, enter the full URL of the repository to the name field," | — | 1 | 19 | :56 |
| "pagination will occur when there more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds." | — | 1 | 20 | :136 |
| "When pagination is used, the next_page_token is given in the response, indicating that there are more results to return." | — | 1 | 19 | :135 |
| "The API has a response size limit of 32MiB when using HTTP/1.1." | — | 1 | 12 | :148 |

- Longest quote in the draft: 20 words (pagination trigger). **No quote over 25 words.** No unlocated quote.
- Note on my first automated pass: a naive regex paired closing and opening quote marks across backtick spans and
  printed false "UNLOCATED" rows (for example "`,` (S108.txt:59)…"). Those were regex artifacts, not draft quotes;
  each real quoted sentence above was confirmed directly. Recorded so the artifact is not mistaken for a finding.

## 3. Facts stated by the draft, checked against the capture (clause 4)

| draft fact | capture evidence | verdict |
|---|---|---|
| Payload has four top-level keys; payload keys at :58-67 | lines 58 `{` … 67 `}`; keys commit, version, package, page_token (verified line 59, 66) | HOLDS |
| commit query: version must not be set; package optional | :34, :36 quoted | HOLDS |
| version in one place only; both = 400 | :40, :41, :47 "Invalid (400 Bad Request):", :46/:48 examples | HOLDS |
| version match is fuzzy | :35 "A fuzzy match is done against upstream versions." | HOLDS |
| names exact; three exceptions PyPI/NuGet/crates.io on :54 | :54 quoted; exactly three named | HOLDS |
| Parameter names and values case-sensitive | :53 "Case Sensitivity: API requests are case-sensitive. Please ensure that you use the correct case for parameter names and values." | HOLDS |
| Git tag: GIT ecosystem, repo URL in name, tag in version; example at :79 | :56 quoted; :79 example `{"package": {"name": "https://github.com/curl/curl.git", "ecosystem": "GIT"}, "version": "8.5.0"}` | HOLDS |
| pagination trigger: >1,000 vulns or >20 s | :136 quoted | HOLDS |
| token loop; token may be sole content | :135, :144, :149 quoted | HOLDS |
| size limit 32 MiB under HTTP/1.1; no limit under HTTP/2; recommends HTTP/2 | :148 quoted (all three sentences on one line) | HOLDS |
| sample response at :82-133 | `{` at :82, `}` at :133 | HOLDS |
| sample record only as response body; fields not asserted | Draft "Distinctness" section and Limits section (S108.txt:82-133 is the sample body); capture :103-125 has ranges/events/ecosystem_specific/database_specific, none asserted by the draft | HOLDS |
| **"rate limits or quotas … The capture has no sentence on either: `grep -n -i 'rate limit\|ratelimit\|quota\|api key\|api_key\|authenticat\|credential' S108.txt` prints nothing."** | re-run: `grep -n -i 'rate limit\|ratelimit\|quota\|api key\|api_key\|authenticat\|credential' <capture>` → no output, **exit 1** (no match). An earlier, broader `grep -i 'rate\|throttl\|429\|overview\|quota'` matched only substrings "integrated"/"crates" (lines 50, 54), not rate limits. | HOLDS |
| overview page (`api/`) statements not in capture | capture is the query page; grep for `overview` = 0 | HOLDS (correctly disclaimed) |
| **"The only limit sentences are the pagination trigger (S108.txt:136) and the HTTP/1.1 size limit (S108.txt:148)."** | `grep -n -i limit <capture>` → lines **148** and **149**. Line 149: "…but were not found within the **time limit**, please keep querying…". | **WEAKENED: contradicted as an exhaustive claim** — see finding F-1 |
| "the pinned capture is the 2026-11-05T07:40:48Z fetch" | `grep -c '07:40' <capture>` → **0** (exit 0 with count 0). The instant appears only in claims.json, draft/manifest.json (`fetched_utc`) and draft/SOURCES-S108-row.md. The draft's own manifest `fetch_method` says: "the original fetch command line is not recorded in the lane". | **NOT ON THE PAGE / NOT BOUND** — see finding F-2 |
| manifest `fetch_method`: "a re-run … on 2026-11-05T07:47:23Z reproduced the sha256 and the 6563 snapshot bytes" | sha and bytes reproduced today (sha `304baa7d…` and 6563 bytes, both exit 0), but no lane receipt of the 07:47:23Z re-run exists | Content matches; the re-run itself is unreceipted (R21) |
| "This entry instructs no call against osv.dev or any other host" | §6 greps: no `api.osv.dev`, no executable request in the draft | HOLDS |

## 4. Findings (clause 4 — overclaim)

**F-1 (Limits clause, WEAKENED).** The draft's Limits section states as an exhaustive fact that "The only limit
sentences are the pagination trigger (S108.txt:136) and the HTTP/1.1 size limit (S108.txt:148)." The capture has
a third limit sentence at **S108.txt:149**: "…but were not found within the time limit, please keep querying…".
Evidence: `grep -n -i limit <capture>` → `148:` and `149:`; `sed -n 149p` shows "within the time limit". Effect: the
statement is a universal negative the page contradicts. The rate-limit disclaimer that follows is still accurate.
Repair (for the scribe, not applied here): reword to name the three limit-bearing lines (:136, :148, :149), or drop "only".

**F-2 (fetch provenance, WEAKENED — R21).** The Limits section ties the pinned capture to "the 2026-11-05T07:40:48Z
fetch", and the registry row (draft/SOURCES-S108-row.md) states "fetched 2026-11-05T07:40:48Z". The capture bytes carry
no timestamp (`grep -c '07:40'` = 0), and the draft manifest admits the original fetch command is not recorded.
Under R21 a fetch instant is evidence only when the capture commit dates it; here the capture is untracked
(`?? corpus/source-snapshots/round-73/`) and the manifest that holds the instant is not landed. The instant therefore
rests on the frozen claim text and an unlanded draft. The sha and byte count do reproduce. Repair: land the manifest and
the capture in one commit (R20) so the commit date is the binding evidence, and state the fetch instant as the manifest's
claim.

**F-3 (disclosure, minor — not a falsifier).** The draft's Distinctness section names F31, F25, F47 and F36 but
not F30 (CVE Services publication API, `PROVINCE.md:176`) or F33 (NVD API 2.0, `PROVINCE.md:192`). F33 is the closest
analogue: both are paged retrieval contracts and F33 owns a "2.0 paging envelope". Overlap check in §5 finds no
re-admitted ground, so this is an omission from the disclosure, not a second admission. Repair: add one line each.

## 5. Overlap with existing rows (clause 5)

| row | owns | F51 touches | re-admits ground? |
|---|---|---|---|
| F31 (S080, `osv-affected-range-events.md`) | the record's `affected[].ranges[].events` timeline; scope limit: service API out | S108 shows a sample record (:82-133) with `ranges`/`events` (:103-112) and `ecosystem_specific`/`database_specific` (:122/:125). Draft asserts NO record field and states "The OSV record format stays with F31" | **No.** The F31 scope limit is preserved; F51 admits the envelope and the request only |
| F25 (S064, CVE JSON record) | CVE record data model | none (different record format) | No |
| F30 (S078, CVE Services write path) | CVE Services publication write path | none (F51 is a read query) | No (see F-3 for disclosure) |
| F33 (S083, NVD API 2.0 retrieval) | NVD response contract and 2.0 paging envelope for one record | OSV pagination is token-based (`page_token`/`next_page_token`) and NVD's is index-based; no NVD ground re-admitted | No (see F-3 for disclosure) |
| F36 (S087), F47 (S103) | GitHub REST advisory interfaces | named in draft | No |
| S080 registry row, `corpus/SOURCES.md:86` | "not the osv.dev service API" (grep -o confirmed, exit 0) | the row is the anchor for F31's gap | Consistent: F51 admits what the row excludes |
| existing knowledge mentions of osv (`openssf-scorecard-checks.md`, `github-advisory-database-curation-semantics.md`) | Scorecard's "OSV-service-backed" detection wording; advisory-DB curation | none of the OSV POST contract | No |

Shared surface, named: both F31 and F51 cite the same osv.dev sample record shape, and both F33/F51 are paged. Neither
re-admits the other's ground. No finding is raised on overlap.

## 6. Q6 (no probing, live queries or credentialed access) — clause 6

Greps on the draft (`grep -n`, exit codes shown):

| pattern | count | lines (abridged) | assessment |
|---|---|---|---|
| `curl` | 1 (exit 0) | :39 the Git example's repo URL `https://github.com/curl/curl.git` inside a quoted sentence | Not a command. The draft quotes a page example. HOLDS |
| `api.osv.dev` | 0 (exit 1) | — | HOLDS |
| `POST` | 6 (exit 0) | :1, :3, :9, Limits, Scope line (`POST /v1/query` as endpoint name) | Endpoint naming only. No request is instructed. HOLDS |
| `token` | 5 (exit 0) | :13 `"page_token": "string"`; :45–:51 `page_token`/`next_page_token` | Pagination tokens, not credentials. HOLDS |
| credential / api key / authenticat | 0 in the draft's operative text (appear only in the Limits disclaimer line) | — | HOLDS |

Q6 HOLDS: no probing, live query, or credential instruction. Draft line 9 disclaims any call.

## 7. Landing gate (state at report time — read-only, not a content attack)

- Lane recheck as written in the draft's `recheck:` line, run from a foreign cwd:
  `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-73/manifest.json --source S108` →
  `manifest UNAVAILABLE reason=missing`, **exit 2**. Fail-closed as designed, but C2's kill rule requires exit 0 after landing.
- Draft manifest against a scratch copy of the capture (same sha): exit **0**, OK=31, FAIL=0 (§2a).
- Capture-binding: `python3 corpus/instruments/capture-binding-check.py` → `FAIL rule=missing-manifest dir=round-73`,
  `records=86 bound=86 unbound=0`, **exit 1**. (An earlier `0` I recorded was the exit of a pipe, not the instrument; corrected here.)
- C2 after-state predicate needs `capture records=87 bound=87` and exit 0; that requires the manifest, the capture and the
  entry to land in one commit (R20). Currently unmet by the lane, which is the integrator's step, not a defect in the draft's content.

## 8. Clause summary

| clause | verdict | evidence |
|---|---|---|
| (1) capture | HOLDS | sha `304baa7d…`, 150 lines, 6563 bytes, exit 0 |
| (2) province | HOLDS (inside, by precedent F30/F33/F36/F47; F31 "stay out" is a row scope limit, not a province refusal) | PROVINCE.md:176, :178, :192 quoted |
| (3) quotes | HOLDS | 31/31 instrument OK, exit 0; prose quotes occ=1 each, max 20 words |
| (4) overclaim | **WEAKENED** | F-1: "only limit sentences" false (S108.txt:149 "time limit"); F-2: 07:40:48Z not in capture bytes (`grep -c` = 0) |
| (5) overlap | HOLDS; disclosure minor WEAKENED | F31 scope kept; F30/F33 not named (F-3) |
| (6) Q6 | HOLDS | §6 greps |

**C2 attack: WEAKENED on the Limits clause** (F-1 the exhaustive "only limit sentences" statement; F-2 the fetch instant
that the capture bytes cannot bind). Contract claims (payload, version rule, names, Git tag, pagination, size) HOLD.

## 9. Checks for the main agent to run after landing (not run by this seat)

1. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-73/manifest.json --source S108; echo $?` → expect 0.
2. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-binding-check.py; echo $?` → expect 0, `records=87 bound=87 unbound=0`.
3. `grep -n -i limit corpus/source-snapshots/round-73/S108.txt` → confirm the entry's Limits wording names :149 or drops "only".
4. `grep -c '' corpus/knowledge/<F51 entry>` and `grep -n '^source:\|^verified-at:\|^recheck:'` to confirm Q1 headers.

## 10. Scope and honesty notes

- No lane file was written. No git mutation was run. No live osv.dev or any other host was queried; the only network-free
  checks were the pinned capture and the lane's own instrument on a scratch copy.
- Scratch dir `/fast/scratch/hyaku/kasegi-r73/K73AttackC2/` holds check.py, run1.txt (lane-manifest recheck, exit 2),
  run2.txt (draft-manifest recheck, exit 0) and mirror/. Removed at seat exit after this report.
- Tools installed: none.
