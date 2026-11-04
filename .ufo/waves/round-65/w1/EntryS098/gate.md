# Gate — F44 / S098 (FIRST PSIRT Services Framework v1.1)

DRAFT by seat `EntryS098` for the L1 (KasegiR65). Round 65, wave 1 — a predata
build-and-falsify wave: **claims are not frozen, and nothing in this block is admitted by
itself.** No production file was edited by this seat.

## Source

- **Opened:** 2026-11-04.
- **URL:** `https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1`
  (HTTP 200, `final_url` equals the request URL).
- **Capture pointer:** `corpus/source-snapshots/round-65/S098.txt`.
- **Capture:** sha256 `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`,
  **170137 snapshot bytes over 229255 fetched bytes**, **1573 lines**. Raw HTML sha256
  `3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11`.
- **Fetch method:** the lane's own instrument, `corpus/instruments/capture-source.py
  --kind html` (default instrument UA), which is also the method the committed capture used.
- **Document body:** L216-L1536. L1537-L1549 is the site's navigation column and
  L1550-L1573 is the Downloads sidebar (`<div id="sidebar">` opens immediately after the
  last content line in the served HTML).
- **Manifest:** `corpus/source-snapshots/round-65/manifest.json` — 18 assertions, all
  `occurrences=1` with `anchor=N-ok`.
- **Recheck (the entry's `recheck:` line, exact form):**

  ```
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-65/manifest.json --source S098
  ```

  Run by this seat against the committed manifest and capture:

  ```
  S098:sha256 OK
  S098:Q01-version OK occurrences=1 anchor=1-ok
  S098:Q02-catalogue-not-requirements OK occurrences=1 anchor=219-ok
  S098:Q03-initial-service-catalogue OK occurrences=1 anchor=219-ok
  S098:Q04-service-area OK occurrences=1 anchor=229-ok
  S098:Q05-intake-main-scenario OK occurrences=1 anchor=681-ok
  S098:Q06-intake-contacts-readiness OK occurrences=1 anchor=681-ok
  S098:Q07-advertise-in-csirt-lists OK occurrences=1 anchor=695-ok
  S098:Q08-report-isolation OK occurrences=1 anchor=713-ok
  S098:Q09-timely-acknowledgement OK occurrences=1 anchor=715-ok
  S098:Q10-cvss-input OK occurrences=1 anchor=853-ok
  S098:Q11-quality-gate-bug-bars OK occurrences=1 anchor=853-ok
  S098:Q12-expectations-to-finders OK occurrences=1 anchor=857-ok
  S098:Q13-established-finder-bypass OK occurrences=1 anchor=875-ok
  S098:Q14-reproduction-required OK occurrences=1 anchor=905-ok
  S098:Q15-isolated-test-environment OK occurrences=1 anchor=918-ok
  S098:Q16-sensitive-storage OK occurrences=1 anchor=930-ok
  S098:Q17-ack-from-finder OK occurrences=1 anchor=1203-ok
  S098:Q18-disclosure-audiences OK occurrences=1 anchor=1231-ok
  RC=0
  ```

## Located quotes

Maximum quote length in this seat's proposed set: **25 words** (E09 at L231 and E10 at
L289 — both at the contract bound and both verified verbatim). Every proposed quote was
re-derived from the committed capture by this seat: verbatim substring of its anchored line,
≤25 whitespace-delimited words, ≥12 normalized characters (the `source-recheck.py` floor).
44 of the 45 are unique in the capture; E35 ("Service 2.1 Intake of Vulnerability
Reporting") occurs twice and is resolved by its anchor. The full 45-quote proposal, its ids
and its anchors are in `claim-table.md` and in the shipped
`manifest-assertions-proposal.json`; the set was exercised against the **real**
`source-recheck.py` instrument over a copy of the committed capture and returned
`S098:sha256 OK` plus 45 quote lines with `RC=0`.

The maximum-length quote of the set, quoted here verbatim:

> "A service is a set of recognizable, coherent actions towards a specific result on behalf of or for the constituency of an incident response team." — E09, L231, 25 words

## Assimilation set

`.ufo/waves/round-65/assimilation/` **exists but is empty** (0 files) at the time of this
gate, so there is no staged adoption set to admit from or reject from. The admit/reject
below are therefore taken from the round's own screened candidate sources for C2, which is
the set the seat spec named.

### Admit

| id | admitted as | document | evidence | entry |
|---|---|---|---|---|
| S098 | tier-A `docs`, `mined`, opened 2026-11-04 | FIRST, PSIRT Services Framework v1.1 — the product-side service catalogue | capture `corpus/source-snapshots/round-65/S098.txt`, sha256 `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`, 1573 lines; manifest with 18 assertions, all `occurrences=1`; recheck `RC=0` (output above) | `.ufo/waves/round-65/w1/EntryS098/first-psirt-services-framework.md` (this seat's draft) |

The admitted ground, stated so a reviewer can check the boundary: the catalogue spine
(service area → service → function → sub-function) over six service areas, the three
organizational models, the Operational Foundations tiers, and the maturity *definition* the
document carries — **not** a maturity-level ladder.

### Reject

| candidate | failing gate | reason (evidence) | flip condition |
|---|---|---|---|
| FIRST's *PSIRT Maturity Document* — `https://www.first.org/standards/frameworks/psirts/psirt_maturity_document` (HTML, 82978 bytes, sha256 `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e`, opened by this seat 2026-11-04) as part of F44 | ground / scope | It is a **different document**. The maturity *levels* — "Maturity Level 1 (Basic)", "Maturity Level 2 (Intermediate)", "Maturity Level 3 (Advanced)", "Beyond 'Level 3'" — live there and in no part of S098: `grep -c -iE 'Maturity Level\|Level [0-9]'` over the S098 body → 0, while the maturity document's own text carries all four level headings. S098 links it only as a sidebar download ("PSIRT Maturity, HTML", L1553). Admitting S098 with level content would attribute words the capture does not contain. | The maturity document is captured as its own source id with its own manifest, digest and entry, and the F44 row is written to exclude level vocabulary. Then the level ladder may be admitted as separate ground, and the F44 entry's maturity section is rewritten to point at it. |
| The multiparty coordination guidelines (FIRST v1.1, `https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1`) as F44's subject | ground / double-counting | Already admitted as **F06** (`corpus/README.md:207`, source **S018**, entry `corpus/knowledge/multiparty-vulnerability-coordination.md`). S098's only FIRST cross-reference of that kind is a footnote URL to the **v1.0** multiparty PDF (L1531) — a different artifact from the v1.1 guidelines the lane holds. | F06 is withdrawn from the frontier table, or S018 is found to state the service-catalogue ground this entry holds — then the multiparty guidelines may be re-admitted against a different source. |

