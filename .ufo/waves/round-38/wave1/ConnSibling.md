# ConnSibling — round 38 wave 1 (connector seat: sibling-overlap ruling for F21/S055 + province fit)

Seat id: `ConnSibling` (leaf connector; no subagent dispatch; no `agent://all`). Assignment: combine
this seat's own sweep (grep the 20 sibling lanes' corpus/SKILL/PROVINCE for `CSAF|VEX|product_status`)
with the facts (kake owns security.txt publishing; `kake-shokunin/corpus/knowledge/security-txt-publishing.md:63`
names `CSAF` as a security.txt extension field) and rule on (1) F21/S055 contested scope —
uncontested / adjacent / contested — and (2) the F21 entry's province fit against the `PROVINCE.md`
Core ("program rules, triage and claim gates, submission/disclosure packaging"). Receipt only.

Object state at this seat's run time (read-only; lane HEAD `700153593eb586c70a6499c8ca225ee4d673bc9b`,
claims frozen at `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`): `claims.json` C2 predicate admits frontier
F21 (OASIS CSAF v2.0 — the VEX profile's product-status categories and machine-readable not-affected
justification flags, "distinct from CVSS severity, KEV status, EPSS likelihood and SSVC decisions")
20→21 with registry row S055; a `corpus/knowledge/csaf-vex-product-status-and-justifications.md`
entry, S055 capture and junk twin are in flight in sibling seats (`ScribeRowS055`, `ScribeEntryF21`,
`ExecC2Capture`, `ExecC2Junk`). Absent-at-run-time is expected, not a defect; this ruling is about
scope, not about landed bytes. No `wave1/ConnSibling.md` existed at write time (ls count 0).

## Sources consolidated

| source | verdict label | load-bearing content |
|---|---|---|
| this seat's sweep — item-mandated surface (`\bCSAF\b|\bVEX\b|product_status` over each of the 20 sibling lanes' `corpus/`, `SKILL.md` (where present), `PROVINCE.md`) | ADJACENT / UNCONTESTED | exactly ONE hit in the whole surface: `kake-shokunin/corpus/knowledge/security-txt-publishing.md:63` — "securitytxt.org already lists one extension, `CSAF` (S079)". Zero `product_status` tokens and zero standalone `VEX` tokens anywhere in the 20 siblings |
| extra probe A — `Vulnerability Exploitability eXchange|not_affected|not-affected` over the same 20-lane surface | 0 hits | the spelled-out VEX phrase and the not-affected flag forms appear nowhere in sibling corpora |
| extra probe B — `\bCSAF\b|\bVEX\b|product_status` over `/home/vgpnk/Projects/shokuknow/doctrine/` | 0 hits | shokuknow doctrine carries zero CSAF/VEX/product_status rows |
| extra probe C — kake whole-repo `git grep` (tracked) for `csaf|vex|product_status` | kake's CSAF footprint is its round-35 security.txt evidence | hits confined to `.ufo/waves/round-35/` security.txt-publishing artifacts: `census.json:416,430,440-441` (CSAF field with value `https://msrc.microsoft.com/csaf/provider-metadata.json`), `census/www.microsoft.com.body:24-25` (`CSAF: https://msrc.microsoft.com/csaf/provider-metadata.json`), `ScoutSecurityTxtCensus.md:30`, `ScribeEntryDraft.md:22`, `ReviewEntryRfcFacts.md:31`, `ReviewProbeMatchesTruth.md:38`; the rest are base64/URL-fuzz control-fixture substrings (no semantics). The knowledge entry's only CSAF sentence is `security-txt-publishing.md:63` |
| extra probe D — sibling registry `S055` in each lane's `corpus/SOURCES.md` | lane-local ids | 14 sibling lanes already carry their own S055 row (chousa, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, mado, mori, souji, tabi, tameshi, tsukuroi); registries are per-lane, so kasegi's S055 admission collides with nothing fleet-wide |
| in-lane prior occupancy — kasegi corpus grep for `\bCSAF\b|\bVEX\b` | capture-level presence, zero knowledge entries | verbatim mentions in committed captures: `source-snapshots/round-24/S001.txt:1122-1123` ("Minimum Requirements for Vulnerability Exploitability eXchange (VEX)"), `S003.txt:286-293` ("Publish advisories using the Common Security Advisory Framework (CSAF) … 13 See Common Security Advisory Framework (CSAF) for more information"), `source-snapshots/round-25/S040.txt:239-240,269-283,354-358` (VEX document row; "RSS, CSAF" availability rows; "CSAF is an industry standard designed to depict vulnerability information in machine-readable format"), `round-26/S040-live.txt` same. No `corpus/knowledge/*.md` entry covers CSAF/VEX today |
| `claims.json` (frozen) | canonical assignment | C2 predicate text for F21/S055 quoted verbatim in the header; `kake` fact given in the item spec |

