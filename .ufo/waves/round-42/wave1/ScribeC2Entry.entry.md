# CVE JSON record format (the CVE Record Format) — the bundled JSON Schema behind every CVE Record: two mutually exclusive shapes (Published, Rejected), one `cna` container plus optional `adp` containers, a three-value version `status` whose default is `unknown`, and CVSS scores inside `metrics[]` rather than a record-level severity

source: S064 — https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json — capture corpus/source-snapshots/round-42/S064.txt (3,545 lines, 84,520 bytes; sha256 b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa): the complete bundled JSON Schema draft-07 document, no slice — `$schema` L2, `$id` L3, title L4, top-level description L5, `definitions` L6-L3462, root `oneOf` L3463-L3544 with the Published branch L3464-L3507 and the Rejected branch L3508-L3543; `status` L128, `product` L137-L470 (`defaultStatus` L343, `versions` L347, `packageURL` L448), `dataType` L472, `dataVersion` L479, `cveMetadataPublished` L485, `cveMetadataRejected` L537, `providerMetadata` L589, `cnaPublishedContainer` L692, `cnaRejectedContainer` L777, `adpContainer` L808, `affected` L887, `references` L1023, `impacts` L1048, `metrics` L1075 (cvssV4_0 L1143, cvssV3_1 L1905, cvssV3_0 L2460, cvssV2_0 L3015, other L3188); the three Gate pins are Q1 L5, Q2 L3466, Q3 L3510
verified-at: 2026-10-28 (fetched this day: the capture_url above, HTTP 200, 133,616 raw bytes, 3,545 raw lines, sha256 44c703322b1fcc532bc1c93f3993a0ba042c1a2831aae8cf39c4fbb707d03c8f at 2026-10-28T11:06:45Z; the instrument's own second fetch at 2026-10-28T11:09:10Z returned the same 133,616 bytes and the identical snapshot sha256 — the served raw body and the capture are both stable across those two fetches; the capture is `capture-source.py --kind text`'s collapse of that body — 3,545 lines, 84,520 bytes, sha256 b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa — and every quote here is pinned to the capture, not to what the URL serves next)
ground: F25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-42/manifest.json --source S064   # prints S064:sha256 OK then one S064:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved — a pinned-capture comparison, not a fresh network check

## Attribution

This is the CVE Program's own schema file (`cve-schema`), and the capture is the whole document, not a slice: 3,545 served lines equal 3,545 capture lines, because `collapse()` removes only the JSON indent runs. The document is a bundled JSON Schema draft-07 file: its only prose is the `description` strings, and its normative content is structure — `required` arrays, `enum` lists, `pattern` strings and `$ref`s. L4's title names the format, L3's `$id` is the schema's canonical identifier, and L5 calls it the blueprint for data that CNAs and Authorized Data Publishers submit.

Lane reading, not a quote: this document defines the field syntax and the required sets; the CNA Rules (F07) define what content a CNA must supply and require the use of approved formats — Claim 6 draws the seam against the S031 capture. Lane reading, not a quote: before this round no lane row or knowledge entry covered this document — `grep -rniE 'cve-schema|CVE Record Format|cveMetadata|CVE JSON'` over corpus/knowledge, corpus/SOURCES.md, corpus/README.md, PROVINCE.md and every capture manifest returned 0 hits, and the sibling-lane knowledge grep for the same family returned 0 files (both commands in the seat receipt).

## Claim 1 — the document is a JSON Schema, and the format version travels inside each record, defaulting to 5.2.0

> "cve-schema specifies the CVE JSON record format. This is the blueprint for a rich set of JSON data" — S064.txt:L5

`dataType` is an enum with exactly one value, `CVE_RECORD` (L472-L477; value L476), so a document that does not declare it is not a CVE Record. `dataVersion` (L479-L484) is a string whose `pattern` accepts any 5.x — major-only, x.y or x.y.z (L482) — and whose `default` is `5.2.0` (L483): the schema validates a version family and names one default, not a fixed edition.

> "The version of the CVE schema used for validating this record. Used to support multiple versions of this format." — S064.txt:L480

Both root branches require exactly four properties — `dataType`, `dataVersion`, `cveMetadata`, `containers` (Published L3500-L3505, Rejected L3536-L3541) — so a CVE Record is the four-key object or it is not one. The key set is closed in both branches (`additionalProperties: false`, L3506 and L3542).

## Claim 2 — the product side is a three-value `status` with an `unknown` default, and a version entry is one version or a range with a declared numbering system

