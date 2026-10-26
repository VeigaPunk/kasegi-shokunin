# ScribeEntriesG2 — round 40 wave 1, knowledge entries for the second mined group (S020, S021, S023, S025)

Seat: ScribeEntriesG2 (scribe, leaf). Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `a7af2ce63bce153757d39bf66b366a96caf30c13`, claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`). Item: write knowledge entries for S020, S021, S023, S025, same format and bar as ScribeEntriesG1, with provenance trio, `ground:`, quotes anchored to captures; if a source is not captured, do not write its entry and report the dependency.

**All four sources were captured by their scout seats in this wave, so all four entries exist.** No dependency blocked an entry.

## Deliverables (byte-exact, in `wave1/`)

| row | deliverable file | lands as | lines | bytes | sha256 |
|---|---|---|---|---|---|
| S020 | `ScribeEntriesG2.doj-vdp-framework-scope-and-authorization.md` | `corpus/knowledge/doj-vdp-framework-scope-and-authorization.md` | 139 | 17,782 | `25f357f1458cd15ea25b73afafc8bf9caf4a81bfcc35aad0c6abab20cf372e48` |
| S021 | `ScribeEntriesG2.cisa-bod-20-01-vdp-minimums.md` | `corpus/knowledge/cisa-bod-20-01-vdp-minimums.md` | 162 | 20,119 | `f83a03cd9307fae0ffbdbbd6dc3cfb40d03725a13fa0e2247ed00a9a9910274c` |
| S023 | `ScribeEntriesG2.cisa-cvd-program-stages.md` | `corpus/knowledge/cisa-cvd-program-stages.md` | 134 | 18,214 | `3fd49ca4b5bb2a17f65aa92c8762f2473796cdfe06be16174dad430c5233b4a4` |
| S025 | `ScribeEntriesG2.cve-bench-agent-exploitation-benchmark.md` | `corpus/knowledge/cve-bench-agent-exploitation-benchmark.md` | 141 | 20,566 | `dd6c780e82c51a2b4dd11229d7cf5174c9709c241d052b5d6eb754c199c20c19` |

Slugs match what ScribeRows proposed for its `used-by` cells (messaged and confirmed before writing: `doj-vdp-framework-scope-and-authorization`, `cisa-bod-20-01-vdp-minimums`, `cisa-cvd-program-stages`, `cve-bench-agent-exploitation-benchmark`). Each deliverable contains only the entry text — no validation tables, no seat notes.

## Captures used (scout deliverables, read-only to this seat)

| row | wave1 capture | lines | bytes | sha256 | HTTP | fetched_utc | record quotes |
|---|---|---|---|---|---|---|---|
| S020 | `ScoutS020.capture.txt` | 319 | 16,693 | `8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c` | 200, `application/pdf`, 140,909 raw bytes | 2026-10-26T21:16:10Z | 1 (Q1 @142) |
| S021 | `ScoutS021.capture.txt` | 432 | 58,004 | `72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329` | 200, `text/html`, 127,832 raw bytes | 2026-10-26T21:15:57Z | 1 (Q1 @133) |
| S023 | `ScoutS023.capture.txt` | 213 | 14,357 | `52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087` | 200, `text/html`, 75,587 raw bytes | 2026-10-26T21:16:01Z | 2 (Q1 @151, Q2 @154) |
| S025 | `ScoutS025.capture.txt` | 1,490 | 71,851 | `faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b` | 200, `application/pdf`, 602,933 raw bytes | 2026-10-26T21:16:02Z | 2 (Q1 @32, Q2 @507) |

I did not fetch any source; these are the scouts' bytes. `sha256sum` over my scratch copies reproduced each record's `sha256` exactly (`S020 8fc334be…5458c`, `S021 72dbba57…e329`, `S023 52a6671f…6087`, `S025 faa1c1f8…9b7b`).

## Validation run (all against a scratch fixture, since `corpus/source-snapshots/round-40/` is not landed yet)

Scratch: `/fast/scratch/hyaku/kasegi-r40/ScribeEntriesG2/` with `fixture/` holding the four captures renamed to the landed stems (`S020.txt` … `S025.txt`) and a `manifest.json` (`schema_version: 1`, `sources: [4 records]`) assembled from the scouts' records. This is the exact layout the entry `recheck:` lines name.

**1. `source-recheck` on the fixture — four sources, exit 0 each.** Command shape:
`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /fast/scratch/hyaku/kasegi-r40/ScribeEntriesG2/fixture/manifest.json --source S0XX`

```
S020:sha256 OK
S020:Q1 OK normalized=markup-whitespace occurrences=1 anchor=142-ok
exit=0
S021:sha256 OK
S021:Q1 OK occurrences=1 anchor=133-ok
exit=0
S023:sha256 OK
S023:Q1 OK occurrences=1 anchor=151-ok
S023:Q2 OK occurrences=1 anchor=154-ok
exit=0
S025:sha256 OK
S025:Q1 OK normalized=markup-whitespace occurrences=1 anchor=32-ok
S025:Q2 OK normalized=markup-whitespace occurrences=1 anchor=507-ok
exit=0
```

**2. Every blockquote in every entry re-located in its capture.** 72 blockquotes total (S020 14, S021 21, S023 16, S025 21); matcher = whitespace-collapsed containment in `lines[anchor-1 : anchor+3]` (the instrument's own window) plus a ≤25-word cap. Result: `bad 0`; longest quote 22 words.

**3. Every falsifiable-check command in every entry executed against the fixture.** 41 commands (S020 8, S021 10, S023 11, S025 12) extracted from the `` `cmd` → `expected` `` pairs and run with `bash -c`; **41 OK, 0 mismatch**. This covers the per-entry anchor checkers (FC-7 S020 = `anchors_ok 15 of 15`, FC-10 S021 = `anchors_ok 27 of 27`, FC-9 S023 = `anchors_ok 17 of 17`, FC-9 S025 = `anchors_ok 32 of 32`).

**4. Header/Q10 conformance.** Each entry opens `# title` / blank / `source:` / `verified-at:` / `ground:` / `recheck:`; each `recheck:` line parses under `bash -n` (exit 0), carries its own `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix, and names exactly the manifest and `--source` id of its own header. Each entry has `## Falsifiable rule and checks` and `## Rejected over-generalizations`.

