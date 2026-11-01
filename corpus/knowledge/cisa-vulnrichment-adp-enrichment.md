# CISA Vulnrichment — CISA's ADP-container enrichment of public CVE records: SSVC decision points on every analyzed CVE, CWE and/or CVSS for higher-risk ones, KEV blocks for KEV-listed CVEs, a CNA-precedence rule that drops ADP assessments when the CNA catches up, a major.minor.patch SSVC version encoding, and CPE discontinued since 2024-12-10

source: S081 — https://raw.githubusercontent.com/cisagov/vulnrichment/develop/README.md — capture corpus/source-snapshots/round-51/S081.txt (120 lines, 8290 bytes; sha256 2da0941448d88f48bfc7275c6444abf3aaf57244719e64b3b3ab6591f4458b65; fetched 2026-11-01T02:48:34Z, HTTP 200, 8501 raw bytes — CISA's own README.md at the repository's default branch `develop`): project definition S081.txt:2, process S081.txt:6-8, three decision points S081.txt:14, KEV-block condition S081.txt:58, CPE stop S081.txt:104, drop rule S081.txt:114, SSVC version encoding S081.txt:117-118, consumption note S081.txt:3; manifest corpus/source-snapshots/round-51/manifest.json (12 assertions Q1-Q12, each exactly-once at its pinned anchor)
verified-at: 2026-11-01 (opened this round: the capture is the raw README text at the mutable branch ref, so the recheck pins the captured bytes and the 90d row recheck exists to re-open the ref, not to trust it)
ground: F32
recheck: (python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-51/manifest.json --source S081 || python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-51/manifest.json --source S081)   # interpreter-portable form (run from the lane root, no `cd` prefix); prints S081:sha256 OK then one S081:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

This is CISA's own README of its Vulnrichment project ("# CISA Vulnrichment", S081.txt:1), read as the
agency's self-description of its enrichment program and nothing wider (Q4). The document speaks in the
first person for the program ("CISA will take each CVE through an SSVC scoring process", S081.txt:6), so
every rule below is CISA's stated practice for its own ADP container — not a property of the CVE Record
format, of any CNA, or of ADP publishing in general. The README is on a mutable branch (`develop`) and
says so itself: "This project is under active development, so keep an eye on this README.md for updates."
(S081.txt:4).

## Claim 1 — the program is an enrichment layer on public CVE records, applied in a fixed order

> "the public repository of CISA's enrichment of public CVE records through CISA's ADP (Authorized Data Publisher) container" — S081.txt:2

CISA assesses new and recent CVEs, and "First, CISA will take each CVE through an SSVC scoring process."
(Q2, S081.txt:6). "Every CVE analyzed by the CISA ADP will have three SSVC decision points listed."
(Q5, S081.txt:14). Beyond SSVC, enrichment is conditional: "CISA will determine if there is enough
information to assert a specific CWE identifier and/or a CVSS score." (Q3, S081.txt:7) — for CVEs rated
"Total Technical Impact," "Automatable," or Exploitation "Proof of Concept" or "Active Exploitation"
(S081.txt:7), though CISA reserves the right to provide metrics even to CVEs that do not rate high on any
decision point (S081.txt:7). The falsifiable rule: an ADP container whose SSVC `options` carry a fourth
decision point, or whose CWE/CVSS enrichment is presented as universal, is not describing this program as
its own README defines it.

## Claim 2 — the CNA-precedence rule: ADP data never overwrites and retires on CNA catch-up

> "At no point will CISA overwrite the originating CNA's data in the original CNA container in the CVE record." — Q4, S081.txt:8