> "The status 'unknown' indicates that it is unknown or unspecified whether the given version is affected." — S064.txt:L129

`status` is an enum of exactly three values — `affected` L132, `unaffected` L133, `unknown` L134 (L128-L136) — and the same description names an investigation not undertaken and a vendor not disclosing the status among the reasons an 'unknown' status can exist (L129). The schema records no reason and no investigation state: `unknown` is the absence of a claim, not a claim.

> "If not specified, defaultStatus defaults to 'unknown'. Versions or defaultStatus may be omitted, but not both." — S064.txt:L344

`versions` is an array of one `oneOf` four shapes (L355-L386): `{version,status}` with `maxProperties` 2; `{version,status,versionType}` capped at 3; `{version,status,versionType,lessThan}`; `{version,status,versionType,lessThanOrEqual}`. A range therefore cannot be read without its `versionType` (L397-L410; examples `custom`, `git`, `maven`, `python`, `rpm`, `semver` at L402-L409), because the comparison semantics belong to that value.

> "An entry with only 'version' and 'status' indicates the status of a single version." — S064.txt:L354

> "clients must re-sort the list themselves rather than assume it is sorted." — S064.txt:L421

`changes` (L419-L446) refines a status inside a range, and the schema tells clients not to trust its order. `packageURL` is a purl with one hard rule attached:

> "The Package URL MUST NOT include a version." — S064.txt:L449

The default is the sharpest difference from the lane's CycloneDX ground: CycloneDX's version status default is `affected` (`S060.txt:L105`), so the same omission asserts the opposite in the two formats. A reader who assumes an omitted status means affected is wrong here (Rejected over-generalization 4).

## Claim 3 — every record has exactly one `cna` container, and only the Published shape admits `adp` containers

> "At a minimum, a 'cna' container containing the vulnerability information provided by the CNA who initially assigned the CVE ID must be included." — S064.txt:L3479

The Published `containers` object (L3478-L3497) has two properties — `cna` (ref `cnaPublishedContainer`, L3482-L3484) and `adp` (array of `adpContainer`, `minItems` 1, `uniqueItems`, L3485-L3492) — and requires `cna` (L3494-L3496). The Rejected `containers` object (L3522-L3534) has one property, `cna` (ref `cnaRejectedContainer`, L3526-L3528), and requires it (L3530-L3532); there is no `adp` key in that branch, so a rejected record cannot carry an ADP container at all.

`providerMetadata` (L589-L610) is the only required member of every container's provider block (`required: [orgId]`, L606-L608): each container names its provider by the CVE program's organization UUID, `shortName` is optional, and `dateUpdated` is replaced by the system of record at submission (L601-L604).

> "an ADP container must indicate which ADP is the source of the information in the object" — S064.txt:L809

The ADP container additionally requires `minProperties` 2 (L877-L880), so repeating `providerMetadata` alone does not make a container. The published CNA container's required set is four fields — `providerMetadata`, `descriptions`, `affected`, `references` (L765-L769).

> "The CNA container must include the required information defined in the CVE Rules" — S064.txt:L693

That sentence is also the seam: the schema defers content requirements to the CNA Rules while fixing the field set that carries them (Claim 6).

## Claim 4 — `state` is a one-value enum per shape, and a record moves between shapes rather than listing states

> "When a CNA populates the data associated with a CVE ID as a CVE Record" — S064.txt:L3466

The root `oneOf` (L3463) has exactly two branches — Published (L3464-L3507) and Rejected (L3508-L3543) — and the branch is selected by `cveMetadata` (refs at L3475-L3477 and L3519-L3521). The Published metadata `state` enum contains exactly one value, `PUBLISHED` (L527-L533; value L531); the Rejected metadata `state` enum contains exactly one value, `REJECTED` (L575-L580; value L579) and adds `dateRejected` (L571-L573). Both metadata shapes require the same three fields — `cveId`, `assignerOrgId`, `state` (Published L488-L492, Rejected L540-L544).

The transition is described in prose, not as an enum: `serial` increments on each change, and its description says the incremented value moves to the Rejected schema on a PUBLISHED->REJECTED transition and to the Published schema on a REJECTED->PUBLISHED transition (L516). So the current state is the shape you are reading and the number of changes is `serial`; there is no field that enumerates affected / under-investigation the way CSAF's `product_status` does (Claim 7, FC-2).

## Claim 5 — scores live in `metrics[]` as four CVSS shapes or a non-standard `other` block, scoped by scenario and attributed to the container