## Q1 — Is F21/S055 contested? ADJACENT (one fellow-lane touch) / otherwise UNCONTESTED; not contested

- **Sweep result.** On the item-mandated surface (20 siblings × corpus/SKILL/PROVINCE), the only
  occurrence of the three tokens is kake's `security-txt-publishing.md:63`. That line states a
  security.txt *field-registry* fact: per securitytxt.org (S079), `CSAF` is the one extension field
  IANA-style registries list, alongside the rule that unknown fields are ignored (S078). It is a
  statement about the field *name* in a security.txt file — the pointer a publisher puts in the file
  — not about CSAF v2.0's internal schema.
- **kake's own scope line.** kake's `PROVINCE.md` Core is web properties & publishing; its round-35
  frontier step explicitly declares its boundary: "Vulnerability handling itself stays out of
  province: report intake, triage, remediation, disclosure timing, bounty and policy operation, and
  whether any named contact channel works, are not kake's ground" (round-35 section). kake's CSAF
  touch is therefore a *publication-channel* artifact (where the field lives, what its value URI
  points at), and kake itself disclaims the vulnerability-handling semantics that F21 occupies.
- **No competing ground.** No sibling registry row, knowledge entry, SKILL.md or PROVINCE.md claims
  the VEX profile's product-status categories or the machine-readable not-affected justification
  flags; no sibling has any `product_status` token; none of the 20 sibling lanes contests, assigns,
  or partially overlaps the F21 standard-content ground.
- **Id note.** S055 is lane-local: siblings hold their own S055 rows (14 observed) and kasegi's S055
  admission is independent. No fleet-wide source-id ledger exists, so no id collision is created or
  resolved by this ruling.

**Q1 ruling: adjacent (kake field-pointer touch; reported, not absorbed) and otherwise uncontested.**
The only cross-lane contact is kake's security.txt extension-field mention; it is evidence-shaped
(field syntax / publication channel), not scope-shaped (standard content). Per `PROVINCE.md` Adjacent
("Sibling lanes are reported, not absorbed") and `PROTOCOL.md:457-461`, the correct disposition is a
report, not an absorption: kake stays the owner of security.txt field placement; kasegi takes the
CSAF v2.0 standard-content ground.

## Q1b — Nearest-neighbour disposition: kake security.txt CSAF field — REPORT, NOT ABSORBED

kake's CSAF sentence sits inside its security.txt publishing entry (S078/S079-grounded). Its round-35
census recorded `CSAF` as a served field on `www.microsoft.com` with value
`https://msrc.microsoft.com/csaf/provider-metadata.json` (evidence files above). That is the *pointer*
to provider metadata — the publication-channel half of CSAF — never the standard's vocabulary.
F21/S055 is the CSAF v2.0 standard itself (OASIS Standard): the VEX profile's product-status
categories and the machine-readable not-affected justification flags a vendor publishes. Same acronym
family, different object class: field-name pointer vs standard content schema. Disposition: **reported
in this ruling and available to the L1 as a round-38 lesson note ("not absorbed" lead); not absorbed
into kasegi's corpus, not cited by the F21 entry, not a registry row.** No `PROVINCE.md` refinement
is required; the adjacency is evidence-shaped, not scope-shaped.

