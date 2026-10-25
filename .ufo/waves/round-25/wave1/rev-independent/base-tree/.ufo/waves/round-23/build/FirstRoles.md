# FirstRoles — S018 finder/vendor/coordinator roles and source limits

Seat: KasegiR23.FirstRoles-5 (read-only leaf). Observed 2026-10-20 21:42–21:47 UTC
(18:42–18:47 -0300), base `922a4dde90b60b465e2b8b241d1fe363f1f27e98` plus the untracked
round-23 working tree. Axis named: **depth:verifiability** (does a located quote + executable
recheck survive?) and **coverage** (does F06 have the role evidence its row asks for?).

Method: live read-only GETs of three official FIRST resources, byte-level text extraction,
and exact-substring checks with fail-closed negative controls. No production edits by this
seat; this file is the only artifact I wrote. The tree moved during observation (a sibling
changed S018's status `queued`→`mined` and used-by; anchor and version fields unchanged), so
re-read status fields before admission. No tool installs or updates were performed.

## 1. Answer: the roles

Primary required quote (14 words), exact location `#Definitions` (`<h2 id="Definitions">`),
bullet `Coordinator:`; PDF v1.1 p. 4:

> “Optional participant that can assist vendors and finders in handling and disclosing vulnerability information.”

Supporting role definitions, same section, each ≤25 words:

| Role | Exact quote | Confidence |
|---|---|---|
| Finder | “Individual or organization that identifies a potential vulnerability in a product or service.” (13 w) | observed, HTML + PDF p. 4 |
| Vendor | “Individual or organization that developed the product or service or is responsible for maintaining it.” (15 w) | observed, HTML + PDF p. 4 |
| Coordinator | “Optional participant that can assist vendors and finders in handling and disclosing vulnerability information.” (14 w) | observed, HTML + PDF p. 4 |
| Upstream Vendor | “Vendor that provides a product or technology to a downstream vendor.” (11 w) | observed, HTML + PDF p. 4 |
| Downstream Vendor | “Vendor that receives a product or technology from an upstream vendor for use in the downstream vendor’s product, technology, or service.” (21 w) | observed, HTML + PDF p. 4 |

Figures 1 and 3 are JPG/PNG with alt text only (`Stakeholder roles and communication paths`;
`Vulnerability with coordinated disclosure`), so the diagram's role topology is **not**
text-verifiable from this source.

### Falsifiable finding (the role-set boundary)

The document's “generalized coordinated disclosure process” in Use Case 2 lists exactly four
role headings: **Finder, Vendors, Defenders, Users** (HTML `#Use-Case-2-Vulnerability-with-coordinated-disclosure`;
PDF p. 12). **Coordinator is not one of them**; it is defined as “Optional participant” and
appears under the separate heading “Use coordinators when appropriate.”

Check: if S018 required a coordinator in every multi-party case, then (a) the Definitions entry
would not begin “Optional participant”, and (b) the generalized role list would include it.
Neither holds. [INFERENCE] A worksheet that makes a coordinator row mandatory over-reads
S018; one that records “coordinator: none/unknown” is consistent with the source.
Rejected over-generalization: “FIRST requires finder, vendor and coordinator tri-party
coordination.” Surface scan: 2 occurrences of “safe harbor”, both as an incentive a *Vendor can
offer* (build trust; Use Case 2 Variant 1 prevention); 1 occurrence of “authoriz” and it is
“unauthorized changes.” [INFERENCE] The document grants no testing right and imposes no duty.

## 2. Date and version (as printed, not inferred)

- Web body, immediately under the H1: `<em>Version 1.1</em><br /><em>Released Spring, 2020</em>` (1 occurrence each).
- URL route `/.../multiparty/guidelines` returns **301** to `/.../guidelines-v1.1` (observed).
- FIRST SIG page (`/global/sigs/vulnerability-coordination/multiparty/`) says “Version 1.1 is
  available as: HTML Format / PDF Format” and its Release History says “The first revision was
  published in May 2020.”
- PDF (`FIRST-Multiparty-Vulnerability-Coordination-v1.1.pdf`, 892,129 B, 31 pp) cover prints
  “Spring 2020”; `pdfinfo` reports CreationDate 2020-05-14 18:40:37 -03, ModDate 2020-06-19
  11:52:04 -03.

**Observed contradiction:** the HTML `<title>` and `og:title` both say
“Guidelines and Practices for Multi-Party Vulnerability Coordination and Disclosure - version
1.0” (2 occurrences), while the body, URL slug, SIG page and PDF filename all say 1.1.
[INFERENCE] Treat the title/og metadata as stale; cite “Version 1.1, released Spring 2020;
FIRST release history says first revision May 2020.” There is **no official day-level date**: no
`<time>`, no JSON-LD (`application/ld+json` count 0), no datePublished/citation meta, and no
visible published/updated line. HTTP `Last-Modified: 2026-01-26T14:43:46Z` dates the page, not
the text.

## 3. Source limits (with exact text)

1. **Non-normative best practice.** Notice: “These descriptions are for informational purposes
   only.” (7 w) and “FIRST.Org is not liable for any damages of any nature incurred as a result
   of or in connection with the use of this information.”
2. **Recommendation strength.** “Practices are denoted as strong recommendations (“should”) or
   suggestions (“can,” “could,” or “may”).” (13 w). Nothing is “must”; no compliance or
   enforcement mechanism is defined.
3. **Scope.** “This guidance is targeted at vulnerabilities that have the potential to affect a
   wide range of vendors and technologies simultaneously.” (20 w). It is not a single-vendor or
   single-product procedure and not a legal deadline.
4. **Not the ISO standard.** “This document differs from the ISO vulnerability disclosure and
   handling standards (ISO/IEC 29147 and ISO/IEC 30111).” (16 w). Definitions are borrowed:
   “Definitions that are available in ISO/IEC 29147:2014 are used with minimal modification.”
5. **Coordinator is optional and under-specified.** No authority, selection criteria, SLA,
   jurisdiction or accountability is defined; the only selection rule is conditional: “To
   reduce confusion when multiple coordinators are involved, one coordinator should be selected
   as lead.” (15 w).
6. **Not a CVE/CNA rule source.** Its CVE footnote points at the legacy `cve.mitre.org` rules
   page; [INFERENCE] current CNA obligations must come from S022/S030, not S018.
7. **No authorization effect.** The only “safe harbor” mentions are vendor-offered incentives;
   [INFERENCE] the document neither authorizes testing nor promises non-enforcement.

## 4. Executed verification (observed, not inferred)

Live recheck, run within the 2026-10-20 21:45–21:46Z observation window; all positive checks
exited 0, both negative controls exited 1:

```bash
set -o pipefail
H=$(curl -fsSL https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1) || exit 2
S=$(curl -fsSL https://www.first.org/global/sigs/vulnerability-coordination/multiparty/) || exit 2
printf '%s' "$H" | tr -d '\n' | grep -Fq 'Optional participant that can assist vendors and finders in handling and disclosing vulnerability information.' || exit 1
printf '%s' "$H" | tr -d '\n' | grep -Fq '<em>Version 1.1</em>' || exit 1
printf '%s' "$H" | tr -d '\n' | grep -Fq '<em>Released Spring, 2020</em>' || exit 1
printf '%s' "$S" | tr -d '\n' | grep -Fq 'first revision was published in May 2020' || exit 1
echo S018-OK quote+version+release+sig-date
```

Observed: HTML 94,680 B, SIG page 38,666 B; `positive_quote_exit=0`,
`positive_version_exit=0`, `positive_release_exit=0`, `positive_sig_date_exit=0`;
`negative_wording_exit=1` (`Coordinator: Required participant`),
`negative_date_exit=1` (`...May 2021`). The command fails closed on wording drift, version
drift and date drift.

Pinned snapshot: `sha256sum -c` over
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/S018.txt`
with `d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4` exited 0. But that
file is an 86-line normalized **excerpt**: the three role quotes are present, while
`informational purposes`, `Version 1.1` and `May 2020` are **absent** (grep counts 0). A
pinned-only recheck therefore cannot verify the source-limit or date/version claims.

Instrument state at observation: `corpus/instruments/source-recheck.py` exists (9,408 B,
mtime 2026-10-20 18:44:35 -0300) and its docstring states it verifies “captured bytes, not
current upstream availability or freshness”; the manifest the existing F06 draft names,
`corpus/source-snapshots/round-23/manifest.json`, was **absent** (no `manifest.json` anywhere
in the tree), and the draft's exact recheck command exited **2** with
`manifest UNAVAILABLE reason=missing`.

## 5. Admission risks handed to L1 (no self-credit)

- **Q3 gap in the existing draft** (`corpus/knowledge/multiparty-vulnerability-coordination.md`):
  its Limits paragraph asserts “FIRST describes best current practices” without quoting the
  Notice. Add the 7-word Notice quote with location `#Introduction`/Notice (HTML), PDF p. 3.
- **Q3 date gap:** the entry header says “version 1.1, Spring 2020” but carries no verbatim
  quote for it; add the body `Version 1.1` / `Released Spring, 2020` line or the SIG
  release-history sentence, with location.
- **Q7:** the entry's current recheck exits 2 because the manifest is absent; even once
  supplied it is a pinned-bytes check. Either land a manifest and label it as pinned (not
  fresh), or use the live command above, which names what it checked and has observed
  fail-closed controls.
- **R8:** the S018 row in `corpus/SOURCES.md` anchors only “Guiding Concepts and Best Current
  Practices”; the role definitions live in **Definitions**. A corrected/broadened anchor is a
  new row beginning “supersedes S018 —”, not an in-place edit. The row's status/used-by were
  updated `queued`→`mined` mid-observation; the immutable anchor/version text was not.
  No production edit made here.
- **Q4:** do not write “FIRST requires a coordinator” or “FIRST mandates negotiated timelines”;
  the text is “should”, and the coordinator is optional.
- **Coverage:** `corpus/README.md` still shows F06 queued; observed admitted F06–F08 count = 0.
  This report records evidence for L1's admission decision; it does not admit F06.

## 6. Remaining unknowns

- Official day-level publication date: not published (only “Spring 2020” / “May 2020”).
- Why the page title/og:title still says version 1.0: unresolved FIRST editorial inconsistency;
  the body/URL/slug/SIG/PDF all say 1.1.
- PDF internal Title is the placeholder “Document title” and Author “Pepa”; these are not
  bibliographic assertions and must not be cited as such.
- The snapshot pins an excerpt, not raw HTTP bytes; a future change outside the excerpt would
  not be detected by the pinned digest.

Tooling record: no installs or updates (nothing needed).