## Rejected readings (the entry's own)

Carried in full in `first-psirt-services-framework.md` §"Rejected readings" and graded in
`claim-table.md`. The four that bear on the gate: "the framework defines maturity levels"
(rejected — 0 occurrences in the capture), "the framework mandates these services"
(rejected — "shall" 0, "conform" 0, and the page's own "may provide" / "free to implement
their own model"), "this is the multi-party coordination framework" (rejected — F06/S018),
"this is a CVD phase-and-role model" (rejected — F43; no phase model, no matrix, 0
`<table>` elements).

## Finding for the L1 — the manifest's `body_lines` excludes the maturity definition

The committed manifest declares `body_lines: [216, 1450]`. That range stops inside Annex 2
(Acknowledgements, L1448-L1466): it **excludes the Glossary (L1498-L1512)**, and with it
the capture's *only* maturity definition at L1510, and it also excludes Annex 3/4/5
(L1467-L1497) and the Annex 1 supporting-resources list (L1440-L1447) whose ISO edition
years the entry's date analysis depends on.

Consequence: the entry's maturity sentences (claim-table rows C-24, C-25, C-26, C-28) are
pinned at L1510 and L1553, **outside** the manifest's declared body range. The recheck
instrument does not enforce `body_lines`, so those rows pass the recheck as written — the
range is metadata, not a gate — but a reader who trusts `body_lines` as "the document body"
will believe the Glossary is not part of S098, which is false.

Two options for the L1, both verified as harmless to the existing 18 assertions:

1. **Widen `body_lines` to `[216, 1536]`** and add the maturity and taxonomy assertions
   (E01-E45, the set this seat exercised at `RC=0`). This is the option this seat's draft
   assumes.
2. **Leave `body_lines` as it is** and note in the entry that the maturity definition sits
   outside the declared body range, citing L1510 explicitly.

This seat did **not** edit the manifest — it is L1's production surface.

## Limits of this gate

- The recheck compares digest-pinned local bytes and manifest quotes. It does not establish
  upstream freshness, that any team implements any service, or that a particular disclosure
  met any duty.
- The capture is a web rendering of a Word-produced PDF. The same document exists as
  `FIRST_PSIRT_Services_Framework_v1.1.pdf`, which carries a printed version and date the
  HTML does not; a date-bearing or page-bearing citation needs its own capture.
- Byte-identity across this seat's capture, ScoutS098's candidate and L1's committed capture
  shows the *bytes* reproduce; it is not independent confirmation of the document's meaning.
- No frontier counter, census, claim-package gate or freeze check was run by this seat, and
  no score movement is claimed.
