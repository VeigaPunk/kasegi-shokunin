# CraRecipients — CRA Article 14 recipients / Article 16 platform

Seat: KasegiR23.CraRecipients-5 (scout, read-only). Round 23, base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`.
Axes served: `depth:verifiability` (exact located quotes, version identity, reproducible fetch),
`coverage` F08 (CRA reporting duties: recipients, coordinator, ENISA, platform).
Wrote no production file, no clone, no commit, no lane/fleet state change; installed nothing.

## 1. Source identity and version (observed)

| field | value |
|---|---|
| act | Regulation (EU) 2024/2847 of 23 October 2024 (Cyber Resilience Act) |
| OJ | OJ L series, 2024/2847, **20.11.2024** (header lines: `L series`, `2024/2847`, `20.11.2024`) |
| signature | `Done at Strasbourg, 23 October 2024.` (end of act, before the ELI line) |
| ELI | `http://data.europa.eu/eli/reg/2024/2847/oj` (printed in the act itself and in the OJ RDF) |
| CELEX | `32024R2847` (OJ RDF `resource_legal_id_celex`) |
| version mined | **original OJ act**, not a consolidation; English XHTML generated 2024-11-25 |
| artifact | `http://publications.europa.eu/resource/cellar/21b7d4eb-a6e2-11ef-85f0-01aa75ed71a1.0006.03/DOC_1` |
| bytes / sha256 | 710,696 B / `fe0cca4a0caec50e7cf5a91432b94a19b211f86be8584fdba56372bdcea571ed` |
| HTTP validators | `ETag: "Con-20241125174506000"`, `Last-Modified: Mon, 25 Nov 2024 16:45:06 GMT`, re-read 2026-10-20T21:46:02Z |
| generator | `CONVEX # converter_version:9.16.1 # generated_on:20241125-1721 # ELI version:0.2` |
| OJ RDF | `http://publications.europa.eu/resource/celex/32024R2847` (`application/rdf+xml`, 2,245,247 B, sha256 `de7659867222fd1a11367d4c3fbd8e0ee462bdacf43ec8cd376d3cee482a3905`): `date_publication` 2024-11-20; `date_document` / `work_date_document` 2024-10-23 |

Access facts, so a verifier can separate "not found" from "not reachable":

- `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng` (the assignment URL) returned **HTTP 202**: 0 bytes
  with a bare curl, and a 2,035-byte JavaScript page (`window.awsWafCookie…`) with a browser User-Agent —
  an AWS WAF challenge with **no article text** in either case. `legal-content/EN/TXT/HTML/?uri=OJ:L_202402847`
  and `legal-content/EN/TXT/?uri=CELEX:32024R2847` returned the same 202/2,035-byte challenge.
  `https://data.europa.eu/eli/reg/2024/2847/oj` returned 202 with the body not inspected.
- The OJ object was therefore retrieved through Publications Office **Cellar content negotiation**
  (`celex/32024R2847` → 303 → the DOC_1 URL above). This is the same OJ act, not a mirror.
- No consolidated text observed: `resource/celex/02024R2847`, `…/02024R2847-20241210`,
  `…-20260911`, `…-20261020` all returned **HTTP 404** on 2026-10-20. Claim limited to those probes.
- RDF/RDF projection contains no `amended_by` / `consolidated_by` triple for this act (not asserted as proof
  of no amendments; only that this projection did not expose one).

Conclusion for the row: cite **OJ L, 2024/2847, 20.11.2024; CELEX 32024R2847; original English OJ act
(Cellar DOC_1, sha256 fe0cca4a…)**. The `/oj/eng` HTML page was **not** observed; do not claim otherwise.

## 2. Article 14 recipients (observed text, exact locators)

- **Art 14(1), first sentence** — actor is the *manufacturer*; recipients are the **CSIRT designated as
  coordinator** (per paragraph 7) **and ENISA**; channel is the **single reporting platform established
  pursuant to Article 16** (second sentence).
