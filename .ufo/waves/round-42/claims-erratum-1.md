# kasegi round-42 claims erratum 1 — scope clarifications (pre-data, pre-scoring)

Frozen claims: `.ufo/waves/round-42/claims.json` (committed `0566bd66e93d429b2df8b6751cf10cbdc391e79b`).
These errata CLARIFY ambiguous wording and repair one self-contradictory frozen number; no predicate is
narrowed, no target is moved, and no seat had scored any claim when this was written. Found via wave-1
seat receipts (`wave1/ConnWave2Seed.txt` items 1, 8, 9, 46-49; `wave1/RevRegistry.md` F1-F3;
`wave1/ScoutF25Lead.facts.txt` row-id suggestion).

- **E1 — C2 registry counting value.** The C2 predicate requires "one new registry row S064 (mined) +
  at least one rejected screened row S065+", i.e. `64+R`; the counting command's printed expectation
  `63 -> 64` contradicts it (a rejected row still matches the row-counting grep — the lane already
  carries 10 rejected rows inside its 63). The landed scout screen recorded TWO rejects (S065 = OSV
  schema, S066 = NVD API 2.0 schema), so the concrete after-value is **66**: the command reads
  `63 -> 66` where 66 = 63 + S064 (mined) + S065 + S066 (rejected). The mined-status probe stays
  `0 -> 1` (only S064 is `mined`); the rejected rows are probed by their `rejected` status cells and
  the Gate's URL/date/quote/flip record.

- **E2 — J11 (F-CORR) duplication semantics.** The frozen wording "no `Correction (round <n>)` block is
  duplicated verbatim" is literally false at Y by construction: the committed r41 duplication (D-r41-1,
  SCORECARD.md ~L1602-1605 = ~L1607-1610) is KEPT as history (append-only; it is never rewritten). J11's
  positive limb therefore reads: every verbatim-duplicated `Correction (round <n>)` line-block per file
  is either absent OR is named line-range-exactly by an appended `Correction-dedup (round 42)` marker;
  and its replay limb re-executes a synthetic duplication carrying NO marker and requires rejection
  (`rejected=1`). The committed r41 duplicated state is "detected, not silently passed" precisely
  because J11 fails without the marker.

- **E3 — J3 (F-TABLE) one-row-per-basename scope.** A literal "no instrument basename appears in more
  than one row" fails on pre-existing documented pairs that are not the defect: `r36-closure.sh`
  carries two legitimate Round-36 rows (SKILL.md L1111/L1113, distinct verdict-map cells) and
  `anchorcheck.py` carries two rows (L982/L1041, the second a documented round-29 state). J3's
  uniqueness limb is scoped to `r*-closure.sh` basenames exclusive of those declared pairs, which the
  suite names in its own declaration list; the contiguity limb (no blank line between a table header
  separator and its rows) and the bare-pipe / leading-whitespace cell limbs apply to all
  Gates-and-probes rows. Legacy rows' escaped `\|` cells (e.g. L1111 verdict maps) are ACCEPTED — the
  bare-pipe limb rejects only unescaped pipes that change a row's cell count. The repair itself is
  D-r41-3: remove the blank line after the Round-40 separator and the duplicate `r40-closure.sh` row.

- **E4 — J5/J13 scan-root resolution.** J5's replay stray sits outside the suite-configured scratch root
  but inside its observed parent (a sibling `kasegi-r4[0-9]*`-named dir beside the configured root), per
  ScoutDefeatsR41 D05's resolution — a truly host-global stray is unroutable and out of scope. J13's
  quiescence scan is rooted at the run's `--scratch-root` argument: at receipt time the L1 runs the
  suite with `--scratch-root /fast/scratch/hyaku/kasegi-r42`, so any leftover seat dir under that
  prefix (or under the parent family pattern `kasegi-r4[0-9]*`) is a red stray and must be cleaned
  before the receipt run — that cleanup IS the check's job, not a bypass.

- **E5 — J12 scope confirmation.** J12 guards corpus-path deletions and `density.py` byte-identity only
  (corpus/ paths). The F-TABLE repair legitimately DELETES lines from SKILL.md (the stray blank line and
  the duplicate row); SKILL.md is outside corpus/ so J12 does not port the retired r41 `skdel==0`
  clause. The density-metric side effect (fewer path citations in SKILL.md) is a consequence of defect
  repair, disclosed in the report — the owned-axis guard is `density.py` byte-identical, which holds.
