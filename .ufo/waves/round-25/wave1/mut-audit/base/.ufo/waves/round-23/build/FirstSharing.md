# FirstSharing — FIRST multi-party guidelines: secure information-sharing and third-party limits

- Item: `FirstSharing` (scout), wave `kasegi-r23-build`, master `922a4dd`
- Source row: **S018** — FIRST, *Guidelines and Practices for Multi-Party Vulnerability Coordination and Disclosure*
- Target URL: https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1
- Opened: **2026-10-20** (anonymous GET, public docs, read-only)
- Scope: secure information-sharing practice + third-party limitations only. Roles are `FirstRoles`; negotiation timelines are `FirstTimes`. No production edits.

## Provenance (re-runnable)

| field | value |
|---|---|
| HTTP | `200`, `content-length: 94680` |
| response `date:` | `Tue, 20 Oct 2026 21:42:49 GMT` |
| raw HTML SHA-256 | `94febe95b8182ff362508a68f1939cead6499e02e042cb593099bfbf954ff5bb` (94,680 bytes) |
| `last-modified:` | `Mon, 26 Jan 2026 14:43:46 GMT` — site asset mtime, **not** a document revision date |
| displayed version/date | H1 byline: `Version 1.1` / `Released Spring, 2020` |
| ISO date on page | none — regex `\b\d{4}-\d{2}-\d{2}\b` over page text returns 0 matches |
| retained snapshot | `corpus/source-snapshots/round-23/S018.txt`, 86 lines, 8,372 bytes, sha256 `d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4` |
| snapshot coverage | normalized reader **excerpt**; ends at "…one coordinator should be selected as lead." It contains the sharing bullet (line 55) but **not** the version byline |

Recheck command (fails closed on any byte change):

```bash
curl -sS https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1 \
  | sha256sum   # expect 94febe95b8182ff362508a68f1939cead6499e02e042cb593099bfbf954ff5bb
```

## Primary quote — secure information-sharing (21 words, verbatim)

> All parties should implement measures to secure communication and handling of sensitive information. (e.g., implementing encryption of communication with external stakeholders).

Location: `§ Guiding Concepts and Best Current Practices` → `§ Build and maintain trust` → first bullet
(H2/H3; snapshot `S018.txt:55`). The duty is addressed to **"All parties"**, and the named third-party control is **encryption of communication with external stakeholders** — not a marking, vetting or authorization scheme.

Editorial mirror (same norm, different wording) — `§ Use Case 2` → `§ Variant 4: Vendor makes the vulnerability details public prior to remediation` → `Prevention`, 3rd bullet (17 words):

> Vendor should implement measure to secure communication channels, such as implementing encryption of communication with external stakeholders.

The singular "measure" is the source's own typo; it is kept as a verbatim-fidelity marker (a retyped quote usually reads "measures").

## Third-party limitation evidence (every quote ≤25 words, verbatim)

1. **Inventory is a recommendation, not an enforced dependency map** — `§ Establish a strong foundation of processes and relationships`, 4th bullet (21 words):
   > Vendor should consider tracking the use of third-party components to better develop inventory and an understanding of upstream and downstream dependencies.

2. **Near-duplicate must not be merged** — `§ Use Case 2` → `§ Variant 3: Missing communication between upstream and downstream vendors` → `Prevention` carries a 20-word re-ordering ("to develop better inventory and understanding"). Both strings occur exactly once; they are not interchangeable, and a quote taken from one will not match the other.

3. **NDA appears only as a failure cause, never as a requirement** — `§ Variant 3` → `Causes` (12 words):
   > Vendor fails to pre-establish trusted communication channels or NDAs with downstream stakeholders.

4. **Publishing your own fix can expose a third party** — `§ Minimize exposure for stakeholders`, last bullet (20 words):
   > Vendors should be aware that publication of fixes can disclose the presence of the same vulnerability in other vendors’ components.

5. **Peer set may be unknowable** — `§ Use Case 2` → `§ Variant 6: Missing communication between peer vendors impedes coordination` → `Causes` (23 words):
   > Vendor may not be aware that peers use the same component or technology or may not be aware of all potentially affected peers.

6. **Withholding is an acknowledged incentive** — same `Variant 6` → `Causes` (9 words):
   > Vendor may intentionally withhold information for perceived competitive advantage.

7. **Defenders' outward sharing is constrained** — `§ Use Case 2` → `Description` → `Defenders` (23 words):
   > Develop mitigations or signatures to detect and defend the users against vulnerability, without containing or inferring information that may assist a potential attacker.

8. **Proof-of-concept sharing may be limited-audience** — `§ Use Case 4` → `§ Variant 1: Finder publishes vulnerability details and vulnerability is exploited` → `Prevention` (12 words):
   > Finders can provide proof-of-concept tests to a limited audience, including affected vendors.

