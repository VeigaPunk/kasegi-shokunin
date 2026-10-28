# R44W2Crit02 — counter-defect attack on C2 (frozen counter reads 0/0; round measures with a table-aware counter)

Seat: R44W2Crit02 (leaf, falsify wave, round 44 attempt 2, wave 2). Read-only except this Report.
Attack tree: commit `8063547d0ce647d6f9eafc3c8d0a502616685218`. Frozen base: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` (pinned in `.ufo/waves/round-44/controls/c2-do-nothing.txt:2`). Freeze commit: `6631401`.
Scratch used and removed: `/fast/scratch/hyaku/kasegi-r44/R44W2Crit02/` (base and after trees extracted read-only via `git archive <hash> | tar -x -C`).

## 0. The frozen predicate sentence and target value (quoted, unedited)

From `.ufo/waves/round-44/claims.json`, claim C2 (`axis: coverage`), frozen 2026-10-28:

- `before`: "25 admitted public-practice frontier rows (F01-F25), 68 SOURCES registry rows and 62 knowledge entries; one source-grounded frontier move is absent."
- `after` (the target): "26 admitted frontier rows, at least one newly opened tier-A source row cited by a new knowledge entry, 63 knowledge entries, plus a recorded reject and non-author admit/reject spot-check; SOURCES census validates exit 0."
- Target value: **26 admitted frontier rows** (from a frozen base of 25), with SOURCES and knowledge legs 68→(unstated)/62→63.
- Frozen `counter` string, leg 1 (the disputed one): `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` (legs 2–3: SOURCES grep, knowledge `find | wc -l`).
- Frozen `kill_rule`: "A do-nothing replay cannot reach F26 or the new sourced entry; no coverage credit unless F26, its captured source, knowledge entry and registry row all land and the non-author gate agrees."

## 1. Verified facts (all commands run by this seat, not taken from receipts)

| # | Probe | Command (cwd = scratch tree) | Result |
|---|---|---|---|
| 1 | Frozen leg 1 at base | `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` in base export | `0`, exit=1 |
| 2 | Frozen leg 1 at attack tree | same in after export | `0`, exit=1 |
| 3 | Frozen leg 2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | base `68`, after `70` |
| 4 | Frozen leg 3 | `find corpus/knowledge -maxdepth 1 -name '*.md' \| wc -l` | base `62`, after `63` |
| 5 | Table-aware counter at base | `python3 corpus/instruments/r44-frontier-count.py --root <base>` | `frontier rows=25 admitted=25` |
| 6 | Table-aware counter at attack tree | same `--root <after> --ids` | `frontier rows=26 admitted=26`, ids F01…F26 contiguous |
| 7 | Why leg 1 is dead | `grep -n -m2 '^| id\|^| F01' corpus/README.md` at base | line 200 header `\| id \| topic \| status \| entry \| sources \| next \|` — status is the **third** cell; the frozen regex demands it in the **second** cell |
| 8 | F26 landing shape | `git diff 6631401 8063547 -- corpus/README.md` | original 25-row table byte-unchanged; F26 appended in a new section with its own table (after README.md:628) |
| 9 | Claims frozen unedited | `git diff 6631401 8063547 -- .ufo/waves/round-44/claims.json` | empty (byte-identical) |
| 10 | Audit's "double-escaped" variant | `grep -cE '^\\| F[0-9]+ \\| admitted \\|' corpus/README.md` | base `612`, after `632` = whole-file line counts (`wc -l` gives 612/632), reproducing `c2-counter-audit.txt` exactly |
| 11 | Wideness probe on replacement | status-cell census over all `\| F\d+ \|` rows in after tree | `26 admitted`, no other status, no stray F-rows outside tables (rows==admitted in both worlds) |

Committed controls corroborate every number above: `c2-frozen-counter-replay.txt` (0/68/62 base, 0/70/63 worktree), `c2-counter-audit.txt` (frozen 0/0, control 612/632, diagnostic 25/26), `c2-frontier-counter.txt` (base `--expect 26` → `verdict=SHORT exit=1`; after → exit=0).

## 2. Strongest argument that this is a hidden TARGET change (steelman)

1. **The counter field is the only committed operationalization, and it was swapped post-freeze.** claims.json's `counter` string is the measurement contract frozen with the claim. Its F-leg defines "admitted frontier row" as *status in cell 2*; the round's operative instrument (`r44-frontier-count.py`) measures *status in cell 3, whitespace-stripped, whole-file scope*. Those are different predicates as implemented. Under the frozen instrument the after-state is not merely unmet — it is **unreachable in any world** (leg 1 reads 0 at base and 0 after, exit=1 both). So the round's "26" exists only in units of an instrument that did not exist at freeze; the frozen claim can never pass as written, and the round replaced the measure rather than the world. If the counter string is the contract, this is a post-freeze contract amendment — a target change in the evidence layer even if the prose layer is unchanged.
2. **The frozen before-value was never measurable by the frozen counter.** Leg 1 reads 0 at base, so the `before` cell's "25 admitted … rows" was frozen in units of an instrument that had never been run and could never produce it. The 25 first appears in round-44 controls via a *third* regex variant ("diagnostic"), chosen by the author after seeing the data. That is post-hoc instrument selection — the same unbacked-numeral defect class the round claims to fix (routed defect 1: `closed=13/19` unbacked; defect 3: "a numeric claim needs its counting command").
3. **The round could not reproduce its own frozen instrument.** `c2-do-nothing.txt` admits the first replay attempt double-escaped the regex and printed 612 (a whole-file line count, verified in probe 10). Three regexes circulated (frozen 0, control 612/632, diagnostic 25/26); the story of 25→26 rests entirely on the third, which is not in the frozen claim.
4. **Reachability depends on a post-freeze scope choice.** The original frontier table still has 25 rows; F26 lives in an appended second table with a different header (`| id | topic | status | entry | sources | next |`). Only because the replacement counter scans the whole file (as the frozen grep also did) does the appended row count toward "26 admitted frontier rows". A same-table counter would read 25 after. The kill rule's "cannot reach F26" is thus decided by an instrument-scope decision made after freeze.

## 3. Strongest rebuttal (counter fix, not target change)

1. **The replacement reproduces the frozen numbers exactly where they exist.** At the frozen base the table-aware counter reads `rows=25 admitted=25` with ids F01–F25 (probe 5) — byte-for-byte the frozen `before` cell (25, F01-F25). Its only movement is the claimed +1 (26, F26). A hidden target change leaves a signature somewhere — base ≠ 25, extra rows counted, different file or scope, non-admitted rows admitted. Probe 11 shows none: every F-row in both worlds has status exactly `admitted`; rows==admitted; ids contiguous. There is no world in which the new instrument and the frozen prose disagree.
2. **The frozen F-leg is not a stricter measure of the same predicate — it measures nothing.** The base table's header (README.md:200 at `5ab3a60`) puts status in cell 3; the frozen regex demands cell 2. It reads 0 in *every* world (probes 1–2), so it cannot separate a do-nothing replay from a real F26 landing: both read 0, both exit 1. A claim whose counter can neither pass nor fail has no kill rule — the opposite of the evidence discipline the round must uphold. Repairing it is the only way to make the frozen kill rule decidable.
3. **The repair is minimal and the untouched legs corroborate it.** Two of the three frozen legs work and are preserved verbatim: SOURCES 68→70 (matches frozen before 68), knowledge 62→63 (matches 62→63). A deliberate target move would not leave two of three legs byte-identical and in exact agreement with the frozen before-cell.
4. **The swap is documented, not hidden — the append-only discipline is respected.** claims.json is byte-unchanged freeze→attack (probe 9); the defect is recorded in committed controls with the exact decoded command, the pinned base hash and both outputs (`c2-frozen-counter-replay.txt`, `c2-counter-audit.txt`, which closes with "Frozen predicates exactly as recorded in claims.json and controls/do-nothing.txt were not modified"); the replacement is a separate registered instrument whose docstring states the same-predicate claim and cites the falsifying control. The target artifact moved only by the sanctioned append: the original table and its 25 rows are byte-unchanged (probe 8), and the README amendment explicitly retains the 25/25 parenthetical as history.
5. **On the self-referential-validation prong:** the do-nothing control does not rest on the new counter alone. The frozen counter's two working legs independently separate base from after (68/62 vs 70/63), the base hash is pinned, and `c2-counter-audit.txt` runs all three variants side by side so the discrepancy is auditable rather than buried.

## 4. Which the evidence supports

**The counter-fix reading.** The decisive fact is probe 5: at the frozen base the replacement counter reads exactly the frozen before-value (25 admitted, F01–F25), and its only delta is the claimed +1 with F26's status cell exactly `admitted`. A hidden target change has no surviving signature in any probe. The frozen F-leg is structurally incapable (status is cell 3 in the actual table; the regex demands cell 2), reads 0 in every world, and would have made C2's kill rule undecidable. The round documented the defect, kept the frozen string unedited, and added a separate instrument — the repair pattern its own routed defects (1, 3) demand.

**Residual genuine defects (stated plainly, no inflation):**
- **Freeze-time validation gap (real, process-level).** C2 was frozen with an F-leg that had never been run against the base: the `before` cell (25) was unbacked by the frozen counter at freeze time, and the first post-freeze replay attempt mis-implemented the regex (612). The defect was discovered after freeze, not prevented. Lesson worth routing: every counter leg must be executed against the frozen base *before* the claim freezes.
- **The frozen counter string is now dead weight inside the live claims file.** Anyone replaying claims.json verbatim gets 0/70/63 — not 25→26 — and the file gives no pointer to the operative instrument. The divergence lives only in controls and the instrument docstring. This is a documented repair, not a hidden target move, but the claims file itself is internally inconsistent with its own receipt.

## 5. Tooling

No tools installed or upgraded. Stock `git`, `grep`, `find`, `wc`, `awk`, `python3` only; no pacman, no network installs, no writes outside this Report and scratch.

## 6. Limitations

- I did not audit the SOURCES census exit-0 leg, the non-author admit/reject spot-check, or the registry emitter (`wave-registry.py`) — out of scope for this item.
- I verified the counter layer only; I did not re-verify the substantive truth of F26's source capture (S069) beyond confirming the row, the knowledge entry count and the SOURCES delta.
- Scratch `/fast/scratch/hyaku/kasegi-r44/R44W2Crit02/` is removed at yield; nothing was written under /tmp or outside the lane.
