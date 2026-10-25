# ScribeAssim — round-30 assimilation evidence

Axes: **coverage** (F14 source/entry assimilation) and **depth:verifiability** (traceable source identifiers, quote locations, schema/census evidence). Scope: read-only package comparison plus report/evidence artifacts inside the lane; no production or registry edits by this seat.

## Status and byte limits

This report records available bytes, not an asserted completed integration. At inspection, lane `corpus/SOURCES.md` had rows through S047 and the F14 README appendix had landed, but F14 knowledge entry and round-30 capture manifest were not present. `ConnStagedCensus.md` and its `reg-ids`, `staged-ids`, `collisions` outputs were not present in the wave output directory at inspection, so this report does not invent their contents. The staged package source is `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`; package and absent-defect register are read-only.

The `SOURCES.append.md` path in initial supplied instruction text contained a typo (`SOURCESUR.append.md`); that path returned not found. The actual `SOURCES.append.md` was then read successfully. No tool install was needed. No live network or bounty target was contacted by this seat.

## ID lists / collision evidence

Requested copies `assimilation/reg-ids`, `assimilation/staged-ids`, and `assimilation/collisions` are **not produced**: ConnStagedCensus output was unavailable in the observed wave reports, and the complete collision computation/output was not available to copy. This is an evidence gap, not a zero-collision claim.

Observed lane state: `corpus/SOURCES.md` contains registry rows S001–S047; its tail includes new S046 and S047. Staged package row ids are S031–S124 (94 rows), as stated in `MERGE-REPORT.md` and visible in `SOURCES.append.md`. Numeric overlap is expected; numeric identity alone cannot establish source identity. Lane source row listing and staged row listing were inspected using `grep` pattern `^\| S[0-9]{3} \|` on each file; results were returned, but no copies were saved under assimilation/.

## Adopted-id mapping and URL-equality proof

Frozen claim C2 declares the document-based map `S049→S046`, `S050→S047`; staged ids are renumbered by continuing the lane registry. Comparisons of exact source URL strings:

| staged id | staged URL | lane id | lane URL | result |
|---|---|---|---|---|
| S049 | `https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf` | S046 | same URL in lane row | exact URL match |
| S050 | `https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html` | S047 | same URL in lane row | exact URL match |
| staged S043 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | S041 | same URL in lane row | exact URL match; reuse existing document/source id |

The staged entry cites S043 for the JPCERT/CC guideline; lane row S041 is the same document, not an arithmetic conversion. Lane SOURCES tail lines 52–53 identify S046/S047 and their capture locations. The F14 README appendix reports F14 sources `S046, S047, S041`.

## Gate-quote compliance

The F14 gate-quote check cannot be marked passed from observed bytes: the final lane entry and manifest were not available, so there are no final assertions/locations to count or validate. Staged entry has no quoted claim fragments in its body, and its prose statements are not a substitute for the required per-claim located quotations. The frozen task requires each quote ≤25 words and located; defer verdict until the final entry, captures and manifest are present and checked (including exactly-once/stem binding per QUALITY Q9).

## Normalization notes: staged cells → lane schema

1. **S049/S050 fields are clean in stage.** Both staged rows are 11 cells with no embedded pipe; `kind=docs`, `tier=A`, `status=mined`, date `2026-10-23`, `recheck=180d`, and `used-by` the single F14 entry. Lane convention requires adopted ids and round-30 opening date; observed lane rows S046/S047 are opened `2026-10-25` and use `90d` (S047) / `180d` (S046). Their anchors point to round-30 captures.
2. **S120 is not appended as-is.** Staged row S120 has an embedded literal pipe in the teaches cell, which breaks the lane's 11-column pipe-delimited schema. It requires escaping or rewriting before append. No S120 row appears in the observed lane tail; the task's “nog staged row appended as-is” appears to be a malformed name for this no-go check. This seat does not certify all 94 staged rows or a full census; S120 specifically is unsafe verbatim.
3. Other staged rows S081–S119 and S121–S124 include prose appended to `recheck` beyond duration. Registry convention uses bare cadence tokens (`90d`, `180d`, `on-release`); strip/move procedural prose before adopting those rows. S049/S050 themselves already have bare `180d`.
4. S049/S050 `opened` dates are ISO, but staged 2026-10-23 differs from lane adoption date 2026-10-25. The observed lane rows use 2026-10-25.
5. Keep adopted knowledge entry ids document-bound: replace S049/S050 with S046/S047, and staged JPCERT S043 with lane S041; preserve matching URLs/anchors. Do not renumber by arithmetic.

## Quarantine-slice context (not a gate verdict)

`assimilation/quarantine-slice` and `ScoutQuarantineSlice.md` record seven rows: S037/S054 marked payload-absent; S048/S065/S068/S069/S070 marked never checked. The scout identifies S069/S070 URLs as suspected truncated and the other five as full locators. This is an extraction from the absent-defect register, not a fresh-fetch result or a verdict by this seat. No quarantine row is deemed adoptable here.

## Inputs and artifact paths

- Frozen C2 mapping: `.ufo/waves/round-30/claims.json` (claim C2 assimilation block).
- Staged ids and source rows: `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (read-only).
- Package summary: `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md` (read-only).
- Staged F14 entry: `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (read-only).
- Lane ids: `corpus/SOURCES.md`; currently observed S001–S047.
- Frontier evidence: `.ufo/waves/round-30/wave1/ExecReadmeF14.md`.
- Quarantine extraction: `.ufo/waves/round-30/assimilation/quarantine-slice`; scout: `.ufo/waves/round-30/wave1/ScoutQuarantineSlice.md`.
