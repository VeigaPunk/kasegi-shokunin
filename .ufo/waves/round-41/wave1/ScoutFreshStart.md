# ScoutFreshStart — round-41 wave-1 receipt (scout)

Seat: ScoutFreshStart (leaf; no subagents). Deliverable: `.ufo/waves/round-41/wave1/ScoutFreshStart.txt` — the owed-items checklist, 29 lines, sha256 `7ed75a1841cd8d3cc561d51416bb2aba734c25df677543d0d169dd320a7609ac`.

## Task
Read the last three rejected closures (r38/r39/r40 verifier spotchecks §5), build the owed-items checklist mapping every routed defect to a round-41 closure (I-check, named seat deliverable, or out-of-scope reason), and flag anything unmapped.

## Method / commands run (all read-only; cwd scratch `/fast/scratch/hyaku/kasegi-r41/ScoutFreshStart`, lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

1. `grep -n "^#" corpus/lessons/round-{38,39,40}-verifier-spotcheck.md` → located §5 "Routed defects" at r38:153, r39:156, r40:174.
2. `grep -c '^- \*\*R[0-9]' round-38-verifier-spotcheck.md` → **5** (r38 routes R1-R5 only; no R6/R7 exist). r39 → **7** (R1-R7); r40 `^- \*\*D[0-9]` → **7** (D1-D7).
3. Parsed `.ufo/waves/round-41/wave1-dispatch.json` → 60 seats; read every task spec; mapped routed items to `ExecI*`, `Scribe*`, `Rev*`, `Crit*`, `Mut*`, `Scout*`, `Sentinel*` owners and to claims.json I1-I12.
4. `grep -n "Correction (round" SCORECARD.md LOG.md SHONEN.md corpus/lessons/round-{38,39,40}.md` → confirmed prior-round closures: `Correction (round 39)` appends close r38 R2/R3 (SCORECARD:1560,1579,1580; LOG:1704,1718,1719; SHONEN:190,203; round-38.md:311); `Correction (round 40)` appends close r39 R2 (SCORECARD:1588,1589; LOG:1723,1724; SHONEN:207,208,219; round-39.md:98,99).
5. `grep -n 'M38-5|M38-7|M39-2' corpus/QUALITY.md` → R36 (cites M38-5/M38-7) and R37 (cites M39-2) present → r38 R4 closed r39, r39 R5 closed r40 (verifier re-derived `grep -cE 'M39-2' QUALITY.md` 0→1, r40 spotcheck :86).
6. `ls /fast/scratch/hyaku/` → no `kasegi-r39*` entry (only live r41 + sibling lanes) → r39 R4 leftover confirmed removed.
7. `awk '/^## Mistakes/,/^## [^M]/' corpus/lessons/round-{39,40}.md` → M39-1 (r38 R1 class mined, R34 criterion), M39-3 (R3 class, R35), M39-4 (R4 class, R36), M40-1 (r39 R1 mined evidence-provenance, captured-by fix + R37).
8. `sed -n '101,105p' corpus/lessons/round-39.md` → "Gate additions (round 40, verifier R6)" section carries URL+date+located quotes for S056/S058/S059 → r39 R6 closed r40.
9. `sed -n '82,90p' corpus/lessons/round-40-verifier-spotcheck.md` → verifier's plain re-derivation: r39 R2 swept, R5 0→1, R6 +11/−0, R1 mined M40-1, R3 "controls are now in the receipt's H8 transcript", R4 no leftover → r39 R1-R6 all closed in r40; R7 carried to r40 D3 → r41.
10. r40 defect sites verified live: `sed -n '9p;27p;29p;31p' corpus/lessons/round-40.md` → L9 wrong tallies "33/35 = 94% … 50/89" (D5), L27 garbled "tier A +3?mined" (D4), duplicated `## Gate` at L29/L31 (D4); `sed -n '1118,1123p' SKILL.md` → blank L1121 breaks the registry table before the r40 row at L1122 (D6).
11. `sed -n '855,889p' corpus/instruments/r40-closure.sh` → r40 H8 runs the export's own suite in leaf mode over base+r39 head and compares actual tallies (`[ "$b" -lt 10 ] && [ "$rc" -eq 1 ] …`) → lineage of r38 R5's G8 sub-class; r41 I10/ExecI10NegCtl strengthens it with the killable M-H8a predicate.
12. `sed -n '89,94p;136,138p;553,580p' corpus/instruments/r38-closure.sh` → r38 G4 "compares counts, not identities" (dispatch tasks vs results seats). `grep -n 'check_h' corpus/instruments/r40-closure.sh` + header (`sed -n '1,40p'`) → r40 H1-H10 list: H4 = located-quotes check; NO dispatch/results seat-identity limb exists in r40/r41.
13. `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → green (scratch 25% used, 608.9G free).

## Checklist result
The full 19-row checklist is the deliverable (`ScoutFreshStart.txt`): r38 R1-R5 (5 rows), r39 R1-R7 (7 rows), r40 D1-D7 (7 rows). Summary of statuses: **5 MAPPED-NEW** (r38 R5 mutants/escapes limb-family, r39 R7, r40 D1-D6 — the six r40 rows land via I1+I2+I3-I11 + ExecI1Blocks/ScribeCorrections/ScribeScorecard/ScribeShonenLog/ScribeLesson/ExecI3-I11 limb seats + RevD4D5D6 erratum blocks + ExecI7Registry.skill-fix.txt), **13 MAPPED-GUARD** (r38 R1-R4, r39 R1-R6 — each closed in an intermediate round, re-derived by the next verifier, and guarded this round by the frozen I-checks or named verifier seats), **1 OUT-OF-SCOPE** (r40 D7 — protocol-lane-owned, status-neutral), **1 OPEN sub-class** (below).

## Flags (unmapped items)
- **r38 R1-R7 vs file**: the round-38 spotcheck §5 routes only **R1-R5** (`grep -c` → 5). No R6/R7 rows exist; nothing missing, the prompt range was template spill.
- **OPEN — r38 R5 sub-class "G4 counting seats not identities"**: no round-41 I-check or named seat deliverable binds a dispatch's `taskCall.tasks` to a results file's seats *by identity*. The limb was dropped in the r39/r40 suite redesign (r40 H4 is the located-quotes check, not seats); neither the r39 nor the r40 verifier re-routed the class; SentinelScope is watch-only (it lists stray files, not a claim check). If the verifier requires a live limb for this class it has no owner this wave — recommend the L1 either rule it retired (the check was removed, so the defeat has no live limb to fool) or assign a wave-2 limb. Everything else maps: **no other routed item is unmapped.**

## Notes for the L1
- Deliverable file `ScoutFreshStart.txt` is the landable checklist only; this receipt carries the evidence. Place/lift as needed.
- Scratch `/fast/scratch/hyaku/kasegi-r41/ScoutFreshStart` removed at yield per I6 discipline.
