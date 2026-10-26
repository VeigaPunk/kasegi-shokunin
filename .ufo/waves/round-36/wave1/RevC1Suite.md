# RevC1Suite — round 36, wave 1

Seat item: review the drafted `corpus/instruments/r36-closure.sh` (from ExecC1SuiteBuild) against
export-mode purity (no worktree reads), structural (not file-wide literal) E1/E3/E7 checks,
`bash -n` cleanliness, cd-prefix, absence of hardcoded /tmp, TMPDIR honouring, kill-rule clauses
(no count-zero escape). Run `bash -n` and the plain run's refusal path on a scratch copy; do not
modify the lane. Defect list (severity) + verdict (ADMIT / REFUSE with repair paths).

## Bytes reviewed

Two digests saw batteries:

- `76273416f7a6668a702eadf5a6c03b80ae87ad4793f652880303fcb7f8230323` (817 ln) — the builder's
  announced "frozen" bytes; superseded the same hour.
- **`4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (894 ln, 755 mode) — the
  bytes actually committed at lane `2c26a97e` as `corpus/instruments/r36-closure.sh`; still
  identical at lane HEAD `e9c57c43` at review time. All verdicts below are against these bytes.**

Freeze history observed: ff616adc (737) → 77a96185 (746) → a6c1c922 (767) → dc5208fa (774) →
76273416 (817, announced FROZEN) → d1f3f32a (854) → 4db1ae70 (894, committed). The announced freeze
did not hold; the committed digest is the only one that matters and is the one reviewed.

Scratch root: `/fast/scratch/kasegi-r36-RevC1Suite-hold/` (secondary hold outside the swept seat
root; deleted before yield, together with `/fast/scratch/hyaku/kasegi-r36/RevC1Suite/`). LSP
device: no server answered for a bash-only file — text/execution evidence only.

## Criteria verdicts (committed bytes 4db1ae70)

| criterion | verdict | evidence |
|---|---|---|
| `bash -n` | PASS | whole-file `bash -n` exit 0 |
| export-mode purity | PASS (documented live limbs) | plain run refuses: `bash r36-closure.sh` → exit 2 "refusing to run against the live worktree" (measured); every file check `cd "$tree"`-scoped (E1/E2/E3/E5/E7/E8) or git `-C`-ref-scoped (E4/E6/E9); only non-export reads are ref-scoped git object reads against `$LANE` (archive, rev-parse, cat-file -e, merge-base --is-ancestor, ls-tree, ls-files) plus E9's inherently-live quiescence limbs, all documented in the header. E4's `tracked-index` (`git ls-files`) limb is live-by-construction and conjunctive with the authoritative `ls-tree -r <ref>` limb — on the base-export run it read 1 while `tracked-ref` read 0 and the conjunction stayed open (safe direction; measured) |
| refusal path | PASS | no args → 2; unknown arg → 2; `--export-ref` without value → 2; unresolvable ref → 2; `--work` inside the lane → 2 with **no filesystem trace** (guard precedes mkdir; measured against `$LANE/.ufo/waves/round-36/revc1-probe-wd`) |
| structural E1 | PASS | hash extraction scoped to the LAST `^#{1,4} .*Round[- ]?36` block (`e1_final_hashes` awk), `[Ff]inal lane commit` line ±4 lines, 40-hex tokens split on non-hex runs (64-hex digests not misread); gates `placeholders=0 ∧ lane-hash-markers=0 ∧ round36-section=1 ∧ total≥1 ∧ bound=total`. Attacks: round-36 section with no final-commit line → open (`round36-final-lane-commits=0`); binds HEAD → closed; binds orphan hash unresolvable in the audited repo → open (`bound<total`). Selftest mutant `history-only` (final-commit line outside any round-36 heading) rejected |
| structural E3 | PASS | `e3_registry_rows` awk counts only first-cell exact-basename table rows inside a `## …Gates & probes registry…` section (per-round "registry addition" headings also match, correctly). Attacks: both rows under `## Cited paths` → 0/0 open; rows inside the registry → 1/1 closed. Selftest mutants: inexact basename (`r-defect-closure.sh`), mention-not-row, rows-outside-registry — all rejected |
| structural E7 | PASS | third-column row-anchored `^\| R[0-9]+ \|[^|]*\|\s*supersedes R2[23]($|[^0-9])`; prose negation on a row-less tree → open; proper R-id row → closed; `[^0-9]` guard blocks `R220`-class overmatch |
| hardcoded /tmp | PASS | `grep -n '/tmp'` → only the header prose "honouring TMPDIR" |
| TMPDIR honouring | PASS | auto work dir via `mktemp -d -t`; with unwritable `TMPDIR` → die exit 2 ("cannot create a work dir"); with writable `TMPDIR` → created and removed under it, zero residue in `$TMPDIR` and `/tmp` |
| cd-prefix | PASS | every check's first filesystem action is `( cd "$tree" || { printf 'tree-unreadable'; … }` or `git -C "$LANE"`; no check reads a path outside `$tree`/ref-scoped git |
| kill-rule / count-zero escapes | PASS | `run_suite_report` requires exactly 9 `^E[1-9] payload=` lines and `counted == k`; a check that dies with empty output still emits its `closed=0` line; `selftest` increments `CASES` inside each case (skipped case → `problem=cases=N expected=9`), the judge requires 9 `verdict=pass` case lines whose `mutants=ok/n` are matched by exactly n detail lines with ok `rejected=1` (`mutants=0/0` forgery rejected), and four forgeries (summary-only, cases-lines-only, failed-cases+summary, detail-free all-pass) are all rejected (measured) |
| claim limbs, reproduced | PASS | base export `3266c99` → `closed=0/9 exit=1`; judged export `0aee0ef` → `closed=3/9 exit=1` (<9/9); landed tree at `2c26a97e` via `--lane <scratch clone>` → **`closed=9/9 exit=0`**; `--selftest` on the same tree → **`cases=9 failures=0 exit=0`** (24/24 mutants rejected with limb attribution, four forgeries rejected) |
| lane untouched | PASS | `git status --porcelain` byte-identical before/after the whole battery; suite uses `git --no-optional-locks status` (no `.git/index.lock` churn); exports/attacks all in scratch |

