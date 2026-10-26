# ExecRegressionBase — before-control replay at the round-36 base (round 36)

Seat: `ExecRegressionBase` (executor, leaf). Judged axes: `depth:verifiability`, `coverage`.
Milestone: round-36. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only; the only lane
write is this receipt). Base commit `cc692008b0cfd58d18275aa6c4aed79620120799` (tree
`c6f1dbec5c8763fbe368abda6d1e575008ff235c`); claims-freeze commit
`b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`; lane HEAD at my read = `b47f2cdf…` (detached).

## 1. Scope and method

Assigned item: replay the two frozen before-controls at the base commit and confirm each value, and
check that every `claims.json` literal is satisfiable at base. Method — all read-only:

1. `git archive cc69200… | tar -x -C $S/base` — the *tracked* base tree, so the replay is against
   committed bytes, not the live (dirty) worktree. Two more exports were taken so each literal has its
   negative control: round-35 base `3266c993…` (`$S/r35base`, 121 MiB) and round-35 judged head
   `0aee0ef1…` (`$S/r35head`, 124 MiB); base export is 126 MiB.
2. Counting commands are the ones frozen in `claims.json` (`counting_commands`), applied from inside the
   export root, plus the narrowest scope that reproduces the frozen value for each key.
3. `py3 corpus/instruments/frontier-recheck-count.py` was run twice at base (identical output).
4. Live-state keys (`worktree_clean`, `scratch_leftovers`) are replayable only as derivations, because a
   worktree/scratch state is not a property of a past commit; both are labelled `MATCH (derived)` below
   with the evidence that fixes the captured value.
5. No mutating git, no lane write, no pacman, no tool install (nothing needed), no subagent, and the
   single permitted read-only labrat probe was not used (no external fact was required).

Byte binding at base (blob id at `cc69200`; lines; sha256 prefix of the export file):

| file | blob | lines | sha256[:16] |
|---|---|---|---|
| `SCORECARD.md` | `a1e366fc56a7e3a986d803d58eef374932e62439` | 1404 | `ed6e931f795c070e` |
| `SKILL.md` | `b1bdf8f914f921b97608be883002fbd39077d0e9` | 1104 | `daeff71be4d0ee99` |
| `corpus/README.md` | `bd77ef45acf7da50d1b7d1feb28eaa2c6528bf55` | 396 | `277f04cedfb06f49` |
| `corpus/SOURCES.md` | `f32225733eb12deca4f18bffb8eb82e9944f9646` | 112 | `0f95a132a69e2708` |
| `corpus/QUALITY.md` | `4b675483f2cec11a6c983702b1cc5053e5731be2` | 250 | `d4f83bb1206f5084` |
| `.ufo/waves/round-34/wave1/L1Integration.md` | `557957a4b359ed25c79c91c829065c084fae0bf2` | 40 | `76f190a003931aee` |
| `.ufo/waves/round-35/wave1-results.json` | `ef2e87c44cb4dea1d9ba88e5d69cbf85259786dd` | 391 | `0d28a45c8386cb63` |
| `.ufo/waves/round-35/claims-erratum-d5.md` | `e0d91cec9ac6781e2bb41dcb2b6fa6ea8430f855` | 262 | `eee0bb579844ad9d` |

`SCORECARD.md`'s base blob equals the blob the sibling `ExecAncestry` seat read at master
(`a1e366fc…`) — the freeze commit touched only `.ufo/waves/round-36/`, so both seats measured one blob.

## 2. `c1-controls/before.txt` — replay table

| # | key | frozen | reproduced at `cc69200` | command (inside the export) | verdict |
|---|---|---|---|---|---|
| 1 | `suite_missing` | `1` | `1` | `ls corpus/instruments/r36-closure.sh` → `No such file or directory`; the base tree has no `.ufo/waves/round-36` and no `r36-closure.sh` (`git ls-tree -r cc69200 -- corpus/instruments` lists `r35-defect-closure.sh`, not `r36-…`) | **MATCH** |
| 2 | `placeholder_filled` | `0` | `0` | `grep -c -F 'filled by the L1' SCORECARD.md` → `0` (grep exit 1) | **MATCH** |
| 3 | `placeholder_angle` | `0` | `0` | `grep -c -F '<LANE_HASH>' SCORECARD.md` → `0` — **only under the `SCORECARD.md` scope**; repo-wide the same token yields 502 lines/89 files (see F1) | **MATCH** (scope pinned) |
| 4 | `r36_registry` | `0` | `0` | `grep -c -F 'r36-closure.sh' SKILL.md` → `0` | **MATCH** |
| 5 | `r35_registry` | `0` | `0` | `grep -c -F 'r35-defect-closure.sh' SKILL.md` → `0`; control that the scope is not too broad: `grep -c -F 'r-defect-closure' SKILL.md` → `4` (one registry row + three prose lines in the round-35 registry addition, `SKILL.md:1093-1104`) | **MATCH** (exact basename required, as the key states) |
| 6 | `worktree_clean` | `0` | `0` (not clean) | derivation: `git log -1 --diff-filter=A --name-status b47f2cd` adds exactly `.ufo/waves/round-36/{c1-controls/before.txt,c2-controls/before.txt,census-before.txt,claims.json}` → those four paths were **untracked** at capture, so `git status --porcelain` was non-empty (`worktree_clean=0`). Live worktree at my read: 9 untracked paths | **MATCH (derived)** |
| 7 | `scratch_leftovers` | `0` | `0` at base time (dir absent) | `/fast/scratch/hyaku/kasegi-r36` did not exist at base; at my read it holds 48 seat dirs (wave in flight), i.e. the key is a *live* measurement, not a base property | **MATCH (derived)** |

