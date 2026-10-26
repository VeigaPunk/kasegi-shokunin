# OASIS CSAF v2.0 VEX profile — product_status categories and the five machine-readable not-affected justification flags: the vendor's product-level assertion, not a severity, a likelihood, or a proof

source: S055 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html — capture corpus/source-snapshots/round-38/S055.txt (5,146 lines, 272,441 bytes; sha256 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42): title L1, OASIS Standard L3, date L4, TC L18, work-product components L27-L33, abstract L42, status L44, IPR mode L46, copyright L53, examples informative L498, JSON language L502, semantic scope L510/L515-L516, CVSS delegation L518/L521-L527, aggregate severity L1233/L1246, VEX definition L394, flags L1729/L1737-L1739/L1757-L1769, product_status L1855/L1887-L1894, profiles L2069-L2078, VEX profile L2134-L2156, tests 6.1.27.7 L2843-L2861, 6.1.27.9 L2876-L2877, 6.1.27.10 L2932-L2933, 6.1.33 L3095-L3097
verified-at: 2026-10-26 (quotes re-checked against the pinned capture the same day it was fetched: 2026-10-26T18:27:29Z, HTTP 200, 414,858 raw bytes)
ground: F21
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055   # prints S055:sha256 OK then one S055:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the sha256 differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

This is a standard, not a vendor report. The stage and date lines read "OASIS Standard 18 November 2022" (L3-L4); the issuing body is the `OASIS Common Security Advisory Framework (CSAF) TC` (L18), the title is `Common Security Advisory Framework Version 2.0` (L1), and the abstract is the committee's own scope statement: "the definitive reference for the language which supports creation, update, and interoperable exchange of security advisories as structured information" (L42). Approval is stated as "This document was last revised or approved by the membership of OASIS on the above date." (L44); the IPR mode as "This specification is provided under the Non-Assertion Mode of the OASIS IPR Policy" (L46); the notice as "Copyright © OASIS Open 2022. All Rights Reserved." (L53).

Everything cited below is the Technical Committee's text. Example content is not: "All examples in this document are informative only." (L498). The standard makes no claim that any vendor publishes conforming VEX documents, and it allows local profiles at the implementer's discretion: "Local or private profiles MAY exist and tools MAY choose to support them." (L2075). A claim about a named vendor's VEX practice is therefore a claim about that vendor, never an inference from this document alone (Q4).

## What CSAF v2.0 is, in the document's own scope

- A JSON language for advisories, not a scanner or a database: "The Common Security Advisory Framework (CSAF) is a language to exchange Security Advisories formulated in JSON." (L502).
- The prose is one part of a larger work product: "This prose specification is one component of a Work Product that also includes:" (L27) — the aggregator, CSAF and provider JSON schemas (L28-L33), which are not in this capture.
- A successor: "This specification replaces or supersedes:" (L35) the `CSAF Common Vulnerability Reporting Framework (CVRF) Version 1.2` (L36).
- Profile-driven, with a mandatory base: "Each CSAF document MUST conform the CSAF Base profile." (L2070), and "A profile can always add, but never subtract nor overwrite requirements defined in the profile it extends." (L2071). Profiles exist because "To ensure a common understanding of which fields are required in a given use case the standard defines profiles." (L2069).
- VEX is one profile of the standard — section `4.5 Profile 5: VEX` (L2134) — and a VEX document declares itself: "The value of /document/category SHALL be csaf_vex." (L2156). The prefix is reserved: "Values of /document/category starting with csaf_ are reserved for existing, upcoming and future profiles defined in the CSAF standard." (L2073).

## Claim 1 — VEX states affectedness per product, and the reason for it

> "The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability." — L2135

The terminology entry is narrower than the name suggests: VEX "enables a supplier or other party to assert whether or not a particular product is affected by a specific vulnerability" (L394). Two consequences come from the wording itself: the grammatical subject is a product, and the grammatical verb is `assert` — the definition says the document records an assertion, not that anything was verified.

## Claim 2 — a VEX vulnerability item must resolve to one of four product_status categories, drawn from eight

> "For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status." — L2844

`product_status` "contains different lists of product_ids which provide details on the status of the referenced product related to the current vulnerability." (L1855), and "The eight defined properties are First affected (first_affected), First fixed (first_fixed), Fixed (fixed), Known affected (known_affected)" (L1855) — with known_not_affected, last_affected, recommended and under_investigation completing the eight (L1855). Only four of the eight satisfy the profile: the mandatory test's failing example carries `first_fixed` and `recommended` alone, and its verdict is "None of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status." (L2861). So `first_affected`, `first_fixed`, `last_affected` and `recommended` may appear in a VEX document but never stand in for the required category.

The four values are version lists with distinct definitions:

