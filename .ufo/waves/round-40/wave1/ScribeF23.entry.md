# CycloneDX v1.7 `vulnerabilities[].analysis` — the analyst-decision record (six states, nine justifications, five responses) that is not CSAF's `product_status`, and the third vocabulary beside it in `affects[].versions[].status`

source: S060 — https://cyclonedx.org/docs/1.7/json/ — capture corpus/source-snapshots/round-40/S060.txt (111 lines, 4,889 bytes; sha256 d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779): title L1, `analysis` object L2-L4, `state` L5-L15, `justification` L16-L29, `response` L30-L41, `detail` L42-L44, `firstIssued` L45-L47, `lastUpdated` L48-L50, `affects` L51-L68, `versions`/`version`/`range` L69-L103, per-version `status` L104-L111
verified-at: 2026-10-26 (capture fetched 2026-10-26T21:16:18Z, HTTP 200, 6,419,901 raw bytes; the slice digest was re-computed this day; the manifest records that the raw page digest is not stable across fetches — a second fetch changed 3,936 bytes of Cloudflare mail-obfuscation tokens — while the normalized page text and this slice are)
ground: F23
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S060   # prints S060:sha256 OK then one S060:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

This is CycloneDX's own JSON reference, and this capture is a declared slice of it, not
the whole page. The slice's L1 is the page's title line ("CycloneDX v1.7 JSON Reference
CycloneDX 1.7 (JSON)"); the manifest records the scope as page-text L16060-L16169 appended
to that title line, so capture line k ≥ 2 is page-text line 16058 + k, and the full 22,795-line
normalized page is not committed.

What the slice contains is schema field documentation, not prose: entries read as a field
name (`state` L5, `justification` L16, `response` L30), a `Type:` line (L6, L17, L31), a
`Must be one of:` list and a `NameDescription` table header (L8-L9, L19-L20, L35-L36). Read
a claim here as a statement about field definitions on this page — never as evidence about
a named vendor's practice, and never as a conformance rule without checking whether the
obligation is `MUST`, `SHALL`, `should` or absent (the slice's verbs are measured in FC-1).

No edition or ratification statement is in the slice: it carries no date line, no ECMA
number and no status line. A claim that v1.7 is the ratified edition belongs to the
overview or standards page, not to this capture.

## Claim 1 — `analysis` is one per-vulnerability assessment object, and its stated job is exploitability

> "An assessment of the impact and exploitability of the vulnerability." — S060.txt:L4

The object's own description names two things — impact and exploitability — and no product
list: the object carries scalars (`state` L5-L15, `justification` L16-L29, `detail` L42-L44,
`firstIssued` L45-L47, `lastUpdated` L48-L50), one repeatable enum (`response` L30-L41) and
one reference array (`affects` L51-L68). There is no `product_status`-style block of
per-status id lists in the slice at all: the product-side vocabulary lives one level down, in
`affects[].versions[].status` (Claim 7), which is a version-level status, not this object's
state.

Consequence for a reader: a CycloneDX BOM answers "what did the analyst conclude about this
vulnerability, and why" at the object, and "which version is affected" in `affects`. The two
answers are separate fields and can disagree; an `analysis.state` of `not_affected` beside a
version whose `status` is the default `affected` (L105) is a contradiction the schema allows
and no line here forbids.

## Claim 2 — `state` is one scalar enum of six values, and one of them has no CSAF twin

> "Declares the current state of an occurrence of a vulnerability, after automated or manual analysis." — S060.txt:L7

`state` is `Type: enum (of string)` (L6) — a single value, not a list — and its six values are
(L10-L15):

| value | the page's description | line |
|---|---|---|
| `resolved` | "The vulnerability has been remediated." | L10 |
| `resolved_with_pedigree` | "The vulnerability has been remediated and evidence of the changes are provided in the affected components pedigree" | L11 |
| `exploitable` | "The vulnerability may be directly or indirectly exploitable." | L12 |
| `in_triage` | "The vulnerability is being investigated." | L13 |
| `false_positive` | "The vulnerability is not specific to the component or service and was falsely identified or associated." | L14 |
| `not_affected` | "The component or service is not affected by the vulnerability. Justification should be specified for all not_affected cases." | L15 |

Three of these have no counterpart in CSAF's `product_status` vocabulary, and `false_positive`
is the sharpest: it says the finding does not belong to the component at all, which is a
statement about the tool or the finding, not about a product version's exposure. The CSAF
profile's four mandatory categories (S055.txt:L2844) contain nothing with that meaning.

`resolved_with_pedigree` is a schema-level claim of evidence: the state asserts that verifiable
commit history or diffs accompany it (L11). That is checkable — the pedigree either exists in
the referenced component or it does not — and `resolved` alone asserts nothing of the kind.

## Claim 3 — `justification` is one scalar enum of nine, and its obligation is `should`

> "The rationale of why the impact analysis state was asserted." — S060.txt:L18

`justification` is also `Type: enum (of string)` (L17) — one value — with nine reasons
(L21-L29): `code_not_present`, `code_not_reachable`, `requires_configuration`,
`requires_dependency`, `requires_environment`, `protected_by_compiler`,
`protected_at_runtime`, `protected_at_perimeter`, `protected_by_mitigating_control`.

The binding sentence is a `should`, not a `MUST`: "Justification should be specified for all
not_affected cases." (L15). The field is therefore optional at the schema level while being
recommended whenever the state is `not_affected` — and the nine reasons split into different
kinds of claim:

- **Absence** (`code_not_present` L21, `requires_dependency` L24) — the code or dependency is
  not there.
- **Reachability** (`code_not_reachable` L22) — the vulnerable code is not invoked at runtime.
- **Configuration and build** (`requires_configuration` L23, `requires_environment` L25,
  `protected_by_compiler` L26) — exploitability depends on a switch the consumer may not share.
- **Runtime and perimeter control** (`protected_at_runtime` L27, `protected_at_perimeter` L28,
  `protected_by_mitigating_control` L29) — a control, not an absence.

Lane reading, not a quote: `protected_at_perimeter` is a claim about a deployment, so it is
not a property of the component version at all. A consumer who inherits that reason inherits
a statement about someone else's network.

## Claim 4 — `response` is a repeatable five-value enum on a different axis from `state`

> "A response to the vulnerability by the manufacturer, supplier, or project responsible for the affected component or service." — S060.txt:L32

> "More than one response is allowed." — S060.txt:L32

> "Responses are strongly encouraged for vulnerabilities where the analysis state is exploitable." — S060.txt:L32

`response` is `Type: array of enum (of string)` (L31), so it carries zero or more of five
values (L37-L41): `can_not_fix`, `will_not_fix`, `update`, `rollback`,
`workaround_available`. It answers a different question from `state`: `state` is what the
analyst concluded, `response` is what the responsible party intends to do about it. The two
are only linked by a recommendation — recommended when the state is `exploitable` (L32) —
never by a requirement, and either can appear without the other.

`can_not_fix` and `will_not_fix` are distinct answers and both are legitimate: an inability and
a refusal read differently to a reporter deciding whether to keep arguing. Neither is a status
change — nothing in the slice says a `will_not_fix` response makes the state `not_affected`.

## Claim 5 — `detail` is free text carrying the impact-statement job

> "If a vulnerability is not exploitable, this field should include specific details on why the component or service is not impacted" — S060.txt:L44

`detail` is `Type: string` (L43). It is where the "why" goes that the nine-enum justification
cannot express, and its own sentence repeats the `should` form. Being free text, it is
quotable and not comparable across producers: two `code_not_reachable` analyses can carry
detail text of any length, and nothing in the slice requires the detail to name a call path, a
build flag or a test.

## Claim 6 — the timestamps are fields of the analysis, so a reaffirmation is machine-readable

> "The date and time (timestamp) when the analysis was first issued." — S060.txt:L47

> "The date and time (timestamp) when the analysis was last updated." — S060.txt:L50

`firstIssued` and `lastUpdated` are `date-time` strings (L46, L49). This is the one place where
the CycloneDX object overlaps the CISA issuance guidance F22 holds: the "most recently
updated" stamp that S057 describes as a reaffirmation signal (S057.txt:L136-L138) is a data
field here. What the slice does not carry is any rule about when to write it: no trigger, no
lifecycle, no obligation to update after triage.

## Claim 7 — `affects[].versions[].status` is a third vocabulary: affected, unaffected, unknown

> "The components or services that are affected by the vulnerability." — S060.txt:L53

> "Zero or more individual versions or range of versions." — S060.txt:L71

`affects` is an array of objects whose `ref` is required and whose `versions` is optional
(L51-L68, L71); each version entry carries either a `version` string (L82-L92) or a `range` in
package-url vers syntax (L93-L103), plus a status:

> `Type: enum (of string) Default: "affected"` — S060.txt:L105

> "The vulnerability status for the version or range of versions." — S060.txt:L106

with three values: "The version is affected by the vulnerability." (`affected`, L109), "The
version is not affected by the vulnerability." (`unaffected`, L110) and "It is unknown (or
unspecified) whether the given version is affected." (`unknown`, L111).

Three properties of this enum matter and none is stated as a requirement:

1. **The default is `affected`** (L105). An entry that names a version and omits the status
   asserts affectedness without saying so.
2. **`unknown` is not `in_triage`.** A version-status `unknown` (L111) says nothing about an
   investigation; only the analysis state `in_triage` (L13) does.
3. **The three values are not CSAF's eight.** CSAF's `product_status` holds eight named
   properties across product-id lists (S055.txt:L1855), of which four satisfy the profile's
   mandatory test (S055.txt:L2844). Here there are three inline version-level values, and
   `fixed` is not among them — a fixed version is simply not affected, or carries a resolution
   in the analysis object.

## Comparison with S055 (CSAF v2.0 VEX `product_status`)

| dimension | CSAF v2.0 VEX profile — S055 | CycloneDX v1.7 `analysis` — S060 |
|---|---|---|
| unit | product_id lists under eight `product_status` properties (S055.txt:L1855) | one `analysis` object per vulnerability, plus `affects[]` bom-refs (L2-L4, L51-L68) |
| mandatory content | at least one of `fixed`, `known_affected`, `known_not_affected`, `under_investigation` (S055.txt:L2844) | no `MUST` or `SHALL` in the slice; the two obligations are `should` (L15, L44) |
| vocabulary | 4 mandatory categories of 8, plus 5 not-affected labels (S055.txt:L1763-L1769) | 6 states (L10-L15), 9 justifications (L21-L29), 5 responses (L37-L41), 3 version statuses (L109-L111) |
| not-affected reason | "an impact statement SHALL exist as machine readable flag" (S055.txt:L2151-L2152) | "Justification should be specified" (L15); a single enum value, not a flag record |
| affected obligation | action statement in `remediations` (S055.txt:L2153) | a `response` array whose values are intentions (L32, L37-L41), encouraged when `exploitable` |
| repeatability | one justification per product — a product may not be in two flag items (S055.txt:L3096) | one scalar `justification` per analysis object (L17); only `response` repeats (L31) |
| shape of "unknown" | `under_investigation` as a product-status category (S055.txt:L2844) | `in_triage` as a state (L13) and `unknown` as a version status (L111) — two different fields |

No justification label is shared. Each of the five CSAF labels occurs zero times in this
capture (FC-2), and none of the nine CycloneDX reasons is a CSAF label name: `code_not_present`
is not `component_not_present`, and `code_not_reachable` is not
`vulnerable_code_not_in_execute_path`. A crosswalk is therefore a translation a reader must
argue for, not a lookup.

## Comparison with S057 (CISA "When to Issue VEX Information")

The CISA guidance (S057) answers who issues, when, and what a downstream consumer may reuse;
this page defines fields and no issuance rule at all — `issue` occurs zero times in the slice and `issued` once, inside
the `firstIssued` description (L47). Three sharper contrasts:

1. **Lifecycle.** S057 expects `under_investigation` first and an update when triage concludes
   (S057.txt:L132-L135). CycloneDX has the same shape as data (`in_triage` L13 beside
   `resolved`/`not_affected`/`exploitable` L10-L15) and states no transition. An `in_triage`
   analysis may stay stale forever without violating this page.
2. **Reaffirmation.** S057 describes a timestamp-only update as a reaffirmation of the standing
   status (S057.txt:L136-L138). `lastUpdated` (L50) makes that signal checkable; nothing here
   requires the issuer to set it, and no field distinguishes "re-derived" from "restamped".
3. **Inheritance.** S057 says an upstream status is not inherited by default (S057.txt:L183-L186)
   and names the two not-affected labels that may be, with a re-introduction exception
   (S057.txt:L189-L191).
   Nothing in this slice is an inheritance rule: `analysis` hangs off one vulnerability in one
   BOM, and `affects` points at that BOM's own `bom-ref` values (L57-L68), so there is no
   upstream/downstream relation to inherit along.

## How a bounty or security researcher uses it

1. **Read `state` first, then `justification`, then `response`.** `state` is the conclusion
   (L10-L15); `justification` explains it and may be absent (L15, `should`); `response` is an
   intention and may name a refusal (`will_not_fix`, L38) without changing the state.
2. **Do not read a missing justification as a pre-verification claim.** The rule is `should`
   (L15); a `not_affected` with no justification is a permitted, weaker statement than CSAF's
   flag obligation (S055.txt:L2151-L2152).
3. **Check `affects[].versions[].status` before believing a clean analysis.** The default is
   `affected` (L105), so an entry that names a version and omits the status is asserting
   affectedness — and a `not_affected` state beside it is the internal contradiction to quote
   in a duplicate report.
4. **Do not translate `false_positive` into "not affected."** It alleges the finding does not
   belong to the component (L14); that is a claim about the tool or the report, and the
   reporter's evidence is exactly what tests it.
5. **Treat `protected_at_perimeter` as a deployment claim.** It is one of the nine reasons
   (L28) and asserts an external control. Where the reporter is testing the deployed service,
   a perimeter claim that the reporter passed through is falsified by the report itself.
6. **Ask for the pedigree behind `resolved_with_pedigree`.** The value itself promises
   verifiable commit history or diffs (L11); either they are there or the state overstates.
7. **Do not cite this object as a VEX requirement.** `VEX`, `SBOM`, `severity`, `score` and
   `product_status` occur zero times in the slice (FC-2); it defines CycloneDX fields, not a
   disclosure standard.

## Falsifiable rule and checks

**Falsifiable rule.** Any statement about this object is falsified by the following, each
checkable against the 111-line capture: (a) describing `state` as a list or as
`product_status`-shaped, when it is one enum value (L6, L10-L15); (b) claiming the object
requires a justification, when the sentence is `should` (L15) and `MUST`/`SHALL` occur zero
times in the slice; (c) claiming CycloneDX shares CSAF's five justification labels, when each
of the five occurs zero times and the nine reasons are different names (L21-L29); (d) claiming
`response` is single-valued, when it is an array and "More than one response is allowed" (L31-L32);
(e) claiming a version is unaffected by omission, when the status default is `affected` (L105);
(f) claiming this page sets an issuance, lifecycle or inheritance rule, when it states none and
the matching words occur zero times.

**FC-1 — every quoted span is verbatim, ≤25 words, and on its declared line.** Under
whitespace collapse, each of the 12 anchored blockquote spans occurs exactly once in the
capture and its declared line lies inside the occurrence; the longest is 21 words (L44). The
table cells' quoted descriptions of the six states and three version statuses resolve the same
way. The only quoted spans in this entry that are not from this capture are the S055 quotation
attributed to `S055.txt:L2151-L2152` and the rejected over-generalizations, which are labels a
reader might assert, not source text. The obligations are measured, not asserted: `SHALL`=0,
`MUST`=0, `should`=2 (L15, L44).

**FC-2 — vocabulary.** `grep -oF <word> S060.txt | wc -l` gives `VEX=0 CSAF=0 CVSS=0
severity=0 score=0 product_status=0 known_affected=0 known_not_affected=0
under_investigation=0`, and each of the five CSAF labels `component_not_present`,
`vulnerable_code_not_present`, `vulnerable_code_not_in_execute_path`,
`vulnerable_code_cannot_be_controlled_by_adversary`, `inline_mitigations_already_exist`
gives 0. Lane counts on the same capture (`grep -oiF <word> | wc -l`, case-insensitive):
`state=3 justification=2 response=3 analysis=6 detail=1 affects=1 firstIssued=1
lastUpdated=1`, so no comparison here rests on a word this page uses.

**FC-3 — the enum sizes are counted, not remembered.** The `state` table's value lines are
L10-L15 (6), `justification` L21-L29 (9), `response` L37-L41 (5), version `status` L109-L111
(3). A count script that selects lines beginning with `"` inside each `Must be one of:` block
returns `6 9 5 3`.

**FC-4 — the three rare states occur exactly once each.** `false_positive` (L14), `in_triage`
(L13) and `resolved_with_pedigree` (L11) each occur once, so the "no CSAF twin" argument
cannot be resting on a second, different use of the same word.

**FC-5 — the default is stated on the type line.** `grep -n 'Default' S060.txt` returns L105
only: `Type: enum (of string) Default: "affected"`. No other field in the slice carries a
default, so the affected-by-omission reading applies to version status alone.

**FC-6 — the slice boundary is declared.** `wc -l` gives 111 and `sha256sum` gives
`d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779`, matching the manifest
record; the capture's last line is the `unknown` value (L111), so no claim here reads past the
`analysis`/`affects` slice into the rest of the reference.

**FC-7 — the timestamp fields are inside the object, not beside it.** `firstIssued` (L45) and
`lastUpdated` (L48) sit between `detail` (L42) and `affects` (L51) in the field order, so
reading them as object fields rather than document metadata follows the page's own structure.

## Rejected over-generalizations

1. **"CycloneDX analysis is CSAF `product_status` under different names."** Rejected: the
   vocabularies do not intersect (FC-2), the object is one assessment per vulnerability rather
   than per-product id lists (L2-L4), and one state (`false_positive`, L14) has no CSAF
   category at all.
2. **"A justification is required for `not_affected`."** Rejected: the sentence is "Justification
   should be specified for all not_affected cases." (L15), and `MUST`/`SHALL` occur zero times
   in the slice (FC-1). Required is what S055 says about CSAF flags (S055.txt:L2151-L2152), not
   what this page says.
3. **"`response` is the remediation status."** Rejected: it is an array of intentions (L31-L41)
   with no stated effect on `state`; `can_not_fix` and `will_not_fix` are responses, not states,
   and the page never says a response changes the analysis.
4. **"A version entry without a status is unaffected."** Rejected: the default is `affected`
   (L105, FC-5). Omission asserts affectedness, the opposite of the tempting reading.
5. **"CycloneDX defines when a VEX/analysis must be issued or updated."** Rejected: no issuance
   rule is in the slice; `issue` occurs zero times and `issued` once as a timestamp description
   (L47). Issuance is S057's layer.
6. **"`protected_at_perimeter` means the component is not vulnerable."** Rejected: the reason is
   one of nine rationale values (L28) describing where attacks are blocked; it is not a statement
   about the code, and the same object can carry `state: exploitable` with it.
7. **"`unknown` version status means the vendor is still investigating."** Rejected: the
   description is "It is unknown (or unspecified) whether the given version is affected."
   (L111) — it makes no claim about an investigation, which is what the state `in_triage` (L13)
   names.

## Honest limit

- **One page slice, one fetch.** This is the `analysis`/`affects` region of the v1.7 JSON
  reference as normalized on 2026-10-26; the full page is 22,795 lines and is not committed,
  and no claim here reaches outside L2-L111 of the capture. A revised reference is a new pin.
- **Schema documentation, not prose standard.** The slice has no chapter text, no edition line
  and no conformance verbs beyond two `should` sentences; whether v1.7 is the ratified edition,
  and what its normative prose says, is a different source.
- **Raw-page digest instability is disclosed, not hidden.** The manifest records that two
  fetches of the same byte count produced different raw digests because Cloudflare rewrites
  mail-obfuscation tokens; the normalized slice is stable and is what the recheck compares.
- **No producer practice is asserted.** Nothing here says any tool or vendor emits `analysis`
  objects, or that a BOM in the wild carries one; the page defines fields.
- Documentation only: the capture holds public reference text, no credential, session or
  private URL, and this entry quotes none.
