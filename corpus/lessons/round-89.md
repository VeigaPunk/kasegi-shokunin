# Round 89 — lesson (kasegi, attempt 1)

Read first: the r88 closure (`admitted`) and `corpus/lessons/round-88-verifier-spotcheck.md` (both claims VERIFIED; routed defects 1–8), `corpus/lessons/round-88.md` (M88-1, M88-2) and the r86/r87 rejected closures. Base `090a46f89932324787e00ca20b1007f893934c9a`, freeze `94573d2573dc6cca83454cc65b787d37d96988f5`, C1 landing `eb5f0df8eaceca617465e493c710e8626e9aa618`, C2 landing `c61c55868e6d28653f57413bac6a6de5a398d11f` (`.ufo/waves/round-89/landing.json`). Frozen claims, predicates, kill rules and executed controls: `.ufo/waves/round-89/claims.json`, `.ufo/waves/round-89/controls/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; internal-citation repoint, score not claimed to move).** Knowledge-scope tranche 4: the 9 bare sibling-entry citations in `corpus/knowledge/triage-thresholds.md` for which the round-88 non-author seat ReviewC1Semantics named a supported target — 5 re-anchors of the r88 WRONG keys and 4 prefix repoints of proxy false negatives. Map `.ufo/waves/round-89/c1/repair-map.json`, labels `.ufo/waves/round-89/c1/labels.tsv` (each pair bound to its review line). Meter 777/1798 → exactly 785/1797. The counter replaces the r88 lexical proxy M8 with M9 (label binding) and reads the after-scope from a commit (r88 CriticClaims D1).
- **C2 — coverage, capability extension of `capture-secret-scan` (sourced: S128, S130).** New edge class `cloudfront-signed-url-signature` (Amazon CloudFront signed URLs, canned and custom policy) and the r88 F1 fix (Azure SAS matches after a `\u0026` or `%26` separator in any parameter position). Frozen counter `.ufo/waves/round-89/c2/capability-check.py` K1–K8: K7 draws signature values at run time from a printed seed (r88 CriticClaims D4) and K8 maps every statement clause to a planted case (M88-2).

## Outcome

- **C1:** P1 (`KNOWLEDGE-METER-RESULT pass rc=0`, 777/1798 → 785/1797, M1–M7, M9), P2 (15/15 pins) and P3 (`LANDING-SCOPE from=94573d25 to=eb5f0df8 changed=1 outside=0 verdict=PASS`) hold at `eb5f0df8` (`.ufo/waves/round-89/l1/c1-landing-r89.txt`). CriticClaims re-ran P1–P3: VERIFIED. ExecC1Indep re-derived every number without the counter: AGREE 10/10. ReviewC1Labels labels all 9 pairs CORRECT at the landing. R140 is scoped out, not passed: its keys were selected by a non-author, 9/9 are labelled (a census, not a sample), and `r140-check.py` cannot parse the four-column labels (CriticClaims C1-F2). Qualifiers: M1 does not assert the base reading (C1-F1); one composite token `claim-package-contract.md:9-16, 28-38` (`triage-thresholds.md:457`) stays bare because neither `apply-map.py` nor `resolve.py` treats it as one citation (ReviewC1Labels F1).
- **C2:** P1 (`CAPABILITY-CHECK-RESULT pass rc=0`, K1–K8, seeds 1822445695 at landing, 8989 and 1 by CriticClaims), P2 (scanner `95f24a54…`, allowlist `76245bba…` and SCORECARD row byte-equal) and P3 (`changed=3 outside=0 verdict=PASS`) hold at `c61c5586` (`.ufo/waves/round-89/l1/c2-landing-r89.txt`); CriticClaims: VERIFIED, and coverage, not quality (C2-F7). Qualifier (M89-2): the frozen `clauses` field says K8 maps "every statement clause"; three statement details are unbound — the `%26` start (mutant `no26` passes K1–K8), the 20-parameter window (`{0,1}` passes) and the 40/8–32 widths (`{13,}`, `{8,64}`, `{1,32}` pass) — CriticClaims C2-F1…F4, CriticHarm F2. The landed scanner does what the statement says on each (probes: `%26` start hits, 20 between hits / 21 misses, 39/40 and 7/8/32/33 at the stated bounds).
- **Harm found and repaired in the integration commit:** the C2 landing moved the scanner's lines and closed two of its named limits, so `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` contradicted the instrument (4 false statements, 29 of 43 line references stale; CriticHarm F1, ReviewC2Scanner F1). The ScribeEntry candidate (CriticHarm checked its 30 instrument citations against master) replaces the entry and adds Claim 7 (CloudFront, S128/S130); `presigned-url-credentials-in-captured-evidence.md:69` is repointed (`57-62` → `77-82`, `line 57` → `line 77`). S128/S130 flip to `mined`.

## Gate

### S128 — Amazon CloudFront Developer Guide, Create a signed URL using a canned policy (admitted, used by the instrument)

- **URL:** https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html, HTTP 200.
- **Accessed:** 2026-11-07 (capture 05:14:06Z; normalized sha256 equal to ScoutSources' round-88 lead capture `cd246e7d…`).
- **Capture:** `corpus/source-snapshots/round-89/S128.txt`, sha256 `cd246e7debb4ea67cccf783ac6b16307b1d0febbda9de133df29a5ada5ea3331`; manifest `corpus/source-snapshots/round-89/manifest.json`, `source-recheck.py` rc 0.
- **Located quote, S128.txt:72 (14 words):** "A hashed, signed, and base64-encoded version of the JSON policy statement. For more". Also :70 "&Signature=hashed and signed version of the policy", :77 the Key-Pair-Id example `K2JCJMDEHXQW5F`, :202-211 the `+`→`-`, `=`→`_`, `/`→`~` replacement table, :13 the example signed URL (Expires, Signature, Key-Pair-Id, Hash-Algorithm).
- **Row change (old → new):** new row, status `queued` (freeze `94573d25`) → `mined` (integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`.

