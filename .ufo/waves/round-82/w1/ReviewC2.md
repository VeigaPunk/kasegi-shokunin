# ReviewC2 — round 82 C2 review: F58 draft `corpus/knowledge/osv-high-quality-record-import-bar.md`

Scope: the draft entry against S116.txt and manifest; Distinctness against F31 (`osv-affected-range-events.md`) and F57 (`osv-importfindings-record-quality-feedback.md`); Not claimed and Limits commands; S116 row in SOURCES.md. Read-only. Receipts: `ReviewC2-receipts/checks.txt`.

## Verified (no defect)

- All six located quotes occur verbatim, once each, on the cited lines (25, 36, 41, 44, 47, 51). Word counts 12/23/6/10/19/13 match the gate table.
- The recheck line matches frozen B0/B5. `source-recheck.py` prints six OK lines and sha256 OK, exit 0. The r82 entry gate (G1–G5) passes, exit 0.
- Every `(S116.txt:n)` cite and the range cites (21, 22-23, 27, 28, 29-33, 37-55, 38-40, 45-46, 48-50, 52-55, 56-62, 63-86, 64, 86) point at the text described. The F31 cites S080.txt:760-766 are correct.
- The six rules follow from the page, and the rejected over-generalizations are not stated by it (Claims 1–6, apart from the items below). Bullet mapping on lines 42–51 is complete: 44, 47 and 51 are claimed; the rest are in Not claimed.
- Distinctness literal sweep: no hits for the six phrases outside the draft. F31 and F57 are described accurately, and the F57 Limits "navigation only" wording is matched.
- SOURCES.md S116 row: 11 cells, same as the S115 row. Status, date, recheck and used-by are correct, and the locator figures match the capture.

## Findings, by severity

### H1 — HIGH (verifiability): a stated grep does not do what the entry says
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:92` (Limits, bullet 1).
- **Evidence:** the entry says `grep -n -i -E 'IMPORT_FINDING|finding' corpus/source-snapshots/round-82/S116.txt` prints nothing and exits 1. It actually prints `7:GET /v1experimental/importfindings` and exits 0, because "finding" is a substring of "importfindings".
- **Replacement** (the command was run and prints nothing, exit 1):
  `- how OSV.dev enforces each property or which import finding a failure produces: \`grep -n -i -w -E 'IMPORT_FINDING|findings?' corpus/source-snapshots/round-82/S116.txt\` prints nothing and exits 1.`

### M1 — MEDIUM (claim accuracy, internal contradiction): title says "live" URLs
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:1`.
- **Evidence:** the title says "live reference URLs". Claim 6 (lines 53–59) and the page (S116.txt:51) bind the check to "the time of publication", and the entry says a link that breaks later does not fail the property. The title contradicts the entry's own rule. "GIT commits in the named repo" should also say "specified", the page's word (S116.txt:47).
- **Replacement line 1:**
  `# OSV.dev's import bar for an OSV record: the purpose, the schema-validation prerequisite, package-level precision as the minimum, distinct range ends, GIT commits in the specified repo, and reference URLs that answer 2xx or 3xx at publication`
- The G1 header gate reads lines 3–8 only, so this does not affect it.

### M2 — MEDIUM (attribution overclaim): "every claim is the page's own statement"
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:9`.
- **Evidence:** the falsifiable rules, the paraphrases, the rejected over-generalizations and the "Why it is bounty ground" paragraph (lines 11, 17, 19, 25, 27, 31, 35, 41, 43, 49, 51, 57, 59) are the entry's own reading. Some are labelled ("not a page sentence"), but the attribution says otherwise. The "Why" paragraph's GHSA example is not on the page at all.
- **Replacement for the sentence at line 9 that begins "Every claim below":**
  `Every quoted clause below is the page's own statement, quoted from the pinned capture \`corpus/source-snapshots/round-82/S116.txt\` with the line the text occupies; the paraphrases, falsifiable rules, rejected over-generalizations and the bounty-ground rationale are this entry's reading of those lines.`

### M3 — MEDIUM (provenance overreach): the link to "the quality bar" is inferred
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:9` (Attribution, first sentence).
- **Evidence:** the sentence "It is the document the importfindings page links as the quality bar (F57, ..., S115.txt:14)" treats a navigation-bar entry as the bar. S115.txt:14 is the nav link, and F57's own Limits calls it "navigation only". S115.txt:34 says "OSV.dev's quality bar" without naming a document.
- **Replacement for that sentence:**
  `It is the page the importfindings page lists in its navigation under the same title (F57, \`corpus/knowledge/osv-importfindings-record-quality-feedback.md\`, S115.txt:14, navigation only); that page does not name which document is "OSV.dev's quality bar" (S115.txt:34), so the identification rests on the matching title and is this entry's inference.`