> "Collection of impact scores with attribution." — S064.txt:L1077

The `metrics` definition (L1075) is an array of objects whose `anyOf` requires exactly one of five keys: `cvssV4_0` (L1086, schema at L1143), `cvssV3_1` (L1091, schema at L1905), `cvssV3_0` (L1096, schema at L2460), `cvssV2_0` (L1101, schema at L3015) or `other` (L1106, schema at L3188). Each CVSS block is itself a draft-07 schema with its own title (L1145, L1907, L2462, L3017).

> "Must contain: At least one entry, can be text, CVSSv2, CVSSv3, others may be added." — S064.txt:L1082

A metric object may name a `format` (L1111-L1116) and carries `scenarios` (L1117-L1141) whose `value` defaults to `GENERAL` (L1130) — the scope is a scenario string, not a product list. The non-standard shape is explicit:

> "A non-standard impact description, may be prose or JSON block." — S064.txt:L3190

There is no record-level severity property: `severity` occurs 11 times in the capture — three CVSS `severityType` definitions (L1592, L2152, L2832), seven `$ref`s to them, and one unrelated word in a credits description (L3305). A record can therefore carry several scores from several containers, including prose ones, and no field picks the authoritative one.

## Claim 6 — the seam with the CNA Rules: the format defines the fields, the rules require the content and mandate the format

> "MUST meet any requirements set by any approved formats or submission mechanisms, for example, the CVE Record Format" — S031.txt:L112

The CNA Rules capture states that requirement for CNAs (`S031.txt:L112`) and, for rejection, requires the program's formats and an explanation (`S031.txt:L102`). This schema supplies those formats: it fixes `required` sets, `enum` values and `pattern`s, and it points back at the rules for what must be inside the required fields (L693). Read as a pair, the rules answer what a CNA must say and this document answers where and in what shape it goes; neither alone is the whole rule. Reading this schema as the source of CNA obligations — or the CNA Rules as the field dictionary — is the misreading Rejected over-generalization 1 rejects.

## Claim 7 — this schema is not a VEX vocabulary, not CSAF, and not CycloneDX

The capture contains no VEX vocabulary at all: `VEX` 0, `product_status` 0, `known_affected` 0, `not_affected` 0, `under_investigation` 0, `justification` 0, `CSAF` 0, `CycloneDX` 0, `SBOM` 0 (FC-2). The nearest thing it has is the version `status` enum (Claim 2), which is a per-version affectedness value, not a per-product VEX status with a justification flag.

The lane already holds the VEX vocabulary at F21: CSAF requires, for `product_status` / `known_not_affected`, that an impact statement "SHALL exist as machine readable flag" (`S055.txt:L2151`). This schema has no equivalent field and no `justification` value list. F23's CycloneDX `analysis` object (`S060.txt:L5-L15`) carries an analyst decision with six states and a `should` justification; neither concept exists here.

Rejection is the one state this document models in full: the Rejected branch (L3508-L3543) requires the rejected container's `rejectedReasons` (L798-L801) and permits `replacedBy` (L788-L800):

> "An object containing the vulnerability information provided by a CVE Numbering Authority (CNA) for a rejected CVE ID." — S064.txt:L778

> "Contains an array of CVE IDs that this CVE ID was rejected in favor of because this CVE ID was assigned to the vulnerabilities." — S064.txt:L790

> "A Rejected CVE Record remains on the CVE List so that users can know when it is invalid." — S064.txt:L3510

So a rejected ID is a record that states why it is invalid and what replaced it — never a deletion.

## How a bounty or security researcher uses it