### S130 — Amazon CloudFront Developer Guide, Create a signed URL using a custom policy (admitted, used by the instrument)

- **URL:** https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-custom-policy.html, HTTP 200.
- **Accessed:** 2026-11-07 (capture 05:14:09Z; normalized sha256 equal to the round-88 lead capture `dcdaa123…`).
- **Capture:** `corpus/source-snapshots/round-89/S130.txt`, sha256 `dcdaa1233df06b7304bc29c8af89371d81e7b0fa816251532ef9c52c8356ca39`.
- **Located quote, S130.txt:163 (17 words):** "anyone with the signed URL can access all of the files in any distribution that is associated". Also :66 "Policy=base64 encoded version of", :75-84 the Signature and Key-Pair-Id parameters, :14 the example custom-policy signed URL.
- **Row change (old → new):** new row, status `queued` → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py`.

### Rejected this round

- **S129 — Google Cloud Storage, V2 signing process (legacy)**, https://docs.cloud.google.com/storage/docs/access-control/signed-urls-v2, HTTP 200 on 2026-11-07, captured to scratch only (262 lines, sha256 `517f22a3…`). Kept as a `rejected` registry row: the page names `Signature` and `GoogleAccessId` as values a program supplies (scratch lines 155-160) but shows no query-string form or example URL, so the parameter shape a scanner needs cannot be located in it; it marks itself legacy (line 105). Flip: a first-party capture that shows a V2 signed URL's query parameters as text.
- **Both captures hold AWS's own example signature** (S128:13, S130:14; the value contains `EXAMPLE`, Key-Pair-Id `K2JCJMDEHXQW5F` is the documented example). The candidate scanner hits both; two digest-bound allowlist rows were added before the freeze and the scan receipt is `.ufo/waves/round-89/controls/capture-scan-r89.txt` (QUALITY R138).

### considerthese and assimilation

- **considerthese:** the intake gate in `capture-source.py` (`considerthese/2026-10-24.md:49-52`, routed by the r88 spot-check for the third time, defect 5) is **declined this round, explicitly**: C2 already changes the `capture-secret-scan` capability on the coverage axis and an intake gate would be a second change to the same capture path in the same round; R138's manual scan-before-commit was run (`controls/capture-scan-r89.txt`). Flip: a round with no `capture-secret-scan` claim takes it.
- **Assimilation: none.** Lane 127 registry ids at the check (taken before this round's S128–S130 rows), staged 94, collisions 94/94 (`.ufo/waves/round-89/assimilation/collisions`; the staged file predates the lane's S031–S130 expansion). Guard proof on an indented `  | S002 |` row: 0–3-space pattern finds S002, column-zero pattern finds none, `PASS` (`.ufo/waves/round-89/assimilation/guard-proof.txt`). Quarantine slice re-derived: 7 rows (`quarantine-slice`), not hand-checked this round. Open L0 `kasegi | round-77` unchanged.

## Mistakes

**M89-1 — class `plant-outside-instrument-scope`.**

- **What happened:** the first draft of the C2 counter's K7 (generated values) planted its first positive at `g/source-snapshots/G1.txt`. The scanner's `--rev` mode scans only capture-class paths (`is_capture_path`: `corpus/source-snapshots/`, practice evidence, `*-receipts/` dirs, `live-*` files), so that plant could never be hit: the positive control failed K7 at both seeds (`.ufo/waves/round-89/controls/c2-controls-r89-first-run.txt`), and every negative control carried the same spurious miss, which would have made each of them "fail for the right reason" by accident.
- **Captured-by:** the executed positive control (claim-sizing rule: build and run the controls before freezing). Nothing structural would have caught it had the positive control been skipped.
- **Fix:** QUALITY R141 — every planted case a capability counter expects the instrument to hit lies inside the instrument's own scope; check `.ufo/waves/round-89/l1/r141-check.py --counter <counter> --scanner <scanner>`. The plant moved to `g/x-receipts/live-g1.txt` before the freeze; the controls were re-run (`controls/c2-controls-r89.txt`).
- **Shown able to fail:** `.ufo/waves/round-89/l1/r141-check-r89.txt` — the frozen counter prints `expected=19 out_of_scope=0 verdict=PASS`; the first-run counter (reconstructed by reverting the plant path) prints `R141 OUT g/source-snapshots/G1.txt … verdict=FAIL exit=1`.

**M89-2 — class `hand-listed-clause-map-claimed-complete` (recurrence of M88-2 in weaker form).**

- **What happened:** to close M88-2 the C2 counter gained K8, a hand-authored `CLAUSES` list (10 entries), and the frozen `claims.json` field says K8 "maps every statement clause to a plant". Three details of the statement have no entry and no plant: the `%26` start boundary, the "up to 20 other parameters between" window, and the 40-character / 8–32 width bounds. Executed mutants that drop or widen each pass K1–K8 (`.ufo/waves/round-89/w1/CriticClaims.md` C2-F1…F4, `CriticHarm.md` F2, `MutC2Scanner.md` rows 2, 5, 14). The landed scanner implements each detail as stated; only the counter cannot see a regression.
- **Captured-by:** none before the freeze — the clause list was written by the pattern's author from the statement, and nothing compared the two texts. The attack seats caught it after landing.
- **Fix (routed, round 90):** derive the clause list from the frozen statement mechanically — every numeral, separator token and parameter name in the statement must appear in at least one `CLAUSES` entry with a positive and a boundary-negative plant (`%26` start; 20 hit / 21 miss; 39/40; 7/8 and 32/33). A counter whose clause list lacks a statement token fails its own selftest.
- **Shown able to fail:** not yet; the `no26`, `win1`, `floor13`, `kpi64` mutants in `.ufo/waves/round-89/w1/CriticClaims-receipts/` are the failing cases the round-90 counter must kill.

**M89-3 — class `control-input-read-from-moving-path`.**

- **What happened:** two of the frozen C2 controls (`r88`, `noallow`) take their instrument or allowlist from the lane working tree (`$L/corpus/instruments/…`), which the C2 landing then overwrote. Re-run after the landing, both controls build trees identical to the positive control and pass, the opposite of their recorded expectations (`.ufo/waves/round-89/w1/MutC2Counter.md` §S1). The recorded `controls/c2-controls-r89.txt` is sound because it ran before the landing; the script is not re-runnable.
- **Captured-by:** none; R139/R141 bound the landing diff and plant scope, not control inputs.
- **Fix (routed, round 90):** every control input is read from a pinned revision (`git show <base>:<path>`) or a frozen wave file, never from a lane path a landing can change; MutC2Counter's commit-bound rebuild restores `r88` K3/K4/K7/K8 FAIL and `noallow` K3 FAIL (receipt).
- **Shown able to fail:** MutC2Counter's post-landing re-run of the as-written script is the failing case.

## Routed-defect disposition (r88 spot-check §6)

| # | r88 routed defect | r89 disposition |
|---|---|---|
| 1 | F1/M88-2: `\u0026`/`%26` boundary, clause plant, generated-value limb | Done in C2: `_LB` lookbehind; K4 plant `E3.json` (S127:605 order, JSON-escaped); K7 generated values; K8 clause map. The fixture-literal control fails K7 only. |
| 2 | Counter binding (survivors, M8 isolation, commit-bound P1) | Partly: C1's P1 is commit-bound (`--after-rev`; the working-tree-only control fails M1–M3); M8 is retired, replaced by M9. The r88 MutC2Scanner survivors on the Azure window, name width and `sv` form are not re-planted (see wave findings). |
| 3 | SCORECARD command sha pins | Done: the round-89 `capture-secret-scan` command carries `--instrument-sha256` and `--gate-sha256`. |
| 4 | C1 tranche 4 under R140 | Done as C1 for the 9 keys a non-author named a supported target for; the map is reviewer-selected, not proxy-selected, so R140's sample floor does not apply (9/9 labelled). `mission-control.md:43-46` stays out (the row overstates its companion); the 39 unsampled drift exclusions stay out. |
| 5 | Intake gate in `capture-source.py` | Explicitly declined this round (above). |
| 6 | S127 anchor cell | Already recorded in the r88 lesson Gate (D8). |
| 7 | Seat scratch paths | Every seat prompt names `/fast/scratch/hyaku/kasegi-r89/<seat>`; leftovers are reported below. |
| 8 | Open L0 (expired STS token in history) | Unchanged, operator-owned. |

## Wave findings (none re-scores a claim)

One v1 wave, 14 seats (`.ufo/waves/round-89/w1-results.json`).

- **ReviewC1Labels:** 9/9 pairs CORRECT at `eb5f0df8`; labels bind 9/9. F1 composite token at `triage-thresholds.md:457` stays bare; F2 the `:35-36` label omits r88's "1/3" site fraction (outcome correct: only site 225 moved); F3/F4 stale rows 249, 155, 438. Tranche-5 input: all 39 unsampled r88 drift exclusions labelled (46 sites: 40 WRONG with a supporting range for 33 keys, 3 UNCLEAR, 2 CORRECT, 1 mention) at `ReviewC1Labels-receipts/tranche5-labels.tsv` — non-author labels for a round-90 map under R140.
- **ExecC1Indep:** independent meter AGREE on all 10 numbers (777/1798, 785/1797, token sets, line diff, M4/M5, M9, pins).
- **MutC1Counter:** 37 mutants; the frozen control set alone kills 11 (29.7 %); 14 extra plants kill 13 more; 13 survive as structural or redundant guards. Routed: plants for the surviving M9/M4 mutants.
- **CriticClaims:** C1 VERIFIED, C2 VERIFIED on P1–P3 re-run; C1-F1 (no base limb), C1-F2 (R140 scoped out, recorded above), C2-F1…F4 (M89-2), C2-F5 (S128/S130 status — flipped at integration).
- **CriticHarm:** NO HARM on C1, density (`SKILL.md` byte-identical, 273.2), instruments, deletions, pins and wave-dir hygiene; HARM F1 (knowledge entry contradicted the instrument) repaired in the integration commit; F2 = M89-2.
- **ReviewC2Scanner:** CHANGES-REQUESTED (round 90), no change to the frozen instrument needed: F1 = the entry drift (repaired); F2 `%26` unplanted (M89-2); F3 a `Key-Pair-Id` over 32 characters is a silent total miss, unlisted; F4 standard-base64 `+ / =`, HAR name/value arrays and percent-encoded values are unlisted misses; F5 S130 status (flipped). No false positive found; r88 F1 fixed without regression.
- **MutC2Scanner:** 61 mutants (47 on the round-89 additions, 14 r88 survivors re-run): 25 killed, 35 survived, 1 seed-dependent. Survivors name their killing plants (window, name class, floor 64, `%26` CloudFront start).
- **MutC2Counter:** 35 counter mutants, 20 survive the frozen control suite (11 drop a documented conjunct, 5 weaken K7 value derivation, 4 equivalent); S1 = M89-3.
- **SentinelRegex:** REFUTED (no super-linear growth): paired doubling ratios 1.97–2.04 from 1 to 8 MiB on every adversarial class; worst 1.52 s at 4 MiB (`cf-many-long`), 2.43 s at 8 MiB. Qualifier: the `\u0026` boundary makes `\u0026`-dense text 25–28× more expensive for the Azure shape, still linear and under 1 s at 4 MiB; routed (literal prefilter).
- **Seat scratch:** no `/fast/scratch/hyaku/kasegi-r89/<seat>` directory remained after the wave (`ls` shows only the L1's own `l1/`, removed after landing).
- **ExecC2Corpus:** four more first-party pages (signed cookies, code examples, aws-sdk-js-v3 signer README, private-content overview): 0 hits, none carries an example signed URL; 27 fixture cases as designed; FN-1 standard base64, FN-3 `%26` start-only. Sibling read-only sweep (kagi, kaidoku, kama): 0 CloudFront hits; 3 generic `credential` hits routed to their owners (L0 `kasegi | round-89`).
- **ScoutSources:** S128/S130 re-opened live, sha256 equal to the manifest and to the r88 lead receipt; 5/5 manifest quotes at their anchors; S129 rejection holds; round-90 leads opened (see `ScoutSources.md` §2).
- **ScribeEntry:** candidate entry (Claim 7 CloudFront, FC-8/FC-9 checks, instrument references repointed) — admitted by the L1 after CriticHarm's citation check.
- **ConnectorOverlap:** no sibling lane holds a CloudFront or Azure SAS detector; the new shape flags committed live CloudFront signed URLs in two sibling wave receipts (kengaku r95, kama r47) — routed to the operator (L0 `kasegi | round-89`), never edited here. 7+ reviewer-named correct ranges still unapplied at master (round-90 C1 input).
- **ReviewWindow:** CONFIRMED for Azure: the documented user-delegation SAS parameter `skdutid` (7 letters, Microsoft's create-user-delegation-sas page) is outside `_PARAM`'s `[A-Za-z]{2,6}`, so `sv=…&skdutid=…&sig=…` is missed; REFUTED for CloudFront (5/5 documented names in class). Window boundary measured: 20 between hit, 21 miss, both shapes. Routed: widen the Azure name class, sourced on that page.