- "Fixed (fixed) of value type Products (products_t) represents that these versions contain a fix for the vulnerability but may not be the recommended fixed versions." (L1887)
- "Known affected (known_affected) of value type Products (products_t) represents that these versions are known to be affected by the vulnerability." (L1888)
- "Known not affected (known_not_affected) of value type Products (products_t) represents that these versions are known not to be affected by the vulnerability." (L1890)
- "Under investigation (under_investigation) of value type Products (products_t) represents that it is not known yet whether these versions are or are not affected" (L1894)

`fixed` and `known_not_affected` are therefore different claims about different versions: a fixed version contains the fix, while a not-affected version needs no remediation — "No remediation is required regarding this vulnerability." (L1890).

## Claim 3 — known_not_affected carries an impact-statement obligation

> "For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats." — L2151-L2152

Either form satisfies it, but the human-readable form has two constraints: "the details field SHALL contain a a description why the vulnerability cannot be exploited." (L2152), and the category must be `impact` (L2152). Test 6.1.27.9 repeats the obligation in test form: "it MUST be tested that a corresponding impact statement exist in /vulnerabilities[]/flags or /vulnerabilities[]/threats" (L2877). The `impact` category is defined as "The value impact indicates that the details field contains an assessment of the impact on the user or the target set" (L2060) and, in the alternative, "or a description why it cannot be exploited." (L2060).

A flag is one product-scoped record — it "contains product specific information in regard to this vulnerability as a single machine readable flag." (L1737) — and it exists to be consumed mechanically: "These flags enable the receiving party to automate the selection of actions to take." (L1738). The labels are not local vocabulary: "The given values reflect the VEX not affected justifications." (L1762).

## Claim 4 — known_affected carries a different obligation: an action statement

> "additional product specific information SHALL be provided in /vulnerabilities[]/remediations as an action statement." — L2153

Test 6.1.27.10 makes it checkable: "it MUST be tested that a corresponding action statement exist in /vulnerabilities[]/remediations" (L2933). A missing fix is a permitted action statement, not a silent status change: "The use of the categories no_fix_planned and none_available for an action statement is permitted." (L2154). And `known_affected` itself recommends action: "Actions are recommended to remediate or address this vulnerability." (L1888).

## Claim 5 — the five labels, each with the standard's one-line meaning

The enum has exactly five values (L1757-L1761), and the standard supplies one meaning per value (L1763-L1769):

| label | the standard's meaning | line |
|---|---|---|
| `component_not_present` | "The software is not affected because the vulnerable component is not in the product." | L1763 |
| `vulnerable_code_not_present` | "The product is not affected because the code underlying the vulnerability is not present in the product." | L1764 |
| `vulnerable_code_cannot_be_controlled_by_adversary` | "vulnerable code is used in such a way that an attacker cannot mount any anticipated attack." | L1766 |
| `vulnerable_code_not_in_execute_path` | "The affected code is not reachable through the execution of the code, including non-anticipated states of the product." | L1767 |
| `inline_mitigations_already_exist` | "Built-in inline controls or mitigations prevent an adversary from leveraging the vulnerability." | L1769 |

The two `not present` labels are not interchangeable, and the standard draws the line itself: with `vulnerable_code_not_present` "the component in question is present, but for whatever reason (e.g. compiler options) the specific code causing the vulnerability is not present" (L1765). The reachability label covers more than one call path — execution "including non-anticipated states of the product" (L1767) — and concerns "Components that are neither used nor executed by the product." (L1768). The mitigation label claims a control, not the absence of the defect (L1769).

## Claim 6 — one justification per product, and product groups may carry it

> "it MUST be tested that a Product is not member of more than one Flag item with a VEX justification code" — L3096

That is the substance of test 6.1.33 (L3095-L3097): a vendor cannot publish two competing not-affected reasons for the same product. The rule is deliberately forward-compatible: "Additional flags with a different purpose might be provided in later versions of CSAF." (L3097).

Group-level statements are allowed but do not relax per-product coverage — the standard requires that "for each Product ID the required information according to its product status as stated in the two points above is available" (L2155), which it spells out as "all products with the status known_not_affected MUST have an impact statement" (L2155).

## Claim 7 — the standard validates presence, not truth

> "the use of JSON schema allows validation and proof of model conformance" — L510

Schema validation is structural, and content consistency is the producer's job: "Consistency on the content level thus is in the responsibility of the producer of such documents" (L515). Semantic checking is explicitly outside the specification: "any deep validation on a semantic level (e.g. does the CWE match the described vulnerability) is to be ensured by the producer" (L516), and "It is out of scope for this specification." (L516). A conforming VEX flag therefore establishes that a justification of the required shape was published — not that the justification is correct.

