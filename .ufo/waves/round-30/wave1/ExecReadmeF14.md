# ExecReadmeF14 — wave 1 report (round 30, F14 README appends)

Seat: L2 leaf `ExecReadmeF14` (sole writer of `corpus/README.md` appends for round 30).

## Scope executed
Appended (R6, no existing line touched) to `corpus/README.md`, after the last line
(former line 264, the F13 appendix row):

1. **Coverage-map appendix row** (same shape as the F13 appendix row):
   `| Japanese severity vocabulary and handling-priority model (round 30) | `knowledge/japanese-severity-vocabulary-and-impact-model.md` | S046, S047 (S041) — public primary, opened 2026-10-25 |`
2. **F14 frontier row** (same shape as F13's row in its appendix table):
   `| F14 | Japanese severity vocabulary and the handling-priority model | admitted | knowledge/japanese-severity-vocabulary-and-impact-model.md | S046, S047, S041 | Keep each 深刻度 band label attached to the CVSS version that produced it (v2 bands survive beside v3); JVN translates CVSS base scores into Japanese vocabulary rather than scoring independently, so derive handling priority from the P-guideline steps, not from the label alone. |`
3. **Amendment paragraph** (historical note, never rewriting earlier text):
   `[r30 amendment, appended 2026-10-25] … at round 30 the frontier stands at **14/14 admitted** — F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30. The 0/18 sentence is untouched …`

Append landed as a `## Round-30 admission — coverage map row and Frontier F14 (appended 2026-10-25)` section mirroring the round-29 section shape, including the R6 preamble and both tables.

## Evidence (exact, measured post-append)
- **`awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → `14`** (was 13 pre-append).
- **Head bytes unchanged**: `head -c 27638 corpus/README.md | sha256sum` → `67d94e80d7253edcb1988f204a5176434b12cac93afd43db058b4c80a3a2c860` — identical to the pre-append whole-file sha256 of `corpus/README.md` (27638 bytes, 264 lines), so only a pure append occurred.
- **Post-append whole-file sha256**: `df04b0490591446c6605d421569a497845c22546dc27ea5a020fff770f2fc64f` (29620 bytes, 291 lines).
- **Final tail** (last 30 lines of `corpus/README.md`):
  ```
  | id | topic | status | entry | sources | next |
  |---|---|---|---|---|---|
  | F13 | Program severity ladders and reward scales | admitted | knowledge/program-severity-ladders-and-reward-scales.md | S043, S044, S045 | Keep each platform's ladder as its own suggested baseline — distinct from CVSS-B and from other programs' reward ceilings; do not generalize a payout scale across programs. |

  ## Round-30 admission — coverage map row and Frontier F14 (appended 2026-10-25)

  The coverage map above is not edited in place (R6): the round-30 entry
  `knowledge/japanese-severity-vocabulary-and-impact-model.md` (Frontier F14, sources S046 +
  S047 + S041; source basis: the IPA JVN activity report PDF and the IPA JVN quarterly
  registration report, both first registered this round, plus the already-registered
  JPCERT/CC 2026 guideline S041, all captured 2026-10-25 under
  `corpus/source-snapshots/round-30/`) is recorded here as an appended amendment so every
  existing line keeps its number. The coverage-map row is appended here rather than inserted
  into the map, and the F14 frontier row is listed here on the same table shape as the
  frontier above.

  | Area | Entry | Source basis |
  |---|---|---|
  | Japanese severity vocabulary and handling-priority model (round 30) | `knowledge/japanese-severity-vocabulary-and-impact-model.md` | S046, S047 (S041) — public primary, opened 2026-10-25 |

  | id | topic | status | entry | sources | next |
  |---|---|---|---|---|---|
  | F14 | Japanese severity vocabulary and the handling-priority model | admitted | knowledge/japanese-severity-vocabulary-and-impact-model.md | S046, S047, S041 | Keep each 深刻度 band label attached to the CVSS version that produced it (v2 bands survive beside v3); JVN translates CVSS base scores into Japanese vocabulary rather than scoring independently, so derive handling priority from the P-guideline steps, not from the label alone. |

  [r30 amendment, appended 2026-10-25] The parenthetical above records the round-26 frontier
  state and is retained as history, not rewritten (R9): at round 30 the frontier stands at
  **14/14 admitted** — F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round
  26, F12 at round 28, F13 at round 29, F14 at round 30. The 0/18 sentence is untouched: the
  lost-domain denominator still holds 0 of 18 surfaces present, and the frontier count stays
  outside it.
  ```

## Files changed
- `corpus/README.md` (append only; 264 → 291 lines).

## Risks / notes
- The knowledge entry `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` and the round-30 SOURCES rows (S046/S047) are owned by other wave seats; this README append references them per the assigned wording and was verified against the byte state at measurement time (pre-append sha256 above). If those seats' deliverables differ from the claim predicate, the L1 gate will catch it via the C2 counter commands — this seat wrote only the README append.
- No tools installed (no install needed); no commands contacted any live bounty target.

## Blockers
None.