1. **Read `dataType` and `dataVersion` before the finding.** A CVE Record is `CVE_RECORD` (L476) at some 5.x (L482); the `5.2.0` on L483 is the schema's default, not a promise that the record you hold was written to it, and both root branches require the key (L3500-L3505, L3536-L3541).
2. **Read `cveMetadata.state` next.** REJECTED (L579) means the ID is not to be used; the rejection carries `rejectedReasons` (L798-L801) and may carry `replacedBy` (L788-L800), so the correct follow-up is the replacement ID, not a resubmission.
3. **Then the version answer, with its range.** `affected[]` entries carry `versions[]` with a three-value `status` (L131-L135); a version entry is either a single version (L354) or a range that is uninterpretable without its `versionType` (L397-L410) and exactly one of `lessThan` / `lessThanOrEqual` (L411-L418).
4. **Read `unknown` as "no claim", never "clean".** The description lists possible reasons for `unknown` without recording which applies (L129), and `defaultStatus` defaults to `unknown` (L344). A record that names a product and omits versions has asserted nothing about versions.
5. **Read `metrics[]` per container and keep the format with the number.** One record can carry CVSS v2.0, v3.0, v3.1, v4.0 and `other` blocks (L1086-L1106), scoped by scenario (L1117-L1141) and attributed to the container's provider (L589-L610). Quoting "the CVSS" of a CVE ID without the container and the format is not reproducible from the record.
6. **Treat `unaffected` as a version fact only.** It is one enum value (L133) beside `affected` and `unknown`; the schema carries no VEX justification, no not-affected reason list and no statement about testing permission (FC-2).
7. **Do not read this document as what a CNA is obliged to publish.** The obligations are the CNA Rules' (`S031.txt:L112`, `S031.txt:L102`); this schema fixes the field set those obligations land in and even defers content requirements back to the rules (L693).

## Comparison with S055 (CSAF v2.0 VEX) and S060 (CycloneDX v1.7 `analysis`)

| question | this schema (S064) | CSAF VEX (S055) | CycloneDX analysis (S060) |
|---|---|---|---|
| product-status vocabulary | none; version `status` enum of 3 (L131-L135) | `product_status` with `known_not_affected` and the rest; a machine-readable flag is required for that status (`S055.txt:L2151`) | `analysis.state` enum of 6 and `justification` of 9 (`S060.txt:L5-L29`) |
| justification field | absent (`justification` 0, FC-2) | flag or justification obligation for `known_not_affected` (`S055.txt:L2151`) | `justification` under a `should` obligation (`S060.txt:L15`) |
| version-status default | `unknown` (L344) | status lives in `product_status` lists, not in a version default | `affected` (`S060.txt:L105`) |
| severity | `metrics[]`, five shapes including `other` (L1086-L1106) | the VEX document's own scoring layer | `analysis` carries no score |

The table is a reading of three pinned captures; nothing in it says a producer emits all three documents for the same CVE ID.

## Falsifiable rule and checks

**Falsifiable rule.** Any statement about this document is falsified by: (a) naming a top-level property other than `dataType`, `dataVersion`, `cveMetadata`, `containers`, when both root branches require exactly those four (L3500-L3505, L3536-L3541); (b) calling `state` a multi-value status field, when each metadata shape's enum holds exactly one value (L530-L533, L578-L580); (c) reading an omitted version status as `affected`, when `defaultStatus` is `unknown` (L344); (d) attributing a VEX justification or not-affected flag to this schema, when that vocabulary occurs zero times (FC-2); (e) naming a record-level severity, when the only severity vocabulary is CVSS-internal `severityType` (L1592, L2152, L2832) and metrics are per-container (L1075-L1106); (f) claiming a single point version, when `dataVersion` accepts any 5.x and defaults to 5.2.0 (L482-L483).

**FC-1 — every quoted span is verbatim, ≤25 words, exactly once, on its declared line.** Under whitespace collapse, each anchored blockquote span occurs exactly once in the capture and its declared line holds it; the longest is 24 words (`replacedBy`, L790). The obligations are measured, not asserted: uppercase `MUST` 2, `MUST NOT` 1, `SHALL` 0, `SHOULD` 0, `MAY` 0; lowercase `should` 10 and `may` 10 in descriptions — the schema binds through `required`, `enum` and `pattern`, not through prose verbs. The only quoted spans in this entry that are not from this capture are the rejected over-generalization labels, which are assertions a reader might make, not source text.

**FC-2 — vocabulary census.** `grep -oF <word> S064.txt | wc -l` gives `VEX=0 product_status=0 known_affected=0 not_affected=0 under_investigation=0 justification=0 CSAF=0 CycloneDX=0 SBOM=0`; the same command gives `severity=11 score=17 CVSS=14 adp=9 cna=17 PUBLISHED=9 REJECTED=9`.

**FC-3 — the enum sizes are counted, not remembered.** `dataType` L475-L477 (1 value), `status` L131-L135 (3), published `state` L530-L533 (1), rejected `state` L578-L580 (1), reference `tags` L50-L70 (19 values at L51-L69), `metrics` shapes L1086-L1106 (5), `versionType` examples L402-L409 (6). A count script over the lines between each `"enum": [` and its closing `]` reproduces each number.

