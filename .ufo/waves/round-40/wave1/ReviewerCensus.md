# ReviewerCensus — round-40 wave 1 receipt

Seat: ReviewerCensus (leaf, no subagent dispatch). Item: run the source census and
registry-shape checks on the claims-freeze commit, confirm exit 0 with only W04
S028/S029 and no new malformed rows; deliver outputs; no lane edits.
Axes judged: depth:verifiability, coverage.

## Scope and method

- Freeze commit `5e985b74075dd3813a63d7750966bf8abf693465` (tree
  `5e82a2a5c4ad244760c8860a053b4b73356c6708`) resolved in the lane repo
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (`git cat-file -t` → `commit`).
- Exported read-only to scratch with
  `git -C <lane> archive 5e985b7… | tar -x -C $S/export`; all checks ran from the
  export, never from the lane working tree. No lane, fleet, or shokuknow writes.
- Scratch `S=/fast/scratch/hyaku/kasegi-r40/ReviewerCensus/` created with
  `mkdir -p`, TMPDIR-bound work only; removed before yield (see Cleanup).
- Disk guard green before the run: `/tmp` 3% used, `/fast/scratch/hyaku` 26% used.
- No tools installed or upgraded (none needed); no pacman run.

## Naming note (CORPUS.md)

No file named `CORPUS.md` exists anywhere in the freeze tree
(`git ls-tree -r --name-only 5e985b7… | grep -i corpus` returns only
`.ufo/waves/round-2x/...` fixture paths). The lane registry is
`corpus/SOURCES.md`; the fleet-root `/home/vgpnk/Projects/shokunin/CORPUS.md` is
the corpus contract prose (no registry rows). The item's "histograms from
CORPUS.md" was therefore computed from the exported registry
`<export>/corpus/SOURCES.md` — the same file the census validate targets.

## Commands run and outputs (verbatim)

1. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/export/corpus/SOURCES.md`
   → exit=0, stderr empty:
   ```
   file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
   file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
   file	ok	/fast/scratch/hyaku/kasegi-r40/ReviewerCensus/export/corpus/SOURCES.md
   ```
   Re-run under the same command → exit=0, `diff` of the two runs: byte-identical.

2. `sources-census.sh census --file $S/export/corpus/SOURCES.md` → exit=0:
   rows 59; tier.A 55 / tier.B 2 / tier.C 2 / tier.invalid 0;
   status.queued 9 / status.mined 44 / status.rejected 6 / status.invalid 0;
   FLEET missing 0.

3. Manual awk histograms over the same export (independent of the tool;
   Registry-section-scoped, `-F'|'`, tier=$5, status=$9):
   ```
   registry_rows=59
   NF_histogram: NF=13 n=59
   duplicate_id_rows_total=0
   tier_histogram: A=55 B=2 C=2
   status_histogram: mined=44 queued=9 rejected=6
   ```
   Tool and manual histograms agree on every bucket.

4. Freeze-state cross-checks (same awk/grep over the export):
   `queued_ids: S016 S017 S019 S020 S021 S022 S023 S024 S025` (exactly the nine
   C2 rows); `S060plus_rows=0`; `frontier_rows=22` (corpus/README.md).
   Matches `.ufo/waves/round-40/c2-controls/before.txt` line for line
   (queued 9, registry 59, frontier 22, S060+ 0).

## Findings

- Census validate on the freeze export: **exit 0**; findings are exactly the two
  expected W04 warnings (S028, S029 duplicate URLs across scopes) and nothing
  else — no E-codes, no new W-codes.
- No new malformed rows: 0 × E01 (all 59 registry rows NF=13), 0 × E03
  (duplicate-id total 0), and the manual NF/duplicate-id histograms confirm the
  tool's clean result independently.
- Registry shape at freeze: 59 rows; tiers 55 A / 2 B / 2 C (no invalid);
  statuses 44 mined / 9 queued / 6 rejected (no invalid); queued ids are exactly
  the nine C2 rows. This is the C2 "before" baseline, unchanged and clean.
- Digests: exported registry sha256
  `f33d10f45142b6d59969cedbfc35a1d29a3ba672d62067da8424fc0d32a728f2`;
  validate stdout sha256
  `df8095327d734f698bef5176b22a62097394572a363642e87d42cd1ace8891a4`;
  census stdout sha256
  `241ac7795eb32c1eed85c55be50f4c4e3e0a3bebb93af1fc73776ee364c70a4f`;
  manual-histograms sha256
  `504ee8d2a331beaad3f294acd10573b546631458f6ba81b126768528177cb1db`.
- Run time (UTC): 2026-10-26T21:19:04Z.

## Deliverable

- `wave1/ReviewerCensus.txt` — 39 lines, sha256
  `bb30d9f424c1a5a201d0b6239da5d248e006f1a69b81c00bdc48735144520208`
  (1374 bytes). Contains only the landable census outputs and the verdict line;
  the `file ok` third field is the scratch export path (verbatim tool output;
  the run was from the export, not the lane tree).

## Residual risk / gaps

- None in scope. The validate `ok` line's path is scratch-bound by construction
  (run-from-export requirement); the registry bytes it names are pinned by the
  sha256 above. No lane edits were made or needed.

## Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r40/ReviewerCensus/` removed before yield;
receipt and deliverable live in the wave dir. No other writes.
