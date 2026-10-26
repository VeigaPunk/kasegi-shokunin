# CSAF v2.0 — negative control twin for F21: fabricated claims that MUST fail the pinned-source check

control: negative — every quoted sentence below is invented; none of the four occurs in the S055 capture
source: S055 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html — capture corpus/source-snapshots/round-38/S055.txt
forged-at: 2026-10-26 (kasegi-shokunin round 38, seat ExecC2Junk)
ground: F21 (adversarial twin — must NOT be admitted in place of the real entry)
expected: source-recheck.py over S055 prints one `MISMATCH reason=quote-not-found` line per claim and exits 1

## Claim 1 — a mandatory CVSS v4.0 score

> "CSAF requires every advisory to carry a CVSS v4.0 score."

## Claim 2 — justification-free VEX status

> "The VEX status known_not_affected needs no justification."

## Claim 3 — maintained by FIRST

> "CSAF is maintained by FIRST."

## Claim 4 — mandated SSVC decision points

> "CSAF v2.0 mandates SSVC decision points."
