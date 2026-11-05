# GitHub Advisory Database: the curation semantics behind the global advisories API

source: S105 — https://docs.github.com/en/code-security/security-advisories/global-security-advisories/about-the-github-advisory-database — GitHub Docs, "GitHub Advisory database"; capture corpus/source-snapshots/round-70/S105.txt (sha256 9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350, 656 lines, 22791 snapshot bytes over 616388 fetched bytes, fetched 2026-11-05T00:14:43Z): the page purpose at S105.txt:558, the advisory classes at S105.txt:568-608, GHSA id shape at S105.txt:611-616, CVSS provenance at S105.txt:621-634, EPSS sync semantics at S105.txt:636-640, community contributions at S105.txt:642-643
verified-at: 2026-11-05
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-70/manifest.json --source S105   # 19 pinned quotes (Q01-Q19), each located at its anchor; every class, source and field rule below is read from the captured page
ground: F48 — what the GitHub Advisory Database *admits* and how it labels it: the three advisory classes (GitHub-reviewed vulnerability, unreviewed NVD-imported vulnerability, malware) with their admission path and alerting consequence, the imported feeds, the supported-registry gate on review, the GHSA identifier shape, CVSS version provenance, EPSS sync semantics, and the community-contribution path. F47/S103 holds the REST read interface and its filter defaults; this entry is the curation semantics F47 explicitly left unopened.

## Scope and decision rule

F47 could say "an unfiltered list returns reviewed, non-malware advisories" but not *what reviewed
means*, *where the unreviewed and malware classes come from*, or *which fields GitHub authored versus
imported*. This entry answers those three questions from the database's own documentation page, so a
reader can decide what a GHSA record proves before treating it as a finding, a fix version or a score.

Decision rule for "what does this advisory record actually assert?":

1. **Class first.** Each advisory is one of three classes, and the class decides whether the record
   was checked for validity at all.
   - **GitHub-reviewed vulnerability.** Advisories are mapped to packages "in ecosystems we support"
     and "We carefully review each advisory for validity and ensure that they contain a full
     description and both ecosystem and package information." (`S105.txt:584`). Review is scoped to a
     supported registry: "We review advisories if they are for a vulnerability in a package that comes
     from a supported registry." (`S105.txt:585`).
   - **Unreviewed vulnerability.** "Unreviewed advisories are published automatically into the GitHub
     Advisory Database, directly from the National Vulnerability Database feed." (`S105.txt:601`), and
     "Dependabot doesn't create Dependabot alerts for unreviewed advisories as this type of advisory
     isn't checked for validity or completion." (`S105.txt:602`). An unreviewed record is an NVD
     import, not a GitHub judgment.
   - **Malware.** "We publish them automatically into the GitHub Advisory Database from the npm
     security team and the OpenSSF Malicious Packages repository." (`S105.txt:604`); they are
     searchable as `type:malware` (`S105.txt:606`), they carry no fix version
     (`S105.txt:571`), and "Our malware advisories are mostly about substitution attacks."
     (`S105.txt:607`).
2. **Then the field provenance.** GHSA ids, CVSS versions and EPSS scores have different authors and
   different update guarantees (table below). A severity read from an imported CVE is the
   maintainer's CVSS version, not GitHub's; an EPSS percentile is only refreshed "when
   significantly different" (`S105.txt:639`).
3. **Then the fix claim.** Vulnerability advisories carry the affected version range and "the earliest
   version where the problem was fixed" (`S105.txt:570`); malware advisories deliberately carry no
   fix version, because "the only safe course of action is not to use the package at all"
   (`S105.txt:571`). A record whose class is malware can never support a "patched in X" statement.

### Advisory classes: admission, alerting, and what the record proves