## 3. `c2-controls/before.txt` — replay table

| # | key | frozen | reproduced at `cc69200` | command (inside the export) | verdict |
|---|---|---|---|---|---|
| 1 | `frontier` | `18` | `18` | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `18`; ids are exactly `F01…F18` (no `F19`) | **MATCH** |
| 2 | `registry_rows` | `52` | `52` | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `52`; rows run `S001…S052` | **MATCH** |
| 3 | `s053_rows` | `0` | `0` | same regex with `S053` → `0` | **MATCH** |
| 4 | `entries_citing` | `0` | `0` | `grep -rlE '^source: S053 ' corpus/knowledge \| wc -l` → `0` | **MATCH** |
| 5 | `knowledge_entries` | `47` | `47` | `ls corpus/knowledge/*.md \| wc -l` → `47` | **MATCH** |
| 6 | `harness` | `entries=21 pass=21 exit=0` | `entries=21 pass=21 exit=0`, exit `0` | `python3 corpus/instruments/frontier-recheck-count.py` (tail line; run twice, identical; `PASS F01…F18` incl. the two F09/F10/F11 double rows) | **MATCH** |
| 7 | `junk_present` | `1` | `0` for the round-36 twin; `1` only under a "committed c2 junk twin exists in the lineage" reading | `ls .ufo/waves/round-36/c2-controls/junk-f19.md` → absent (the base tree has no `round-36` dir at all); the newest committed twin is `.ufo/waves/round-35/c2-controls/junk-f18.md` (plus round-34 `junk-f17.md`, `junk-checker.py`) | **DIFF / ambiguous** (F6) |

C2's own frozen `before` prose (`claims.json` C2, `before[1]`) says "junk-f19 absent (control not yet
built)", which contradicts the `junk_present=1` key under the plain reading. The value cannot come from
the round-36 twin: that file is still absent at my read, and the freeze commit added only the four
`c1-controls`/`c2-controls`/`census`/`claims` paths. The other six C2 keys reproduce exactly.

## 4. `claims.json` literals — satisfiability at base

"SAT" = the literal is evaluable on base bytes and its base value is the one the frozen `before`/kill
rule implies. "Pre-satisfied" = already true at base (a guard against regression, not a round-36 gain).
"Open" = false at base, so the round-36 after-state must make it true.

