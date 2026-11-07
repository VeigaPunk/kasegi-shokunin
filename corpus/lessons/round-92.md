# Round 92 — lesson (kasegi, attempt 1)

Read first: the r91 closure (`admitted`) and `corpus/lessons/round-91-verifier-spotcheck.md` (both claims verified; routed defects 1–8), `corpus/lessons/round-91.md` (M91-1..3). Base `0628fd247914555838a42c02ba5d4ac08b7e095d`, freeze `9e4f0d6830dcc9a30c6f524c48d074ec8979f040`, C1 landing `cb1ef2b9856df79c530f3ff1374fa9691ff56233`, C2 landing `58c0c115342877ee556cae19928d69839b0b29f0`, landing receipts `ee830069af1255043aeb39f1d324e6b3e5d69dbd`. Frozen claims, predicates, kill rules and executed controls: `.ufo/waves/round-92/claims.json`, `.ufo/waves/round-92/controls/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; citation repair, score not claimed to move).** Tranche 7: the 30 (site, key) labels the round-91 non-author seat ReviewC1Labels wrote (`.ufo/waves/round-91/w1/ReviewC1Labels-receipts/round92-labels.tsv` at `d0bd4758`). The 25 pairs whose label names an edit get that edit in `corpus/knowledge/triage-thresholds.md` (24 sites) and `corpus/knowledge/root-loss-2026-10-12.md:68`: 10 range repoints, 7 CORRECT qualifications to `corpus/knowledge/<key>`, 2 single-token `MATCHES:` cells to the table's `—` (369, 370), 2 token drops that keep the cell's other tie (58, 144), 2 named repoints (150, 152) and 2 whole-cell repairs (155, 249). The 3 no-edit CORRECT pairs and the 2 EXCLUDED errata pairs (437, 438) stay unchanged. Counter successor binds the map on (site, key) pairs (r91 closure routed defect 2) and makes a CORRECT label's qualification expressible (r91 routed). Pinned meter 947/1947 → exactly 960/1944.
- **C2 — coverage (score 8 held), capability extension of `capture-secret-scan` (sourced: S136, S137).** New shape `github-token`: GitHub's prefixed tokens `ghp_`/`gho_`/`ghu_`/`ghs_`/`ghr_` + exactly 36 base62 characters, and the stateless installation form `ghs_<APPID>_<JWT>` (round-91 ScoutSources lead A: eight bare-prefix fixtures were all missed). Fine-grained `github_pat_` is a named known limit (no opened source states its length).

## Outcome

- **C1:** P1 `KNOWLEDGE-METER-RESULT pass rc=0` (M0 947/1947, M1 960/1944, M3, M4, M5, M6, M9 25/25, M10 want=25 mapped=25 with kinds dash-cell 2, drop-token 2, excluded 2, named 2, named-cell 2, no-edit 3, qualify 7, range 10), P2 pins equal, P3 two paths (`.ufo/waves/round-92/l1/c1-landing-r92.txt`).
- **C2:** P1 `CAPABILITY-CHECK-RESULT pass rc=0` at run-time seed 989818075, 9191 and 1 (K1–K8, K8 29 clauses), P2 landed sha256 `04666f67…` = frozen candidate, P3 two paths and the row equals the frozen candidate row (`.ufo/waves/round-92/l1/c2-landing-r92.txt`).

## Gate

### S136 — GitHub Docs, About authentication to GitHub (admitted, used by the instrument)

- **URL:** https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github, HTTP 200.
- **Accessed:** 2026-11-07 (capture 08:59:56Z).
- **Capture:** `corpus/source-snapshots/round-92/S136.txt`, sha256 `f0edd23c8d6d53a066a6bb90fe4f4f754746df418d833acfc48c44d13943cca0` (equal to the round-91 ScoutSources lead-A capture); manifest `corpus/source-snapshots/round-92/manifest.json`, `source-recheck.py` rc 0 (anchors 158, 160; `.ufo/waves/round-92/controls/source-recheck-r92.txt`); scanned with the frozen candidate before the freeze, hits 0 (`.ufo/waves/round-92/controls/capture-scan-r92.txt`).
- **Located quote, S136.txt:158 (13 words):** "GitHub issues tokens that begin with a prefix to indicate the token's type." Lines 162–167 are the six prefix rows; line 160 holds the stateless `ghs_APPID_JWT` rollout and "installation tokens being exactly 40 characters long".
- **Row change (old → new):** new row, status `queued` (freeze `9e4f0d68`) → `mined` (integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`.

### S137 — The GitHub Blog, Behind GitHub's new authentication token formats (admitted, used by the instrument)

