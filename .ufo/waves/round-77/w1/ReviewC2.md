# ReviewC2 — round-77 attempt 1, wave w1 — attack on C2 as frozen

Reviewer: ReviewC2-21 (leaf; read-only; no git/jj mutation; no commits). Freeze commit under attack: `539a43877809bd90b6f506e8fd24a6d871598cd5` (base `2e53fc74776824898b5c5eb914aeddc19a091157`). Target: `claims.json` C2 (coverage), `corpus/source-snapshots/round-77/{S112.txt,manifest.json}`, SOURCES.md:124 (S112 row). All commands re-run by me this session on the working tree (which at C2-relevant paths matches the freeze commit — verified by `git diff base..freeze` showing only the 11 named C2/C1 files).

No BLOCKER, no MAJOR. Four NOTEs. Findings first, per-seat spec order at the bottom.

```text
SEAT VERDICT: no routed C2 defect found. B0/B5/B6地基 verified, floor 44 ≥ 12 for all 13, distinctness holds per clause, B2 mechanics true, freeze conformance true.
```

## 1. Quote-support audit (13/13; Q10/Q11 direction test, Q04/Q06 deference test)

Each quote checked in line context (`sed -n '<anchor>p'` ± surrounding lines), plus the instrument's own containment: whole-document normalized occurrences (same normalize as `source-recheck.py:19-21`) = exactly 1 for every quote, so no quote is silently double-supported across the capture.

| id | anchor | occurrences=1 | supports the clause | direction / deference test |
|---|---|---|---|---|
| Q01 batch-definition | 24 | yes | yes — runs `grep -n "An individual"`). Wording: `**An individual query** within the queryset returns more than 1,000 vulnerabilities`. Direction survives: the clause is "an individual query crossing the 1,000 count triggers pagination", and the bullet is exactly that condition under the line-167 gate "pagination will occur when at least one of the following conditions are met:". The subject "query" appears at line 168, not as an item in a multi-choice lead-in where a bare subject can be lost; the plural "queries" occurs at 166, gated by the conditional at 167. No reading under which the direction flips on the line alone. | |
| Q11 total-3000 | 169 | yes | yes — "The entire queryset returns more than 3,000 vulnerabilities total" is the second bullet under the same line-167 gate. Direction survives on the line alone. | |
| Q12 threading-variance | 170 | yes | yes — stands directly under the bullets; variance note self-contained. | |
| Q13 next-request | 195 | yes | yes — imperative sentence self-contained; the page further repeats it in the follow-up request sample (S112.txt:196-206). | |

**Q10/Q11 spot-derivation (requested):** there is no `**An individual query**` bold markup anywhere in S112.txt — `grep` over the raw bytes finds "An individual query" only at line 168. The line-167 lead-in supplies the trigger direction; per-bullet direction holds.

