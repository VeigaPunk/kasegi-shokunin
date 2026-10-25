# Round-29 assimilation report — kasegi

**Theme:** program severity ladders and reward scales (F13).

**Package provenance:** `/home/vgpnk/Projects/shokuknow/merge/kasegi` was read-only. Its `MERGE-REPORT.md`, `SOURCES.append.md`, and selected candidate knowledge entries were read; nothing was written to the package. No campaign tool was run there. This report records the staged-package/lane join and the F13 adoption decision; it is not an independent verification of every research claim.

## Staged and lane ID sets

The staged registry list is the 94 IDs **S031–S124** (`.ufo/waves/round-29/assimilation/staged-ids`). The lane registry list at base revision `7a6591c1eb8a14f427297980a96fa8bb339f29ee` is the 42 IDs **S001–S042** (`assimilation/reg-ids`). Both sequences are contiguous. Their numeric intersection is 12 IDs, **S031–S042** (`assimilation/collisions`). These are ID collisions, not necessarily duplicate documents: among the numeric overlaps, only staged S042 matches lane S042 by URL.

## By-document join and renumbering

Independent ScoutAssimilation and ConnStagedCensus measurements agree on the canonical-URL join. Census: 42 lane rows; 94 staged rows, of which 91 have URLs and three are own-work rows (S072, S110, S113). One staged row matches lane under the same ID; 12 match under different IDs; 78 URL-bearing staged rows are absent by URL; 81 total staged rows are absent when own-work rows are included.

| Staged ID | Lane ID | Document identity / decision |
|---|---|---|
| S039 | S033 | e-Gov lawdata; existing document |
| S040 | S034 | MIC/Soumu citizen page; existing document |
| S041 | S035 | NPA commentary PDF; existing document |
| S042 | S042 | IPA intake-process page; same ID and document, adopted in round 28 |
| S043 | S041 | JPCERT/CC 2026 guideline PDF; existing document, cite lane S041, do not re-register |
| S055 | S036 | Cybozu handling policy; existing document |
| S056 | S037 | Cybozu bounty FAQ; existing document |
| S057 | S038 | GMO Pepabo policy; existing document |
| S060 | S039 | Hitachi HIRT process; existing document |
| S064 | S041 | JPCERT/CC 2026 guideline PDF; existing document, cite lane S041 |
| S068 | S040 | Cisco policy; existing document |
| S076 | S041 | JPCERT/CC 2026 guideline PDF; existing document, cite lane S041 |
| S123 | S032 | NIST SP 800-115; existing document |

For this round’s F13 target, the three documents are absent by URL and IDs are free: **staged S031 → lane S043** (HackerOne policy_versions), **staged S032 → lane S044** (Bugcrowd VRT README), **staged S033 → lane S045** (Bugcrowd CWE mapping JSON). Round-29 scout findings report zero lane rows carrying any of those URLs and zero existing S043/S044/S045 rows. The frozen C2 claim defines the same mapping. The full join table was assigned to `ConnStagedCensus-2` at `.ufo/waves/round-29/wave1/ConnStagedCensus.md`; the compact delivered census findings and independent scout calculation agree.

The alias map has no constant offset: staged S039→lane S033 and staged S123→lane S032 are far apart numerically. Do not renumber by arithmetic. Also, staged S043, S064 and S076 are three section-scoped records for the same JPCERT/CC PDF already held as lane S041; registering any as a new lane row duplicates the document (round-28 scratch validation measured a W04 duplicate-URL warning for staged S043 alongside lane S041).

**Round-28 correction:** staged S042 maps to lane S042, not S041; the URLs differ (IPA process page vs JPCERT/CC guideline). Staged S043 maps to lane S041.

## Guard proof

The round-29 scout re-ran the discriminating fixture: under `^ {0,3}\|`, the two-space-indented S002 registry fixture produced one collision (`a-collisions`, S002); under column-zero-only `^\|`, the same fixture produced zero collisions (0 bytes). Thus the 0–3-space-tolerant guard detects the indented duplicate the column-zero form misses. This is guard-fixture evidence; the round-29 base collision artifact separately records the actual 12-ID intersection.

## Admitted, not adopted, and quarantine

- **F13 target:** staged S031/S032/S033 are the intended rows for one entry, `corpus/knowledge/program-severity-ladders-and-reward-scales.md`, under lane IDs S043/S044/S045. Scout found the three staged rows schema-clean (NF=13 / 11 columns; kind docs/docs/dataset; tier A; status mined; bare 90d rechecks). Scout reports that the landed captures digest-match their manifest, fresh S032/S033 fetches locate anchors, and the S031 page presents a JavaScript-gated shell while capture is a one-line JSON response with quotes located. The frozen C2 claim identifies this theme and mapping. This report does not independently establish the final lane entry’s full gate results.
- **Other reviewed staged candidates:** `program-scope-rules-and-asset-boundaries.md`, `claim-packaging-and-report-quality.md`, and `chinese-program-severity-instrument.md` were read as package material, not adopted F13 outputs. The staged used-by targets were absent in lane at the scout’s measurement, so premature registry rows naming them would trigger E11 until their entries land. No gate rejection is claimed here.
- **Ground namespace:** the staged severity entry’s package `ground: F10` is not the lane’s F10 topic; lane F10 is vendor-side disclosure policy, and the new lane frontier is F13. Lane entry must use lane F13 and rows S043/S044/S045, not staged IDs. The staged source headers require re-pointing to those lane IDs.
- **Quarantine slice:** seven rows; none adopted. Fresh ScoutAssimilation-2 verdicts: S037 `fetched-no-quote`; S054 `fetched-no-quote`; S048 `unfetchable`; S065 `reachable-quote-located`; S068 `already-mined-by-document` (lane S040); S069 and S070 `reachable-quote-located` using their full staged URLs (the register locators are truncated). Thus the register’s older “could not be fetched” class was disproved for S065/S069/S070 in this round’s fresh checks; none of the seven was adopted. The F13 target URLs are absent from the quarantine slice. Exact fetch sizes, anchors, and flip conditions are in the scout report/receipt, not reconstructed here.

## Evidence boundary

Consulted: frozen claims; lane registry/frontier and scorecard; QUALITY; round-28 lesson and verifier spot-check; proposal memo; instruments README; read-only package report, registry and selected entries; round-29 `staged-ids`, `reg-ids`, `collisions`, `quarantine-slice`, `c2-controls/before.txt`, and `census-before.txt`; delivered findings from `ScoutAssimilation`, `ConnStagedCensus-2`, and `ScoutAssimilation-2`. No source fetch was run by this scribe; no tools were installed. Model route table lists `openai-codex/gpt-6-luna`, matching the session runtime identity.

This is an assimilation report, not a claim that the round is closed: final lane entry landing and its complete gate results remain outside the evidence directly inspected here.
