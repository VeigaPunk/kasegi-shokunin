# OSV affected-range events — the OSV format's per-package version timeline: `affected[].ranges[].events` as introduced/fixed/last_affected/limit status changes with an implicit `limit` `"*"`, three range types whose orderings are evaluated differently (SEMVER precedence, ecosystem-specific logic, Git commit-graph reachability), and event version strings that may not match the upstream repository's own versions

source: S080 — https://ossf.github.io/osv-schema/ — capture corpus/source-snapshots/round-50/S080.txt (1462 lines, 70913 bytes; sha256 97b850a4bcd90600bb39391df3293e4591b9dd84170e94ecfd48f40e08cfeda9; fetched 2026-11-01T01:17:14Z, HTTP 200, 228890 raw bytes — the same raw byte count the round-42 S065 screen recorded on 2026-10-28, so the served page was unchanged across those two opens): version line S080.txt:4, purpose S080.txt:9-10, stability S080.txt:17, required envelope fields S080.txt:374-375, range type S080.txt:706-708, SEMVER versions-list carve-out S080.txt:714-715, ECOSYSTEM ordering S080.txt:719-721, GIT ordering S080.txt:729-730, GIT versions-list duty S080.txt:733-735, the four event verbs S080.txt:739-742, special values S080.txt:751-755, upstream-mismatch caveat S080.txt:746-748, fixed-vs-last_affected S080.txt:760-766, introduced-required S080.txt:777, GIT repo requirement S080.txt:788, database_specific out-of-scope S080.txt:790-793; manifest corpus/source-snapshots/round-50/manifest.json (16 assertions Q1-Q16, each exactly-once at its pinned anchor; `source-recheck.py --source S080` exits 0)
verified-at: 2026-11-01 (opened this round: the capture above is `capture-source.py --kind html`'s collapse of the served page, and every quote here is pinned to that capture, not to what the URL serves next)
ground: F31
recheck: (python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-50/manifest.json --source S080 || python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-50/manifest.json --source S080)   # interpreter-portable form (appended 2026-11-01): runs under python3 where that name exists, else under python (the Windows workspace host has no python3 — the Store alias stub exits non-zero and the fallback runs); run from the lane root, no `cd` prefix. Prints S080:sha256 OK then one S080:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

This is the OpenSSF OSV project's own specification page ("Open Source Vulnerability format",
title line S080.txt:1), read as the project's self-description of its format and nothing wider
(Q4). The page names its purpose in the first person plural — "We hope to define a simple
format that all vulnerability databases can export" (S080.txt:11) — so statements about what
databases do are the project's design intent, not an observed property of any database. The
page carries a version line and a stability statement (Q1, Q3 below): "Version 1.9.2 (October
13, 2026)" (S080.txt:4) and "This format is stable, but further backwards compatible changes
may still be made." (S080.txt:17). What any particular OSV producer publishes, and what
osv.dev's service does with it, is outside these bytes; the page itself puts per-database
`database_specific` values "beyond the scope of this document" (Q11).

## Claim 1 — the envelope is minimal by rule: two required fields, one conditional third

> "The id and modified fields are required. For schema versions above 1.0.0, the schema_version field is also required." — S080.txt:374-375

A record with an id and a modification timestamp is a well-formed OSV record as far as the
required set goes; everything else is optional. The lane's falsifiable check: an OSV record
that carries neither `modified` nor (above format 1.0.0) `schema_version` is malformed by the
format's own required set, independent of any database's additional practice. This envelope is
the whole of the format's mandatory surface — the page's purpose statement scopes it to
"describing vulnerabilities in open source packages" (S080.txt:9-10), and the required set
stays at two fields regardless of how many optional vocabulary groups a record carries.

## Claim 2 — affected-ness is read from an events timeline, and the timeline has exactly four verbs

> "Introduces a vulnerability: {"introduced": string}" — S080.txt:739
> "Fixes a vulnerability: {"fixed": string}" — S080.txt:740
> "Describes the last known affected version: {"last_affected": string}" — S080.txt:741
> "Sets an upper limit on the range being described: {"limit": string}" — S080.txt:742

