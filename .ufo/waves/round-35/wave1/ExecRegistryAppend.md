# ExecRegistryAppend — kasegi-shokunin round 35 (S052 registry append)

Seat: ExecRegistryAppend-3, executor, axes depth:verifiability + coverage. Lane write scope:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Assigned file: `corpus/SOURCES.md` (append only: one
registry row, one `## Search log` bullet, three `## Registry changes` lines) plus this receipt.

Author of record: this seat. The round-35 `ScribeSOURCESRow` seat produced no draft (`.ufo/waves/round-35/
wave1/ScribeSOURCESRow.md` absent; the only reachable ScribeSOURCESRow instance was the round-34 one, which
refused to author round-35 bytes — correct, its ticket is frozen). I raised the gap to L1 KasegiR35 with the
measured pre-state and was authorised to author the three blocks from the shape fixed in my own ticket,
publishing their digests before the append.

## Pre-state (immutable input to this seat)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ sha256sum corpus/SOURCES.md
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md
$ wc -l corpus/SOURCES.md
105 corpus/SOURCES.md
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
51
$ grep -n '^## ' corpus/SOURCES.md
3:## Registry
59:## Paths
66:## Search log
79:## Leads (unopened)
85:## Registry changes
```

Anchors: last registry row `| S051 |` at :57 (end of the `## Registry` table); last `## Search log` bullet at
:77 (blank :78, `## Leads (unopened)` :79); last line :105 (the round-34 R8 tally bullet).

## Provenance facts from the capture seat (ExecC2Capture, message of 2026-10-26)

- `https://www.cisa.gov/known-exploited-vulnerabilities.json` -> **HTTP 404** (46916-byte HTML error page) under
  the instrument UA, a desktop Chrome UA and curl default; reproduced twice. Wrong path, not a missing artifact.
- Catalog page `https://www.cisa.gov/known-exploited-vulnerabilities-catalog` links three machine-readable
  files (CSV, JSON feed, JSON schema).
- Capture = the JSON feed `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`:
  requested URL == effective URL (no redirect), HTTP 200, content-type application/json, fetched
  2026-10-26T06:32:40Z, fetched_bytes 1807090, snapshot 1479694 bytes, 27870 lines, sha256 `d69349e8…77e8826`;
  `manifest.json` sha256 `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee` (5631 bytes).
- Its correction to my own wording, adopted: `severity` occurs twice in the capture (L5135, L11629) and
  `score` once (L23592) — all in prose or a URL slug, none as a field name, so the row says "no severity
  **field**", never "no severity token". `cvss` occurs zero times.

## Frozen blocks (v3, published before the append)

