# Round 91 — lesson (kasegi, attempt 1)

Read first: the r90 closure (`admitted`) and `corpus/lessons/round-90-verifier-spotcheck.md` (both claims verified; routed defects 1–7), `corpus/lessons/round-90.md` (M90-1..3). Base `bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`, freeze `53ab692a7b544c35141e2b19f7413cbdb767c1ad`, C1 landing `8a1a00c639ba808a701d1f186aac9ebd0045deaa`, C2 landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70`, landing receipts `bcbfbde63b83c9336e845001323b5c92419e526a`. Frozen claims, predicates, kill rules and executed controls: `.ufo/waves/round-91/claims.json`, `.ufo/waves/round-91/controls/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; citation repair, score not claimed to move).** Tranche 6: the six round-91 labels the round-90 non-author seat ReviewC1Sites wrote (`.ufo/waves/round-90/w1/ReviewC1Sites-receipts/round91-labels.tsv` at `e993fd18`), applied as the edits the labels name to `corpus/knowledge/triage-thresholds.md`: sites 141, 142, 226, 368 drop a `MATCHES:` tie no range of the cited entry supports (the table's `—`), 454 is repointed to `corpus/knowledge/ev-model.md:13-25`, 457's composite token becomes `corpus/knowledge/claim-package-contract.md:9-16`. Counter successor adds M9 (each edit equals the label-named edit) and M10 (mapped sites = labelled sites; r90 closure routed defect 1). Pinned meter 890/1883 → exactly 891/1880.
- **C2 — coverage (score 8 held), capability extension of `capture-secret-scan` (sourced: S133, S134).** New shape `cloudfront-signed-cookie-signature` (CloudFront signed cookies were a documented known limit) and the Azure SAS name window widened from 2–6 to 2–7 letters so the user-delegation field `skdutid` no longer hides a SAS (ScoutSources r90 lead 1, ReviewWindow r89).

## Outcome

- **C1:** P1 `KNOWLEDGE-METER-RESULT pass rc=0` (M0 890/1883, M1 891/1880, M3, M4, M5, M6, M9 6/6, M10 6/6), P2 pins equal, P3 one path (`.ufo/waves/round-91/l1/c1-landing-r91.txt`).
- **C2:** P1 `CAPABILITY-CHECK-RESULT pass rc=0` at run-time seed 2890978206, 9191 and 1 (K1–K8), P2 landed sha256 `89e283c6…` = frozen candidate, P3 two paths (`.ufo/waves/round-91/l1/c2-landing-r91.txt`).

## Gate

### S133 — Microsoft Learn, Create a user delegation SAS (admitted, used by the instrument)

- **URL:** https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas, HTTP 200.
- **Accessed:** 2026-11-07 (capture 07:48:19Z).
- **Capture:** `corpus/source-snapshots/round-91/S133.txt`, sha256 `56d858ac8c2988fdf95a045b5a75f13cc5a28a1f71b3786638522775b1786cd6` (equal to the round-90 ScoutSources lead capture); manifest `corpus/source-snapshots/round-91/manifest.json`, `source-recheck.py` rc 0 (anchors 571, 567); scanned with the frozen candidate before the freeze, hits 0 (`.ufo/waves/round-91/controls/capture-scan-r91.txt`).
- **Located quote, S133.txt:571 (13 words):** "The sduoid and skdutid fields are supported with version 2025-07-05 and later." Line 177 holds the field token `skdutid` in the SAS field table; line 870 is the documented example SAS whose parameter order the K4 plant follows.
- **Row change (old → new):** new row, status `queued` (freeze `53ab692a`) → `mined` (integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`, `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md`.

### S134 — Amazon CloudFront Developer Guide, signed cookies with a custom policy (admitted, used by the instrument)

- **URL:** https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-custom-policy.html, HTTP 200.
- **Accessed:** 2026-11-07 (capture 07:48:20Z).
- **Capture:** `corpus/source-snapshots/round-91/S134.txt`, sha256 `ddf45b805c7f67f29cf15f60f805fd636968f14734f4e342c697760f8b49f1cc`; manifest anchors 97, 17 rc 0; scan hits 0.
- **Located quote, S134.txt:17 (10 words):** "and a CloudFront signed cookie requires three name-value pairs." Also :97 "A hashed, signed, and base64-encoded version of the JSON" (the signature cookie), :31 "case-sensitive." (cookie attribute names), :123 the documentation's 28-character example value (a negative plant).
- **Row change (old → new):** new row, status `queued` (freeze) → `mined` (integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`, `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md`.

### Rejected this round

- **S135 — Amazon CloudFront Developer Guide, signed cookies with a canned policy**, https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-canned-policy.html, HTTP 200 on 2026-11-07, captured to scratch only (sha256 `d6fccb868f4a8367da95912ee818d2a00807575ed23419c7b2395c5aaff3994c`). Located quote, scratch line 17 (6 words): "are: CloudFront-Expires, CloudFront-Signature, and". Kept as a `rejected` row: the signature cookie has S134's name and value form, so the page adds no detectable shape; `CloudFront-Expires` is a timestamp, not credential material. Flip: a round that binds the cookie shape to its companion pairs cites it as the canned-policy form.

### considerthese and assimilation

- **considerthese:** no new proposal mined this round. The latest file's open items were taken in rounds 87–90 (`2026-10-24.md:49-52` intake gate implemented in round 90); C2 extends the same capture-hygiene line by source-grounded shapes, not by a new proposal.
- **Assimilation: none.** Registry ids 135 (after S133–S135), staged 94, collisions 94/94 (`.ufo/waves/round-91/assimilation/collisions`; the staged file predates S031–S135). Quarantine slice re-derived: 7 rows (`assimilation/quarantine-slice`), not hand-checked this round; nothing appended from the package.

## Mistakes

**M91-1 — class `boundary-tuned-to-separator-not-to-container` (this round, pre-freeze).**

- **What happened:** the first candidate reused the CloudFront URL left boundary `_CF_LB` (not preceded by a letter, digit, `_` or `-`, or right after `\u0026`/`%26`) for the cookie shape. A JSON string that joins several `Set-Cookie` values with an escaped newline (`...; Path=/\nCloudFront-Signature=...`) puts the letter `n` right before the cookie name, so the candidate missed a real-length signature in practice evidence. Every K-limb but K4/K8 passed; the selftest passed because its cases had no JSON-joined form.
- **Captured-by:** the executed positive control (claim-sizing rule: run the controls before freezing) — `candidate-pinned` failed K4 and K8 on plant `corpus/practice/p/evidence/E4.json` in the first control run.
- **Fix:** a cookie-specific boundary `_CK_LB` that also admits the end of a JSON `\n` escape; selftest case `cf-cookie-json-joined`; forgery F8 (the first candidate's boundary) added to the frozen controls.
- **Shown able to fail:** `.ufo/waves/round-91/controls/c2-controls-r91.txt` control `F8-no-json-newline`: K4 `missing=corpus/practice/p/evidence/E4.json|cloudfront-signed-cookie-signature`, K8 fails the JSON-join clause, rc 1.

**M91-2 — class `meter-blind-edit` (this round, pre-freeze).**

- **What happened:** the partial control that skips site 457 reads 891/1880 like the candidate: resolve.py does not tokenise the composite `claim-package-contract.md:9-16, 28-38` as one GONE citation, so repairing it moves neither the numerator nor the denominator. A counter bound only on the meter (M1) would have passed a landing that skipped one of the six labelled edits.
- **Captured-by:** M3 (`bad_lines=1`) on the frozen map and M10 (`unapplied=457`) on the partial map (`controls/c1-controls-r91.txt`, controls `partial-5-of-6`, `partial-own-map`).
- **Fix:** none needed for this round's claim (M3 and M10 both bind the edit); routed rule: a citation-repair tranche states for each site whether the meter can see it, and a site the meter cannot see is bound by a line-diff or completeness limb, never by the meter alone.
- **Shown able to fail:** control `partial-5-of-6` (`controls/c1-controls-r91.txt`) fails on M3 alone (`LIMB M3 FAIL ... bad_lines=1`; M1 is not among the failing limbs): the meter reads 891/1880 for a landing that skipped site 457.

**M91-3 — class `instrument-landing-shifts-knowledge-anchors` (this round, found after landing).**

- **What happened:** the C2 landing inserted docstring lines and a pattern into `capture-secret-scan.py`, shifting its line layout (+6 to +35 lines). Two admitted knowledge entries cite the instrument by line: 97 citation tokens in `cloud-signed-url-credentials-in-captured-evidence.md` and `capture-intake-gate.md` now pointed at other bytes, four block quotes no longer appeared at their anchors, and several sentences still said CloudFront signed cookies were a named limit and that the Azure window spans 2–6-letter names. Every frozen limb passed: the counter binds the instrument, not the entries that describe it; resolve.py and `anchorcheck.py` are range-only, and a shifted citation is still in range.
- **Captured-by:** none before the landing; the non-author seat ReviewC2Scanner (F1, HIGH) after it. P3 bound the landing to the instrument and the row, so the repair could not ride the landing.
- **Fix (integration, in round):** `.ufo/waves/round-91/l1/reanchor-scanner-cites.py` maps every citation from base to landing bytes with a difflib line map (`l1/reanchor-r91.txt`, 97 tokens), the stale sentences were rewritten by hand, and `l1/quote-anchor-check.py` now reports `bad=0 out_of_range=0` over both entries and the admitted new entry. QUALITY R143.
- **Shown able to fail:** `.ufo/waves/round-91/l1/quote-anchor-r91.txt` — the two entries at base vs the base instrument: `bad=0`; the same entry bytes vs the C2 landing instrument: `bad=4` (capture-intake-gate.md:69, :71, :109, :111).

## Routed-defect disposition (r90 spot-check §6)

| # | r90 routed defect | r91 disposition |
|---|---|---|
| 1 | C1-F1 completeness limb | Done: M10 in the round-91 counter (mapped = labelled), shown able to fail by control `partial-own-map`. |
| 2 | C2 counter clauses unbound (C2-F1..F3: `line=`, whole bytes, `--kind text`, "imported") | Not this round: those are capture-source.py (intake gate) clauses; C2 changes the scanner and P3 binds its landing to the scanner. Routed to round 92. |
| 3 | C2-F4 missing explicit `--allow` loads as empty | Not this round (capture-source.py surface); routed to round 92. |
| 4 | C2-F6 / M90-2 `file://` status=None crash | Not this round (capture-source.py surface); routed to round 92. |
| 5 | Carried: M89-2/M89-3 counter successor; r140-check four columns; composite token 457; ReviewC1Sites round-91 labels | 457 and the round-91 labels done as C1; M89-2 boundary plants applied in the C2 counter (39/40 floor, 8-letter window, case, prefix, scope); r140-check routed. |
| 6 | Seat hygiene: `mktemp -d /tmp` in a seat preamble | Done in the wave context: "never mktemp under /tmp", scratch `$S` with trap in every item. |
| 7 | Sibling credential material (L0 `kasegi | round-89`) | Unchanged, operator-owned. |

## Wave findings (none re-scores a claim)

One v1 wave, 13 seats (`.ufo/waves/round-91/w1-dispatch.json`; results `w1-results.json`, 13/13 with output, 0 dead).

- **CriticClaims:** C1 VERIFIED, C2 VERIFIED (P1 at seeds 424242, 9191, 1; P2, P3). Routed: C1-F1 M10 compares site sets, so a seventh label row on an already-mapped site would pass (`CriticClaims-receipts/c1-m10-hole.txt`; the frozen labels have 6 rows); C2-F1 four statement clauses lack a K8 clause or plant — forgeries FC1 (no `\u0026`/`%26` cookie boundary), FC2 (any preceding letter), FC3 (`\n` join keyed to `Path=/`), FC4 (Azure `{1,7}`) pass every K limb unpinned. The landed instrument implements all four clauses (`c2-forgery-behaviour.txt`): the gap is in the counter. Q1: 891/1880 is the token arithmetic of the six edits (+1 from 454; −3 removed GONE tokens; 457 never counted), not four repaired citations.
- **ExecC1Indep:** AGREE on every number; own git-show checker pass; live lane and shared clone byte-identical.
- **ReviewC1Sites:** 141, 142, 226, 368, 457 CORRECT; 454 WRONG at row level — its edited token is correct, but the untouched second token `SKILL.md:494-506` is park/autopsy prose (the EV formula is at `SKILL.md:828-848`), pre-existing and invisible to M5/M9/M10. D2 (367, 369, 370) and D3 (SKILL.md token drift at 58, 144, 459) routed to round 92. The em dash is a by-usage convention the tie legend (`triage-thresholds.md:37-40`) does not define (Q1).
- **ReviewC1Labels:** 30 non-author round-92 labels (10 CORRECT, 10 repoint, 10 content-repair) over the 20 GONE bare keys naming an existing entry, `ReviewC1Labels-receipts/round92-labels.tsv`, verified 30/30; projected 891/1880 → 905/1877. The round-91 counter cannot express a CORRECT label's qualification edit (routed).
- **MutC1Counter:** 36 mutants; 14 killed by the frozen controls, 7 more by ten routed controls R1–R10, 12 equivalent with proofs, 3 detail-only. Frozen controls confound M10 with M6 and M9 with M6 (each forgery used its own map against the frozen sha); R1/R2 isolate them.
- **ReviewC2Scanner:** REQUEST-CHANGES. F1 = M91-3 (repaired). F2 no limb binds the knowledge anchors (R143 check now exists). F3 the cookie bullet does not cite its alphabet (S134 416-426) or case-sensitivity (S134 30-31) source lines. F4 quoted cookie values are neither detected nor listed. F5 `_CK_LB` accepts any backslash-n pair (false-positive side only). F6 "every round-89 shape behaves as before" is imprecise for Azure, which widens by design. `[A-Za-z]{2,7}` is exact for S133's 26 documented names.
- **MutC2Scanner:** 23 mutants, 13 killed, 7 survivors with plants (1-letter and digit names, quote-terminated values, `%26` cookie boundary, `+` in the cookie value, space before `=`, underscore name), 3 equivalent.
- **MutC2Counter:** 35 mutants, 32 survive: every forgery is rejected by the instrument's own selftest (K1) as well as K4/K7/K8, so no behavioural limb is a sole guard; K5 and K6 are unexercised by any control; capture scope has no control; K7 has no JSON `\n` case. The control script's comment that unpinned forgeries are judged only by K2–K8 is wrong (K1 selftest also rejects them).
- **CriticHarm:** NO HARM on density (273.2), false positives (1734 capture files and 113 snapshots: 0 hits), old capability commands (only the documented pin move at r89), ReDoS (worst 0.031 s on 1 MiB). The intake gate inherits both shapes (loopback refusal); the round-90 counter's G0 reads `shapes=12 missing=cloudfront-signed-cookie-signature` (derived list predates the shape). Q3: `html_to_text` drops tag attributes, so an `href`-only SAS is not in the gate's bytes (pre-existing, routed). Q4: `--files` allowlist keys are path strings; pass repo-relative paths.
- **SentinelCookie:** 67 probes: 29 detected, 21 out of scope (16 documented limits all missed, as stated), 17 bypasses; F1 colon-form object dumps (dict repr, `get_dict()`, `parse_qsl`, YAML), F2 Netscape cookie jar, F3 quoted value, F4 `\u003d`/`&#61;`, F5 non-letter Azure names, F6 `--rev` scope covers no round-91 wave report file (only `*-receipts/` and `live-*`). Routes R1–R7 to round 92.
- **ScoutSources:** S133/S134 live re-fetch byte-identical to the snapshots; recheck rc 0; S135 rejection AGREE clause by clause. Round-92 leads: A GitHub "About authentication to GitHub" (token prefixes, line 158; 8 bare-prefix fixtures all missed) OPEN; B Azure account SAS CLOSED (already detected; the 2–7 window covers every documented name); C HAR cookie object OPEN but tier-limited (the W3C draft marks itself abandoned).
- **ConnectorOverlap:** proposes one round-92 grounding tranche pairing the ReviewC1Labels set with the instrument-anchor class (R143) under a (site, key) M10.
- **ScribeEntry:** candidate admitted as `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md` after the L1's quote/anchor check (57 quotes, 228 citations, one anchor widened 91 → 91-92); FC-1 23 spans pass; no credential-shaped values.
