# OSV.dev's import bar for an OSV record: the purpose, the schema-validation prerequisite, package-level precision as the minimum, distinct range ends, GIT commits in the named repo, and live reference URLs

source: S116 — https://google.github.io/osv.dev/data_quality.html (anchor: the "Properties of a High Quality OSV Record" page, version 1.0.0, capture corpus/source-snapshots/round-82/S116.txt)
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-82/manifest.json --source S116

## Attribution

This is the OSV.dev project's own page headed "Properties of a High Quality OSV Record" (S116.txt:21), version "1.0.0 (SEMVER)" (S116.txt:22-23). It is the document the importfindings page links as the quality bar (F57, `corpus/knowledge/osv-importfindings-record-quality-feedback.md`, S115.txt:14). Every claim below is the page's own statement, quoted from the pinned capture `corpus/source-snapshots/round-82/S116.txt` with the line the text occupies. The manifest records `https://google.github.io/osv.dev/data_quality.html` as both the requested and the final URL at HTTP 200 (`corpus/source-snapshots/round-82/manifest.json`, `fetched_utc 2026-11-06T20:53:38Z`).

Why it is bounty ground: a researcher who files or reviews an advisory that will be published in OSV format (a GHSA, a home-database record) can check these properties before submission, and a record that misses them is the kind the import-findings endpoint reports as not imported (F57 Claim 3).

## Claim 1 — the purpose: the "good enough" record OSV.dev imports

"Describe the “good enough” OSV record that will be imported by OSV.dev" (S116.txt:25). The page defines an import threshold, not an ideal record: what a record must carry for OSV.dev to import it (S116.txt:25).

Falsifiable rule: a reviewer who treats this page as an optional style guide for OSV records misreads its stated purpose, which ties the properties to records OSV.dev will import (S116.txt:25). A reader checks it by reading the Purpose line under the version.

Rejected over-generalization, not a page sentence: every record that meets these properties stays in OSV.dev forever. The page puts later revalidation of imported records out of scope (S116.txt:27, not pinned) and makes no permanence promise.

## Claim 2 — the prerequisite: schema validation against the declared schema_version

"a record passes JSON Schema validation for the version of the OSV Schema it declares itself to comply with in the schema_version field" (S116.txt:36). Validation is against the schema version the record itself declares (S116.txt:36); the same sentence names 1.0.0 as the version used when the field is absent (S116.txt:36, outside the pinned span).

Falsifiable rule: validating a record that declares schema_version 1.2.0 against the latest OSV Schema instead of 1.2.0 departs from the page, which binds validation to the declared version (S116.txt:36). A reader checks it by reading the Valid paragraph's first sentence.

Rejected over-generalization, not a page sentence: passing JSON Schema validation alone makes a record high quality. The page calls it a prerequisite (S116.txt:36) and lists the Precise and Identifiable properties after it (S116.txt:37-55).

## Claim 3 — package-level precision is the minimum

"Package-level precision is the minimum standard." (S116.txt:41). A record must at least let a consumer decide impact per package; symbol-level detail is finer than the floor (S116.txt:41).

Falsifiable rule: an advisory that names only a vendor or a product line, with no package an automated consumer can match, is below the floor the page sets at package level (S116.txt:41). A reader checks it by reading the paragraph after the three consumer questions.

Rejected over-generalization, not a page sentence: OSV.dev requires vulnerable-function or symbol data in every record. The page sets the minimum at package level (S116.txt:41) and defers validating vulnerable functions to a future iteration (S116.txt:28, not pinned).

## Claim 4 — a range's introduced and fixed values must differ

"introduced and fixed versions or commits can’t be the same" (S116.txt:44). A range whose introduced event equals its fixed (or last_affected) event describes no affected span, and the page lists distinct ends as a property of a precise record (S116.txt:44).

Falsifiable rule: a submitted range with introduced 1.4.0 and fixed 1.4.0 fails the distinct-ranges property the page lists for precise records (S116.txt:44). A reader checks it by reading the third bullet under Precise.

Rejected over-generalization, not a page sentence: any two ranges in one record must not share a version. The bullet speaks of introduced against fixed or last_affected within a range (S116.txt:44), not of separate ranges.

## Claim 5 — GIT range commits must exist in the specified repo

"for commit (GIT) ranges the commits exist in the specified repo (i.e. they are not from another GitHub fork)" (S116.txt:47). A commit hash taken from a fork, absent from the repo the range names, fails the property (S116.txt:47).

Falsifiable rule: a GIT range whose fixed commit lives only in a contributor's fork, not in the repo URL the range declares, breaks the commits-exist property (S116.txt:47). A reader checks it by reading the sixth bullet under Precise.

Rejected over-generalization, not a page sentence: every GIT commit must be on the default branch. The page requires existence in the specified repo (S116.txt:47); it names no branch.

## Claim 6 — reference URLs answer 2xx or 3xx at publication

"reference URLs return a 2xx or 3xx response at the time of publication" (S116.txt:51). The check is tied to the publication instant; a redirect is acceptable (S116.txt:51).

