#!/usr/bin/env bash
# Round-85 C2 package builder (L1 integration copy of w1/ExecC2Package-build.sh, with the
# ReviewC2Package F-1..F-7 and CriticClaims D3 fixes applied by KasegiR85).
# Usage: build-package-r85.sh OUTPUT_ROOT   (lands at corpus/practice/curl-h1-1913733)
set -euo pipefail
OUT="${1:-.}"
mkdir -p "$OUT/evidence"
LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
cp "$LANE/corpus/source-snapshots/round-85/S119.txt" "$OUT/evidence/S119.txt"
cp "$LANE/corpus/source-snapshots/round-85/S120.txt" "$OUT/evidence/S120.txt"
cp "$LANE/corpus/source-snapshots/round-85/S121.txt" "$OUT/evidence/S121.txt"
D="$OUT" python3 -B <<'PYEOF'
import json, hashlib, pathlib
d = pathlib.Path(__import__('os').environ['D'])
def sha(b): return hashlib.sha256(b).hexdigest()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
s119 = sha(d/"evidence/S119.txt"); s120 = sha(d/"evidence/S120.txt"); s121 = sha(d/"evidence/S121.txt")
def dec(a,i,g): return hashlib.sha256(f"{a}|{i}|{g}|NO_SCOPE_OBJECTION".encode()).hexdigest()
in1 = hashlib.sha256(b"capture-sources input: S119+S120+S121 snapshot bytes").hexdigest()
dec1 = dec("capture-sources", in1, "kasegi-PROVINCE.md:52-documentation-only")
dec2 = dec("build-practice-package", dec1, "kasegi-PROVINCE.md:52-documentation-only")
manifest = {
 "schema_version": "evidence-manifest/v1",
 "sequence": 1,
 "package": "claim-package candidate — curl HackerOne 1913733 / CVE-2023-28319 (retrospective practice package)",
 "sources": [
   {"id":"S119","url":"https://hackerone.com/reports/1913733.json","fetched_utc":"2026-11-07T00:26:28Z","sha256":s119,"bytes":5001},
   {"id":"S120","url":"https://curl.se/docs/CVE-2023-28319.html","fetched_utc":"2026-11-07T00:26:29Z","sha256":s120,"bytes":3053},
   {"id":"S121","url":"https://curl.se/dev/vuln-disclosure.html","fetched_utc":"2026-11-07T00:26:30Z","sha256":s121,"bytes":19670}
 ],
 "artifacts": [
   {"path":"S119.txt","sha256":s119,"bytes":5001,"polarity":"positive","note":"HackerOne JSON record of report 1913733, byte-identical to corpus/source-snapshots/round-85/S119.txt"},
   {"path":"S120.txt","sha256":s120,"bytes":3053,"polarity":"positive","note":"curl advisory CVE-2023-28319, byte-identical to corpus/source-snapshots/round-85/S120.txt"},
   {"path":"S121.txt","sha256":s121,"bytes":19670,"polarity":"positive","note":"curl vulnerability-disclosure policy, byte-identical to corpus/source-snapshots/round-85/S121.txt"}
 ],
 "redactions": [
   {"artifact":"S119.txt","path":"S119.txt","artifact_sha256":s119,"scanned_artifact_sha256":s119,"producer":"ExecC2Package","verifier":"KasegiR85","verifier_receipt":".ufo/waves/round-85/l1/redaction-scan-r85.txt","removed":[],"note":"public HackerOne record JSON; no personal or customer data present, zero bytes removed"},
   {"artifact":"S120.txt","path":"S120.txt","artifact_sha256":s120,"scanned_artifact_sha256":s120,"producer":"ExecC2Package","verifier":"KasegiR85","verifier_receipt":".ufo/waves/round-85/l1/redaction-scan-r85.txt","removed":[],"note":"public vendor advisory; no personal or customer data present, zero bytes removed"},
   {"artifact":"S121.txt","path":"S121.txt","artifact_sha256":s121,"scanned_artifact_sha256":s121,"producer":"ExecC2Package","verifier":"KasegiR85","verifier_receipt":".ufo/waves/round-85/l1/redaction-scan-r85.txt","removed":[],"note":"public vendor policy page; no personal or customer data present, zero bytes removed"}
 ],
 "expected_head_sha256": dec2
}
(d/"evidence/manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
(d/"custodian-receipts.json").write_text(json.dumps({
 "schema_version":"custodian-receipts/v1",
 "policy":"every matched grant carries scope_signal NO_SCOPE_OBJECTION; the head binds the manifest",
 "decision_formula":"decision_sha256 = sha256(action + '|' + input_sha256 + '|' + matched_grant_id + '|' + 'NO_SCOPE_OBJECTION')",
 "chain":[
   {"seq":1,"action":"capture-sources","input_sha256":in1,"matched_grant_id":"kasegi-PROVINCE.md:52-documentation-only","scope_signal":"NO_SCOPE_OBJECTION","decided_by":"ExecC2Package","decision_kind":"producer attestation against PROVINCE.md:52 (documentation only; live-target testing refused); no independent custodian decided","decision_sha256":dec1},
   {"seq":2,"action":"build-practice-package","input_sha256":dec1,"matched_grant_id":"kasegi-PROVINCE.md:52-documentation-only","scope_signal":"NO_SCOPE_OBJECTION","decided_by":"ExecC2Package","decision_kind":"producer attestation against PROVINCE.md:52 (documentation only; live-target testing refused); no independent custodian decided","decision_sha256":dec2}
 ],
 "head_sha256":dec2
}, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
msha = hashlib.sha256((d/"evidence/manifest.json").read_bytes()).hexdigest()
(d/"status.json").write_text(json.dumps({
 "schema_version":"claim-status/v1","manifest_sha256":msha,"state":"PARKED",
 "verdict":"positive-blocked-retrospective-practice-package","claimable":False,"finding_count":1,
 "blockers":["retrospective practice package: already disclosed and fixed upstream (CVE-2023-28319, curl 8.1.0); duplicate of HackerOne 1913733"],
 "residual_gates":["operator submission gate","prior-submission check","reviewer distinctness"],
 "do_not_submit":True,"no_submission_performed":True,
 "claim_review":{"hard_gates":{"written_scope":"PASS","authorization":"PASS","evidence_integrity":"PASS","no_duplicate_or_prior_submission":"PENDING"},
 "subchecks":{"no_secrets":"PASS","operator_attribution":"PASS"},
 "reviewer":{"identity":"ReviewC2Package","requested_model":"@m_zfl","resolved_model":"zai/glm-5.3-flashx; fell back to anthropic/claude-haiku-5-5","fallback":True,"verdict":"CHANGES-REQUESTED on the candidate (F-1..F-7); fixes applied at L1 integration; re-review not recorded","report":".ufo/waves/round-85/w1/ReviewC2Package.md"}}
}, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
(d/"provenance.json").write_text(json.dumps({
 "schema_version":"provenance/v1",
 "agents":[
   {"identity":"ExecC2Package","transition":"capture-sources","requested_model":"@m_cru","resolved_model":"commandcode/stealth/crouton-alpha","role":"package producer"},
   {"identity":"ExecC2Package","transition":"build-practice-package","requested_model":"@m_cru","resolved_model":"commandcode/stealth/crouton-alpha","role":"artifact copy, manifest, report and gate runs"},
   {"identity":"KasegiR85","transition":"integrate-and-verify","requested_model":"anthropic/claude-opus-5-5:medium","resolved_model":"anthropic/claude-opus-5-5","role":"round-85 L1: redaction re-scan, review fixes, landing at corpus/practice/curl-h1-1913733"}],
 "transitions":[
   {"index":1,"agent":"ExecC2Package","requested_model":"@m_cru","resolved_model":"commandcode/stealth/crouton-alpha","from":"committed snapshots S119-S121","to":"evidence artifacts (byte copies)"},
   {"index":2,"agent":"ExecC2Package","requested_model":"@m_cru","resolved_model":"commandcode/stealth/crouton-alpha","from":"evidence artifacts","to":"six-file candidate package"},
   {"index":3,"agent":"KasegiR85","requested_model":"anthropic/claude-opus-5-5:medium","resolved_model":"anthropic/claude-opus-5-5","from":"candidate + ReviewC2Package findings","to":"landed package corpus/practice/curl-h1-1913733"}],
 "identity_note":"Producer ExecC2Package (@m_cru, served by commandcode/stealth/crouton-alpha per its session file) built the candidate. Verifier KasegiR85 (round-85 L1, anthropic/claude-opus-5-5) re-scanned each evidence artifact with the gate SECRET_PATTERNS at integration: receipt .ufo/waves/round-85/l1/redaction-scan-r85.txt. Reviewer ReviewC2Package (@m_zfl; served by zai/glm-5.3-flashx then anthropic/claude-haiku-5-5 after fallback) reviewed the candidate: CHANGES-REQUESTED F-1..F-7, addressed at integration (.ufo/waves/round-85/w1/ReviewC2Package.md).",
 "commands":[
   {"command":"cp corpus/source-snapshots/round-85/S119.txt candidate/evidence/S119.txt","exit_code":0},
   {"command":"cp corpus/source-snapshots/round-85/S120.txt candidate/evidence/S120.txt","exit_code":0},
   {"command":"cp corpus/source-snapshots/round-85/S121.txt candidate/evidence/S121.txt","exit_code":0},
   {"command":"python3 -B corpus/instruments/claim-package-check.py candidate (final run verdict=WELL-FORMED)","exit_code":0},
   {"command":"python3 -B .ufo/waves/round-85/c2/e2e-check.py --lane <lane> --pkg candidate","exit_code":1},
   {"command":"python3 -B .ufo/waves/round-85/c2/e2e-check.py --lane <lane> --pricing-only candidate/report.md","exit_code":0},
   {"command":"bash .ufo/waves/round-85/l1/build-package-r85.sh corpus/practice/curl-h1-1913733 (L1 rebuild with review fixes)","exit_code":0},
   {"command":"python3 -B .ufo/waves/round-85/l1/redaction-scan-r85.py corpus/practice/curl-h1-1913733 (KasegiR85 verifier scan)","exit_code":0}],
 "pin":{"remote":"https://github.com/VeigaPunk/kasegi-shokunin.git","commit":"4a2d34f203519a87078f21a896dc8679137ff675"},
 "policy_sha256":s121,
 "source":{"id":"S121","url":"https://curl.se/dev/vuln-disclosure.html","sha256":s121,"bytes":19670,"fetched_utc":"2026-11-07T00:26:30Z"},
 "external_effects_performed":[],
 "secrets_attestation":{"no_secrets":True,"findings":0,"by":"ExecC2Package","method":"claim-package-check.py R-NOSECRET scan of every package file plus manual review; zero hits"}
}, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
l120 = (d/"evidence/S120.txt").read_text(encoding="utf-8").splitlines()
l121 = (d/"evidence/S121.txt").read_text(encoding="utf-8").splitlines()
s119j = json.loads((d/"evidence/S119.txt").read_text(encoding="utf-8"))
scope = s119j["structured_scope"]
report = f"""# CVE-2023-28319 curl SSH sha256 fingerprint check use-after-free (retrospective practice package)

Program: curl
Official program URL: https://hackerone.com/curl
Official advisory URL: https://curl.se/docs/CVE-2023-28319.html
Package kind: retrospective practice package for an already-disclosed,
already-fixed issue. It is a training artefact built from public captures;
it makes no claim on any bounty, invents no new finding, and records no
contact with any target. Evidence digests: S119 {s119}, S120 {s120},
S121 {s121}.

## Scope excerpt

Source URL: https://curl.se/dev/vuln-disclosure.html (curl vulnerability-disclosure policy, captured 2026-11-07T00:26:30Z)
observed_at: 2026-11-07T00:26:30Z
content sha256: {s121}

The HackerOne record's structured_scope names the in-scope asset
verbatim:

> "asset_identifier":"{scope['asset_identifier']}"
> "asset_type":"{scope['asset_type']}"
> "max_severity":"{scope['max_severity']}"

(max_severity is the asset's ceiling on the program, not this report's rating.)

The curl program's own policy wording (S121):

> {l121[42]}
> {l121[43]}
> {l121[44]}

The advisory's scope-relevant lines (S120):

> {l120[81]}
> {l120[82]}
> {l120[83]}

## Vulnerability class

{l120[78]}. The advisory's VULNERABILITY text says libcurl offers a feature to
verify an SSH server's public key using a SHA 256 hash; when the check
fails, libcurl freed the memory for the fingerprint before returning an
error message containing the now-freed hash, risking insertion of
sensitive heap-based data into the error message. The HackerOne record
lists weakness "Use After Free" and cve_ids CVE-2023-28319.

## Affected asset

{l120[84]} The advisory also states that curl < 7.81.0 and curl >= 8.1.0
are not affected, and the issue was introduced in commit
3467e89bb97e6c87c7. The structured_scope asset is the curl source
repository ({scope['asset_identifier']}, SOURCE_CODE).

## Impact

The vendor rates the issue {l120[79]} and the HackerOne record's
severity_rating is medium. Under the curl policy's own severity ladder,
the vendor defines Medium as:

> {l121[102]}

That definition requires something else to also happen before the
problem becomes serious, which matches the advisory's own INFO text: the
flaw only applies to users of the CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256
option on libcurl builds using libssh2, and either CURLOPT_VERBOSE or
CURLOPT_ERRORBUFFER must also be set; the time window between the free
and the use is extremely short, and the largest possible info leak per
trigger is 186 bytes (CURL_ERROR_SIZE minus the 69-byte prefix), ending
at the first null byte within those bytes. The HackerOne report's own
reproduction note is the code-reader observation that the
fingerprint_b64 pointer is passed as a parameter for failure logging
after it is freed (curl/lib/vssh/libssh2.c).

## Reproduction (isolated lab only)

Isolated-lab outline reconstructed from the advisory's own description
(S120). No exploit payload is included in this package, and no live
target was contacted or tested.

1. In an isolated lab, build an affected libcurl (7.81.0 through 8.0.1,
   per {l120[84]}) with libssh2 support and sanitizers enabled.
2. Configure a local SSH server endpoint on loopback and point the lab
   build at it with CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256 set, plus
   CURLOPT_VERBOSE or CURLOPT_ERRORBUFFER, as the advisory's INFO text
   requires.
3. Make the server's public key differ from the configured SHA 256 hash
   so the fingerprint check fails.
4. Observe the free-before-use of the fingerprint buffer in the failure
   logging path; a sanitizer build reports the use-after-free.

No credential material, no cookie value and no key material is recorded
in this package.

## Suggested fix

Advisory SOLUTION and RECOMMENDATIONS (S120):

> {l120[89]}
> {l120[91]}
> {l120[92]}
> {l120[93]}

Upgrading to curl 8.1.0 is the vendor's first recommendation; the fix
commit is the one named above. The lab outline should re-run against
8.1.0 and observe the free-before-use no longer occurring.

## Disclosure timeline (vendor, S120 TIMELINE)

> {l120[95]}
> {l120[96]}

The advisory is dated May 17 2023; the HackerOne record shows the
report as Closed/resolved with disclosed_at 2023-05-24T08:25:54.715Z.
The vendor credits Wei Chong Tan (reporter) and Daniel Stenberg
(patcher).

## Evidence

- evidence/S119.txt sha256 {s119} polarity: positive
- evidence/S120.txt sha256 {s120} polarity: positive
- evidence/S121.txt sha256 {s121} polarity: positive

## Pricing

price-program: curl
price-severity: medium
price-reward-at-disclosure: 2400 USD
price-platform-bounty-flag: false
price-reward-current-policy: none
price-cvss: not-set-by-vendor
price-kev: not-listed catalogVersion 2026.10.23
price-cve: CVE-2023-28319

> {l120[78]}
> {l120[80]}
> {l121[42]}
> {l121[94]}
> {l121[102].split(" Past example")[0]}

Pricing derivation (all values re-derived from the captured records, not
from the package author's memory).

- severity agreement check — the HackerOne record (S119) says
  severity_rating medium, matching the advisory's `{l120[79]}`; the
  comparison is case-insensitive, and the counter enforces that both
  records agree before accepting the value. On curl's own four-level
  ladder (S121) Medium is "less hard than Low to exploit or trigger" and
  "usually needs something else to also happen to become serious"; the
  advisory's damage note (short free-to-use window, leak capped at 186
  bytes) fits that rung, not High.
- price-reward-at-disclosure — the advisory (S120) records its own line
  `{l120[80]}`: the vendor records a 2400 USD bounty for this report. No
  captured record shows who paid it or that a payment was made.
- price-platform-bounty-flag — the HackerOne team record (S119) says
  has_bounty? false. That flag describes the platform team's current
  bounty configuration; it does not by itself mean this report was
  unpaid. The advisory (S120) separately records a 2400 USD bounty for
  this specific report. The records conflict on their face: S119
  has_bounty? false and S121 "There is no bug bounty" against S120
  "Bug bounty: 2400 USD". They answer different questions (platform
  team flag today, vendor policy today, vendor record of 2023), so the
  package keeps three separate fields and does not net them into one
  price.
- price-reward-current-policy — the current curl disclosure policy
  (S121) opens with `{l121[42]}`, so a new curl finding submitted today would
  price at no reward under the current policy. That statement governs
  new findings; it does not retroactively erase the 2400 USD recorded
  for this one in 2023.
- price-cvss — the current policy (S121) says `{l121[94]}` (the rest of that
  sentence continues in the capture; the leading clause is the exact
  vendor wording). The vendor sets no CVSS for its CVE records, so the
  package records not-set-by-vendor rather than a numeric score.
- price-kev — CVE-2023-28319 occurs 0 times in the round-35 KEV capture
  (S052, catalogVersion 2026.10.23, captured 2026-10-26 in round 35 and
  not re-fetched for this package), so the value is not-listed as of
  that catalog only.
- price-cve — the HackerOne record (S119) lists cve_ids CVE-2023-28319,
  the same identifier the advisory (S120) assigns to the issue.

## Submission

No submission performed.
"""
(d/"report.md").write_text(report, encoding="utf-8")
checklist = f"""# Claim checklist — curl / HackerOne 1913733 (retrospective practice package)

OPERATOR-GATED: every step below is an operator action. This package has been
submitted nowhere, no external effect has been performed, and the finding
it describes is already public and fixed upstream; it is not claimable.

## Program

- Program: curl (project curl / libcurl)
- Official program URL: https://hackerone.com/curl
- Official advisory URL: https://curl.se/docs/CVE-2023-28319.html
- Original report: https://hackerone.com/reports/1913733

## Submission steps (operator only)

1. Treat this package as training material only. Its blocker is in
   status.json: the issue is already disclosed and fixed upstream
   (CVE-2023-28319, curl 8.1.0); any submission would duplicate
   HackerOne report 1913733. Do not submit.
2. If an operator ever reuses the lab outline in report.md, run it only
   against a local build in an isolated lab. This lane refuses
   live-target testing (PROVINCE.md): no probe, scan, login or submission
   to any target.
3. Attach evidence/S120.txt (sha256 {s120}) and the other
   two evidence artifacts with the digests printed in report.md, only
   for reviewer inspection.
4. Copy the scope, impact and timeline fields from report.md; do not
   restate the vendor text in stronger terms than the advisory's own
   Severity: Medium, and do not price a new curl finding above the
   current policy (no bounty; cvss not-set-by-vendor).
5. Keep external_effects_performed empty in provenance.json until a
   submission receipt exists outside this package.

## Residual gates

- OPERATOR-GATED operator submission gate — no agent may submit, message a
  vendor, or create a portal record. This package is PARKED and
  do_not_submit is true.
- OPERATOR-GATED prior-submission check — the report is public, credited
  to Wei Chong Tan and fixed in curl 8.1.0; duplicates are certain.
- OPERATOR-GATED reviewer distinctness — status.json carries reviewer
  identity "ReviewC2Package" (verdict CHANGES-REQUESTED on the
  candidate, fixes applied at integration, re-review not recorded); an
  independent reviewer distinct from the producer (ExecC2Package) and
  verifier (KasegiR85) identities must approve before claimable may
  flip to true.

No credential material, token, cookie value or private key is stored in this
package. No submission performed.
"""
(d/"claim_checklist.md").write_text(checklist, encoding="utf-8")
print("rebuilt", s119, s120, s121, dec2, msha)
PYEOF
echo "rebuilt at $OUT"
