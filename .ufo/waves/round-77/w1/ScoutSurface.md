# ScoutSurface — F54 distinctness + surface recon (read-only)

Seat: `ScoutSurface` (scout, leaf). Round 77, attempt 1, wave w1.
Freeze commit read: `539a43877809bd90b6f506e8fd24a6d871598cd5`. Base: `2e53fc74776824898b5c5eb914aeddc19a091157`.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scratch: `/fast/scratch/hyaku/kasegi-r77/ScoutSurface` (removed at yield).
No git/jj mutation, no corpus edit, no registry edit. Read-only git only (`show|log|rev-parse|ls-tree|diff|status`).

Receipts written by this seat (this dir):
- `ScoutSurface.endpoint-probe-r77.txt` — the six HTTP receipts + two morning-slug 404 reproductions.
- `ScoutSurface.sweep-table-r77.txt` — raw grep output for every pattern, the anchor-vs-actual-line check over all three OSV manifests, the F54 id state, and the 21-lane sibling sweep.
- `ScoutSurface.distinctness-verdicts-r77.txt` — the per-clause verdict table.

Subject: the OSV.dev `POST /v1/querybatch` contract (frontier F54 candidate, C2 claim), candidate ground = the batch-contract clauses pinned in `corpus/source-snapshots/round-77/manifest.json` (Q01–Q13).

---

## 1. Summary

| question | answer |
|---|---|
| Is any B6 ground already held? | **No** — 13/13 quoted clauses are new to the lane's held set (S080/F31 record format, S108/F51 single-query contract, S111 overview). Three clauses (Q07, Q08, Q12) are the batch page's **restatements of already-held S108 sentences**; the restatement is a new citation, not a new rule, and B6's cross-reference is satisfied. |
| Do the four other endpoint pages' URL shapes resolve? | **Yes — 4/4 HTTP 200**, at the S111-navigation slugs `get-v1-vulns/`, `post-v1-determineversion/`, `get-v1-importfindings/`, `post-v1-ubuntu-binary-to-source/`. The morning slugs (`get-v1-vulns-id/` and siblings) reproduce **404**, 11373 bytes. |
| Sibling overlap? | **None.** `querybatch` occurs in exactly one lane's `corpus/knowledge/` (kasegi's own F51 entry). Zero hits across all 20 other lanes. |
| Defects found | **Two**, both routed (not edited): F1 the manifest anchors Q04/Q05 sit one line off their quotes; F2 the round-77 lesson's slug-lead line names slugs that are **not in any frozen capture** and its "morning slug" attribution is unverifiable from the corpus. |

---

## 2. (1) QUALITY R114 subject sweep + R125 admitted-entry sweep

**R114 — by SUBJECT, not by neighbour.** Subject = the OSV project / osv.dev. Command and full output: `ScoutSurface.sweep-table-r77.txt` §1.

`grep -rn -i 'osv' corpus/SOURCES.md corpus/knowledge/*.md` — every OSV hit in the lane, with verdict:

| path:line | what it holds | verdict for F54 |
|---|---|---|
| `corpus/SOURCES.md:71` | S065 — Open Source Vulnerability (OSV) format schema (`ossf.github.io/osv-schema/`) | record format; **already-held, excluded by B6** |
| `corpus/SOURCES.md:86` | S080 — OpenSSF OSV format specification, same URL as S065 (dup URL, inherited W04) | record format; **already-held, excluded by B6** |
| `corpus/SOURCES.md:93` | S086 — OpenSSF Scorecard checks (mentions OSV service) | unrelated subject; no contest |
| `corpus/SOURCES.md:120` | S108 — OSV.dev API reference, `POST /v1/query` | **already-held** (F51). Cross-referenced by B6. |
| `corpus/SOURCES.md:123` | S111 — OSV.dev API overview, status `queued` | **already-held (queued)**. B6: "the overview page stays S111 (queued)". |
| `corpus/SOURCES.md:124` | S112 — OSV.dev API reference, `POST /v1/querybatch` | the round-77 row under review |
| `corpus/knowledge/osv-affected-range-events.md:1,3,10,18,90` | F31 / S080 OSV record format | **already-held**, excluded by B6 |
| `corpus/knowledge/osv-post-v1-query-contract.md:1,3,9,21,45,47,49,51,63,75,78` | F51 / S108 single-query contract | **already-held**; `:75` explicitly defers `POST /v1/querybatch` as "listed, not described" |
| `corpus/knowledge/openssf-scorecard-checks.md:31,34,35,83` | OSV service as a *consumer* of Scorecard data | unrelated subject; no contest |
| `corpus/knowledge/github-advisory-database-curation-semantics.md:75,120` | cites the OSV *format* statement (S105.txt:567) | unrelated subject; no contest |
| `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md:79` | "F31 / S080 (OSV format ranges): unrelated" | no contest |

