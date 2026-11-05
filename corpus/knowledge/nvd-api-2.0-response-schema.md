# NVD API 2.0 response schema — the JSON Schema that defines the response F33 admitted as served: NVD's own enrichment vocabulary (evaluator*/cisa* mirror fields, NVD-side metrics), the required envelope, and the per-record required five

source: S085 — https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema — capture corpus/source-snapshots/round-53/S085.txt (543 lines, 7590 bytes; sha256 4d1c4e7732e128750a00557b0f16e69f021d2d5d25e2f55dfe8a9d5faa9a44d2; fetched 2026-11-01T06:16:10Z, HTTP 200, 10394 raw bytes — the same raw byte count the round-42 S066 screen recorded on 2026-10-28, so the served artifact is unchanged across the two opens); manifest corpus/source-snapshots/round-53/manifest.json (13 assertions Q1-Q13, each exactly-once at its pinned anchor)
verified-at: 2026-11-01 (opened this round; a static schema artifact served from NIST's csrc host — the 90d row recheck re-fetches it, and a changed sha re-fails the capture)
ground: F34
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && (python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-53/manifest.json --source S085 || python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-53/manifest.json --source S085)   # interpreter-portable form (run from the lane root, no `cd` prefix); prints S085:sha256 OK then one S085:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

This is NIST's own schema document speaking: the bytes are what NIST's csrc host served at the schema
URL, read as evidence of what the API 2.0 response CONTRACT declares — nothing wider. It is a derived,
NVD-enriched projection of the CVE Record Format (F25/S064), which is exactly why it is its own
surface: the fields that make it NVD's own (the evaluator* and cisa* mirror keys, NVD's metrics
vocabulary) are the fields the record format does not carry. The round-42 screen rejected this same
URL on the primary-of-record criterion (row S066, kept byte-identical rejected); this entry re-opens
it under the unspent term of that row's own flip — "NVD-specific enrichments (vulnStatus, evaluator*
fields, cisa* mirror fields, NVD-side metrics/weaknesses)" — the interface-contract term having been
the one F33's live-response admission spent. The developer-hub documentation pages remain JS-walled
for this lane's instrument (rejected row S084); no rate-limit, authentication or query-parameter claim
is made anywhere here: a response-body schema defines none of those.

## Claim 1 — the document is the versioned response contract, and the served envelope is schema-required

The schema self-identifies with a version: `"title": "JSON Schema for NVD Vulnerability Data API
version 2.2.4"` (S085.txt:3, Q1), under JSON Schema draft-07 (`"$schema":
"http://json-schema.org/draft-07/schema#"`, S085.txt:2, Q2). The paging envelope F33 observed served
is here REQUIRED, not observed: `resultsPerPage` is a top-level property (S085.txt:505, Q13) and the
root `required` list names all seven envelope keys (resultsPerPage, startIndex, totalResults, format,
version, timestamp, vulnerabilities). Falsifiable rule: a response payload missing any of the seven
is not a valid NVD API 2.0 response by this contract — testable with any JSON Schema draft-07
validator against the captured schema. Rejected over-generalization: this pins the RESPONSE shape
only; it does not assert that NIST validates every served payload against this schema, and it makes
no claim about request-side validation.

## Claim 2 — the NVD-only enrichment vocabulary is schema-declared, and one live response need not carry it

The mirror fields that make this projection NVD's own are declared properties of every record:
`"evaluatorComment": {` (S085.txt:36, Q4), `"evaluatorSolution": {` (S085.txt:39, Q5),
`"evaluatorImpact": {` (S085.txt:42, Q6), and the KEV-derived cisa block `"cisaExploitAdd": {`
(S085.txt:45, Q7) with `"cisaRequiredAction": {` (S085.txt:53, Q8) beside cisaActionDue and
cisaVulnerabilityName. F33's Limits state these are "NOT present in this response (this record
carries none)" — the schema proves the absence was an instance fact, not a contract fact.
Falsifiable rule: a record object MAY omit all of these (none is in the per-record `required` five),
so absence of evaluator*/cisa* fields in a served record asserts nothing about the record's standing
in the API — only the contract's presence-when-present. Rejected over-generalization: the cisa*
field names ground nothing about the KEV catalog's own content (F18/S052); they are NIST's mirror of
it inside this response shape.

