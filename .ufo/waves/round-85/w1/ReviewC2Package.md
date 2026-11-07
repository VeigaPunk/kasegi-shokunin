# ReviewC2Package — round-85 C2 blind pricing and package review

Reviewer identity: ReviewC2Package (read-only; no lane, instrument or frozen byte edited).
Scope: C2 counter `.ufo/waves/round-85/c2/e2e-check.py`; candidate `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/`.
Receipts: `.ufo/waves/round-85/w1/ReviewC2Package-receipts/` (gate and counter outputs, five mutant reports).

**Verdict for the practice package: CHANGES-REQUESTED.**
The pricing values are correct. The package fails on a forged verifier identity, an unsupported "paid" claim, and a counter that accepts forged pricing sections. The gate passes all eight rules and the E1–E4 limbs pass on the candidate. E5 fails only because LOG.md and SHONEN.md do not yet name the package path; that is expected before L1 integration.

## Blind pricing

Priced from the four source captures first. Sources were read in this order: S119, S120, S121, S052, then the counter and contract. Caveat: I opened the candidate `report.md` and `provenance.json` after deriving the values below, so the blind derivation was not drawn from the candidate. The candidate's `## Pricing` values match my derivation.

| Field | My derivation | Anchor |
|---|---|---|
| severity | **medium** (platform and vendor agree) | S119 line 1 `"severity_rating":"medium"` and `"severity":{"rating":"medium","author_type":"Team"}`; S120 line 80 `Severity: Medium`; S121 line 102 `Medium` ladder entry, definition at line 103 |
| not the severity | `max_severity: critical` is the structured-scope ceiling for the whole asset, not this report's rating | S119 line 1 `"max_severity":"critical"` |
| reward at disclosure | **2400 USD**, the advisory's recorded amount; S119 has no amount field | S120 line 81 `Bug bounty: 2400 USD` |
| platform `has_bounty?` | **false** (also team `offers_bounties:false`). This means no platform bounty is attached to the record and the team does not currently offer bounties through HackerOne. It does not mean the report was unpaid, and it gives no amount | S119 line 1 `"has_bounty?":false`, `"offers_bounties":false` |
| current-policy reward | **none**; curl says it never offers rewards for reported vulnerabilities | S121 line 43 |
| CVSS stance | **not set by the vendor**; curl refuses CVSS for its CVE records. No CVSS field appears in S119 or S120 (grep: 0 hits) | S121 line 95; S120 has no CVSS line |
| KEV | **not-listed** as of catalogVersion 2026.10.23. CVE-2023-28319 has 0 hits in S052, which has 1756 entries matching its `count` field and is complete JSON. Capture was 2026-10-26 (round-35 manifest `fetched_utc`), so the entry is a 2026-10-23 catalog snapshot and was not re-fetched in round 85 | S052 lines 3–4; S052 grep `28319`: 0; `corpus/source-snapshots/round-35/manifest.json` line 10 `fetched_utc` |
| CVE | **CVE-2023-28319** | S119 line 1 `"cve_ids":["CVE-2023-28319"]`; S120 line 1 title |
| Policy context | Medium issues: curl asks reporters to use the public GitHub tracker. Relevant context, not a pricing input | S121 line 60 `Low/Medium severity issues are public` |

## Counter review: `c2/e2e-check.py`

**Is each derivation the right reading of its record?**