## Defect list

**D-Rev-1 (Major, claim-relevant) — E8 accepts a negation mention; "correction recorded" is not
discriminated from "correction not made".** `check_e8` body (`r36-closure.sh:427` in the committed
bytes): `m36=$(grep -cF -- 'M36' corpus/lessons/round-36.md)`. Attack fixture (scratch clone of the
judged export delivered as a fixture git repo via `--lane`, stale line removed from the round-35
lesson): a round-36 lesson reading "…no M36 rows minted; source-recheck unaffected…" plus a
`source-recheck` mention closes E8 (`m36-rows=1,names-corrected-line=1,stale-line=0 → closed=1`) —
indistinguishable from the real-shape control carrying an actual `M36-1` row (also `closed=1`).
The selftest's four E8 mutants do not cover this shape, so no committed fixture proves E8
discriminates. Under the frozen C1 kill rule ("any single E-check's fixture proves the check can
pass while its defect is present") this is the r35 F-5 check-vs-own-text class on the claim's own
evidence instrument. Reproduced on the committed bytes.
**Repair (one line + one mutant):** `m36=$(grep -cE -- '(^|[^0-9A-Za-z])M36-[0-9]+([^0-9]|$)'
corpus/lessons/round-36.md 2>/dev/null)` (id-anchored; row-anchored `^\|?.*M36-[0-9]` preferred to
also survive an id-shaped negation), and add a selftest mutant `E8-negation` (lesson "no M36 rows
minted" + source-recheck mention + clean round-35 lesson) expected rejected with limb
`m36-rows=0`. The real lesson at `2c26a97e` carries four `M36-1..4` rows, so the repair does not
move the green reading.

No other defect found in the reviewed criteria. Notes (not defects): E4's `tracked-index` limb and
E9's limbs are live-by-construction and documented; E1 accepts any 40-hex token on the bound line
(fail-closed — it must resolve and be an ancestor); E7's third-column anchor would accept a
semantically nonsensical real row (beyond a text instrument); `suite problem=self-report` shape
matches the r35 `report_ok` rule.

## Filing-order notes for the L1 (from the measured E9 limbs)

1. `scratch-seat-dirs` counted 9 live seat dirs under `/fast/scratch/hyaku/kasegi-r36/` during my
   battery — every seat (mine included) must remove its dir before the final counting run.
2. `head-match` requires the run's `--export-ref` to equal live HEAD: pass the final hash
   explicitly, and make the counting run the last lane-touching action.
3. `status-dirty` was 1–19 during the wave; the final run needs the quiescent tree.

## Incidents (environmental, not suite defects)

- My seat scratch dir `/fast/scratch/hyaku/kasegi-r36/RevC1Suite/` was deleted twice by an
  unidentified peer mid-review (builder denies; their removal inventory is self-scoped and checks
  out). Evidence was re-based in the hold area; no verdict depends on the lost copies.
- The announced byte freeze did not hold (two post-freeze edits before the commit landed); the
  verdict is pinned to the committed digest `4db1ae70…`.

Tooling installs: none (stock git/bash/coreutils only).

## Verdict

**REFUSE — one repair path, everything else ADMIT-quality.** Land the D-Rev-1 repair (E8
id-anchored grep + `E8-negation` selftest mutant) as an erratum commit or amend before filing;
re-run the four counting commands afterwards. Every other reviewed criterion passes on the
committed bytes, and all four frozen C1 counting-command limbs reproduce exactly (0/9 base,
3/9 judged, 9/9 landed tree, cases=9 failures=0). If the repair lands post-claims-freeze, the
digest move is contract-relevant: the C1 after-state names this instrument, so the SKILL.md
registry row and the lesson should carry the new digest.

## Addendum (post-yield, builder response)

ExecC1SuiteBuild reproduced D-Rev-1 independently and built a tested v2 candidate:
sha256 `7f54f0e50023f5320fc889ffe44797c251db7eca849424df63f2eeff690467b7` (898 lines, `bash -n`
clean, two hunks vs `4db1ae70`: the id-anchored `grep -cE` exactly as repaired above plus a
`m36-negated` selftest mutant). Builder-measured limbs on v2: base 0/9, judged 3/9, head `a23dc47`
8/9 (only E9, live), selftest cases=9 failures=1 (only E9's live positive), E8 mutants 5/5 with
`m36-negated rejected=1`, four forgeries rejected; full diff in the builder's receipt
§ "v2 candidate — E8 row-id". v2 is recorded but unlanded: five seats' receipts pin `4db1ae70`,
so adoption is the L1's call. My verdict stands as stated: REFUSE pending that repair (or an
equivalent) landing, or an explicit L1 acceptance of the disclosed residue; the addendum closes
the "repair not yet executed" gap to "repair exists and is measured by its author, unlanded".
My scratch (seat dir + hold area) is fully removed — the E9 seat-dir condition is one seat lighter.

## Resolution (final)

KasegiR36 filed round 36 with the suite at `4db1ae70` (C1 held: `closed=9/9 exit=0` at `274fa9ae`,
base 0/9, judged 3/9, selftest failures=0) and recorded the disclosed kill-rule-hit/limit matrix
(E8 two tokens included, with the full CritC1Kill set) as the round-37 backlog — the explicit
acceptance my REFUSE was conditioned on. **The conditional REFUSE is discharged on that record;
the seat closes with the finding filed as round-37 backlog**, v2 `7f54f0e5…` preserved unlanded
behind E1 `on-head` (if landed, the registry row and lesson must move the digest with it).