Whole-file digest of the frozen block set (the block set is the three fenced blocks below; the file it was
frozen in is `blocks.md` in this seat's scratch, deleted at yield): **blocks v3 sha256
`b087410ef54fda074030ca0635cd138fd208cd17b167d057e2126c58422e9e28`**, block digests
`ba69e0a05d7f437e684cc7714592cadb898bf35e874ddc4188ee17632bb3bc66` (row),
`f2ab0a647031489dd96f5e5fe35b20318ebae7ed9bd8cdcb6fbc51e8ff42ab54` (search-log bullet),
`70c3f0ef946fb01ea5e4329c03275216110aa0a2c98b79299ceffa4b6fa359ff` (R8 block).

Revision trail, both superseded revisions never applied (SOURCES.md was untouched while they existed):
v1 whole-file `8b61d27c0cd03e983d5a8a0a2a32b2a87fbd2da5d4266f5b57a4df576f02fa41` (row `58a42729…`, bullet
`9a228209…`, R8 `17007763…`) carried the 404 path in the `source` cell before the capture seat's measurement
arrived; v2 whole-file `c47f1a4dfee983359c1a377c529670537d74af03d3194af336060cbe485eb5b6` (row `05c4310a…`,
bullet and R8 identical to v3) had the effective URL but not the manifest quote pin, which RevRowS052's item
requires and S043's precedent carries. v3 changes only the row's `anchor` cell.

### 1. Registry row (one physical line)

```
| S052 | CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed) — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | dataset | A | CISA's own Known Exploited Vulnerabilities catalog statements as the captured feed states them: the catalog version and release, the per-record field set, and the remediation clock each record carries | capture corpus/source-snapshots/round-35/S052.txt (sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826, 1479694 bytes, 27870 lines): L2 title; L3 catalogVersion 2026.10.23; L4 dateReleased; L5 count 1756 with the L6 vulnerabilities array; first record L7-L22 carrying cveID L8, vendorProject L9, product L10, vulnerabilityName L11, dateAdded L12, shortDescription L13, requiredAction L14, dueDate L15, knownRansomwareCampaignUse L16, forensicTriage L17, notes L18, cwes L19-L21; exploitation-status span L15472-L15475 under record cveID L15465; remediation-clock span L19165-L19168 under record cveID L19161; no cvss field and no severity field on any record; manifest corpus/source-snapshots/round-35/manifest.json (sha256 06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee) pins quotes Q1-Q5 to L2, L3, L4, L15472 and L19165, each occurrences=1 | CISA's catalog states exploitation status per record, with a dateAdded to dueDate remediation clock and a knownRansomwareCampaignUse label, and carries no severity or CVSS score, so a KEV listing is a prioritization signal that a severity score cannot supply | mined | 2026-10-26 | 90d | corpus/knowledge/cisa-kev-catalog.md |
```

### 2. Search-log bullet (one physical line)

```
- CISA known-exploited-vulnerabilities sweep (round 35); question: does the lane hold a source that prioritizes by known in-the-wild exploitation rather than by severity, and does CISA's own catalog add ground that the lane's severity sources (S001, S002, S046, S047) and platform ladders (S043, S044, S049, S050, S051) do not; where: CISA's own catalog page at https://www.cisa.gov/known-exploited-vulnerabilities-catalog and the machine-readable files it links, with the JSON feed https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json captured under the instrument UA into corpus/source-snapshots/round-35/S052.txt (status 200, content-type application/json, requested URL == effective URL with no redirect, fetched 2026-10-26T06:32:40Z, fetched_bytes 1807090, snapshot 1479694 bytes, 27870 lines, sha256 d69349e8…77e8826) and read in full, plus an eight-term negative sweep (KEV, known exploited, known-exploited, CISA, exploited vulnerabilities, exploitation, BOD 22-01, BOD 26-04) over the lane's own corpus/knowledge/*.md (46 files at this writing), corpus/README.md, corpus/SOURCES.md and SKILL.md; date: 2026-10-26; identified 5 candidate surfaces, screened 5, included 1, excluded 4. Included: the KEV catalog JSON feed as S052. Excluded: the guessed path https://www.cisa.gov/known-exploited-vulnerabilities.json (HTTP 404, a 46916-byte HTML error page under the instrument UA, a desktop Chrome UA and curl default — reproduced twice, so that path is nobody's feed), the catalog page itself (an index of links, not a dataset, and not captured), the CSV sibling https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv (the same records in another serialization, no ground beyond S052) and the schema sibling https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json (field types only); the per-CVE NVD detail links inside each record's notes were not treated as surfaces at all, being per-vulnerability. PRE-STATE sweep: KEV 0, known exploited 0, known-exploited 0, BOD 22-01 0, BOD 26-04 0 files; CISA 2 knowledge files and 7 SOURCES rows, exploited vulnerabilities 1, exploitation 3 — the nearest existing ground is severity vocabulary, not exploitation status. Stop: CISA's own dataset is the authoritative statement of its own catalog, so no aggregator or vendor re-report was screened.
```

### 3. Registry-changes lines (three bullets, in order)

```
- S052 row added: new row (id `S052`, kind `dataset`, tier A scoped to CISA's own Known Exploited Vulnerabilities catalog statements, status mined, opened 2026-10-26, recheck `90d`, used-by `corpus/knowledge/cisa-kev-catalog.md`), anchor pinned to the round-35 capture `corpus/source-snapshots/round-35/S052.txt` (sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, 1479694 bytes, 27870 lines: L2 title, L3 catalogVersion 2026.10.23, L4 dateReleased, L5 count 1756, L6 vulnerabilities array, first record L7-L22 with cveID L8, dateAdded L12, requiredAction L14, dueDate L15, knownRansomwareCampaignUse L16, forensicTriage L17, cwes L19-L21; exploitation-status span L15472-L15475, remediation-clock span L19165-L19168). Live-capture admission, not a staged row: no staged S052 for this document exists in the campaign package, so no staged cell is carried and no staged id is remapped. The `source` cell carries the effective URL `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` — requested URL equals effective URL, no redirect — and not the guessed path `https://www.cisa.gov/known-exploited-vulnerabilities.json`, which returns HTTP 404 under three UAs.
- S052 cells not edited after append: the row is authored and applied in this one round-35 step, so there is no old → new cell transition on it; a later correction lands as its own appended statement under R8 rather than by rewriting this line.
- No status/recheck/used-by cell changed on any pre-existing row; S001–S051 untouched (logged). Registry 51 rows pre-append → 52 post-append (R8).
```

## Shape checks on the frozen row (before the append)

```
$ awk -F'|' '{print "NF="NF}' (row)      -> NF=13   (11 cells + 2 borders)
$ cells with a '|' or TAB inside         -> 0
$ id S052 / kind dataset / tier A / status mined / opened 2026-10-26 / recheck 90d   -> census enums satisfied
$ grep -c 'known-exploited-vulnerabilities' corpus/SOURCES.md  -> 0  (no duplicate URL; census E04 safe)
```

Anchor locators re-read from the capture at freeze time (all exit 0):

```
$ awk 'NR==2||NR==3||NR==4||NR==5||NR==6||NR==7||NR==21||NR==22' corpus/source-snapshots/round-35/S052.txt
2:"title": "CISA Catalog of Known Exploited Vulnerabilities",
3:"catalogVersion": "2026.10.23",
4:"dateReleased": "2026-10-23T19:30:18.9209Z",
5:"count": 1756,
6:"vulnerabilities": [
7:{
21:]
22:},
$ awk 'NR>=15465 && NR<=15475' …   # record Mitel MiVoice Connect: dueDate L15472, knownRansomwareCampaignUse L15473
$ awk 'NR>=19161 && NR<=19168' …   # record Citrix SD-WAN and NetScaler: dateAdded L19165, requiredAction L19167, dueDate L19168
$ python3 -c 'json.load(...)["count"]'  -> 1756 entries; 12 per-record keys, no severity/cvss key
$ grep -ci cvss corpus/source-snapshots/round-35/S052.txt  -> 0
$ grep -ci severity …  -> 2 (L5135, L11629: prose/URL slug, not a field)
```

Negative sweep (PRE-STATE, 46 knowledge files, this seat's own measurement):

```
$ for t in KEV "known exploited" "known-exploited" CISA "exploited vulnerabilities" "BOD 22-01" "BOD 26-04" exploitation; do … done
KEV                      knowledge=0 README=0 SOURCES=0 SKILL=0
known exploited          knowledge=0 README=0 SOURCES=0 SKILL=0
known-exploited          knowledge=0 README=0 SOURCES=0 SKILL=0
CISA                     knowledge=2 README=0 SOURCES=7 SKILL=0
exploited vulnerabilities knowledge=1 README=0 SOURCES=0 SKILL=0
BOD 22-01                knowledge=0 README=0 SOURCES=0 SKILL=0
BOD 26-04                knowledge=0 README=0 SOURCES=0 SKILL=0
exploitation             knowledge=3 README=0 SOURCES=3 SKILL=0
```

Dry-run apply on a copy in `/fast/scratch/hyaku/kasegi-r35/ExecRegistryAppend-3/` (never the lane file):
five insertions, zero deletions, `rows=52 malformed=0`, `grep -c '^| S052 |'` -> 1, file 105 -> 110 lines.

## Sibling search-log draft (surfaced, not applied)

`.ufo/waves/round-35/wave1/ScribeSearchLog.md` §5 (24,690-byte file, landed 03:38Z) is a second, later-authored
round-35 Search-log bullet. Its fenced block: 4,495 bytes, one line, sha256
`dc1a549a0cf23d77…` — **not** my landed bullet (2,394 bytes, `f2ab0a647031489d…`), so per the L1's rule I
applied mine (published first), did not apply theirs, and did not edit the landed line. `cmp` on the two
bullets: `differ: char 8, line 1`, exit 1.

Substantive deltas, mine (landed, :79) → theirs (unapplied):

| aspect | landed bullet | ScribeSearchLog §5 |
|---|---|---|
| sweep scope | `corpus/knowledge/*.md` (46), `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`; eight terms | every markdown file under `corpus/` + `SKILL.md` (105 files); nine terms, adds EPSS, exploit maturity, exploitation status, prioritiz, drops known-exploited |
| surfaces | 5 identified, 5 screened, 1 included, 4 excluded | 7 identified, 7 screened, 3 included, 4 excluded |
| catalog page | excluded as an index, not captured | captured: 284330 bytes, 3544 lines, sha256 `75a7af09…08aaa1`, prints "Showing 1 to 20 of 1756 results" |
| CSV sibling | excluded (same records, no ground beyond S052) | captured: 1073722 bytes, 1757 lines, sha256 `cb77ba6e…5d2778`, reconciled record-for-record (1756 cveIDs identical as a multiset, 12 columns = 12 record fields) |
| schema sibling | excluded (field types only) | captured: 3623 bytes, 102 lines, sha256 `0d5865c9…88b0e7` |
| directives | neither opened; `BOD 22-01` mentioned only as a string inside record cells | both opened: BOD 22-01 (87312 bytes) title "… (Revoked)", body "This Directive has been revoked. It is superseded by BOD 26-04."; BOD 26-04 (84350 bytes) supersedes it |
| KEV in the lane | "KEV 0 … files" inside the declared scope | "KEV 1 file/1 hit", located at `corpus/lessons/round-22.md:91` |

I re-measured the sibling's capture-side numbers against the landed capture; all hold: records whose
`requiredAction` names BOD 22-01 = 340, names BOD 26-04 = 139, distinct `dueDate` values = 513,
`dateAdded` range 2021-11-03…2026-10-23, `forensicTriage` Yes = 91, `knownRansomwareCampaignUse` Known = 361
(my earlier line-grep of 277 for "BOD 26-04" counts `notes` lines too, which is why record-level 139 is the
right number for a cell-level claim).

**Scope limitation of my own bullet, reported rather than repaired**: the PRE-STATE sweep it records does not
cover `corpus/lessons/*.md`, and that directory does carry the token — `corpus/lessons/round-22.md:91` quotes
the CWE Top 25 cell "CVEs in KEV: 7" under the S015 row. The bullet's `where:` clause names its surfaces, so
the "KEV 0" count is true of the surfaces it lists; a reader who takes it as a whole-corpus claim would be
wrong. The wider bullet closes that gap and adds three captured surfaces; the choice between them is the L1's,
and replacing a landed Search-log line is a correction, not an append, so I made none.

## Report

Seat: ExecRegistryAppend-3. Deliverable landed: `corpus/SOURCES.md` — the S052 registry row, the round-35
Search-log bullet and the three R8 lines, byte-identical to the frozen v3 blocks published above before the
file was touched. No other row, cell, section or file was modified by this seat.

### Post-append state (immediately after the append; the two L1-granted corrections below take the file to 112 lines)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ sha256sum corpus/SOURCES.md
510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829  corpus/SOURCES.md
$ wc -l corpus/SOURCES.md
110 corpus/SOURCES.md
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
52
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md
1
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/{n++; if (NF!=13) bad++} END{print "rows="n, "malformed="bad+0}' corpus/SOURCES.md
rows=52 malformed=0
$ grep -n '^## ' corpus/SOURCES.md
3:## Registry   60:## Paths   67:## Search log   81:## Leads (unopened)   87:## Registry changes
$ grep -n '^| S052 |' corpus/SOURCES.md            -> 58   (directly after | S051 | at :57)
$ grep -n 'CISA known-exploited-vulnerabilities sweep (round 35)' corpus/SOURCES.md -> 79
$ grep -n 'S052 row added' corpus/SOURCES.md       -> 108  (R8 lines :108-:110; last line :110 is the tally bullet)
$ diff -u <pre> corpus/SOURCES.md                  -> 5 insertions, 0 deletions
```

### Byte identity of the landed blocks

```
row     landed sha256 ba69e0a05d7f437e684cc7714592cadb898bf35e874ddc4188ee17632bb3bc66  == frozen block 1 digest
bullet  landed sha256 f2ab0a647031489dd96f5e5fe35b20318ebae7ed9bd8cdcb6fbc51e8ff42ab54  == frozen block 2 digest
R8      landed sha256 70c3f0ef946fb01ea5e4329c03275216110aa0a2c98b79299ceffa4b6fa359ff  == frozen block 3 digest
frozen block set sha256 b087410ef54fda074030ca0635cd138fd208cd17b167d057e2126c58422e9e28
```

The three blocks were extracted from this receipt's own fenced blocks, not retyped, and compared to the landed
lines with `==` on the full text (all True) — the landed line is the frozen byte string plus its newline.

### Census (the gate my ticket names)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
$ … sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
kasegi	rows	52
kasegi	tier.A	49   kasegi tier.B 1   kasegi tier.C 2
kasegi	status.mined	40   status.queued 9   status.rejected 3
FLEET	rows	52   FLEET.tier.invalid 0   FLEET.status.invalid 0   missing 0
exit=0
```

Only the two pre-existing W04 warnings (S028/S029); no E-code, and E11 on S052 is clear because
`corpus/knowledge/cisa-kev-catalog.md` (88 lines at the final read, sha256
`da81204b3fbca378aa311406fd3a46394759967ecc3445297335a7526c573acf`, mtime 03:39:03Z — it grew by one line
after my pre-append read of 87) exists and cites `source: S052` — 1 match.

### Manifest binding re-checked after the append

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
exit=0
```

### L1-granted correction appends (after the initial landing)

The L1 granted both corrections I raised, as append-only statements (the landed rows and bullet stay
byte-intact; nothing was rewritten). Appended at EOF, after the :110 tally bullet:

```
:111  792 bytes  sha256 396d5ebac2956524b119c0b3c3e8ff21f2ef560feb455b1113095f2b720f5925
      - Round-35 Search-log bullet superseded: … `.ufo/waves/round-35/wave1/ScribeSearchLog.md` §5
        (4495 bytes, sha256 `dc1a549a0cf23d77099f6242420042841d6e89ec032c002e172c1d9f632f4d49`) …
        the landed bullet stays byte-intact and this line is the record of the supersession, not a rewrite (R8).
:112  516 bytes  sha256 8be3b5c2a49d7a1e1fb68fdd15c77cf9a043b05ee732c9a7d8a7ee54a127e0d2
      - Round-35 Search-log bullet scope correction: … scoped to `corpus/knowledge/*.md` (46 files),
        `corpus/README.md`, `corpus/SOURCES.md` and `SKILL.md` only; that scope excludes `corpus/lessons/`,
        and the KEV token pre-existed there at `corpus/lessons/round-22.md:91` … (R8).
```

Both lines carry zero pipes and zero tabs, so neither can trip census E12 or the NF=13 row rule.

### Final state after the two correction appends

```
$ wc -l corpus/SOURCES.md
112 corpus/SOURCES.md
$ sha256sum corpus/SOURCES.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
52
$ awk -F'|' … '{n++; if (NF!=13) bad++}' corpus/SOURCES.md
rows=52 malformed=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

### Risks and blockers

- The sibling bullet was a live disagreement about the record of this sweep; the L1 granted the append-only
  supersession line at :111, so the landed bullet (:79) stays byte-intact and the wider `ScribeSearchLog.md`
  §5 bullet is now the recorded record of the sweep rather than the operative text.
- The PRE-STATE scope gap is closed in the file: :112 states the "KEV 0" counts cover only
  `corpus/knowledge/*.md` (46), `corpus/README.md`, `corpus/SOURCES.md` and `SKILL.md`, and names the
  pre-existing token at `corpus/lessons/round-22.md:91` (CWE Top 25 cell "CVEs in KEV: 7" under S015).
- The row's `teaches` cell and the entry both rest on the capture only. The sibling's revoked-BOD-22-01 finding
  comes from two directive pages this seat never opened and is deliberately absent from the row and from my
  bullet; it appears in the file only inside the supersession line, attributed to the §5 draft's measurements.
- Nothing else blocks: capture, manifest, entry and registry row are all on disk and every counting command in
  this seat's assignment exits 0. No installs were made (no tool changes to record).
- Scratch `/fast/scratch/hyaku/kasegi-r35/ExecRegistryAppend-3/` deleted before yield (verified absent); the
  frozen block set and the pre/post copies are not left on disk — this receipt is the record.
