# Round 88 — lesson (kasegi, attempt 1)

Read first: the r87 closure and `corpus/lessons/round-87-verifier-spotcheck.md` (C1 NOT VERIFIED on frozen P3; routed defects 1–7), `corpus/lessons/round-86-verifier-spotcheck.md` and `corpus/lessons/round-87.md`. Two rejected closures in a row (r86, r87) mean a third pauses the lane, so both r88 claims carry a P3 that names their allowed landing paths, and each landing was checked with `.ufo/waves/round-87/l1/landing-scope-check.py` before it was cited. Base `6beead9148945fa695cf3139e8fc9d8e91cc5fd0`, freeze `7f2ebebf7588ead4f4248478f18b989983e94b69`, C1 landing `fd33e1bfe26ad9af13c138feb87c9f222be957cb`, C2 landing `b43dc2154bc09470da2209fb626021da3af3593e` (`.ufo/waves/round-88/landing.json`). Frozen claims, predicates, kill rules and executed controls: `.ufo/waves/round-88/claims.json`, `.ufo/waves/round-88/controls/`. One v1 wave `w1` ran 14 seats; reports under `.ufo/waves/round-88/w1/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; internal-citation repoint, score not claimed to move).** Knowledge-scope tranche 3, a new citation class: backticked sibling-entry citations `<name>.md[:N[-M]]` in `corpus/knowledge/*.md` that resolve.py classifies GONE because they omit the `corpus/knowledge/` prefix. The frozen map `.ufo/waves/round-88/c1/repair-map.json` holds 50 keys (claim-gates ×19, ops-invariants ×10, mission-control ×7, claim-package-contract ×5, nine other entries ×1). A new limb M8 requires every citing line of an anchored key to share an identifier with the cited line range; 54 anchored keys fail it and are excluded, not repointed (`.ufo/waves/round-88/c1/excluded.json`). Meter 703/1754 → exactly 742/1743; counter `.ufo/waves/round-88/c1/knowledge-meter.py` (M1–M6, M8).
- **C2 — coverage, capability extension of `capture-secret-scan` (sourced: S126, S127).** Two new edge classes, cloud signed-URL signatures: `gcs-signed-url-signature` (X-Goog-Signature, 64+ hex; S126) and `azure-sas-signature` (`sig=` of 40+ base64/percent characters in the same query as `sv=YYYY-MM-DD`, either order, `&`/`&amp;`/`\u0026`; S127), plus the `corpus/practice/<pkg>/evidence/` scope (r87 ReviewC2Scanner F1). Frozen counter `.ufo/waves/round-88/c2/capability-check.py` (K1–K6; K4 now exercises `--files`, the r87 routed gap; K6 shows the base instrument misses every round-88 addition).

## Outcome

- **C1:** P1 (`KNOWLEDGE-METER-RESULT pass rc=0`, after 742/1743, M1–M6/M8), P2 (15/15 pins) and P3 (`LANDING-SCOPE from=7f2ebebf to=fd33e1bf changed=8 outside=0 verdict=PASS`) hold at `fd33e1bf` (`.ufo/waves/round-88/l1/c1-landing-r88.txt`); ExecC1Indep re-derived map and exclusions independently, 50/50 and 59/59 identical; CriticClaims re-ran P1–P3: VERIFIED. Semantic qualifier (frozen kill rule: reverted later, reported, never re-scored): ReviewC1Semantics labels the 50 keys 41 CORRECT / 8 WRONG / 1 UNCLEAR; the 8 WRONG citation sites are reverted to their base bytes in the integration commit (7 table cells in `triage-thresholds.md`, one site of a two-key line partially, and the `ground:` line of `japanese-domestic-disclosure-workflow.md`, whose bare name labels the staged shokuknow copy, not the lane entry). See M88-1.
- **C2:** P1 (`CAPABILITY-CHECK-RESULT pass rc=0`, K1–K6), P2 (scanner, allowlist and SCORECARD row byte-equal to the frozen candidates) and P3 (`changed=2 outside=0 verdict=PASS`) hold at `b43dc215` (`.ufo/waves/round-88/l1/c2-landing-r88.txt`); CriticClaims: VERIFIED. Qualifier: the statement's `\u0026` separator clause is true only when the matched parameter is the first in the query (ReviewC2Scanner F1; the left boundary rejects a start after the escape's trailing `6`); the frozen counter cannot see it (F2). The scanner is frozen; the fix is routed to round 89. See M88-2.

## Gate

### S126 — Google Cloud Storage documentation, Signed URLs (admitted, used by the instrument and one entry)

- **URL:** https://docs.cloud.google.com/storage/docs/access-control/signed-urls (the `cloud.google.com` URL redirects here), HTTP 200.
- **Accessed:** 2026-11-07 (captures at 03:30:05Z and 03:30:10Z, byte-identical).
- **Capture:** `corpus/source-snapshots/round-88/S126.txt`, sha256 `b04de8a94c7905d8b768b8dcd7d7e354df3f972ef292bb3e1a1f36aea000b83d`; manifest `corpus/source-snapshots/round-88/manifest.json`, `source-recheck.py` rc 0.
- **Located quote, S126.txt:423-424 (16 words):** "Anyone in possession of the signed URL can use it while it's active, regardless of whether". Also :487 "X-Goog-Signature: The authentication string that allowed requests using".
- **Row change (old → new):** status `queued` (freeze) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md`.

### S127 — Azure Storage REST API reference, Create a service SAS (admitted, used by the instrument and one entry)

- **URL:** https://learn.microsoft.com/en-us/rest/api/storageservices/create-service-sas, HTTP 200.
- **Accessed:** 2026-11-07 (two byte-identical captures).
- **Capture:** `corpus/source-snapshots/round-88/S127.txt`, sha256 `66f8a35e9d598e5f5eecedd9003a7ba7f99c1eda24963e4cf1891245bdfb1312`.
- **Located quote, S127.txt:639 (24 words):** "Used to authorize access to the blob. The signature is an HMAC that's computed over a string-to-sign and key by using the SHA256 algorithm". Also :605 the service SAS example URI ending `&sv=2022-11-02&sr=b&sig=<signature>`. The manifest quote Q01 (S127:404) is 29 words; it is a recheck pin, not this Gate's quote (CriticClaims D8).
- **Row change (old → new):** status `queued` → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md`. Erratum (CriticClaims D8): the row's anchor cell names `601` (the revocation paragraph) beside 402-404, 605 and 638-639; 601 is used by the admitted entry's Claim 4, so the cell is not wrong, but the signature table is 402-404 and 638-639. Not edited (CORPUS rule 2).

### Rejected or deferred this round

- **Azure Storage, "Grant limited access to Azure Storage resources using shared access signatures (SAS)"** — https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview, HTTP 200 on 2026-11-07, captured to scratch (174 lines). Rejected as the C2 source: its example SAS URI (line 80) renders as an image, so the capture holds no `sig=` example, and it never names the `sig` parameter. Flip condition: a capture that carries the example URI as text. S127 replaces it.
- **Google Cloud Storage, "Signatures"** — https://docs.cloud.google.com/storage/docs/authentication/signatures, HTTP 200, captured to scratch (719 lines). Rejected as the C2 source: it describes the signing process but states the `X-Goog-Signature` query parameter only in a form-field list (line 537); the Signed URLs page (S126) states both the parameter and the bearer property. Flip condition: a claim about the V4 signing algorithm itself.
- **Round-87 rejection, wording update (r87 spot-check routed defect 5):** the S3 SigV4 query-auth URL now answers `302` to `https://docs.aws.amazon.com/AmazonS3/latest/API/` before serving the 2,343-byte meta-refresh shell (the r87 lesson recorded HTTP 200 for the URL itself). Outcome unchanged.

### considerthese and assimilation

- **considerthese:** the still-unimplemented proposal closest to this round is `considerthese/2026-10-24.md:49-52` (2026-10-24: capture hygiene at intake). Not implemented this round: C2 already moves coverage and an intake gate in `capture-source.py` would be a second claim on the same axis; routed to round 89 (third round routed, CriticClaims r87 F6).
- **Assimilation: none.** Lane 127 ids, staged 94, collisions 94/94 (`.ufo/waves/round-88/assimilation/collisions`; the staged file predates the lane's S031–S127 expansion). Guard proof on an indented `  | S002 |` row: 0–3-space pattern finds the collision, column-zero pattern misses it, `PASS` (`.ufo/waves/round-88/assimilation/guard-proof.txt`). Quarantine slice re-derived: 7 rows (`quarantine-slice`), unchanged and not hand-checked this round (adoption stays closed). Open L0 `kasegi | round-77` unchanged.
- **Errata recorded (r87 spot-check routed defect 4):** the round-87 manifest quote `S125:Q01-prefix-intro` is declared at anchor 303 while the sentence starts on 304; the manifest is a frozen pin and stays unedited; the anchor-tolerance test is routed to round 89.
- **Prose residue (routed defect 6):** `openssf-scorecard-api-contract.md`'s unbackticked `S102.txt:13` is a prose mention; resolve.py does not collect it; left unchanged.

## Mistakes

**M88-1 — class `lexical-proxy-passes-wrong-anchor`.**

- **What happened:** the round-88 map selected sibling-entry citations with a lexical content proxy (M8: one shared 5+ character identifier between the citing line and the cited range) and froze it with controls that tested only the proxy's rejections (the drift-forge control). The non-author semantic review found 8 of 50 keys WRONG (`.ufo/waves/round-88/w1/ReviewC1Semantics.md` §1): 7 anchored keys passed on a generic word (`decision`, `status`, `SUBMITTED`) and one unanchored key, which M8 exempts, named a foreign file of the same name. CriticClaims measured M8's selectivity: a median 15 % of disjoint ranges in the same entry also pass. The proxy also rejects valid pointer rows whose only backticked span is the citation (4 of 15 sampled exclusions are false negatives).
- **Captured-by:** none before the freeze. The counter's M8 is a proxy by declaration, and no rule required a semantic sample of the passed keys.
- **Fix:** QUALITY R140 — a proxy-selected repoint map is frozen only after a non-author hand-labelled sample of at least 15 keys (unanchored included) shows no WRONG key; check `.ufo/waves/round-88/l1/r140-check.py`. The 8 WRONG sites are reverted to base bytes in the integration commit.
- **Shown able to fail:** `.ufo/waves/round-88/l1/r140-check-r88.txt` — the frozen map against the 50 labels prints `wrong=8 … verdict=FAIL exit=1`; the map without those keys prints `PASS`; 9 labels print `FAIL`.

**M88-2 — class `statement-clause-not-bound-by-counter`.**

- **What happened:** the C2 statement lists `&`/`&amp;`/`\u0026` separators "either order"; the counter's K4 plants the JSON-escaped form only with the matched parameter first in the query, where the pattern's left boundary does not bite. ReviewC2Scanner F1 shows a JSON-escaped copy of S127's own example URI (sv sixth) is missed, and a one-line lookbehind fix passes K1–K6 exactly like the landing (F2), so the counter cannot tell them apart.
- **Captured-by:** none. Every planted case was written by the author of the pattern, from the same mental model.
- **Fix (routed, round 89):** every enumerated clause of a capability statement maps to a planted case in the position the source documents (here: S127:605's parameter order, JSON-escaped), and the counter carries a generated-value limb (CriticClaims D4) so a fixture-literal detector fails.
- **Shown able to fail:** not yet: the fix is a round-89 counter amendment; ReviewC2Scanner's `repro-review-c2.py --only u0026` is the failing case it must kill (`.ufo/waves/round-88/w1/ReviewC2Scanner-receipts/`).

## Routed-defect disposition (r87 spot-check §6)

| # | r87 routed defect | r88 disposition |
|---|---|---|
| 1 | P3 scope breach: wire R139 into landing | Done: both claims carry a P3 naming their allowed paths; each landing's path list was written explicitly and `landing-scope-check.py` printed `verdict=PASS` before the landing was cited (`.ufo/waves/round-88/l1/c1-landing-r88.txt`, `c2-landing-r88.txt`). CriticClaims adds that C1's P1 reads the working tree (D1); the landing clone was clean. |
| 2 | Scanner scope/detection gaps | Partly answered by C2: practice-evidence scope, `--files` limb (K4), GCS V4 and Azure SAS shapes. HAR, percent-encoding, gzip/UTF-16/base64, CloudFront, GCS V2 stay named limits. |
| 3 | Intake gate in `capture-source.py` | Not taken; routed to round 89. |
| 4 | Manifest anchor erratum D-1 | Recorded above; manifest unedited. |
| 5 | S3 URL 302 wording | Recorded above. |
| 6 | Unbackticked `S102.txt:13` | Left unchanged (prose mention). |
| 7 | Open L0 (expired STS token in history) | Unchanged, operator-owned. |

## Wave findings (none re-scores a claim)

- **ExecC1Indep:** independent re-derivation matches the frozen map 50/50 (keys and values) and the exclusions 59/59 (reason strings identical); the frozen counter re-run on a clone of `fd33e1bf` passes M1–M6/M8 at 742/1743.
- **ReviewC1Semantics:** 41 CORRECT / 8 WRONG / 1 UNCLEAR over the 50 keys; of 15 sampled drift exclusions, 4 are proxy false negatives (pointer rows whose only backticked span is the citation) and 2 more suppress one valid site. The 8 WRONG sites are reverted (M88-1).
- **MutC1Counter:** 36 mutants, 29 killed (18 by the frozen eight controls at limb level, 11 only by added isolating controls), 7 survivors (6 equivalent on the frozen tree, 1 stricter-only). At rc level the frozen eight kill 9/36; no frozen control isolates M8 (`drift-forge` also fails M1), so an M8-disabled counter still prints rc 1 there (F1); fix: a drift forge scored at its own target 743/1743.
- **CriticClaims:** C1 VERIFIED, C2 VERIFIED on P1–P3 re-run. Qualifiers: C1's P1 reads the clone's working tree, not the commit (D1); M8 median selectivity 15 % (D2); 55 eligible bare sibling citations remain outside `corpus/knowledge/` (D3); a fixture-literal detector passes K1–K6 (D4); sourcing is shape-level, thresholds and separators are engineering (D6); SCORECARD counting command omits the sha pins (D7); S127 anchor cell (D8); the lesson file the dispositions cite did not exist yet at the landings (D9, closed by this lesson).
- **CriticHarm:** HARM on two collateral points, both fixed in the integration commit: the `japanese-domestic-disclosure-workflow.md:7` repoint (H1, reverted) and three stale sentences in `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md` describing the instrument (H2: shape count, `cases=19`, exit-code line anchor; updated). density, deletions, gate selftests and owned surfaces: no harm.
- **ReviewC2Scanner:** CHANGES-REQUESTED for round 89: F1 (high) `\u0026` misses whenever the matched parameter is not first; F2 the counter cannot see F1 and the 64-hex floor is held only by the sha pin; F3 known-limits list incomplete; F4 20-parameter / 2–6-letter window; F5 no left boundary on the GCS name; F6 `%26` unrecognised.
- **MutC2Scanner:** 24 mutants over the round-88 code, 9 killed, 15 survived (1 equivalent): the counter does not bind the `{0,20}` window, the parameter-name width, the 40-char floor from below, the `sv` date form, the lookbehind, the GCS hex floor from above, `(?i)`, two practice-scope relaxations or the selftest case count. Each survivor names the planted case that would kill it (round 89).
- **MutC2Counter:** 24 counter mutants, 17 killed (8 by the frozen controls, 9 only by designed controls), 1 detected-but-not-verdict-killed, 3 equivalent, 3 structurally unkillable by controls.
- **SentinelRegex:** REFUTED (no super-linear growth; exponents ≈ 1.0 up to 4 MiB). The Azure alternation has no literal prefix and is the dominant cost (≈ 2.8 s on 4 MiB of dense `sv=`); a gated literal prefilter or an atomic value class is routed (D1). HIT lines never print matched bytes.
- **ExecC2Corpus:** on four further first-party pages: 0 false positives; the GCS manual-signing page's 512-hex example is soft-wrapped and missed (named representation limit); CloudFront example missed (out of scope).
- **ScoutSources:** S126/S127 re-open live, HTTP 200, snapshot sha256 equal, all four manifest quotes present once at their anchors; the S126 raw body varies by one nav attribute (202,352 vs 202,356 bytes) while the normalized snapshot is stable (Q-V1). Five round-89 leads opened (CloudFront signed URLs, GCS V2, Azure user-delegation SAS `skv=`, HackerOne `expiring_url`, GitHub raw `?token=`), not yet SOURCES rows.
- **ExecReanchor:** for the 54 drift exclusions, 4 unique best candidate ranges, 8 ties, 42 none within ±3 lines (`.ufo/waves/round-88/w1/ExecReanchor-receipts/reanchor-candidate.json`): most drift is larger than a small offset.
- **ConnectorOverlap:** sibling lanes (kengaku, kama, kotodama, mado) carry ad hoc signed-URL regexes or captured CloudFront URLs in wave receipts; none is a committed instrument kasegi could import. In kasegi `SKILL.md`, 9 of 12 line-anchored `corpus/knowledge/` citations fail the M8 proxy; its first example (`SKILL.md:120` → `program-quirks.md:10`, "fee gate" vs "$100 submission deposit") is a proxy false negative, not drift, which is M88-1's point from the other side: the proxy is no semantic test in either direction.
- **ScribeEntry:** `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` drafted with checks FC-1…FC-7; admitted by the L1 with one added limit (the F1 `\u0026` position limit) and the Azure bullet qualified.
