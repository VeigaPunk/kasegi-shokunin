# ScoutDistinct — R125 admitted-entry sweep + R114 subject sweep over the seven C2 clauses (round-78 attempt 1)

Seat: ScoutDistinct (scout; leaf; read-only). Scope: the seven quoted clauses of the frozen C2 claim
(`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-78/claims.json`, C2), as pinned in
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-78/manifest.json`.
Freeze commit `2d81fe84506b323fb32beb137d5bd21db6a5c13d`, base `0687cca8645884aba30c8eb5fa2d8ecaca7245cf`.
No lane file was edited; nothing was committed.

Corpus state at the freeze commit: 91 admitted entries in `corpus/knowledge/*.md`
(`git ls-tree -r --name-only 0687cca… -- corpus/knowledge/ | grep -c '\.md$'` → `91`),
Frontier rows F01–F53 (F53 at `corpus/README.md:1187`), registry `S112` row present at `corpus/SOURCES.md:124`
with `status=queued`, `used-by=—`.

Snapshot bytes verified: `corpus/source-snapshots/round-78/S112.txt` sha256
`f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907`, byte-identical to
`corpus/source-snapshots/round-77/S112.txt` (216 lines, 4575 bytes). Quotes re-located by the lane's own
instrument (`TMPDIR=/fast/scratch/hyaku/kasegi-r78/ScoutDistinct python3 corpus/instruments/source-recheck.py
--manifest corpus/source-snapshots/round-78/manifest.json --source S112`):

```text
S112:sha256 OK
S112:Q01-batch-definition OK occurrences=1 anchor=24-ok
S112:Q02-return-shape OK occurrences=1 anchor=24-ok
S112:Q03-ordering OK occurrences=1 anchor=24-ok
S112:Q09-partial-tokens OK occurrences=1 anchor=166-ok
S112:Q10-individual-1000 OK occurrences=1 anchor=168-ok
S112:Q11-total-3000 OK occurrences=1 anchor=169-ok
S112:Q13-next-request OK occurrences=1 anchor=195-ok
rc=0
```

Literal absence (B6's mechanical half), `grep -F -l` of each of the seven quotes over `corpus/knowledge/*.md`:
**0 files for each of the seven**. Paraphrase half (this seat) below.

## 1. Per-clause table

| Clause (quote / line on S112) | Verdict | Held location (or none) | One-sentence reason |
|---|---|---|---|
| **Q01** "Query for multiple packages (by either package and version or git commit hash) at once." (`:24`) | **NOVEL** | none in an admitted entry | The batch endpoint's own purpose — many packages in one request — is held nowhere admitted: F51 is scoped to `POST /v1/query` only and lists `POST /v1/querybatch` as *listed-not-described* ground (`corpus/knowledge/osv-post-v1-query-contract.md:75`, scope limit `:80`), and no admitted entry mentions a batched OSV lookup. |
| **Q02** "Returns vulnerability ids and modified field only." (`:24`) | **PARTLY-HELD** | field pair + its meaning: `corpus/knowledge/osv-affected-range-events.md:23` (F31, S080.txt:374-375 — "The id and modified fields are required"); F51 disclaims the record format at `corpus/knowledge/osv-post-v1-query-contract.md:74` | What is held is *which fields an OSV record carries* (F31's required-envelope rule); what is new is the **endpoint's response projection** — the batch endpoint returns only those two fields and not whole records — which F31 does not claim (F31's scope limit at `PROVINCE.md:178` excludes "the osv.dev service API"). |
| **Q03** "The response ordering will be guaranteed to match the input." (`:24`) | **NOVEL** | none | No admitted entry states an OSV *response*-ordering rule: the only ordering sentences in `corpus/knowledge/` are `corpus/knowledge/github-global-security-advisories-rest-api.md:78` (GitHub's advisories API — different organisation, and an absence of guarantee) and F31's range-type ordering (`corpus/knowledge/osv-affected-range-events.md:68,:74`) which is about record-internal range evaluation, not response order. |
| **Q09** "However, a querybatch request may return results with a next_page_token for only a few of the total queries." (`:166`) | **PARTLY-HELD** | the token mechanic: `corpus/knowledge/osv-post-v1-query-contract.md:47` (F51 Claim 5: token means more results, S108.txt:135; next request must include `page_token`, S108.txt:144) and its falsifiable rule at `:49` | F51 holds the single-query token loop; the new content is the **set-level partiality** — tokens are distributed per query and only some queries in one request carry one, so extra requests are scoped to those queries — which a single-query page cannot supply. |
| **Q10** "An individual query within the queryset returns more than 1,000 vulnerabilities" (`:168`) | **PARTLY-HELD** | the 1,000 figure and its pagination-trigger role: `corpus/knowledge/osv-post-v1-query-contract.md:47` (F51, S108.txt:136 — "more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds"), restated at `:51` | The threshold *number* is F51's, but its **scope object differs**: F51's trigger counts the single endpoint's whole response (and is paired with a 20-second trigger), whereas S112:168 counts **one query inside a queryset** under the disjunction gate at `:167`; the batch page states no time-based trigger (`grep -n -i 'second' S112.txt` → no match, rc=1). |
| **Q11** "The entire queryset returns more than 3,000 vulnerabilities total" (`:169`) | **NOVEL** | none | A **set-level** threshold is held nowhere: `grep -rn '3,000' corpus/ PROVINCE.md SKILL.md` returns exactly one hit, `SKILL.md:675` (a bounty-dollar band, unrelated), and F51 holds only the per-response 1,000/20-second triggers — the lane holds no total-of-queryset pagination threshold at all. |
| **Q13** "To get the next page of results, your next request should specify page_token only for the queries that returned next_page_token." (`:195`) | **PARTLY-HELD** | the "next request must include page_token" mechanic: `corpus/knowledge/osv-post-v1-query-contract.md:47` (F51, S108.txt:144) | What is new is **selectivity**: the follow-up request carries a token for *only* the token-bearing queries (F51's single-query rule is unconditional, one token); the round-77 manifest's own unpinned line `S112.txt:194` ("each result has a distinct next_page_token … the third result does not include one") is the corroborating but **unpinned** sentence. |

**Summary of the sweep:** 3 NOVEL (Q01, Q03, Q11), 4 PARTLY-HELD (Q02, Q09, Q10, Q13), **0 HELD**.
No clause is a restatement of admitted F51 ground in the round-77 sense (Q07/Q08/Q12, dropped at
`corpus/lessons/round-77.md:13`), because each of the seven either states a batch-only fact (Q01, Q03, Q09's
partiality, Q10's scope, Q13's selectivity) or states an endpoint-projection fact that F31's format rule does
not reach (Q02). The four PARTLY-HELD verdicts are *scope* overlaps, not content duplicates, and each is
discharged by attributing the held part to its owner rather than re-teaching it.

## 2. Clauses I judge NOVEL

- **Q01** — batch endpoint definition, `:24`. No admitted entry; F51:75/:80 explicitly parks the endpoint.
- **Q03** — input-matched response ordering, `:24`. No admitted entry holds any OSV response-order rule.
- **Q11** — whole-queryset 3,000 threshold, `:169`. No admitted entry holds a set-level threshold; the numeral
  `3,000` occurs nowhere in the corpus outside `SKILL.md:675` (bounty dollars).

## 3. Clauses I think should be dropped

**None of the seven must be dropped on distinctness grounds.** Two drafting hazards do attach to the set as
frozen, and both are for the L1/drafter to handle inside the entry, not by changing the claim:

1. **Q10 is the highest paraphrase risk of the seven** (medium). If the entry states its rule as "pagination
   occurs above 1,000 vulnerabilities" it collapses into F51:47 / S108.txt:136. It survives **only** if its
   falsifiable rule is scoped to "an individual query *within the queryset*" (and, ideally, paired with Q11's
   set-total limb). If the drafter cannot scope it, drop **Q10** and keep Q11 — Q11 carries the genuinely new
   half of the trigger set, Q10 carries the numeral F51 already owns.
2. **Q13 shares its clause stem with F51:47 / S108.txt:144** ("To get the next page of results, your next
   request … page_token"). Its novelty is the word **"only"** (per-query selective replay). It must be written
   with that selectivity, or it too becomes a restatement.

Two further notes on the *dropped* set (frozen: Q04/Q05/Q06/Q07/Q08/Q12 are not claimed), which the drafter
must respect:

- **Q12 (`:170`) is dropped as F51-held, but it is the qualifier on Q10/Q11.** S112:170 says "These numbers can
  vary slightly because of threading…" — "these numbers" = the 1,000/3,000 figures claimed by Q10/Q11. The
  round-77 draft listed exactly this as a rejected over-generalization ("The 1,000 and 3,000 figures are hard
  limits a client may rely on. Not a page sentence…"). Since Q12 is not claimed, the entry must still cite
  `S112.txt:170` (located, **not** pinned in the round-78 manifest) as the reason Q10/Q11 are page-stated
  thresholds and not guarantees, and must not present 3,000 as a hard limit.
- **Q04/Q05/Q06 dropped** also removes the round-77 anchor defect: the round-78 manifest pins
  `24,24,24,166,168,169,195` — all exact-line correct — so the r77 one-line drift (declared `:30`/`:31` vs
  actual `:31`/`:32`) does not recur.

## 4. Other lane-owned files that already name querybatch as described ground (item 3 of the seat spec)

| File:line | What it says | Bearing on the claim |
|---|---|---|
| `corpus/knowledge/osv-post-v1-query-contract.md:75` | F51's Limits bullet: "the other endpoints in the page's navigation (**POST /v1/querybatch**, GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). They are **listed, not described**." | The endpoint *path string* is already-held listed-not-described ground; it must not be claimed as new. The only mention of querybatch in all of `corpus/knowledge/` (`grep -rn -i querybatch corpus/knowledge/` → 1 hit, this line). |
| `corpus/knowledge/osv-post-v1-query-contract.md:74` | F51 Limits: "the OSV record format … its fields belong to F31." | Confirms Q02's held half lives with F31; the entry claims the projection, not the record fields. |
| `corpus/knowledge/osv-post-v1-query-contract.md:80` | F51 scope limit: "the request and response contract of `POST /v1/query` only … the other endpoints stay out." | F51 disclaims the batch endpoint; Q01/Q03/Q09/Q10/Q11/Q13 do not restate F51. |
| `corpus/knowledge/osv-post-v1-query-contract.md:63` | F51 Distinctness: F31 / S080 own the record format. | Cross-reference the entry must cite for Q02's field half. |
| `corpus/knowledge/osv-affected-range-events.md:23` | F31: "The id and modified fields are required. For schema versions above 1.0.0, the `schema_version` field is also required." (S080.txt:374-375) | The held half of Q02. Note the batch endpoint returns id+modified *without* `schema_version` — the entry may note the difference, but must not restate F31's required-set rule. |
| `PROVINCE.md:178` | F31 scope limit: "the format's range/event semantics only — **the osv.dev service API** … stay out". | F31 does not reach Q02's endpoint projection. |
| `PROVINCE.md:219` | F51 Frontier amendment: single-query contract; scope limit "not the other endpoints". | Same as F51:80. |
| `corpus/README.md:1159` | F51 Frontier row (single-query contract). | No querybatch mention. |
| `corpus/README.md` (whole file) | `grep -n 'F54' corpus/README.md` → no hits; `grep -n -i 'querybatch' corpus/README.md` → no hits (rc=1); the only `batch` hit is `:22` "Board intake + batch finalize" (unrelated). | **No Frontier row F01–F53 names querybatch as described ground**; the F54 row does not exist yet at the freeze commit. |
| `PROVINCE.md` (whole file) | `grep -n -i querybatch PROVINCE.md` → no hits (rc=1). | PROVINCE names no querybatch ground. |
| `corpus/SOURCES.md:123` (S111 row) | `status=queued`, `used-by=—`; scope cell says "not any other endpoint's payload or parameters"; `S111.txt:30` = "Batched query vulnerabilities for given package versions and commit hashes." | **Adjacent, queued, not held.** The overview page names the batch capability in one weaker line (no "at once"); Q01's claim is the endpoint's own definition. The entry must state that S111 stays queued and is not claimed (as the round-77 draft did). |
| `corpus/SOURCES.md:124` (S112 row) | `status=queued`, `used-by=—`; scope cell already names "the queries-array payload, the ids-and-modified-only return shape, the input-matched response-ordering guarantee, the per-item version rules with the 400 Bad Request consequence, and the per-query pagination semantics (next_page_token per result, the 1,000/3,000 thresholds, the threading-variance note, the follow-up-request rule)"; teaches cell "Batch OSV lookups by request shape: one POST carries a queries array … results carry vulnerability ids and modified only in input order, and pagination is per-query at the 1,000/3,000 thresholds…". | The registry already *describes* the source's content in prose, including the three clause families this claim drops (version rule/400, threading note). B1 permits only the `status`/`used-by` cells to change, so the row will keep describing scope the entry does not claim — acceptable (a source-row scope cell describes the page, not the entry), but the entry's `source:`/`recheck:` lines must cite the **round-78** manifest, not round-77's (round-77's still pins 13 quotes and would print 13 OK lines). |

## 5. Falsifiable-rule interactions the drafter should encode (measured, not inferred)

- **F51:49's rule is response-shaped; the batch shape breaks its naïve generalization.** F51's falsifiable rule
  is "a response that contains `next_page_token` is not the complete answer to the query". In the batch
  response the token sits **per result item** (`S112.txt:171-193`, `"results": [ { "vulns": [...],
  "next_page_token": "token for query 1" }, … ]`), and the item without a token is complete. The entry should
  therefore state the per-item rule for Q09/Q13, and may flag that F51's response-level phrasing does not
  transfer verbatim.
- **Q10/Q11 need the S112:167 gate.** `:167` = "For the v1/querybatch endpoint pagination will occur when **at
  least one of the following conditions are met**:". `:167` and `:194` are **located but not pinned** in the
  round-78 manifest (anchors are 24,24,24,166,168,169,195), so the entry may cite them as context in a
  Limits/rejected-over-generalization section but must not ground a claimed clause on them.
- **The batch page states no time-based trigger and no response-size limit.** `grep -n -i 'second' S112.txt` →
  no match (rc=1); `grep -n -i -E 'MiB|size limit|response size' S112.txt` → no match (rc=1). Those stay with
  F51 (S108.txt:136, :148); the entry's Limits section should record the two absences as measured on this
  capture, as F51 does for S108.
- **No rate limit / credential sentence on the batch page.** `grep -n -i -E 'rate limit|ratelimit|quota|api
  key|api_key|authenticat|credential' S112.txt` → no match (rc=1). The overview page's rate-limit answer
  (`S111.txt:36`) stays with the queued S111 row.

## 6. Verdict

No routed C2 defect found from this seat. B6's literal half passes (0 files per quote). The paraphrase half
passes for all seven clauses: 3 NOVEL, 4 PARTLY-HELD with the held part named and attributable, 0 HELD, and
**no clause restsates F51**. Two drafting conditions attach to the frozen set and are recorded above for the
L1: **Q10** must be scoped to "an individual query within the queryset" (its numeral belongs to F51:47), and
**Q13** must carry its "only" (selective replay) or it becomes S108.txt:144 restated. **Q11** is the one
threshold clause the lane holds nowhere and is the safest load-bearing new fact in the set.

## SHONEN

- Read (read-only, no edits): `corpus/source-snapshots/round-78/{S112.txt,manifest.json}`,
  `corpus/source-snapshots/round-77/{S112.txt,manifest.json}`, `corpus/source-snapshots/round-73/S108.txt`,
  `corpus/source-snapshots/round-76/S111.txt`, `corpus/knowledge/osv-post-v1-query-contract.md` (all),
  `corpus/knowledge/osv-affected-range-events.md` (Claim 1), `corpus/knowledge/github-global-security-advisories-rest-api.md:54,:78`,
  `corpus/knowledge/openssf-scorecard-checks.md:31-42,:77`, `corpus/knowledge/github-advisory-database-curation-semantics.md:75,:120`,
  `corpus/SOURCES.md:120-124`, `corpus/README.md:1135-1189`, `PROVINCE.md:178,:197,:219`,
  `corpus/lessons/round-77.md:9,:13`, `.ufo/waves/round-78/claims.json`, `.ufo/waves/round-78/w1-spec.json`,
  `.ufo/waves/round-77/w1/entry-osv-post-v1-querybatch-contract.md`.
- Ran (read-only over committed bytes; `TMPDIR` = scratch): `source-recheck.py --manifest
  corpus/source-snapshots/round-78/manifest.json --source S112` (rc=0, 7/7 `anchor=<n>-ok`);
  `git ls-tree`/`git show`/`git log` at base and freeze; `grep`/`awk` census sweeps as quoted above.
- Not run (out of seat scope, no full gate suite): `frontier-recheck-count.py`, `capture-binding-check.py`,
  `sources-census.sh`, `source-recheck.py` on the round-77 manifest.
- Wrote: this file only, at `.ufo/waves/round-78/w1/ScoutDistinct.md`. No lane-tree edit, no commit, no push.
