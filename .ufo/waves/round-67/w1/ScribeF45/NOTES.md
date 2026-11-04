# ScribeF45 — measurement receipts, round-67 w1

Seat: `ScribeF45` (scribe, leaf member — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base revision at capture: `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`.
Scratch: `/fast/scratch/hyaku/kasegi-r67/ScribeF45/` (deleted on exit; all durable receipts copied into this seat
directory first).

## 1. What this seat did

Independently opened and captured FIRST's PSIRT Maturity document with the lane's own instrument
(`corpus/instruments/capture-source.py`), then drafted — **from its own capture bytes only** — a knowledge entry,
a README coverage-map row, a Frontier F45 row and an 11-column `corpus/SOURCES.md` registry row. Nothing was
written to production; the L1 lands every production byte.

This seat's scope is **C2 (coverage)** only. C1 (the depth:verifiability multi-head SIGPIPE repair) is not this
seat's scope; the sibling seats `ExecMultiHeadGate`, `ExecMultiHeadProbes`, `ExecMultiHeadDriver`,
`MutationMultiHead`, `ReviewMultiHead`, `CriticMultiHead`, `SentinelMultiHead` and `RevengerMultiHead` own it.
This seat made **no change** to `corpus/instruments/figure-audit.py` and ran **no** figure-audit probe.

## 2. Capture receipts

### 2.1 S100 — the HTML page named in the wave spec

```
$ python3 -B corpus/instruments/capture-source.py --id S100 \
    --url "https://www.first.org/standards/frameworks/psirts/psirt_maturity_document" \
    --out <seat>/S100.txt --kind html
S100 status=200 fetched_bytes=82978 snapshot_bytes=59068 \
  sha256=cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f \
  utc=2026-11-04T20:52:02Z
```

HTTP response headers observed on a companion fetch:
`Last-Modified: Mon, 26 Jan 2026 14:43:46 GMT`, `Content-Type: text/html; charset=UTF-8`,
`Content-Length: 82978`.

Committed capture: `S100.txt` — 478 lines, 59068 bytes, sha256 `cf834a65…bff9f`.
Content body: L216-L464. Site navigation occupies L1-L215; the footer navigation resumes at L465 and the
copyright footer is L478.

### 2.2 S101 — the PDF companion

```
$ python3 -B corpus/instruments/capture-source.py --id S101 \
    --url "https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Maturity_Document.pdf" \
    --out <seat>/S101.txt --kind pdf
S101 status=200 fetched_bytes=644190 snapshot_bytes=58889 \
  sha256=a55e315ffaeda54436d190ff0e77560224a2fd803f8f4a34f5adf90d01185bc8 \
  utc=2026-11-04T20:53:24Z
```

`pdfinfo maturity.pdf`: Pages 29, CreationDate `Thu Dec  6 17:32:58 2018 -02`, Producer/Creator
`Microsoft® Word for Office 365`, PDF version 1.7, raw sha256
`f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`.

The PDF's raw digest **reproduces the round-65 lead's recorded companion-PDF digest exactly**.

### 2.3 The raw-HTML digest is not reproducible — measurement

The round-65 lead recorded `sha256 334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e` at
82978 bytes. This seat measured why that digest cannot be re-derived:

| fetch | raw bytes | raw sha256 | CSP nonce in tail |
|---|---|---|---|
| no query, t0 | 82978 | `fce2d8307e9e17c2…` | `tSpAxu6OKaKmpw9JA1x55w` |
| no query, t0+65 s | 82978 | `fce2d8307e9e17c2…` | `tSpAxu6OKaKmpw9JA1x55w` |
| `?cb=1` | 82978 | `1ec384fce4c40e9a…` | `RSxZYY1E6_wLxySWOOEx-g` |
| `?cb=2` | 82978 | `7fefa22617e92301…` | `R6H_r06INjpwRmqoysKeYA` |

Byte-diff of the `?cb=1` and `?cb=2` responses: **84 differing byte positions in 4 runs of 21 bytes**, at offsets
82449-82469, 82542-82562, 82634-82654 and 82860-82880 — every one of them a `nonce="…"` attribute value.
Nothing else differs; the byte length is identical at 82978.

The `capture-source.py` **normalized-text** snapshot digest was `cf834a65…bff9f` on **all six** fetches
(2 user agents, 3 cache-busting query strings, 1 no-query fetch 65 s later) — reproducible. The committed
snapshot, not the raw HTML, is the anchor.

**Consequence for the L1:** the round-65 lead's `334aeb01…` is a raw digest over a nonce-bearing response and
must be retired, not carried forward. The replacement anchors are `cf834a65…` (normalized HTML) and
`f217c446…` (raw PDF).

### 2.4 Quote verification with the production instrument

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py \
    --manifest .ufo/waves/round-67/w1/ScribeF45/manifest-candidate.json
S100:sha256 OK
S100:M01-purpose-line OK occurrences=1 anchor=217-ok
… (40 S100 lines) …
S101:sha256 OK
S101:P01-cover-year OK occurrences=1 anchor=3-ok
… (10 S101 lines) …
EXIT=0
```

**50/50 quotes OK, exit 0.** Every quote is exactly-once in its capture and every declared anchor verifies.

## 3. Body-scoped measurements (over S100 content L216-L464)

| measurement | value |
|---|---|
| `Maturity Level` occurrences | 12 |
| level heading patterns found | `Basic`, `Intermediate`, `Advanced` (exactly three) |
| `Level 4` occurrences | **0** |
| `\bshall\b` occurrences | **0** |
| `certif` occurrences | **0** |
| `conform` occurrences | **0** |
| `compliance` occurrences | **0** |
| `\bMUST\b` occurrences | 1 (S100 L292, "these key things MUST be in place…") |
| `\bmust\b` (any case) | 12 |
| `[Mm]aturity` occurrences | 21 |
| `ISO/IEC 29147` | 3 |
| `ISO 30111` | 1 |
| `CVSS` | 6 |
| `Bug Bar` | 1 |
| `embargo` | 1 |
| `reproduction` | 3 |
| `charter` | 7 |
| year tokens in the body | `2013` only (the CSIRT-framework origin story at L220) |

Over the **whole** S098 capture (`corpus/source-snapshots/round-65/S098.txt`): `grep -c -iE "Maturity Level"` = **0**.
S098's only maturity *definition* is the glossary entry at S098 L1510.

## 4. Annex 7 checklist structure (the per-level capability-area counts)

Measured by walking the S100 capture's own heading lines between L398 and L464:

| level | capability areas named | heading lines |
|---|---|---|
| Maturity Level 1 | 5 — Operational Foundations, Vulnerability Discovery, Vulnerability Triage, Remediation, Vulnerability Disclosure | L399, L404, L407, L410, L413 |
| Maturity Level 2 | 7 — Operational Foundations, Stakeholder Ecosystem Management, Vulnerability Discovery, Vulnerability Triage, Remediation, Vulnerability Disclosure, Training & Education | L419, L428, L432, L434, L437, L439, L442 |
| Maturity Level 3 | 6 — Operational Foundations, Stakeholder Ecosystem Management, Vulnerability Discovery, Remediation, Vulnerability Disclosure, Training & Education | L446, L449, L453, L457, L460, L462 |

Level 3 names **no** Vulnerability Triage heading. This is a measured absence from the *checklist*, not an
assertion about what a Level-3 team does; the draft entry states it as "the Level 3 checklist names no
Vulnerability Triage heading — measured, not assumed."

## 5. The figures are not in either capture

Figures 1-3 are PNG images. The HTML references them as
`PSIRT-maturity/figure1.png`, `figure2.png`, `figure3.png` with `alt` text matching the captions.
`pdftotext` over the PDF in **plain** mode and in **`-layout`** mode yields **0** occurrences of each figure's
box labels (`Established Finders`, `Internal Stakeholder Management`, `USE CASE 1`, `Service Area 1` — all 0 in
both extractions). The per-level service-area *listings* therefore exist only in pixels.

Fetched in this seat for inspection, digests recorded but **not** part of either committed capture:

| file | bytes | sha256 |
|---|---|---|
| `figure1.png` | 32448 | `66d89066da216c026dbef1f12613e5901e0d816c340affb1abc56aead4a0e847` |
| `figure2.png` | 103995 | `5d6ff047ff1ecf12909cec4cd12bc875577d77a4b28acb8056f95a44ae78323d` |
| `figure3.png` | 162903 | `bdfbc9a04ad063d7c181e42232ebfb44bab59f2452dc7d0e8feb922ca8e59d00` |

The draft entry therefore makes **no claim about figure contents**. The per-level counts in claim C15 come from
the Annex 7 checklist's own text heading lines, which are line-anchored and verifiable.

## 6. What this seat explicitly refuses to assert, and why

1. **That FIRST publishes a PSIRT maturity *certification*, *rating* or *score*.** The document's own PDF cover
   says the descriptions are "for informational purposes only" (S101 L8); the term is defined as "a profile of a
   product security team" (S100 L224); and the content body carries zero `shall` / `certif` / `conform` /
   `compliance` occurrences. The only `MUST` in the body (L292) is addressed to the team about its own
   foundations, not to a reader of the document.
2. **That a fourth level exists.** `Level 4` occurs 0 times. The "Beyond 'Level 3'" heading (L353) is followed
   by a single rhetorical line (L354) and then Annex 1 (L355). It names no level and no capability.
3. **Any publication date for the HTML page.** The body carries no date token but `2013` (L220, the origin
   story). The HTTP `Last-Modified` header (2026-01-26) is a server header, not an edition. The PDF cover's
   `2019` (S101 L1) and `pdfinfo`'s CreationDate (2018-12-06) belong to the PDF artifact and are reported as
   such. `verified-at` in the draft entry is therefore an access date, not an edition.
4. **That the raw-HTML sha256 in the round-65 lead is reproducible.** §2.3 measures why it is not.
5. **That the figures show anything.** §5 measures why the text captures cannot carry them.
6. **That the maturity document adds service-catalogue ground.** L356 defers the glossary and supporting
   resources to the PSIRT Services Framework, and L227 attributes the Operational Foundations concept to that
   framework. The catalogue, the qualification gate, the reproduction duty and the three organizational models
   stay with F44/S098.
7. **That any team operates at, or was ever assessed against, any level.** Nothing in either capture reports a
   team's level, an audit, an attestation or an outcome.
8. **That the maturity document's ISO/IEC 29147 / ISO 30111 mentions state requirements.** It names them (3 and
   1 occurrences) as references; the requirements stay with F11.
9. **Any claim about the PDF's page-number artifact lines.** The `pdftotext` layer interleaves bare page
   numbers (e.g. S101 L589 `19`, L590 `20`); the draft entry cites none of them.
10. **Fresh upstream verification.** The recheck compares digest-pinned local bytes against manifest quotes. It
    is not a fresh network check, and it establishes neither upstream freshness nor any team's practice.

## 7. Files this seat wrote

| path | what |
|---|---|
| `.ufo/waves/round-67/w1/ScribeF45/S100.txt` | the HTML capture (478 lines, 59068 bytes, sha256 `cf834a65…bff9f`) |
| `.ufo/waves/round-67/w1/ScribeF45/S101.txt` | the PDF capture (768 lines, 58889 bytes, sha256 `a55e315f…185bc8`) |
| `.ufo/waves/round-67/w1/ScribeF45/manifest-candidate.json` | candidate manifest, 50 quotes, passes the production `source-recheck.py` with exit 0 |
| `.ufo/waves/round-67/w1/ScribeF45/first-psirt-maturity-document.md` | draft knowledge entry (18 attributed claims, 8 package rules, 7 rejected readings, limits section) |
| `.ufo/waves/round-67/w1/ScribeF45/rows-draft.md` | README coverage-map row + Frontier F45 row + the prose paragraph, in the round-65 block shape |
| `.ufo/waves/round-67/w1/ScribeF45/sources-row-draft.md` | the two 11-column registry rows + the three registry-changes bullets |
| `.ufo/waves/round-67/w1/ScribeF45/NOTES.md` | this file |
| `.ufo/waves/round-67/w1/ScribeF45.md` | the seat report |

## 8. Tooling

**No tool was installed or upgraded in this seat.** The task needed only `python3 -B` (the host interpreter),
`curl`-equivalent `urllib` fetching through the lane's own `capture-source.py`, and `pdftotext`/`pdfinfo` from
the host's already-installed `poppler-utils` (`/usr/bin/pdftotext`, confirmed present before use). The
operator tooling directive was read (`/home/vgpnk/.omp/agent/RULES.md`) and no pacman transaction was filed or
executed; the host-wide pacman pause was not touched.
