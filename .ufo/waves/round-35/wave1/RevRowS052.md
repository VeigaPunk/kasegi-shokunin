# RevRowS052 — round-35 review of the S052 registry row, Search-log bullet and R8 lines

Seat: RevRowS052 (reviewer, L2 leaf, kasegi-shokunin round 35, hyaku run 8). Item: review the landed
S052 registry row in `corpus/SOURCES.md` (11 columns/NF=13; no `|` inside cells; tier A scoped to
CISA's own KEV catalog statements; anchor pinned to the round-35 capture with line locators; quote
≤25 words located in the capture; `opened 2026-10-26`; `recheck 90d`; `used-by` exactly the F18
entry; kind dataset; status mined) and confirm the round-35 `## Search log` bullet and
`## Registry changes` R8 lines are present and truthful.

## Verdict: **matches**

Every criterion holds on the landed bytes (`corpus/SOURCES.md` sha256 `510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829`,
110 lines / 64 172 B). Three prose-only observations for the L1 (§7), none a corpus defect.

## Report

### 0. Timing (why the review ran late)

At first check (06:36:38Z) `corpus/SOURCES.md` was still the round-34 tree (105 lines,
`S052_rows=0`): the S052 append had not landed. I ran all capture-side, manifest-side and
draft-truthfulness checks **before** the landing, messaged `ExecRegistryAppend-3` (who confirmed
ownership, answered my manifest-pin question by re-freezing the row as v3 with an S043-style
manifest pin, and reported the append blocked only on the F18 entry landing), and received the
landing ping. Row checks below were run **after** the landing, on the landed bytes (first measured
110 lines at 06:38:22Z).

### 1. The landed row — `corpus/SOURCES.md:58` (verbatim, one physical line)

```
| S052 | CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed) — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | dataset | A | CISA's own Known Exploited Vulnerabilities catalog statements as the captured feed states them: the catalog version and release, the per-record field set, and the remediation clock each record carries | capture corpus/source-snapshots/round-35/S052.txt (sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826, 1479694 bytes, 27870 lines): L2 title; L3 catalogVersion 2026.10.23; L4 dateReleased; L5 count 1756 with the L6 vulnerabilities array; first record L7-L22 carrying cveID L8, vendorProject L9, product L10, vulnerabilityName L11, dateAdded L12, shortDescription L13, requiredAction L14, dueDate L15, knownRansomwareCampaignUse L16, forensicTriage L17, notes L18, cwes L19-L21; exploitation-status span L15472-L15475 under record cveID L15465; remediation-clock span L19165-L19168 under record cveID L19161; no cvss field and no severity field on any record; manifest corpus/source-snapshots/round-35/manifest.json (sha256 06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee) pins quotes Q1-Q5 to L2, L3, L4, L15472 and L19165, each occurrences=1 | CISA's catalog states exploitation status per record, with a dateAdded to dueDate remediation clock and a knownRansomwareCampaignUse label, and carries no severity or CVSS score, so a KEV listing is a prioritization signal that a severity score cannot supply | mined | 2026-10-26 | 90d | corpus/knowledge/cisa-kev-catalog.md |
```