The events array is a sequence of single-verb objects, and the page names the four verbs and
nothing else (S080.txt:739-742); the objects "represent a "timeline" of status changes for the
affected package" (S080.txt:743-744). Two structural rules are checkable against any record:
every event object carries exactly one verb (S080.txt:757-759 gives the invalid two-verb
example), and "There must be at least one introduced object in the events array." (S080.txt:777).
A range with no `introduced` event is malformed; a range whose events use a fifth verb is not
this format.

The timeline's boundaries are also rule-bearing, not cosmetic: `introduced` admits the special
value "0" that "represent[s] a version that sorts before any other version" (Q8,
S080.txt:751-752), and the range's end is closed by `fixed` or `last_affected` — or by nothing,
because "If no limit events are provided, an implicit { "limit": "*" } is assumed to exist."
(Q9, S080.txt:754-755). The falsifiable consequence: an OSV range with an `introduced` event
and no `fixed`/`last_affected`/`limit` event is still bounded — it is unbounded only under the
implicit `"*"` limit, which is assumed, not written.

## Claim 3 — `fixed` and `last_affected` are not interchangeable, and the page prefers one

> "last_affected should be thought of as the hard ceiling of the vulnerability at the time of publication in the absence of a fixed version." — S080.txt:763-764

A record may carry "last_affected" or "fixed" events "but not both" (S080.txt:760-761), and
the page states its own preference with a reason: `fixed` "precisely identifies the version
which contains the fix" while `last_affected` "opens up the possibility for false negatives"
(S080.txt:762-766). Reading rule: a `last_affected` ceiling means versions above it are
"unaffected" by the page's own convention (S080.txt:765), so a report that treats
`last_affected` as a fix version asserts something the format does not say — the fix version is
unknown when only a ceiling is given.

## Claim 4 — one type per range, and the type decides how orderings are evaluated

> "In the ranges field, the type field is required. It specifies the type of version range being recorded and defines the interpretation of the events object’s introduced, fixed, and any type-specific fields." — S080.txt:706-708