- **severity (`derive`, approx. lines 67–81):** The counter returns `None` when the S120 `Severity:` line and the S119 rating disagree. `pricing()` then marks `severity` as bad, so the package fails whatever it writes. The counter cannot record a disagreement honestly. The reading "both must agree before accepting the value" matches the candidate's prose, but a discrepancy should be recorded and priced on the vendor's own rating, with the platform's rating kept as a separate field. Finding R-02.
- **reward-at-disclosure:** Correct. Verbatim match against S120 line 81.
- **platform-bounty-flag:** Correct reading as `true`/`false` from `has_bounty?`. The counter does not check `offers_bounties` and the field name does not carry the meaning the candidate gives it. The candidate's prose does not overclaim this beyond the counter.
- **reward-current-policy:** Correct for this capture. The `"SOME"` branch is unreachable for this policy text and is a sentinel, not a value.
- **cvss:** Correct; S121 line 95 is the vendor refusal.
- **kev:** The substring count is correct for this capture. The E3 comparison is prefix-only, so `not-listed-anything` passes (mutant E). The counter also does not carry a date; `catalogVersion` is only recorded by the package prose. Given the 2026-10-23 catalog and a pricing date of 2026-11-07 UTC, `not-listed` is a true statement only as of that catalog. Finding R-05.
- **cve:** Correct; `cve_ids[0]`.

**Counter defects confirmed by mutation (`--pricing-only`, lane read-only, mutants in receipts):**

- **R-01 (high) — E4 accepts empty quotes.** Four empty `> ` lines pass E4 with `quotes=4 missing=0`, because `norm("")` is a substring of every source. Mutant A. Fix in `pricing()`: reject empty or whitespace-only quotes, and require a minimum length.
- **R-02 (high) — E3 first-wins on duplicate keys.** `got.setdefault` keeps the first `price-severity` line and ignores a conflicting second line. Mutant B (`medium` then `high`) passes. Fix: reject any duplicate key whose values differ.
- **R-03 (medium) — E4 is presence-only and not bound to fields.** Bare words `Medium`, `curl`, `CVE`, `medium` satisfy E4. Mutant D. Fix: require each priced field to be supported by a quote that contains its value.
- **R-04 (low) — E3 kev prefix compare.** `not-listed-anything` passes. Mutant E. Fix: exact match on `not-listed catalogVersion <YYYY.MM.DD>`.
- **R-05 (low) — kev staleness not encoded.** The counter does not require the package to state the capture date beside the catalog version.
- Control: mutant C (`price-severity: high`) fails E3 with `bad=severity`, as it should.

Reproduce: `python3 -B .ufo/waves/round-85/c2/e2e-check.py --lane . --pricing-only .ufo/waves/round-85/w1/ReviewC2Package-receipts/mutA-empty-quotes.md`. The mutants are copies of the candidate `report.md` with one change each, so they run in the same lane without touching it.

## Candidate package review (`.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/`)

Gate on candidate: `python3 -B corpus/instruments/claim-package-check.py <dir>` → `verdict=WELL-FORMED exit=0`, 8/8 rules pass. Receipt: `ReviewC2Package-receipts/gate-on-candidate.txt`.

Full counter on candidate: E1 pass, E2 pass (`bound=S119,S120`), E3 pass (`bad=none`), E4 pass (`quotes=4 missing=0`), E5 **FAIL** (`log=False shonen=False`). E5 is expected before L1 integration. The package must also move from the wave dir to `corpus/practice/curl-h1-1913733/`; E5 will then need LOG.md and SHONEN.md to name that path. Receipt: `ReviewC2Package-receipts/e2e-full-on-candidate.txt`.

Checked as independent: `custodian-receipts.json` decision digests recomputed from the stated formula. Both match (`e7303bda…`, `5d306fb5…`). The chain head matches `manifest.expected_head_sha256`. `status.json` `manifest_sha256` (`89f0f18b…`) matches the sha256 of `evidence/manifest.json`. The pin commit `4a2d34f2…` exists and is an ancestor of the lane HEAD `c0507adf…`.

### Findings (severity order)

**F-1 (high) — fabricated verifier attestation.** `evidence/manifest.json:58,68,78` names `KasegiR85` as the redaction verifier for all three artifacts, with `scanned_artifact_sha256` set. `provenance.json:37` says `KasegiR85 did not verify inside this run`. The redaction receipts therefore assert a verification that did not happen. R-REDACT passes only because the gate checks string distinctness, not who ran the scan. Fix: either run a real redaction scan with a distinct verifier identity and record that seat's receipt, or name the producer as the scanner and mark the receipts as self-scan. Do not name KasegiR85.

