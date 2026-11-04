# ScribeF45 — F45 coverage draft: FIRST's PSIRT Maturity document opened, captured and drafted

**Seat:** `ScribeF45` (scribe, leaf member — no subagent dispatch, no `task` call, no `agent://all` broadcast).
**Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
**Base revision at capture:** `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`.
**Run UTC:** 2026-11-04T20:52Z – 2026-11-04T21:0xZ.
**Round milestone:** predata multi-head SIGPIPE input-completeness repair + F45 PSIRT maturity screening.
**Scope:** **C2 (coverage) only.** C1 (the depth:verifiability multi-head SIGPIPE repair) is not this seat's scope.

---

## 1. Behavior — what this seat actually did

Independently opened and captured FIRST's PSIRT Maturity document with the lane's own instrument
(`corpus/instruments/capture-source.py`), then drafted, **from this seat's own capture bytes only**, the three
production artifacts the L1 is to land. **No production file was written.** `corpus/instruments/figure-audit.py`,
`corpus/ledger`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`, `SCORECARD.md`, `SKILL.md`,
`PROVINCE.md` and `LOG.md` are byte-unchanged. No commit, push, stash, checkout or mutating git/jj command was
run; the lane's git and jj state and the git index were not touched.

### 1.1 The capture (this seat's own, not ScoutF45's)

```
$ python3 -B corpus/instruments/capture-source.py --id S100 \
    --url "https://www.first.org/standards/frameworks/psirts/psirt_maturity_document" \
    --out <seat>/S100.txt --kind html
S100 status=200 fetched_bytes=82978 snapshot_bytes=59068 \
  sha256=cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f \
  utc=2026-11-04T20:52:02Z
```

```
$ python3 -B corpus/instruments/capture-source.py --id S101 \
    --url "https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Maturity_Document.pdf" \
    --out <seat>/S101.txt --kind pdf
S101 status=200 fetched_bytes=644190 snapshot_bytes=58889 \
  sha256=a55e315ffaeda54436d190ff0e77560224a2fd803f8f4a34f5adf90d01185bc8 \
  utc=2026-11-04T20:53:24Z
```

Committed receipts in this seat's directory: `S100.txt` (478 lines, 59068 bytes, sha256 `cf834a65…bff9f`,
content body L216-L464) and `S101.txt` (768 lines, 58889 bytes, sha256 `a55e315f…185bc8`; the PDF's raw bytes
are 644190 bytes, raw sha256 `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`, 29 pages,
`pdfinfo` CreationDate 2018-12-06).

**The PDF's raw digest reproduces the round-65 lead's recorded companion-PDF digest exactly.** The PDF URL
`.../psirts/FIRST_PSIRT_Maturity_Document.pdf` was found by probing, not by trusting the round-65 note; the
`/education/` form 404s.

### 1.2 The three drafted artifacts

| artifact | file | what it holds |
|---|---|---|
| (a) knowledge entry | `w1/ScribeF45/first-psirt-maturity-document.md` | H1 + `source:` (S100 **and** S101) + `verified-at:` + `recheck:` + `ground:` header; **18 attributed claims** (C1-C18) each with a ≤25-word verbatim quote and a line number; **8 falsifiable package rules**; **7 rejected readings**; a **scope-and-limits** section; 53 line-anchored quotes in total |
| (b) README rows | `w1/ScribeF45/rows-draft.md` | the exact 3-column **coverage-map row** and the exact 6-column **Frontier F45 row**, plus the prose paragraph that follows the Frontier table, all in the round-65 admission block's shape |
| (c) registry rows | `w1/ScribeF45/sources-row-draft.md` | the two **11-column** `corpus/SOURCES.md` registry rows (kind / tier / scope / anchor / teaches / status / opened / recheck / used-by) with `teaches` measured at 19 and 18 words (≤25 bound), plus the three `## Registry changes` bullets the L1 is to append |

### 1.3 Gates this seat actually exercised (all run, all reported as observed)

