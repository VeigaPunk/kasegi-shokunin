# K72Connector — sibling-overlap scan, round 72 attempt 1

Read-only scan. No writes into the lane tree, no mutating git/jj, no fetches.

## (1) Sibling `bugzilla` hit table

Siblings scanned: every `*-shokunin` under `/home/vgpnk/Projects/shokunin/` (21 repos).
For each: `corpus/knowledge/` (all files, case-insensitive), `corpus/README.md`, `corpus/SOURCES.md`.
Method: `grep -ril 'bugzilla' corpus/knowledge/` then per-file `grep -n -i 'bugzilla'`; same for README/SOURCES.

| repo | path | line | term |
|---|---|---|---|
| kasegi-shokunin | corpus/SOURCES.md | 211 | Bugzilla (in a round-43 advisory-screening record: "43 per-CVE entries … 0 Description or Severity lines … Bugzilla id" — a *rejected* candidate's field list, not a Bugzilla source) |

All other 20 sibling repos: **zero** `bugzilla` hits in `corpus/knowledge/`, `corpus/README.md`, `corpus/SOURCES.md`.
No sibling holds a Bugzilla source, entry, or frontier row. The only lane-internal hit is the kasegi
SOURCES.md:211 mention, which is a rejected-candidate field description inside a round-43 search-log
sentence, not an admitted Bugzilla artifact.

## (2) S107 registry collisions

`grep -n 'S107' kasegi-shokunin/corpus/SOURCES.md` → **no output (exit 1)**. The lane registry tops at
S106 (round-71); S107 is unassigned in this lane and is exactly the id C2 claims.

Sibling `S107` uses (each sibling numbers its own registry; collisions are per-lane facts, not defects):

| repo | SOURCES.md line(s) | S107 subject |
|---|---|---|
| chousa-shokunin | 117, 238, 391 | システマティックレビューの基礎 (J-Stage article) |
| kaidoku-shokunin | 113, 117(S111 ref) | onekey-sec/sasquatch release sasquatch-v4.5.1-6 |
| kake-shokunin | 115, 121(S113 ref) | W3C XML Schema 1.1 Part 2 Datatypes |
| kama-shokunin | 119, 144(S132 ref), 643 | llama.cpp src/llama-context.cpp @ 704366d76 |
| kengaku-shokunin | 122 | Terminal-Bench 2.0 protein-assembly task instruction |
| kotoba-shokunin | 119 | Gemini CLI GEMINI.md docs |
| kotodama-shokunin | 136 | Glottolog 5.3 BANZSL family node |
| kumitate-shokunin | 120, 245, 324, 326 | RabbitMQ 4.4 consumer acknowledgements docs |
| mado-shokunin | 119, 126(S114 ref) | CPython 3.14.8 shlex reference |
| mori-shokunin | 113 | omp docs subagents/settings/tools pages |
| revenger-shokunin | 122, 522 | Agentic Binary Reverse Engineering survey |
| souji-shokunin | 142, 143(S108), 310, 312 | Python RecursionError docs |
| tabi-shokunin | 121 | RFC 9110 HTTP Semantics |
| tameshi-shokunin | 119, 143(S268) | TensorFlow Federated golden testing docs |
| tsukuroi-shokunin | 113 | pacman refresh/cache-clean man page |

Repos with **no** S107 row: audio, game-dev-2d, game-dev-3d, kagi, kasegi (this lane), lore.
None of the sibling S107 subjects is Bugzilla-related; no cross-lane subject collision with C2's
Bugzilla REST API claim.

## (3) `considerthese/` and `merge/` unimplemented-proposal check

- `considerthese/` exists at lane root with 8 dated files (2026-10-19 … 2026-10-26). Precise scan for
  `bugzilla|bug tracker|issue tracker|bug report|bug-report|rest interface|REST API` (case-insensitive):
  **zero hits**. Earlier loose `bug` hits were all "Bugcrowd"/severity-lens carry-overs, unrelated.
- No `merge/` directory exists anywhere under the lane (checked `kasegi-shokunin/merge`,
  `kasegi-shokunin/corpus/merge`, and `find -maxdepth 2 -name merge` across all 21 siblings): **none**.

Finding: **no unimplemented Bugzilla / bug-tracker / bug-report-REST proposal** is pending in the lane.

## (4) QUALITY.md criteria the F50 entry must meet, not already named in r70/r71 lessons

F50 is a frontier admission: it lands a `corpus/knowledge/*.md` entry (Q1–Q10 apply), a SOURCES.md
registry row (R8/R100/R102/R104 apply), a README frontier row, and a `corpus/source-snapshots/round-72/`
capture with manifest (R20/R21 apply). The r70/r71 lessons name R102, R104, R105, R108, R111, R113,
R114, R56/R64/R65/R67/R69 in their C2 sections. Criteria in QUALITY.md that bind this entry and are
**not** named in the round-70 or round-71 lesson text:

| id | criterion (short) |
|---|---|
| Q1 | `source:`/`verified-at:`/`recheck:` header lines on the entry |
| Q2 | every load-bearing claim rests on ≥1 tier-A/B row opened this round |
| Q3 | verbatim ≤25-word quotes with exact located anchors |
| Q4 | attribution kept (Bugzilla's own policy, never generalized) |
| Q5 | ≥1 falsifiable rule + ≥1 rejected over-generalization |
| Q6 | documentation-only; no probing/submission instructions |
| Q7 | executable `recheck:` command, fail-closed on missing source |
| Q8 | captured-source comparison under declared normalization |
| Q9 | quote exactly-once in capture or carries verified `anchor` line |
| Q10 | `recheck:` is one `bash -n`-parseable command with `cd <lane-root> &&` prefix |
| R8 | new registry row for any corrected/superseded anchor (S107 is new, not superseding) |
| R20 | capture snapshot ships `manifest.json` in the same commit; `url` + `fetched_utc` per record |
| R21 | manifest carries url + fetch instant so fabrication is separable |
| R12 | the entry's `recheck:` `--source` ids must cover its header `source:` ids and be cited |

Most load-bearing for F50 specifically: **Q3/Q9** (every quote located in S107.txt), **Q10/R12**
(recheck line form and source coverage), **R20/R21** (manifest + provenance in the same commit),
**R114** (subject sweep — Bugzilla vs the lane's existing tracker/disclosure entries F27/F28/F40/F49).

## (5) Strongest measurable C1↔C2 cross-claim connection

`frontier-recheck-count.py` and `capture-binding-check.py` — two of C2's four counter instruments —
are themselves heads inside the `figure-audit.py` gate that C1 repairs (`figure-audit.py:151,163,175,185`
name them in the python-head tables; `:806-808` are the new `--work`/`--scratch` selftest cases), so
the C1 realpath-basename policy change directly re-adjudicates whether C2's own counter commands are
admitted as read-only derives — one line: *C1's gate is the admission oracle for the instruments C2's
counters invoke.*

## Notes

- No tool installs were needed; no RULES.md-gated action taken.
- Scratch dir `/fast/scratch/hyaku/kasegi-r72/K72Connector/` was created and is empty of cited
  artifacts (all findings are read-only greps/reads; nothing citable was staged there).