| literal (as frozen) | base `cc69200` | `3266c99` (r35 base) | `0aee0ef` (r35 judged head) | status | note |
|---|---|---|---|---|---|
| `grep -c 'filled by the L1' SCORECARD.md` (kill rule: `!= 0` fires) | `0` | `1` (`SCORECARD.md:1240`) | `1` (`:1271`) | **SAT**, pre-satisfied | kill rule does not fire at base and fires at both negative controls — exactly the spot-check D1 shape |
| `grep -c '<LANE_HASH>' SCORECARD.md` | `0` | `0` | `0` | **SAT scoped**, **UNSAT repo-wide** | repo-wide 502 lines / 89 files at base (486 lines in 82 `.ufo/waves` files, 16 lines in 7 files outside it: `LOG.md`, 5 lessons, `r35-defect-closure.sh`) → E1 **must** be `SCORECARD.md`-scoped (F1) |
| `Final lane commit:` line: hash exists and is an ancestor of the exported ref | 2 such lines; `:987-988` → `7963976e…` (round-34, R1), `:1129-1130` → `c1c6a5f8…` (round-35, D1); both `cat-file -e` present and `merge-base --is-ancestor … cc69200` = yes | `:1129` reads `**Final lane commit: the L1 fills this line in the closing commit.**` — no hash at all | same two hashes as base | **SAT** | the hash sits on the line **after** the token, and the round-34 token line already carries `690b69da…` and `9f98488…` inline (both also ancestors) → a same-line regex binds a non-final hash (F3) |
| `Erratum (round 35)` in `SCORECARD.md` (E2 anchor) | `1` (`:1246`) | `0` | `1` | **SAT**, pre-satisfied | discriminates against `3266c99` |
| `201.2` in `SCORECARD.md` | 8 occurrences on 6 lines: `1246, 1250, 1269, 1307, 1312×2, 1314×2` | `0` | `3` lines | **SAT** but **non-discriminating alone** | only `:1246`/`:1250` belong to the erratum; `:1269`, `:1307`, `:1312`, `:1314` are round-35 rows that survive deletion of the erratum sentence (F2) |
| `201.7` in `SCORECARD.md` (the stale figure) | `5` lines | `2` | `4` | **SAT** | also present in rounds-35 rows; pair it with the stale-row marker, not with a bare count |
| `round-34 depth:density row` in `SCORECARD.md` (stale-row bytes) | `1` | `0` | `1` | **SAT**, pre-satisfied | the strongest single limb of E2 |
| `SKILL.md` exact basename `r35-defect-closure.sh` (E3) | `0` | `0` | `0` | **SAT**, open | absent at all three refs — this is the round-35 registration defect E3 closes |
| `SKILL.md` exact basename `r36-closure.sh` (E3) | `0` | `0` | `0` | **SAT**, open | instrument itself absent at base |
| round-35 `wave1-results.json` tracked (E4) | `1` (`git ls-tree -r cc69200 -- .ufo/waves/round-35/wave1-results.json`) | `0` | `0` | **SAT**, pre-satisfied | tracked only from `980aa3d`; untracked at the judged head — the routed "uncommitted round work" defect |
| round-35 results provenance note (E4) | `0` — no `.ufo/waves/round-35/*provenance*`; the only committed note is `.ufo/waves/round-34/wave1-results.json.provenance.md` (107 lines, added at `aa6ad99`) | `0` | `0` | **SAT**, open | E4's two limbs differ at base: tracked=1, provenance=0 (F5) |
| `.ufo/waves/round-35/claims-erratum-d5.md` present (E5) | `1` (13 086 B, 262 lines) | `0` | `1` | **SAT**, pre-satisfied | discriminates against `3266c99` |
| `Correction (round 35)` in `L1Integration.md` (E6) | `1` real file (`.ufo/waves/round-34/wave1/L1Integration.md`, 40 lines) — but **9** `L1Integration.md` copies carry it (the real one + 8 under `corpus/instruments/r35-fixtures/`) | `0` anywhere | `1` real + 8 fixtures | **SAT**, pre-satisfied | an unscoped repo-wide grep is fixture-shadowed (F4) |
| `supersedes R22` / `supersedes R23` in `corpus/QUALITY.md` (E7) | `1` / `1` (rows `R26` at `:249`, `R27` at `:250`, plus the round-35 supersession section `:231-250`) | `0` / `0` | `1` / `1` | **SAT**, pre-satisfied | discriminates against `3266c99` |
| round-36 lesson with the false-evidence correction (E8) | absent — no `corpus/lessons/round-36*.md`, no `.ufo/reports/round-36/`, `grep -ci 'round-36'` = 0 in `SCORECARD.md`/`SKILL.md`/`QUALITY.md`/`LOG.md` | absent | absent | **SAT**, open | the literal is evaluable; only the round-36 lesson can make it true |
| E9 quiescence | `git status --porcelain` = 9 paths at my read; scratch = 48 seat dirs at my read | — | — | **SAT**, open | live keys; the closing commit must absorb the wave scaffolding |

Every frozen literal is evaluable at base; none is unsatisfiable **as written**, and two require an
explicit scope (F1, F4) to stay meaningful.

## 5. Findings for the C1 suite author (advisory, no lane write)

- **F1 — `<LANE_HASH>` must be `SCORECARD.md`-scoped.** Base repo-wide: 502 lines / 89 files (`.ufo/waves`
  490 lines; outside it `LOG.md` 2, five `corpus/lessons/round-*.md`, and `corpus/instruments/
  r35-defect-closure.sh` comment text). A tree-wide E1 token check is unsatisfiable and would be red at
  every head, including the final one.