## How a bounty or security researcher uses it

1. **Read the vendor's VEX before disputing a not-applicable decision or filing a duplicate.** Find the vulnerability item, then the `product_id` for the exact version under test; statuses are per-version lists (L1855, L1885-L1894), and products resolve through `/product_tree`, "which lists all products referenced later on in the CSAF document regardless of their state." (L2139). A statement about one version says nothing about another.
2. **Separate affected from not affected mechanically.** At least one of the four categories must be present (L2844); `fixed` is not `known_not_affected` (L1887 versus L1890); `under_investigation` means the answer is not known yet (L1894), not that the product is clean.
3. **For `known_not_affected`, read the justification, not just the category.** It may be a flag (L1737) or a `threats` entry with category `impact` (L2877, L2152), and a group-level statement can cover many product IDs (L2155).
4. **Check the flag's specific reason against the product.** The label fixes what the vendor is claiming (L1763-L1769): `component_not_present` is a claim about the component set — the reason VEX is "especially helpful in efficiently consuming SBOM data" (L394); `vulnerable_code_not_present` concedes the component is present (L1765); `vulnerable_code_not_in_execute_path` claims unreachability across "non-anticipated states of the product" (L1767); `inline_mitigations_already_exist` claims a built-in control (L1769). Each is checkable against the code or the dependency inventory; none is proof on its own (L516).
5. **For `known_affected`, read the action statement.** An affected product needs one in `remediations` (L2933), and `no_fix_planned` / `none_available` are legitimate answers (L2154) — the absence of a patch does not retract affectedness.
6. **Do not treat the VEX as a verdict on your report.** It is the vendor's product-level assertion (L394), and semantic verification is out of scope for the standard (L516); the lane's reading is that a program's scope call or duplicate decision stays with the program.

## Sources overlap — CSAF VEX against CVSS (F01), KEV (F18), EPSS (F19) and SSVC (F20)

On the normalized capture `CVSS` occurs 73 times and `EPSS`, `KEV` and `SSVC` occur 0 times each. Lane analysis, not a quote: VEX says whether and why a product version is affected; F01's CVSS scores severity, F18's KEV lists exploited vulnerabilities, F19's EPSS estimates exploitation probability, F20's SSVC emits a stakeholder priority decision — none of those is a product-status category, and this document defines none of them.

- **CVSS is delegated, not redefined.** Under "Delegation to industry best practices technologies" (L518) the standard lists "Common Vulnerability Scoring System (CVSS) Version 3.1 [CVSS31]" (L522) and the v3.0/v2.0 schemas (L521-L527); score objects carry CVSS values "abiding by the schema at https://www.first.org/cvss/cvss-v2.0.json." (L2026).
- **The product status constrains the score, not the reverse:** "A score object SHOULD reflect the associated product's status" (L2028).
- **CSAF's own severity field is not a scale.** The range of `aggregate_severity` is producer-defined — "The range of values in this field is defined according to the document producer's policies and procedures." (L1233) — and it is document-level: "It is a document-level metric and applied to the document as a whole — not any specific vulnerability." (L1233). Its text "provides a severity which is independent of - and in addition to - any other standard metric" (L1246).
- **The nearest exploitation field is prose.** `threats` category `exploit_status`: "The value exploit_status indicates that the details field contains a description of the degree to which an exploit for the vulnerability is known." (L2059) — a narrative field, not a probability, and not part of `product_status`; the captured bytes never mention EPSS, KEV or SSVC.

## Falsifiable rule and checks

**Falsifiable rule.** A statement about a CSAF VEX document is falsified by any of: (a) reading `known_not_affected` as proof of non-exploitability, when it is a party's assertion (L394) and semantic validation is out of scope (L516); (b) treating `fixed` as equivalent to `known_not_affected`, when the standard defines them separately (L1887, L1890); (c) saying a VEX item needs only `first_affected`, `first_fixed`, `last_affected` or `recommended`, when 6.1.27.7 requires one of four other values (L2844, L2861); (d) saying a `known_not_affected` product needs no impact statement, when the profile requirement and test 6.1.27.9 demand one (L2152, L2877); (e) saying an unfixed `known_affected` product may omit an action statement, when 6.1.27.10 requires one and `no_fix_planned` / `none_available` are permitted categories (L2933, L2154); (f) presenting a CSAF document as carrying a CSAF-defined severity scale or exploitation probability, when the severity text is producer-defined (L1233) and EPSS, KEV and SSVC never occur; (g) assigning two not-affected justifications to one product, when 6.1.33 forbids it (L3096).