| class | admission path | Dependabot alert? | what the record proves |
|---|---|---|---|
| GitHub-reviewed vulnerability | imported from the feeds below, then reviewed for validity, description and ecosystem/package data (`S105.txt:584`) | yes, for a dependency on the package (`S105.txt:599`) | a maintained range statement with a fixed version (`S105.txt:570`) |
| unreviewed vulnerability | automatic, directly from the NVD feed (`S105.txt:601`) | no (`S105.txt:602`) | an NVD import only; not checked for validity or completion |
| malware | automatic, from the npm security team and the OpenSSF Malicious Packages repository (`S105.txt:604`) | yes when malware alerts are enabled (`S105.txt:605`) | "no safe versions" (`S105.txt:571`); mostly substitution attacks (`S105.txt:607`) |

The substitution-attack note carries a scoping caveat worth quoting exactly: Dependabot "doesn't look
at project configurations to determine if the packages are coming from a private registry"
(`S105.txt:607`), so a same-name alert cannot distinguish the malicious package from a legitimate one,
and "Users who have their dependencies appropriately scoped should not be affected by malware."
(`S105.txt:607`).

### Imported feeds (the database is an aggregator, not an author)

"We add advisories to the GitHub Advisory Database from the following sources:" (`S105.txt:573`) —
security advisories reported on GitHub, the National Vulnerability Database, the npm Security
advisories database, the FriendsOfPHP database, the Go Vulncheck database, the Python Packaging
Advisory database, the Ruby Advisory database, the RustSec Advisory database, and community
contributions (`S105.txt:574-582`). The page also states the format: "Security advisories are
published as JSON files in the Open Source Vulnerability (OSV) format." (`S105.txt:567`).

### Supported ecosystems (the review gate's allow-list)

Composer, Erlang, Go, GitHub Actions, Maven, Npm, NuGet, Pip, Pub, RubyGems, Rust and Swift
(`S105.txt:586-597`), each named after its package registry except GitHub Actions and Swift, whose
registry cell reads "Swift (registry: N/A)" (`S105.txt:597`). An advisory for a package outside these
registries is not reviewed into the database.

### Field provenance

| field | author | rule and location |
|---|---|---|
| GHSA id | GitHub, on creation or import | `GHSA-xxxx-xxxx-xxxx`, charset `23456789cfghjmpqrvwx`, lowercase (`S105.txt:611-616`) |
| CVSS severity | maintainer for a GitHub-obtained CVE; NVD version for an import | 3.1 and 4.0 supported (`S105.txt:621`); GitHub-obtained CVE uses the maintainer's version, 3.1 or 4.0; imported CVE supports 4.0, 3.1 and 3.0 (`S105.txt:628`) |
| severity label | CVSS Section 5 | one of low, medium/moderate, high, critical (`S105.txt:623-627`) |
| EPSS percentage | FIRST | daily synchronization; percentages "always fully synchronized" (`S105.txt:639`) |
| EPSS percentile | FIRST | refreshed only "when significantly different" (`S105.txt:639`); "we do not author this data, but rather source it from FIRST" (`S105.txt:640`) |
| community edits | GitHub Security Lab curation team | a PR to `github/advisory-database`; published only if accepted (`S105.txt:642`), with credit type "Analyst" (`S105.txt:643`) |

## How this changes a reading

- A count of advisories is a count of *records in one class*, never of "the database". F47's `type`
  filter selects the class; this entry says what each class was checked for.
- A severity or EPSS number is a third-party value passed through GitHub: quote the CVSS version and
  the sync rule rather than treating the displayed number as GitHub's assessment.
- A "no fix" record is evidence about the class (malware), not about remediation effort: the page
  states malware has no safe versions at all.
- Community contributions are reviewed content, not wiki content: acceptance by the Security Lab
  curation team is the gate (`S105.txt:642`).

## Limits

- The page describes policy; it publishes no counts, no review latency and no per-advisory history.
  Nothing here supports "N advisories exist" or "review takes X days".
- Class membership of a specific advisory is a query result (F47's `type` filter), not something this
  page can assert for any one GHSA.
- The OSV-format statement is a format fact; the OSV schema's own fields stay with S080.
- EPSS percentile staleness is documented as a rule, but the page states no tolerance value.
