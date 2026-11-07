# GitHub Advisory Database: the curation semantics behind the global advisories API

source: S105 — https://docs.github.com/en/code-security/security-advisories/global-security-advisories/about-the-github-advisory-database — GitHub Docs, "GitHub Advisory database"; capture corpus/source-snapshots/round-70/S105.txt (sha256 9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350, 656 lines, 22791 snapshot bytes over 616388 fetched bytes, fetched 2026-11-05T00:14:43Z): the page purpose at S105.txt:558, the class sub-headings at S105.txt:568-572 and S105.txt:600-607, the sources and ecosystem lists at S105.txt:573-599, GHSA id shape at S105.txt:611-616, CVSS provenance at S105.txt:621-628, EPSS sync semantics at S105.txt:639-640, community contributions at S105.txt:642-643
verified-at: 2026-11-04
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-70/manifest.json --source S105   # 19 pinned quotes (Q01-Q19), each located at its anchor; every quoted rule below is pinned to its anchor, while the class count and the two F47-derived reading rules are this entry's reading and are marked as such
ground: F48 — what the GitHub Advisory Database *admits* and how it labels it: the page's three class sub-headings (GitHub-reviewed vulnerability, unreviewed NVD-imported vulnerability, malware) with their admission path and alerting consequence, the eight imported feeds plus the community-contribution channel, the supported-registry gate on review, the GHSA identifier shape, CVSS version provenance, EPSS sync semantics, and the community-contribution path. F47/S103 holds the REST read interface and its filter defaults; this entry is the curation semantics F47 explicitly left unopened.

## Scope and decision rule

F47 could say "an unfiltered list returns reviewed, non-malware advisories" but not *what reviewed
means*, *where the unreviewed and malware records come from*, or *which fields GitHub authored versus
imported*. This entry answers those three questions from the database's own documentation page, so a
reader can decide what a GHSA record proves before treating it as a finding, a fix version or a score.

Decision rule for "what does this advisory record actually assert?":

1. **Class first.** The page groups records under three class sub-headings — "GitHub-reviewed
   vulnerability advisories" (`corpus/source-snapshots/round-70/S105.txt:572`), "Unreviewed vulnerability advisories"
   (`corpus/source-snapshots/round-70/S105.txt:600`) and "Malware advisories" (`corpus/source-snapshots/round-70/S105.txt:603`) — and its intro only says the problems
   "come in several varieties" (`corpus/source-snapshots/round-70/S105.txt:569`). Review status decides whether validity was checked:
   reviewed records are checked (`corpus/source-snapshots/round-70/S105.txt:584`), unreviewed ones are not (`corpus/source-snapshots/round-70/S105.txt:602`), and the
   page says nothing about a validity review of malware records.
   - **GitHub-reviewed vulnerability.** Advisories are mapped to packages "in ecosystems we support"
     and "We carefully review each advisory for validity and ensure that they contain a full
     description and both ecosystem and package information." (`corpus/source-snapshots/round-70/S105.txt:584`). Review is scoped to a
     supported registry: "We review advisories if they are for a vulnerability in a package that comes
     from a supported registry." (`corpus/source-snapshots/round-70/S105.txt:585`).
   - **Unreviewed vulnerability.** "Unreviewed advisories are published automatically into the GitHub
     Advisory Database, directly from the National Vulnerability Database feed." (`corpus/source-snapshots/round-70/S105.txt:601`), and
     "Dependabot doesn't create Dependabot alerts for unreviewed advisories as this type of advisory
     isn't checked for validity or completion." (`corpus/source-snapshots/round-70/S105.txt:602`). An unreviewed record is an NVD
     import, not a GitHub judgment.
   - **Malware.** "We publish them automatically into the GitHub Advisory Database from the npm
     security team and the OpenSSF Malicious Packages repository." (`corpus/source-snapshots/round-70/S105.txt:604`); they are
     searchable as `type:malware` (`corpus/source-snapshots/round-70/S105.txt:606`); "Malware alerts do not contain a fix version,
     because the defining characteristic of a malware alert is that there are no safe versions"
     (`corpus/source-snapshots/round-70/S105.txt:571`); and "Our malware advisories are mostly about substitution attacks."
     (`corpus/source-snapshots/round-70/S105.txt:607`).