**FC-1 — every quoted span is verbatim, ≤25 words, on its declared line.** Observed `spans 70 distinct 68 words_max 25 anchors_ok 70 of 70`: two of the 68 distinct spans occur twice in the capture (the IPR-mode sentence at L46 and L321, the `/product_tree` requirement at L2127 and L2139) and each carries the anchor of the occurrence meant here; the other 66 occur exactly once (quote table and command in the seat receipt).

**FC-2 — vocabulary.** Counting with `grep -oF <word> S055.txt | wc -l`: `score=101 scoring=2 severity=15 CVSS=73 product_status=79 known_not_affected=18 known_affected=21 under_investigation=12 csaf_vex=10 VEX=21 EPSS=0 KEV=0 SSVC=0`; all 15 `severity` hits are `aggregate_severity` or the terminology example (L381), none a CSAF-defined scale.

**FC-3 — the label enum has five values.** `sed -n '1757,1761p'` returns `component_not_present`, `inline_mitigations_already_exist`, `vulnerable_code_cannot_be_controlled_by_adversary`, `vulnerable_code_not_in_execute_path`, `vulnerable_code_not_present` — five lines, no sixth.

**FC-4 — the four required categories and the failing example.** `grep -n 'at least one of the elements fixed, known_affected'` returns L2844; the example at L2852-L2861 carries `first_fixed` and `recommended` only and is labelled `Example 82 which fails the test` (L2852).

**FC-5 — the two obligations sit on different statuses.** `grep -n 'known_not_affected an impact statement'` returns L2152 and `grep -n 'known_affected additional product specific information'` returns L2153; the tests at L2877 and L2933 repeat each obligation.

**FC-6 — the neighbour axes are absent.** The same `grep -oF | wc -l` count gives `EPSS=0`, `KEV=0`, `SSVC=0` and `CVSS=73`; among scoring systems the reference list names only CVSS (L522), and no field in `product_status` accepts a probability, a catalog membership or a priority decision.

## Rejected over-generalizations

1. **VEX tells you whether the vulnerability is exploitable.** Rejected: the profile's stated purpose is affectedness — "The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability." (L2135) — and the only exploitation-shaped field, `threats`/`exploit_status`, is a free-text description (L2059), not part of `product_status`.
2. **`known_not_affected` means the finding is invalid or the program need not pay.** Rejected: the value records that a party asserts the versions are "known not to be affected by the vulnerability" (L1890); the standard tests for the presence of a justification, not its truth (L2877, L516), so a finding has to be argued against the specific label (L1763-L1769).
3. **`fixed` and `known_not_affected` are the same thing.** Rejected: `fixed` is about versions containing a fix (L1887), `known_not_affected` is about versions needing no remediation (L1890), and 6.1.27.7 lists them as separate acceptable categories (L2844).
4. **A VEX flag is a CVE-level verdict.** Rejected: `product_status` "contains different lists of product_ids which provide details on the status of the referenced product" (L1855), and a flag's scope is product- or group-scoped (L1737). One vulnerability item can carry different statuses for different products.
5. **CSAF defines a severity score.** Rejected: numeric scores are CVSS objects validated against FIRST schemas (L2026-L2028), and the aggregate severity text has a producer-defined range (L1233).
6. **Every not-affected product must carry a flag.** Rejected: the requirement accepts a human-readable justification in `threats` with category `impact` (L2152), and 6.1.27.9 accepts either location (L2877).
7. **All vendors publish VEX.** Rejected: the standard defines profiles and allows local or private ones (L2075); it makes no adoption claim, so vendor practice is a separate, vendor-specific source.
8. **The examples are normative.** Rejected: "All examples in this document are informative only." (L498), including the group-coverage illustration at L2931.

## Honest limit

- **Prose specification only.** The three JSON schemas are separate work-product components (L28-L33) and are not in this capture; type and enum facts quoted here are the prose's statements, and the standard delegates schema conformance to validation (L510).
- **One stage pinned.** This is the `os` stage dated 18 November 2022 (L3-L4); the status block names "possible later revisions of this document" (L44), so a later stage is a new pin, not a correction.
- **Normalized lines, and split sentences.** Line numbers are lines of the normalized capture, not PDF pages. The profile's two requirement sentences share the `For each item in` lead-in on L2151 and finish on L2152 (impact statement) and L2153 (action statement), so those quotes match only after the declared whitespace normalization.
- **The document's own typos are preserved inside quotes.** L2152 reads `contain a a description`; L2155 reads `MAY also be provide`; L2071 reads `indirect through`. A quote that silently repaired them would not match the capture.
- **Not a compliance finding about any vendor.** Nothing here asserts that a named vendor's VEX is wrong; the standard's rules describe what a document must contain, and only the document in hand can be tested against them.
- Documentation only: the capture holds public web text, no credential, session or private URL, and this entry quotes none (Q6). Nothing here authorizes probing, scanning, logging in to, or submitting against any target.
