# CriticC2 — F48 entry vs S105: overreach audit

Seat: CriticC2 (leaf, no dispatch). Target: `corpus/knowledge/github-advisory-database-curation-semantics.md`
at frozen `e74ba6b5d522b1e91dca3a2d244585d6b7babdc5`, against `corpus/source-snapshots/round-70/S105.txt`.
No lane file edited. Lane reads via `git show`/`git archive` only.

## Verdict

The mechanical provenance layer is sound and current: all 19 pinned quotes locate at their anchors, the
entry's own `recheck:` line exits 0, and a live refetch today reproduces the pinned snapshot byte-for-byte
(zero drift). The **prose** layer does not survive as written: 5 wrong/misquoted statements and 6
unsupported generalizations, the worst being that rule 2 inverts the page's own CVSS provenance
distinction and that rule 1 states a class count the page never states.

C2's frozen predicate (counters) is untouched by any of this — no counter moves. What is refuted is the
entry's own provenance claim (`...:5`, "every class, source and field rule below is read from the captured
page"), not the admission of F48.

## Receipts (all under /fast/scratch/hyaku/kasegi-r70/CriticC2, removed before yield)

```
$ git -C <lane> archive e74ba6b… corpus/source-snapshots/round-70/S105.txt \
      corpus/source-snapshots/round-70/manifest.json corpus/knowledge/…-semantics.md | tar -x -C $S
9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350  corpus/source-snapshots/round-70/S105.txt
d479c4954675b52c1ae49901efb1c780f686d686c96f6f24e4ab31d660fea72f  corpus/knowledge/…-semantics.md
22791 corpus/source-snapshots/round-70/S105.txt ; 656 lines          # matches :3 and pins-r70.txt
```
Both hashes equal `pins-r70.txt`. Snapshot bytes/lines match the entry's header claim exactly.

```
$ python3 -B source-recheck.py --manifest corpus/source-snapshots/round-70/manifest.json --source S105
S105:sha256 OK
S105:Q01-purpose OK occurrences=1 anchor=558-ok      … Q19-credit OK occurrences=1 anchor=643-ok
exit=0        # 19/19 OK, snapshot sha256 unchanged after the run (instrument wrote nothing)
```
Independent re-check of every quoted span in the entry against its cited line (substring test, 18 explicit
`"quote" (`S105.txt:N`)` pairs): **17 OK, 1 MISS** — see O13.

### Drift test (live page, today)

```
$ curl -sS -L -A "Mozilla/5.0 (compatible; omp-critic/1.0)" -o live-S105.html <S105 url>
200 616388                       # byte count identical to manifest .bytes
$ sha256(live html) = 4d46d23199ae03f90f1dabcf7a8f8df8e048300478dc287508901bfe51b0aa80
$ re-applied the instrument's own html_to_text (capture-source.py:48-53) to that html:
live text sha256 = 9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350
identical: True | 656 lines
```
**Zero drift.** Every citation below is current against the live page as of 2026-11-05T00:30Z (host local
2026-11-04 21:30 -03). No finding in this report is a staleness finding.

## The seven assigned questions

### (a) "three advisory classes" — the page does not say three

Structure: one section heading `Types of security advisories` (L568), then **three class sub-headings**:
`GitHub-reviewed vulnerability advisories` (L572), `Unreviewed vulnerability advisories` (L600),
`Malware advisories` (L603). There is no fourth class heading. The page TOC (L560-565) lists only
`About…`, `Types of security advisories`, `Information…`, `Community contributions`, `Further reading` —
the three class names do not appear in it.

The only count language on the page is **"These problems come in several varieties"** (L569), followed by
exactly two definitions: vulnerability (L570) and malware (L571). The word "three" never occurs in the
snapshot near advisories (`grep -nE "three|several|varieties"` → only L569, L602, L607, L643).

So: the three-count is the entry's structural reading of three headings, presented as a page fact at
`…:6` ("the three advisory classes"), `…:17` ("one of three classes") and repeated in `corpus/README.md`
F48 row and the manifest note. It is corroborated by **S103**, not S105: the REST `type` parameter
"Can be one of: reviewed, malware, unreviewed" (`S103.txt:294`, F47/S103). That is a legitimate
corroboration — but it is a second authority, and the entry must cite it as such.

