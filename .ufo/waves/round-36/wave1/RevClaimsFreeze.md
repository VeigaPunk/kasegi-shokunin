# RevClaimsFreeze — round-36 claims-freeze review (base cc692008)

Seat: RevClaimsFreeze (reviewer, leaf). Route: L1 KasegiR36, inline spawn handoff, hyaku run 9.
Reviewed object: `.ufo/waves/round-36/claims.json` as frozen at b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6 (single commit directly on base cc692008b0cfd58d18275aa6c4aed79620120799). Method: every literal constant in the C1/C2 predicates, kill rules, and counting commands was executed against a `git archive cc692008` export in scratch; no lane file was edited; all git use read-only.

## Sanity of the freeze object itself

- claims.json is tracked at b47f2cd and the committed blob is byte-identical to the worktree copy (`git show b47f2cd:.ufo/... | diff -q -` clean).
- Base contains zero `round-36` paths (`git ls-tree -r cc692008 | grep -c round-36` = 0) — the freeze commit introduces the claims, nothing else round-36.
- Cited r35 export refs resolve and are ancestors of base: 3266c993… (r35 base) and 0aee0ef1… (r35 judged head) both `cat-file -e` OK, both `merge-base --is-ancestor` OK. The C1 counting commands are runnable as written.

## Satisfy/fail table — literal constants vs base tree

| # | Constant (claim, scope) | Base expectation | Observed | Verdict |
|---|---|---|---|---|
| 1 | `filled by the L1` in SCORECARD.md (C1 kill-rule form) | 0 | 0 | SATISFIED |
| 2 | `<LANE_HASH>` in SCORECARD.md (E1) | 0 | 0 | SATISFIED |
| 3 | `201.2` (E2; canonical target per r35 instrument line 179: `grep -c -F -- '201.2' SCORECARD.md`) | >=1 | 6 | SATISFIED |
| 4 | `Correction (round 35)` in .ufo/waves/round-34/wave1/L1Integration.md (E6) | >=1 | 1 | SATISFIED |
| 5 | `supersedes R22` / `supersedes R23` in corpus/QUALITY.md (E7) | >=1 each | 1 / 1 | SATISFIED |
| 6 | round-35 wave1-results.json tracked (E4) | tracked | tracked at cc692008; 25 provenance-related lines in file | SATISFIED |
| 7 | .ufo/waves/round-35/claims-erratum-d5.md (E5) | present | present | SATISFIED |
| 8 | SKILL.md rows matching `r36-closure` (E3) | 0 | 0 | SATISFIED |
| 9 | SKILL.md exact-basename row `r35-defect-closure.sh` (E3) | 0 | 0 (file exists at corpus/instruments/, registry row absent) | SATISFIED |
| 10 | corpus/instruments/r36-closure.sh (suite) | missing (ls exit 2) | absent, ls exit 2 | SATISFIED |
| 11 | E1 form: Final lane commit hash exists and is ancestor | yes | 7963976e… and c1c6a5f8… (the two Final-lane-commit lines at base) both exist and are ancestors of base | SATISFIED |
| 12 | frontier rows `^\| F[0-9]+ \|` in corpus/README.md | 18 | 18 | SATISFIED |
| 13 | registry rows `^\|\s*S[0-9]{3,}\s*\|` in corpus/SOURCES.md | 52 | 52 | SATISFIED |
| 14 | `S053` in corpus/SOURCES.md | 0 | 0 | SATISFIED |
| 15 | knowledge files matching `^source: S053 ` | 0 | 0 | SATISFIED |
| 16 | `ls corpus/knowledge/*.md \| wc -l` | 47 | 47 | SATISFIED |
| 17 | F19 row in corpus/README.md | 0 | 0 | SATISFIED |
| 18 | harness `frontier-recheck-count.py` at base | entries=21 pass=21 exit 0 | entries=21 pass=21 exit=0 (run inside base export) | SATISFIED |
| 19 | c2-controls/junk-f19.md | absent | absent (0 hits anywhere in tree) | SATISFIED |
| 20 | corpus/source-snapshots/round-36/manifest.json | absent | absent (snapshots hold round-23..35 only) | SATISFIED |
| 21 | corpus/knowledge/epss-exploit-prediction-scoring.md | absent | absent | SATISFIED |
| 22 | claims.json blob == worktree at freeze commit | equal | equal | SATISFIED |