- **Art 14(3), first sentence** — the same recipient clause for **severe incidents**; the concluding clause
  `simultaneously to the CSIRT designated as coordinator, in accordance with paragraph 7 of this Article,
  and to ENISA` is **character-identical** in 14(1) and 14(3). A text-only quote check therefore cannot tell
  the two paragraphs apart; the locator must name the paragraph id (`014.001` vs `014.003` in the OJ XHTML).
- **Art 14(7)** — routing rule: notification goes through the **electronic notification end-point of the
  coordinator CSIRT of the Member State where the manufacturer has its main establishment in the Union**,
  and `shall be simultaneously accessible to ENISA`. Main establishment = where cybersecurity decisions for
  the product are predominantly taken; if undeterminable, the Member State with the highest number of
  employees in the Union. With no Union main establishment, the order is: authorised representative →
  importer → distributor → highest number of users (14(7)(a)–(d)); later notifications may stay with the
  first CSIRT chosen under (d).
- **Art 14(2)/(4)** clocks (context; owned by other seats): 24-hour early warning, 72-hour notification,
  final report 14 days after a corrective/mitigating measure is available (vulnerability track) or one month
  after the incident notification (incident track). The 24-hour clock runs from the **manufacturer becoming
  aware**, not from public disclosure.
- **Art 15(1)** — voluntary notifications may come from `Manufacturers as well as other natural or legal
  persons` to a coordinator CSIRT **or** ENISA. This is a notification channel; it is not a testing,
  asset-scope, or safe-harbor grant.

## 3. Article 16 platform (observed text)

- **16(1)** — `a single reporting platform shall be established by ENISA`; **day-to-day operations managed
  and maintained by ENISA**; architecture permits **Member States and ENISA** to run their own electronic
  notification end-points; scope = notifications under 14(1)/(3) and 15(1)/(2), "in order to simplify the
  reporting obligations of manufacturers".
- **16(2)** — the **coordinator CSIRT initially receiving** a notification disseminates it **without delay**
  via the platform to coordinator CSIRTs of Member States where the manufacturer indicated the product was
  made available. Dissemination may be delayed on justified cybersecurity grounds (including an ongoing CVD
  procedure under Art 12(1) NIS2); a withholding CSIRT must immediately inform ENISA with justification and
  an indication of when it will disseminate. Narrower exceptional limits (points (a)–(c)) restrict what is
  simultaneously visible to ENISA until full dissemination.
- **16(3)** — coordinator CSIRTs pass notified information to their **market surveillance authorities**.
- **16(4)–(5)** — ENISA security measures for the platform; ENISA with the CSIRTs network specifies
  technical/operational/organisational measures and the national/Union end-points.
- **16(6)** — if a coordinator CSIRT learned of an actively exploited vulnerability through a CVD procedure,
  it may delay dissemination only until the involved CVD parties consent.
- **14(9)** — Commission delegated acts on the 16(2) delay grounds, due **by 11 December 2025**;
  **14(10)** — implementing acts on notification format/procedures. **Not opened in this seat**; no claim is
  made about their adoption, content, or current platform operation.

## 4. Exact quotes (all ≤25 words; verbatim)

Word counts are whitespace tokens. "S029.txt" = `corpus/source-snapshots/round-23/S029.txt`
(sha256 `82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c`, 19,900 B), checked with raw
`str.count` (the same comparison `source-recheck.py` performs).

| id | location | quote | words | S029.txt occ. |
|---|---|---|---|---|
| Q1 (primary) | Art 14(1) sentence 1 (also Art 14(3) sentence 1) | "simultaneously to the CSIRT designated as coordinator, in accordance with paragraph 7 of this Article, and to ENISA" | 18 | 2 |
| Q2 | Art 16(1) | "in order to simplify the reporting obligations of manufacturers, a single reporting platform shall be established by ENISA" | 18 | 1 |
| Q3 | Art 14(1) sentence 1 (unique) | "A manufacturer shall notify any actively exploited vulnerability contained in the product with digital elements" | 15 | 1 |
| Q4 | Art 14(3) sentence 1 (unique) | "A manufacturer shall notify any severe incident having an impact on the security of the product with digital elements" | 19 | 1 |
| Q5 | Art 14(7) first subparagraph | "electronic notification end-point of the CSIRT designated as coordinator of the Member State where the manufacturers have their main establishment" | 20 | 1 |
| Q6 | Art 71(2) second subparagraph | "Article 14 shall apply from 11 September 2026" | 8 | 1 |
| Q7 (boundary) | Art 17(4) | "shall not subject the notifying natural or legal person to increased liability" | 12 | 1 |
| Q8 (boundary) | Art 15(5) | "voluntary reporting shall not result in the imposition of any additional obligations" | 12 | 1 |