Second defect in the same sentence: the partition mixes two axes. L570/L571 split by *kind*
(vulnerability vs malware); L572/L600 split vulnerability by *review status*. A malware record is
auto-published (L604) and the page never says it was reviewed for validity, so "one of three classes"
cannot represent it on one axis.

### (b) malware "can never support a patched-in-X statement" — overreach, and in tension with L622

Source, L571: "Malware alerts do not contain a fix version, because the defining characteristic of a
malware alert is that there are no safe versions—the only safe course of action is not to use the package
at all."

Source, L622 (the page's own field inventory): "Each security advisory contains information about **the
vulnerability or malware**, which **may include** the description, severity, affected package, package
ecosystem, affected versions **and patched versions**, impact, and optional information…"

So the page is internally split: L571 says malware *alerts* have no fix version; L622 lists "patched
versions" as an optional field of an advisory record for "the vulnerability or malware". The entry
resolves the split silently in favour of L571, then hardens absence into impossibility:

- `…:31` "they carry no fix version (`S105.txt:571`)" — subject substitution: L571 says **alerts**, not advisories.
- `…:39` "malware advisories **deliberately** carry no fix version" — "deliberately" is not stated; L571 gives a reason ("no safe versions"), not an intent.
- `…:41` "A record whose class is malware **can never** support a "patched in X" statement." — a modal claim about all records, from a sentence about one display object, contradicted by L622's optional-field inventory.

Corrected wording: *"The malware section states that malware alerts do not contain a fix version, because
there are no safe versions (L571). The page's general field inventory (L622) nonetheless lists 'patched
versions' among fields an advisory 'may include' for 'the vulnerability or malware', so the absence is a
statement about the malware alert and not a proof about every malware record. Read a malware record as not
asserting a fix; verify the fix field per record."*

### (c) nine bullets at L574-582; community contributions is not a feed

`sed -n '574,582p' | wc -l` = **9** bullets: GitHub-reported advisories, NVD, npm Security advisories,
FriendsOfPHP, Go Vulncheck, Python Packaging Advisory, Ruby Advisory, RustSec Advisory, Community
contributions. That is **8 imported databases + 1 contribution channel**.

L582 itself is decisive: "Community contributions. For more information, see
https://github.com/github/advisory-database/pulls." L642 defines it: "A community contribution is a pull
request submitted to the github/advisory-database repository…". A PR channel is not an imported feed.

Also: the page's own word is **"sources"** (L573), and the list is open — L583: "If you know of another
database we should be importing advisories from, tell us about it…".

The entry's enumeration (`…:59-63`) is accurate as a list of sources; the **heading** (`…:57`, "Imported
feeds") and the manifest note ("the nine imported feeds") overcount feeds by one, and the parenthetical
"the database is an aggregator, not an author" borrows L640 ("we do not author this data") which is
scoped to **EPSS data only** — GitHub does author the review judgment (L584) and assigns the GHSA id (L611).

Corrected: *"### Sources (eight imported feeds plus a contribution channel) … the page lists nine sources
(L574-582); eight are imported databases and the ninth is a pull-request channel into
github/advisory-database (L582, L642). The list is open (L583). GitHub does not author EPSS data (L640);
it does author the review judgment (L584) and the GHSA id (L611)."*

### (d) supported registries: 12 is right; "outside ⇒ unreviewed" is not

Count: L586-597 = **12** (Composer, Erlang, Go, GitHub Actions, Maven, Npm, NuGet, Pip, Pub, RubyGems,
Rust, Swift). Swift's cell is `Swift (registry: N/A)` (L597) — correct.

But `…:68-69` reads "each named after its package registry except GitHub Actions and Swift, **whose
registry cell reads "Swift (registry: N/A)"**". GitHub Actions' cell is
`GitHub Actions (https://github.com/marketplace?type=actions)` (L589) — a marketplace URL, not N/A. The
relative clause attaches the N/A cell to both items; it is true for Swift only. The page's hedge
"**Generally**, we name our supported ecosystems after…" (L585) is also dropped.

`…:70-71` "An advisory for a package outside these registries is **not reviewed into the database**":
- L585 is "We review advisories **if** they are for a vulnerability in a package that comes from a supported registry" — ordinary English reads as *review is triggered by* registry membership (sufficient), not as a biconditional. The converse is not stated.
- Even on the necessary-condition reading, the licensed contrapositive is "not reviewed ⇒ not from a supported registry", not "outside registry ⇒ not reviewed".
- "not reviewed **into the database**" fuses review status with database membership. Unreviewed advisories *are* in the database (L601) and are by definition not reviewed; the page states no registry filter on the NVD path, so an out-of-registry package can appear as an unreviewed record.
- L598 invites new ecosystems, so the allow-list is open.

Corrected: *"The page states review for advisories 'for a vulnerability in a package that comes from a
supported registry' (L585) and that it names ecosystems after registries 'generally' (L585); it states no
converse. An out-of-registry advisory is therefore not shown to be reviewed — it may be present as an
unreviewed record (L601) — and the list is open (L598)."*

### (e) EPSS percentile tolerance — the entry is right, the percentage quote is not

L639: "GitHub keeps EPSS data up to date with a daily synchronization action. While EPSS score percentages
**will always be fully synchronized**, score percentiles will only be updated **when significantly
different**."

- `…:36` and `…:81` quote "when significantly different" — exact, and the page states **no tolerance value**.
- `…:102` "the page states no tolerance value" — **correct**, and the strongest Limits line in the entry.
- `…:80` quotes percentages as `"always fully synchronized"` — **MISQUOTE**: the source is "will always **be** fully synchronized". Substring test MISS (the only miss out of 18 checked). In a provenance table, an inexact quote is a verifiability defect.

Also worth stating: the daily action runs regardless; only the percentile *update* is conditional. The
entry's "refreshed only when significantly different" loses that the sync itself is daily.

### (f) CVSS provenance — the page makes the distinction the entry's rule 2 loses

L628: "**If GitHub obtains a CVE**, the GitHub Advisory Database uses the CVSS version assigned by the
maintainer, which can be version 3.1 or 4.0. **If the CVE is imported**, the GitHub Advisory Database
supports CVSS versions 4.0, 3.1 and 3.0."

The distinction "obtains a CVE" vs "imported CVE" is exactly as the table's *rule* cell has it
(`…:78`). Two defects around it:

- `…:35-36`: "A severity read from an **imported** CVE **is the maintainer's CVSS version**, not GitHub's" — this attaches the maintainer rule to the wrong branch. L628 assigns the maintainer's version to the *GitHub-obtained* case; for imports it says only which versions are *supported*. As written, rule 2 tells the reader the opposite of the table two lines below it.
- `…:78` author cell "NVD version for an import" — not stated. The page never says who assigns an imported CVE's version, nor which of 4.0/3.1/3.0 an import carries. "supports" ≠ "uses".

Corrected rule 2: *"A severity from a GitHub-obtained CVE carries the CVSS version the maintainer assigned
(3.1 or 4.0); for an imported CVE the page states only that versions 4.0, 3.1 and 3.0 are supported
(L628) — not which version an import carries or who assigns it."* Table author cell: *"maintainer
(GitHub-obtained CVE); unstated for an import (4.0/3.1/3.0 supported)"*.

### (g) community-contribution path and the "Analyst" credit — author inverted

L642: "…you can edit or add any detail, including additional affected ecosystems, the severity level, or
the description of who is impacted. The GitHub Security Lab curation team **will review the submitted
contributions and publish them** onto the GitHub Advisory Database if accepted."
L643: "…the **person who submitted** the community contribution pull request will automatically be
assigned a credit type of **"Analyst"**."
L640: "…this data is **not editable in community contributions**" (EPSS).

`…:82` reads `| community edits | GitHub Security Lab curation team | … with credit type "Analyst" |` —
that gives the team both authorship and the Analyst credit. The page gives authorship to the submitter,
review/publication to the team, and the credit to the submitter. Two material omissions in the same row:
the editable scope (any detail, incl. severity and affected ecosystems, L642) and the EPSS carve-out
(L640). The carve-out matters because the entry's own CVSS row claims severity is maintainer/NVD-authored
while L642 lets a contributor edit the severity level — the entry never reconciles that.

Corrected row: *"| community edits | the submitting contributor, credited "Analyst" | a PR to
`github/advisory-database`; the GitHub Security Lab curation team reviews and publishes it if accepted
(`S105.txt:642`); credit type "Analyst" (`S105.txt:643`); any detail is editable except EPSS data
(`S105.txt:640,642`) |"*.

## Every sentence that outruns the source

Severity: **P1** = must fix (wrong or contradicts source), **P2** = should fix (unsupported
generalization / misquote), **P3** = nit (attribution, range, convention).

| # | entry line | sentence (abbrev.) | source verdict | corrected wording |
|---|---|---|---|---|
| O1 | 17 | "Each advisory is one of three classes" | not stated; L569 "several varieties"; 3 headings only | attribute the 3-value count to S103:294 (F47); say "the page's three class sub-headings (L572, L600, L603)" |
| O2 | 18 | "the class decides whether the record was checked for validity at all" | stated only for 2 of 3: L584 reviewed, L602 unreviewed; malware section (L603-607) silent | "review status decides it: reviewed (L584) vs unreviewed (L602); the page says nothing about validity review of malware" |
| O3 | 31 | "they carry no fix version (L571)" | **wrong subject**: L571 says "Malware alerts" | "malware alerts do not contain a fix version (L571)" |
| O4 | 39 | "malware advisories deliberately carry no fix version" | "deliberately" unstated; L622 tension | drop "deliberately"; add the L622 caveat |
| O5 | 41 | "can never support a "patched in X" statement" | modal overreach; L622 lists patched versions as optional for malware records | "should not be read as a patched-in-X statement; verify the fix field per record" |
| O6 | 47 | "imported from the feeds below, then reviewed" | sequence unstated; NVD is both a reviewed source (L575) and the unreviewed feed (L601) | "listed as a source of reviewed advisories (L572-582); reviewed for validity/description/ecosystem data within supported registries (L584-585)" + note the NVD overlap |
| O7 | 47 | "yes, for a dependency on the package" | dropped precondition: L599 "**If you enable Dependabot alerts** for your repositories" | "yes, if Dependabot alerts are enabled, for a dependency on the package (L599)" |
| O8 | 57 | "Imported feeds (the database is an aggregator, not an author)" | 9 sources = 8 feeds + 1 PR channel (L582, L642); L640's "we do not author" is EPSS-only | see (c) correction |
| O9 | 68-69 | "except GitHub Actions and Swift, whose registry cell reads "Swift (registry: N/A)"" | **wrong for GitHub Actions**: L589 is a marketplace URL; "Generally" (L585) dropped | "GitHub Actions' cell is a marketplace URL (L589); only Swift reads "registry: N/A" (L597); naming is "generally" by registry (L585)" |
| O10 | 70-71 | "outside these registries is not reviewed into the database" | **unsupported**: L585 states no converse; unreviewed records are in the DB (L601); list open (L598) | see (d) correction |
| O11 | 35-36 | "A severity read from an imported CVE is the maintainer's CVSS version" | **wrong branch**: L628 gives the maintainer rule to GitHub-obtained CVEs | see (f) correction |
| O12 | 78 | "NVD version for an import" | not stated; page says versions "supported" (L628) | "unstated for an import (4.0/3.1/3.0 supported)" |
| O13 | 80 | `percentages "always fully synchronized"` | **misquote**: L639 "will always **be** fully synchronized" | quote exactly, or paraphrase without quotes |
| O14 | 82 | `community edits \| GitHub Security Lab curation team` | **wrong author**: L642 team reviews/publishes; L643 credits the submitter | see (g) correction |
| O15 | 82 | (omission) | L640 EPSS "not editable in community contributions"; L642 editable scope | add both to the row |
| O16 | 86-87 | "A count … never of "the database". F47's `type` filter selects the class" | not S105; it is F47/S103 (S103:294) | mark as F47-derived; F47's own form is "reviewed, non-malware", not "one class" |
| O17 | 88-89 | "A severity or EPSS number is a third-party value passed through GitHub" | conflates 3 fields: CVSS score (maintainer/import, L628), severity *label* (Section 5 bands, author unstated, L623), EPSS (FIRST, L640) | split the three; say the page does not state who maps a score to the four labels |
| O18 | 92 | "reviewed content, not wiki content" | "wiki" contrast has no source | drop "not wiki content" |
| O19 | 5 | "every class, source and field rule below is read from the captured page" | **false as written** (O1-O18) | "every quoted rule below is pinned to its anchor; the three-class count and the two F47-derived reading rules are this entry's reading, marked as such" |
| O20 | 3 | "CVSS provenance at 621-634"; "EPSS sync at 636-640"; "advisory classes at 568-608" | ranges over-broad: 629-634 is EPSS intro; sync is 639-640; 573-599 is the sources/ecosystem list | 621-628; 639-640; 568-572 + 600-607 |
| O21 | 4 | `verified-at: 2026-11-05` | host-local date is 2026-11-04 (capture 2026-11-05T00:14:43Z = 21:14 -03); F47 used the local date for a 22:17Z capture | `verified-at: 2026-11-04` or stamp the zone |

## What survives (do not over-correct)

- All 19 quotes at anchors; `recheck:` exit 0; snapshot sha256 unchanged by the run.
- Zero drift: live page re-derives to the pinned sha256 exactly.
- OSV format (L567), GHSA shape/charset/lowercase (L611-616), four Section 5 levels (L623-627),
  unreviewed = automatic NVD import + no alert (L601-602), malware alert enablement (L605), `type:malware`
  (L606), substitution-attack quotes and the "appropriately scoped" sentence (L607) — all verbatim-faithful.
- `…:102` (no EPSS tolerance) is correct and is the model for how the other Limits lines should read.
- `…:12` "the curation semantics F47 explicitly left unopened" is true: F47's entry says
  "**No database semantics.** … deferred to "About the GitHub Advisory database" (`S103.txt:276`), which
  was not opened."

## Impact and disposition

- **C2 counters: unaffected.** `rows/registry/entries/records/knowledge-expected/file-count` do not depend on
  any sentence above; the frozen after-values remain reproducible if the prose is corrected in place.
- **Axis impact: `depth:verifiability`.** The entry is a provenance artifact; a misquote (O13), a
  branch-inverted provenance rule (O11) and an inverted author cell (O14) are exactly what the axis measures.
  The counters cannot offset them. `coverage` is unaffected: F48 is admitted, registered in
  `corpus/README.md` and present in `knowledge-expected.txt`.
- **Blast radius:** the overreaches are confined to this entry plus two copies of its summary — the
  `corpus/README.md` F48 row ("the three advisory classes … the nine imported feeds") and the manifest
  `note`. No other `corpus/knowledge/*.md` cites them (`grep` over all 86 entries: 0 hits outside F48).
- **Pin consequence:** the entry's sha256 `d479c495…` is pinned in `pins-r70.txt`. Any correction moves that
  pin, so it cannot be applied silently inside this wave — L1 must either correct + re-pin in the landing
  commit or file the O1-O21 list as round-71 debt with the pins untouched.
- Smallest safe correction set: O3/O9/O11/O13/O14 (wrong/misquote) plus O5/O8/O10/O19 (the four
  generalizations that a reader would act on). O1/O2/O6/O7/O12/O15-O18/O20/O21 are wording/attribution.

## Scope notes

- S104 (rejected EUVD row) not opened: it is not this seat's artifact and no sentence in F48 depends on it.
- Read-only throughout: `git show`/`git archive` against the lane; the only lane write is this report.
  No git/jj mutation, no fixture repo, no subagent.
- Tooling: nothing installed (pacman guard not needed). Scratch `/fast/scratch/hyaku/kasegi-r70/CriticC2`
  removed before yield; every receipt above is pasted from it.
