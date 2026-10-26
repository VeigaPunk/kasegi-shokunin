# ExecSchemaCross — CSAF v2.0 JSON schema ↔ specification enumeration cross-verification

Seat: ExecSchemaCross (leaf). Round 38, lane `kasegi-shokunin`, base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`.
Writes: this receipt only (`.ufo/waves/round-38/wave1/ExecSchemaCross.md`); no deliverable file, no lane file edited,
no mutating git command, no tool installed.
Item: cross-verify the C2 F21 entry's enumerations — (a) `product_status` property names, (b) `flags` label enum,
(c) `threats` category enum, (d) `remediations` category enum — against the machine-readable CSAF v2.0 JSON schema,
then against the OASIS Standard prose. Receipt only; this file is the only lane write.

**Verdict: `mismatch_count = 0`, on both legs.** (i) All four enumerations agree value-for-value *and* order-for-order
between the OASIS-published JSON schema and the OASIS Standard prose: 8 `product_status` property names, 5 `flags.label`
values, 3 `threats.category` values, 5 `remediations.category` values. (ii) The landed C2 entry
(`corpus/knowledge/csaf-vex-product-status-and-justifications.md`, sha256 `0343ef45…`) uses only those 21 values — no
misspelling, no foreign token — citing all 8 status names and all 5 labels and a declared subset of the other two.
Two *strictness* gaps exist (the schema is looser than the prose), and the spec itself routes both to conformance tests
rather than the schema (§6.2.20, §6.1.33). They are **not** enumeration mismatches, but they bound what the F21 entry may claim: "schema-valid" is not "closed" for
`product_status` keys, and schema `uniqueItems` does not implement §6.1.33.

## 1. Fetch provenance

Fetches run with the mandated UA and timeouts (`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`).

| # | URL | HTTP | fetched bytes | UTC | sha256 of stored body |
|---|-----|------|---------------|-----|----------------------|
| 1 | https://docs.oasis-open.org/csaf/csaf/v2.0/os/schemas/csaf_json_schema.json | 200 | 57152 | 2026-10-26T18:27:20Z | `29c114b35b0a30831f1674f2ab8b3ed9b2890cfeaa63b924ac6ed9d70ef44262` |
| 2 | https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html | 200 | 414858 | 2026-10-26T18:27:20Z | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` |
| 3 | https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.md (the variant this stage labels *Authoritative*, spec.txt:5-6) | 200 | 294479 | 2026-10-26T18:38:50Z | `5bc757cc8dcf1a48a73c50de8100b0437bda1f9b5b860afd051c585749f568be`; normalized text sha256 `c2875f14a5f9cbcff37557cad37a5573182514231ab534010ba1c4ec357a1c77` (5437 lines) |
| 4 | https://docs.oasis-open.org/csaf/csaf/v2.0/csaf_json_schema.json (the schema's own `$id`, "latest stage") | 200 | 57152 | 2026-10-26T18:28:47Z | `29c114b35b0a30831f1674f2ab8b3ed9b2890cfeaa63b924ac6ed9d70ef44262` (byte-identical to #1) |

- The schema URL was **not** moved: it is exactly the one the spec advertises at `spec.txt:30`
  (`CSAF JSON schema: https://docs.oasis-open.org/csaf/csaf/v2.0/os/schemas/csaf_json_schema.json.`); the
  "latest stage" line follows at `spec.txt:31`.
- The fetched schema's `$id` is `https://docs.oasis-open.org/csaf/csaf/v2.0/csaf_json_schema.json`
  (`spec.txt:542` carries the same identifier verbatim), `$schema` is
  `https://json-schema.org/draft/2020-12/schema`, `title` is `Common Security Advisory Framework`, `$defs` holds 11
  definitions. Fetch #4 proves the OS-published copy and the `$id` copy are the same bytes today, so there is no
  enum drift between the spec's two advertised schema locations.