Line digest `ba69e0a05d7f437e684cc7714592cadb898bf35e874ddc4188ee17632bb3bc66` (1 595 chars /
1 597 B) — byte-identical to the v3 row block published in `wave1/ExecRegistryAppend.md` **before**
the append (the executor's published digest; I re-extracted the block and hashed it myself). The
superseded v1 (404 path in the source cell) and v2 (no manifest pin) were never applied.

Per-criterion verdicts:

| criterion | landed evidence | verdict |
|---|---|---|
| 11 columns / NF=13 | `sed -n '58p' \| awk -F'\|'` → `NF=13`; header row `:5` also `NF=13` (id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by); all 11 cells non-empty | **matches** |
| no `\|` inside cells | NF=13 ⟺ 12 boundary pipes; whole-file `grep -cF '\|' corpus/SOURCES.md` → `0` | **matches** |
| tier A scoped to CISA's own KEV catalog statements | cell04 `A`; cell05 opens "CISA's own Known Exploited Vulnerabilities catalog statements as the captured feed states them" and bounds the row to the captured feed's own statements (version/release, per-record field set, remediation clock) — Q4 attribution kept, no generalization | **matches** |
| anchor pinned to the round-35 capture with line locators | cell06 pins `corpus/source-snapshots/round-35/S052.txt` with sha256, byte count and 27 870-line count, then L2/L3/L4/L5/L6, the L7-L22 field map, the L15472-L15475 and L19165-L19168 spans, and the manifest pin — every locator re-opened against the capture (§2) | **matches** |
| quote ≤25 words located in the capture | the row files no verbatim quote (lane row shape — S049/S050/S051 rows carry none either); the round's S052 quotes of record are manifest Q1–Q5: word counts **7 / 2 / 4 / 8 / 19** (max 19 ≤ 25), each located in the capture at its anchor — `source-recheck.py` prints Q1 `anchor=2-ok`, Q2 `3-ok`, Q3 `4-ok`, Q4 `15472-ok`, Q5 `19165-ok`, all `occurrences=1` (§3) | **matches** |
| `opened 2026-10-26` | cell09 | **matches** |
| `recheck 90d` | cell10 (cadence form, same as S006/S007/S043/S044/S045/S047/S049/S051) | **matches** |
| `used-by` exactly the F18 entry | cell11 is the single path `corpus/knowledge/cisa-kev-catalog.md`; the entry exists (88 lines, sha256 `da81204b…73acf`) and its `:3` reads `source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture …`; `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` → `1` | **matches** |
| kind dataset | cell03 `dataset` (second dataset row beside S015; census E05 passes) | **matches** |
| status mined | cell08 `mined` | **matches** |

Row position: `:56` S050, `:57` S051, `:58` S052, `:59` blank, `:60` `## Paths` — last row of the
`## Registry` table, exactly the executor's apply point.

### 2. Anchor locators re-opened against the capture

Capture `corpus/source-snapshots/round-35/S052.txt`, 27 870 lines / 1 479 694 B, sha256
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` (matches the manifest record and
the row's anchor cell). Independently live-verified by `wave1/ScoutKEVLive.md` (re-fetch at
06:36:23Z, `diff` → 0 differing lines, same sha256); I did not re-fetch (the scout's measurement is
on file and the capture digest pins the bytes I checked against).

Locator map verified line-by-line (`sed -n '1,6p'`, `'7,22p'`, `'15461,15476p'`, `'19158,19170p'`):

- L2 `"title": "CISA Catalog of Known Exploited Vulnerabilities",` ✓; L3 `"catalogVersion": "2026.10.23",` ✓; L4 `"dateReleased": "2026-10-23T19:30:18.9209Z",` ✓; L5 `"count": 1756,` ✓; L6 `"vulnerabilities": [` ✓
- First record L7-L22: `{` L7, `cveID` L8 (CVE-2026-114625), `vendorProject` L9 (Arista), `product` L10 (VeloCloud Orchestrator), `vulnerabilityName` L11, `dateAdded` L12 (2026-10-23), `shortDescription` L13, `requiredAction` L14, `dueDate` L15 (2026-10-26), `knownRansomwareCampaignUse` L16 (Unknown), `forensicTriage` L17 (Yes), `notes` L18, `cwes` L19-L21 (`CWE-89`) ✓ — every field-name/line pair in the anchor cell matches
- Exploitation-status span L15472-L15475 under record cveID L15465 (CVE-2022-29499, Mitel MiVoice Connect): `"dueDate": "2022-07-18",` L15472, `"knownRansomwareCampaignUse": "Known",` L15473, `"forensicTriage": "No",` L15474, `"notes": "https:\/\/nvd.nist.gov\/vuln\/detail\/CVE-2022-29499",` L15475 ✓
- Remediation-clock span L19165-L19168 under record cveID L19161 (CVE-2019-12989, Citrix SD-WAN and NetScaler): `"dateAdded": "2022-03-25",` L19165, shortDescription L19166, `"requiredAction": "Apply updates per vendor instructions.",` L19167, `"dueDate": "2022-04-15",` L19168 ✓

Field-set negatives, measured on the parsed JSON (not token greps — the executor's wording
correction, adopted): `count` 1756 = `len(vulnerabilities)` 1756; the per-record key set is exactly
12 keys (`cveID, vendorProject, product, vulnerabilityName, dateAdded, shortDescription,
requiredAction, dueDate, knownRansomwareCampaignUse, forensicTriage, notes, cwes`), one distinct key
set across all 1 756 records, and **no severity/cvss key**; token scan `grep -ic cvss` → 0 lines,
`severity` exactly 2 lines (L5135, L11629 — both URL slugs inside `notes` strings). The anchor
cell's "no cvss field and no severity field on any record" is the field-set claim and holds.

### 3. Manifest and recheck (the row's captured-source binding)

`corpus/source-snapshots/round-35/manifest.json` sha256
`06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee` (5 631 B) — the digest the row's
anchor cell pins. Record: id `S052`, path `S052.txt`, sha256 = the capture's sha256, `url`
byte-equal to the row's source-cell URL token, `fetched_utc 2026-10-26T06:32:40Z` (strict UTC, no
offset — R20/R21 conformant). The `purpose` field declares the `--kind text` choice (the body is
application/json; the default html mode would rewrite `\/` entity sequences), the 404 measurement
on the dispatched URL, the CSV-sibling comparison (200, 1 073 722 B, 1 757 lines, 12 header fields
over the same 1 756 records), and the measured negative (cvss 0, base score 0, risk rating 0;
`severity` twice in prose).

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
recheck_exit=0
```

My own independent check (not the instrument): every quote ≤25 words (7/2/4/8/19), every quote
exactly-once under the declared normalization, Q3/Q4/Q5 spanning 2-4 source lines carry verified
anchors (L4, L15472, L19165). 5/5. The entry's two longer quotes (FCEB sentence ×2, BOD 22-01
sentence ×327) are deliberately outside the manifest and anchored in the entry instead — I verified
both counts: `grep -c` → `2` and `327` (entry FC-9/FC-10).

```
$ python3 corpus/instruments/capture-binding-check.py   (tail)
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=42 with_url=42 with_fetched_utc=4 with_archival=38 snapshot_dirs=11 manifest_dirs=11 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=42 bound=42 unbound=0
binding_exit=0
```

`orphans=1 orphan=S040-live.txt` is the known round-33 R6 item (ExecS040Orphan's lane, not mine).

### 4. Search-log bullet — `corpus/SOURCES.md:79` — present and truthful

Present: one bullet appended as the last `## Search log` bullet (`:77` round-33 CNVD/360SRC bullet,
`:78` round-34 Immunefi bullet, `:79` the round-35 CISA bullet, `:80` blank, `:81` `## Leads`),
byte-identical to the frozen block (`cmp` against the receipt's fenced block → identical; digest
`f2ab0a647031489dd96f5e5fe35b20318ebae7ed9bd8cdcb6fbc51e8ff42ab54`). PRISMA fields all present
(question / where / date 2026-10-26 / identified 5, screened 5, included 1, excluded 4 / stop
rationale). Truthfulness, each load-bearing claim re-verified by me:

- **identified 5 / screened 5 / included 1 / excluded 4**: the five surfaces the bullet names are
  the guessed path, the catalog page, the JSON feed, the CSV sibling and the schema sibling;
  1+4=5 ✓. The snapshot dir holds exactly `S052.txt` + `manifest.json` — the catalog page was
  indeed not captured ✓.
- **"the guessed path … (HTTP 404, a 46916-byte HTML error page under the instrument UA, a desktop
  Chrome UA and curl default — reproduced twice)"**: my own measurement, three UAs in one pass →
  `404 46916` bytes every time (kasegi-shokunin/1.0, desktop Chrome UA, curl default). "Reproduced
  twice" + the first measurement = the manifest's "three measurements" — consistent ✓.
- **"the catalog page itself (an index of links, not a dataset, and not captured)"**: my own fetch
  (200, 284 330 B) — it links each of the three machine-readable files exactly once and carries a
  recent-entries teaser (21 distinct CVE ids in teaser cards, 100 occurrences), no full dataset
  inline. Characterization fair for the exclusion reason; see §7 observation 1.
- **"the CSV sibling … (the same records in another serialization, no ground beyond S052)"**: my
  own fetch (200, **1 073 722 B** — byte-count equal to the manifest's figure), header = the same
  12 field names as the JSON's per-record key set, **1 756** data rows ✓.
- **"the schema sibling … (field types only)"**: my own fetch (200, 3 623 B, application/json,
  `$schema`/`type`/`properties` describing the four top-level fields) ✓.
- **PRE-STATE sweep** ("KEV 0, known exploited 0, known-exploited 0, BOD 22-01 0, BOD 26-04 0
  files; CISA 2 knowledge files and 7 SOURCES rows, exploited vulnerabilities 1, exploitation 3"):
  I re-ran the same eight-term sweep POST-STATE and accounted every delta — knowledge: KEV 0→1,
  known exploited 0→1, known-exploited 0→1, CISA 2→3, exploited vulnerabilities 1→2, BOD 22-01
  0→1, BOD 26-04 0→1, exploitation 3→4 (each +1 = the new F18 entry); SOURCES: CISA 7→9,
  exploitation 3→6, KEV 0→2, known-exploited 0→2, exploited vulnerabilities 0→1, BOD 22-01 0→1,
  BOD 26-04 0→1 (every delta is one of this round's five inserted lines). Post-state = claimed
  PRE-STATE + exactly this round's bytes, so the PRE-STATE numbers are corroborated ✓. Knowledge
  dir "46 files at this writing" → 47 now (the new entry) ✓.
- **capture stats in the bullet** (status 200, content-type application/json, requested URL ==
  effective URL no redirect, fetched 2026-10-26T06:32:40Z, fetched_bytes 1 807 090, snapshot
  1 479 694 B, 27 870 lines, sha256 `d69349e8…77e8826`): all match the manifest record and the
  scout's independent live re-fetch ✓.
- **"the per-CVE NVD detail links inside each record's notes were not treated as surfaces at all"**:
  consistent with the snapshot dir contents (no per-CVE captures) ✓.
- **Stop rationale**: a method statement consistent with the manifest's measured negative ("the
  catalog's prioritization input is therefore exploitation status … not a CVSS score") ✓.

### 5. Registry-changes R8 lines — `corpus/SOURCES.md:108-110` — present and truthful

Present: three bullets appended at file end (`:105`-`:107` are the round-34 S051 lines; `:108`-`:110`
the round-35 lines), byte-identical to the frozen block (digest
`70c3f0ef946fb01ea5e4329c03275216110aa0a2c98b79299ceffa4b6fa359ff`). Truthfulness:

- **":108 S052 row added…"** — every cell it names matches the landed row (id/kind/tier/scope
  summary/status/opened/recheck/used-by; anchor digest + the same locator list I verified in §2) ✓.
  "Live-capture admission, not a staged row: no staged S052 for this document exists in the
  campaign package" — my own read-only grep over `/home/vgpnk/Projects/shokuknow/merge/kasegi/`:
  the package's staged `S052` (`SOURCES.append.md:28`) is the CNNVD weekly advisory
  (cnnvd.org.cn PDF), a different document, so no staged cell is carried and no staged id is
  remapped by this append ✓. "returns HTTP 404 under three UAs" — my own 3-UA measurement ✓.
- **":109 S052 cells not edited after append…"** — `git diff HEAD --numstat -- corpus/SOURCES.md`
  → `5 0` (five insertions, zero deletions); the landed row digest equals the v3 digest the
  executor published before touching the file; single-step author+apply ✓.
- **":110 No status/recheck/used-by cell changed on any pre-existing row; S001–S051 untouched
  (logged). Registry 51 rows pre-append → 52 post-append (R8)."** — numstat `5 0` proves zero
  pre-existing lines touched at all (stronger than the claim); counts 51→52 measured on both sides
  (`git show HEAD:corpus/SOURCES.md` → 51 rows / 105 lines / sha `4c85ff86…77b6`; landed → 52 rows
  / 110 lines / sha `510e3bba…8829`) ✓. "(R8)" is the QUALITY record-R8 logging criterion
  (`corpus/QUALITY.md:50`).

### 6. Landed-tree cross-checks (claims C2 counters, read-only)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        → 52
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md              → 1
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l                     → 1
$ ls corpus/knowledge/*.md | wc -l                                           → 47
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0        (W04 S028/S029 only, as the claim states; no new W, no E line)
```

Outside my item, recorded as observed state for the L1: README frontier rows still `17` and the
harness still `entries=20 pass=20 exit=0` at 06:38Z — the F18 README admission and expected-list
sync are other seats' lanes and had not landed at my check time.

### 7. Findings for the L1 (none a corpus defect)

1. **Catalog-page characterization, prose nuance.** The bullet excludes the catalog page as "an
   index of links, not a dataset, and not captured". Both the exclusion reason and "not captured"
   hold (my own fetch: it links the three machine-readable files; the snapshot dir has no catalog
   page), but the live page also carries a recent-entries teaser — 21 distinct CVE ids in teaser
   cards (100 occurrences), e.g. `CVE-2026-110447` linking to cve.org. "An index of links" is
   therefore slightly incomplete: index of links **plus a recent-entries preview**. This does not
   change the exclusion rationale (the dataset ground is the feed; the page is not the dataset and
   was not captured), so I record it as prose-only.
2. **The landed S052 id takes the id the campaign package staged for a different document.** The
   shokuknow package's staged `S052` is the CNNVD weekly advisory (`SOURCES.append.md:28`,
   cnnvd.org.cn PDF); the landed S052 is the CISA KEV feed. The assimilation lane has already
   accounted for the collision: `renumber-map-post-c2.txt:22` moves staged `S052 -> S074` (pre-C2
   map `:1/:22` shows the staged numbering). The R8 line's "no staged id is remapped" is true for
   this append (the remap lives in the assimilation lane's plan, not in any registry edit) —
   flagged so the L1 sees the collision is handled, not overlooked.
3. **Residual C2 after-state counters outside my row scope:** README F18 admission (frontier
   17→18) and the harness 20→21 had not landed at my check time (§6). The row, entry, bullet and
   R8 side of C2 is landed and verified; the README/harness counters should be re-checked when
   those seats land.

### 8. File digests (measured this seat)

```
510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829  corpus/SOURCES.md                 (110 lines / 64172 B; pre-append committed 4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6, 105 lines / 51 rows)
ba69e0a05d7f437e684cc7714592cadb898bf35e874ddc4188ee17632bb3bc66  corpus/SOURCES.md:58 (the landed S052 row line, with trailing NL)
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt   (27870 lines / 1479694 B)
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json (5631 B)
da81204b3fbca378aa311406fd3a46394759967ecc3445297335a7526c573acf  corpus/knowledge/cisa-kev-catalog.md  (88 lines)
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md  (368 lines, unchanged by this append)
7c1d72990683166aa54401bb63122e25f4fbf14c0e9a9bd980d09ce34b212638  .ufo/waves/round-35/wave1/ExecRegistryAppend.md  (executor receipt; frozen blocks read from it)
a8bdf83ac69b03c8b3551dfe314b1da33da05a8f7cb04aaab20fdf525281002c  .ufo/waves/round-35/wave1/ScoutKEVLive.md  (scout live re-verify receipt)
```

### 9. Tooling and scratch

- No tool installed or upgraded (no `pacman`, `uv`, `npx`, or binary fetch); only lane instruments,
  `curl`, `python3`, coreutils.
- Scratch `/fast/scratch/hyaku/kasegi-r35/RevRowS052/` (landed-row.txt, catpage.html, kev.csv,
  schema.json) — deleted before yielding; receipt first copied into the wave dir. Scratch-left-on-
  disk: **none**.
- Write scope respected: only this receipt under `.ufo/waves/round-35/wave1/`; no jj/git mutations;
  shokuknow and the fleet root read-only (read-only greps over `shokuknow/merge/kasegi/` and the
  lane's own assimilation scratch).