9. **The other named control is access limitation, cited to a standard** — `§ Variant 4` → `Prevention`, 2nd bullet (25 words):
   > Vendor should demonstrate the use of implemented policies and controls to correctly manage and limit access to sensitive vulnerability information (i.e., compliance with ISO/IEC 27001).

## Normative strength (measured, not assumed)

- Occurrences in page text: `MUST` 0, `must ` 0, `SHALL` 0, `shall ` 0, `REQUIRED` 0.
- Self-description, 13 words (`§ Multi-Party Disclosure Use Cases`, intro paragraph):
  > Practices are denoted as strong recommendations (“should”) or suggestions (“can,” “could,” or “may”).
- Consequence: the document creates **no obligation on any third party** to accept shared information, sign an NDA, or apply a traffic marking. "should" is a strong recommendation; "can/could/may" is a suggestion.
- Marking schemes: `TLP` (5 hits) and `Traffic Light` (3 hits) occur **only in site-navigation chrome**; **0** occurrences inside the document body.

## Falsifiable findings

- **F1 — version label contradicted by the page itself.** The H1 byline reads `Version 1.1` / `Released Spring, 2020`, while `<title>` and `og:title` both read `…Disclosure - version 1.0`. A citation keyed on page metadata alone records the wrong version. *Falsifier:* `curl -s <URL> | grep -o '<title>[^<]*'`; if it prints 1.1, F1 is false.
- **F2 — no normative obligation exists.** *Falsifier:* case-sensitive count of `MUST|SHALL|REQUIRED` over the page body; any hit reverses F2.
- **F3 — third-party limits are informational, discovery-based and reputational.** The document supplies inventory ("should consider tracking"), peer awareness ("should develop and maintain awareness of peers"), and an acknowledged withholding incentive; it supplies no enforcement, no disclosure duty on third parties, and no penalty clause. *Falsifier:* locate a normative third-party disclosure duty or sanction in the body; then F3 is false.
- **F4 — no precise publication date exists.** Only "Spring, 2020"; `last-modified: 2026-01-26` is a site re-render and must not be written as the publication date. *Falsifier:* find an ISO date attached to the version byline.
- **F5 — the retained snapshot cannot re-verify version/date.** `S018.txt` is an excerpt that omits the byline (proved: `Version 1.1` absent from snapshot, present in live HTML). A Q1 `source:` line must therefore cite the live URL + hash, not the snapshot alone.

## Rejected over-generalizations (with reason)

- **"FIRST requires NDAs / encrypted channels."** Rejected: the NDA appears only as a cause of failure; encryption is a "should"; the page notice says the descriptions are "for informational purposes only". Stating it as a requirement is an overclaim.
- **"FIRST v1.1 mandates TLP markings."** Rejected: zero body mentions of TLP; all hits are site navigation.
- **"Third parties must be notified."** Rejected: the document's duties attach to vendors, finders, coordinators and defenders; peers "may not be aware" and "may intentionally withhold".
- **"This is version 1.0."** Rejected: the `- version 1.0` string is stale HTML metadata; the displayed byline is 1.1.
- **"The snapshot is the source."** Rejected: it is a normalized excerpt (8,372 bytes vs 94,680 raw), lacking the byline and footnotes.

## Consumer notes for the F06 / S018 row (do not self-admit)

- The existing one-liner ("Coordinate upstream and downstream parties with clear contacts, negotiated timelines and shared disclosure expectations") is supported by § *Establish a strong foundation* and § *Maintain clear and consistent communications*, but it is **not** a secure-sharing claim; if the entry adds one, quote the 21-word primary above.
- Version string the entry must carry: `version 1.1, released Spring 2020`; if page metadata is cited, note the `<title>`/`og:title` still say 1.0.
- Q3 form: each quote above is ≤25 words with an exact section path and a snapshot line where available (only the primary and the GC third-party bullet are in the snapshot, at lines 55 and 30).
- Q5 form: use F1 or F2 as the checkable rule and one rejected over-generalization above as the required rejection.

## Scope limits / remaining unknowns

- Not read: Figures 1–6 (images), footnote targets 1–22, translations, or any errata page; no search performed for a later v1.2.
- No Wayback/archive copy compared; stability of the hash is asserted only for 2026-10-20.
- Document-level scope limits are its own: notice "for informational purposes only"; guidance "targeted at vulnerabilities that have the potential to affect a wide range of vendors and technologies simultaneously" (20 words); SDL activity declared "beyond the scope of this document".
- Read-only seat: no production file edited; no tool installed or updated (none needed).
