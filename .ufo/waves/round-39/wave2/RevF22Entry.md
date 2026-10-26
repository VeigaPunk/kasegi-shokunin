# RevF22Entry — wave-2 falsify receipt (round 39, hyaku run 9)

Seat: RevF22Entry (attack seat, leaf). Item: review the landed F22 knowledge entry
`corpus/knowledge/cisa-when-to-issue-vex.md`, the S057 row, and the rejected rows S056/S058/S059
against the committed capture and QUALITY Q1–Q10; run the S057 source-recheck; verdict ADMIT/REFUSE.
I did not author any bytes under attack (wave-1 authors: ScribeRowS057 / ScribeRowsRejected /
ExecFrontierCapture / entry scribe). All reads at lane HEAD `5006097` (round-39 receipt Y).

## Verdict: ADMIT

The entry, the S057 row and the three rejected rows withstand every attack I ran. Two minor
documentation-precision defects found inside the entry (D1, D2 below) — neither fails any
Q1–Q10 criterion; both are R9-class erratum material, not refusal grounds.

## Attack 1 — provenance is real, not just self-consistent (R21)

Re-fetched both URLs live (curl per seat rules; UA `kasegi-shokunin/1.0`), 2026-10-26T20:19:34Z:

```
HTTP=200 bytes=235270 final=https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf
cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99  pdf.bin      == manifest raw_sha256
HTTP=200 bytes=54453  final=https://www.cisa.gov/resources-tools/resources/when-issue-vex-information
4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d  landing.html == manifest landing_page.raw_sha256
```

Then reproduced the capture independently: `pdftotext -enc UTF-8 pdf.bin -` + an exact replica of
`capture-source.py collapse()` → `cmp` against the landed capture: **clean, byte-identical, 275
lines, 17,971 bytes, sha256 11c8d6d6…** — the landed S057.txt is a faithful conversion of the live
PDF, and the entry's `verified-at` narrative (HTTP 200, 235,270 B, sha256 cbcbd77a…) is confirmed
against today's live bytes. The entry's digest timestamp 19:31:07Z vs manifest `fetched_utc`
19:30:55Z is fetch-then-digest sequencing, consistent.

## Attack 2 — the recheck line (Q7/Q10/R12) and its fail-closed paths

`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057` → exit 0:

```
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
```

- Line form: one command, `cd <lane-root> &&` prefix, human note after `#`; `bash -n` clean; runs
  green from a foreign cwd (`cd / && bash recheck_line.sh` → exit 0). Q10 ✓.
- Output names what was checked and says so: "a pinned-capture comparison under whitespace
  collapse, not a fresh network check" — Q7's semantics sentence is accurate.
- Fail-closed controls (scratch fixtures, sha recomputed where the pin limb alone must fail):
  - missing manifest → `manifest UNAVAILABLE reason=missing`, **exit 2** ✓
  - corrupted capture (1-byte class of text mutated) → `S057:sha256 MISMATCH expected=11c8d6d6… actual=4b17f03d…`, **exit 1** ✓
  - moved quote (capture L133 deleted, manifest sha recomputed) → `S057:Q2 MISMATCH reason=quote-not-found`, **exit 1** ✓ (Q3/Q4 anchors correctly downgrade to `anchor=N-BROKEN` notes)
  The recheck note's claimed exit semantics (2 absent / 1 digest-or-move) reproduce exactly.
- R12: `--source S057` covers the header `source:` id; the manifest lists S057; binding check
  `records=46 bound=46 unbound=0` (round-39 record `url_bound=1 fetched=1`). ✓

## Attack 3 — every cited line resolves in the committed capture

I read all 275 capture lines and machine-checked every citation (scratch script, whitespace-collapse
matching, minimal-occurrence windows):

- **22 blockquote spans** (Claims 1–10): all verbatim under collapse, all distinct (22/22), word
  max = 25 (Claim 1's "Whether, and when…" = exactly 25), and **declared lines lie inside the
  occurrence for 22/22** — FC-1's headline `spans=22 distinct=22 words_max=25 anchors_ok=22 of 22`
  reproduces exactly.
- **30 inline quoted spans / 31 line refs**: all resolve in the capture; zero mis-quotes.
- Reader-direction nit (cosmetic, 3 cases): the occurrence extends 1–2 words onto the line *before*
  the declared start — Claim 3's "When the investigation has concluded…" (first two words end L133,
  declared L134–135), the Attribution "definitions of VEX data elements…" phrase (tail on L17,
  declared L16), Claim 3's "As the supplier refines…" ("As the" ends L99, declared L100–101). A
  reader starting at the declared first line still lands inside the quote; FC-1's stated direction
  (declared ⊆ occurrence) passes for all three.
- **FC-2…FC-6 all reproduce exactly**: `VEX=101 KEV=1 EPSS=0 SSVC=0 CSAF=0 CVSS=0 inherit=4
  action_statement=2 impact_statement=1 under_investigation=2 not_affected=3`; flag enum
  `component_not_present=1 vulnerable_code_not_present=1` + three zeros; `under_investigation` at
  L111+L133; `could be inherited downstream` at L190; `business decision` at L13+L80.
- S057 row's `-layout` cross-refs verified against my own `pdftotext -layout` of the re-fetched PDF:
  L19–20 business decision, L129 second business-decision sentence, L205–213 lifecycle+reaffirmation,
  L287–294 inheritance — all resolve.

## Attack 4 — overgeneralization, credentials, distinctness (Q4/Q5/Q6, item spec)