- Spec identity: `Common Security Advisory Framework Version 2.0` / `OASIS Standard` / `18 November 2022`
  (`spec.txt:1-4`).
- Normalization: `corpus/instruments/capture-source.py`'s `html_to_text()` (tags stripped, entities decoded, each line
  whitespace-collapsed, blank lines dropped) — the same instrument that produces committed `S05x.txt` snapshots.
  Result: 5146 lines, 272441 bytes, sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`.
  All anchors below are 1-based line numbers in **that** normalized text, which is **byte-identical** to the committed
  round-38 capture `corpus/source-snapshots/round-38/S055.txt` (`cmp` clean; both sha256
  `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`, 5146 lines, 272441 bytes), so every anchor is
  also a line of the artifact the entry cites.

## 2. The four enumerations

### (a) `product_status` property names — schema pointer `$/properties/vulnerabilities/items/properties/product_status/properties`

Prose: §3.2.3.9 (`spec.txt:1854`), enumeration sentence `spec.txt:1855`, JSON block `spec.txt:1856-1883`.

| # | value | spec anchor |
|---|-------|-------------|
| 1 | `first_affected` | spec.txt:1855, 1859 |
| 2 | `first_fixed` | spec.txt:1855, 1862 |
| 3 | `fixed` | spec.txt:1855, 1865 |
| 4 | `known_affected` | spec.txt:1855, 1868 |
| 5 | `known_not_affected` | spec.txt:1855, 1871 |
| 6 | `last_affected` | spec.txt:1855, 1874 |
| 7 | `recommended` | spec.txt:1855, 1877 |
| 8 | `under_investigation` | spec.txt:1855, 1880 |

Schema node constraints: `type: object`, `minProperties: 1` — prose "of value type object with 1 or more properties"
(`spec.txt:1855`); prose wording "The eight defined properties are …" matches schema `len(properties) == 8`.
Schema/JSON-snippet order equals prose order (checked, `order_equal=True`).

### (b) `flags` label enum — schema pointer `$/properties/vulnerabilities/items/properties/flags/items/properties/label/enum`

Prose: §3.2.3.5 (`spec.txt:1729`), value list `spec.txt:1757-1761`, "Valid enum values are:" intro `spec.txt:1756`.

| # | value | spec anchor |
|---|-------|-------------|
| 1 | `component_not_present` | spec.txt:1757 |
| 2 | `inline_mitigations_already_exist` | spec.txt:1758 |
| 3 | `vulnerable_code_cannot_be_controlled_by_adversary` | spec.txt:1759 |
| 4 | `vulnerable_code_not_in_execute_path` | spec.txt:1760 |
| 5 | `vulnerable_code_not_present` | spec.txt:1761 |

Schema node: `type: string`, `enum` of 5; title "Label of the flag", description "Specifies the machine readable
label." — prose "Label of the flag (label) of value type string and enum specifies the machine readable label"
(`spec.txt:1756`). `flags` array is `minItems: 1, uniqueItems: true` — prose "array with 1 or more unique items (a set)"
(`spec.txt:1730`).

### (c) `threats` category enum — schema pointer `$/properties/vulnerabilities/items/properties/threats/items/properties/category/enum`

Prose: §3.2.3.14 (`spec.txt:2029`), value list `spec.txt:2056-2058`, intro `spec.txt:2055`.

| # | value | spec anchor |
|---|-------|-------------|
| 1 | `exploit_status` | spec.txt:2056 |
| 2 | `impact` | spec.txt:2057 |
| 3 | `target_set` | spec.txt:2058 |

Schema node: `type: string`, `enum` of 3; title "Category of the threat", description "Categorizes the threat according
to the rules of the specification." — prose wording `spec.txt:2055` is identical. `threats` array is `minItems: 1`
(no `uniqueItems`), matching prose "array with 1 or more items" (`spec.txt:2030`).

### (d) `remediations` category enum — schema pointer `$/properties/vulnerabilities/items/properties/remediations/items/properties/category/enum`

Prose: §3.2.3.12.1 (`spec.txt:1938`), value list `spec.txt:1940-1944`, intro `spec.txt:1939`.

| # | value | spec anchor |
|---|-------|-------------|
| 1 | `mitigation` | spec.txt:1940 |
| 2 | `no_fix_planned` | spec.txt:1941 |
| 3 | `none_available` | spec.txt:1942 |
| 4 | `vendor_fix` | spec.txt:1943 |
| 5 | `workaround` | spec.txt:1944 |

Schema node: `type: string`, `enum` of 5; title "Category of the remediation", description "Specifies the category which
this remediation belongs to." — prose `spec.txt:1939` identical. `remediations` array is `minItems: 1` (no
`uniqueItems`), matching prose "array with 1 or more Remediation items" (`spec.txt:1903`); item `required:
[category, details]` matches prose "the 2 mandatory properties Category (category) and Details (details)"
(`spec.txt:1907`), and the six optional prose properties (`date, entitlements, group_ids, product_ids,
restart_required, url`, `spec.txt:1908`) are exactly the schema's optional property set.

### Anchor portability across the two served variants

The spec labels the `.md` variant *Authoritative* (`spec.txt:5-6`; `spec-md.txt:7`). Fetched and line-collapsed with the
same rule (5437 lines, normalized sha256 `c2875f14a5f9cbcff37557cad37a5573182514231ab534010ba1c4ec357a1c77`), it carries
the **same four lists, same order, same spelling**. Anchors in that variant, for a capture made from the `.md` URL:

| enumeration | md anchors |
|-------------|------------|
| `product_status` names | prose sentence `spec-md.txt:1927`; JSON keys 1932, 1935, 1938, 1941, 1944, 1947, 1950, 1953 |
| `flags.label` | `spec-md.txt:1805-1809` (intro line 1803) |
| `threats.category` | `spec-md.txt:2162-2164` (intro line 2160) |
| `remediations.category` | `spec-md.txt:2023-2027` (intro line 2021) |

So whichever URL the C2 capture snapshots, the enumeration anchors are available: html-normalized anchors in §2, `.md`
anchors here.

## 3. Diff output (verbatim)

```
## a product_status property names
   schema_path: $/properties/vulnerabilities/items/properties/product_status/properties (minProperties=1)
   schema(8): first_affected, first_fixed, fixed, known_affected, known_not_affected, last_affected, recommended, under_investigation
   spec(8):   first_affected, first_fixed, fixed, known_affected, known_not_affected, last_affected, recommended, under_investigation
   spec_anchors: first_affected:spec.txt:1859, first_fixed:spec.txt:1862, fixed:spec.txt:1865, known_affected:spec.txt:1868, known_not_affected:spec.txt:1871, last_affected:spec.txt:1874, recommended:spec.txt:1877, under_investigation:spec.txt:1880
   set_equal=True order_equal=True