- **F2 — `201.2` alone is vacuous for E2 at the round-36 base.** It is already 8 occurrences / 6 lines at
  `cc69200`; five of the six lines are round-35 rows (`:1269` no-harm row, `:1307` measurement-state,
  `:1312` C1 row ×2, `:1314` depth:density row ×2). A check that keys only on the number stays green
  after the erratum sentence and the stale-row marker are deleted. Bind `Erratum (round 35)` +
  `round-34 depth:density row` + the `201.7`→`201.2` pair (all three are 1/1/… at base and 0/0 at
  `3266c99`).
- **F3 — the Final-lane-commit hash is a next-line token, and the older label lines carry other hashes
  inline.** At base `:987` carries `690b69da…` and `9f98488…` *before* the `**Final lane commit:` token,
  with the real hash (`7963976e…`) on `:988`; `:1129`/`:1130` split the same way. Four 40-hex tokens are
  involved and all four are ancestors of base, so ancestry alone cannot separate them: E1 should bind the
  round-36 section, require exactly one label there, resolve the hash to the first 40-hex token at or
  immediately after the token, and then test existence + ancestry. Also match the sibling spelling the
  round-35 spot-check recorded (`the L1 fills this line`) — at `3266c99` `filled by the L1` = 1 **and**
  `fills this line` = 1 on `:1129`, and at base both are 0.
- **F4 — E6 is fixture-shadowed.** `Correction (round 35)` appears in 9 `L1Integration.md` files at base:
  the real `.ufo/waves/round-34/wave1/L1Integration.md` plus 8 under `corpus/instruments/r35-fixtures/`
  (`clean`, `D1`, `D2`, `D3`, `D4`, `D5`, `D7`, `two-defect/D1D2`). Pin the path (or exclude
  `corpus/instruments/r35-fixtures/`) or the check cannot fail when the real file loses the text.
- **F5 — E4's two limbs are not in the same state at base.** round-35 results are tracked (`1`) but have
  no provenance note (`0`), while the round-34 pair is `1`/`1`. E4 is therefore a single-limb gain;
  report it as such rather than as "results not tracked". At the judged head `0aee0ef` both round-35
  limbs read `0`, so E4 also discriminates against the r35-head negative control.
- **F6 — two before-control keys are not base properties.** `worktree_clean=0` is only derivable (the
  freeze commit's four added paths were untracked at capture), and `scratch_leftovers=0` was true only
  because `/fast/scratch/hyaku/kasegi-r36` did not exist yet (48 seat dirs at my read). If E9 is scored
  from these keys, state them as live readings at filing, not as replayable base values. Separately,
  `junk_present=1` in `c2-controls/before.txt` cannot be the round-36 twin (absent at base, still absent
  at my read); either it means "a committed c2 junk twin exists in the lineage"
  (`.ufo/waves/round-35/c2-controls/junk-f18.md`) or the value was taken from an uncommitted tree. The
  L1 should pin the definition when E9/the junk control is scored.

## 6. Verification performed / not performed

Performed: three `git archive` exports (base, r35 base, r35 judged head) and every frozen counting
command run inside the base export; the two live keys re-derived with their evidence; the 15-literal
satisfiability battery run on all three refs; `git ls-tree`/`cat-file -e`/`merge-base --is-ancestor` on
the four `Final lane commit:` hashes plus the label-adjacent tokens; blob/sha256 binding of eight files;
`frontier-recheck-count.py` run twice at base (`entries=21 pass=21 exit=0`).

Not performed, deliberately: no build/lint/test/suite run (the C1 suite does not exist yet and the parent
owns the gate); no write inside the lane repo other than this receipt; no mutating git; no pacman; no
tool install; no subagent dispatch; no labrat probe (nothing external was needed).

Evidence: scratch `/fast/scratch/hyaku/kasegi-r36/ExecRegressionBase/` held `base/`, `r35base/`,
`r35head/` (the three exports), `measure.sh` (the literal battery over the three trees, reproduced in
§4). The directory is removed after this receipt was written, leaving no
`/fast/scratch/hyaku/kasegi-r36/ExecRegressionBase/` residue.

## Report

Item result: **the c1 before-controls replay 7/7 MATCH** (two of them labelled *derived*: `worktree_clean`,
`scratch_leftovers`) and **the c2 before-controls replay 6/7 MATCH, 1 DIFF** (`junk_present=1` is not
reproducible from committed base bytes — F6). All frozen `claims.json` literals are evaluable at base;
none is unsatisfiable as frozen, but E1 (`<LANE_HASH>`) and E6 (`Correction (round 35)`) are only
meaningful when scoped, E2's bare `201.2` literal is already true at the round-36 base and needs the
erratum anchor, and E4 is a single-limb gain at base (tracked=1, provenance=0). No lane file was written
except this receipt; no tooling was installed.