Corrections I made during validation (recorded rather than hidden): three S023/S025 FC commands were written with an ellipsis instead of a full path and are now fully executable; S025 FC-6 was line-oriented `grep` and returned 0 for two phrases that wrap across lines, so it is now a whitespace-collapsed `python3` count; S025's `five attempts` expectation was 2 and measured 3; two blockquote anchors were off by one line (S021 L132 item, S025 L501) and one FC anchor list still carried the stale L502; S025's author count was wrong (sixteen, not fourteen) and the affiliation inference was replaced by the repository URL the paper prints. All re-verified after the fix — the 41/41 and 72/72 figures above are post-fix.

## What each entry claims (one line)

- **S020 (DOJ CCIPS Framework, v1.0 July 2017)** — a non-prescriptive design rubric whose stated purpose is to reduce CFAA exposure by describing authorised conduct (L41); scope is the organisation's own decision set (L45-L65); third-party/cloud-hosted components need exclusion or additional authorisation, and absent a provider agreement the organisation "may lack the authority to authorize others" (L142-L145); the CFAA footnote states the excess-of-authorization and non-domestic elements (L72-L79); the policy must state authorised and unauthorised conduct plainly (L232) and may publish three example commitments (L281-L293), which are examples, not DOJ undertakings.
- **S021 (CISA BOD 20-01, 2020-09-02)** — a compulsory federal direction (L92) requiring a published policy plus handling procedures (L98); element list with an anonymous-reporting statement (L125) and a no-legal-action commitment (L126); four "must not" terms including no vetted-only/citizens-only scope (L132), no disclosure gag beyond "a reasonably time-limited response period" (L133) and no VEP route (L134); scope must grow every 90 days to all internet-accessible systems at 2 years (L139-L140); no mandated fix deadline (L301, L380); 45-90 days is community practice as CISA describes it (L305); template aligns with the DOJ framework (L198); minimums, not ceiling (L204).
- **S023 (CISA CVD program page)** — CISA's own seven-stage coordinator pipeline (L115-L146) with a two-way triage outcome (L125-L127), the Top Level Root / CNA of Last Resort role (L112), mediation as a named coordinator action (L128-L133), publication across advisory/CVE record/CSAF (L141-L145), KEV evaluation as a later stage (L146), a factor-based disclosure timeline (L148-L152) whose only number is an "as early as 45 days" floor for an unresponsive vendor (L151), CVD reports outside VEP adjudication (L153), and CVD separated from VDP (L154-L155).
- **S025 (CVE-Bench, arXiv:2503.17332v4)** — 40 NVD CVEs, web applications only, CVSS v3.1 floor 9.0 (L155, L249-L251, L273); task = CVE + containers + reference exploit (L256-L258), construction 5-24 person-hours per task (L398), selection window 2024-05-01 to 2024-06-14 with four filters (L401-L409); eight standard attack goals (L277-L278) with file deletion excluded for DoS overlap (L333); zero-day vs one-day as the information variable (L370-L373); grading by goal achievement in-container (L410-L415); the reported rates as three separate sentences — abstract "up to 13%" (L33), experiments "up to 10% … 12.5%" (L507), baselines 2.5% and "as high as 13%" at five attempts (L122-L126) — left unreconciled, with the AutoGPT exception (L510-L512, L526-L528) and the configuration (gpt-4o-2024-11-20, 30 iterations, five repeats) attached.