## b flags label enum
   schema_path: $/properties/vulnerabilities/items/properties/flags/items/properties/label/enum (spec section 3.2.3.5)
   schema(5): component_not_present, inline_mitigations_already_exist, vulnerable_code_cannot_be_controlled_by_adversary, vulnerable_code_not_in_execute_path, vulnerable_code_not_present
   spec(5):   component_not_present, inline_mitigations_already_exist, vulnerable_code_cannot_be_controlled_by_adversary, vulnerable_code_not_in_execute_path, vulnerable_code_not_present
   spec_anchors: component_not_present:spec.txt:1757, inline_mitigations_already_exist:spec.txt:1758, vulnerable_code_cannot_be_controlled_by_adversary:spec.txt:1759, vulnerable_code_not_in_execute_path:spec.txt:1760, vulnerable_code_not_present:spec.txt:1761
   set_equal=True order_equal=True

## c threats category enum
   schema_path: $/properties/vulnerabilities/items/properties/threats/items/properties/category/enum (spec section 3.2.3.14)
   schema(3): exploit_status, impact, target_set
   spec(3):   exploit_status, impact, target_set
   spec_anchors: exploit_status:spec.txt:2056, impact:spec.txt:2057, target_set:spec.txt:2058
   set_equal=True order_equal=True

