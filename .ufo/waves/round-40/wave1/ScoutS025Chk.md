# ScoutS025Chk — cross-check of ScoutS025's S025 capture (attack-on-build)

Seat: ScoutS025Chk (reviewer, leaf). Round 40, wave 1. Item: re-fetch/re-open ScoutS025's capture
for row S025, verify sha256/status/size and quote occurrence (grep -c >= 1), assess `mined` vs
`rejected` per QUALITY.md Q1-Q6 and CORPUS.md. Deliverable: `ScoutS025Chk.txt` (one-line verdict,
1997 bytes, 1 line) beside this receipt.

## Row under decision (corpus/SOURCES.md L31, status at check time: queued)

S025 — CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application
Vulnerabilities — https://arxiv.org/abs/2503.17332 — paper — tier A — scope "CVE-Bench's own
measured performance on its real-world web-application exploitation tasks" — anchor "Abstract;
published 2025-03-21, arXiv:2503.17332".

## Independent verification (my own commands, scratch /fast/scratch/hyaku/kasegi-r40/ScoutS025Chk)

### 1. Landed capture re-opened (not trusted, hashed)

```
$ sha256sum .../wave1/ScoutS025.capture.txt
faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b
$ wc -c -l < .../wave1/ScoutS025.capture.txt
   1490   71851
```
Matches ScoutS025.manifest-record.json (`sha256`/`snapshot_sha256` faa1c1f8…, snapshot_bytes
71851, lines 1490) and the IRC record. VERIFIED.

