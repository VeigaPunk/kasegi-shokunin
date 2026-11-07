# ISO/IEC 29147/30111 standard records — the standards-body publisher record of the CVD process standards: identity/editions, publisher status and the to-be-revised stage, the currency statements, the abstract's own division-of-labour sentence, and vendor-side applicability

source: S089 — https://www.iso.org/standard/72311.html — capture corpus/source-snapshots/round-57/S089.txt (6647 snapshot bytes over 88964 fetched; sha256 17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd; recorded fetch 2026-11-03T18:04:24Z, HTTP 200; two same-sha opens this round — recorded + verification re-open, byte-identical after the declared conversion; title L1, abstract scope L84, 30111 cross-reference L91, applicability L92, stage L99, currency L64, successor AWI L204); manifest corpus/source-snapshots/round-57/manifest.json (7 assertions Q1-Q7, each occurrences=1 at its anchor)
source: S090 — https://www.iso.org/standard/69725.html — capture corpus/source-snapshots/round-57/S090.txt (5598 snapshot bytes over 87845 fetched; sha256 2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a; recorded fetch 2026-11-03T18:04:24Z, HTTP 200; two same-sha opens this round; title L1, abstract L84, applicability L85, stage L92, currency L64, successor WD 30111.2 L197, review cadence L109); manifest corpus/source-snapshots/round-57/manifest.json (7 assertions Q1-Q7, each occurrences=1 at its anchor)
verified-at: 2026-11-03 (opened this round; the catalog pages are dynamic publisher pages — byte-stability is asserted within this round's two same-sha opens only, and the 90d row recheck re-fetches)
ground: F38
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S090   # run from any cwd (the cd prefix names the lane root); prints one sha256 OK + one Q-OK line per pinned quote per source with its occurrences= count and anchor note; exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

ISO's own catalog records — the publisher's statement of its own standards: what each document
is, which edition stands, its publication and review status, and (in the abstracts) the scope
ISO claims for it. This entry is documentation-only: it instructs no probing, scanning, login or
submission against any target, carries no credential material, and asserts nothing about the
paywalled normative text of either standard.

## Claim 1 — the records pin identity and edition: 29147:2018 edition 2 and 30111:2019 edition 2

The served records state ISO/IEC 29147:2018 (`corpus/source-snapshots/round-57/S089.txt:52`), titled "Information technology — Security techniques —
Vulnerability disclosure" (`corpus/source-snapshots/round-57/S089.txt:1` Q1; again `corpus/source-snapshots/round-57/S089.txt:53`), edition 2 (`corpus/source-snapshots/round-57/S089.txt:54`), publication date 2018-10 (`corpus/source-snapshots/round-57/S089.txt:97`), reference 72311 (`corpus/source-snapshots/round-57/S089.txt:59`), 32 pages (`corpus/source-snapshots/round-57/S089.txt:103`; the abstract's scope sentence at S089.txt:84 Q2, the 30111 cross-reference at S089.txt:91 Q3) and ISO/IEC 30111:2019 (`corpus/source-snapshots/round-57/S090.txt:52`), titled "Information technology — Security techniques — Vulnerability handling processes" (`corpus/source-snapshots/round-57/S090.txt:1` Q1; again `corpus/source-snapshots/round-57/S090.txt:53`), edition 2 (`corpus/source-snapshots/round-57/S090.txt:54`), publication date 2019-10 (`corpus/source-snapshots/round-57/S090.txt:90`), reference 69725 (`corpus/source-snapshots/round-57/S090.txt:59`), 13 pages (`corpus/source-snapshots/round-57/S090.txt:96`; the abstract's scope sentence at S090.txt:84 Q2). Both carry
the same technical committee (ISO/IEC JTC 1/SC 27, `corpus/source-snapshots/round-57/S089.txt:105`, `corpus/source-snapshots/round-57/S090.txt:98`) and ICS 35.030 (`corpus/source-snapshots/round-57/S089.txt:107`, `corpus/source-snapshots/round-57/S090.txt:100`) in the served general-information
blocks, and ISO's own review machinery is printed on the page: "A standard is reviewed every 5
years" (S090.txt:109 Q7). Falsifiable rule: a claim that a different edition of either standard is
the published one (for example "29147:2022") contradicts these records as served on the recorded
fetch date. Rejected over-generalizations: the page furniture "© ISO 2026" is site copyright
chrome, not an edition date; the CHF prices (179 / 135) are store state at the fetch instant, not
asserted market data; and the life-cycle tables' earlier stage dates are history, not the current
state.

## Claim 2 — both editions are Published and confirmed current while BOTH stand at stage "to be revised", with successor work named

Each record carries the paired status facts side by side: "Status : Published" with stage
"International Standard to be revised [90.92]" (S089.txt:99 Q5; S090.txt:92 Q4), a currency
statement — "This publication was last reviewed and confirmed in 2024." (S089.txt:64 Q6) and
"... in 2025." (S090.txt:64 Q5) — and successor work named in the life-cycle's "Will be replaced
by / Under development" block: "ISO/IEC AWI 29147" (S089.txt:204 Q7) and "ISO/IEC WD 30111.2"
(S090.txt:197 Q6). Falsifiable rule: a reader citing either edition as final/stable ignores the
printed stage; a reader citing a newer PUBLISHED edition contradicts the printed status — the
successor documents are development states (AWI / WD), not published editions. Rejected
over-generalizations: the semantic meaning of stage codes beyond the page's own gloss ("90.92
(To be revised)" is printed; the rest of the numeric ladder is shown only as life-cycle labels),
and any claim about the successor drafts' content or dates (they are named, not opened).

## Claim 3 — the publisher's own division-of-labour sentence separates disclosure (29147) from handling (30111)

ISO's abstract for 29147 scopes it to "requirements and recommendations to vendors on the
disclosure of vulnerabilities in products and services" (S089.txt:84 Q2) and states the split in
one sentence: "Other related activities that take place between receiving and disclosing
vulnerability reports are described in ISO/IEC 30111." (S089.txt:91 Q3). ISO's abstract for 30111
scopes it to "requirements and recommendations for how to process and remediate reported potential
vulnerabilities in a product or service" (S090.txt:84 Q2). Falsifiable rule: a reader swapping the
two roles — citing 29147 for handling/remediation duties or 30111 for the vendor's disclosure
conduct — contradicts the publisher's own words. Kept distinct from F11: the JPCERT/CC 2026
P-guideline (S041) is a THIRD PARTY's reading of the same pair; this claim is the publisher's own
one-sentence version, first-party at the source. Rejected over-generalization: the abstracts'
wording is the catalog record's, not the normative clauses' — clause-level division of labour
stays F11/S041 ground and is not re-asserted here.

## Claim 4 — applicability is vendor-side, and choosing is 29147's own verb

The records address vendors on both sides of the pair: "This document is applicable to vendors who
choose to practice vulnerability disclosure to reduce risk to users of vendors' products and
services." (S089.txt:92 Q4) and "This document is applicable to vendors involved in handling
vulnerabilities." (S090.txt:85 Q3). Falsifiable rule: a reader citing either standard as a duty
binding the FINDER's disclosure conduct over-generalizes the records — the addressed party is the
vendor, and 29147's applicability sentence itself carries the verb "choose". Rejected
over-generalization: "vendors must follow ISO/IEC 29147" — the record says "vendors who choose to
practice"; nothing on these pages mandates adoption, and any per-vendor mandate lives in the
vendor's own policy (F10 ground).

## Distinctness

- vs F11/S041 (the JPCERT/CC 2026 P-guideline): F11 is a national CSIRT's implementation guideline
  reading of the two standards (division paragraph, 図1); F38 is the publisher's own catalog
  record — identity, edition, status, stage, applicability and the abstract's split sentence. The
  S041 ground is unchanged; the pre-freeze screen shows S041 among the citing captures, not a
  holder of this ground.
- vs F10/S040 + the crosswalk entry (vendor disclosure policies): those hold what VENDOR policies
  commit to (Cisco's policy cites ISO/IEC alignment); F38 holds the standards' own publisher
  records. A vendor's claim to follow 29147 is F10 evidence; what ISO says 29147 IS, is this row.
- vs F12/S042 (the Japanese state-coordinated workflow) and F14 (Japanese severity vocabulary):
  national implementation surfaces, not the standards' publisher records.
- vs F02 (coordinator disclosure timelines, ZDI) and F27 (the kernel reporting process): specific
  coordinator/project processes; F38 is the standards-body record of the general process standards.
- Downstream-consumer sweep (pre-freeze receipt limb 4): the snapshots naming the standards
  (S003, S018, S021, S039, S040, S041, S055, S063) are consumers citing the standards; none is a
  capture of the iso.org catalog pages.

## Limits

The normative text of both standards is paywalled and stays unasserted — these records are the
catalog layer only (abstracts, metadata, life cycle). The pages are dynamic publisher pages:
byte-stability was measured WITHIN this round (two same-sha opens per source after the declared
conversion; two raw HTML opens each) and no cross-day stability is claimed; the 90d row recheck
re-fetches, and a moved stage, a published successor edition, or a changed abstract is a DIFFERENT
record state that supersedes by a new row (R8). Prices, language editions (English/French listed),
the OBP "Read sample" surface, the successor drafts' content (AWI 29147, WD 30111.2) and the
French-language pages are unopened/unasserted. Capture-method limit, disclosed: the committed
instrument's urllib open is HTTP-403-blocked by www.iso.org (both URLs, observed 2026-11-03); the
recorded opens used curl with the instrument's own UA string plus the instrument's own html_to_text
conversion (unmodified import) — the failed instrument invocation is the disclosure of record, and
a future recheck via the unmodified instrument may need the same disclosed workaround. No call was
made against any vendor, coordinator or program; the capture is a public catalog read, and
submission/testing remains refused by the province.
