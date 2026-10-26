| page | url | status | fetched_bytes | snapshot_bytes | lines | sha256 |
|---|---|---|---|---|---|---|
| primary pin (erratum 1 URL) | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` | 200 | 143053 | 32623 | 518 | `ff3f3b2c…5fdce21` |
| home-page control | `https://certcc.github.io/SSVC/` | 200 | 105807 | 7730 | 286 | `a6613315…58bb56` |

Instrument used, copied byte-for-byte into scratch for every run below:
`corpus/instruments/source-recheck.py` sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`
(repo copy and scratch copy hashes equal; Python 3.14.8, Linux 7.2.11-arch1-1).
Independent corroboration: seat `ExecC2QuoteOnce` fetched the same overview page at `17:02:11Z` and reports the
same `snapshot_bytes=32623` / `sha256=ff3f3b2c…5fdce21`, so this seat's pin is byte-identical to the quote-pin
capture used by the manifest work — two independent fetches, identical bytes.

## 2. The junk twin content (`c2-controls/junk-f20.md`)

Landed here as content only (this seat's write scope is receipt + scratch). Byte-exact file body, 991 bytes,
sha256 `22ec0dd965913ff8fe83eb880b5033f9757ebcc6ee3d089345d04d2304cbb945`:

```markdown
# SSVC — negative control twin for F20: fabricated claims that MUST fail the pinned-source check

control: negative — every quoted sentence below is invented; none of the four occurs in the S054 capture
source: S054 — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ — capture corpus/source-snapshots/round-37/S054.txt
forged-at: 2026-10-26 (kasegi-shokunin round 37, seat ExecC2JunkControl)
ground: F20 (adversarial twin — must NOT be admitted in place of the real entry)
expected: source-recheck.py over S054 prints one `MISMATCH reason=quote-not-found` line per claim and exits 1

## Claim 1 — a fixed remediation clock

> "SSVC guarantees a fixed remediation deadline for every vulnerability."

## Claim 2 — a replacement for severity scoring

> "SSVC replaces CVSS severity scoring."

## Claim 3 — maintained by FIRST

> "SSVC is maintained by FIRST."

## Claim 4 — a numeric exploitability score

> "SSVC assigns each vulnerability a 0-1 exploitability score."
