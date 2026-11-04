# Registry-row draft — `corpus/SOURCES.md` (ScribeF45, round-67 w1)

**Seat:** `ScribeF45` (scribe, leaf member). **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
**Base revision at capture:** `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`.
**Status:** DRAFT ONLY. The L1 lands these bytes into `corpus/SOURCES.md`. This seat wrote nothing into production.

The registry table at `corpus/SOURCES.md:5-7` is an 11-column table:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

Both rows below are in that shape. `teaches` is measured at **≤25 whitespace-delimited words** (the lane's
`gate-quote-audit.py` bound); the measured count is given under each row.

---

## 1. Row S100 (the HTML page named in the wave spec)

```markdown
| S100 | FIRST PSIRT Maturity Document — https://www.first.org/standards/frameworks/psirts/psirt_maturity_document | docs | A | FIRST's own maturity ladder for a product security team: three named levels (Basic, Intermediate, Advanced) over an operational-foundations floor, with per-level capability expectations — not a certification and not a score | Maturity Level 1 (Basic) L218; Maturity Level 2 (Intermediate) L285; Maturity Level 3 (Advanced) L318; Beyond "Level 3" L353; Annex 7 Sample Checklist L397; capture corpus/source-snapshots/round-67/S100.txt (sha256 cf834a65...bff9f, 478 lines, 59068 bytes, content L216-L464; no publication date in the body; HTTP Last-Modified 2026-01-26) | A maturity level is a capability profile a team selects, not a certification: name the level, then check the foundations floor before calling it met. | mined | 2026-11-04 | 180d | corpus/knowledge/first-psirt-maturity-document.md |
```

- `teaches` measured word count: **19** (whitespace-delimited).
- `kind` = `docs` (FIRST's own publication), `tier` = `A` (primary first-party), `status` = `mined`,
  `opened` = `2026-11-04` (this seat's own capture date), `recheck` = `180d` (tier-A documentation cadence —
  the page states no publication date and its prose is mutable, the same reasoning the round-65 correction
  applied to S098), `used-by` = the new F45 entry only.

## 2. Row S101 (the PDF companion — the durable artifact)

```markdown
| S101 | FIRST PSIRT Maturity Document, PDF — https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Maturity_Document.pdf | docs | A | The same maturity document in its PDF rendering, which carries the document's own non-normativity notice and its date; the durable, byte-reproducible artifact | Cover notice L8; Maturity Level 1 (Basic) L61; Level 2 L285; Level 3 L444; Beyond "Level 3" L587; Annex 7 Sample Checklist L698; capture corpus/source-snapshots/round-67/S101.txt (sha256 a55e315f...185bc8, 768 lines, 58889 bytes; raw PDF 644190 bytes, raw sha256 f217c446...59a31f, 29 pages, pdfinfo CreationDate 2018-12-06) | FIRST's non-normativity notice is the document's own: the descriptions are informational only, and the maturity ladder certifies nothing. | mined | 2026-11-04 | 180d | corpus/knowledge/first-psirt-maturity-document.md |
```

- `teaches` measured word count: **18**.
- The PDF's raw digest `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f` **reproduces the
  round-65 lead's recorded companion-PDF digest exactly** (644190 bytes, 29 pages). This is the one artifact of
  the pair whose *raw* bytes are stable.

## 3. Registry-changes bullets the L1 is to append

Appended at the end of the `## Registry changes` section (`corpus/SOURCES.md:164`), in the bullet shape the
existing entries use:

```markdown
- Round-67 S100 added (docs, scoped tier A, mined, opened 2026-11-04, recheck 180d, used-by corpus/knowledge/first-psirt-maturity-document.md); anchor pinned to the round-67 capture corpus/source-snapshots/round-67/S100.txt (sha256 cf834a65...bff9f, 478 lines, 59068 bytes, content L216-L464; level headings L218/L285/L318, "Beyond Level 3" L353, Annex 7 checklist L397). Registry 99 rows pre-append -> 101 post-append (R8); no pre-existing status, recheck, used-by, id or URL cell changed.
- Round-67 S101 added (docs, scoped tier A, mined, opened 2026-11-04, recheck 180d, used-by corpus/knowledge/first-psirt-maturity-document.md); anchor pinned to the round-67 capture corpus/source-snapshots/round-67/S101.txt (sha256 a55e315f...185bc8, 768 lines, 58889 bytes; raw PDF 644190 bytes, raw sha256 f217c446...59a31f, 29 pages; cover notice L8, level headings L61/L285/L444, "Beyond Level 3" L587, Annex 7 checklist L698). The PDF's raw digest reproduces the round-65 lead's recorded companion-PDF digest exactly.
- Lead retired (round 65 -> round 67): the round-65 lead line for FIRST's PSIRT Maturity document at https://www.first.org/standards/frameworks/psirts/psirt_maturity_document is now admitted as S100 (HTML) and S101 (PDF). Its recorded raw-HTML sha256 `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e` is NOT reproducible and is not carried forward: the page emits a per-response CSP nonce in four script attributes, so six fetches in round 67 gave six distinct raw digests at an identical byte length of 82978 (byte-diff of two raw fetches: 84 differing byte positions in 4 runs of 21 bytes, offsets 82449-82469, 82542-82562, 82634-82654, 82860-82880 — the nonce values only). The reproducible digest is the capture-source.py normalized-text snapshot sha256 cf834a65...bff9f, identical across all six fetches. The lead's factual content ("text carries Maturity Level 1 (Basic) through Beyond Level 3") is CONFIRMED by the round-67 capture; only the digest is superseded.
```

## 4. Notes the L1 must carry into the landing commit

1. **Id choice.** `S100` and `S101` are free at base (the registry's highest row at base is `S099`, the round-66
   own-work diagnostic). The sibling seat `ScoutF45` independently proposed `S100` for the same HTML capture
   with the same normalized digest `cf834a65…`. The L1 lands **one** HTML row and **one** PDF row; two rows
   for the same HTML document would violate R8.
2. **The stem rule forces two ids.** `source-recheck.py` requires the capture file stem to equal the record
   id (Q9 / B1 in `corpus/QUALITY.md`). The PDF is a separate capture file, so it needs its own id and its own
   file. Land them as `corpus/source-snapshots/round-67/S100.txt` and `.../S101.txt` with the manifest at
   `corpus/source-snapshots/round-67/manifest.json`.
3. **Candidate manifest already verifies.** `manifest-candidate.json` in this seat's directory passes the
   production instrument: `python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-67/w1/ScribeF45/manifest-candidate.json`
   → 50/50 quotes OK (S100 × 40, S101 × 10), every one `occurrences=1` with `anchor=N-ok`, **exit 0**.
   The L1 can land that manifest with the id/path rewrites to the production snapshot directory.
4. **Do not carry `334aeb01…` forward.** It is a raw-HTML digest over a nonce-bearing response. See bullet 3
   above for the measurement and the replacement digest.
5. **No `used-by` cell on any other row changes.** S098's `used-by` stays
   `corpus/knowledge/first-psirt-services-framework.md`; the two documents are different sources and F45's
   entry cites S098 only for boundary statements, never for a load-bearing claim.