## Q2 — Province fit of the F21 entry: FITS, no re-scope

- **Domain line.** `PROVINCE.md:3` — "bounty & security research — scopes ~/Projects/bounties,
  program rules, claim packages". Core (`PROVINCE.md:27-33`): "the line-3 domain comprises program
  rules, scopes, and claim packages; the core also covers triage and claim gates, and
  submission/disclosure packaging." CSAF v2.0's VEX profile is the machine-readable packaging vendors
  publish for per-product vulnerability status (affected / not_affected / … and the justification
  flags that make "not affected" machine-checkable). That is disclosure packaging craft — the exact
  surface the Core owns — applied to the claims the lane triages (F02/F03/F06/F10/F11/F15).
- **The F10→F11→F18→F19→F20 precedent ladder.** F10 (vendor-side disclosure policies as corpus
  objects; the row itself reads "the standard edition it names" — CSAF is exactly such a standard
  edition), F11 (ISO/IEC 29147/30111 division-of-labour), F15 (vendor research programme as intake),
  F18 (CISA KEV), F19 (FIRST EPSS), F20 (SSVC). F21 is the next rung: after severity (F13/F17),
  exploitation status (F18) and likelihood (F19) and stakeholder prioritization (F20), the vendor's
  machine-readable advisory format answers *how a vendor states per-product status in a format a
  consumer can automate* — the disclosure-language axis the ladder has not yet indexed. The frozen
  claim itself distinguishes F21 from CVSS severity, KEV status, EPSS likelihood and SSVC decisions,
  matching the per-row "distinct from" discipline of F18/F19/F20.
