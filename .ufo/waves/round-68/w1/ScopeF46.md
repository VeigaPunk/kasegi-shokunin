# ScopeF46 — round 68 W1, C2 sibling-overlap and novelty screen (F46 / S102)

**Verdict: SCOPE CLEAR.** No held row, no sibling province, and no pinned capture already holds the
Scorecard API swagger route family, the `ScorecardResult`/`ScorecardCheck` definitions, or the
aggregate-score field. F46 opens a recorded lead (`corpus/SOURCES.md:164`). It also fills ground
that F35 explicitly left out (`PROVINCE.md:197`, `openssf-scorecard-checks.md:91-92`). So the two
rows complement each other and do not overlap. Four residuals for the entry writer are listed at
the end. None of them defeats the frozen predicate.

Measured at lane HEAD `82b3b7d4704e914eb224e7bb24e57aa9cbd8603f` (= C1 implementation commit;
`git -C <lane> rev-parse HEAD`). Read-only. No lane file edited outside this report and its receipt dir.

Receipts (this dir `w1/ScopeF46/`):
- `corpus-hit-census.txt`: step-2 counts per path and line.
- `sibling-province-screen.txt`: step-3 screen of all 21 `*-shokunin/PROVINCE.md`.
- `snapshot-consumer-sweep.txt`: extra sweep of downstream consumers over `corpus/source-snapshots/**`.

## (1) Held neighbor entries — do they hold the swagger ground?

The columns are: R = swagger route family; SR = the ScorecardResult definition; AG = the aggregate-score field; SC = the ScorecardCheck shape.

| entry | R | SR | AG | SC | holding / disclaiming sentence |
|---|---|---|---|---|---|
| `openssf-scorecard-checks.md` (F35/S086) | no | no | no — **explicitly disclaimed** | no (per-check *documentation*, not the result-object schema) | L91-92: "The aggregate 0-10 score computation, the risk-based weights, the publisher/API endpoints and the Prox/CI integration are NOT in this document and are NOT captured; nothing here asserts them." |
| `cve-services-publication-api.md` (F30/S078) | no (holds a *different* OpenAPI 3.0.2 route family, CVE Services 2.8.8.1) | no | no | no | zero hits for scorecard/swagger/aggregate; it shares only the *shape* of the row (a first-party machine-interface contract) |
| `nvd-api-2.0-retrieval-interface.md` (F33/S083) | no | no | no | no | zero hits; NVD CVE response instance |
| `nvd-api-2.0-response-schema.md` (F34/S085) | no | no | no | no | zero hits; NVD JSON Schema. This is the schema-vs-instance precedent F46 follows (F34 schema / F33 instance ≈ S102 contract / refused live result) |
| `cisa-vulnrichment-record-list.md` (F37/S088) | no | no | no | no | zero hits; git-trees catalog surface |
| `github-repository-security-advisories-rest-api.md` (F36/S087) | no | no | no | no | zero hits; GitHub advisories REST routes |

