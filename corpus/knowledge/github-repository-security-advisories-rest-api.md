# GitHub repository security advisories REST API — the machine interface contract for repository security advisories: the endpoint inventory, its permission model, the create/update body contract, the async CVE request, and the private-fork endpoint

source: S087 — https://docs.github.com/en/rest/security-advisories/repository-advisories — capture corpus/source-snapshots/round-55/S087.txt (3407 lines, 137738 snapshot bytes over 937712 fetched HTML bytes; sha256 3eebdf476fbfe5040ad3367edfe3961fbda1bff412bb74ee43bb08ab2f754b93; recorded fetch 2026-11-01T10:46:13Z, HTTP 200 — byte-identical across three same-sha instrument opens this round, probe 10:37:57Z, recorded 10:46:13Z, verification second open; two raw-HTML curl opens were also byte-identical, sha256 89fa9af3…); manifest corpus/source-snapshots/round-55/manifest.json (14 assertions Q1-Q14, each occurrences=1 at its pinned anchor)
verified-at: 2026-11-01 (opened this round; a generated docs.github.com REST reference page — the served page is statically generated and re-fetched byte-identical within the round, but the URL tracks a live document, so the 90d row recheck re-fetches and a changed sha re-fails the capture; the pinned sha256 is the round-55 authority, not the URL's stability)
ground: F36
recheck: (python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-55/manifest.json --source S087 || python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-55/manifest.json --source S087)   # interpreter-portable form (run from the lane root, no `cd` prefix); prints S087:sha256 OK then one S087:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

This is GitHub Docs' own REST API reference for repository security advisories, speaking as the
platform's machine-interface contract: endpoint paths, HTTP methods, fine-grained token permission
sets, request body schemas and response status codes — nothing wider. Every statement here is the
API's declared contract, and this entry is documentation-only — it instructs no call against any
repository or endpoint. The page also carries the "Privately report a security vulnerability"
endpoint (the reporter-flow API); that flow's semantics stay F28/S073 ground — this entry reads the
page's interface contract, not the reporter flow.

## Claim 1 — the advisory machine interface is a twelve-endpoint family with a two-tier permission model

The reference defines the repository-advisories endpoint family: list (repo-scoped and
organization-scoped), create, get, update, advisory comments (list/create/get/update), CVE request,
and the temporary private fork — twelve `…/repos/{owner}/{repo}/security-advisories…` routes on the
page (S087.txt:1353, Q4; :1869, Q6; :2208, Q8; :2827, Q11; :2874, Q14). The permission model is
per-endpoint and two-tiered: read-shaped endpoints name `"Repository security advisories"`
repository permissions (read) (S087.txt:786, Q1 heading over the :790 permission line; :1844, Q5),
write-shaped endpoints (create, update, CVE request) name the (write) set (S087.txt:1287, Q3;
:2135, Q7; :2800, Q10), and the list endpoint additionally serves unauthenticated callers for
public resources: "This endpoint can be used without authentication or the aforementioned
permissions if only public resources are requested." (S087.txt:793, Q2). Falsifiable rule: a token
granted only the (read) set can list and read advisories but cannot create, update or request a CVE
— each mutating route's own permission line is the test. Rejected over-generalization: the
unauthenticated-read carve-out is the LIST endpoint's own line (:793), not a family-wide property —
create, update, get, CVE and fork endpoints carry no such sentence.

## Claim 2 — create and update are distinct methods with a required-body contract and a state machine of exactly three states

Creation is POST on the collection route (S087.txt:1353, Q4) and amendment is PATCH on the advisory
route (S087.txt:2208, Q8); the create body requires summary, description and a vulnerabilities
array ("summary string Required" S087.txt:1304; each advisory carries an advisory state drawn from
a closed vocabulary: "Can be one of: published, closed, draft" (S087.txt:2194, Q9). Falsifiable
rule: an advisory's lifecycle state is exactly one of draft/published/closed — any other state
string in a repository-advisories payload is outside this API's declared contract — and the
severity field is exclusive with the CVSS vector ("You must choose between setting this field or
cvss_vector_string." S087.txt:1338). Rejected over-generalizations: "published" here is the
advisory's own state on the source repository, not the global GitHub Advisory Database entry
(global advisories are a separate reference page outside this capture); and nothing on this page
makes a published state a disclosure by the lane — submission remains operator-gated.

## Claim 3 — requesting a CVE is a distinct async API action, not a field on create

The CVE request is its own route: POST `repos/{owner}/{repo}/security-advisories/{ghsa_id}/cve`
(S087.txt:2827, Q11) under the write permission set (S087.txt:2800, Q10), and its success code is
202 Accepted (S087.txt:2820). Falsifiable rule: a CVE for a repository security advisory is
requested AFTER an advisory exists (the route is keyed by ghsa_id), through a separate call whose
accepted status is 202 — asynchronous processing, not a synchronous assignment in the response body.
Rejected over-generalization: this is the repository-advisories CVE request route only — CVE
numbering policy, the 72-hour review clock and CNA scope stay F29/S076 ground, and the CVE record
format stays F25/S064; this page asserts none of them.

## Claim 4 — the temporary private fork of F29's lifecycle is created through an endpoint needing a second permission

The private fork has its own route: POST `repos/{owner}/{repo}/security-advisories/{ghsa_id}/forks`
(S087.txt:2874, Q14), and it is the one family endpoint whose permission line names TWO permission
sets: `"Repository security advisories" repository permissions (read) and "Administration"
repository permissions (write)` (S087.txt:2853, Q13), with success again 202 Accepted
(S087.txt:2867). Falsifiable rule: creating the collaboration fork by API requires a token holding
both the advisory (read) set and the Administration (write) set — a token with only the advisory
permissions is insufficient by the page's own line. Rejected over-generalizations: the fork
endpoint is the API form of the lifecycle step F29 documents conceptually (the draft advisory, the
temporary private fork) — the lifecycle semantics stay F29/S076 ground and the reporter flow stays
F28/S073; and the dual-permission rule is this endpoint's own line, not a family-wide requirement.

## Distinctness

- vs F28/S073 (private vulnerability reporting, reporter flow): that is the reporter-side flow and
  its form; this page's "Privately report a security vulnerability" endpoint is the same flow's API
  surface, treated here only as an inventoried route — the flow's semantics stay F28.
- vs F29/S074,S076 (maintainer-side advisory lifecycle, concepts doc): that is the lifecycle WHAT
  (draft advisory, private fork, CVE request via GitHub as CNA, credit, fix version); this is the
  interface HOW — routes, methods, permission sets, body schema, status codes. The S076 capture's
  own pointer ("You can also use the REST API to create, list, and update repository security
  advisories." — S076.txt:574) is the lead this round opened; the two grounds are complementary,
  neither subsumes the other.
- vs F30/S078 (CVE Services publication API): that is the CVE Program's own write path; this is
  GitHub's advisory-surface API that requests a CVE from GitHub-as-CNA — different service,
  different identifier space of action.

## Limits

The capture is one reference page at one instant: rate limits, conditional Cloud-plan parameters,
response body examples and error-body schemas are outside the pinned assertions where the page
carries them only in code-sample blocks this entry does not cite. The docs.github.com page is a
live document; byte-stability within the round is measured, cross-round stability is not asserted —
the 90d row recheck re-fetches. Nothing here asserts any repository's actual advisories, and no
call was made against the API: the capture is documentation, and submission/testing remains
refused by the province.