**FC-4 — the required sets are counted.** Root L3500-L3505 and L3536-L3541 (4); metadata L488-L492 and L540-L544 (3); published CNA container L765-L769 (4: `providerMetadata`, `descriptions`, `affected`, `references`); rejected CNA container L798-L801 (2: `providerMetadata`, `rejectedReasons`); `providerMetadata` L606-L608 (1: `orgId`); ADP container L877-L880 (`required: [providerMetadata]` plus `minProperties: 2`).

**FC-5 — the Rejected branch has no `adp` key.** `sed -n '3522,3534p' S064.txt` shows `properties` with `cna` only and `required: [cna]`; the same range contains no `"adp": {`.

**FC-6 — the two defaults point opposite ways.** `sed -n '344p' S064.txt` gives `unknown`; `sed -n '105p' corpus/source-snapshots/round-40/S060.txt` gives the CycloneDX status default `affected` (F23's capture). The same omission therefore means different things, and no cross-format shortcut is safe.

**FC-7 — the capture is the whole document, not a slice.** `wc -l` gives 3,545, `wc -c` gives 84,520, `sha256sum` gives `b90a51f7…`, and the manifest records `lines == full_text_lines` with indent collapse as the only transformation.

## Rejected over-generalizations

1. **"The CNA Rules define the CVE Record's fields."** Rejected: `S031.txt:L112` requires CNAs to meet requirements set by approved formats, and the field definitions are in this schema (L4-L5 and every `required` / `enum` block cited above); the schema in turn points content requirements back at the rules (L693). The rules and the format are two documents with two jobs.
2. **"A CVE Record has a severity."** Rejected: `severity` occurs 11 times, three as CVSS `severityType` definitions (L1592, L2152, L2832), seven as `$ref`s to them, one in a credits sentence (L3305); both root branches allow only four top-level properties (L3500-L3505, L3536-L3541). Scores live in `metrics[]` and may be prose (`other`, L3188-L3190).
3. **"`status: unaffected` is a VEX not-affected statement."** Rejected: `VEX`, `product_status`, `known_affected`, `not_affected` and `justification` occur zero times (FC-2); CSAF attaches a required machine-readable flag to its not-affected status (`S055.txt:L2151`), and this schema has no such field or flag list.
4. **"An omitted version status means the version is affected."** Rejected: `defaultStatus` defaults to `unknown` (L344), the opposite of the CycloneDX default (`S060.txt:L105`).
5. **"A rejected CVE ID is deleted."** Rejected: the Rejected branch keeps the record on the CVE List (L3510), requires `rejectedReasons` (L798-L801) and allows `replacedBy` (L788-L800).
6. **"`state` records investigation status or severity."** Rejected: each metadata shape's `state` enum holds exactly one value (L530-L533, L578-L580); changes are counted by `serial` (L516), not enumerated as states.
7. **"This document specifies CVE Record Format 5.1.1."** Rejected: `dataVersion`'s pattern accepts any 5.x (L482) and its default is 5.2.0 (L483); the capture names no single point version.

## Honest limit

- **Full document, one fetch pair.** The capture is the complete bundled schema, 3,545 lines / 84,520 bytes / sha256 `b90a51f7…`; the raw body was 133,616 bytes and stable across the two fetches recorded in the `verified-at:` line, and `recheck:` compares the pinned capture, not the network.
- **Schema, not prose.** The document's only prose is its `description` strings; a claim here is about field syntax, required sets and enum values, not about how a CNA fills them. Content obligations belong to the CNA Rules (S031).
- **No edition or ratification statement in the capture.** The file carries `$schema` draft-07 (L2), a `$id` (L3) and no release note; the URL path is `.../main/schema/docs/...`, so `main` is the only version pointer, and `5.2.0` is the schema's own `default`, not a published edition claim.
- **Raw bytes and snapshot differ by design.** `collapse()` drops indent runs: 133,616 raw bytes become 84,520 snapshot bytes at the same 3,545 lines; the manifest records both digests, and a semantic no-op reformat upstream would move the raw digest while the snapshot digest is what this entry pins.
- **No producer practice is asserted.** Nothing here says any CNA or ADP tool emits a conforming record, that any published CVE Record validates against this schema, or that a given vendor supplies a `metrics` block; the document defines fields.
- **Conformance level.** JSON Schema draft-07 validates instances; the lowercase `must`/`may` sentences are prose inside descriptions, and the structural constraints are `required`, `enum`, `pattern`, `minItems`, `uniqueItems` and `additionalProperties: false` — none of them is a vendor process rule.
- Documentation only: the capture is public reference text (no credential, session or private URL), and this entry quotes none.