### M4 — MEDIUM-LOW (paraphrase adds a rule the page does not state)
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:39` (Claim 4 paraphrase).
- **Evidence:** "describes no affected span" is not on the page. The page says only that introduced and fixed "can't be the same" (S116.txt:44).
- **Replacement for that sentence:**
  `A range whose introduced and fixed (or last_affected) values are the same version or commit is not distinct, and the page lists distinct ends as a property of a precise record (S116.txt:44).`

### L1 — LOW (rule text adds a field the page does not name)
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:49` (Claim 5 Falsifiable rule).
- **Evidence:** "the repo URL the range declares" maps the page's "specified repo" onto a range field. S116 names no field; the `repo` field belongs to F31 (S080.txt:788), which this entry does not cite here.
- **Replacement for the rule sentence:**
  `Falsifiable rule: a GIT range whose fixed commit lives only in a contributor's fork, not in the specified repo, breaks the commits-exist property (S116.txt:47). A reader checks it by reading the sixth bullet under Precise.`

### L2 — LOW (paraphrase adds an unstated contrast)
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:15` (Claim 1 paraphrase).
- **Evidence:** "not an ideal record" is a contrast the page does not draw. It says only "good enough".
- **Replacement for the paraphrase sentence:**
  `The page defines the "good enough" record that OSV.dev will import: what a record must carry for that import (S116.txt:25).`

### L3 — LOW (Not claimed inventory is incomplete)
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:69`.
- **Evidence:** the second sentence of the Valid paragraph, "It is also assumed that the vulnerability discussed in the OSV record is valid and affects the software described." (S116.txt:36), is on a cited line but is not in Not claimed.
- **Replacement:** insert, after `the consumer questions (S116.txt:38-40);`:
  ` the second sentence of the Valid paragraph, that the vulnerability is assumed valid and affects the software (S116.txt:36);`

### L4 — LOW (Distinctness gap: shared field name)
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:63–65` (Distinctness).
- **Evidence:** F31 Claim 1 (`corpus/knowledge/osv-affected-range-events.md:23`) holds the `schema_version` field's requirement above 1.0.0 (S080.txt:374-375). This entry's Claim 2 uses the same field, and no bullet says the two do not overlap.
- **Add as a new bullet after line 63:**
  `- F31 / S080 Claim 1 (\`corpus/knowledge/osv-affected-range-events.md:23\`) holds the schema_version field's requirement above 1.0.0 (S080.txt:374-375). This entry's Claim 2 uses the same field only to name the schema version a record is validated against (S116.txt:36) and claims nothing about its requirement.`

### N1 — NIT (illustrative example not on the page)
- **Path:** `corpus/knowledge/osv-high-quality-record-import-bar.md:33` (Claim 3 Falsifiable rule).
- **Evidence:** "names only a vendor or a product line" is an example the entry supplies. It is harmless but reads as the page's wording.
- **Optional replacement:** `Falsifiable rule: an advisory with no package an automated consumer can match is below the package-level floor the page sets (S116.txt:41). A reader checks it by reading the paragraph after the three consumer questions.`

## Residual risk and verification gaps

- The G5 content limb does not catch H1, M1–M4, L1–L2 or L4. Those are content defects and need the L1 to apply the fixes.
- Not checked: the instrument-level B1–B4, B6–B7 predicates (registry diff, knowledge-expected.txt, FRONTIER-CENSUS at landing). Those are not in this item's named commands and belong to the L1's landing run.
- After the fixes, the entry's G1 header and B8 gate should be re-run. Only the line-1 title and the body change, so the gate should still pass.

## Tooling

No tools installed or upgraded. Commands used were read-only: grep, sed, sha256sum, python3 (read-only JSON reads and the r82 gate and recheck instruments run as named). No git writes.

## Result

Six quotes, gate and recheck: pass. Content: 1 HIGH, 4 MEDIUM/MEDIUM-LOW, 4 LOW, 1 NIT. The L1 should apply H1, M1–M4 and L1–L4 before landing; N1 is optional.
