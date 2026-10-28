# ScribeExemplarReport — exemplar prose pair (round 43, C2 coverage / depth:verifiability)

Seat: scribe, leaf (no dispatch). Lane `kasegi-shokunin`, round 43, base
`ab98fac9dce87130bc4f66de89e30650d63943dc`. Claims read first and never edited:
`.ufo/waves/round-43/claims.json` (C2: the exemplar must be built from ONE public
disclosed report captured this round as a new mined registry row, documented by
`corpus/knowledge/claim-package-gate.md`; `claimable` stays false; operator gates
named in `claim_checklist.md`).

## Deliverables (in `.ufo/waves/round-43/w1/`)

| deliverable | lands at | lines | bytes | sha256 |
|---|---|---|---|---|
| `ScribeExemplarReport.report.md` | `corpus/instruments/fixtures/claim-package/exemplar/report.md` | 101 | 4663 | `2bd06e415ee4e63e1a5499a17826b020621c22633e360ceeb5827c29084f1be0` |
| `ScribeExemplarReport.claim-checklist.md` | `corpus/instruments/fixtures/claim-package/exemplar/claim_checklist.md` | 48 | 2618 | `d694052e7aeb3a83923334ba7b9445dc4e311c3a5f51a57f20574d208552e551` |

Only these two files (plus this receipt) were written under the lane. No `corpus/`
write, no fleet-root write, no PATH write, no mutating git/jj command.

## Source it quotes

The capture landed this round as `ExecSourceCapture.S067.txt` (deliverable, not
yet moved into `corpus/source-snapshots/round-43/`; the L1 lands it). I did not
fetch the network: every external fact below is read from those landed bytes.

```
$ sha256sum .ufo/waves/round-43/w1/ExecSourceCapture.S067.txt
327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b  ExecSourceCapture.S067.txt
$ wc -lc ExecSourceCapture.S067.txt
 131 6446 ExecSourceCapture.S067.txt
```

Capture provenance (from `ExecSourceCapture.provenance.txt` / `.manifest.json`):
URL `https://curl.se/docs/CVE-2023-38545.html`, HTTP 200, raw 13940 bytes,
normalized 6446 bytes / 131 lines, fetched `2026-10-28T16:39:59Z`.

The report cites exactly two 64-hex tokens and both are artifact digests in the
exemplar's `evidence/manifest.json` (produced by ExecExemplarPackage):

- `9103704c553579828d1313ca7b9eaedba270a0160e39484e280001629d037cc8` —
  `evidence/source-excerpt.txt`, capture lines 100-114 with a three-line provenance
  header; this is the report's "content sha256".
- `327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b` —
  `evidence/source-capture.txt`, the full 6446-byte capture.

The checklist cites no digest.

## Contract coverage (report.md)

| Contract row (`corpus/knowledge/claim-package-contract.md`) | Where in the deliverable |
|---|---|
| Title | H1 line 1 |
| Program + official URL | header block, lines 3-5 |
| `Scope excerpt` = verbatim policy text + URL + observed_at + content sha256 | `## Scope excerpt`, with URL, `observed_at: 2026-10-28T16:39:59Z`, the excerpt digest and the six verbatim capture lines |
| Vulnerability class | `## Vulnerability class` (CWE-122, SOCKS5 handshake) |
| Repro steps without secrets / live target | `## Reproduction (isolated lab only)`, loopback-only, no external host, states it was not executed |
| Impact tied to the policy's own severity/reward language | `## Impact`, quoting `Severity: High`, `Bug bounty: 4660 USD`, `CWE-122`, `Area: SOCKS5` |
| Affected asset | `## Affected asset`, 7.69.0-8.3.0, introduced-in/fixed-in commit URLs |
| Suggested fix | `## Suggested fix`, upgrade/patch plus the advisory's mitigations |
| Disclosure timeline | `## Disclosure timeline` (2023-09-30, 2023-10-03, 2023-10-11, capture dates) |
| Literal marker `No submission performed` | final line, exactly once |

`claim_checklist.md` carries `OPERATOR-GATED` (4 occurrences), a per-program
operator-only step list, and names the three residual gates (operator submission,
prior-submission check, reviewer distinctness); it stores no credential material.

## Evidence actually run