- **URL:** https://github.blog/engineering/platform-security/behind-githubs-new-authentication-token-formats/, HTTP 200.
- **Accessed:** 2026-11-07 (capture 09:00:04Z).
- **Capture:** `corpus/source-snapshots/round-92/S137.txt`, sha256 `e4aaf2280203278c954124d8a62ac646c8ce2b3a96348ae3e90cbe173e26640d`; manifest anchors 156, 167, 173, `source-recheck.py` rc 0; candidate scan hits 0.
- **Located quote, S137.txt:167 (12 words):** "A 32 bit checksum in the last 6 digits of each token". Line 173 gives the 30-character base62 random part, line 174 "all without changing the token length" (40, the old hex length at line 171), lines 157–161 the five three-letter prefixes.
- **Row change (old → new):** new row, kind `docs` (the freeze draft said `blog`, which the census refuses: M92-1), status `queued` (freeze) → `mined` (integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`.

### Rejected this round

- **S138 — W3C Web Performance WG, HTTP Archive (HAR) format draft**, https://w3c.github.io/web-performance/specs/HAR/Overview.html, HTTP 200 on 2026-11-07 (capture 09:07:41Z), committed this time (`corpus/source-snapshots/round-92/S138.txt`, sha256 `88211ff4f5980591315a6a22e7ae659f1ab1e5a02021f818c18df51cfee80743`) so the rejected row's anchors resolve at closure (r91 closure routed defect 5). Located quote, S138.txt:30-31 (17 words): "This document was never published by the W3C Web Performance Working Group and has been abandoned." Line 29 reads `*DO NOT USE*`. Kept as a `rejected` row: an abandoned draft cannot ground the HAR cookie-object shape (r91 lead C). Flip: an active, maintained specification of the HAR cookie object is opened, or a committed capture of the lane's own carries the form.

### considerthese and assimilation

- **considerthese:** no new proposal mined this round. The latest file (`considerthese/2026-10-26.md`) has no unimplemented item left that C1 or C2 serves; C2 extends the capture-hygiene line (intake gate, round 90) by a source-grounded shape.
- **Assimilation: none.** Registry ids 138 (after S136–S138), staged 94, collisions 94/94 (`.ufo/waves/round-92/assimilation/collisions`; the staged file predates S031–S138). Quarantine slice re-derived: 7 rows (`assimilation/quarantine-slice`), not hand-checked this round; nothing appended from the package.

## Mistakes

**M92-1 — class `registry-enum-drift` (this round, pre-freeze).**

- **What happened:** the S137 row was first written with kind `blog`, a value the CORPUS.md kind enum (`spec · docs · paper · code · tool · dataset · talk · book · community · own-work`) does not hold.
- **Captured-by:** the census gate run before the freeze commit (`sources-census.sh validate`, E05).
- **Fix:** kind `docs` (a first-party engineering account of the token format); the change-log line says `docs`.
- **Shown able to fail:** `.ufo/waves/round-92/l1/m92-1-kind-enum.txt` — a scratch copy of the registry with the draft row prints `E05 S137 kind=blog`; the committed registry reads `kasegi ok`.

**M92-2 — class `reanchor-scope-narrower-than-the-citing-set` (found this round; origin round 88).**

- **What happened:** two block quotes in `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md` (lines 67, 75) pointed at `capture-secret-scan.py:18-19` and `:37-38`, bytes that stopped holding those quotes when the round-88 landing grew the docstring. Round 91 added R143 and re-anchored, but ran its tool over the two entries it knew it had shifted, not over every entry that cites the instrument; the presigned entry was never in the set.
- **Captured-by:** none until this round's R143 pass, which first enumerated the citing set (`grep -rnoE 'capture-secret-scan\.py:[0-9]'` over `corpus/knowledge`: four entries, not two).
- **Fix:** both quotes re-anchored to `:20-21` and `:110-111`; the round-92 R143 pass ran over all four citing entries. Rule (QUALITY R144): an R143 re-anchor runs over the full set of entries that cite the instrument by line, enumerated by a committed grep, never a remembered list.
- **Shown able to fail:** `.ufo/waves/round-92/l1/quote-anchor-r92.txt` — the four entries at the round-92 base read `bad=2` (presigned 67, 75) against the base instrument; after the integration they read `bad=0`.

**M92-3 — class `diff-mapped-anchor-too-wide` (this round, integration).**

- **What happened:** the difflib line map maps a replaced block start→start and end→end, so a citation of the round-91 named-limits block (`:81-87`, `:81`, `:81-83`) became `:81-102`, `:81-96`, `:81-98`: ranges that now also cover the new `github-token` docstring. The quote checker passed them (a quote found anywhere inside a wide range is `ok`). The same tool attributed the bare continuation token `:196-197` (an S134 line pair after an S134 citation) to the scanner because a scanner citation sat between them on the line.
- **Captured-by:** none mechanical; the L1 read every CHANGE line of `.ufo/waves/round-92/l1/reanchor-r92.txt` against the landed bytes.
- **Fix:** the known-limit citations narrowed by hand to `:95-102` (`:96-102` where the sentence says "round-91 text"), `:96` and `:96-98`; `cloud-signed-cookies-and-user-bound-sas.md:49` restored to `:196-197`. The non-author seat ReviewC2Scanner's independent list (`.ufo/waves/round-92/w1/ReviewC2Scanner-receipts/reanchor-r92.tsv`) caught two of the L1's hand ranges as still one line off; both were taken. Routed: the re-anchor tool should refuse (not widen) a citation whose range meets a replaced block, and bare continuation tokens should bind to the nearest preceding full path, not to the instrument.
- **Shown able to fail:** `reanchor-r92.txt` holds the widened CHANGE lines (`capture-intake-gate.md:109 … :81-96`, `cloud-signed-cookies-and-user-bound-sas.md:49 :196-197 -> :218-219`); the checker run right after the tool's `--apply` (before any hand narrowing) printed only the two presigned BAD lines, so it accepted every widened range: the checker alone cannot catch the class.

## Routed-defect disposition (r91 spot-check §6)

| # | r91 routed defect | r92 disposition |
|---|---|---|
| 1 | Row 454's second token `SKILL.md:494-506`; D2/D3 rows 367/369/370 and SKILL.md token drift | 367/369/370 done in C1 (label-named). 454's second token has no non-author label yet: wave item ReviewC1Labels labels it for round 93. |
| 2 | M10 granularity (sites, not (site, key) pairs) | Done: the round-92 map carries the key and M10 compares pairs; controls `wrong-key-column-86`, `excluded-437-applied`, `no-edit-qualified` fail on it. |
| 3 | C2 K8 gaps FC1–FC4 | Not this round: C2 P3 binds the change to the `github-token` shape; the round-92 K8 maps all 16 new statement clauses. Routed to round 93. |
| 4 | SentinelCookie F1–F3 bypasses | Not this round (cookie shape untouched); routed to round 93. |
| 5 | S135 capture in scratch only | Done for this round's reject: S138 is committed with its anchors. |
| 6 | Carried r90 capture-source.py items (M90-2, C2-F4, C2-F1..F3) | Still routed (separate surface). |
| 7 | Assimilation quarantine slice (7 rows) | Carried, not hand-checked. |
| 8 | Fleet-root `f.txt`, `trail-ids.txt` | Not kasegi's; untouched. |

## Wave findings (none re-scores a claim)

- **CriticClaims:** C1 STANDS and C2 STANDS on P1–P3 (C1 frozen command and `--measure-rev` path; C2 at seeds 9191, 1, 271828, 314159). Freeze ordering verified (freeze 06:09:08 precedes both landings; all control receipts are freeze blobs; EXCLUDED is in the freeze bytes and the excluded-437 control could only print `unlabelled=437` with it). C1 forgery variants: an unlabelled in-scope edit fails M3; an out-of-scope edit (`SKILL.md`) passes the meter and is caught only by P3 (scope division, recorded). EXCLUDED is conservative: applying 437 and 438 would read 961/1943, above the claim. Counter gap (low): M3 walks `corpus/knowledge/*.md` only while M9/M10 accept any labelled file. C2 D-1: single-token `_` boundary mutants pass the counter unpinned.
- **ExecC1Indep:** AGREE. Frozen meter in a clean shared clone reproduces every landing line; do-nothing fails M1/M3; the controls script reproduces all 11 verdicts byte-identically (commit ids masked); an independent byte check (no counter import) confirms the 25 edits equal the labels, the 5 unmapped labelled lines are unchanged and no other `corpus/knowledge` line moved.
- **ReviewC1Sites:** on the 25 landed rows 16 CORRECT, 7 UNCLEAR (partial support: 86, 87, 59, 150, 152, 153, 177), 2 WRONG (58, 144: the drop leaves `MATCHES: SKILL.md:117`, a provenance line; the attempts rule is at `SKILL.md:191`, and `MAX_ATTEMPTS` occurs nowhere in SKILL.md). EXCLUDED 437/438 AGREE (438's Supersedes target was `mission-control.md:52` historically, not 37-38); no-edit 3/3 AGREE. Systemic: the five `SKILL.md:N` ties in mapped rows are stale (lane-root refs the meter never classifies). Routed to round 93.
- **CriticHarm:** NO HARM on depth:density (SKILL.md byte-identical, 273.2), false positives (K3 `scanned=1882 hits=0`; `--files` over 218 snapshot and knowledge files: 0 `github-token` hits), ReDoS (linear, worst 113.5 ms/MB cold), old capabilities (round-91 counter unpinned K1–K8 pass at the landing; intake gate G1–G6 pass) and C1 class movement (0 resolved citations lost; 13 INTERNAL entered, 16 GONE-only left). Routed: F1 = ReviewC1Sites' 58/144; F2 six partial `MATCHES` cells should carry a `Partial:` marker.
- **ReviewC1Labels:** six non-author round-93 labels (`ReviewC1Labels-receipts/round93-labels.tsv`, `VERIFY PASS checks=55 failures=0`): 437 and 438 as full cell repairs that keep the errata quote true at a correct anchor, 454's second token `SKILL.md:494-506` → `SKILL.md:827-848`, and the 3 no-edit pairs reconfirmed. The GONE bare-key census at the landing finds exactly 5 sites left (the 2 errata and 3 no-edit). New kinds the round-92 meter cannot express (`cell-repair`, lane-root `SKILL.md` range) are named for the successor.
- **ReviewC2Scanner:** landed shape matches S136/S137 on prefixes, 36-character tail and stateless form; the 20-digit app-id cap and the JSON `\n` exception are lane choices (no source). R143: 75 instrument citations in three entries moved and four quotes broke at the landing (two more stale since round 88); its `reanchor-r92.tsv` (75 rows) was cross-checked against the L1's applied re-anchor: 72 equal, 3 differ, and two of those were taken from the seat (`capture-intake-gate.md:107` → `:96-102`, `cloud-signed-cookies-and-user-bound-sas.md:283` → `:96-98`).
- **MutC2Scanner:** 16 single-token mutants beyond the 10 forgeries: 6 killed (K1/K4/K7/K8 and the instrument selftest), 10 survive the counter unpinned (right/left boundary without `_`, app-id `{0,20}`/letters/`{1,15}`, JWT any separator/two segments, tail with `-`, left boundary without digits, …). Each survivor is rejected by the sha256 pin only.
- **MutC2Counter:** seven forged instruments pass K1–K8 unpinned at all three seeds, among them a harness-gated detector (active only under the counter's own tempdir names) and a path-keyed lookup table with no detection logic; K6 is blind to a removed shape. The pins are the sole guard against them; routed counter defects D1–D5 (randomise plant paths and tempdir names, plant U1–U6 bounds, make K6 require the new shape at the landing).
- **SentinelGitHub:** 69 one-fixture probes: 21 realistic encodings DETECTED (git remote userinfo, `Authorization: token`, `.netrc`, env dumps, YAML/JSON/HAR, curl, JSON `\n`/`\r\n`, BOM, CRLF, stateless form); P1 escape terminators whose last byte is a letter or digit (`\t`, `\r`, `\u0020`, `%20`, `%3A`, `%2F`, `\u0026`, `%26`) hide a token — a measured one-line boundary patch keeps the selftest green; P2 encoded `_` to be named a limit; P3 named limits confirmed; FP class: documentation example values of the published form are hits.
- **ScoutSources:** S136, S137, S138 re-fetched byte-identical; `source-recheck` rc 0; S138 rejection AGREE clause by clause (upstream commit `a702c2a9` "HAR is history" added the banner; no maintained successor exists, flip unmet). Round-93 leads: fine-grained `github_pat_` format in GitHub's REST API description (22 + `_` + 59 base62; the intake gate refuses that file without allowlist rows); GitLab `glpat-` + 20 characters (secret-detection docs, L86-87). The landed shape now hits GitHub's own documentation example tokens, so a capture of GitHub REST docs needs digest-bound allowlist rows.
- **ConnectorOverlap:** sibling scanners detect GitHub tokens unevenly (kagi substring match on six prefixes; kengaku `{36,}` plus fine-grained; chousa `ghp_` and `github_pat_`; tabi `ghp_` only); none detects the stateless form. Within kasegi, `capture-source.py`'s intake gate imports `patterns()` and inherits `github-token`.
- **ScribeEntry:** candidate entry admitted as `corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md` (17 quotes, `quote-anchor-check.py` over the working tree `checked=17 bad=0 cites=81 out_of_range=0`; landed scanner `--files` hits 0). Its F1 (the stateless branch has no right boundary), F4 (the app-id cap is unsourced) and F5 (docstring says `<APPID>`, regex requires digits) are routed qualifiers; F2 (the `--rev` form of the quote check is vacuous on an uncommitted entry) is a method note.
- **MutC1Counter:** 29 single-point mutants of the frozen C1 counter run against the landing and all 11 control variants (pristine vector reproduced verbatim): 7 killed (kind-rule mutants fail M9 at the landing itself), 22 survive the scripted controls; 15 of those are killed by measured proposed controls (wrong `--map-sha256`, base/after target off by one, a qualify label whose key differs from its fix path, an out-of-range end anchor, a duplicated map row, a renamed scope file, an `old` that occurs twice, …: `MutC1Counter-receipts/proposed-controls.tsv`) and 7 are shown entailed or redundant. Routed: the round-93 counter freezes the 15 proposed controls with its other controls.
