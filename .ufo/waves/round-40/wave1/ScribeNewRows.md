# ScribeNewRows — round-40 wave 1 receipt

Seat: ScribeNewRows (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `a7af2ce63bce153757d39bf66b366a96caf30c13`; claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`.
No lane file outside this seat's write scope was written; no tool was installed or upgraded (nothing needed).

## Deliverable

- `.ufo/waves/round-40/wave1/ScribeNewRows.txt` — the three new registry rows S060/S061/S062, full 11-column
  cells, one physical line per row, final newline, no tabs/CR, no `|` inside any cell.
  **lines=3, bytes=5149, sha256=8435ec2869cf1b81b4d20b47a186a8ce43a7306f389d00a4d043daf6bfcb969c**
- Landable as-is: insert immediately after the last registry row (`| S059 | …`, `corpus/SOURCES.md:65`), before
  the blank line and `## Paths` (`:67`), i.e. still inside `## Registry` (E12 would fire otherwise).

## Rows

| id | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|
| S060 | spec | A | mined | 2026-10-26 | on-release | corpus/knowledge/cyclonedx-analysis-subtree.md |
| S061 | docs | A | rejected | 2026-10-26 | 365d | — |
| S062 | spec | B | rejected | 2026-10-26 | 30d | — |

Ids are the next unused after S059 (`grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' corpus/SOURCES.md` → 59
before; `grep -nE '^\|[[:space:]]*S06[0-9]' corpus/SOURCES.md` → no hits before).

### S060 — CycloneDX v1.7 JSON Reference, vulnerabilities analysis subtree (F23) — mined

- Capture: `corpus/source-snapshots/round-40/S060.txt` (scout deliverable `wave1/ScoutF23Lead.capture.txt`,
  4889 bytes, 111 lines, sha256 `d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779`,
  fetched 2026-10-26T21:16:18Z, HTTP 200, raw 6419901 bytes) — manifest record `wave1/ScoutF23Lead.manifest-record.json`
  already carries `id=S060`, `path=S060.txt`, `url=https://cyclonedx.org/docs/1.7/json/`, same sha256, so the row,
  the capture and the manifest record agree on one id and one digest.
- Locators re-checked in the delivered capture: L1 title/version, L7 `analysis.state` description, L15
  `"not_affected"… Justification should be specified…`, L50 `analysis.lastUpdated`.
- `teaches` begins `supersedes S059 —` (R8 supersede form; the r39 S059 row pinned the same page without a capture).
- Reproducibility limit is recorded in the anchor cell, not hidden: raw page sha256 is **not** stable across
  fetches (Cloudflare `data-cfemail` tokens; scout measured `4d9c10da…` then `9a551897…`), while the normalized
  full-page text `ffe8c0b6…f5ba7f4` was byte-identical on both fetches and the committed 111-line slice hashes
  `d6862622…`, so the slice (not the raw bytes) is the unit `source-recheck` measures.
- `scope` cell is byte-identical to S059's (`sha256` of the trimmed scope cell: `a5367f38…dad94a` for both) —
  deliberately, see the W04 control below.

### S061 — CISA VEX Status Justifications (June 2022) — rejected

- Provenance is the scout ledger (`wave1/ScoutS060Leads.txt`, fetched 2026-10-26T21:16:01–21:16:25Z), no lane
  capture: lead URL `…/news-events/news/vulnerability-exploitability-exchange-vex-status-justifications` → 404,
  46957 bytes, sha256 `ec8e69c7…c541a19`; corrected publication page → 200, 56383 bytes, sha256 `2cb3a40b…37191b8c`,
  `Publish Date June 01, 2022`, archive notice; primary PDF `VEX_Status_Justification_Jun22.pdf` 313386 bytes
  sha256 `9a4027c6…fcf513f`, CreationDate 2022-06-30, `pdftotext -layout` text 274 lines sha256 `2b480ac8…cf8df4e6`;
  locators L46-L47 and L208-L209.
- **Decision against the scout's "OPEN ROW" recommendation, on machine-gated grounds:** (a) the scout delivered no
  capture and no manifest record, so a `mined` row could not be bound by `source-recheck` or the audit; (b) no
  entry lands this round that would cite S061, so `mined` would be an unbound row (RevNewRows) and `mined` with
  `used-by = —` raises W03 = a new W code = the C2 kill rule; (c) `queued` would add 1 to `F_total` and break the
  claimed `(20+23)/(20+23) = 43/43 = 1.000` (the measure counts queued rows, `SCORECARD.md:1551`). The rejection
  states the true ground (the five labels are already carried normatively by S055, which cites this PDF as its
  VEX-Justification reference) and a firing flip (a scoped capture of the PDF plus an entry that needs the 3.7.3
  cannot-be-controlled vs inline-mitigations distinction) — recorded now, adjudicable by CritSourceTruth.

### S062 — OASIS CSAF v2.1 Committee Specification Draft 04 — rejected

- Same ledger: v2.1 page 200, 1231332 bytes, sha256 `fdb4bf01…5f366b0` (byte-identical to `csd04/`); directory
  listing 1097 bytes sha256 `5e59949c…2f03775` with csd01 28-May-2025 … csd04 21-Oct-2026 and no `os/`; parent
  listing 392 bytes sha256 `64a94196…6ec94b` (`v2.0/`, `v2.1/` only); `os/` and `os/csaf-v2.1-os.html` both 404,
  41334 bytes, sha256 `e416b400…fcfd731`; locators L498 (CSD 04, 21 October 2026) and L7611 (nine product_status
  properties).
- The round-39 flip monitor therefore **has not fired**; status `rejected`, tier B (unapproved draft, not a tier-A
  normative source), recheck `30d` against the cheap directory listing, flip states the exact 200-plus-front-matter
  condition that would admit it. Draft drift (nine product_status properties vs v2.0's eight; flag-values sentence
  MUST → SHALL) is recorded in `teaches` so the monitor is re-checkable without re-reading 728k of text.

## Validation (commands and actual output)

Scratch mirror = lane `corpus/SOURCES.md` + the three delivered rows inserted at line 65, with `corpus/knowledge`
copied, so census runs over the after-state without touching the lane. All runs under
`S=/fast/scratch/hyaku/kasegi-r40/ScribeNewRows`.

1. After-state validate with the F23 entry's real delivered bytes at the used-by path
   (`mirror3/corpus/knowledge/cyclonedx-analysis-subtree.md` = `wave1/ScribeF23.entry.md`):
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/mirror3/corpus/SOURCES.md" kasegi
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r40/ScribeNewRows/mirror3/corpus/SOURCES.md
exit=0
```
   The entry side of the binding holds too: `source: S060 — https://cyclonedx.org/docs/1.7/json/ — capture
   corpus/source-snapshots/round-40/S060.txt (111 lines, 4,889 bytes; sha256 d6862622…)` and
   `recheck: … --manifest corpus/source-snapshots/round-40/manifest.json --source S060`.
   Pre-landing control on the same mirror without that file printed exactly one finding outside the pre-existing
   W04s — `file E11 S060 missing used-by corpus/knowledge/cyclonedx-analysis-subtree.md`, exit=1 — which is the
   landing dependency, not a row defect.
2. Path-existence control (rows-only mirror + a stand-in file at the used-by path; E11 tests existence only):
```
bash …/sources-census.sh validate --file "$S/mirror2/corpus/SOURCES.md" kasegi
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r40/ScribeNewRows/mirror2/corpus/SOURCES.md
exit=0
```
   i.e. the only census findings the three rows can add are none: the two pre-existing W04s stay the whole list,
   and no E01-E12/W01-W03 appears for S060/S061/S062.
3. Census counts on the rows-only mirror (for the lesson/scorecard arithmetic): `rows 62`, `tier.A 57`, `tier.B 3`,
   `tier.C 2`, `mined 45`, `queued 9`, `rejected 8`, `missing 0`, exit 0. Delta from 59 rows: +2 tier A, +1 tier B,
   +1 mined, +2 rejected, **+0 queued**.
4. W04 mutant control (why S060's `scope` cell repeats S059's verbatim): rewriting only S060's scope cell to any
   other prose prints `file W04 S060 duplicate url cyclonedx.org/docs/1.7/json across scopes`, i.e. a new W code and
   a C2 kill. Trimmed-scope-cell sha256 equality S059 = S060 = `a5367f385e94c5b3cf429299eed99a814c4fb45d2e01df64a492d73688dad94a`.
5. Shape per row (`gawk -F'|'`): `S060 NF=13 kind=spec tier=A status=mined opened=2026-10-26 recheck=on-release
   usedby=corpus/knowledge/cyclonedx-analysis-subtree.md`; `S061 NF=13 kind=docs tier=A status=rejected
   opened=2026-10-26 recheck=365d usedby=—`; `S062 NF=13 kind=spec tier=B status=rejected opened=2026-10-26
   recheck=30d usedby=—`. Host UTC date at validation: `2026-10-26T21:21:13Z` (E08 clean).
6. Counting-command pre-check on the same mirror: `S060+ rows = 3` (`grep -cE '^\|[[:space:]]*S06[0-9][[:space:]]*\|'`),
   `queued anywhere = 9` (unchanged by these rows, so `F_total` stays 22→23 + 0 after the nine are decided).
7. Ids/URLs: registry held no S060+ and no collision; the census `url_of` extraction for the three rows is
   `cyclonedx.org/docs/1.7/json`, `www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf`,
   `docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html`. The CISA PDF URL has 0 hits in `corpus/SOURCES.md`; the
   CSAF v2.1 URL has 1 hit, at `corpus/SOURCES.md:90` in the `## Registry changes` round-38 sweep bullet (not a
   registry row); the CycloneDX URL has 1 hit, on the S059 row it supersedes.

