# ConnCrossCheck — round-35 wave-1 receipt

Seat: ConnCrossCheck (connector, leaf). Scope: cross-check the S052 source
chain end to end and the round-35 manifest records ↔ files ↔ registry rows;
confirm census W04 pair unchanged with no new warnings.

Lane base 3266c9937b03062d9bbc2f436e20820115ed179c; claims freeze
617496b9c6e92bc671e7e78b83df69a04470d0e9. All commands run from the lane
root `/home/vgpnk/Projects/shokunin/kasegi-shokunin` against the working copy
(jj `@` qwsxkpzx, parent lprkqvpk). No scratch directory was created (no
work trees or fixtures needed); nothing to clean up.

## Report

### S052 chain — six links, all agree (ids, URL, sha256)

**1. Registry row** — `corpus/SOURCES.md` line 58 (single S052 row,
`s052_rows=1`, `registry_rows=52`):

`| S052 | CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed) — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | dataset | A | ... | capture corpus/source-snapshots/round-35/S052.txt (sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826, 1479694 bytes, 27870 lines): ... | ... | mined | 2026-10-26 | 90d | corpus/knowledge/cisa-kev-catalog.md |`

Status cells verified by exact grep: `mined | 2026-10-26 | 90d |
corpus/knowledge/cisa-kev-catalog.md`.

**2. Capture file** — `corpus/source-snapshots/round-35/S052.txt`:

```
$ sha256sum corpus/source-snapshots/round-35/S052.txt
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826
$ wc -lc corpus/source-snapshots/round-35/S052.txt
27870 1479694
```

Matches registry row and manifest digest, byte and line counts.

**3. Manifest record** — `corpus/source-snapshots/round-35/manifest.json`
(sha256 06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee):
one record, `id: S052`, `path: S052.txt`,
`url: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
(byte-identical to the registry row and entry header URLs),
`fetched_utc: 2026-10-26T06:32:40Z`, `sha256: d69349e8...9e8826` — matches
the file on disk. Quotes Q1–Q5 at anchors 2, 3, 4, 15472, 19165.

**4. Entry header** — `corpus/knowledge/cisa-kev-catalog.md` line 3 (sole
entry citing S052, `grep -lE '^source: S052 ' corpus/knowledge/*.md` →
exactly this file):

`source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture corpus/source-snapshots/round-35/S052.txt (27,870 lines; sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826): ...`

`ground: F18`, `verified-at: 2026-10-26`, recheck line pins the same manifest
and names the same five anchors.

**5. Harness** — `python3 corpus/instruments/frontier-recheck-count.py`:

```
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
EXIT=0
```

(17 frontier rows now count 18 by the claims' counting command:
`grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 18, F18 appended at
`corpus/README.md` line 388 as a round-35 amendment table, history preserved
per R9 at lines 370–396.)

**6. Source-recheck assertions** —
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052`:

```
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
recheck_exit=0
```

Direct anchor spot-checks against the capture agree: L2 title, L3
catalogVersion 2026.10.23, L4–L5 dateReleased/count 1756, L15465 cveID
CVE-2022-29499 with L15472–L15475 dueDate/knownRansomwareCampaignUse Known/
forensicTriage No/notes, L19161 cveID CVE-2019-12989 with L19165–L19168
dateAdded 2022-03-25/shortDescription/requiredAction/dueDate 2022-04-15.

Independent run of the entry's own falsifiable checks FC-1–FC-11 reproduces
every printed expected value (keys 5 count 1756 records 1756; ids 1756 of
1756; keysets 1 keys 12; Unknown 1395/Known 361, Yes 91/No 1665; forward 1756
of 1756 [(21,1025),(14,280),(181,238)]; bod22 340 bod26 139 both 0 neither
1277; distinct 46 top 893; cvss=0 base score=0 risk rating=0 reward=0
bounty=0 severity+score=3; FCEB=2; BOD22=327; UserResource$UriData at 11954).

**Verdict: no dangling link in the S052 chain.**

### Round-35 manifest ↔ files ↔ registry rows

The round-35 manifest lists exactly one record (S052). Record path resolves
to an existing file whose sha256 equals the record; the registry row S052
names the same capture path and digest; the entry header names the same
capture, digest, and URL. No manifest record points at a missing file; no
registry row references a nonexistent round-35 capture. **No dangling link.**

### Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

The W04 pair is exactly S028/S029 — unchanged from the claims' before state;
no new warnings (no codes other than the two standing W04s plus `ok`).

### Observation (transient mid-wave state, not a defect)

At the start of this seat's run the tree was still integrating: the first
harness run printed `entries=20 pass=20 exit=0` with no F18 line and README
had 17 frontier rows. By the final verification pass the appended round-35
amendment (README lines 370–396, F18 row at line 388) was present and the
harness printed `entries=21 pass=21 exit=0` including `PASS F18 ids=S052`.
All receipt figures above are from the converged final state. Seats reading
README/harness mid-wave should re-run before quoting counts.

### Junk F18 twin (control, out of chain)

`.ufo/waves/round-35/c2-controls/junk-f18.md` is not an admitted README row,
so the harness never binds it; its `source:` line cites a fabricated URL
different from the feed URL, and it declares no manifest record. It stays out
of the chain; rejection is the admission gate's job, not this cross-check's.

### File digests (sha256, converged state)

```
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74  corpus/knowledge/cisa-kev-catalog.md
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  .ufo/waves/round-35/claims.json
```

No tools installed or upgraded this seat. No writes outside the lane wave
receipt directory.
