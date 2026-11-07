# ReviewC2Package — round-86 C2 package review

Reviewer identity: ReviewC2Package (read-only seat; no lane, instrument, or frozen byte edited).
Scope: candidate `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/` against S122/S123 (round-86) and S120/S121 (round-85 reuse), the frozen counter `.ufo/waves/round-86/c2/e2e-check.py` (sha256 `b4a97e09…a834`, matches `claims.json` instruments), the frozen gate `corpus/instruments/claim-package-check.py` (sha256 `8b6f8493…cce6`, matches), `claims.json`, `controls/c2-controls-r86.txt`, PROVINCE.md, QUALITY.md.
Receipts: `.ufo/waves/round-86/w1/ReviewC2Package-receipts/` — `f1-e1-e2-unsatisfiable.txt`, `gate-counter-on-candidate.txt`, `pricing-probes.txt`, `facts-anchors.txt`.
Poll: DONE appeared 2026-11-07T01:11:43Z (loop 3 of the 60 s poll), well inside the 45-minute window; the full candidate was reviewed, not only committed sources.

## Instruments re-run by this reviewer

- Gate on candidate: `rules=8 pass=7 fail=1 verdict=DEFECT exit=1`; the only failing rule is `R-NOSECRET detail=hits=1,first=evidence/S122.txt,shape=credential`. This matches the provenance command entry ("final run; expected fail R-NOSECRET only", exit 1) — honest.
- Counter `--pricing-only` on candidate `report.md`: `E0 pass, E3 pass (sections=1 dup=none bad=none), E4 pass (quotes=6 short=0 missing=0 s123=4), E2E-RESULT pass rc=0`.
- Counter full `--pkg`: `E0/E2/E3/E4 pass, E1 FAIL gate_rc=1, E5 FAIL (pre-integration path)`, rc 1.
- Bindings recomputed independently: `status.json.manifest_sha256` equals sha256 of `evidence/manifest.json` bytes (`9a130c1d…f367`); both custodian decision digests recompute from the stated formula, chain inputs link, `head_sha256 == manifest.expected_head_sha256`.
- Discrimination probes on candidate-derived copies (receipt `pricing-probes.txt`): forged payer (`curl`), forged cve, forged original-report (`1997312`), duplicate `price-payer` key, short quote — all five rc 1, each killed by the intended limb (`E3 bad=<field>` / `dup=payer` / `E4 short=1`).

## Blind pricing (derived from the captures before comparing machine lines; all nine agree)

| field | value | anchor |
|---|---|---|
| program | ibb | S122:1 `"handle":"ibb"`; profile `"name":"Internet Bug Bounty"` |
| payer | internet-bug-bounty (inference, see F-8) | S123:16 payer sentence + S122:1 `"has_bounty?":true` on the IBB record |
| severity | medium | S122:1 `"severity_rating":"medium"` = S120:80 `Severity: Medium` |
| reward-at-disclosure | 2400 USD | S120:81 `Bug bounty: 2400 USD` |
| platform-bounty-flag | true | S122:1 `"has_bounty?":true` |
| original-report | 1913733 | S122 vulnerability_information + S120:83 `Original report: …/1913733` |
| reward-current-policy | ended 2026-01-31 | S123:13 + S121:43 |
| kev | not-listed catalogVersion 2026.10.23 | S052: 0 hits for CVE-2023-28319; captured r35, not re-fetched (candidate says so) |
| cve | CVE-2023-28319 | S122:1 `cve_ids[0]` |

## Fact traceability

