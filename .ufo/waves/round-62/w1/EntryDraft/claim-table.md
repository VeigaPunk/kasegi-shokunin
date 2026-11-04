# S095 pre-counter claim and assertion map — draft

Axes: depth:verifiability (nominal 4 held), coverage (8 held). This seat supplies only the C2/F43 documentation draft; these are not frozen claims or measured score changes.

The proposed entry contains the complete attributed six-row claim table before its review rules. This companion maps those rows to the draft manifest assertion list. Both drafts are supplied before this seat executes any admission counter (none executed). No claim is made about the timing of another seat's or L1's counters.

| Entry claim | Exact S095 capture lines | Assertion ids | Scope / rejection |
|---|---|---|---|
| C1 adapted model, not universal phase count | 57-59, 60-70, 73, 129-140 | Q01-Q03; Q07-Q12 for table distinction | CERT/CC's adaptation, not ISO requirements; rejects exactly-six-universal-phases. |
| C2 report destination | 63 | Q04 | Researcher report to vendor/coordinator; not an initial-publication mandate. |
| C3 analyst validation and Vendor/Coordinator cells | 65, 112-116, 129-134 | Q05-Q09 | Reporter dash is not a prohibition; rejects reporter-must-validate as source attribution. |
| C4 different prioritization objects | 112-116, 135-140 | Q06, Q10-Q12 | Reports for response vs fixes for deployment. |
| C5 remediation mechanisms and fix confirmation | 67, 112-116, 141-146 | Q06, Q13-Q16 | Patch preferred, not exclusive; reporter confirmation belongs to Remediation. |
| C6 public awareness vs deployment | 69, 71, 112-116, 153-158 | Q06, Q17-Q19 | Public announcement does not itself establish deployment. |

## Manifest integration limits

`manifest-assertions.json` is a schema-shaped draft with 19 assertions, not a production capture-provenance record. Its `path: S095.txt` is intended for the eventual manifest in `corpus/source-snapshots/round-62/`, not for execution in this draft directory, which contains no snapshot copy. Do not run it here and call missing-source output an admission result.

The repeated strings “Validates reports received” and “Prioritizes reports for response” have separate numeric anchors for their Vendor and Coordinator cells. The instrument checks four-line anchor windows, not semantic table-column alignment; the full row spans and headings above remain the audit trail for those assignments. A quote-presence pass alone is not proof of the claim interpretation.

L1 must merge these assertions into its capture record with actual capture provenance from the source owner; this seat does not invent fetch timestamps, response sizes, methods, or freshness. The proposed entry's recheck uses the required lane-prefixed production manifest path. That manifest was absent at initial inspection, and no source-recheck, frontier, binding or other admission counter was run by this seat.