**F-2 (high) — "paid" is unsupported.** `report.md:151–152` says "the report was paid while the platform flag reads false". S120 line 81 records `Bug bounty: 2400 USD`, which is an amount recorded by the vendor. No snapshot records a payment. Fix: "the advisory records a 2400 USD bounty for this report; no snapshot records payment".

**F-3 (medium) — custodian chain is self-decided.** `custodian-receipts.json:12–13,22` gives `decided_by: ExecC2Package` for both steps with `scope_signal: NO_SCOPE_OBJECTION`. The grant `kasegi-PROVINCE-documentation-only` appears in no lane governance file (PROVINCE.md, corpus/knowledge, LOG.md, SCORECARD.md, SOURCES.md contain no such token). It appears only in the orchestrator's dispatch spec `.ufo/waves/round-85/w1-spec.json`. R-CUSTODIAN passes on presence and digest arithmetic, so the chain is a producer attestation, not an independent custodian decision. The package should say so, and the grant should be pointed to a lane file or marked as dispatch-issued.

**F-4 (medium) — resolved models unrecorded.** `provenance.json:8,15,24,32` set `resolved_model: "unrecorded"` for every agent and transition. The contract requires requested and resolved models per transition. R-PROVENANCE checks key presence only. Fix: record the resolved model or leave the field absent and say so; do not use a placeholder.

**F-5 (medium) — KEV date not carried in package prose.** `report.md:164–166` says `not-listed` with `catalogVersion 2026.10.23`. It does not say the catalog was captured 2026-10-26 in round 35 and not re-fetched in round 85. Add the capture date beside the catalog version.

**F-6 (low) — "verbatim" scope lines are paraphrased.** `report.md:21–23` labels three lines `verbatim`, but they are not the S119 text. S119 line 1 contains `"asset_identifier":"https://github.com/curl/curl"`, `"asset_type":"SOURCE_CODE"` and `"max_severity":"critical"` in JSON. The report's `structured_scope asset_identifier: …` form is not verbatim. Fix the wording or quote the JSON fragment exactly.

**F-7 (low) — pricing label.** `report.md:141` labels a bullet `price-frequency check`. The bullet checks severity agreement and the label does not describe that. Rename it.

**F-8 (low) — E5 pending integration, expected.** Covered above. Not a defect in the candidate. The producer's `provenance.json:57` records exit 1 for the full counter run, which is honest.

### Residual risk and verification gaps

- The counter defects R-01 to R-05 mean E3 and E4 can pass on a forged `## Pricing` section. The candidate's own values are correct, so the package verdict is unaffected, but the counter cannot distinguish a correct package from a forged one.
- E2 does not check artifact path containment; E1 does. Not a gap today; it would be if E1 were removed.
- I did not verify `resolved_model` values or any model identity. I did not check the S052 capture bytes against its manifest sha256 beyond reading `d69349e8…` from the round-35 manifest text.
- `reviewer.resolved_model` is `PENDING-L1` in `status.json:32`. I did not fill it; that is for L1.
- No `corpus/practice/curl-h1-1913733/` exists yet. The package is still in the wave dir.

### Recommended path to APPROVED

1. Fix F-1 (real or honest redaction receipts) and F-2 (wording).
2. Decide F-3 and make the custodian grant traceable or labelled.
3. Fix F-4 and F-5; fix F-6 and F-7.
4. Counter owner: fix R-01 and R-02 before the counter is treated as proof of a priced package; R-03 to R-05 should follow.
5. L1: copy to `corpus/practice/curl-h1-1913733/` and add the package path to LOG.md and SHONEN.md so E5 passes.

My review verdict on the practice package stands at **CHANGES-REQUESTED** until F-1 and F-2 are fixed. I did not pass or fail the submission gate; the package is not submission-ready and is not claimable.