The three types order versions by three different machines: SEMVER by "the precedence order
defined in section 11 of SemVer 2.0" (S080.txt:710-712), ECOSYSTEM by strings that are
"arbitrary, uninterpreted" and conform to no SemVer ordering (Q13, S080.txt:719-721), and GIT
by commit reachability — "full-length Git commit hashes" (Q6, S080.txt:729-730) where one
commit precedes another when it is its parent. Two type-conditional duties are checkable: a GIT
range must carry the repository URL ("This field is required if affected[].ranges[].type is
GIT.", Q12, S080.txt:788), and the enumerated-versions requirement differs by type —
"Specifying one or more SEMVER ranges removes the requirement to specify an explicit enumerated
versions list" (S080.txt:714-715) while "Specifying one or more GIT ranges does NOT remove the
requirement to specify an explicitly enumerated versions list" (Q14, S080.txt:733-734),
because GIT inclusion "cannot be answered without access to a copy of the underlying Git
repository" (S080.txt:735). The rejected over-generalization: "OSV ranges are semver ranges" —
the format's own text says an ecosystem that does not enforce SemVer should use the ECOSYSTEM
type (S080.txt:717-718), so assuming SemVer ordering for an ECOSYSTEM range is wrong by the
record's own declared type.

## Claim 5 — event version strings are format-internal, not upstream versions

> "these version strings are not guaranteed to exactly match versions of the package found in the upstream package repository" — S080.txt:746-747

The page warns that event values "may be normalized, or have build metadata stripped"
(S080.txt:748). The falsifiable check: string-equality between an OSV event version and a
package manager's version is not evidence of match or mismatch; matching an OSV record against
a real package requires the range type's own evaluation machine — an ECOSYSTEM range's
inclusion query may not "be able to be answered without reference to the package ecosystem's
own logic" (S080.txt:724-725), SemVer precedence for SEMVER, the commit graph for GIT. The same
caveat applies inside GIT ranges, where the `versions` array holds tags that "cannot be relied
upon to conform to any particular package manager's syntax" (S080.txt:700).

## Distinctness — what this row adds beyond F25/F21/F23

The lane's admitted CVE JSON row (F25, source S064) teaches the CVE Record Format's container
model, where a version entry is one version or a range with a declared `versionType` and a
single `lessThan`/`lessThanOrEqual` boundary per entry (S064's Claim 2). This row teaches a
different machine, named by the round-42 S065 flip: OSV's `affected[].ranges[].events` — a
multi-event timeline (several `fixed` events across branches are required by the page's own
cherry-pick rule, S080.txt:771-773), an implicit `"*"` upper bound, and a range type whose
inclusion query may need "the package ecosystem's own logic" (S080.txt:724-725) or a Git
repository — expressiveness the CVE format's one-boundary version entries do not carry. CSAF/VEX
(F21) is advisory product-status vocabulary and CycloneDX (F23) is SBOM analysis states; neither
models ecosystem-scoped version timelines. This row re-opens the round-42 S065 screen under its
recorded flip condition ("a future frontier needs OSV-specific range semantics
(affected[].ranges[].events ...) that the CVE format cannot express" — corpus/SOURCES.md S065,
rejected 2026-10-28); the flip's other named term (`database_specific` `extracted_events`) does
not appear on the opened page — `grep -c extracted corpus/source-snapshots/round-50/S080.txt`
prints 0 — and the page declares per-database `database_specific` values beyond its scope (Q11,
S080.txt:790-793), so this row claims nothing about them.

documentation-only: this entry describes a published format for reading records; it instructs
no probing, scanning or submission against any target, and carries no credential material (Q6).

## Correction (round 57, 2026-11-02) — evaluation union and exclusion scope

Supersedes Claim 2's implication that events alone decide affectedness and Claim 3's
sentence beginning `A record may carry` at original line 60; preserves the historical bytes.
Correction source: S089, https://ossf.github.io/osv-schema/, Evaluation and Requirements,
version 1.9.2, independently reopened 2026-11-02; captured at
`corpus/source-snapshots/round-57/S089.txt` lines 760-761 and 819-856.
Correction verified-at: 2026-11-02.
Correction recheck (from lane root): `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089`.

For the matching package, explicit version membership OR any range membership establishes
affectedness. Excluding a version from a range does not cancel its explicit membership.
The fixed/last_affected prohibition is per events array, not per record, package, or all ranges.
Boundary decisions differ: fixed excludes its boundary; last_affected includes its boundary.
Absent explicit limits means no upper limit; the old Claim 2 wording `still bounded` must
not be read as a finite bound. Event values and explicit versions have distinct comparison roles.
Located source quotes are recorded once in `corpus/lessons/round-57.md` Gate, Q1/Q2.

Operational check: `python3 corpus/instruments/osv-semantic-check.py` exercises frozen
synthetic inputs, including explicit-only and explicit-overrides-fixed, separate-arrays
versus mixed-same-array, wrong-package, boundaries, and unsupported comparators.
`osv-affectedness.py` is a deliberately bounded teaching implementation, NOT a scanner:
exact ecosystem/name identity; exact explicit-version strings; numeric-release-only SEMVER
x.y.z without leading zeros (plus introduced 0 / limit *). Prereleases/build metadata,
ECOSYSTEM and GIT range comparison are unsupported, not inferred unaffected. Another
supported true OR limb may still establish affectedness. Structural errors in matching
entries are rejected before evaluation; conflicting equal-version event kinds are unsupported.
This extra validation is local admission policy, not the specification's evaluation pseudocode.
It neither validates the full OSV schema nor establishes deployment exposure, exploitability,
withdrawal handling, normalized package equivalence, or authorization to test a real target.

Gate rejection: a universal comparator and a range-only classifier are refused. Flip requires
an independently sourced comparator and new frozen semantic controls, not a type-name cast.