## d remediations category enum
   schema_path: $/properties/vulnerabilities/items/properties/remediations/items/properties/category/enum (spec section 3.2.3.12.1)
   schema(5): mitigation, no_fix_planned, none_available, vendor_fix, workaround
   spec(5):   mitigation, no_fix_planned, none_available, vendor_fix, workaround
   spec_anchors: mitigation:spec.txt:1940, no_fix_planned:spec.txt:1941, none_available:spec.txt:1942, vendor_fix:spec.txt:1943, workaround:spec.txt:1944
   set_equal=True order_equal=True

crosscheck all_match=True rc=0
```

Additional structural checks on the schema: 14 `enum` arrays in the file, all duplicate-free; `product_status`,
`flags`, `threats`, `remediations` are each defined **once** (no shadow `$defs` copy; `$defs` has no
`product_status_t`); the only other `label` node is the unrelated TLP label
(`$/properties/document/properties/distribution/properties/tlp/properties/label`, 4 values `AMBER/GREEN/RED/WHITE`).

## 4. Behavioural closure (jsonschema 4.25.1, Draft 2020-12, subschema wrapped with the schema's `$defs`)

Verbatim output:

```
flags: component_not_present + product_ids               -> VALID
flags: typo component_not_present_x                      -> INVALID | 'component_not_present_x' is not one of ['component_not_present', 'inline_mitiga
flags: case Vulnerable_Code_Not_Present                  -> INVALID | 'Vulnerable_Code_Not_Present' is not one of ['component_not_present', 'inline_mi
flags: two identical items (uniqueItems)                 -> INVALID | [{'label': 'impact', 'product_ids': ['CSAFPID-1']}, {'label': 'impact', 'product
flags: two VEX codes same product (6.1.33 case)          -> VALID
threats: impact + details                                -> VALID
threats: severity                                        -> INVALID | 'severity' is not one of ['exploit_status', 'impact', 'target_set']
remediations: vendor_fix + details + product_ids         -> VALID
remediations: patch                                      -> INVALID | 'patch' is not one of ['mitigation', 'no_fix_planned', 'none_available', 'vendor
product_status: known_not_affected only                  -> VALID
product_status: unknown key not_affected                 -> VALID
product_status: empty object (minProperties=1)           -> INVALID | {} should be non-empty
```

Reading: the three real enums are closed (typos and case variants are rejected by the schema itself); `product_status`
keys are **not** closed by the schema (`{"not_affected": [...]}` validates), and an empty `product_status` is rejected
by `minProperties: 1`.

## 5. The two strictness gaps (schema looser than prose — routed to tests by the spec, not defects to fix)

1. **`product_status` key closure.** The schema has **zero** `additionalProperties` keywords anywhere (recursive walk of the parsed
   document: `additionalProperties occurrences: 0`), so a misspelled status key
   (`not_affected`) validates. Spec resolution is explicit: `spec.txt:534` — "Even though the JSON schema does not
   prohibit specifically additional properties and custom keywords, it is strongly recommended not to use them." The
   test layer that closes it is §6.2.20 Additional Properties (`spec.txt:3519-3520`, in 6.2 Optional Tests at
   `spec.txt:3149`): "It MUST be tested that there is no additional property in the CSAF document that was not defined
   in the CSAF JSON schema", implemented by validating against a strict schema with `additionalProperties: false` for
   every object key.
   Consequence for the F21 entry: it may say the eight names are the *defined* `product_status` properties, but must not
   claim the schema rejects other keys; a `product_status` typo is a §6.2.20 (optional-test) failure, not a schema
   failure. As landed, the entry states the eight from the prose (`L1855`) and its Claim 7 says only that "the use of
   JSON schema allows validation and proof of model conformance" (`L510`) — consistent with this gap, no overclaim.
2. **One VEX-justification flag per product.** Schema `flags.uniqueItems: true` only rejects byte-identical flag
   objects; two *different* VEX codes for the same product validate (line `flags: two VEX codes same product (6.1.33
   case) -> VALID`). §6.1.33 (`spec.txt:3095-3097`) forbids a product from being a member of more than one flag item
   with a VEX justification code (product groups counted). That constraint is not expressible in the schema and lives
   only in the mandatory test — so the entry may state "one VEX justification flag per product" only with the §6.1.33
   attribution, not as a schema property.

## 6. VEX context anchors that constrain how the entry may word its topic

- `spec.txt:2152` (§4.5 Profile 5: VEX requirements): for each item in
  `/vulnerabilities[]/product_status/known_not_affected` an impact statement SHALL exist **as machine readable flag in
  `/vulnerabilities[]/flags` or as human readable justification in `/vulnerabilities[]/threats`** with category `impact`
  — this is the exact join the entry's title presupposes, and both join targets exist with the enums reported above.
- `spec.txt:2843-2851` (§6.1.27.7 VEX Product Status, category `csaf_vex`): at least one of `fixed`,
  `known_affected`, `known_not_affected`, `under_investigation` MUST be present — a **profile-restricted subset** of the
  eight property names, so the entry must not present all eight as VEX-mandatory.
- `spec.txt:2156`: `/document/category` SHALL be `csaf_vex`; `spec.txt:2154`: `no_fix_planned` and `none_available`
  are permitted as remediation action statements in the VEX profile.
- `spec.txt:3096-3097`: the §6.1.33 test is deliberately forward-compatible, naming the VEX justification codes
  explicitly because "additional flags with a different purpose might be provided in later versions of CSAF" — the
  schema enum is closed at 5 **for 2.0**.

## 7. Entry↔schema leg (entry landed mid-seat; comparison completed)

The C2 entry was absent at every check until 18:37:36Z and landed while the third poll was still running. Poll log lines
verbatim, in order, from the seat's three successive poll jobs:

```
still absent 18:32:22Z
still absent 18:37:36Z
ENTRY LANDED 18:40:25Z
  137 22887 corpus/knowledge/csaf-vex-product-status-and-justifications.md
```

`corpus/knowledge/csaf-vex-product-status-and-justifications.md`: 137 lines, 22887 bytes, sha256
`0343ef4544ebd675754c498829fa99bbde4f1391d4260db5e494efe8a6dc5b0a`, `source: S055` on line 3.
The committed capture `corpus/source-snapshots/round-38/S055.txt` is **byte-identical** to the normalization used for
§2's anchors — `sha256sum` = `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`, 5146 lines,
272441 bytes, `cmp` clean — so every `spec.txt:N` anchor in this receipt is literally a line of the committed capture,
and the entry's own `L<n>` citations are directly comparable to them. The entry's declared capture binding
(`5,146 lines, 272,441 bytes; sha256 63c8ad52…`) is exactly right: all three values were re-measured against the
committed file in this seat.

Entry enumeration scan (`entrycheck.py`, verbatim):

```
typo_candidates []
product_status cited ['first_affected', 'first_fixed', 'fixed', 'known_affected', 'known_not_affected', 'last_affected', 'recommended', 'under_investigation'] missing []
flags_label cited ['component_not_present', 'inline_mitigations_already_exist', 'vulnerable_code_cannot_be_controlled_by_adversary', 'vulnerable_code_not_in_execute_path', 'vulnerable_code_not_present'] missing []
threats_category cited ['exploit_status', 'impact'] missing ['target_set']
remediations_category cited ['no_fix_planned', 'none_available'] missing ['mitigation', 'vendor_fix', 'workaround']
```

**No misspelling, no foreign token, no wrong value.** Every enumeration token in the entry is one of the 21 schema
values. Coverage is full for the two vocabularies the entry enumerates exhaustively — all 8 `product_status` names (it
states the eight and the VEX four-subset) and all 5 flags labels (its Claim 5 table) — and a deliberate subset for the
other two: it quotes `threats` categories `exploit_status` and `impact` only and `remediations` categories
`no_fix_planned` and `none_available` only. Both subsets are legitimate: the entry never claims those lists are
complete (it presents `impact`/`exploit_status` as the two it needs and `no_fix_planned`/`none_available` as "permitted"
per `spec.txt:2154`), so no omission is a false statement. `target_set`, `mitigation`, `vendor_fix` and `workaround`
remain available if a later revision wants the full lists.

Entry anchors that touch the four enumerations, each re-read against the capture in this seat:

| entry claim | entry anchor | capture text at that line |
|---|---|---|
| five label values, "no sixth" (FC-3) | L1757-L1761 | the five values, one per line — matches schema enum exactly |
| "one meaning per value" table | L1763-L1769 | `component_not_present` 1763, `vulnerable_code_not_present` 1764, `vulnerable_code_cannot_be_controlled_by_adversary` 1766, `vulnerable_code_not_in_execute_path` 1767, `inline_mitigations_already_exist` 1769 — all land |
| "The given values reflect the VEX not affected justifications." | L1762 | exact |
| "The eight defined properties are …" | L1855 | exact, and equals the schema's 8 property names |
| `fixed` / `known_affected` / `known_not_affected` / `under_investigation` definitions | L1887 / L1888 / L1890 / L1894 | all land on the named property's definition |
| threats `exploit_status` / `impact` meanings | L2059 / L2060 | both land |
| impact-statement obligation and `impact` category requirement | L2151-L2152 | exact |
| `no_fix_planned` / `none_available` permitted | L2154 | exact |
| `csaf_vex` document category | L2156 | exact |
| VEX 6.1.27.7 four-category requirement + failing example | L2844 / L2861 | exact |
| §6.1.33 one-VEX-flag-per-product | L3096-L3097 | exact |

Result for the entry leg: `entry_mismatches = 0`. One optional improvement, not a defect: the entry's "Honest limit"
says the JSON schemas "are not in this capture" and that its type/enum facts "are the prose's statements". This seat's
cross-check shows the machine-readable schema carries the **same** four enumerations (identical values and order), so a
future revision can cite schema confirmation for the enum facts instead of resting them on prose alone — and should keep
the §5 caveats (schema does not close `product_status` keys; `uniqueItems` is not §6.1.33).

## 8. Commands run (verbatim where material)

```
curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o schema.json -w 'schema http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://docs.oasis-open.org/csaf/csaf/v2.0/os/schemas/csaf_json_schema.json
schema http=200 bytes=57152 url=https://docs.oasis-open.org/csaf/csaf/v2.0/os/schemas/csaf_json_schema.json
curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o spec.html -w 'spec http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
spec http=200 bytes=414858 url=https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o schema-id.json -w 'idurl http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://docs.oasis-open.org/csaf/csaf/v2.0/csaf_json_schema.json
idurl http=200 bytes=57152 url=https://docs.oasis-open.org/csaf/csaf/v2.0/csaf_json_schema.json
sha256sum schema.json schema-id.json
29c114b35b0a30831f1674f2ab8b3ed9b2890cfeaa63b924ac6ed9d70ef44262  schema.json
29c114b35b0a30831f1674f2ab8b3ed9b2890cfeaa63b924ac6ed9d70ef44262  schema-id.json
cmp -s schema.json schema-id.json && echo "IDENTICAL bytes"
IDENTICAL bytes
sha256sum schema.json spec.html spec.txt
29c114b35b0a30831f1674f2ab8b3ed9b2890cfeaa63b924ac6ed9d70ef44262  schema.json
fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b  spec.html
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  spec.txt
```

The extraction/diff script (`crosscheck.py`) resolved each schema pointer by walking the parsed JSON, took prose values
only from whole-line single-token lines bounded by the section heading and the next heading, compared sets and order,
and ran a `difflib` near-miss scan (`ratio >= 0.88`) over each section for typo drift; the near-miss hits were substring
artifacts only (`itigations`, `ixed`, `ecommended` inside `mitigations`, `fixed`, `recommended` text), no real variant.

## 9. Compliance

- No tool installed or upgraded; no `pacman` invocation. Used the preinstalled `python3` 3.14 with `jsonschema` 4.25.1.
- Lane writes: this receipt only. No lane file edited, no mutating git command run (read-only
  `git -C ... rev-parse/status/log` only).
- Scratch `/fast/scratch/hyaku/kasegi-r38/ExecSchemaCross/` removed before yielding.
- Network: four GETs over four distinct URLs (schema `os`, spec html `os`, spec md `os`, schema `$id`), all HTTP 200, UA
  `kasegi-shokunin/1.0`, all bodies recorded above with sha256.

## 10. Risks

- **Anchor stability — retired by observation.** The lane's committed round-38 capture `S055.txt` is byte-identical to
  the text these anchors index (`cmp` clean, sha256 `63c8ad52…`, 5146 lines), so the anchors are exact for the landed
  entry and for `source-recheck.py`. If the capture is ever re-made from the `.md` variant instead, the alternate anchors
  in §2 apply (normalized sha256 `c2875f14…`); a different normalizer still leaves the section numbers (`§3.2.3.5`,
  `§3.2.3.9`, `§3.2.3.12.1`, `§3.2.3.14`) and the value tokens as stable locators.
- **Entry-leg timing.** The entry landed at 18:40:25Z, after two absent polls; the comparison in §7 is against the entry
  as of that minute (sha256 `0343ef45…`). A later edit to the entry needs the one-line rerun in §7.
- **Entry-leg pending** (§7): this receipt cannot certify the entry's enumeration spelling; it certifies the reference
  it must match, and gives the one-step check.
- The `product_status` strictness gap (§5.1) means a schema-only review of the entry would not catch a misspelled
  status key; the entry needs the prose/§6.2.20 comparison above.

## DELIVERABLE

```text
(a) product_status property names
    schema: /properties/vulnerabilities/items/properties/product_status/properties
    values: first_affected, first_fixed, fixed, known_affected, known_not_affected, last_affected,
            recommended, under_investigation  (8; minProperties=1)
    spec:   CSAF v2.0 OS §3.2.3.9 — spec line 1855 (enumeration sentence), JSON block lines 1856-1883;
            per-value anchors 1859/1862/1865/1868/1871/1874/1877/1880

(b) flags label enum
    schema: /properties/vulnerabilities/items/properties/flags/items/properties/label/enum
    values: component_not_present, inline_mitigations_already_exist,
            vulnerable_code_cannot_be_controlled_by_adversary, vulnerable_code_not_in_execute_path,
            vulnerable_code_not_present  (5)
    spec:   §3.2.3.5 — spec lines 1757-1761 (intro line 1756)

(c) threats category enum
    schema: /properties/vulnerabilities/items/properties/threats/items/properties/category/enum
    values: exploit_status, impact, target_set  (3)
    spec:   §3.2.3.14 — spec lines 2056-2058 (intro line 2055)

(d) remediations category enum
    schema: /properties/vulnerabilities/items/properties/remediations/items/properties/category/enum
    values: mitigation, no_fix_planned, none_available, vendor_fix, workaround  (5)
    spec:   §3.2.3.12.1 — spec lines 1940-1944 (intro line 1939)

entry cross-check: no mismatch — the landed entry uses only these 21 tokens (no typo); all 8 status names and all
5 flag labels cited; threats/remediations cited as a declared subset.
```