## Landing dependencies (L1)

1. Land `wave1/ScoutF23Lead.capture.txt` as `corpus/source-snapshots/round-40/S060.txt` and merge
   `wave1/ScoutF23Lead.manifest-record.json` into `corpus/source-snapshots/round-40/manifest.json`
   (`schema_version: 1`, `sources: [ … id S060 … ]`) — the row's anchor and the F23 `recheck:` line both name that
   path, and its sha256 is the one in both.
2. Land `wave1/ScribeF23.entry.md` at `corpus/knowledge/cyclonedx-analysis-subtree.md` (path corroborated by
   `wave1/ExecH9DeclaredBlocks.readme.txt:5,15,19` and the seat's own correction message); the pre-landing control
   in Validation run 1 shows that this file's absence is the only census finding the rows can produce.
3. `wave1/ScribeGateBlocks.txt` can reuse S061/S062's `teaches` cells verbatim as the Gate's rejected rows
   (reason + flip), and S060's locators L7/L15/L50 with Q1 (`S060.txt:7`, 13 words) for the admitted quote.
4. No edit is proposed to `## Leads (unopened)` — the CISA June-2022 lead is no longer listed there (r39 moved it
   out); the two new rows are the disposition record.

## Known limits

- S061/S062 rest on the scout's fetch ledger, not a lane capture, so no manifest record may anchor either row
  (same rule as S056/S058/S059); their quotes/definition locators cannot be rechecked by `source-recheck` until a
  capture is taken — that is exactly what each `flip` states.
- S060 measures the normalized slice; the raw HTML digest drifts at Cloudflare-token bytes (documented in the
  anchor cell and by the scout's two fetches).
- The S061 rejection is a coverage decision, not a claim that the document is thin: it is first-party, archived and
  the origin of the five labels, and the flip is written to fire as soon as a capture plus a citing entry exist.

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ScribeNewRows/` (mirror, mirror2, mut, rows.txt) removed after copying the
deliverable into the wave dir.
