# Rows draft — README coverage map + Frontier F45 (ScribeF45, round-67 w1)

**Seat:** `ScribeF45` (scribe, leaf member). **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
**Base revision at capture:** `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`.
**Status:** DRAFT ONLY. The L1 lands these bytes into `corpus/README.md`. This seat wrote nothing into production.

The two tables below are in the exact shape of the round-65 admission block at `corpus/README.md:1035-1046`
(three-column coverage map, then the six-column Frontier table). Line numbers of the *source captures* are
S100/S101 line numbers, not README line numbers.

---

## 1. README coverage-map row (3-column table shape)

```markdown
| Area | Entry | Source basis |
|---|---|---|
| FIRST PSIRT maturity ladder: three named levels, the operational-foundations floor and the per-level capability checklist | knowledge/first-psirt-maturity-document.md | S100, S101, FIRST first-party maturity document (HTML page + PDF companion), opened 2026-11-04 |
```

## 2. Frontier F45 row (6-column table shape)

```markdown
| F45 | FIRST PSIRT Maturity Document — the maturity ladder for a product security team: three named levels (Basic, Intermediate, Advanced) over an operational-foundations floor, with the direction of travel from reactive to proactive, Level 2 gated on Level 1, and a per-level capability checklist that grows by service area | admitted | knowledge/first-psirt-maturity-document.md | S100, S101 | Read a maturity level as a capability profile a team selects, not a certification or a score: name the level, check the operational-foundations floor first, and treat the document's own "informational purposes only" notice as binding on every attribution. |
```

## 3. The prose paragraph that follows the Frontier table (round-65 block shape)

```markdown
F45 adds the level structure that F44 (S098) explicitly does not hold: measured over the whole S098 capture, `grep -c -iE "Maturity Level"` returns 0 and its only maturity definition is the glossary entry at L1510, so the three level names — "Maturity Level 1 (Basic)", "Maturity Level 2 (Intermediate)", "Maturity Level 3 (Advanced)" — and the "Beyond 'Level 3'" heading exist in no part of S098. F45 adds no new service catalogue: the document defers its own glossary and supporting resources to the PSIRT Services Framework (S100 L356) and names the Operational Foundations concept as the framework's (S100 L227), so the qualification gate, the reproduction duty and the three organizational models stay with F44/S098. The maturity document certifies nothing: its own PDF cover states the descriptions are "for informational purposes only" (S101 L8), and the content body carries zero occurrences of "shall", "certif", "conform" or "compliance" (measured over S100 L216-L464).
```

## 4. Notes the L1 must carry into the landing commit

1. **The round-65 lead line in `corpus/SOURCES.md` records a non-reproducible digest and must be corrected.**
   The current lead line (`corpus/SOURCES.md:244`) reads:
   > "Lead added (round 65, not admitted): FIRST PSIRT Maturity document at https://www.first.org/standards/frameworks/psirts/psirt_maturity_document — opened only for boundary screening this round (HTTP 200, 82978 bytes, sha256 `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e`; text carries "Maturity Level 1 (Basic)" through "Beyond Level 3")."

   The `334aeb01…` value is a **raw-HTML** digest. Measured in this seat: the page emits a per-response CSP
   nonce in four script attributes, so six fetches gave six distinct raw digests at an identical byte length
   of 82978; the byte-diff of two raw fetches is exactly 84 differing byte positions in 4 runs of 21 bytes
   (offsets 82449-82469, 82542-82562, 82634-82654, 82860-82880) and nothing but the nonce values.
   **The raw-HTML digest cannot be reproduced and must not be carried forward as an anchor.** The
   reproducible digests are the normalized-text snapshot `cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f`
   (identical across all six fetches) and the PDF's raw digest
   `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`, which **does** reproduce the round-65
   lead's companion-PDF record exactly. The lead's factual content ("text carries Maturity Level 1 (Basic)
   through Beyond Level 3") is confirmed by this seat's own capture; only the digest is unusable.
2. **The capture directory.** This seat's captures are at
   `.ufo/waves/round-67/w1/ScribeF45/S100.txt` and `S101.txt`. The L1 lands them as
   `corpus/source-snapshots/round-67/S100.txt` and `corpus/source-snapshots/round-67/S101.txt`, with the
   manifest at `corpus/source-snapshots/round-67/manifest.json` (candidate: `manifest-candidate.json` in this
   seat's directory; it already passes the production `source-recheck.py` with 50/50 quotes OK and exit 0).
   `source-recheck.py` requires the capture file stem to equal the record id (Q9 / B1), so the stems must be
   `S100.txt` and `S101.txt` — do not rename them.
3. **Registry ids.** `S100` and `S101` are this seat's proposal and are free at base (the registry's highest
   row at base is `S099`, the round-66 own-work diagnostic). The sibling seat `ScoutF45` independently proposed
   `S100` for the same HTML capture with the same normalized digest; the L1 must land **one** HTML record and
   **one** PDF record, not two rows for the same document. If the L1 prefers a single id, fold the PDF quotes
   into the `S100` record — but the `source-recheck.py` stem rule means the PDF capture then needs its own id
   and its own file, so two ids is the cleaner landing.
4. **`corpus/instruments/knowledge-expected.txt`** must gain the new entry path
   `corpus/knowledge/first-psirt-maturity-document.md`, or `recheck-audit.py`'s expected-list check will
   report it as unexpected. The file is a sorted list of `corpus/knowledge/*.md` paths.
5. **Figures are not in either capture.** Figures 1–3 are PNG images (`PSIRT-maturity/figure1.png`,
   `figure2.png`, `figure3.png`) and the PDF renders the same diagrams as images; `pdftotext` in plain and
   `-layout` mode yields zero occurrences of the figure box labels. The draft entry therefore makes no claim
   about figure contents, and the per-level capability-area counts are taken from the Annex 7 checklist's own
   text heading lines instead. If the L1 wants the diagrams as ground, that needs a separate image-grounding
   admission with its own digests — it is out of scope for this seat's draft.