## Claim 3 — NVD's metrics container is its own vocabulary beside the CNA's, and the ssvcV203 block is a declared metric

The metrics object is defined by NVD's own description: `"description": "Metric scores for a
vulnerability as found on NVD."` (S085.txt:96, Q9) — the container-level statement that what follows
is NVD-served scoring, per-version containers cvssMetricV40/V31/V30/V2 plus `"description": "SSVC
V2.0.3 score."` (S085.txt:128, Q10) for the ssvcV203 block F33 saw served with CISA ADP data inside.
Falsifiable rule: any cvssMetric*/ssvcV203 entry a consumer reads is an NVD-container fact whose
source attribution lives in the entry's own `source`/`type` fields (F33's Primary/Secondary rule),
never in the container name. Rejected over-generalization: Q10 pins the container declaration only —
the SSVC decision-tree semantics stay F20's, and the ADP enrichment program that generates the data
stays F32's; this schema defines neither.

## Claim 4 — the record identity and shape constraints the contract enforces

A record's `id` must match `"pattern": "^CVE-[0-9]{4}-[0-9]{4,}$"` (S085.txt:329, Q11), the
per-record required five are id, published, lastModified, references and descriptions (root of the
cve_item definition's `required` list), the vulnerabilities array is the `"description": "NVD feed
array of CVE"` (S085.txt:525, Q12) whose items wrap exactly one `cve` key, and vulnStatus — the
change-tracking field F33 read as served vocabulary — is a declared property (S085.txt:25, Q3).
Falsifiable rule: a payload whose record id deviates from the pattern, or whose record omits any of
the required five, is invalid under this contract regardless of which CNA produced it — checkable
against the captured schema bytes. Rejected over-generalization: vulnStatus's VALUE vocabulary
(Modified etc.) is not enum-constrained here (`"type": "string"`), so no closed set of lifecycle
states is asserted from this document; F33's served instance value stays an instance observation.

## Distinctness — what this row adds beyond F33/F25/F32 and the screened neighbors

F33/S083 is the interface AS SERVED for one record (instance); this is the schema that DEFINES the
response (contract) — the same envelope F33 pinned as served is here schema-required (Q13 + the
root required list), and the fields F33's Limits deferred ("S066's schema artifact on csrc.nist.gov
remains the natural next capture") are pinned here as Q4-Q8. F25/S064 is the canonical CVE Record
Format; this document is NVD's derived projection of it for retrieval — its NVD-only keys are what
this entry claims, and nothing here re-states record-format ground. F32/S081 is the ADP enrichment
program; Q10 pins only this schema's declaration of the container its data arrives in. The extended
pre-freeze screen (receipt `.ufo/waves/round-53/controls/neighbor-screen-r53.txt`, run before the
freeze commit) found the schema URL named only by the rejected S066 row and the r42 lesson records
of that screen, the mirror-field names only in F33's own Limits disclaimer, and ZERO downstream
consumers across corpus/source-snapshots/.

## Limits

- One artifact at one instant (fetched 2026-11-01T06:16:10Z). The 10394-byte raw count matches the
  round-42 screen's record byte-for-byte, but the recheck's authority is the pinned sha256, not the
  size coincidence.
- The schema references external schema documents by URL (cvss-v2.0/v3.0/v3.1/v4.0.json,
  ssvc-v2.0.3.json, cve_affected_1.0.json); those referenced documents are NOT captured and nothing
  here asserts their content.
- Rate limits, authentication, query parameters and error responses are outside a response-body
  schema; none is asserted. The developer-hub documentation surface stays S084-rejected (JS-walled).
- The rejected round-42 row for this URL (S066) stays byte-identical; the re-open is recorded in the
  S085 row and here, never by editing the old row.