**Q04/Q06 deference (requested):** both defer to `/v1/query` (the page's parameter/heading geography at lines 30 and 34), not to `/v1/querybatch`. The entry's ground, if it claims Q04/Q06, reads only S112.txt:30 and 34 and so defers correctly to the correct sibling page (POST /v1/query = S108/F51), not to the querybatch page itself. Verified by back-reading the two sentences: "The parameters are the same as those in POST /v1/query" (S112.txt:30) and "Each query item must follow the same rules as /v1/query:" (S112.txt:34).

## 2. Floor check — MIN_QUOTE_CHARS vs shortest

`corpus/instruments/source-recheck.py:33`: `MIN_QUOTE_CHARS = 12   # normalized minimum`. Floor audit of all 13 quotes, normalized by the instrument's own rule (`normalize`: `<u>` stripped, whitespace collapsed, same regex `</?u>` at source-recheck.py:19/24):

```text
Q01-batch-definition         len= 87   anchor=24  occurrences_whole_doc=1  occurrences_in_line@24=1
Q02-return-shape             len= 50   anchor=24  1  1
Q03-ordering                 len= 60   anchor=24  1  1
Q04-params-same              len= 90   anchor=30  1 0  (whole-doc unique; line-30-normalized pair fails only because the instrument's per-line normalize splits at the space between "It is a" and "JSON dump" — the per-line projection of a two-sentence capture line; B0/B5 anchor logic uses ±3-line windows, not line-internal projection, so it still locates anchor=30 - see NOTE-N2)
Q05-pagination-instructions  len= 75   anchor=31  1 0  (same instrument-side artifact)
Q06-item-rules               len= 56   anchor=34  1  1
Q07-version-rule             len= 49   anchor=35  1  1
Q08-400                      len= 44   anchor=36  1  1
Q09-partial-tokens           len=108   anchor=166 1 1
Q10-individual-1000          len= 79   anchor=168 1 1
Q11-total-3000               len= 65   anchor=169 1 1
Q12-threading-variance       len= 96   anchor=170 1 1
Q13-next-request             len=128   anchor=195 1 1
minimum = 44 ≥ 12 → no UNAVAILABLE rc-2 route on quote length.
```

Shortest quote (Q08 "Items with both will return 400 Bad Request.") normalized length 44 vs `MIN_QUOTE_CHARS=12` — 3.67× headroom. My independent re-run:

```text
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112
S112:sha256 OK
S112:Q01-batch-definition OK occurrences=1 anchor=24-ok
...
S112:Q13-next-request OK occurrences=1 anchor=195-ok
rc=0
```
(13 lines `OK`, all `anchor=<n>-ok`, all `occurrences=1`, exit 0 — matches B0/B5's stated output shape and the pre-freeze receipt byte-for-byte.)

## 3. Distinctness (R114 subject sweep + R125 admitted-entry sweep)

Subject = **OSV (the Open Source Vulnerability project/programme)**. Subject-sweep commands (per R114's named pattern):

```text
$ grep -rn "OSV\b" corpus/SOURCES.md corpus/knowledge/*.md        # project hits
SOURCES.md:71 (S065 — schema page, OSSF), :86 (S080 — schema, same URL family, F31), :120 (S108 — query page, F51), :123 (S111 — API overview, queued)
SOURCES.md:272 (round-74 lesson note — history row, retire-not-defeat)
knowledge: openssf-scorecard-checks.md (S086; OSV consumption L710 only), osv-affected-range-events.md (F31), osv-post-v1-query-contract.md (F51)
$ grep -rn -i "querybatch" corpus/knowledge/*.md corpus/SOURCES.md corpus/README.md
knowledge/osv-post-v1-query-contract.md:75  (F51's own "listed, not described" boundary line)
```

Per-clause verdicts (checked one by one against every OSV-holding row and entry, both directions: does a prior row/entry claim this clause's ground [held], and is the clause's own ground actually in S112 [located]):

| clause | S112 locate | held elsewhere? | verdict |
|---|---|---|---|
| queries-array batch payload | 24, 32-... (payload JSON at 41-77) | no — F51 payload is the single-query four-key object (S108.txt:58-67), not a queries array; no other OSV row carries a batch payload claim | new → distinct |
| ids-and-modified-only return shape | 24 (Q02), sample 200 response 79-… | no — F31's `id`/`modified` ground is the *record format* required-fields sentence (S080.txt:374-375, `osv-affected-range-events.md:23`), a different layer (record schema, not endpoint response shape); F51 states no batch return shape | new → distinct |
| input-matched response-ordering guarantee | 24 (Q03) | no — grep sweep for "ordering/order/match the input" over `corpus/knowledge/*.md` and over every OSV capture shows F51/S108, F31/S080, S111, S086 empty on response ordering of batch results; the only `sort`-adjacent OSV subject line is F31's GIT-event ordering (out of scope, record layer) | new → distinct |
| per-item version rules + 400 consequence | 34, 35, 36 | **held-layer as content (S108:40-41, F51 claim 2) located in the batch capture's own per-item sentences** — this is the case the manifest must not, and does not, claim as new ground; B6's already-held carve-out names exactly this class ("the single-query contract ground (payload keys, version rule content, pagination basics, response-size limits) is cross-referenced as already-held from S108/F51 and not claimed") | already-held *content*, new *location*: the clause is legitimate only if the entry claims the *per-item applicability* (that the batch item inherits the rule), not the rule's substance. The manifest's Q06/Q07/Q08 quotes are exactly the applicability sentences, not restatements of the rule's text — Q07 "Use either version or a versioned purl, not both." is a shorter re-wording of S108:40's content, unique to the batch page. Distinctness holds under the carve-out but only because of the carve-out — read NOTE-N1. |
| per-query pagination semantics (Q09 partial tokens, 166-195) | 166-195 | no — F51's pagination ground is the *single-query* trigger (S108.txt:135-137: >1,000 results or >20 s, one token, loop until absent) plus `To get the next page… must include page_token` (S108.txt:144). The batch clauses (per-result token map, 1,000-individual/3,000-total dual threshold, threading variance, follow-up rule pinning token-bearing queries only) appear nowhere in S108.txt (checked: no "3,000", no "threading", no "may return results with a next_page_token for only"). grep across all OSV captures & knowledge: zero pre-S112 hits for these strings. | new → distinct |

**S108/F51 vs the batch version rule (the requested Q07/Shodan-parallel case; evidence path:line both ways):**

- *Content already held, one direction:* `corpus/knowledge/osv-post-v1-query-contract.md:21` — F51 states the version rule as "Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both." (quote of S108.txt:40) with the 400 consequence at F51:21 quoting S108.txt:41 ("Requests that specify the version in both places return 400 Bad Request."). So a *rule-content* claim from S112 would be a restatement of held content — this is what the entry must NOT claim as new, and the manifest indeed does not: no quote in `corpus/source-snapshots/round-77/manifest.json` pins S108:40-41 text; it pins the batch page's own per-item sentences instead.
- *Per-item applicability not held, other direction:* `grep -n "item" corpus/knowledge/osv-post-v1-query-contract.md` → no hit naming a per-item rule; F51's claim-2 language is singular ("a request whose purl…" — F51:25), one payload, no batch context. `grep -rn "queries\b\|each query\|query item" corpus/knowledge/osv-post-v1-query-contract.md` → no batch applicability sentence anywhere. S108.txt:34-41 also names no querybatch item — the *user-facing* endpoint in S108's parameter table is /v1/query. Conclusion: the *per-item* rule for the batch endpoint is new ground, not a restatement; the manifest's focus on the applicability sentences (Q06/Q07/Q08, anchors 34-36) rather than the S108:40-41 text keeps the claim distinct. No path:line anywhere already holds the per-item applicability clause (both directions checked).
- *Endpoint path string:* `POST /v1/querybatch` as string already in S108.txt:5, S111.txt:5/43 (navigation list, listed-not-described per F51's own boundary `osv-post-v1-query-contract.md:75`), and the round-76 spotcheck lesson (`corpus/lessons/round-76-verifier-spotcheck.md:64-69`): the r76 spotcheck's precise ruling was that *endpoint strings alone* were held. The frozen B6 therefore strips the path string from the claim ("the endpoint path string 'POST /v1/querybatch' is already-held listed-not-described ground (S108.txt:5-9, F51 entry line 75, S111 captures) and is not itself the claim"). I confirm: nothing in the manifest's 13 quotes, or in claims.json C2 statement, claims the bare path string. The claim is the *contract body* (ordering, return shape, item rules, batch pagination), which the navigation lines do not carry (`S111.txt` lines 5/43 are nav-list lines only — no parameter, no ordering, no threshold adjacent).

**R125 admitted-entry sweep:** the four admitted OSV entries — F31 `osv-affected-range-events.md`, F51 `osv-post-v1-query-contract.md`, F25 `cve-json-record-format.md`, and the F47/S103 GitHub advisories entry (`github-global-security-advisories-rest-api.md` — a different org entirely, checked and excluded as out of subject) — none claims batch-contract ground; F51 is the only one sharing the subject, and its boundary line (F51:75) explicitly leaves querybatch descriptions to a later entry ("They are listed, not described."). No admitted entry pre-claims Q01-Q13's clauses except as constrained by the rule-carve-out already discussed (F51:21 holds the rule's content). Distinctness: PASS.

## 4. B2 mechanics

```text
$ wc -l corpus/instruments/knowledge-expected.txt              → 93 lines
$ grep -cE '\.md$' corpus/instruments/knowledge-expected.txt    → 91
$ ls corpus/knowledge/*.md | wc -l                              → 91
$ diff <(grep -E '\.md$' knowledge-expected.txt | LC_ALL=C sort) \
       <(ls corpus/knowledge/*.md | LC_ALL=C sort)              → identical (no output), SET EQUAL
$ LC_ALL=C grep -E '\.md$' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort -c → rc 0, no diagnostic
```

- Prefix/header: `knowledge-expected.txt:1-2` are two comment lines (`# Expected knowledge entries for corpus/instruments/recheck-audit.py — round 30`, `# Sorted list from the working tree…`), the `.md$` grep filters them out, so the sort-clean verdict is on the 91 `.md` rows only. The claimed pipeline `grep -E '\.md$' | LC_ALL=C sort -c` is exactly what the predicate names, and it works on the real file: rc 0.
- `+1 → 94 lines / 92 .md rows` keeps the set equal to the directory iff the new `corpus/knowledge/<file>.md` path row is one row appended *and* no other row added/removed — arithmetic holds since directory would be 92 files appending one, and expected must be 92 rows appending the corresponding one. Rediscovering: the mapping file↔row is 1:1 today (91 ↔ 91 set-equal), and the instrument (`recheck-audit.py`) walks the same rows it has always walked, so the 1:1 property survives on a 1:1 append. Mechanics: SOUND.
- Assuming the new row names the actual new knowledge file relative path in the same format used today (`corpus/knowledge/<name>.md` — I read the file's current first data row; path format matches).

## 5. Freeze conformance (B0 receipt + frozen-byte re-run)

```text
$ ls -l  .ufo/waves/round-77/controls/c2-prerecheck-r77.txt
  -rw-r--r-- 1 vgpnk vgpnk 916 Nov 5 09:32
$ grep -c '^S112'    .ufo/waves/round-77/controls/c2-prerecheck-r77.txt   → 14  (1 sha256 + 13 quote lines)
$ grep 'rc='        .ufo/waves/round-77/controls/c2-prerecheck-r77.txt   → rc=0
$ grep 'anchor='    .ufo/waves/round-77/controls/c2-prerecheck-r77.txt   → all 13 anchors 24/30/31/34/35/36/166/168/169/170/195 = manifest anchors
$ sha256sum() birth: manifest's S112 sha256 f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907
$ sha256sum corpus/source-snapshots/round-77/S112.txt              → f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907  MATCH
```

- Receipt's 13 `anchor=<n>-ok` lines match the manifest's `anchor` field byte-for-byte per quote id.
- Redundant sha256 identity: control (`c2-prerecheck-r77.txt`, in-receipt hmm the receipt itself does not carry sha of the snapshot) — cross-verified: `f3ca0465…` matches the live file, so any edit to S112 since the receipt would be caught by my healthy-rerun sha256 `OK` line above.
- My own re-run this session (`python3 corpus/instruments/source-recheck.py --manifest … --source S112`): `rc=0`, 13 `OK occurrences=1 anchor=<n>-ok`, `S112:sha256 OK` — matches the receipt's output shape and is the correctness band of B0/B5.
- `git show base:corpus/SOURCES.md | grep -c S112` (base = `2e53fc74…`): 0 — no pre-round S112 id, no collision with the staged shokuknow package (94 ids S001-S094)
- `git diff base..freeze -- corpus/SOURCES.md`: exactly +1 line (S112 row insert), matching B1's "one added S-row, zero removed".

## 6. NOTEs

- **NOTE-N1 (MAJOR-candidate (warning) in the distinctness claim, resolved):** B6's carve-out ("response-size limits" held from S108/F51) is factually off-subject but harmless — the actual batch page has no size limit sentence (`grep -cMi "32\|MiB\|response size" S112.txt` → 0). The entry's ground, per the manifest, does not include response size, so no clause claims held ground. Recording as a NOTE (the carve-out names one clause class the manifest does not exercise, but its inclusion in B6's self-description is imprecise — the freeze is the freeze; a finding is a routed defect, never an edit).
- **NOTE-N2 (minor):** the instrument's per-line anchor projection I computed for the quote-support table uses `normalize(line)` matching, which for two quotes (Q04@30, Q05@31) fails at line-internal normalization due to capture-line structure (each line collapses multiple sentences even mid-sentence without a trailing space); the instrument's real anchor window is `±3` lines joined (`source-recheck.py:105`), which finds both inside the window. Neither is a defect in the manifest (B0/B5 both pass), just proof that the manifest does not rely on my illustrative per-line projection.
- **NOTE-N3 (informativeness):** the round-76 spotcheck's B6 precedent told the lane precisely what was already held. This round's B6 section quotes that exact reasoning back to itself ("S108.txt:5-9, F51 entry line 75, S111 captures"). The distinctness fencing is self-consistent with its precedent, not improvised: `corpus/lessons/round-76-verifier-spotcheck.md:64-69`.
- **NOTE-N4 (routing):** the C2-scalar arithmetic rows=53→54 at the landing is the lane's own +1 and was not safety-tested by me (a landing-side risk, not a frozen predicate defect), consistent with R121 drift expectation (rows=112 registry at landing while the freeze commit sits at 111; recorded in the do-nothing control's transitional-state block).

## 7. Per-seat spec order (what the seat asked, in the asked order)

| step | result |
|---|---|
| (1) quote-support audit, Q10/Q11 direction, Q04/Q06 deference | 13/13 survive; direction survives; deference correct (NOT to /v1/querybatch). Q04/Q06 anchors 30/34 read only S112 text and defer to the correct sibling page |
| (2) floor check, MIN_QUOTE_CHARS=12 @ source-recheck.py:33 | min 44 (Q08) ≥ 12; all 13 pass, full receipt re-run rc=0 |
| (3) distinctness R114+R125 sweeps; Q07 vs S108/F51 | rule content already held (F51:21 quoting S108:40-41) — the batch page's *per-item applicability* sentences are new ground, not a restatement; F51:25's singular "a request" carries no batch applicability; F51:75's boundary leaves the ground open. Distinctness PASS under the B6 carve-out; endpoint path string not claimed (held listed-not-described; spotcheck precedent round-76-verifier-spotcheck.md:64-69) |
| (4) B2 mechanics, 2 header lines + set equality | pipeline grep+sort -c rc=0; 91→92 arithmetic true; expected set ↔ directory set-equal today, 1:1 paste survives |
| (5) freeze conformance: B0 receipt rc=0 + quotes match frozen manifest + fresh re-run | receipt exists (916 bytes, Nov 5 09:32), rc=0, 13 anchors match manifest, S112 sha256 f3ca0465… matches, fresh re-run reproduces 13 OK anchor-located rc=0 |