2. **Then the field provenance.** GHSA ids, CVSS versions and EPSS scores have different authors and
   different update guarantees (table below). The CVSS-version rule is branch-specific: "If GitHub
   obtains a CVE, the GitHub Advisory Database uses the CVSS version assigned by the maintainer, which
   can be version 3.1 or 4.0. If the CVE is imported, the GitHub Advisory Database supports CVSS
   versions 4.0, 3.1 and 3.0." (`corpus/source-snapshots/round-70/S105.txt:628`) — the page does not state who assigns an imported
   CVE's version. An EPSS percentile is only refreshed "when significantly different"
   (`corpus/source-snapshots/round-70/S105.txt:639`).
3. **Then the fix claim.** Vulnerability advisories carry the affected version range and "the earliest
   version where the problem was fixed" (`corpus/source-snapshots/round-70/S105.txt:570`). Malware alerts "do not contain a fix
   version" (`corpus/source-snapshots/round-70/S105.txt:571`), but the page elsewhere lists "patched versions" among the fields an
   advisory may carry (`corpus/source-snapshots/round-70/S105.txt:622`), so read the fix field per record rather than inferring it from
   the class; a malware record should not be read as a patched-in-X statement without that field.

### Advisory classes: admission, alerting, and what the record proves

| class | admission path | Dependabot alert? | what the record proves |
|---|---|---|---|
| GitHub-reviewed vulnerability | listed as a source of reviewed advisories (`corpus/source-snapshots/round-70/S105.txt:573-582`), then reviewed for validity, description and ecosystem/package data within a supported registry (`corpus/source-snapshots/round-70/S105.txt:584-585`); NVD appears both here and as the unreviewed feed (`corpus/source-snapshots/round-70/S105.txt:601`) | yes, if Dependabot alerts are enabled, for a dependency on the package (`corpus/source-snapshots/round-70/S105.txt:599`) | a maintained range statement with a fixed version (`corpus/source-snapshots/round-70/S105.txt:570`) |
| unreviewed vulnerability | automatic, directly from the NVD feed (`corpus/source-snapshots/round-70/S105.txt:601`) | no (`corpus/source-snapshots/round-70/S105.txt:602`) | an NVD import only; not checked for validity or completion |
| malware | automatic, from the npm security team and the OpenSSF Malicious Packages repository (`corpus/source-snapshots/round-70/S105.txt:604`) | yes when malware alerts are enabled (`corpus/source-snapshots/round-70/S105.txt:605`) | malware alerts carry no fix version (`corpus/source-snapshots/round-70/S105.txt:571`); mostly substitution attacks (`corpus/source-snapshots/round-70/S105.txt:607`) |

The substitution-attack note carries a scoping caveat worth quoting exactly: Dependabot "doesn't look
at project configurations to determine if the packages are coming from a private registry"
(`corpus/source-snapshots/round-70/S105.txt:607`), so a same-name alert cannot distinguish the malicious package from a legitimate one,
and "Users who have their dependencies appropriately scoped should not be affected by malware."
(`corpus/source-snapshots/round-70/S105.txt:607`).

### Sources: eight imported feeds plus a community-contribution channel

"We add advisories to the GitHub Advisory Database from the following sources:" (`corpus/source-snapshots/round-70/S105.txt:573`).
The eight feeds are security advisories reported on GitHub, the National Vulnerability Database, the
npm Security advisories database, the FriendsOfPHP database, the Go Vulncheck database, the Python
Packaging Advisory database, the Ruby Advisory database and the RustSec Advisory database
(`corpus/source-snapshots/round-70/S105.txt:574-581`); the ninth bullet is community contributions through pull requests to
`github/advisory-database` (`corpus/source-snapshots/round-70/S105.txt:582`), which the page treats as an editing channel rather than a
feed. The page also states the storage format: "Security advisories are published as JSON files in the
Open Source Vulnerability (OSV) format." (`corpus/source-snapshots/round-70/S105.txt:567`). The page's own "we do not author this data"
sentence (`corpus/source-snapshots/round-70/S105.txt:640`) is scoped to EPSS, not to the advisory records.

### Supported ecosystems (the review gate's allow-list)