- **Prior occupancy of the same vocabulary.** In-lane captures already name CSAF and VEX verbatim:
  S001.txt (FIRST CVSS v4.0 user guide: VEX "affected" status reference), S003.txt (CISA CVD
  program: "Publish advisories using the Common Security Advisory Framework (CSAF)"), S040.txt /
  S040-live.txt (Cisco: VEX document rows, "RSS, CSAF" availability, "CSAF is an industry standard
  designed to depict vulnerability information in machine-readable format"). Novelty of S055 is
  **standard-level** (first OASIS CSAF v2.0 methodology ground, first knowledge entry), never
  concept-level or vocabulary-level.
- **Consequence for C2 scoring (stated, not enacted).** The coverage claim should be phrased as a
  frontier opening over already-present adjacent ground: first CSAF/VEX methodology ground in the
  registry (genuinely new row + entry). Risk is **under-credit, not collision**. No province re-scope
  is implied or needed; the entry grounds solely on kasegi's own S055 capture.

## Caveats consolidated

- **A (kake phrasing).** Cite `security-txt-publishing.md:63` exactly: the sentence reports a
  field-registry fact (S079). Never read kake as owning CSAF ground, and never read kake as
  contesting it: kake's own PROVINCE.md disclaims vulnerability-handling semantics entirely.
- **B (novelty phrasing).** Never claim "CSAF/VEX was absent from the lane": S001/S003/S040/S040-live
  name both since rounds 24–26. Correct phrase: "first CSAF/VEX methodology ground" / "first CSAF
  registry row".
- **C (ids).** Sibling S055 rows are lane-local; the S055 id itself is not a collision vector.
  kasegi's S055 row is a new scalar registry row in its own `corpus/SOURCES.md`.
- **D (sweep method).** A broad substring pass over the same surface matches only `WAVEX`
  (audio-shokunin format strings) and `CONVEX_PARTITION` (game-dev-2d-shokunin navigation fixtures) —
  classified false positives, no vulnerability-domain semantics. The verdict rests on the
  word-bounded tokens `\bCSAF\b`, `\bVEX\b`, `product_status` plus the spelled-out phrase probe.

## Final ruling text for the lesson (splice-ready)

## DELIVERABLE

```markdown
### Contested scope — one adjacent touch, ruled rather than left silent (F21/S055)

`wave1/ConnSibling.md` consolidates the round-38 sweep evidence and rules on F21/S055 under `PROTOCOL.md:457-461` and kasegi's `PROVINCE.md` Adjacent ("Sibling lanes are reported, not absorbed"):

- **Adjacent, not contested.** The 20 sibling lanes' corpus/SKILL/PROVINCE surfaces hold zero ground on CSAF, standalone VEX, or `product_status`: `grep` for `\bCSAF\b|\bVEX\b|product_status` over every sibling lane's `corpus/`, `SKILL.md`, `PROVINCE.md` → exactly one hit, kake-shokunin/corpus/knowledge/security-txt-publishing.md:63, where `CSAF` is named as a security.txt extension field listed by securitytxt.org (S079). No sibling registry or knowledge entry claims the VEX profile's product-status categories or the machine-readable not-affected justification flags, and no sibling `product_status` token exists anywhere.
- **kake's touch is field-pointer, not standard content.** kake owns security.txt publishing (web properties & publishing province; round-35 frontier step) and explicitly disclaims the vulnerability-handling semantics: "report intake, triage, remediation, disclosure timing, bounty and policy operation ... are not kake's ground" (kake PROVINCE.md round-35 section). Its CSAF mention is the extension-field name whose value is a URI to provider metadata (e.g. `https://msrc.microsoft.com/csaf/provider-metadata.json`), recorded in kake's round-35 census; it does not claim CSAF v2.0's internal schema. Reported here, not absorbed into kasegi's corpus, not cited by the F21 entry.
- **Uncontested elsewhere.** Zero other sibling-lane claims; shokuknow doctrine carries zero CSAF/VEX/product_status rows; the spelled-out "Vulnerability Exploitability eXchange" and `not_affected`/`not-affected` forms appear nowhere in sibling corpora. Source ids are lane-local: siblings each hold their own S055 row; kasegi's S055 row is independent and collides with nothing fleet-wide.
- **Province fit.** F21 fits the Core without re-scope: CSAF v2.0's VEX profile is the machine-readable packaging vendors publish for per-product vulnerability status (affected / not_affected / …), which is the submission/disclosure-packaging surface the Core owns, and it extends the lane's own disclosure ladder (F10 vendor-side disclosure policies → F11 ISO 29147/30111 → F18 KEV → F19 EPSS → F20 SSVC → F21 CSAF/VEX). Novelty is standard-level, never concept-level: prior captures already name CSAF and VEX verbatim (S001.txt, S003.txt, S040.txt, S040-live.txt) but no knowledge entry exists yet — phrase the admission as "first CSAF/VEX methodology ground".
- **Ruling.** F21/S055 is adjacent (kake field-pointer touch) and otherwise uncontested; no report-to-lane absorption arises; no `PROVINCE.md` refinement is required. C2 coverage scoring should treat the opening as adjacent-ground (under-credit risk, not collision risk).
```

Deliverable block: 9 lines, sha256 `71af61b217ad69caabe8b9a1601c91c89de78517ba17b6bb9401f53847e09b76` (verified byte-identical against the scratch copy).

## Housekeeping

- Writes: this receipt only (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/wave1/ConnSibling.md`).
  No lane/fleet/shokuknow file edited; no git/jj mutation (read-only `rev-parse`/`grep`/`ls` only);
  no tool installed (none needed — pacman pause respected); no network fetches performed (no source
  opened; all evidence is local); no subagents dispatched; no `agent://all`.
- Scratch `/fast/scratch/hyaku/kasegi-r38/ConnSibling/` created at seat start, held only the
  deliverable-block fixture, and is removed before yield; verified empty at exit.

Report: .ufo/waves/round-38/wave1/ConnSibling.md