Scratch `S=/fast/scratch/hyaku/kasegi-r43/ScribeExemplarReport` (disk guard read
before the pass; `/fast` 27 % used, 593 G free). Gate under test: the landed
ExecGateCore deliverable
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py`.

Package assembly: the five non-prose files and four evidence artifacts were copied
from the `ExecExemplarPackage.*` wave-dir deliverables into `$S/pkg`, and
`report.md` / `claim_checklist.md` were my two deliverables. Then:

```
$ python3 ExecGateCore.claim-package-check.py "$S/pkg"   # exit=0
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=2,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/ScribeExemplarReport/pkg rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```

### Quote fidelity (each line compared to the capture at its stated number)

```
quoted lines: 6
line 71: IDENTICAL :: This flaw makes curl overflow a heap based buffer in the SOC
line 100: IDENTICAL :: CWE-122: Heap-based Buffer Overflow
line 101: IDENTICAL :: Severity: High
line 108: IDENTICAL :: Bug bounty: 4660 USD
line 112: IDENTICAL :: Affected versions: libcurl 7.69.0 to and including 8.3.0
line 113: IDENTICAL :: Not affected versions: libcurl < 7.69.0 and >= 8.4.0
fidelity: all-verbatim
excerpt body lines: 15 line100-114 match: True
all quote lines present in capture: True
```

### Mutant controls (each copy of `$S/pkg` with one delta; gate run on the copy)

```
--- m1 (marker line deleted)          RULE R-REPORT verdict=fail detail=marker=absent        exit=1
--- m2 (excerpt digest last byte 8→9) RULE R-REPORT verdict=fail detail=cited=2,unbound=1      exit=1
--- m3 (Scope excerpt heading renamed)RULE R-REPORT verdict=fail detail=scope-excerpt=absent   exit=1
--- m4 (all https:// → http://)       RULE R-REPORT verdict=fail detail=url=absent             exit=1
--- m5 (appended "token: <40 hex>")   RULE R-NOSECRET verdict=fail detail=hits=1,first=report.md,shape=credential  exit=1
--- m6 (appended 65-hex run)          RULE R-REPORT verdict=pass cited=2,unbound=0; R-NOSECRET hits=0  exit=0
```

So the marker, the scope phrase, the program URL and the cited-digest binding are
each load-bearing, and a secret-shaped labelled hex is caught. m6 is the
whole-token control: a 65-character hex run adds no cite (the R41 boundary holds
for this rule).

Static scans on the deliverables:

```
$ grep -oP '(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])' ScribeExemplarReport.report.md | sort -u
327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b
9103704c553579828d1313ca7b9eaedba270a0160e39484e280001629d037cc8
$ <same on claim-checklist.md> | wc -l
0
$ grep -cF 'No submission performed' ScribeExemplarReport.report.md
1
$ grep -c 'OPERATOR-GATED' ScribeExemplarReport.claim-checklist.md
4
$ grep -c '<pending' <both files>
0
```

## Overlap and landing decision for the L1

`ExecExemplarPackage` also emitted a `report.md` / `claim_checklist.md` pair (its
item names all six files); it passes the gate too. **Land exactly one pair, never
a concatenation.** If the L1 prefers this pair: the manifest, custodian chain and
status bind none of `report.md`'s bytes, and my report cites only the two artifact
digests above, so no other file changes. If it prefers the other pair, this pair
is redundant and can be dropped without touching C2's counters.

## Limits / honesty

- I did not fetch the advisory; the quotes and dates are the landed capture's
  bytes, and `observed_at` is the capture's fetch instant, not a second fetch.
- The program's live submission form and current policy page are not in the
  capture, so the checklist says the operator confirms them and asserts no URL
  beyond the captured ones.
- The fixture reviewer/redaction identities are role names, not an independent
  reviewer; reviewer distinctness is therefore carried as an open residual gate.
- `2026-10-25 11:18:20 GMT` is the capture's `Last-Modified` header; the advisory
  text itself dates from 2023-10-11.

## Tooling / cleanliness

Nothing installed or upgraded (no pacman, no `uv`, no PATH write; no network).
`TMPDIR` was set to `$S` for every write; no fixture used a relative path.
Scratch `/fast/scratch/hyaku/kasegi-r43/ScribeExemplarReport` is removed before
yield (`rm -rf`, verified absent).
