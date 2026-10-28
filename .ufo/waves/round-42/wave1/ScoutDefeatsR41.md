# Receipt — ScoutDefeatsR41 (kasegi round 42 wave 1, scout)

Deliverable: `.ufo/waves/round-42/wave1/ScoutDefeatsR41.txt` — 80 lines, sha256 `833073e105bd8738494cdf01cec03074eba0b9e25a683929bf4f27466f93687b` (copied byte-exact from scratch; `wc -l` and `sha256sum` output shown in Commands).

## Assignment executed

Read `.ufo/waves/round-42/claims.json` (frozen C1/C2 — C1 names the seven repair families and per-family replay artifacts). Read every committed file in `.ufo/waves/round-41/wave2/` — 32 entries: 26 seat receipts (9 Crit*, 11 Mut*, 6 Rev*) + 5 sidecars (`MutSkillTablePipes.findings.md`, `MutSuite.findings.txt`, `RevCaptureNormalization.receipt.md`, `RevRunUtc.receipt.md`, `RevScanOwnership.receipt.md`) + `swarm-registry.json` (seat metadata, not an artifact). Cross-checked the seat roster against `kasegi-r41-falsify-results.json` (33 seats, JSON outputs for the seats that filed no wave2 file) and `wave2-extra-items.json` (assigned probe specs). Cataloged each artifact by defeated check, mutation class, r41-selftest detection (graded lines verified verbatim in `final-gates/all-gates.txt`), and r42 family mapping.

## Findings summary (full catalog in deliverable)

- **11 replay-required executed defeats (D01–D11)** covering all seven families: F-EVID D01 (evidence-not-named union mutant), F-TOKEN D02 (`closed=10/100` mangled tally), F-TABLE D03/D04 (bare-pipe cell, leading-whitespace first cell — the two MutSkillTablePipes survivors; the two killed variants recorded as rejection-positive controls G12), F-SCAN D05 (outside-configured-root `/tmp/kasegi_r41_outside_probe` stray), F-DECL D06 (undeclared changed-path pair via committed scratch fixture + T7 cross-round note), F-BIND D07–D09 (missing-path, URL case-flip, URL trailing-slash manifest mutations), F-FLIP D10 (F24 admitted→explored → `entries=26 pass=26 exit=0`).
- **Flagged mapping decision**: D11 (unreferenced mined `S999` row survives `capture-binding-check.py` at `records=63 bound=63 unbound=0`) — binding completeness, adjacent to but textually outside the named J6 variants; recommend J6 replay covers it. G18 (JSON-only CritRegistryRecordCompleteness) is the same class, unexecuted.
- **UNMAPPED (none-new)**: G05 S063 `recheck:` line hard-codes the lane path (non-portable recheck — no J check or C2 clause owns it); G06 census freshness mutations never executed.
- **r41 selftest detection verdicts** (from `final-gates/all-gates.txt` graded lines): only D01 and D02 were *flagged* by the selftest (`I1 mutants=1/2`, `I3 mutants=0/1`, both `verdict=fail`) — flagging the fixture's own inadequacy while the defect still passed (`rejected=0`, the defeats). D03/D04/D05/D06 have no covering fixture; D07–D11 target instruments outside the r41 suite's selftest entirely.
- **J8–J13 inputs** are gap/design artifacts, not family replays: J8 ← G02 (digest-after-run + duplicate-case fixtures absent), G04, G08, G09; J9 ← G03 (ref-not-found distinct red confirmed, foreign-ref already rejected); J10 ← G01 (MutSuite: red baseline voids kill attribution → per-case private mutated copy); J11 ← lane-state duplication (SCORECARD.md:1602-1605 == 1607-1610, no wave2 attack artifact); J12 ← no artifact (density.py byte-identity re-derived in RevC1Counters.md: `ee803726…f710`); J13 ← G17 (RevScanOwnership's accidental `kasegi-r41` stray under suite root → `closed=0` is the quiescence shape).

## Commands run (verbatim)

- `ls -la .ufo/waves/round-41/wave2/` → 32 entries listed above.
- `read` on each of the 31 artifact files + `swarm-registry.json` parse → member roster 33 seats; members without filed files: RevReceipt, CritFresh, CritLessonTally, LabCaptureTruth, CritRegistryRecordCompleteness, CritProvinceBoundary, MutSelftestBaseline (outputs recovered from `kasegi-r41-falsify-results.json`).
- `read .ufo/waves/round-41/final-gates/all-gates.txt` → 31 lines; graded selftest lines quoted per entry.
- `read corpus/lessons/round-41-verifier-spotcheck.md:130-155` → §5 routed queue + D-r41-1..5; `read corpus/lessons/round-41.md:72-122` → wave-2 defeat summary confirming the defeat set.
- `read .ufo/waves/round-42/c1-controls/do-nothing.txt` → base control: r42 suite absent (exit 127), r41 suite at base `closed=8/12`, I1/I3 families open.
- `grep Planned-for-round-42 SCORECARD.md` → line 1628 (I1/I3 repair + green I2/Y + clean scratch baseline; F24 revisit only after L0 ruling).
- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → green (`/fast/scratch/hyaku` 27%, 592.4G free).
- `wc -l` + `sha256sum` on the deliverable → `80` lines, sha256 `833073e105bd8738494cdf01cec03074eba0b9e25a683929bf4f27466f93687b`.

## Boundaries observed

No lane/fleet writes outside `.ufo/waves/round-42/wave1/ScoutDefeatsR41.txt` (deliverable) and this receipt. No git/jj mutation, no installs, no network fetch. Scratch `/fast/scratch/hyaku/kasegi-r42/ScoutDefeatsR41/` removed after deliverable was copied out.

## Notes for consumers

- Replay limbs re-execute *committed* artifacts: the substrate for D01/D02 is the embedded `selftest_case_i1`/`selftest_case_i3` mutation code inside committed `corpus/instruments/r41-closure.sh` (exported at J); for D03–D11 the wave2 file is the executed spec whose exact mutation bytes the limb re-applies to a scratch copy. T7's substrate is r40 `wave2/RevC1Counters.defeats.txt` (cross-round — ScoutDefeatsR40 owns that catalog).
- Two UNMAPPED entries (G05 recheck portability, G06 census freshness) are routed-defect candidates for the L1/report, outside the seven named families — a committed Z artifact cannot kill C1 on them, but nothing currently checks them either.
