# R44Scout6 — considered proposals against frozen C1 and C2

Read-only. No production edit, no commit, no action on a proposal.

## Finding

No unimplemented considerthese proposal is a current item that meets frozen C1 or frozen C2.

C1 stays at 8 unresolved routed defects: the named counter `corpus/instruments/r44-routed-defects.py` is absent, and no committed `Correction (round 44)` exists. C2 stays at 25 admitted frontier rows, 68 source rows, and 62 knowledge entries on the committed tree. `F26` / `S069` / `Google Cloud VRP` occur in no committed proposal file.

## Committed baseline

- HEAD `66314015122b9aa32dc40f2f1815df56624c26d1` — `round-44: freeze claims and validated wave` (2026-10-28 15:47:51 -0300).
- Named freeze `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` is that commit's parent (`do-nothing.txt` line 2).
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a HEAD -- corpus SHONEN.md SCORECARD.md` printed no output. Corpus bytes at HEAD are the freeze bytes. The only commit after the named freeze adds `.ufo/waves/round-44/` control files.

Commands below were run against `git show HEAD:<path>` unless marked worktree.

## C1 — committed

| command | result |
|---|---|
| `git show HEAD:corpus/lessons/round-43-verifier-spotcheck.md \| grep -Ec '^6\. Routed defects\|^\[0-9\]+\\. \\*\\*'` | `8` |
| `git cat-file -e HEAD:corpus/instruments/r44-routed-defects.py` | absent (same path absent on disk) |
| `git grep -c 'Correction (round 44)' HEAD -- corpus SCORECARD.md SHONEN.md LOG.md` | no stdout, exit 1 |

The eight items are `corpus/lessons/round-43-verifier-spotcheck.md:101-108` under the heading at line 97. One numeral was re-counted: `corpus/lessons/round-43.md:90` and `:101` still say `29-character prefix`; `python3 -c 'print(len("c6ae07c6a541e0e96d0040afb6"))'` prints `26`.

The claims counter for this axis is `python3 corpus/instruments/r44-routed-defects.py` (`claims.json:14`). That file is not in the tree, so the after-state "0 of those same 8" is not reached. `.ufo/waves/round-44/controls/c1-do-nothing.txt`, named at `claims.json:15`, is not in the tree; the measured control is `.ufo/waves/round-44/controls/do-nothing.txt:4-7`.

## C2 — committed

| command | result |
|---|---|
| `git show HEAD:corpus/README.md \| grep -cE '^\| F[0-9]+ \| .* \| admitted \|'` (control regex, `do-nothing.txt:10`) | `25` |
| `git show HEAD:corpus/README.md \| grep -cE '^\| F[0-9]+ \| admitted \|'` (`claims.json:23` literal) | `0` |
| `git show HEAD:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | `68` |
| `git ls-tree --name-only HEAD:corpus/knowledge \| grep -c '\.md$'` | `62` |
| `git grep -n -E 'F26\|S069\|Google Cloud VRP' HEAD -- considerthese corpus/knowledge/considerthese-proposals-ledger.md` | no match |
| `git grep -n F26 HEAD -- corpus/README.md` | `F26 absent at HEAD` |

The claims.json frontier pattern asks for `admitted` in column 2. Committed rows put the topic there and `admitted` in column 3 (`corpus/README.md:202` is `| F01 | CVSS v4.0 severity and vector semantics | admitted |`). That literal therefore prints 0 on the same blob the control regex counts as 25. `.ufo/waves/round-44/controls/c2-do-nothing.txt` (`claims.json:24`) is not in the tree.

## Proposals inspected

Reflections on disk: `considerthese/2026-10-19.md` through `considerthese/2026-10-26.md` (eight files). Ledger: `corpus/knowledge/considerthese-proposals-ledger.md`. Last real heading is `## Round-42 dispositions` at line 134. `git show HEAD:…ledger.md | grep -c '^## Round-43 dispositions'` → `0`. `grep -c '^## Round-42 dispositions'` → `1`.

### 2026-10-26 proposals (current reflection)

| # | text | committed status | C1/C2 fit |
|---|---|---|---|
| 1 | `considerthese/2026-10-26.md:29` distance to next score | Landed. Ledger line 138. Block at `SCORECARD.md:1532`. | Already landed. Moves neither the eight defects nor F26. |
| 2 | `:30` one end-to-end domain task; H1 or Immunefi disclosure; price through F13/F17/F18; rebuild a claim checker | Checker half is in HEAD: `corpus/instruments/claim-package-check.py` and `corpus/knowledge/claim-package-gate.md` (`git cat-file -e` present). Both absent at round-43 base `ab98fac9dce87130bc4f66de89e30650d63943dc`. Lesson `corpus/lessons/round-43.md:134-144` records `landed (r43)` and leaves open the lost `ops/claim-check.mjs` parity plus three operator gates. Ledger line 139 still says the checker is absent, because that section measures `ab98fac9` and no Round-43 section was appended. `SHONEN.md:287` box 2 is still `[~]` (no submission; none claimable). | The open remainder is a live domain task and operator gates. It is outside the eight spotcheck items, and the proposal names no new frontier row. |
| 3 | `:31` quiescence gate before `complete` | Landed. Ledger line 140. | Already landed. |
| 4 | `:32` cap or externalise `.ufo/` wave evidence (releases, LFS, or prune) | Open, operator-owned. Ledger line 141. | Outside C1 item 5. That item (`round-43-verifier-spotcheck.md:105`) is an empty `names=` in `.ufo/waves/round-43/w1-REGISTRY.txt`, a selftest receipt with no `export-ref`, and an untracked `all-gates.at-Y.txt.tmp`. |
| 5 | `:33` land the owed F18 `PROVINCE.md` amendment | Landed r36. Ledger line 142. | Already landed. The item is F18. |
| 6 | `:34` second daily run, per-round digest, or weekly cloud pass | Open, operator-owned. Ledger line 143. `considerthese/` still has the eight daily files and none later. | Outside both frozen after-states. |
| 7 | `:35` proposal-status ledger | Sections through round 42 are in the ledger. Round-43 section count is 0. R31 (`corpus/QUALITY.md:278`) requires old→new in the lesson and in the ledger for a proposal the round touches. Round 43 touched proposal 2 in `corpus/lessons/round-43.md:131-149` only. | Unimplemented upkeep. The C1 counter and the C2 counts do not read this section. |