Falsifiable rule: a record published with a reference that answered 404 at publication fails the property; one whose link breaks a year later does not, by this page's wording (S116.txt:51). A reader checks it by reading the last bullet under Precise.

Rejected over-generalization, not a page sentence: reference URLs must keep resolving for the life of the record. The page binds the response codes to the time of publication (S116.txt:51) and leaves later bit rot to a separate document (S116.txt:27, not pinned).

## Distinctness

- F31 / S080 (`corpus/knowledge/osv-affected-range-events.md`) holds the OSV range-event format: the four event verbs, the fixed-or-last_affected exclusivity (S080.txt:760-761) and the preference for fixed over last_affected (S080.txt:762-766). This page repeats that preference (S116.txt:43) and the exclusivity in its appendix (S116.txt:86); neither is pinned or claimed here. Claim 4 (introduced differs from fixed) is not a schema rule F31 states.
- F57 / S115 (`corpus/knowledge/osv-importfindings-record-quality-feedback.md`) holds the endpoint that reports records failing the quality bar; it names this page only as an unopened link (its Limits, "the quality bar itself"). This entry holds the bar.
- Literal sweep before this entry: `grep -rli -- '<q>' corpus/knowledge` for "good enough", "JSON Schema validation", "Package-level precision", "distinct ranges", "another GitHub fork", "2xx or 3xx" printed nothing for each (run 2026-11-06).

## Not claimed

Not claimed: the out-of-scope note and its companion document "Managing the Perishability of OSV Records" (S116.txt:27, unopened); the deferred vulnerable-function validation (S116.txt:28); the audience and rationale (S116.txt:29-33); the consumer questions (S116.txt:38-40); the bullets of S116.txt:42-43, 45-46 and 48-50 (introduced defined, the fixed-over-last_affected preference held by F31, introduced before fixed, versions exist in the ecosystem, ecosystem and name canonical, purl conformance); the Identifiable clauses (S116.txt:52-55); the example records (S116.txt:56-62, sample data); Appendix A (S116.txt:63-86), which the page itself labels as generated by Gemini from the OSV JSON schema (S116.txt:64) — a summary of the schema, held at its source by F31 / S080.

## Gate — S116 (OSV.dev, Properties of a High Quality OSV Record)

- **URL:** https://google.github.io/osv.dev/data_quality.html (HTTP 200; the manifest records the final URL equal to the requested URL).
- **Access date:** 2026-11-06. Capture `corpus/source-snapshots/round-82/S116.txt` (sha256 `2198d329bf6a8711ac28ae9221351162d61679699c0b45acb8ebb95cadce9ca0`, 87 lines, 6586 snapshot bytes; the served page was 24473 raw bytes), `fetched_utc 2026-11-06T20:53:38Z`.
- **Six located quotes, one per claimed clause, each verbatim at its snapshot line, word counts by `len(quote.split())`:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| cl1 purpose | Q01-purpose | S116.txt:25 | 12 | Describe the “good enough” OSV record that will be imported by OSV.dev |
| cl2 valid prerequisite | Q02-valid-prerequisite | S116.txt:36 | 23 | a record passes JSON Schema validation for the version of the OSV Schema it declares itself to comply with in the schema_version field |
| cl3 package-level minimum | Q03-package-level-minimum | S116.txt:41 | 6 | Package-level precision is the minimum standard. |
| cl4 distinct range ends | Q04-distinct-ranges | S116.txt:44 | 10 | introduced and fixed versions or commits can’t be the same |
| cl5 GIT commits in repo | Q05-git-commits-in-repo | S116.txt:47 | 19 | for commit (GIT) ranges the commits exist in the specified repo (i.e. they are not from another GitHub fork) |
| cl6 reference URLs | Q06-reference-urls | S116.txt:51 | 13 | reference URLs return a 2xx or 3xx response at the time of publication |

- **Recheck receipt:** the `recheck:` line above printed `S116:sha256 OK` and one `S116:<pin> OK occurrences=1 anchor=<n>-ok` line per pinned quote, exit 0 (`.ufo/waves/round-82/controls/c2-prefreeze-r82.txt`).

## Limits

The page does not establish, and this entry does not claim:

- how OSV.dev enforces each property or which import finding a failure produces: the capture carries the word only in the navigation link `GET /v1experimental/importfindings` (S116.txt:7) and states no enforcement rule; `grep -n -i -E 'IMPORT_FINDING|finding' corpus/source-snapshots/round-82/S116.txt` prints that one navigation line and exits 0.
- that a record meeting the properties is imported, or a record missing one is refused, in any specific case; this entry made no call to api.osv.dev or to any import pipeline.
- the current state of the page: the manifest records the fetch instant 2026-11-06T20:53:38Z, version 1.0.0 (S116.txt:23).

Scope limit: six properties of the OSV.dev import bar as stated on the "Properties of a High Quality OSV Record" page only — the purpose (S116.txt:25), the schema-validation prerequisite (S116.txt:36), the package-level minimum (S116.txt:41), distinct introduced and fixed values (S116.txt:44), GIT commits in the specified repo (S116.txt:47) and reference URLs at publication (S116.txt:51). The range-event format stays with F31 (S080) and the import-findings endpoint with F57 (S115).