24/24 satisfiable at base. Zero constants contradict the base tree.

## Do-nothing control — targets unreachable at base

Every after-target misses on the untouched base, so no arm of either kill rule can be met without the claimed work:

| Target (after-value) | Base observation | Met? |
|---|---|---|
| frontier = 19 | 18 | missed |
| registry = 53 | 52 | missed |
| S053 row / citing entry | 0 / 0 | missed |
| knowledge = 48 | 47 | missed |
| harness entries=22 pass=22 | entries=21 pass=21 | missed |
| r36-closure.sh present, closed=9/9 | absent, ls exit 2 (kill arm fires) | missed |
| SKILL.md registry rows for both basenames | 0 rows | missed |
| source-recheck S053 exit 0 | exit 2 (round-36 manifest absent) | missed |
| capture-binding exit 0 | exit 0, but vacuous — see Finding 1 | vacuous pass |
| junk-f19 built and rejected | control not built | missed |
| round-36 capture + manifest committed | absent | missed |

The freeze therefore discriminates: a do-nothing lane fails C1 (suite missing) and fails C2 on at least five independent arms. Verdict: **freeze OK**.

## Findings

1. LOW (calibration, C2): `capture-binding-check.py` exits 0 at base although the round-36 capture/manifest is absent. The instrument (892 lines; docstring: "walks every snapshot directory under corpus/source-snapshots/") audits only directories that exist, so it detects *unbound*, never *absent*. The kill rule's phrase "capture/manifest absent or unbound (capture-binding-check)" over-credits this one instrument for the absent half. Non-blocking: the composite kill rule still kills do-nothing via `source-recheck --manifest …/round-36/manifest.json` (exit 2 at base) and the harness counter.
2. NOTE (C1 execution constraint): placeholder tokens exist at base outside the top-level files — 44 files match `filled by the L1` and 89 match `<LANE_HASH>` tree-wide, including .ufo/waves history, corpus/lessons/round-3{3,4,5}*.md, LOG.md, SHONEN.md, considerthese/2026-10-26.md, and the corpus/instruments/r35-fixtures/ mutant trees (10 and 7 files respectively outside .ufo/waves). Top-level SCORECARD.md is clean on both greps. r36-closure.sh's E1 must scope its placeholder grep the way the kill rule does (top-level files) or exclude fixtures/history, otherwise closed=9/9 is unreachable on any real export.
3. NOTE (E1 line selection): base SCORECARD.md carries two `**Final lane commit:` lines (round-33 section, hash 7963976e…; round-34 section, hash c1c6a5f8…). Both bind cleanly at base (exist + ancestor), so the E1 predicate form is satisfiable; at the final head, E1 must select the round-36 section's line (the newest), not the first match.
4. INFO: current worktree shows 9 porcelain lines, all round-36 wave apparatus (.ufo/waves/round-36/wave1/*, dispatch/spec files) — in-flight seat receipts, not base violations. E9 quiescence remains a filing-time target and must be re-checked at filing.

## Residual risk and verification gaps

- E8 (round-36 lesson false-evidence correction), E9 (quiescence), and every `closed=…` run of r36-closure.sh are filing-time targets over a head that does not exist yet; not verifiable at freeze time and out of this review's scope. The freeze itself places no unsatisfiable constant on the base.
- Scratch-leftover state at base instant was not retroactively observable; current /fast/scratch/hyaku/kasegi-r36 holds in-flight seat dirs, consistent with mid-wave.
- Tools: none installed (bash/git/python3 already present; pacman untouched per host pause). Scratch /fast/scratch/hyaku/kasegi-r36/RevClaimsFreeze removed after this receipt was written.
