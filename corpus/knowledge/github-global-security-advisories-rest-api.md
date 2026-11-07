# GitHub global security advisories REST API: the read interface over the GitHub Advisory Database

source: S103 — https://docs.github.com/en/rest/security-advisories/global-advisories — GitHub Docs, "REST API endpoints for global security advisories", REST API version 2026-03-10; capture corpus/source-snapshots/round-69/S103.txt (sha256 c531c1e9b3eb9b4443e9851edc479e137eff772fb41dca3db16d697ac514344f, 585 lines, 15500 snapshot bytes over 329039 fetched bytes, fetched 2026-11-04T22:17:58Z): the page purpose at S103.txt:273, the list endpoint at S103.txt:274-346, the get endpoint at S103.txt:457-476, the request examples at S103.txt:349-357 and S103.txt:479-487
verified-at: 2026-11-04
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-69/manifest.json --source S103   # 13 pinned quotes (Q01-Q13), each located at its anchor; Q11 occurs twice (once per endpoint) and is pinned at its first line; every parameter and value below is read from the captured page, not from a fresh network fetch or a served advisory
ground: F47 — the read interface over GitHub's global advisory database: the two endpoints (list and get-by-GHSA), the list endpoint's filter parameters with their enumerated values and defaults, the reviewed-only/malware-excluded default, the pagination and sort controls, and the unauthenticated-public access statement. The repository-scoped advisory REST API stays with F36/S087, the maintainer advisory lifecycle with F29/S074, and any single advisory's values with S068.

## Scope and decision rule

This entry records how a reader **queries** the GitHub Advisory Database through the REST API: which
endpoints exist, which filters the list endpoint accepts, and what the list returns when no filter is given.
The source is GitHub Docs' own REST reference page for the "global security advisories" category, captured as
HTML and converted to text (`S103.txt:LINE`). The page states its purpose as "Use the REST API to view global
security advisories." (`corpus/source-snapshots/round-69/S103.txt:273`) and is versioned: "API Version: 2026-03-10 (latest)" (`corpus/source-snapshots/round-69/S103.txt:13`);
both request examples send `X-GitHub-Api-Version: 2026-03-10` (`corpus/source-snapshots/round-69/S103.txt:356`, `corpus/source-snapshots/round-69/S103.txt:486`).

Why this is not held ground: the lane's repository-advisory REST entry
(`corpus/knowledge/github-repository-security-advisories-rest-api.md:45-46`, F36/S087) reads "published" as the
advisory's own state on the source repository, "not the global GitHub Advisory Database entry (global
advisories are a separate reference page outside this capture)". This page is that separate reference. S068 holds one advisory instance;
it does not hold the query interface.

Decision rule for "how do I pull advisories from GitHub's database, and what does an unfiltered pull contain?"
— read the reference, then set `type` explicitly:

1. **Two endpoints, both GET.** "List global security advisories" (`corpus/source-snapshots/round-69/S103.txt:274`; request line
   `get/advisories`, `corpus/source-snapshots/round-69/S103.txt:349`, URL `https://api.github.com/advisories`, `corpus/source-snapshots/round-69/S103.txt:357`) and "Get a global
   security advisory" (`corpus/source-snapshots/round-69/S103.txt:457`), which "Gets a global security advisory using its GitHub Security
   Advisory (GHSA) identifier." (`corpus/source-snapshots/round-69/S103.txt:458`); its one path parameter is `ghsa_id string Required`
   (`corpus/source-snapshots/round-69/S103.txt:471`), and it answers `200OK` or `404Resource not found` (`corpus/source-snapshots/round-69/S103.txt:475-476`).
2. **An unfiltered list is not the whole database.** "If no other parameters are defined, the request will
   return only GitHub-reviewed advisories that are not malware." (`corpus/source-snapshots/round-69/S103.txt:275`) and "By default, all
   responses will exclude advisories for malware, because malware are not standard vulnerabilities."
   (`corpus/source-snapshots/round-69/S103.txt:276`). The `type` parameter carries "Default: reviewed" (`corpus/source-snapshots/round-69/S103.txt:293`) and "Can be one of:
   reviewed, malware, unreviewed" (`corpus/source-snapshots/round-69/S103.txt:294`). A count taken from an unfiltered list is therefore a
   count of reviewed, non-malware advisories, never of the database.
3. **Access needs no token for public data.** "This endpoint can be used without authentication if only public
   resources are requested." (`corpus/source-snapshots/round-69/S103.txt:283`, repeated for the get endpoint at `corpus/source-snapshots/round-69/S103.txt:465`), and a
   fine-grained token used with it "does not require any permissions" (`corpus/source-snapshots/round-69/S103.txt:282`). The page lists
   `422Validation failed, or the endpoint has been spammed.` and `429Too many requests` for the list endpoint
   (`corpus/source-snapshots/round-69/S103.txt:345-346`); it states no numeric rate limit.

