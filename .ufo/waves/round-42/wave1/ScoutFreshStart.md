# ScoutFreshStart — fresh-start coverage matrix (routed-defect -> J<n>/C2-item)

Seat: ScoutFreshStart (scout, leaf). Round-42 wave 1, item: coverage-of-debt receipt.
Deliverable: `.ufo/waves/round-42/wave1/ScoutFreshStart.txt` — 118 lines, 9237 bytes,
sha256 `1496a7ff208a58d052d3926d621427c8781bb030870893a7597345ffc0f31dd4`.

## What was read (all at base 5053a7f46de35784cff4b56756906e9014a38276)

- `.ufo/waves/round-42/claims.json` — frozen C1 (J1-J13 + 7 named repair families
  F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP, J8-J13) and C2 (F25 lead screen,
  S064 row/capture/manifest/entry, harness 28/28, binding 56/56, audit expected=61,
  census exit 0, measure 1.000, junk-twin control, F24 parked).
- `corpus/lessons/round-41-verifier-spotcheck.md` section 5 (lines 130-155):
  D-r41-1..D-r41-5 + carried wave-2 queue (I1, I3, I7, I5/I12, I6 stray,
  capture-binding missing-path/URL, frontier status-flip).
- `corpus/lessons/round-40-verifier-spotcheck.md` section 5 (lines 174-208): D1-D7.
- `corpus/lessons/round-39-verifier-spotcheck.md` section 5 (lines 156-189): R1-R7.
- r41 wave-2 defeat artifacts: `MutSuite.findings.txt`, `RevC1Counters.md` (I1/I3
  surviving mutants), `MutSkillTablePipes.findings.md` (bare-pipe + leading-whitespace
  survivors), `MutScratchTiming.md` (outside-configured-root stray), `MutC2Chain.md`
  (probe A: F24 admitted->explored -> `entries=26 pass=26 exit 0` SURVIVED),
  `MutBindingExistence.md` (missing-path + URL-case + trailing-slash all bound=63
  SURVIVED), `CritDeclarationCoverage.md` (validated-subset, not completeness),
  `CritI12Necessity.md` (T7 symlink limb necessity), `CritC2Live.md`,
  `CritC1KillRule.md`, `MutAuditUnexpected.md` (orphan mined row survives binding).
- `corpus/lessons/round-{39,40,41}.md`, `SCORECARD.md` (L1588-1628, incl "Planned for
  round 42"), `LOG.md`, `SHONEN.md`, `corpus/QUALITY.md` (M39-2 -> R37 criterion),
  `SKILL.md` L1106-1129 (registry blocks), `corpus/README.md` frontier rows F20-F24,
  `c1-controls/do-nothing.txt`, `c2-controls/before.txt`.

## Findings

Every instrument-routable routed defect in the three section-5 documents maps to a
frozen J-check or C2 item — full matrix in the deliverable. Three exceptions flagged:

1. **D-r41-4 (report "Stale-lane" line)** — NO closing J/C2 check; L1-owned report
   conformance item for the round-42 report.
2. **D-r41-5 (wave-2 0 connector seats)** — NO closing J/C2 check; L1-owned
   dispatch-shape item, carried on the queue.
3. **r40 D7 (queued->rejected teaches rewrite ambiguity)** — NO closing check and
   explicitly not kasegi-owned (protocol-lane contract ambiguity, status-neutral).

Two live-base collision flags for the suite owner (residual unknowns, not defeats):

- **J3 scope**: base SKILL.md already violates both J3 invariants — blank L1121
  between the round-40 table separator (L1120) and its row (L1122), and
  `r40-closure.sh` basename appears in two rows (L1122, L1128). An unscoped J3 is
  red at Y by construction; the suite must scope to the newest block + an appended
  repair marker, or the lane must append a dedup/repair block (append-only rule:
  deleting L1121/L1128 trips J12's no-deletion guard — actually J12 is
  corpus-paths-only, but SKILL.md edits remain append-only convention).
- **J11 scope**: base SCORECARD.md already carries the verbatim duplicated
  `Correction (round 41)` block (L1602-1605 = L1607-1610). J11's "no duplicated
  Correction block" is red at Y unless scoped to round-42+ corrections or a dedup
  marker is appended (verifier said "no rewrite — append-only").

C2 no-overlap prescreen for the lead class: `grep -rniE 'osv|cve[ -]?(record|5\.|json
schema|services)'` over `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md` and
`corpus/knowledge/` returned zero hits — neither OSV schema nor CVE Record Format is
covered by an existing lane row or entry. Frontier currently 24 rows (F20-F24
confirmed admitted).

## Commands run (verbatim outputs)

- `bash scripts/hyaku/disk-guard.sh status` -> /fast/scratch/hyaku 27% used, 592.6G
  free (green; ran before reads).
- `ls corpus/lessons | grep -iE 'verifier|round-(39|40|41)'` -> three spotcheck files
  present (18449, 19163, 15057 bytes).
- `grep -c 'M39-2' corpus/QUALITY.md` -> `1`.
- `grep -n '^Correction (round 41)' SCORECARD.md` -> L1602-1605 and duplicate L1607-1610.
- `grep -nE 'r4[012]-closure' SKILL.md` -> r40-closure.sh rows at L1122 AND L1128;
  blank L1121 between separator L1120 and row L1122 (D-r41-3 confirmed live).
- `grep -cE '^\| F[0-9]+ \|' corpus/README.md` -> `24`.
- `wc -l` + `sha256sum` on deliverable -> 118 lines, sha256 above.
- `git status --short` -> only untracked wave1 sibling artifacts + this seat's two
  files; no tracked modifications by this seat.

## Tooling / network / writes

- Tools installed: none. Network fetches: none.
- Writes: `.ufo/waves/round-42/wave1/ScoutFreshStart.txt` (deliverable) + this
  receipt only. No lane/git mutations, no fleet-root or sibling-lane writes.
- Scratch `/fast/scratch/hyaku/kasegi-r42/ScoutFreshStart/` created for TMPDIR and
  removed before filing (rm -rf; verified gone).

Report: .ufo/waves/round-42/wave1/ScoutFreshStart.md