## Findings the L1 should read before landing

1. **Landing map required** — the entries' `recheck:` lines and `source:` lines name `corpus/source-snapshots/round-40/S0XX.txt` and `corpus/source-snapshots/round-40/manifest.json`, which do not exist yet. L1 must copy `wave1/ScoutS0XX.capture.txt` → `corpus/source-snapshots/round-40/S0XX.txt` (stem must equal the id, or `source-recheck` reports `reason=stem-mismatch`) and merge the four records into one manifest with `schema_version: 1`.
2. **Two record shapes in one wave.** `ScoutS020/S021/S023.manifest-record.json` are bare source objects; `ScoutS025.manifest-record.json` is already a full manifest document (`schema_version`, `purpose`, `sources: [ … ]`). A naive `sources = [json.load(f) for f in records]` merge produces one malformed entry for S025. My scratch fixture merges them by unwrapping `sources` when present — that is the merge the 4× exit-0 run above used.
3. **Registry row S025 wording is not the paper's.** The row says "resolve up to 13% of vulnerabilities"; v4 says "can exploit up to 13% of the vulnerabilities" (L33) and the word "resolve" does not occur in that sentence. The entry quotes v4 and records the divergence as a rejected over-generalization, so a `used-by` cell that repeats the row's verb would contradict its own entry.
4. **S021's page lists BOD 19-02 and BOD 22-01 as revoked** (L398, L401) and BOD 26-04 as current (L389-L395). The entry claims only BOD 20-01's own text and says so; it does not assert present in-force status.
5. **S023 has no publication date.** `grep -ciE 'published|updated'` → 0 on the capture (entry FC-6), matching the registry row's "page has no visible publication date". The entry pins the fetch instant instead of an edition.
6. **Two source-side typos are quoted verbatim, not corrected**: S020 L283 "will not to pursue civil action"; S023 L153 "are no subject to VEP adjudication" (and "Lean more about VEP"). A future proofreader must not "fix" them — the manifest assertion for S023 Q1-adjacent text and the entries' FC checks match the captured bytes.
7. **S025's figures are not uniform** (13% abstract vs 12.5% one-day in the experiments section). The entry reports all three sentences with their anchors and refuses to merge them; anyone writing a SCORECARD line from this entry should cite the sentence, not "the paper's rate".
8. **`ground:` assignments** are one existing frontier row each: S020 → F09 (extends F03), S021 → F03 (with its clock material extending F02), S023 → F06, S025 → F04. I opened no new frontier row and touched no `corpus/README.md`; if ScribeF23/ScribeNewRows wants a different row for any of these, the `ground:` line is the only line that changes.

## Out of scope / not done here

- `corpus/SOURCES.md` rows for S020/S021/S023/S025 (ScribeRows), statuses and `used-by` cells.
- Landing the captures and the round-40 manifest, and any `corpus/README.md` frontier edit (L1 / ScribeF23 / ScribeNewRows).
- Running `source-recheck` against the real landed manifest (RevC2Entries does that after landing) and any SCORECARD/LOG/lesson append (ExecH2/ExecH3/ExecH4/ExecMistakesDraft seats).
- No product code, instrument, judge, or config was edited; no git mutation of any kind was run; no network fetch was made by this seat.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r40/ScribeEntriesG2/` (fixture + drafts) was removed after the deliverables were copied: `rm -rf -- /fast/scratch/hyaku/kasegi-r40/ScribeEntriesG2` then `test -e` → absent (`removed`); no scratch dir survives.
- Writes: the four deliverables above and this receipt, all under `wave1/`. Nothing else in the lane, fleet, or sibling repos was written.
- Tools installed: none. `pdftotext`/`python3` were already present; no `pacman` invocation (host-wide pause respected).

## Known limits

- The four captures are the scouts' bytes, and my validation is a *fixture* run, not a run against the landed corpus paths; it proves the entries' checks and recheck lines are executable and that the records bind, not that L1's merge will be correct (see finding 2).
- `source-recheck` verifies the manifest's assertions only: S020 (1), S021 (1), S023 (2), S025 (2). The entries' remaining claims rest on their own FC checkers, which re-run against the landed capture and are reproduced verbatim in each entry.
- S020 and S025 are PDF-derived text; the S020 page furniture (`N|Page`) and the S025 two-column interleave are documented in each entry's Scope and limits, and no claim depends on a figure image.
- Time: all capture instants are 2026-10-26T21:15:57Z–21:16:10Z; `verified-at: 2026-10-26` in each entry is the authoring day, not a source date.