"Generally, we name our supported ecosystems after the software programming language's associated
package registry." (`corpus/source-snapshots/round-70/S105.txt:585`) — Composer, Erlang, Go, GitHub Actions, Maven, Npm, NuGet, Pip,
Pub, RubyGems, Rust and Swift (`corpus/source-snapshots/round-70/S105.txt:586-597`). GitHub Actions' cell is a marketplace URL, not a
registry (`corpus/source-snapshots/round-70/S105.txt:589`); only Swift reads "Swift (registry: N/A)" (`corpus/source-snapshots/round-70/S105.txt:597`). The page states
no converse about packages outside these registries: unreviewed records are in the database
(`corpus/source-snapshots/round-70/S105.txt:601`) and the list is open to suggestions (`corpus/source-snapshots/round-70/S105.txt:598`).

### Field provenance

| field | author | rule and location |
|---|---|---|
| GHSA id | GitHub, on creation or import | `GHSA-xxxx-xxxx-xxxx`, charset `23456789cfghjmpqrvwx`, lowercase (`corpus/source-snapshots/round-70/S105.txt:611-616`) |
| CVSS version | maintainer for a GitHub-obtained CVE; unstated for an import | 3.1 and 4.0 supported (`corpus/source-snapshots/round-70/S105.txt:621`); GitHub-obtained CVE uses the maintainer's version (3.1 or 4.0); an imported CVE supports 4.0, 3.1 and 3.0 (`corpus/source-snapshots/round-70/S105.txt:628`) |
| severity label | unstated | one of four levels defined in CVSS Section 5: low, medium/moderate, high, critical (`corpus/source-snapshots/round-70/S105.txt:623-627`); the page does not state who maps a score to a label |
| EPSS percentage | FIRST | daily synchronization; percentages "will always be fully synchronized" (`corpus/source-snapshots/round-70/S105.txt:639`) |
| EPSS percentile | FIRST | refreshed only "when significantly different" (`corpus/source-snapshots/round-70/S105.txt:639`); "we do not author this data, but rather source it from FIRST" (`corpus/source-snapshots/round-70/S105.txt:640`); not editable in community contributions (`corpus/source-snapshots/round-70/S105.txt:640`) |
| community edits | submitter, gated by GitHub Security Lab | a PR to `github/advisory-database` may edit or add detail (ecosystems, severity, description); the Security Lab curation team reviews and publishes if accepted (`corpus/source-snapshots/round-70/S105.txt:642`); the submitter is credited with type "Analyst" (`corpus/source-snapshots/round-70/S105.txt:643`) |

## How this changes a reading

- *(F47-derived reading, not S105's words.)* A count from F47's unfiltered list is a count of reviewed,
  non-malware records, never of "the database" (S103.txt:275-276); this entry says what each class was
  checked for.
- Split three numbers that are often collapsed: the CVSS **version** and score are the maintainer's or
  an import's (`corpus/source-snapshots/round-70/S105.txt:628`), the four **severity labels** are CVSS Section 5 bands with an unstated
  mapping author (`corpus/source-snapshots/round-70/S105.txt:623`), and **EPSS** is FIRST's data passed through GitHub with the sync
  rule above (`corpus/source-snapshots/round-70/S105.txt:639-640`).
- A malware record's missing fix version is a class rule about alerts (`corpus/source-snapshots/round-70/S105.txt:571`), not a
  remediation judgment: check the record's own patched-versions field (`corpus/source-snapshots/round-70/S105.txt:622`) before saying
  anything about a fix.
- A community contribution is reviewed content: acceptance by the Security Lab curation team is the
  gate (`corpus/source-snapshots/round-70/S105.txt:642`), and the contributor is credited rather than treated as the author of the
  record.

## Limits

- The page describes policy; it publishes no counts, no review latency and no per-advisory history.
  Nothing here supports "N advisories exist" or "review takes X days".
- Class membership of a specific advisory is a query result (F47's `type` filter), not something this
  page can assert for any one GHSA.
- The OSV-format statement is a format fact; the OSV schema's own fields stay with S080.
- EPSS percentile staleness is documented as a rule, but the page states no tolerance value.
- The page does not state who assigns an imported CVE's CVSS version, nor who maps a score to the four
  severity labels.