**Clause-by-clause** (distinctive-string grep per clause; full table in `ScoutSurface.distinctness-verdicts-r77.txt`):

| clause | anchor | verdict | evidence |
|---|---|---|---|
| Q01-batch-definition | 24 | **new** | `S112.txt:24`; no corpus hit. `S111.txt:30` "Batched query vulnerabilities for given package versions and commit hashes." is the overview's one-line listing = listed-not-described. |
| Q02-return-shape | 24 | **new** | `S112.txt:24`; zero hits outside round-77. `S080.txt:32,109` "modified" is the **record** field (F31), not the endpoint return shape. |
| Q03-ordering | 24 | **new** | `S112.txt:24`; `grep -rn 'guaranteed' corpus/knowledge/` → only `cisa-cvd-program-stages.md:48` and `osv-affected-range-events.md:90` (both unrelated); `grep -rn 'match the input' corpus/` → **0 hits**. |
| Q04-params-same | 30 | **new** | `S112.txt:31`; the *deferred* content (params) is already-held S108/F51; the batch-multiplicity clause is new. |
| Q05-pagination-instructions | 31 | **new** | `S112.txt:32`; batch-specific pointer, no corpus hit. |
| Q06-item-rules | 34 | **new** | `S112.txt:34`; batch-level scoping sentence. The rules it references are already-held S108/F51. |
| Q07-version-rule | 35 | **new (restatement)** | `S112.txt:35` "Use either version or a versioned purl, not both." ≡ already-held `S108.txt:40` (quoted at `osv-post-v1-query-contract.md:21`). Same rule, batch wording. |
| Q08-400 | 36 | **new (restatement)** | `S112.txt:36` "Items with both will return 400 Bad Request." ≡ already-held `S108.txt:41` (`osv-post-v1-query-contract.md:21`). |
| Q09-partial-tokens | 166 | **new** | `S112.txt:166`; batch-only partial-token distribution. F51 holds the single-query mechanism (`S108.txt:135`). |
| Q10-individual-1000 | 168 | **new** | `S112.txt:168`; per-query-in-queryset threshold. F51 holds the single-query trigger (`S108.txt:136`). |
| Q11-total-3000 | 169 | **new** | `S112.txt:169`; `3,000` elsewhere only in `round-24/S014.txt:168` (CVE counts, unrelated). |
| Q12-threading-variance | 170 | **new (restatement)** | `S112.txt:170` "These numbers can vary slightly because of threading and the page size may change in the future." ≡ already-held `S108.txt:136` "The page size can vary slightly because of threading and may change in the future.", **already quoted in `corpus/knowledge/osv-post-v1-query-contract.md:47`**. Different referent (the 1,000/3,000 thresholds vs the single-query page size); same rule. |
| Q13-next-request | 195 | **new** | `S112.txt:195`; per-query token selection. F51 holds the single-query follow-up (`S108.txt:144`). |

**R125 — admitted-entry sweep.** The already-held set is checked for the *admitted entries*, not only the navigation captures:

- `corpus/knowledge/osv-post-v1-query-contract.md` (F51, admitted): grep `threading` → 1 hit, `:47` — this is the **Q12 substance already held**. grep `next_page_token` → `:45,47,49` — the single-query token mechanism (Q09/Q13 cite it as already-held). grep `400 Bad Request` → `:21` — the **Q08 substance already held**. grep `Use either the top-level version field` → `:21` — the **Q07 substance already held**.
- `corpus/knowledge/osv-affected-range-events.md` (F31, admitted): the record format only (Q02's `modified` field is the record's, not the endpoint's).
- `corpus/knowledge/openssf-scorecard-checks.md`, `github-advisory-database-curation-semantics.md`, `fuzzilli-js-engine-fuzzing-framework.md`: no batch-contract ground.

**Verdict on the seat's question — is any B6 ground already held?**
**No.** B6's own carve-out already anticipates the only overlaps: "the single-query contract ground (payload keys, version rule content, pagination basics, response-size limits) is cross-referenced as already-held from S108/F51 and not claimed". Q07/Q08/Q12 are the batch page's restatements of exactly that already-held single-query content, cited at their new locations (`S112.txt:35,36,170`), not claimed as new rules. The S112 registry row (`corpus/SOURCES.md:124`) states the same exclusions, and F51's Limits bullet (`corpus/knowledge/osv-post-v1-query-contract.md:75`) already deferred this endpoint. **B6 holds.**

**One thing the drafted entry must not do (advisory to the L1):** Q07/Q08/Q12 are restatements. If the entry presents them as *the OSV version rule* / *the 400 rule* / *the threading caveat* rather than as *the batch page's own restatement of the rule F51 already holds at S108.txt:40,41,136*, the entry re-claims held ground and B6 fails at review. The scope limit should be: this entry owns the **batch** contract; the version rule, the 400 consequence and the page-size caveat remain F51's, cited across.

---

## 3. (2) Four HTTP receipts for the leads section

Reproduced with `curl -sS -o /dev/null -w 'code=%{http_code} bytes=%{size_download}' -L`. Full receipt: `ScoutSurface.endpoint-probe-r77.txt`.

| URL | code | bytes |
|---|---|---|
| `https://google.github.io/osv.dev/get-v1-vulns/` | **200** | 19961 |
| `https://google.github.io/osv.dev/post-v1-determineversion/` | **200** | 30242 |
| `https://google.github.io/osv.dev/get-v1-importfindings/` | **200** | 16418 |
| `https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/` | **200** | 18769 |
| `https://google.github.io/osv.dev/post-v1-querybatch/` (S112's own page) | 200 | 30406 |
| `https://google.github.io/osv.dev/post-v1-query/` (S108's own page) | 200 | 33417 |

Morning-slug 404 reproduction (the round-77 lesson's `R-77-C` claim):

| URL | code | bytes |
|---|---|---|
| `https://google.github.io/osv.dev/get-v1-vulns-id/` | **404** | 11373 |
| `https://google.github.io/osv.dev/post-v1-determineversion-id/` | **404** | 11373 |

The 11373-byte 404 body matches the byte count recorded in the round-77 lesson's reject line (`corpus/lessons/round-77.md:12`, untracked working-tree file). **The four lead slugs are live and the morning slugs are dead, exactly as the lesson says.** No capture was taken and no registry edit was made, per the seat bounds.

Where the live slugs come from: the live page's own navigation `href`s, extracted read-only from `https://google.github.io/osv.dev/post-v1-querybatch/` → `href="/osv.dev/get-v1-vulns/"`, `/osv.dev/post-v1-determineversion/`, `/osv.dev/get-v1-importfindings/`, `/osv.dev/post-v1-ubuntu-binary-to-source/`.

---

## 4. (3) Sibling overlap

Read-only scan of every lane's `corpus/knowledge/` at `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge` (21 lanes; full table `ScoutSurface.sweep-table-r77.txt` §4):

| lane | `querybatch` hits | `osv.dev` hits |
|---|---|---|
| kasegi (this lane) | **1** (`osv-post-v1-query-contract.md:75`, the deferral) | 3 |
| all 20 other lanes (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi) | **0** | **0** |

Also checked: no lane's `corpus/SOURCES.md` contains `querybatch` or `osv.dev` (kake/kengaku/chousa/kagi/tabi/souji → 0 each).

**Verdict: no sibling adjacency, nothing to absorb.** This agrees with `ConnectorOverlap` §3 (`w1/ConnectorOverlap.md`), which reached the same conclusion over the same trees; I report it independently rather than citing it as proof.

---

## 5. Defects found (routed, not edited)

### F1 — the frozen manifest anchors Q04 and Q05 one line off their quotes (C2 B0/B5, depth:verifiability)

`corpus/source-snapshots/round-77/manifest.json` declares `Q04-params-same` at `anchor: 30` and `Q05-pagination-instructions` at `anchor: 31`. Their quotes are **not** on those lines:

| quote | declared anchor | line the quote is actually on | anchor == actual? |
|---|---|---|---|
| Q04 "The parameters are the same as those in POST /v1/query, but you can make multiple queries." | 30 | **31** | no |
| Q05 "Instructions are available for handling pagination for querybatch requests." | 31 | **32** | no |
| the other 11 quotes | — | — | yes (all exact) |

Computed by locating each normalized quote in `corpus/source-snapshots/round-77/S112.txt` line-by-line (`ScoutSurface.sweep-table-r77.txt` §2):

```
round-73/S108: quotes=31 anchors_not_on_quote_line=0
round-76/S111: quotes=13 anchors_not_on_quote_line=0
round-77/S112: quotes=13 anchors_not_on_quote_line=2
   ('Q04-params-same', 30, [31])
   ('Q05-pagination-instructions', 31, [32])
```

The same off-by-one appears in the S112 registry row's cites cell (`corpus/SOURCES.md:124`): "parameters S112.txt:30, item version rules and 400 S112.txt:34-36" — the parameters sentence is at 31, and line 30 is the bare heading "Parameters". The manifest's own `anchor` semantics are the "line the quote is read from", so the row's "parameters S112.txt:30" points a reader at the heading instead of the sentence.

**Why this is not caught.** `corpus/instruments/source-recheck.py:110` builds the anchor window as `raw_lines[max(0, anchor - 1):anchor + 3]` — a **four-line window starting at the anchor**, not an exact-line test. With `anchor=30` the window is lines 30–33, which contains the Q04 quote on line 31; with `anchor=31` the window is lines 31–34, which contains the Q05 quote on line 32. Both therefore report `anchor=N-ok`. Reproduced: `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112` → all 13 quotes `OK occurrences=1 anchor=<n>-ok`, rc 0 — identical to the frozen receipt `.ufo/waves/round-77/controls/c2-prerecheck-r77.txt`. **B0 and B5 pass as written; the anchors are nonetheless wrong by one line for two of the thirteen clauses.**

Impact: B0/B5 are satisfied and the quoted text is genuinely present (both quotes do occur exactly once). The risk is to the *entry's* citations — a reader who opens `S112.txt:30` to check the parameters sentence finds only the heading, and the row's "S112.txt:30" cite is wrong. Round-73/S108 and round-76/S111 have zero such anchors, so this is a regression introduced by the round-77 manifest, not a lane-wide convention.

Routing: the frozen bytes are attack-only ("a finding is a routed defect, never an edit"). Options for the L1, in preference order: (a) leave the manifest bytes alone and make the *entry* cite the true lines (`S112.txt:31` for the parameters sentence, `:32` for the pagination pointer) with a one-line note that the manifest anchor is a window anchor, not a line pointer; (b) if the anchors are load-bearing for a downstream reader, the successor round freezes a corrected manifest (the round-76 precedent, R-B, is that a manifest is not repaired in place). Note the source-recheck receipt itself is unaffected either way.

### F2 — the round-77 lesson's four-endpoint lead line mis-attributes the slug source, and its "S111 navigation" pointer is wrong (C2 coverage, R-125)

`corpus/lessons/round-77.md:12` (untracked working-tree file, written by the L1, not committed):

> reject line (leads, not adopted): `GET /v1/vulns/{id}`, `POST /v1experimental/determineversion`, `GET /v1experimental/importfindings`, `POST /v1experimental/ubuntu/binary-to-source` — the four sibling endpoint pages were probed at the morning slugs `get-v1-vulns-id` and siblings and returned HTTP 404 (`11373 B`, receipts `/fast/scratch/hyaku/kasegi-r77/l1-research/`); **the S111 navigation names the live slugs** `get-v1-vulns/`, `post-v1-determineversion/`, `get-v1-importfindings/`, `post-v1-ubuntu-binary-to-source/` (**`S111.txt` navigation lines**).

Both clauses about the slug source are wrong against the frozen bytes:

1. **The S111 capture does not contain the live slugs.** `grep -c 'get-v1-vulns\|post-v1-determineversion\|get-v1-importfindings\|post-v1-ubuntu-binary-to-source' corpus/source-snapshots/round-76/S111.txt` → **0**, and the same grep over `round-73/S108.txt` and `round-77/S112.txt` → **0**. The captures are tag-stripped text (`grep -c 'href' S112.txt` → 0), so the navigation *hrefs* never survive capture. What S111.txt actually holds is the API path strings: `S111.txt:5` "POST /v1/querybatch", `:7` "GET /v1experimental/importfindings", `:8` "POST /v1experimental/ determineversion", `:9` "POST /v1experimental/ubuntu/binary-to-source" — the `/v1experimental/…` forms, **not** the `get-v1-importfindings/` etc. doc slugs. The live slugs are recoverable only from the live page's `href` attributes (fetched read-only; see §3), never from a capture.
2. **The slug sets the lesson contrasts are not the slug sets the probes used.** The lesson contrasts the *doc* slugs (`get-v1-vulns/`) against *morning* slugs (`get-v1-vulns-id`). But the path strings the S111/S112 captures hold are the API paths (`GET /v1/vulns/{id}`) — a third family. And `GET /v1/vulns/{id}` is not a URL on google.github.io at all; the doc page for that endpoint is `get-v1-vulns/`, which I confirmed 200.

The lesson's *conclusion* survives — the four doc slugs are live (4/4 HTTP 200) and the morning slugs are dead (404, 11373 B, reproduced above) — but the line cites the wrong evidence for it. Under R125 the lead record must say which clauses are already held and where the new ground comes from; a lead whose slug source is attributed to a capture that does not contain those strings is not verifiable from the corpus, and a successor following the cite would go looking for `get-v1-vulns/` in S111.txt and find nothing.

Routing: the lesson is an L1-owned working-tree file. Suggested correction for the L1's `corpus/lessons/round-77.md:12` (and for `R-77-C` at `:41`): name the live slugs as taken from the **live page's navigation hrefs** (with the probe receipts in this wave dir), and record the API path strings as the already-held listed-not-described ground from `S111.txt:5,43` / `S108.txt:5-9`. The lesson's `R-77-C` text says "the S111-navigation slugs are the live ones" — the live slugs are the *doc-site* slugs, and they are not the S111 navigation's strings; the two should be distinguished.

---

## 6. Coverage context — F54 id and the S112 id collision

- **F54 is free.** `grep -c 'F54' corpus/README.md` → **0**; the README frontier rows run `F01 … F53` (53 rows, `grep -oE '^\| F[0-9]+ \|' corpus/README.md`). Round 76 *considered* F54 for the **S111 overview** and refused it (`corpus/lessons/round-76.md:7,9`; `corpus/lessons/round-76-verifier-spotcheck.md:85,92`), so F54 was never bound to a row. Round 77's F54 is the querybatch contract — a different subject, and the id is unclaimed. Note the id is now bound to a *different* subject than round 76's F54 candidate; the README is the source of truth and carries no F54 row, so nothing conflicts, but the lesson should say that round 76's F54 was the S111 overview (refused) so the two are not conflated.
- **S112 id collision with the staged shokuknow package.** B7's first limb is true — `git show 2e53fc7:corpus/SOURCES.md | grep -c 'S112'` → **0**. But B7's stated reason for safety is false: it says the staged package is "94 ids, S001–S094" and that "the new S112 is outside that range". Measured: the staged file `/home/vgpnk/Projects/shokunnow/merge/kasegi/SOURCES.append.md` has 94 rows / 94 unique ids spanning **S031–S124**, and **S112 IS among them** (`SOURCES.append.md:88`, "TC260's own suggestion route and the standards platform's project record"), as is S111 (`:87`). Ids above S094 in the staged set: S095–S124, 30 of them. So the new S112 **does** collide with a staged id — 82 ids collide in total (staged ∩ registry). `ConnectorOverlap` §1 reached the same count independently; I reproduce it here because B7 is a frozen predicate clause whose supporting premise is wrong, and B7 is one of the predicates C2 is scored on. The collision is an id collision, not a content collision (the staged S112 is a different document — the TC260 route probe — and the staged S111 is the NCSC weekly report).
  Effect on the claim: B7's *conclusion* (this is not a merge that the lane can perform blind) is unaffected and the C2 admission can still land — but the sentence "so the staged shokuknow package … cannot collide with it" is a false premise inside a frozen predicate. This is the same L0-routed id question round 76 raised as R-D (`corpus/lessons/round-76.md:40`) and it is still open for S111 as well. Routed to the L0 question file; not a C2 kill on its own.

---

## 7. Checks run (all read-only; each command's output is in a receipt above)

| check | command | result |
|---|---|---|
| freeze identity | `git -C … log --oneline -3 539a4387` | `539a438` = "round-77: freeze C1 (recheck-cwd RESULT-limb gate, 12 checks, 5 mutant kills) and C2 (F54 OSV querybatch on S112) with controls and R126 pre-freeze receipt"; parent `2e53fc7` = the stated base |
| capture bytes | `git show 539a438:corpus/source-snapshots/round-77/S112.txt \| sha256sum` | `f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907` = manifest `sha256`; 216 lines / 4575 bytes = manifest `lines`/`bytes` |
| manifest quotes | `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112` | rc 0, `S112:sha256 OK`, 13 quotes `OK occurrences=1 anchor=<n>-ok` — byte-identical to the frozen receipt `controls/c2-prerecheck-r77.txt` |
| anchor exactness | per-line location of each normalized quote in S112.txt (all three OSV manifests) | **2 anchors off by one** in round-77; 0 in round-73 and round-76 → **F1** |
| registry counts | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 112; `ls corpus/knowledge/*.md \| wc -l` → 91; `wc -l < corpus/instruments/knowledge-expected.txt` → 93; `grep -cE '\.md$' …` → 91 | matches the frozen control `controls/c2-base-counters-r77.txt` freeze-tree state (rows=112, records=91, knowledge 91) |
| F54 id | `grep -c 'F54' corpus/README.md` → 0; README frontier rows F01–F53 (53) | F54 unclaimed |
| HTTP receipts | 6 live + 2 morning-slug probes | 4/4 leads **200**; 2/2 morning slugs **404** (11373 B) |
| sibling overlap | 21 lanes × `corpus/knowledge/` for `querybatch` / `osv.dev` | only kasegi's own F51 deferral; **0** elsewhere |
| staged id set | `grep -oE '^\|[[:space:]]*S[0-9]{3,}' …/SOURCES.append.md` | 94 unique ids, **S031–S124**, S112 present → **§6** |

## 8. Unresolved / not established by this seat

- Whether the L1 will amend the frozen manifest anchors (F1) or route it to a successor round. Not mine to decide; the frozen bytes are attack-only.
- Whether the four endpoint leads will be captured (each needs its own capture + distinctness sweep; R-77-C). This seat captured nothing, per bounds.
- The S111/S112 id collision with the staged shokuknow package is an L0 question (round 76's R-D), not resolved here.
- `git status --porcelain` at the time of writing shows only untracked round-77 wave artifacts (`w1/`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`) plus the L1's untracked `corpus/lessons/round-77.md`. I created only the three `ScoutSurface.*` receipts and this report in `.ufo/waves/round-77/w1/`, plus scratch under `/fast/scratch/hyaku/kasegi-r77/ScoutSurface/` (removed before yield).