| gate | command | result |
|---|---|---|
| capture instrument | `capture-source.py --kind html` and `--kind pdf` | both exit 0; digests above |
| **production recheck on the candidate manifest** | `python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-67/w1/ScribeF45/manifest-candidate.json` | **54/54 quotes OK** (S100 × 44, S101 × 10), each `occurrences=1` with `anchor=N-ok`, plus 2 `sha256 OK` lines; **exit 0** |
| production recheck **fail-closed on an absent manifest** | same command with the manifest removed | `manifest UNAVAILABLE reason=missing`, recheck **rc=2**; `recheck-audit.py` reports `gated … FAIL`, **exit 1** |
| production recheck **fail-closed on a tampered capture** | one byte appended to `S100.txt` | `S100:sha256 MISMATCH expected=cf834a65… actual=b17f9c76…`, **rc=1** |
| production recheck **fail-closed on a forged quote** | a manifest quote replaced with a plausible-sounding sentence | `S100:M01-purpose-line MISMATCH reason=quote-not-found`, **rc=1** |
| production recheck **fail-closed on a non-unique quote with no anchor / with a broken anchor** | a phrase occurring twice, anchor dropped and set to 999 | `Z01-dup-noanchor MISMATCH reason=occurrence-not-unique`; `Z02-dup-broken-anchor MISMATCH reason=anchor-out-of-range`, **rc=1** |
| **production `recheck-audit.py`** on a scratch fixture carrying the draft entry + the two captures + the manifest | `python3 corpus/instruments/recheck-audit.py --root <fixture>` | `frozen=111 strict=111111 lane=0 foreign=0 executes PASS`; `strict pass=1/1 cdroot_fail=0 instrument_fail=0 own_fail=0`; **exit 0** |
| production `recheck-audit.py` **fail-closed** | same, with the manifest removed | `gated … FAIL`, `paths_fail=1`, **exit 1** |
| entry-quote fidelity (seat-local script) | every `"…" (S10x L<n>, N words)` span in the entry re-located in the named capture and re-counted | **53 quotes, 0 bad, 0 missing from the manifest** |
| lane instruments consulted | `source-recheck.py`, `recheck-audit.py`, `capture-source.py`, `anchorcheck.py`, `citation-ground-check.py`, `gate-quote-audit.py`, `density.py`, `QUALITY.md` Q1-Q9/R8/R12, `SOURCES.md` registry shape | read; no production mutation |

`recheck-audit.py` was run on a **scratch fixture** (`/fast/scratch/…/audittest/`) carrying the draft entry and the
two captures, with the entry's `cd` root rewritten to the fixture — because the audit requires the manifest
path to exist under the audited root, and the production snapshot directory does not exist until the L1 lands
it. That is a fixture, not a production run; the fixture was deleted with the scratch tree.

### 1.4 Body-scoped measurements (all over S100 content L216-L464)

`Maturity Level` 12 · `Level 4` **0** · `\bshall\b` **0** · `certif` **0** · `conform` **0** ·
`compliance` **0** · `\bMUST\b` 1 (L292) · `ISO/IEC 29147` 3 · `ISO 30111` 1 · `CVSS` 6 · `Bug Bar` 1 ·
`embargo` 1 · `reproduction` 3 · `charter` 7 · year tokens: `2013` only.

Over the **whole** S098 capture: `grep -c -iE "Maturity Level"` = **0** — so F45's level vocabulary is absent
from F44's source, and F44's own entry already says so.

Annex 7 per-level capability-area headings, counted from the capture's own heading lines: Level 1 = **5**
(L399, L404, L407, L410, L413); Level 2 = **7** (L419, L428, L432, L434, L437, L439, L442); Level 3 = **6**
(L446, L449, L453, L457, L460, L462). Level 3 names no Vulnerability Triage heading — measured, not assumed.

---

## 2. Gates and what the L1 must do

**Nothing below is done. The L1 lands every production byte.**

1. **Land the captures** as `corpus/source-snapshots/round-67/S100.txt` and `.../S101.txt`, with the manifest at
   `corpus/source-snapshots/round-67/manifest.json`. The stems **must** be `S100.txt` / `S101.txt`:
   `source-recheck.py` requires the capture stem to equal the record id (Q9 / B1). The candidate manifest is
   `w1/ScribeF45/manifest-candidate.json` and already passes the production instrument with exit 0.
2. **Land the entry** as `corpus/knowledge/first-psirt-maturity-document.md`.
3. **Add the entry path to `corpus/instruments/knowledge-expected.txt`** (a sorted list of `corpus/knowledge/*.md`
   paths) or `recheck-audit.py`'s expected-list check reports it unexpected.
4. **Land the two registry rows and the three registry-changes bullets** (drafts in `sources-row-draft.md`).
   Registry ids `S100`/`S101` are free at base (the highest row at base is `S099`). The sibling seat `ScoutF45`
   independently proposed `S100` for the same HTML capture with the same normalized digest — land **one** HTML
   row and **one** PDF row, not two rows for one document (R8).
5. **Land the README coverage-map row, the Frontier F45 row and the prose paragraph** (drafts in `rows-draft.md`).
6. **Land the entry's `recheck:` line** as drafted — it chains `--source S100` and `--source S101` against the
   round-67 manifest, the same shape as the multi-source entry
   `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:7`.
7. **Correct the round-65 lead line** (`corpus/SOURCES.md:244`) — see §3.1.

---

## 3. Findings

