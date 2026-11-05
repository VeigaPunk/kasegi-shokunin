# ReviewC2 — C2 re-measure at committed tip (round 71, wave 1)

Verdict: **C2: NOT VERIFIED** — five of the frozen after-values do not reproduce from the
landed commit `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60` (lane HEAD, also `origin/master`).
Each failing value reproduces the **before** value instead: the corpus integration half of C2
(registry row S106, knowledge entry, README F49 row, knowledge-expected lines) is absent from
the commit and from the working tree. The capture half (S106.txt, manifest.json, records=85)
did land.

## Method

Committed bytes only, extracted from the tip into scratch:
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60 | tar -x -C /fast/scratch/hyaku/kasegi-r71/ReviewC2/extract`
(→ `EXTRACTED`). Plain grep/ls/wc/sort/python counts over the extracted tree; no lane
instrument was run for the counts. `git rev-parse HEAD` → `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`.

## Count table — frozen after_values vs measured at tip

| # | Value | Frozen after | Measured | Delta | Matches before? |
|---|---|---|---|---|---|
| 1 | SOURCES.md registry rows | 106 | **105** | −1 | yes (before=105) |
| 2 | corpus/knowledge/*.md files | 87 | **86** | −1 | yes (before=86) |
| 3 | README.md frontier rows | 49 | **48** | −1 | yes (before=48) |
| 4 | knowledge-expected.txt lines | 89 | **88** | −1 | yes (before=88) |
| 5 | knowledge-expected.txt entries (non-#) | 87 | **86** | −1 | yes (before=86) |
| 6 | `LC_ALL=C sort -c` exit | 0 | **0** | — | — |
| 7 | summed sources[] / manifest dirs | 85 / 44 | **85 / 44** | 0 | after ✓ |
| 8 | S106.txt sha256 | 291f36c2…f59db | **291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db** | match | after ✓ |

## MEASURED commands and observed output

1. `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `105`
   (re-confirmed on the committed blob directly: `git show 4e33119:corpus/SOURCES.md | grep -cE …` → `105`;
   working-tree file also `105`)
2. `ls corpus/knowledge/*.md | wc -l` → `86`
3. `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `48`
4. `wc -l < corpus/instruments/knowledge-expected.txt` → `88`
5. `grep -vc '^#' corpus/instruments/knowledge-expected.txt` → `86`
6. `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt; echo sort_exit=$?` → `sort_exit=0`
7. python3 over `corpus/source-snapshots/**/manifest.json` (glob, `len(json['sources'])` summed) → `dirs=44 sources_sum=85`
8. `sha256sum corpus/source-snapshots/round-71/S106.txt` → `291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db`;
   `wc -l -c < …S106.txt` → `148 15004` (both match the frozen capture constants)

## Why the five failures are real absences, not pattern misses

- `grep -n 'S106' corpus/SOURCES.md` → no match (rc=1). Highest registry id at tip: `S105`
  (`grep -oE '^\|[[:space:]]*S[0-9]{3,}' … | sort | tail -2` → `S104`, `S105`).
- `grep -rln 'F49' corpus/` (recursive, whole extracted corpus) → **no file matches**; F49
  appears nowhere at the tip. Highest frontier row: `F48`.
- `grep -n 'zdi' corpus/instruments/knowledge-expected.txt` → single line `88:corpus/knowledge/zdi-disclosure-policy.md`
  (the pre-existing entry). The claimed new entry
  `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` does not exist; `ls corpus/knowledge/ | grep -i zdi` → `zdi-disclosure-policy.md` only.
- `grep -rln 'S106' corpus/` → only `corpus/source-snapshots/round-71/manifest.json` cites
  S106. No knowledge entry, no README row, no SOURCES row references it.

## Row-shape checks — UNMEASURABLE

The F49 row does not exist at the tip, so none of the row-shape items can be measured:
11 cells, tier `A`, status `mined`, `used-by` → existing file citing S106, `opened 2026-11-05` —
all fail by absence (no row to inspect; no entry file exists to be the used-by target).

## Commit scope confirms the split

`git show 4e33119 --stat` → exactly 4 files:
`.ufo/waves/round-71/controls/c1-candidate-trial-r71.txt`, `corpus/instruments/figure-audit.py`,
`corpus/source-snapshots/round-71/S106.txt`, `corpus/source-snapshots/round-71/manifest.json`.
The commit never touches `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`,
or `corpus/instruments/knowledge-expected.txt`.

`git status --porcelain` (working tree) → ` M corpus/QUALITY.md` plus untracked
`.ufo/waves/round-71/*` only: no pending corpus integration. A commit `b6d3d99`
(QUALITY.md +1 line, 22:31:30 −03) is reachable from no branch (`git branch -a --contains` →
empty) and touches nothing else. `git log origin/master --oneline -3` tops out at `4e33119`.
No ref I could reach carries the missing integration.

## What did land (capture half, verified)

- `round-71/manifest.json`: `sources[]` = 1 entry, `id=S106`,
  `url=https://www.zerodayinitiative.com/about/`, **15 quotes**, every quote an object with
  `id`/`quote`/`anchor` and an integer `anchor` (`all_have_int_anchor= True n= 15`) — satisfies
  the "≥8 pinned located quotes" limb of the sourced claim for the capture artifact.
- S106.txt contains the claimed subject matter (counts ≥1 each for `120` (day window),
  `15 business` (days), `monetary|payment` (acquisition flow)).
- Global manifest sum 85 over 44 dirs equals the frozen after value (84+1 from this capture).

## Kill-rule application

C2 kill rule: "Any frozen after-value that does not reproduce from the landed commit defeats
C2; the census must exit 0 at round end." Five frozen after-values (rows #1–#5) do not
reproduce — all five sit at their before values. The census/entry/frontier integration half of
C2 is not landed. **C2: NOT VERIFIED** — missing: registry row S106 in corpus/SOURCES.md,
`corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`, the F49 row in
corpus/README.md, and the two knowledge-expected.txt additions (89/87).

Residual risk: none for the measurements (plain counts over committed bytes, cross-checked
blob-direct and in the working tree). I did not run the lane census/binding instruments (per
seat scope), so instrument-level verdicts (`frontier-recheck-count`, `capture-binding-check`,
sources-census.sh) remain L1's to run — at this tip they cannot reach the frozen after values
given the underlying file counts above.

Scratch `/fast/scratch/hyaku/kasegi-r71/ReviewC2/` removed after writing this report.