### 2. Fresh re-fetch + full pipeline regeneration

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o S025.pdf https://arxiv.org/pdf/2503.17332
raw-PDF refetch: status=200 bytes=602933 sha256=334417c3bbc4fbaa1777df3a98b5c518e9187cac3b21714879116a0260f26cb1 utc=2026-10-26T21:20:38Z
$ python3 corpus/instruments/capture-source.py --id S025 --url https://arxiv.org/pdf/2503.17332 --kind pdf --out S025-regen.txt
S025 status=200 fetched_bytes=602933 snapshot_bytes=71851 sha256=faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b utc=2026-10-26T21:20:38Z
$ cmp S025-regen.txt .../wave1/ScoutS025.capture.txt && echo BYTE-IDENTICAL
BYTE-IDENTICAL to landed capture
```
Raw bytes (sha256 334417c3…, 602933 B), HTTP 200, and the converted snapshot all reproduce.
pdftotext 26.08.0 (poppler, /usr/bin, preinstalled — no install performed this round). VERIFIED.

### 3. Abs landing page re-fetch (declared metadata-only input)

```
status=200 bytes=44575 fetched_utc=2026-10-26T21:18:29Z
sha256 28675fd2808412c1255561965bfc8d409d979f05cea2877db5acc0606146d627
HTTP/2 200, content-type: text/html; charset=utf-8
```
Byte-identical to the scout's fetch 2.5 minutes earlier (manifest `landing_page.raw_sha256`
28675fd2…, raw_bytes 44575). Page states "Submitted on 21 Mar 2025" and "last revised 24 Jun 2025
(this version, v4)" with [v1]–[v4] markers — the manifest's `revision` note confirmed. VERIFIED.

### 4. Quote occurrence (the grep -c >= 1 requirement)

Plain single-line grep of the full quoted sentences returns 0 — pdftotext hard-wraps lines
mid-sentence (Q1 starts at end of L32, continues L33: "…agent framework can / exploit up to 13%
of the vulnerabilities."). Under the capture's declared normalization class (whitespace collapse,
Q8's `normalized=markup-whitespace` family; here newline→space + space-collapse):

```
Q1 occurrences: 1   (16 words, Abstract L31-34, anchor 32)
Q2 occurrences: 1   (20 words, §4 "Success Rate." L506-510, anchor 507)
"resolve up to" anywhere: 0
"exploit up to 13": 1     "12.5": 1     "zero-day": 28
```
Both quotes exactly-once with anchors (Q9 satisfied); both ≤ 25 words, locations exact, numbers
copied from source (Q3 satisfied). The instrument-verified anchors stand as filed; my counts are
a cross-check, not a replacement for the entry's own recheck line. VERIFIED with the stated
normalization — a gate that greps raw lines will see 0 and must apply the declared collapse.

### 5. Verdict assessment (Q1-Q6, CORPUS.md)

- Tier: original paper = tier A for the row's scope (SOURCES.md contract v1). Q2-compatible.
- New ground: `grep -rin CVE-Bench corpus` hits only SOURCES.md; no knowledge entry cites S025;
  adjacent rows S029/S030 cover CVE-definition ground, F23 covers CycloneDX analysis subtree —
  neither covers the benchmark's measured agent-exploit performance. Not covered/superseded →
  `mined`, not `rejected`. (Agrees with ScoutS025's receipt §b, whose chain L71 placement and
  S010-only generic-benchmark citation I spot-checked.)
- Q4: teachable content is the paper's own first-party measurements (13% abstract; 10% zero-day /
  12.5% one-day §4; 8 pre-defined attack types; closed 40-CVE set) — entry must label these
  first-party and keep the paper's own Limitation boundary; the row's `teaches` line already
  scopes it that way.
- Q5: falsifiable rules should quote §4's 10%/12.5% (exact figures) rather than the abstract's
  rounded 13% — in-source internal rounding, flagged by the scout too.
- Q6: paper is documentation; no probing instructions, no credentials.
- CORPUS.md rule 1 (Gate records URL, access date, ≤25-word quote + location) and Q3 (location
  plus revision): the round-40 Gate block must quote the **v4** wording and name revision
  2025-06-24; the row's anchor field ("published 2025-03-21") names v1's date and stays immutable
  (R8) — the revision the capture binds is v4, and the Gate/entry must say so.

### 6. Discrepancy finding — pinned with fresh evidence (sharper than the receipt's [INFERENCE])

Round-22 lesson L101 (and the registry row's 2026-10-19 basis) quote: "Our evaluation shows that
the state-of-the-art agent framework can resolve up to 13% of vulnerabilities." — ABSENT from the
v4 PDF text (`resolve up to` → 0). New evidence: my abs-page fetch of TODAY (2026-10-26T21:18:29Z)
still serves that exact wording — `resolve up to 13` ×3 (citation_abstract meta ×2 + visible
blockquote) and `exploit up to 13` ×0. So the r22 quote is a verbatim-accurate capture of arXiv's
metadata abstract, which itself has drifted from the v4 PDF's internal abstract ("Our experiments
show … exploit up to 13% of the vulnerabilities."). Conclusion: source-internal
metadata-vs-PDF drift at arXiv, not a transcription error by the lane. Disposition per R9/R8:
append/record in the round-40 Gate (and let the entry cite v4 wording + v4 revision); do not
rewrite the r22 lesson or the row's immutable fields.

## Cross-check of ScoutS025's receipt claims

| claim | my result |
|---|---|
| capture 71851 B / 1490 lines / sha faa1c1f8… | reproduced byte-identical |
| raw PDF 602933 B / sha 334417c3… / HTTP 200 | reproduced (fresh fetch 21:20:38Z) |
| abs page 44575 B / sha 28675fd2… / HTTP 200 | reproduced byte-identical |
| v4 = last revised 2025-06-24 | confirmed on abs page |
| Q1/Q2 exactly-once, anchors 32/507 | confirmed under declared normalization |
| "resolve up to 13" absent from v4 | confirmed (0) |
| receipt says "the abs page itself is v4 (checked)" | nuance: page *serves v4 as current*, but its metadata abstract text is still the pre-v4 wording — see §6 |
| no tools installed; disk guard green | same: no installs; disk guard green at 21:14Z (/fast/scratch 26%) |

## Residual risks / gaps

- The landed snapshot binds v4 as served 2026-10-26; a v5 would re-open quotes (recheck cadence
  `on-release` on the row is right).
- Plain `grep -F` on raw lines cannot see either quote (line-wrap); any gate counting occurrences
  must declare the normalization (Q8) — recorded above.
- Q1's sentence begins at end of L32 (anchor L32 = sentence start; manifest documents this);
  Q2 begins at end of L507 (the receipt records an earlier draft anchored 508 was corrected).
- My fetches: abs 2026-10-26T21:18:29Z (200, 44575 B), PDF 2026-10-26T21:20:38Z (200, 602933 B);
  UA kasegi-shokunin/1.0, --max-time 90, both into scratch.

## Other

Scratch dir /fast/scratch/hyaku/kasegi-r40/ScoutS025Chk removed after copying deliverable +
receipt into the wave dir. Tools installed: none. No git/jj mutations anywhere. Lane files
touched: only `.ufo/waves/round-40/wave1/ScoutS025Chk.txt` and this receipt.