Command for the five non-F35 entries (output: only their header lines; the only extra hit is the `openapi` term in F30's own source line, L3/L78):
`for f in cve-services-publication-api nvd-api-2.0-retrieval-interface nvd-api-2.0-response-schema cisa-vulnrichment-record-list github-repository-security-advisories-rest-api; do grep -niE 'scorecard|swagger|openapi|aggregate|ScorecardResult|ScorecardCheck|/projects/|definitions' corpus/knowledge/$f.md; done`

Whether S086's capture already holds the API: `grep -niE 'aggregate|api\b|/projects/|weight' corpus/source-snapshots/round-54/S086.txt` returned 4 lines, and none of them is the Scorecard API:
- L114 is a branch-protection reviewer weight.
- L183 is the *OpenSSF Best Practices badge API*, a different service.
- L385 is the GitHub License API.
- L697 reads "there is no API available".

## (2) Corpus grep (knowledge/ + README + SOURCES + SKILL + PROVINCE)

Python `re` with IGNORECASE, line-hit counts; full table in `corpus-hit-census.txt`.

| pattern | total | paths |
|---|---|---|
| `scorecard` | 44 lines / 66 matches | ledger 12, F35 entry 12, root-loss 1, source-tree-loss 1, README 6, SOURCES 8, SKILL 3, PROVINCE 1 |
| of which the `SCORECARD.md` filename | 19 lines / 25 matches | ledger 12, F35 L82, root-loss L30, source-tree-loss L349, SOURCES L93/L221, SKILL L1071/L1098 |
| `scorecard` excluding `SCORECARD.md` | 29 lines / 41 matches | F35 entry 11, README 6 (L828-830, 837, 841, 887), SOURCES 8 (L93, 95, 152, 154, 164, 221, 222, 226), SKILL 2 (L1071, 1115), PROVINCE 1 (L197), ledger 1 (L81) |
| `securityscorecards` | **0** | — |
| `swagger` | **0** | — |
| `aggregate score` (literal) | **0** | — |
| `aggregate[- ]score` | 4 lines | SOURCES L164, L221, L239, L244 |

Each hit is classified as one of three kinds.

- **Held ground (F35 only, check documentation):** the F35 entry; README L828-830, L837, L841 (the F35 map and frontier rows); SOURCES L93 (S086 row) and L221-222 (F35 sweep and registry bullets); PROVINCE L197. Every one of them is check-documentation ground. Where they mention the aggregate score or the API, they disclaim it. For example, SOURCES L93 says "the aggregate 0-10 score computation, weights, publisher/API and Prox stay out (not in this document)". PROVINCE L197 says "the aggregate 0-10 score computation, weights, publisher/API and Prox are unasserted".
- **Lead, which F46 consumes:** SOURCES L164: "OpenSSF Scorecard aggregate-score/API documentation — unopened portion only; S086 already holds the check documentation, not a general scorecard.dev API contract." SOURCES L239 records the narrowing ("OpenSSF whole-surface lead → narrowed to aggregate-score/API only (S086 holds checks)"). SOURCES L244 says "the OpenSSF aggregate-score/API portion remain[s] unopened". SOURCES L154 is an older "stay unopened leads" note.
- **Incidental, not this ground:**
  - every `SCORECARD.md` filename hit;
  - README L887 and SOURCES L95/L226, which name the round-52 lane SCORECARD "planned-for-53";
  - SKILL L1071 ("a reworded SCORECARD bar") and L1115 ("D-D SCORECARD round-38 section");
  - ledger L81 (`ExecConsiderthese.scorecard.append.md`).
- **New:** none. No held line names `securityscorecards`, `api.scorecard.dev`, swagger, `ScorecardResult`, `ScorecardCheck` or the aggregate-score field.

Extra consumer sweep over `corpus/source-snapshots/**` (`snapshot-consumer-sweep.txt`):
- `securityscorecards`, `scorecard.dev`, `ScorecardResult`, `ScorecardCheck` and `Aggregate score` appear only in `round-68/S102.txt` and `round-68/manifest.json`, i.e. the C2 input itself.
- `swagger` has one more hit, `round-32/S050.txt:449` ("/ swagger-ui 等"). That is 360SRC's list of sensitive paths, so it is incidental.
- `ossf/scorecard` appears in S086 L98/170/276/473/527/528. All of these are GitHub repo/issue/blob links inside the check documentation, so they are incidental.

## (3) Province boundary

- **kasegi:** line 3 reads "**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages". A supply-chain risk-scoring API is inside the province because the precedent is already admitted. F35 (PROVINCE L197) put the Scorecard *program's* check rules in the corpus as triage-adjacent security-health scoring. F30/F36 (L176/L199) admitted first-party machine-interface contracts. F34 (L195) admitted a contract artifact over a served instance. "Live-target testing is refused; this corpus is documentation only" (L52) is satisfied: S102 is a static contract, and the one served instance was refused (claims.json `refused_candidate`; `corpus/lessons/round-68.md:22-26`).
- **Siblings:** I screened all 21 `*-shokunin/PROVINCE.md` files for `scorecard|securityscorecards|swagger|openssf|supply[- ]chain|risk[- ]scor|security[- ]health` (`sibling-province-screen.txt`). No sibling claims this ground.
  - Every sibling `scorecard` hit is the lane's own `SCORECARD.md` filename: game-dev-2d L12, game-dev-3d L55/56/67/82, kaidoku L588/603, kama L17/174, kengaku L91/751/864/1108, kumitate L12, mado L65/126/141, mori L619, tsukuroi L222…L529.
  - The only `supply-chain` hit is a *disclaimer*, kake L504: "Domain boundary unchanged: this is evidence about the lane's own instruments, not supply-chain provenance and not any claim about a published site."
  - Zero `openssf`/`swagger`/`securityscorecards` in any sibling.
  - kasegi's Adjacent list (L45-50: chousa, kagi, kake, kengaku) names no supply-chain owner either.

## What the capture actually holds (novelty confirmed against S102 itself)

`json.loads(S102.txt)` succeeds:
- **paths:** `/projects/{platform}/{org}/{repo}` with get and post; `/projects/{platform}/{org}/{repo}/badge` with get; `/version` with get.
- **definitions:** Error, Repo, ScorecardCheck, ScorecardResult, ScorecardVersion, VerifiedScorecardResult, VersionInfo.
- **info:** title "OpenSSF Scorecard API", version 1.1.0.
- **host and schemes:** `api.scorecard.dev`, `["https"]`.
- **anchors:** `score` with "Aggregate score of the repository" at L352-353; ScorecardCheck at L297; ScorecardResult at L336.
- `sha256sum S102.txt` gives `6ebb8552…c2caa0` and `wc -l` gives 429, both matching the frozen pin.

## Residuals and disagreements (for the L1 / entry writer; none touches the frozen counts)

1. **The aggregate-score lead is only partly consumed.** S102 holds the aggregate-score *field*, typed and described as "Aggregate score of the repository" (L353). It does not hold how the score is computed or weighted. The F46 entry must keep "computation and weights unasserted". Otherwise it claims more than its source, and the SOURCES L164 lead should be narrowed to "computation/weights only" rather than retired outright. This follows the r56/r57 practice of recording the lead flip in Registry-changes bullets while leaving the lead bytes unchanged.
2. **Host and served URL differ.** The URL fetched is `api.securityscorecards.dev/swagger.json`, but the contract declares `host: api.scorecard.dev` (L17). The claim names both. The entry's source line should say which one is the fetch URL and which one is the document's declared host, so a recheck re-fetches the right one. SOURCES L164 calls it the "scorecard.dev API contract", which matches the declared host.
3. **Manifest byte field.** `round-68/manifest.json` gives `"bytes": 11802` with no `snapshot_bytes`, while the file on disk is 7595 bytes (`stat -c %s`).
   - This matches the S087 convention, where `bytes` is the fetched size (937712) and `snapshot_bytes` is 137738.
   - The S086 manifest also sets `snapshot_bytes`; for S086 both fields equal the file size, 46441.
   - S102's manifest omits `snapshot_bytes`. The lesson draft (`corpus/lessons/round-68.md:14`) states "11802 fetched bytes, normalized snapshot 7595 bytes".
   - The SOURCES row should carry both figures. The manifest is a committed pre-freeze input, so I did not edit it.
4. **The surface is wider than the target.** The contract also defines a POST route (with VerifiedScorecardResult), the badge route and `/version`, which the frozen target does not name. Admitting "the route family" is accurate. Any claim about the POST (publish) semantics needs its own located quote.

## Tooling / hygiene
No tools installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r68/ScopeF46/` was created and then removed before yield. No git mutation. Nothing under /tmp is cited.