### 3.1 The round-65 lead records a digest that cannot be reproduced — it must be retired

The current lead line reads:
> "Lead added (round 65, not admitted): FIRST PSIRT Maturity document at … (HTTP 200, 82978 bytes, sha256
> `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e`; text carries "Maturity Level 1 (Basic)"
> through "Beyond Level 3")."

`334aeb01…` is a **raw-HTML** digest, and the page emits a per-response CSP nonce in four script attributes.
Measured here: six fetches (two user agents, three cache-busting query strings, one no-query fetch 65 s later)
produced **six distinct raw sha256 values at an identical byte length of 82978**. The byte-diff of two raw
responses is **exactly 84 differing byte positions in 4 runs of 21 bytes** (offsets 82449-82469, 82542-82562,
82634-82654, 82860-82880) and nothing but the nonce values. So the recorded raw digest is not re-derivable.

The reproducible anchors are the `capture-source.py` **normalized-text** snapshot digest
`cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f` — **identical across all six fetches** —
and the PDF's raw digest `f217c446…`, which reproduces the round-65 companion-PDF record exactly.

The lead's **factual** content is confirmed by this seat's own capture: the text does carry
"Maturity Level 1 (Basic)" through "Beyond Level 3". Only the digest is unusable. **Only the digest is
superseded — the lead's substance stands.**

### 3.2 The non-normativity notice lives in the PDF rendering, not the HTML one

The document's own cover states that the descriptions are "for informational purposes only" (S101 L8). The HTML
rendering of the same document does **not** carry that sentence (measured: `grep -c 'informational purposes'`
over S100 = 0, over S101 = 1). A package that quotes the disclaimer must cite the PDF capture; the draft entry's
C17 says exactly that and refuses the HTML attribution.

### 3.3 Three named levels, and a fourth heading with no content

`Level 4` occurs **0** times in the content body. "Beyond 'Level 3'" (S100 L353) is a heading whose entire body
is one rhetorical line (L354), with Annex 1 beginning at L355. The PDF carries the same heading at L587 with the
same single-line body. This entry therefore holds **three** levels and does not read "Beyond Level 3" as a
further level.

### 3.4 The overlap with F44/S098 is bounded, and the two documents are not interchangeable

The maturity document names a bug bar, isolated reproduction, the three organizational models and the
established-finder bypass — **all four also appear in S098**. The draft entry keeps the separation explicit:
each row states *this* document's wording and the rules section names which document owns the other claim
(qualification gate and reproduction duty → F44/S098; level structure and per-level capability → F45). The
maturity document itself defers its own glossary and supporting resources to the Services Framework (L356) and
attributes the Operational Foundations concept to it (L227), so it is not a substitute catalogue. The
per-level capability-area counts in C15 come from the Annex 7 checklist's own text heading lines, **not** from
the figures.

### 3.5 The figures cannot be read from either capture

Figures 1-3 are PNG images (`PSIRT-maturity/figure{1,2,3}.png`); the PDF renders the same diagrams as images.
`pdftotext` in plain **and** `-layout` mode yields **0** occurrences of the figure box labels
("Established Finders", "Internal Stakeholder Management", "USE CASE 1", "Service Area 1"). The per-level
service-area *listings* exist only in pixels. The draft entry makes **no claim about figure contents**; only the
captions and the PDF's Annex 2 illustration list (L596-L598) are cited. The PNG digests are recorded in
`NOTES.md` for the record but the images are **not** part of either committed capture.

### 3.6 A date cannot be asserted for the HTML page

The HTML content body carries one year token, `2013`, and it is the origin story at L220. The HTTP
`Last-Modified` header (2026-01-26) is a server header, not an edition. The PDF cover's `2019` (S101 L1) and
`pdfinfo`'s CreationDate (2018-12-06) belong to the PDF artifact and are reported as such. `verified-at` in the
draft entry is an **access date, not an edition**.

---

## 4. What this seat explicitly refuses to assert, and why

1. **That FIRST publishes a PSIRT maturity certification, rating or score.** The document's own notice says the
   descriptions are informational only (S101 L8); the term is "a profile of a product security team" (S100 L224);
   the content body has **0** `shall` / `certif` / `conform` / `compliance`. The single `MUST` (L292) is aimed
   at the team about its own foundations, not at a reader of the document.
2. **That a fourth level exists.** `Level 4` = 0 occurrences; "Beyond Level 3" is a heading plus one line.
3. **Any publication date for the HTML page.** §3.6.
4. **That the round-65 lead's raw digest is reproducible.** §3.1.
5. **Anything about the figures' contents.** §3.5.
6. **That the maturity document adds service-catalogue ground.** L356 and L227 defer it to the Services
   Framework; the catalogue, the qualification gate, the reproduction duty and the three organizational models
   stay with F44/S098.