### 2026-10-25 rows that the base table still labels open

The base table (`ledger` lines 11-16) is append-only. Later committed records supersede two of its `open` cells:

- Proposal 2, base line 12, still says `open`. Round-31 line 28 records mined → `corpus/instruments/score-gap.py`.
- Proposal 5, line 15, mined round 29 → `corpus/QUALITY.md:89` R15 (runnable closure checks). Round-31 line 32 restates mined. This is the closest C1-shaped proposal. It names D24-* and R25-* defects from 2026-10-25 (`considerthese/2026-10-25.md:70-74`). It does not name the round-43 eight, and it is not the missing `r44-routed-defects.py`.
- Proposal 6, base line 16, still says `open`. `corpus/QUALITY.md:227` R23 and `:250` R27 record the event-driven cadence landing.

Proposal 3 (line 13) is partially landed: the severity-tables plank is F13; the SHONEN box 2 remainder is the same open remainder as 2026-10-26 proposal 2.

`git grep` of committed `considerthese/` and the ledger for `F26`, `S069`, and `Google Cloud VRP` matched nothing, including the 2026-10-19 through 2026-10-24 reflections.

## Do-nothing discrimination

On committed HEAD the frozen before-state still holds: 8 routed items, no `Correction (round 44)`, counter script absent, frontier control-regex 25, sources 68, knowledge 62. Inspecting proposals does not move either after-state.

`do-nothing.txt:16` records `python3 corpus/instruments/claim-package-check.py --selftest => selftest cases=10 failures=0`. This seat did not re-run it. That result is the round-43 checker (proposal 2's landed half), which is already in the freeze corpus. It is not an F26 admission and not a closure of the eight defects.

The claims.json frontier literal prints 0 on the committed README. It also printed 0 on the dirty worktree README below, whose F26 row uses the same column shape as F01–F25. The control regex is the command that returns 25 at HEAD.

## Worktree drift at measurement time

`git status --porcelain` against HEAD `6631401` showed uncommitted production paths. This seat did not write them and did not revert them.

| path | status | what the diff contains |
|---|---|---|
| `corpus/README.md` | `M` +19 | `## Round-44 admission` and an F26 row (worktree lines 614-630 at read time) |
| `corpus/SOURCES.md` | `M` +2 | S069 `mined` tier A and S070 `rejected` tier C |
| `PROVINCE.md` | `M` +2 | `[r44 Frontier amendment]` for F26 / S069 |
| `corpus/instruments/knowledge-expected.txt` | `M` +1 | the new knowledge basename |
| `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` | `??` | untracked entry; no line matches `considerthese` or `proposal` |
| `corpus/source-snapshots/round-44/S069.txt`, `manifest.json` | `??` | untracked capture |

Worktree counters at that moment:

- control frontier regex → `26`
- `claims.json:23` frontier regex → `0`
- sources regex → `70` (68 committed + S069 + S070)
- `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `63` (62 committed + the untracked entry)

Those worktree numbers are not a landing: the paths are absent from HEAD `6631401`. They are also not a considered proposal: committed `considerthese/` and the ledger contain none of `F26`, `S069`, or `Google Cloud VRP`, and the untracked entry does not cite a proposal. C2's kill rule (`claims.json:21`) requires F26, its captured source, the knowledge entry, and the registry row to land, plus a non-author admit/reject gate.

## Limitations

- The eight defect mechanisms were not re-executed. Measured facts are the frozen count of 8, the missing counter, the missing `Correction (round 44)`, and the still-present `29-character` sentences at `round-43.md:90` and `:101`.
- Base-table cells that still say `open` for 2026-10-25 proposals 2 and 6 are stale relative to the round-31 section and to QUALITY R23/R27. The status column above follows those later committed records.
- `HYAKU_SCRATCH` was unset. Scratch used `/fast/scratch/hyaku/kasegi-r44/R44Scout6` (root named in earlier lane logs). Removed on exit (`REMOVE_OK`). Parent directory left in place.
- No tool installed. `/home/vgpnk/.omp/agent/RULES.md` read. Pacman not invoked.
- No git/jj index change and no commit by this seat.

## Action

None.