- **Guidance scope kept.** Every generalization is either quoted or labelled "Lane reading, not a
  quote"; the falsifiable rule and all 8 rejected over-generalizations each carry a capture-grounded
  reason; the Honest limit block states guidance-not-requirements, one-snapshot, no vendor practice.
  No sentence in the entry asserts a mandate the document does not make.
- **No credential material.** Scan of entry + capture for password/token/api-key/bearer/cookie/
  vault:///private-URL patterns: clean; capture URLs are all public cisa.gov links. Q6 ✓.
- **Distinct from S055/S053/S054 ground.** In the capture `EPSS=0 SSVC=0 CSAF=0 CVSS=0` — the
  entry never leans on the neighbours' vocabularies; corpus-wide, `reaffirm` and "when to issue"
  occur in exactly one knowledge file (this one), so the issuance/lifecycle/reaffirmation/
  inheritance layer is new ground vs S055 (document-content contract), S053 (EPSS likelihood),
  S054 (SSVC decisions). The "Sources overlap" section states the division correctly.

## Attack 5 — the S057 row and the rejected rows

- S057 row: `NF=13 cells=11 https_tokens=1` (the one https token = the manifest `url`, byte-bound
  by capture-binding-check B5); tier A, kind docs, status mined, opened 2026-10-26, recheck 180d,
  used-by path exists; **byte-identical to wave1 deliverable `wave1/ScribeRowS057.row.md`**.
- S056/S058/S059: `status rejected`, `flip:` tokens present in `teaches`, used-by `—`,
  **byte-identical to their wave1 deliverables**; every cited r38 digest (67bafe17…, 1e73325c…,
  9375415c…, ff875e45…, afb22b46…) occurs verbatim in `.ufo/waves/round-38/wave1/ScoutVexLeads.md`,
  and the rows' line locators match that ledger. Rejection reasons are sound: S056's vocabulary is
  the one S055's profile already mirrors; S058 is a community spec at a mutable `main` with no
  established v0.2.0 date (ledger confirms the revisions table ends 2023-07-18); S059 is a genuinely
  different vocabulary needing a scoped 6.4 MB-subtree capture. r38's rejection of S057 vs r39's
  admission is coherent (r38 scoped F21 to CSAF content; F22 is exactly the layer r38 said was
  "genuinely beyond" it).
- junk-f22 control is a real negative twin: 4 fabricated claims → 4× `MISMATCH
  reason=quote-not-found`, exit 1, with a positive control (real quotes, exit 0) and an isolation
  control (genuine sentences under the junk ids, exit 0) — rejection tracks content, not ids.

## Attack 6 — C2 counters at HEAD (supporting)

frontier rows 22; registry rows **59** (E1 corrected value; as-frozen 58 superseded); knowledge
files 51; entries citing S057: 1; harness `entries=25 pass=25 exit=0` (F22 row PASS);
`capture-binding-check.py` `records=46 bound=46 unbound=0`; `recheck-audit.py --quiet`
`expected=51 missing=0 unexpected=0 exit=0`. All green.

## Findings

**Minor (entry, erratum-class — do not flip the verdict):**
- **D1.** "Sources overlap" says "`KEV` once (L129)" — the capture has the literal `KEV` on **L130**
  (`(KEV) catalog.4`); L129 carries the spelled-out "Known Exploited Vulnerability". Off-by-one
  pointer on a non-load-bearing line ref (Claim 5's own L127–L130 pin is correct).
- **D2.** FC-1 claims "the **49** shorter inline quotes resolve the same way" — not reproducible
  from the landed bytes: a pair-aware count finds **43** resolving inline quoted spans in the body
  (51 quoted spans total, 8 being the deliberately-non-capture rejected-over-generalization labels),
  44 including the H1 title quote. The substantive claim (every inline quote resolves — zero
  failures) holds; the figure 49 matches no natural counting I tried. R19-class unreproducible
  specimen figure.

**Observations (adjacent landed bytes, not the entry/rows):**
- The round-39 lesson's quote list labels "Q2 `:79-81`" (business decisions) — the manifest's Q2 is
  the lifecycle pin (anchor 132, L132–134); the 79–81 quote is quoted in the entry (Claim 1) but is
  not one of the four manifest pins. Lesson-level labeling drift only; lesson Q3/Q4 correspond.
- Three citations' occurrences extend 1–2 words onto the line before the declared start (Attack 3
  reader-direction nit) — cosmetic, passes FC-1's stated direction.

## Residual risk / verification gaps

- The capture's fidelity is now double-verified (wave-1 re-open + my independent re-fetch and
  pdftotext reproduction), but cisa.gov can republish/replace the PDF at any time — the 180d
  recheck cadence and the manifest's raw_sha256 are the tripwires; a changed upstream digest is a
  new pin, not a correction (the entry's Honest limit already says this).
- I did not re-verify the r38 ScoutVexLeads fetches themselves (only that the landed rows' digests
  occur verbatim in that committed receipt) — the rejected rows make no capture claim, so nothing
  hangs on them beyond the ledger.
- Tooling: no installs or upgrades were needed (pdftotext already present at /usr/bin/pdftotext;
  all other work used stock python3/curl/git). Nothing to record under the 2026-10-19 tooling
  authorization.

Scratch `/fast/scratch/hyaku/kasegi-r39/RevF22Entry/` removed before yield; no other file in the
lane tree, fleet root, or sibling repos was written.