Enrichment fills gaps only: CISA populates the ADP container "For those CVEs that do not already have
these fields populated by the originating CNA" (S081.txt:8). The rule has a retirement arm — "if a CVE
entry is updated to include that data after the CISA ADP has made their assessment, the CISA ADP will
drop its own assessments from the CVE entry" (Q8, S081.txt:114) — and a conflict arm: duplicate
CNA-plus-ADP data "should be treated as an error in the CISA ADP container, and the originating CNA's
data should take precedence" (Q9, S081.txt:114). The falsifiable checks: an ADP container that edits a
CNA-container value contradicts the program's own rule (Q4); a reader who treats a surviving ADP CWE/CVSS
as evidence the CNA had none should first check the record's update history, because CNA catch-up removes
the ADP values by design.

## Claim 3 — SSVC data is versioned data: decode against the version, not against an assumed tree

> "this results in a version number of 2.0.3: SSVC version 2.0, CISA Coordinator tree version 3." — Q10, S081.txt:117

SSVC data "is encoded in a way that aligns with the schema for the SSVC version used in the decision tree
that generated the data" (S081.txt:116); the version field encodes `major.minor` as the SSVC version and
`patch` as the decision-tree version. Consumers are "urged to observe the version when decoding SSVC
scores" (Q12, S081.txt:118), and tree updates "will result in changes to the version string"
(S081.txt:118). The falsifiable rule: an SSVC decode that assumes one fixed tree schema across ADP
records can misread records generated under a different `major.minor.patch` — the version field is
load-bearing, not metadata.

## Claim 4 — conditional enrichment is conditional: KEV blocks and the CPE stop

> "For those that aren't, no update will occur." — Q6, S081.txt:58

For CVEs on the KEV catalog the ADP adds a KEV block (S081.txt:58, with the schema asset named in the
README); for those that are not, nothing is added. The rejected over-generalization: **"no KEV block in
the ADP container means the vulnerability is not exploited"** — the README says only that no update will
occur, which is silence, not a negative assertion; exploitation status comes from the KEV catalog itself
(F18), not from the absence of an ADP block. The same conditionality has a sunset: "as of December 10,
2024, CISA will no longer be adding CPE strings to the enriched dataset" (Q7, S081.txt:104) — surviving
CPE strings are historical, so a CPE field in an ADP container is not evidence of current CISA practice.
The README also fixes consumption: "Downstream consumers need not fork and track this GitHub repo if they
are already consuming live CVE data." (Q11, S081.txt:3) — the repo is a window on the enrichment, not a
required distribution channel.

## Distinctness — what this row adds beyond F18/F20/F22/F25/F30

The pre-freeze neighbor screen (run before the round-51 freeze landed; the round-50 D1 lesson makes it
mandatory): `grep -ric vulnrichment corpus/knowledge/ corpus/README.md PROVINCE.md corpus/SOURCES.md
SKILL.md` printed zero hits for every file, and "Authorized Data Publisher" zero hits in PROVINCE.md and
corpus/README.md — the surface is new to the province. The adjacent ground is named, not absorbed: F18
(S052) is the KEV **catalog** — the prioritization feed; this row is the in-record **KEV block** CISA's
ADP writes into CVE records for catalog-listed CVEs (S081.txt:57-68, linking the catalog). F20 (S054) is
CERT/CC's SSVC **framework** — decision points and stakeholder models; this row is CISA's **operational
application** of SSVC to CVE records plus CISA's own version encoding for it (Q10). F22 (S057) is VEX
issuance guidance — the README touches no VEX vocabulary. F25 (S064) is the CVE Record **format** (the
CNA/ADP container model); this row is a content **policy for one ADP's container** — what CISA writes
into it and when it yields (Q4, Q8, Q9) — a layer the format itself does not define. F30 (S078) is the
CVE Services **interface**, whose scope limit says "the service interface only"; the README names the
CVE Services API and the GitHub API as access paths (S081.txt:3) but the surface admitted here is CISA's
enrichment program and its data rules, not the service.

documentation-only: this entry describes a published enrichment program for reading records; it
instructs no probing, scanning or submission against any target, and carries no credential material (Q6).