### The list endpoint's filters (as the page declares them)

| parameter | declared type | values / default | location |
|---|---|---|---|
| `ghsa_id` | string | one GHSA identifier | `corpus/source-snapshots/round-69/S103.txt:289-290` |
| `type` | string | `reviewed`, `malware`, `unreviewed`; default `reviewed` | `corpus/source-snapshots/round-69/S103.txt:291-294` |
| `cve_id` | string | one CVE identifier | `corpus/source-snapshots/round-69/S103.txt:295-296` |
| `ecosystem` | string | `rubygems`, `npm`, `pip`, `maven`, `nuget`, `composer`, `go`, `rust`, `erlang`, `actions`, `pub`, `other`, `swift` | `corpus/source-snapshots/round-69/S103.txt:297-299` |
| `severity` | string | `unknown`, `low`, `medium`, `high`, `critical` | `corpus/source-snapshots/round-69/S103.txt:300-302` |
| `cwes` | string or array of strings | e.g. `cwes=79,284,22` | `corpus/source-snapshots/round-69/S103.txt:303-305` |
| `is_withdrawn` | boolean | — | `corpus/source-snapshots/round-69/S103.txt:306-307` |
| `affects` | string or array of strings | package or package@version; "A maximum of 1000 packages can be specified." | `corpus/source-snapshots/round-69/S103.txt:308-311` |
| `published`, `updated`, `modified` | string | a date or date range | `corpus/source-snapshots/round-69/S103.txt:312-320` |
| `epss_percentage`, `epss_percentile` | string | match on the advisory's EPSS values | `corpus/source-snapshots/round-69/S103.txt:321-326` |
| `before`, `after` | string | a cursor from the Link header | `corpus/source-snapshots/round-69/S103.txt:327-330` |
| `direction` | string | `asc`, `desc`; default `desc` | `corpus/source-snapshots/round-69/S103.txt:331-334` |
| `per_page` | integer | "The number of results per page (max 100)."; default 30 | `corpus/source-snapshots/round-69/S103.txt:335-337` |
| `sort` | string | `updated`, `published`, `epss_percentage`, `epss_percentile`; default `published` | `corpus/source-snapshots/round-69/S103.txt:338-341` |

Two consequences for bounty and disclosure work. First, the database exposes EPSS as a filter and sort key
(`corpus/source-snapshots/round-69/S103.txt:321-326`, `corpus/source-snapshots/round-69/S103.txt:341`); the page's own gloss is "The EPSS percentage represents the likelihood of
a CVE being exploited." (`corpus/source-snapshots/round-69/S103.txt:323`) — the score's meaning and model stay with F19, and this page only
states that the database carries it. Second, `ecosystem` is a closed list of thirteen values on this page
(`corpus/source-snapshots/round-69/S103.txt:299`): an advisory for a package outside those ecosystems cannot be selected by ecosystem here.

### What the page does not establish

- **No response schema is in the capture.** The page shows one example response per endpoint
  (`corpus/source-snapshots/round-69/S103.txt:358-456` and the get example after `corpus/source-snapshots/round-69/S103.txt:487`); its field names (`ghsa_id`, `cve_id`,
  `type`, `severity`, `vulnerabilities[].vulnerable_version_range`, `cvss_severities.cvss_v3/cvss_v4`, `epss`,
  `withdrawn_at`, `credits`, at `corpus/source-snapshots/round-69/S103.txt:365-430`) are an example's keys, and its values
  ("Heartbleed security advisory", `CVE-2050-00000`) are placeholders. The collapsed "Response schema" tab
  (`corpus/source-snapshots/round-69/S103.txt:360`) was not expanded by the static capture. Read keys from the example, never values.
- **No database semantics.** What "reviewed" requires, how malware advisories are curated and how unreviewed
  advisories enter are deferred to "About the GitHub Advisory database" (`corpus/source-snapshots/round-69/S103.txt:276`), which was not opened.
- **No ordering guarantee beyond `sort`/`direction`, no completeness statement, no numeric rate limit.**

## Gate

Admitted 2026-11-04 (round 69) on S103, opened this round by the L1 (`capture-source.py --kind html`, HTTP
200, 329039 fetched bytes). Located quote (≤25 words, `corpus/source-snapshots/round-69/S103.txt:275`): "If no other parameters are defined,
the request will return only GitHub-reviewed advisories that are not malware." Thirteen quotes are pinned in
`corpus/source-snapshots/round-69/manifest.json` (maximum 17 words).

Refused the same round: ENISA's EUVD API documentation (https://euvd.enisa.europa.eu/apidoc) — the served
HTML is a 3062-byte single-page-application shell with no documentation text; the text exists only after
JavaScript rendering, so the lane's capture instrument cannot produce a line-anchored snapshot (receipt
`.ufo/waves/round-69/controls/euvd-refusal-r69.txt`). Flip condition: a statically served or line-anchorable
rendering of the same documentation.