Checked in the Cellar XHTML but **not** in S029.txt (snapshot starts at Article 14, so these cannot be
manifest-checked against it):

| id | location | quote | words | Cellar occ. |
|---|---|---|---|---|
| Q9 (boundary) | recital 75 (`id="rct_75"`, printed "(75)") | "Member States should aim to address, to the extent possible, the challenges faced by vulnerability researchers, including their potential exposure to criminal liability" | 23 | 1 |
| Q10 (boundary) | recital 76 (`id="rct_76"`, printed "(76)") | "Manufacturers of products with digital elements should put in place coordinated vulnerability disclosure policies" | 14 | 1 |
| Q11 | Art 13(8), CVD-policy subparagraph before paragraph 9 | "Manufacturers shall have appropriate policies and procedures, including coordinated vulnerability disclosure policies, referred to in Part II, point (5), of Annex I" | 22 | 1 |

Q1 preferred form if a single contiguous quote must also carry the actor: use Q3 + Q1 as two located
quotes. A single ≤25-word span containing "A manufacturer" through "ENISA" does not exist.

## 5. Falsifiable finding

**The CRA Article 14 duty runs manufacturer → (CSIRT designated as coordinator + ENISA), through the
Article 16 platform; the operative text creates no researcher testing authorization and no public-disclosure
deadline.** Each clause is checkable against the quotes above:

1. Actor: Art 14(1)/(3) say "A manufacturer shall notify…" (Q3/Q4); Art 15(1) opens *voluntary* notification
   to "other natural or legal persons". A statement that researchers/finders carry the Article 14 24-hour duty
   is false on this text.
2. Recipients: coordinator CSIRT **and** ENISA (Q1), with routing fixed by 14(7) (Q5). "ENISA only",
   "the Commission", or "the national authority of the Member State of sale" are not supported.
3. Platform operator: ENISA establishes it and manages day-to-day operations (Q2); Member States and ENISA
   run end-points. "Commission-operated" is false.
4. Timing: the 24-hour early warning runs from the **manufacturer becoming aware** (Art 14(2)(a), 14(4)(a));
   Article 14 applies from **11 September 2026** (Q6), not 11 December 2027. Public-disclosure-clock readings
   are false.
5. Authorization boundary: the only researcher-specific text is recital 75 (Q9), addressed to **Member
   States** ("in accordance with national law"), encouraging non-prosecution guidelines. The CRA does not
   say testing is authorized. Art 15(5)/17(4) (Q7/Q8) protect the *notifier* from added obligations/liability;
   they are not scope or safe-harbor grants.
6. Verifier trap: Q1 passes a text-only check at **two** paragraphs. A manifest/recheck that records only the
   quote string cannot distinguish 14(1) from 14(3); the location field (paragraph id) must be checked
   separately.

Corollary for corpus use: "not a complete current compliance assessment" is the correct scope; the seat did
**not** verify implementing/delegated acts, platform operation, national law, or product applicability.

## 6. S024 row handling (recommendation only — read-only seat)

Observed state at 2026-10-20 (`corpus/SOURCES.md` sha256 `32a19dc4…`): S024 is still `queued`, scope says
"(Article 14 wording not yet verified against EUR-Lex)", anchor says "Article 14 not reached … re-open before
mining". S029 already exists with `supersedes S024 —` in its *teaches* field and `mined | 2026-10-20`, but its
teaches field names only the clock distinction, and its scope does not name recipients/ENISA/platform.
`corpus/lessons/round-23.md` (sha256 `82419293…`) records `S029, supersedes S024` with only the 14(2)(c) quote.