7. **That any team operates at, or was assessed against, any level.** Nothing in either capture reports a
   team's level, an audit, an attestation or an outcome.
8. **That the document's ISO/IEC 29147 / ISO 30111 mentions state requirements.** They name them (3 and 1
   occurrences) as references; the requirements stay with F11.
9. **Fresh upstream verification.** The recheck compares digest-pinned local bytes against manifest quotes. It is
   not a fresh network check and establishes neither upstream freshness nor any team's practice.
10. **Any claim about the C1 SIGPIPE repair.** Not this seat's scope; the sibling seats own it and this seat
    changed no gate code.

---

## 5. Out of scope for this seat (not done, by design)

- **C1 / depth:verifiability**: the multi-head SIGPIPE input-completeness repair in
  `corpus/instruments/figure-audit.py` — the `cat_sigpipe_exempt` per-head input-count rule, the r66
  byte-identity constraint, the unknown-head residuals. Owned by `ExecMultiHeadGate`, `ExecMultiHeadProbes`,
  `ExecMultiHeadDriver`, `MutationMultiHead`, `ReviewMultiHead`, `CriticMultiHead`, `SentinelMultiHead`,
  `RevengerMultiHead`. This seat touched **no** gate code and ran **no** figure-audit probe.
- **The L1's production integration**: landing the captures, manifest, entry, `knowledge-expected.txt`, the two
  registry rows, the registry-changes bullets and the README rows.
- **The round-65 lead-line correction** — drafted here, landed by the L1.
- **Sibling coordination**: `ScoutF45` (capture/scout) and `ScopeF45` (coverage screen) ran independently. This
  seat did not read, copy or depend on `ScoutF45`'s capture bytes; this seat's `S100.txt` was fetched by this
  seat's own `capture-source.py` invocation, and the two independently produced the identical normalized digest
  `cf834a65…` — which is corroboration, not derivation.

---

## 6. Touched surfaces

| path | write? | what |
|---|---|---|
| `.ufo/waves/round-67/w1/ScribeF45/S100.txt` | **created** | this seat's HTML capture |
| `.ufo/waves/round-67/w1/ScribeF45/S101.txt` | **created** | this seat's PDF capture |
| `.ufo/waves/round-67/w1/ScribeF45/manifest-candidate.json` | **created** | candidate manifest, 54 quotes, passes production `source-recheck.py` with exit 0 |
| `.ufo/waves/round-67/w1/ScribeF45/first-psirt-maturity-document.md` | **created** | draft knowledge entry |
| `.ufo/waves/round-67/w1/ScribeF45/rows-draft.md` | **created** | README coverage-map row + Frontier F45 row + prose |
| `.ufo/waves/round-67/w1/ScribeF45/sources-row-draft.md` | **created** | the two 11-column registry rows + registry-changes bullets |
| `.ufo/waves/round-67/w1/ScribeF45/NOTES.md` | **created** | measurement receipts, refusals, file inventory |
| `.ufo/waves/round-67/w1/ScribeF45.md` | **created** | this report |
| `/fast/scratch/hyaku/kasegi-r67/ScribeF45/` | **created, then deleted** | scratch; all durable receipts copied out first |
| every production path (`corpus/instruments/figure-audit.py`, `corpus/ledger`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`, `corpus/instruments/knowledge-expected.txt`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `MANIFEST.json`) | **NOT written** | read-only; the L1 lands them |
| lane git / jj state, the git index, sibling lanes, the fleet repo | **NOT touched** | no commit, push, stash, checkout or mutating git/jj command |

---

## 7. Tooling

**No tool was installed or upgraded.** The task needed only `python3 -B` (the host interpreter), `urllib`
fetching through the lane's own `capture-source.py`, and `pdftotext` / `pdfinfo` from the host's already-present
`poppler-utils` (`/usr/bin/pdftotext`, confirmed present before use). `/home/vgpnk/.omp/agent/RULES.md` was read
first; the operator tooling directive is satisfied vacuously (nothing to install), and the **host-wide pacman
pause was not touched** — no pacman transaction was filed or executed, no `-Sy`/`-Syu`/`-U`/`-R`, no partial
upgrade, no host service restarted, and nothing created, modified or deleted in `~/.local/bin` or any other PATH
directory.

---

## 8. Artifact paths

```
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45/S100.txt
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45/S101.txt
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45/manifest-candidate.json
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45/first-psirt-maturity-document.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45/rows-draft.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45/sources-row-draft.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScribeF45/NOTES.md
```

Report path relative to the lane root: `.ufo/waves/round-67/w1/ScribeF45.md`.