Every load-bearing sentence in `report.md` was located in a capture: verbatim JSON fragments (title, severity_rating, has_bounty?, cve_ids, handle, offers_bounties, profile name, original-submission line) each occur exactly once in S122; the S121:43 and S123:13/15/16/27 quotes are exact; the S120-based class/impact/fix/timeline statements match (CWE-416 at :79, options and 186-byte cap in INFO, Fixed-in and A/B/C recommendations, TIMELINE, CREDITS); "Closed/resolved, submitted 2023-05-23, disclosed 2023-06-25" matches S122 `state/substate/submitted_at/disclosed_at`. Pricing fields are kept separate and not netted: the flag contrast with round-85's S119 `false` is explained as two different teams' flags, and the KEV value is dated to the r35 catalog. Scope wording is consistent with PROVINCE.md: documentation only, isolated-lab outline with no payload, `No submission performed`, PARKED / `do_not_submit`, OPERATOR-GATED residual gates. No secret values appear outside `evidence/S122.txt` (grep for the token/credential/signature values: clean); the notes name only the field.

## Findings

**F-1 (blocker, claim-level — not the candidate author's fault): frozen C2 P1∧P2 is unsatisfiable; E1 and E2 cannot both pass on any package.**
E2 requires an artifact under `pkg/evidence/` byte-identical to `S122.txt`. Those bytes trip the gate's `credential` pattern (`…Security-Token=…`, first match at byte offset 1404, two occurrences — receipt `f1-e1-e2-unsatisfiable.txt` §A). The gate's R-NOSECRET walks every package file, so the byte-identical artifact always fails it. Three independent proofs: (a) pattern test on the snapshot bytes; (b) the live gate over the pre-freeze `b3` control attributes `hits=1,first=evidence/S122.txt,shape=credential` (§B); (c) constructive: a package binding S122 with complete manifest maintenance passes 7/8 rules and fails exactly R-NOSECRET (§C). The freeze's own `controls/c2-controls-r86.txt` corroborates: both S122-binding controls (`b3-wrong-subject`, `b3-url-added`) print `LIMB E1 FAIL gate_rc=1`, while `claims.json` C2 `do_nothing` describes them as failing E0 and is silent on E1 — the freeze misread its own control output (R22/R25 pre-freeze-satisfiability class). Consequence: at any landing, P1 (`LIMB E0-E5 pass … rc=0`) and P2 (`verdict=WELL-FORMED`, exit 0) are false, and the kill rule fires.
Fix (operator-owned; no wave seat may edit frozen bytes): either amend the claim post-freeze — E2 binds S122/S123 by the manifest-recorded sha256 plus a documented redacted artifact (the `removed` field records the stripped `profile_picture_urls` variants, so the package no longer replicates third-party CDN signature material), with controls re-derived; or accept the kill at landing, record M86-x (unsatisfiable frozen predicate, E1∧E2, controls showed `gate_rc=1` pre-freeze), and re-freeze a corrected counter next round. Do not weaken the gate's R-NOSECRET instead: on this capture the rule is doing its job.

**F-2 (medium): "expired" is false as of writing and carries no as-of date.** `X-Amz-Date=20261107T005829Z` with `X-Amz-Expires=3600` means the token expired at 2026-11-07T01:58:29Z; the candidate was written 01:05–01:11Z and the token was live then (and at review time). The word "expired" appears in `report.md` §Evidence, the S122 redaction note in `evidence/manifest.json`, and `provenance.json` secrets_attestation. Fix (all three): "a short-lived presigned-URL session token (X-Amz-Date 2026-11-07T00:58:29Z, X-Amz-Expires 3600 s; auto-expired after 2026-11-07T01:58:29Z) inside a public profile-picture URL".

**F-3 (medium): all four redaction receipts name verifier `KasegiR86` with receipt `.ufo/waves/round-86/l1/redaction-scan-r86.txt (pending L1 verification)` — the file does not exist and no scan has run.** This is the r85 F-1 class (attesting a verification that has not happened), here future-labelled but still carried in signed-shaped receipts (`scanned_artifact_sha256` asserted equal). Fix: set `verifier` to `"ExecC2Package (self-scan; independent re-scan pending at integration)"` or `"PENDING-L1"`; L1 writes the real identity and receipt when the scan actually runs. R-REDACT stays green (non-empty, distinct).

**F-4 (low-medium): `provenance.json` commands[4] records a command that never ran.** `bash .ufo/waves/round-86/l1/build-package-r86.sh … (L1 rebuild with review fixes; pending)` with `exit_code: 2` — the script does not exist in `.ufo/waves/round-86/l1/`. A commands[] entry asserts execution. Fix: delete the entry; keep the planned L1 rebuild in `identity_note` or a separate planned-steps note outside `commands[]`.

**F-5 (low-medium): `report.md` says "S122's `bounty_amount` is null" — the capture has no `bounty_amount` field at all** (grep count 0; receipt `facts-anchors.txt`). A field that is absent is not a null field, and the sentence names a JSON path the artifact cannot support. Fix: "S122 carries no bounty-amount field; the captured amount comes only from S120." (Observation, out of seat scope: the frozen SOURCES.md S122 row tail "not the bounty amount, which the record leaves null" invites the same misreading; flag for the round lesson, R8 governs the row.)

**F-6 (low): `report.md` §Evidence says "The gate's R-NOSECRET rule is documented to be unreachable on this capture" — backwards.** The rule is not unreachable; it deterministically fires on this capture (that is why the gate prints DEFECT). Fix: "the gate's R-NOSECRET rule fires on this capture (credential shape, `evidence/S122.txt`); the candidate therefore cannot print `verdict=WELL-FORMED` as-is, and the E1/E2 reconciliation is routed to the operator (status.json blockers[])."

**F-7 (low): two blanket "no credential/token" sentences contradict the bound artifact.** `report.md` Reproduction: "No credential material, no cookie value and no key material is recorded in this package." `claim_checklist.md`: "No credential material, token, cookie value or private key is stored in this package." — while `evidence/S122.txt` stores an AWS session-token value and an access-key id inside two signed URLs (disclosed in the adjacent note). Fix: qualify both — "No usable program credential is recorded in this package; the one exception, the presigned-URL token inside the byte-identical S122 artifact, is documented in §Evidence."

**F-8 (recommended, non-blocking): make the payer inference level explicit.** The package is substantially honest here — it separates the program-level payer statement (S123) from any disbursement claim, denies a per-party split twice, and quotes S122's flag without upgrading it to a payment record. One sentence would close the gap: "No capture names the payer of this specific report's bounty; `internet-bug-bounty` is the program-level payer named by S123, joined to this report by S122 being the IBB team's own record of it with `has_bounty?` true." Add it to the `price-payer` derivation.

**F-9 (expected, no fix): E5 fails pre-integration** because LOG.md/SHONEN.md cannot name the wave-dir path; provenance records the full-counter exit 1 honestly; `status.json` reviewer block is correctly PENDING-L1 and will record this review.

## Residual risk and verification gaps

- The pre-freeze `b3` scratch packages (used for §B) are the freeze driver's leftovers, not rebuilt by me; §B's other failing rules there (manifest polarity/redact/status) are artifacts of that driver's quick construction, which is why §C's constructive package was needed for a clean attribution.
- The custodian chain reuses the round-85 decision digests verbatim (formula does not bind package bytes); shape-valid and labelled a producer attestation, same as the landed r85 package, but a reader cannot tell from the chain alone which captures it covers.
- "cross-checked 2026-11-07" in the §Scope excerpt is vague (no named method); harmless, tighten opportunistically.
- I did not re-verify the S052 KEV capture bytes against its r35 manifest beyond digest arithmetic already recorded by the lane, and I did not re-fetch anything on the network (out of seat scope).
- Counter limits carried from r85 remain (E4 quotes are not field-bound; kev `catalogVersion` string is not machine-checked); the frozen controls and my probes cover this candidate's bytes, and M85-2's compensation ("C2's subject evidence is ReviewC2Package's independent read") is satisfied by this review.

## Verdict

The candidate's facts, pricing, honesty, and province wording are sound — every check I could run passes, and the producer recorded its own failing gate run truthfully. But the package cannot land as-is: the frozen E1∧E2 pair is unsatisfiable (F-1, operator-level), and F-2/F-3/F-4/F-6/F-7 are wording/attestation defects that should be fixed before integration. F-1 must go back to Main with the evidence; the rest are one-pass text fixes.

CHANGES-REQUESTED