Recommended, in order of least change (L1 decides; R8 governs):

1. Flip **S024 status** `queued → superseded` (no such status exists in the current 18 mined / 9 queued /
   3 rejected tally; if L1 prefers no new status, leave S024 queued and rely on S029's `supersedes S024 —`).
   Either way, record the old→new status/recheck/used-by in the round-23 lesson, as R8 requires.
2. Add Q1 (and Q2) to `corpus/source-snapshots/round-23/manifest.json` under S029 and to the F08 entry's
   "Exact located quotes" table (it currently has no quote for the recipients or the platform claim, although
   its Rule paragraph asserts both). This is the direct content gap this seat closes.
3. If the recipients/platform locators must appear in an immutable row anchor (R8 strictness), add a new row
   beginning `supersedes S024 —` with anchor `Articles 14(1), 14(3), 14(7), 16(1)-(6), 71(2)`; do **not**
   rewrite S024's or S029's anchor in place. Do not add recital 75 to S029's anchor without a successor row.

Observation, not defect: at the digests above, `corpus/source-snapshots/round-23/manifest.json` does not
exist, while the F08 entry's `recheck:` command uses it. That command will exit **2 UNAVAILABLE** until the
RecheckSources seat lands the manifest. S029's snapshot covers Articles 14–17 and 71 (Article 17(1)–(6) is
present though S029's scope lists only 14–16+71).

## 7. Proposed manifest fragment for S029 (not applied)

```json
{
  "id": "S029",
  "path": "S029.txt",
  "sha256": "82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c",
  "quotes": [
    {"id": "art14-1-recipients", "quote": "simultaneously to the CSIRT designated as coordinator, in accordance with paragraph 7 of this Article, and to ENISA", "location": "Article 14(1) sentence 1; same clause occurs in 14(3)"},
    {"id": "art14-1-duty", "quote": "A manufacturer shall notify any actively exploited vulnerability contained in the product with digital elements", "location": "Article 14(1) sentence 1"},
    {"id": "art14-3-duty", "quote": "A manufacturer shall notify any severe incident having an impact on the security of the product with digital elements", "location": "Article 14(3) sentence 1"},
    {"id": "art14-7-endpoint", "quote": "electronic notification end-point of the CSIRT designated as coordinator of the Member State where the manufacturers have their main establishment", "location": "Article 14(7) first subparagraph"},
    {"id": "art16-1-platform", "quote": "in order to simplify the reporting obligations of manufacturers, a single reporting platform shall be established by ENISA", "location": "Article 16(1)"},
    {"id": "art71-2-applies", "quote": "Article 14 shall apply from 11 September 2026", "location": "Article 71(2) second subparagraph"}
  ]
}
```

Caveat: `source-recheck.py` (sha256 `f743942d…`) matches raw substrings and reports `location` as metadata
only; it cannot detect the 14(1)/14(3) duplicate. It also cannot attest upstream currency — it is a pinned
snapshot check, per the instrument docstring.

## 8. Scope limits / unresolved

- Direct EUR-Lex ELI HTML was WAF-blocked (202) in this environment; the OJ act was read through Cellar.
  No claim about the live `/oj/eng` page rendering.
- Implementing/delegated acts under 14(9)/(10) and their effect on platform delay grounds were not opened;
  the 11 December 2025 delegated-act deadline is quoted from Article 14(9) only.
- Platform operational status as of 2026-10-20 was **not** tested (no contact, no submission, per doc-only
  scope). The text mandates establishment; it does not date operation.
- No consolidated/amended text observed (four 404 probes); no amendment analysis.
- No legal advice, no jurisdiction/product-class analysis, no CVSS severity, no disclosure-timeline general
  rule; F08's manufacturer/researcher distinction is preserved, not extended.
- Recital quotes (Q9–Q11) are verified in the Cellar artifact only; they are outside S029.txt and therefore
  outside any manifest check keyed to S029.
